"""Execute hidden Python practice answers and ensure a wrong answer is rejected.

Runs temporary in-memory notebook copies; source notebooks remain output-free.
"""

import ast
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
paths = sorted((root / "notebooks/topics/python/practice").glob("python-challenges-*.ipynb")) + sorted(
    (root / "notebooks/topics/python/practice").glob("python-drills-*.ipynb")
)


def verify(p):
    n = json.loads(p.read_text())
    cells = n["cells"]
    exercises = 0
    for i, c in enumerate(cells):
        if c["cell_type"] != "markdown" or "Show solution" not in "".join(c["source"]):
            continue
        match = re.search(r"```python\n(.*?)\n```", "".join(c["source"]), re.S)
        if not match:
            continue
        solution = match.group(1)
        stub = cells[i - 2]
        check = cells[i - 1]
        tree = ast.parse("".join(stub["source"]))
        defs = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        target = defs[-1].name
        stub["source"] = solution.splitlines(keepends=True)
        original = "".join(check["source"])
        wrong = (
            "async def _wrong(*args, **kwargs):\n    return None\n"
            if isinstance(defs[-1], ast.AsyncFunctionDef)
            else "def _wrong(*args, **kwargs):\n    return None\n"
        )
        extra_mutant = ""
        if target in {"count_with_lock", "sum_with_queue"}:

            class RemoveLock(ast.NodeTransformer):
                def visit_With(self, node):
                    if any(
                        isinstance(item.context_expr, ast.Name) and item.context_expr.id == "lock"
                        for item in node.items
                    ):
                        return node.body
                    return self.generic_visit(node)

            unlocked = ast.unparse(ast.fix_missing_locations(RemoveLock().visit(ast.parse(solution))))
            invocation = (
                "count_with_lock(4, 2500)" if target == "count_with_lock" else "sum_with_queue(list(range(10000)), 4)"
            )
            extra_mutant = (
                f"\nexec({unlocked!r})\n"
                f"for _attempt in range(5):\n    assert not protected_updates(lambda: {invocation}, 10000)\n"
                f"{target} = _saved_answer\n"
            )
        check["source"] = (
            "_before = dict(_tally)\n"
            + original
            + '\nassert (_tally["passed"] - _before["passed"] == '
            + '_tally["total"] - _before["total"]), "reference failed"\n'
            + "_saved_tally = dict(_tally)\n_saved_answer = "
            + target
            + "\n"
            + wrong
            + target
            + " = _wrong\n"
            + original
            + '\nassert (_tally["passed"] - _saved_tally["passed"] < '
            + '_tally["total"] - _saved_tally["total"]), "wrong answer escaped"\n'
            + target
            + " = _saved_answer\n_tally = _saved_tally\n"
            + extra_mutant
        ).splitlines(keepends=True)
        exercises += 1
    NotebookClient(
        nbformat.reads(json.dumps(n), as_version=4),
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(p.parent)}},
    ).execute()
    return f"PASS {p.name}: {exercises} reference answers and wrong-answer checks"


with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [(p, pool.submit(verify, p)) for p in paths]
    failed = False
    for p, f in futures:
        try:
            print(f.result(), flush=True)
        except Exception as e:
            failed = True
            print("FAIL", p.name, str(e)[-5000:], flush=True)
    if failed:
        raise SystemExit(1)
