from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ast
import subprocess
import tempfile
import json
import os

app = FastAPI()

# Simple, permissive CORS (what you had earlier)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str


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

        # THIS IS THE VERSION YOU HAD WORKING
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


@app.get("/")
def root():
    return {"status": "ok", "message": "CTT backend is running"}


@app.post("/flow")
def analyze_code(req: CodeRequest):
    functions = extract_functions(req.code)
    graph = generate_call_graph(req.code)

    return {
        "functions": functions,
        "graph": graph,
    }
