from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ast
import tempfile
import subprocess
import json
import os

app = FastAPI(
    title="CTT Backend",
    description="Static Python code analysis and call graph generation",
    version="1.0.0",
)

# ✅ CORS — PUBLIC API (works on mobile + desktop)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all origins
    allow_credentials=False,      # MUST be False with "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------

class CodeRequest(BaseModel):
    code: str


# ---------- Utilities ----------

def extract_functions(code: str):
    tree = ast.parse(code)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "lineno": node.lineno,
            })

    return functions


def generate_call_graph(code: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, "input.py")
        output_path = os.path.join(tmpdir, "flow.json")

        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code)

        # Run code2flow
        subprocess.run(
            [
                "code2flow",
                code_path,
                "--language",
                "py",
                "--output",
                output_path,
                "--format",
                "json",
            ],
            check=True,
        )

        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    nodes = []
    edges = []

    for node_id, node_data in data.get("nodes", {}).items():
        label = node_data.get("label", node_id)
        nodes.append({
            "id": label,
            "type": "function",
        })

    for edge in data.get("edges", []):
        edges.append({
            "from": edge["source"],
            "to": edge["target"],
        })

    return {
        "nodes": nodes,
        "edges": edges,
    }


# ---------- Routes ----------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CTT backend is running"
    }


@app.post("/flow")
def analyze_code(req: CodeRequest):
    try:
        functions = extract_functions(req.code)
        graph = generate_call_graph(req.code)

        return {
            "functions": functions,
            "graph": graph,
        }

    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Syntax error: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
