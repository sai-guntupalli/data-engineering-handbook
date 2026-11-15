"""Python lessons: turn asserts into output lines that show the value being checked."""
import ast, json, re, sys
from pathlib import Path

def src(c): return "".join(c["source"])

def is_literal(node):
    try:
        ast.literal_eval(node)
        return True
    except Exception:
        return isinstance(node, ast.Call) and getattr(node.func, "id", "") in {"Decimal", "date", "datetime", "timedelta", "set", "frozenset"}


def show_expr(node, code):
    """Return a list of expressions to print for an assert test."""
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
        out = []
        for v in node.values: out += show_expr(v, code)
        return out
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], (ast.Eq, ast.Is)):
        left, right = node.left, node.comparators[0]
        if is_literal(right):
            return [ast.unparse(left)]
        if is_literal(left):
            return [ast.unparse(right)]
        return [ast.unparse(node)]  # two expressions: show the comparison itself
    if isinstance(node, ast.Compare) and len(node.ops) > 1 and all(isinstance(o, ast.Eq) for o in node.ops):
        return [ast.unparse(node.left)]
    return [ast.unparse(node)]

def fmt(expr):
    if "{" in expr or "}" in expr or "\\" in expr:
        return f"print({expr!r}, '->', {expr})"
    q = "'" if '"' in expr else '"'
    if q in expr:
        return f"print({expr!r}, '->', {expr})"
    return f"print(f{q}{{{expr} = }}{q})"

def convert(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code
    lines = code.splitlines(keepends=True)
    nodes = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Assert)), key=lambda n: n.lineno, reverse=True)
    for n in nodes:
        indent = re.match(r"\s*", lines[n.lineno - 1]).group(0)
        last = lines[n.end_lineno - 1]
        comment = ""
        m = re.search(r"\)\s*(#.*)$|[\w\]\"']\s+(#.*)$", last.rstrip("\n"))
        if m and n.lineno == n.end_lineno:
            comment = "  " + (m.group(1) or m.group(2))
        exprs = show_expr(n.test, code)
        new = [f"{indent}{fmt(e)}{comment if i == len(exprs) - 1 else ''}\n" for i, e in enumerate(exprs)]
        lines[n.lineno - 1:n.end_lineno] = new
    return "".join(lines)

def migrate(path):
    nb = json.loads(Path(path).read_text())
    for c in nb["cells"]:
        if c["cell_type"] == "code" and re.search(r"^\s*assert\b", src(c), re.M):
            c["source"] = convert(src(c))
    Path(path).write_text(json.dumps(nb, indent=1) + "\n")

if __name__ == "__main__":
    for p in sys.argv[1:]: migrate(p)
