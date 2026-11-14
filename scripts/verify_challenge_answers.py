"""Verify current SQL, PySpark and DuckDB answers and their published sample-output tables.

Regression statements are restored only in temporary notebook copies. Source notebooks
contain questions, sample data, exercise cells and hidden reference implementations.
"""

import argparse
import ast
import hashlib
import html
import inspect
import json
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, InvalidOperation
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/challenge-checks"


def expected_tables(source):
    """Read only output tables; SQL question cells also contain input tables."""
    output = source.split("**Expected output**", 1)[1]
    tables = []
    current = []
    for line in output.splitlines() + [""]:
        if line.startswith("|"):
            current.append([html.unescape(v.strip().strip("`")) for v in line.strip("|").split("|")])
        elif current:
            if len(current) < 2 or not all(set(v) <= set("-: ") for v in current[1]):
                raise ValueError("Malformed sample-output table")
            width = len(current[0])
            if any(len(row) != width for row in current[2:]):
                raise ValueError("Sample-output row has a different width than its header")
            tables.append({"columns": current[0], "rows": current[2:]})
            current = []
    if not tables:
        raise ValueError("Expected at least one sample-output table")
    return tables


def normalize(value):
    if value is None:
        return ("null", "")
    if isinstance(value, bool):
        return ("bool", str(value).lower())
    text = str(value)
    if text == "null":
        return ("null", "")
    if text in {"true", "false"}:
        return ("bool", text)
    try:
        number = Decimal(text)
        if number.is_finite():
            return ("number", number)
    except InvalidOperation:
        pass
    return ("text", text)


def compare_table(expected, actual):
    """Check column names, row count, row order, values, nulls and booleans."""
    if expected["columns"] != actual["columns"]:
        raise AssertionError(f"Sample columns differ: {expected['columns']} != {actual['columns']}")
    matches = len(expected["rows"]) == len(actual["rows"])
    for left, right in zip(expected["rows"], actual["rows"], strict=False):
        matches = matches and len(left) == len(right)
        for wanted, got in zip(left, right, strict=False):
            if isinstance(got, str):
                # Postal padding and a phone's '+' are meaningful string content.
                matches = matches and str(wanted) not in {"null", "true", "false"} and str(wanted) == got
            else:
                matches = matches and normalize(wanted) == normalize(got)
    if not matches:
        raise AssertionError(f"Sample rows differ: expected {expected['rows']}, got {actual['rows']}")


def rebuild_solution(source, recipe):
    tree = ast.parse(source)
    fingerprint = hashlib.sha256(source.strip().encode()).hexdigest()
    if fingerprint != recipe["fingerprint"]:
        raise ValueError("Reference implementation changed: review and update its regression recipe")
    blocks = {}
    for block in recipe["blocks"]:
        blocks.setdefault(block["after_statement"], []).append(block["source"])
    if any(index < 0 or index > len(tree.body) for index in blocks):
        raise ValueError("Regression block refers to a missing statement")
    parts = list(blocks.get(0, []))
    for index, node in enumerate(tree.body, 1):
        parts.append(ast.get_source_segment(source, node))
        parts.extend(blocks.get(index, []))
    return "\n\n".join(parts) + "\n"


def verified_notebook(fixture):
    path = ROOT / fixture["notebook"]
    notebook = nbformat.read(path, as_version=4)
    by_id = {c.id: c for c in notebook.cells}
    answers = {c.id for c in notebook.cells if "solution" in c.metadata.get("tags", [])}
    if answers != set(fixture["solutions"]):
        raise ValueError("Every hidden answer must have exactly one regression recipe")
    helpers = (
        "from decimal import Decimal, InvalidOperation\n"
        + inspect.getsource(normalize)
        + "\n"
        + inspect.getsource(compare_table)
        + "\n_challenge_outputs = {}\n"
        + "def _frame_data(frame):\n"
        + "    rows = frame.collect() if hasattr(frame, 'collect') else frame.fetchall()  # Spark or DuckDB\n"
        + "    return {'columns': list(frame.columns), 'rows': [list(row) for row in rows]}\n"
        + "def _capture_sql(cell_id, query):\n"
        + "    _challenge_outputs.setdefault(cell_id, []).append(_frame_data(spark.sql(query)))\n"
        + "\n".join(fixture["helpers"])
    )
    removed = {}
    for entry in fixture["removed_cells"]:
        if entry["before"] not in by_id:
            raise ValueError("Regression fixture refers to a removed notebook cell")
        restored = nbformat.from_dict(entry["cell"])
        if isinstance(restored.source, list):
            restored.source = "".join(restored.source)
        removed.setdefault(entry["before"], []).append(restored)
    for cell_id, recipe in fixture["solutions"].items():
        cell = by_id[cell_id]
        if "solution" not in cell.metadata.get("tags", []):
            raise ValueError("Reference answer must remain tagged as a hidden solution")
        source = rebuild_solution(cell.source, recipe)
        example = fixture["examples"][cell_id]
        tables = expected_tables(by_id[example["expected_cell"]].source)
        if "output_indices" in example:
            source = source.replace("spark.sql(q).show()", f"_capture_sql({cell_id!r}, q)")
            expressions = [f"_challenge_outputs[{cell_id!r}][{index}]" for index in example["output_indices"]]
        else:
            expressions = [f"_frame_data({frame})" for frame in example["frames"]]
        if len(tables) != len(expressions):
            raise ValueError("Each requested result needs exactly one published output table")
        for expected, expression in zip(tables, expressions, strict=True):
            source += f"\ncompare_table({expected!r}, {expression})\n"
        cell.source = source
    cells = []
    for cell in notebook.cells:
        cells.extend(removed.get(cell.id, []))
        cells.append(cell)
        if cell.cell_type == "code" and cell.source.startswith("# Setup:"):
            cells.append(nbformat.v4.new_code_cell(helpers))
    cells.append(nbformat.v4.new_code_cell("if 'spark' in globals():\n    spark.stop()"))
    notebook.cells = cells
    return path, notebook


def verify(fixture_path):
    fixture = json.loads(fixture_path.read_text())
    path, notebook = verified_notebook(fixture)
    NotebookClient(
        notebook,
        timeout=180,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
    ).execute()
    return f"PASS {path.name}: {len(fixture['solutions'])} answers, regression cases and published output tables"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", help="Optional notebook stems to verify")
    args = parser.parse_args()
    fixtures = sorted(FIXTURES.glob("*.json"))
    if args.notebooks:
        fixtures = [p for p in fixtures if p.stem in args.notebooks]
        if len(fixtures) != len(set(args.notebooks)):
            parser.error("Unknown challenge notebook")
    if not fixtures:
        parser.error("No challenge verification fixtures found")
    failed = False
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [(p, pool.submit(verify, p)) for p in fixtures]
        for path, result in results:
            try:
                print(result.result(), flush=True)
            except Exception as error:
                failed = True
                print(f"FAIL {path.stem}: {str(error)[-6000:]}", flush=True)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
