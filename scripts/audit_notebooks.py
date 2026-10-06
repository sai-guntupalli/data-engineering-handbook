#!/usr/bin/env python3
"""
Audit notebook structure and print a compact inventory.

The goal is not to execute notebooks; `scripts/run_notebooks.py` does that for
the hand-written practice notebooks. This script checks that every notebook is
valid JSON, has Jupyter metadata, has non-empty cells, and exposes enough cell
statistics for the documentation app to render useful previews.

Usage:
  python3 scripts/audit_notebooks.py
  python3 scripts/audit_notebooks.py --quiet
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"


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

    cells = notebook.get("cells")
    if not isinstance(cells, list) or not cells:
        errors.append("missing notebook cells")
        cells = []

    counts = {"markdown": 0, "code": 0, "asserts": 0}
    for index, cell in enumerate(cells):
        cell_type = cell.get("cell_type")
        source = cell_source(cell)
        if not source.strip():
            errors.append(f"cell {index} has empty source")
        if cell_type == "markdown":
            counts["markdown"] += 1
        elif cell_type == "code":
            counts["code"] += 1
            counts["asserts"] += source.count("assert ")
        else:
            errors.append(f"cell {index} has unexpected type {cell_type!r}")

    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args()

    failures = 0
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
        if not args.quiet:
            print(
                f"OK   {rel} "
                f"markdown={counts['markdown']} code={counts['code']} asserts={counts['asserts']}"
            )

    if failures:
        print(f"\n{failures} notebook(s) failed audit.", file=sys.stderr)
        return 1

    print(f"Audited {len(notebooks)} notebook(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
