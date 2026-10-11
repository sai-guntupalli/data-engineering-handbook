#!/usr/bin/env python3
"""
Audit notebook structure and print a compact inventory.

Notebooks are the source of truth in this repository, so this script is the
structural gate: valid JSON, Jupyter metadata, an author watermark (stamped by
scripts/watermark_notebooks.py), non-empty cells, valid Python in every code
cell, no IPython magics or shell escapes, no committed error outputs, and no
leftovers from the old markdown pipeline.

Execution is handled separately by `scripts/run_notebooks.py`.

Usage:
  python3 scripts/audit_notebooks.py
  python3 scripts/audit_notebooks.py --quiet
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

from watermark_notebooks import CREDIT_LINE, expected_watermark


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"

# Lines that begin with an IPython cell/line magic or a shell escape: %%cell, %line,
# !shell. A bare "%%" or "!" followed by a word character is required so that modulo
# expressions and negations that start a line are not flagged.
MAGIC_RE = re.compile(r"^\s*(?:%%|%[A-Za-z]|![A-Za-z])", re.M)
PIPELINE_MARKERS = (
    "Generated from `content/",
    "Notebook inventory:",
    "# Colab setup:",
)


def python_version_gate() -> int:
    """Refuse interpreters older than pyproject.toml requires-python (>=3.12).

    Notebooks use 3.10+ syntax (match/case), so an old system python3 would
    otherwise fail with misleading per-cell "syntax errors" instead of this
    clear setup message.
    """
    if sys.version_info >= (3, 12):
        return 0
    print(
        f"This repository requires Python 3.12+; found "
        f"{sys.version_info.major}.{sys.version_info.minor}.\n"
        "Install the pinned interpreter first: make setup",
        file=sys.stderr,
    )
    return 1


def cell_source(cell: dict) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source)


def audit(path: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"], {}

    if notebook.get("nbformat") != 4:
        errors.append("expected nbformat 4")
    if "kernelspec" not in notebook.get("metadata", {}):
        errors.append("missing kernelspec metadata")

    author_watermark = expected_watermark(path.relative_to(ROOT).as_posix())
    watermark = notebook.get("metadata", {}).get("watermark")
    if watermark is None:
        errors.append("missing author watermark metadata (run: make watermark)")
    else:
        for key in ("author", "repository", "source", "license"):
            if watermark.get(key) != author_watermark[key]:
                errors.append(f"watermark.{key} is stale (run: make watermark)")
        extra = sorted(set(watermark) - set(author_watermark))
        if extra:
            errors.append(f"watermark has unexpected keys: {extra}")

    cells = notebook.get("cells")
    if not isinstance(cells, list) or not cells:
        errors.append("missing notebook cells")
        cells = []
    if cells and CREDIT_LINE not in cell_source(cells[0]):
        errors.append("first cell lacks the author credit line (run: make watermark)")

    counts = {"markdown": 0, "code": 0, "asserts": 0}
    for index, cell in enumerate(cells):
        cell_type = cell.get("cell_type")
        source = cell_source(cell)
        if not source.strip():
            errors.append(f"cell {index} has empty source")
        if any(marker in source for marker in PIPELINE_MARKERS):
            errors.append(f"cell {index} still contains an old markdown-pipeline note")
        if cell_type == "markdown":
            counts["markdown"] += 1
            if source.count("```") % 2:
                errors.append(f"cell {index} has unbalanced code fences")
        elif cell_type == "code":
            counts["code"] += 1
            counts["asserts"] += len(re.findall(r"\bassert\b", source))
            if MAGIC_RE.search(source):
                errors.append(f"cell {index} uses an IPython magic or shell escape")
                continue
            try:
                ast.parse(source)
            except SyntaxError as exc:
                errors.append(f"cell {index} has a Python syntax error: {exc.msg} (line {exc.lineno})")
            error_outputs = [
                output
                for output in cell.get("outputs") or []
                if isinstance(output, dict) and output.get("output_type") == "error"
            ]
            if error_outputs:
                first = error_outputs[0]
                evalue = str(first.get("evalue", "")).splitlines()
                detail = evalue[0][:140] if evalue else "traceback omitted"
                errors.append(
                    f"cell {index} has a committed error output: "
                    f"{first.get('ename', 'Exception')}: {detail}"
                )
        else:
            errors.append(f"cell {index} has unexpected type {cell_type!r}")

    return errors, counts


def main() -> int:
    gate = python_version_gate()
    if gate:
        return gate
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="only print failures and the summary")
    args = parser.parse_args()

    failures = 0
    total_cells = total_code = total_asserts = 0
    notebooks = sorted(NOTEBOOKS_DIR.rglob("*.ipynb"))
    for path in notebooks:
        errors, counts = audit(path)
        rel = path.relative_to(ROOT)
        if errors:
            failures += 1
            print(f"FAIL {rel}", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            continue
        if counts:
            total_cells += counts["markdown"] + counts["code"]
            total_code += counts["code"]
            total_asserts += counts["asserts"]
        if not args.quiet:
            print(
                f"OK   {rel} "
                f"markdown={counts.get('markdown', 0)} code={counts.get('code', 0)} "
                f"asserts={counts.get('asserts', 0)}"
            )

    if failures:
        print(f"\n{failures} notebook(s) failed audit.", file=sys.stderr)
        return 1

    print(
        f"Audited {len(notebooks)} notebook(s): {total_cells} cells, "
        f"{total_code} code cells, {total_asserts} asserts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
