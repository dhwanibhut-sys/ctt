from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.code2flow_runner import run_code2flow
from app.dot_parser import parse_dot
from app.ast_parser import extract_functions

app = FastAPI()
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CTT backend is running"
    }


# ✅ Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

@app.post("/flow")
def analyze_code(data: CodeInput):
    dot_graph = run_code2flow(data.code)
    graph = parse_dot(dot_graph)
    functions = extract_functions(data.code)

    return {
        "functions": functions,
        "graph": graph
    }