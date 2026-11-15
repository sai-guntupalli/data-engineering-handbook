"""Mechanical migration of older lesson notebooks towards the house standard.

- setup cell: PACKAGES form -> two-line form
- '## Setup' -> '## Setup and sample data'
- learner asserts: dropped when the cell already shows the same query, otherwise turned into output
- returns a report of asserts it could not convert, for manual review
"""
import ast
import json
import re
import sys
from pathlib import Path


def src(cell):
    return "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]


def pip_spec(spec: str) -> str:
    name = re.split(r"[<>=!~\[]", spec)[0]
    extras = re.search(r"\[[^\]]+\]", spec)
    m = re.search(r">=\s*(\d+)\.(\d+)(?:\.\d+)?\s*,\s*<\s*(\d+)\.(\d+)", spec)
    base = name + (extras.group(0) if extras else "")
    if m and m.group(1) == m.group(3) and int(m.group(4)) == int(m.group(2)) + 1:
        return f"{base}~={m.group(1)}.{m.group(2)}.0"
    return base


def two_line_setup(cell_source: str) -> str | None:
    m = re.search(r"PACKAGES\s*=\s*(\{.*?\})", cell_source, re.S)
    if not m:
        return None
    packages = ast.literal_eval(m.group(1))
    specs = []
    for spec in packages.values():
        s = pip_spec(spec)
        if s not in specs:
            specs.append(s)
    return "# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).\n!pip install -q " + " ".join(specs)


def convert_asserts(code: str):
    """Return (new_code, unresolved) where unresolved lists assert sources needing a hand edit."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code, ["<syntax>"]
    lines = code.splitlines(keepends=True)
    edits = []  # (start, end, replacement)
    unresolved = []
    shown = set(re.findall(r"spark\.sql\((\w+)\)\.show\(", code))

    def sql_arg(node):
        # spark.sql(X).collect() -> X node
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"collect", "count", "first"}:
            inner = node.func.value
            if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Attribute) and inner.func.attr == "sql":
                return inner.args[0] if inner.args else None, node.func.attr
        return None, None

    for node in tree.body:
        if not isinstance(node, ast.Assert):
            continue
        start, end = node.lineno - 1, node.end_lineno
        indent = re.match(r"\s*", lines[start]).group(0)
        test = node.test
        replacement = None
        if isinstance(test, ast.Compare) and len(test.ops) == 1 and isinstance(test.ops[0], ast.Eq):
            arg, method = sql_arg(test.left)
            if arg is not None and method == "collect":
                if isinstance(arg, ast.Name) and arg.id in shown:
                    replacement = ""
                else:
                    text = ast.get_source_segment(code, arg)
                    replacement = f"{indent}spark.sql({text}).show()\n"
                    if isinstance(arg, ast.Name):
                        shown.add(arg.id)
        if replacement is None:
            unresolved.append(ast.get_source_segment(code, node))
            continue
        edits.append((start, end, replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        lines[start:end] = [replacement] if replacement else []
    new = "".join(lines)
    new = re.sub(r"\n{3,}", "\n\n", new).strip("\n")
    return new, unresolved


def migrate(path: Path, dry=False):
    nb = json.loads(path.read_text())
    report = []
    for i, cell in enumerate(nb["cells"]):
        s = src(cell)
        if cell["cell_type"] == "code":
            if "PACKAGES" in s:
                new = two_line_setup(s)
                if new:
                    cell["source"] = new
                continue
            if "solution" in cell.get("metadata", {}).get("tags", []):
                continue
            if re.search(r"^\s*assert\b", s, re.M):
                new, unresolved = convert_asserts(s)
                cell["source"] = new
                for u in unresolved:
                    report.append((i, u))
        else:
            if re.match(r"## Setup\s*$", s.split("\n")[0]):
                cell["source"] = "## Setup and sample data" + s[len(s.split("\n")[0]):]
    if not dry:
        path.write_text(json.dumps(nb, indent=1) + "\n")
    return report


if __name__ == "__main__":
    for p in sys.argv[1:]:
        rep = migrate(Path(p))
        print(f"== {p}: {len(rep)} unresolved")
        for i, u in rep:
            print(f"  [{i}] {u[:160]!r}")


def finish_asserts(code: str):
    """Second pass: delete asserts that re-check something the cell already shows; print the rest."""
    tree = ast.parse(code)
    lines = code.splitlines(keepends=True)
    edits, left_over = [], []
    printed = " ".join(re.findall(r"print\((.*)\)", code))
    for node in tree.body:
        if not isinstance(node, ast.Assert):
            continue
        start, end = node.lineno - 1, node.end_lineno
        test = node.test
        replacement = None
        if isinstance(test, ast.Name):
            replacement = ""
        elif isinstance(test, ast.Compare) and len(test.ops) == 1 and isinstance(test.ops[0], ast.Eq):
            left = ast.get_source_segment(code, test.left)
            m = re.search(r"spark\.sql\((\w+)\)", left)
            names = re.findall(r"\b([a-z_]\w*)\b", left)
            if m and f"spark.sql({m.group(1)}).show" in code:
                replacement = ""
            elif isinstance(test.left, ast.Name) and test.left.id in printed:
                replacement = ""
            elif re.search(r"\.show\(", code) and any(f"{n}.show(" in code for n in names):
                replacement = f"print({left!r}, '->', {left})\n"
            else:
                replacement = f"print({left!r}, '->', {left})\n"
        if replacement is None:
            left_over.append(ast.get_source_segment(code, node))
            continue
        edits.append((start, end, replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        lines[start:end] = [replacement] if replacement else []
    return re.sub(r"\n{3,}", "\n\n", "".join(lines)).strip("\n"), left_over


def finish(path):
    nb = json.loads(Path(path).read_text())
    left = []
    stop = next((i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "markdown" and re.search(r"^## (Practice questions|Answers)", src(c), re.M)), len(nb["cells"]))
    for i, c in enumerate(nb["cells"][:stop]):
        if c["cell_type"] == "code" and re.search(r"^assert\b", src(c), re.M):
            new, lo = finish_asserts(src(c))
            c["source"] = new
            left += [(i, x) for x in lo]
    Path(path).write_text(json.dumps(nb, indent=1) + "\n")
    return left


def asserts_to_prints(code: str) -> str:
    """Any remaining assert becomes a labelled print of the same expression."""
    tree = ast.parse(code)
    lines = code.splitlines(keepends=True)
    nodes = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Assert)), key=lambda n: n.lineno, reverse=True)
    for n in nodes:
        indent = re.match(r"\s*", lines[n.lineno - 1]).group(0)
        expr = ast.unparse(n.test)
        label = expr if len(expr) < 70 else expr[:67] + "..."
        lines[n.lineno - 1:n.end_lineno] = [f"{indent}print({label!r}, '->', {expr})\n"]
    return "".join(lines)


def all_asserts_to_prints(path):
    nb = json.loads(Path(path).read_text())
    for c in nb["cells"]:
        if c["cell_type"] == "code" and re.search(r"^\s*assert\b", src(c), re.M) and "solution" not in c.get("metadata", {}).get("tags", []):
            c["source"] = asserts_to_prints(src(c))
    Path(path).write_text(json.dumps(nb, indent=1) + "\n")
