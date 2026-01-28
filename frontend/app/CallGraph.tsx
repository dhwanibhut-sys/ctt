"use client";

import ReactFlow, {
  Background,
  Controls,
  MarkerType,
} from "reactflow";
import dagre from "dagre";
import "reactflow/dist/style.css";

type Edge = {
  from: string;
  to: string;
};

type Props = {
  edges: Edge[];
  onNodeClick?: (node: string) => void;
};

const nodeWidth = 160;
const nodeHeight = 60;

export default function CallGraph({ edges, onNodeClick }: Props) {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: "TB", nodesep: 50, ranksep: 70 });

  const nodesSet = new Set(edges.flatMap(e => [e.from, e.to]));

  nodesSet.forEach((n) => {
    g.setNode(n, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((e) => {
    g.setEdge(e.from, e.to);
  });

  dagre.layout(g);

  const nodes = Array.from(nodesSet).map((name) => {
    const { x, y } = g.node(name);
    return {
      id: name,
      data: { label: name },
      position: { x: x - nodeWidth / 2, y: y - nodeHeight / 2 },
      style: {
        background: "#fdf2f8",
        border: "2px solid #ec4899",
        borderRadius: 12,
        color: "#9d174d",
        fontWeight: 600,
        cursor: "pointer",
        padding: 12,
        boxShadow: "0 6px 14px rgba(236,72,153,0.25)",
      },
    };
  });

  const flowEdges = edges.map((e, i) => ({
    id: `e-${i}`,
    source: e.from,
    target: e.to,
    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: "#ec4899",
    },
    animated: true,
    style: {
      stroke: "#ec4899",
      strokeWidth: 2,
    },
  }));

  return (
    <div className="w-full h-[340px] rounded-xl border border-pink-200 bg-white">
      <ReactFlow
        nodes={nodes}
        edges={flowEdges}
        fitView
        onNodeClick={(_, node) => onNodeClick?.(node.id)}
      >
        <Background color="#fbcfe8" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
