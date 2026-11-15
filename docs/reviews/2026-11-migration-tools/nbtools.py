"""Build notebooks from a compact spec and print executed outputs for checking notes.

Spec format: a string where cells are separated by lines '%% md', '%% code' or '%% solution'.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path("/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/review")
OUT = Path("/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/executed")


def parse(spec: str) -> list[dict]:
    cells, kind, buf = [], None, []

    def flush():
        if kind is None:
            return
        text = "\n".join(buf).strip("\n")
        if kind == "md":
            cells.append({"cell_type": "markdown", "metadata": {}, "source": text})
        else:
            meta = {"tags": ["solution"]} if kind == "solution" else {}
            cells.append({"cell_type": "code", "metadata": meta, "source": text, "outputs": [], "execution_count": None})

    for line in spec.splitlines():
        if line.startswith("%% "):
            flush()
            kind, buf = line[3:].strip(), []
        else:
            buf.append(line)
    flush()
    return cells


def build(relpath: str, spec: str) -> Path:
    path = REPO / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = {"cells": parse(spec), "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    path.write_text(json.dumps(nb, indent=1))
    subprocess.run(["uv", "run", "--no-project", "python", "scripts/notebook_format.py", str(path.relative_to(REPO))], cwd=REPO, check=True, capture_output=True)
    return path


def run(relpath: str, show: bool = True, limit: int = 1500) -> bool:
    import os
    env = {**os.environ, "JAVA_HOME": "/opt/homebrew/opt/openjdk@17", "PATH": "/opt/homebrew/opt/openjdk@17/bin:" + os.environ["PATH"]}
    r = subprocess.run(["uv", "run", "--extra", "notebooks", "python", "scripts/run_notebooks.py", "--output-dir", str(OUT), relpath],
                       cwd=REPO, capture_output=True, text=True, env=env)
    ok = r.returncode == 0
    if not ok:
        print(r.stdout[-4000:], r.stderr[-6000:])
        return False
    if show:
        nb = json.loads((OUT / relpath).read_text())
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] != "code":
                continue
            text = ""
            for o in c.get("outputs", []):
                if "text" in o:
                    text += "".join(o["text"])
                elif "data" in o and "text/plain" in o["data"]:
                    text += "".join(o["data"]["text/plain"])
            print(f"--[{i}]\n{text[:limit]}")
    return ok


if __name__ == "__main__":
    run(sys.argv[1], limit=int(sys.argv[2]) if len(sys.argv) > 2 else 1500)
