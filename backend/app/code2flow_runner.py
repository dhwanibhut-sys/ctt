import subprocess
import uuid
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
CODE2FLOW_EXE = os.path.join(BASE_DIR, "venv", "Scripts", "code2flow.exe")

def run_code2flow(code: str) -> str:
    file_id = str(uuid.uuid4())
    py_file = os.path.join(TEMP_DIR, f"{file_id}.py")
    dot_file = os.path.join(TEMP_DIR, f"{file_id}.dot")

    with open(py_file, "w", encoding="utf-8") as f:
        f.write(code)

    cmd = [
        CODE2FLOW_EXE,
        py_file,
        "--language", "py",
        "--output", dot_file
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # Return empty dot graph if code2flow fails
        return "digraph G { }"

    with open(dot_file, "r", encoding="utf-8") as f:
        return f.read()
