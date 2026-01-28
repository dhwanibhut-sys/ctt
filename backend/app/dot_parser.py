import re


def clean_label(label: str) -> str:
    """
    Convert labels like:
    '0: (global)()' -> '(global)'
    '1: add()'      -> 'add'
    """
    # Remove index prefix if present
    if ":" in label:
        label = label.split(":", 1)[1]

    # Remove parentheses
    label = label.replace("()", "").strip()
    return label


def parse_dot(dot: str):
    id_to_label = {}
    raw_edges = []

    # Matches node definitions like:
    # "node_xxx" [label="1: add()", shape=box];
    node_pattern = re.compile(
        r'"?([\w\d_]+)"?\s*\[.*label="([^"]+)".*\]'
    )

    # Matches edges like:
    # "node_xxx" -> "node_yyy";
    edge_pattern = re.compile(
        r'"?([\w\d_]+)"?\s*->\s*"?([\w\d_]+)"?'
    )

    # ---------- PASS 1: extract node labels ----------
    for line in dot.splitlines():
        node_match = node_pattern.search(line)
        if node_match:
            node_id, label = node_match.groups()
            id_to_label[node_id] = label

    # ---------- PASS 2: extract edges ----------
    for line in dot.splitlines():
        edge_match = edge_pattern.search(line)
        if edge_match:
            src_id, dst_id = edge_match.groups()
            raw_edges.append((src_id, dst_id))

    # ---------- BUILD CLEAN NODES ----------
    nodes = []
    seen = set()

    for label in id_to_label.values():
        clean = clean_label(label)
        if clean not in seen:
            seen.add(clean)
            nodes.append({
                "id": clean,
                "type": "function"
            })

    # ---------- BUILD CLEAN EDGES ----------
    edges = []

    for src_id, dst_id in raw_edges:
        src_label = clean_label(id_to_label.get(src_id, src_id))
        dst_label = clean_label(id_to_label.get(dst_id, dst_id))

        edges.append({
            "from": src_label,
            "to": dst_label
        })

    return {
        "nodes": nodes,
        "edges": edges
    }
