"use client";

import { useState } from "react";
import CallGraph from "./CallGraph";



export default function Home() {
  const [selectedFn, setSelectedFn] = useState<any>(null);

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function analyzeCode() {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("https://ctt-z2mq.onrender.com/flow", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ code }),
});


      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Backend not connected");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-pink-50 px-6 py-10">
      {/* HEADER */}
      <div className="max-w-5xl mx-auto mb-8">
        <h1 className="text-4xl font-bold text-pink-700 mb-2">
          Python Code Analyzer
        </h1>
        <p className="text-pink-600">
          Analyze Python functions and call flow using AST + static analysis
        </p>
      </div>

      {/* INPUT */}
      <div className="max-w-5xl mx-auto bg-white rounded-xl shadow-md border border-pink-100 p-6 mb-8">
        <label className="block text-sm font-medium text-pink-700 mb-2">
          Paste Python code
        </label>

        <textarea
          className="w-full h-44 p-4 border border-pink-300 rounded-lg font-mono text-sm text-gray-900 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-pink-500"
          placeholder={`def add(a, b):\n    return a + b\n\nx = add(2, 3)`}
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <div className="mt-4 flex items-center gap-4">
          <button
            onClick={analyzeCode}
            className="bg-pink-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-pink-700 transition"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {error && (
            <span className="text-sm text-red-500">{error}</span>
          )}
        </div>
      </div>

      {/* RESULTS */}
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* FUNCTIONS */}
        <div className="bg-white rounded-xl shadow-sm border border-pink-100 p-5">
          <h2 className="text-lg font-semibold text-pink-700 mb-3">
            Functions (AST)
          </h2>

          {!result && !loading && (
            <p className="text-sm text-gray-400">No analysis yet</p>
          )}

          {loading && (
            <p className="text-sm text-pink-500">
              Extracting functions…
            </p>
          )}

          {result?.functions?.length > 0 && (
            <ul className="text-sm space-y-2">
              {result.functions.map((fn: any, i: number) => (
                <li
                  key={i}
                  className="bg-pink-50 border border-pink-300 rounded-md px-3 py-2 text-gray-900"
                >
                  <span className="font-semibold">{fn.name}</span>
                  <span className="text-gray-700">
                    ({fn.args.join(", ")})
                  </span>
                  <span className="text-gray-500">
                    {" "}
                    — line {fn.lineno}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* CALL GRAPH (VISUAL) */}
        <div className="bg-white rounded-xl shadow-sm border border-pink-100 p-5">
          <h2 className="text-lg font-semibold text-pink-700 mb-3">
            Call Graph
          </h2>

          {!result && !loading && (
            <p className="text-sm text-gray-400">
              No graph generated
            </p>
          )}

          {loading && (
            <p className="text-sm text-pink-500">
              Building call graph…
            </p>
          )}

          {result?.graph?.edges?.length > 0 && (
           <CallGraph
  edges={result.graph.edges}
  onNodeClick={(name) => {
    const fn = result.functions.find((f: any) => f.name === name);
    setSelectedFn(fn || null);
  }}
  
/>

          )}
          {selectedFn && (
  <div className="mt-4 bg-pink-50 border border-pink-200 rounded-lg p-4">
    <h3 className="font-semibold text-pink-700 mb-1">
      Function Details
    </h3>
    <p className="text-sm text-gray-800">
      <b>Name:</b> {selectedFn.name}
    </p>
    <p className="text-sm text-gray-800">
      <b>Arguments:</b> {selectedFn.args.join(", ")}
    </p>
    <p className="text-sm text-gray-800">
      <b>Line:</b> {selectedFn.lineno}
    </p>
  </div>
)}

        </div>
      </div>
    </main>
  );
}
