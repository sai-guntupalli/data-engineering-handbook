#!/usr/bin/env python3
"""
Execute the Jupyter notebooks in notebooks/ so their outputs are reproducible.

Usage:
  python3 scripts/run_notebooks.py            # execute every notebook and save outputs
  python3 scripts/run_notebooks.py --check    # execute without writing outputs (CI-safe)
  python3 scripts/run_notebooks.py notebooks/03_sql_interview_questions.ipynb

Requires the notebook extra:
  uv sync --extra notebooks
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"


def _fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def main() -> int:
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        return _fail(
            "Notebook dependencies are missing. Install them with:\n"
            "  uv sync --extra notebooks\n"
            "or: pip install nbformat nbclient ipykernel"
        )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="notebooks to run (default: all in notebooks/)")
    parser.add_argument("--check", action="store_true", help="execute without saving outputs")
    parser.add_argument("--timeout", type=int, default=600, help="per-cell timeout in seconds")
    args = parser.parse_args()

    if args.files:
        paths = [Path(f) if Path(f).is_absolute() else ROOT / f for f in args.files]
    else:
        paths = sorted(NOTEBOOK_DIR.glob("*.ipynb"))

    if not paths:
        return _fail(f"No notebooks found in {NOTEBOOK_DIR}")

    failures: list[str] = []
    for path in paths:
        if not path.exists():
            failures.append(f"{path} (missing)")
            print(f"MISS {path}")
            continue

        try:
            notebook = nbformat.read(path, as_version=4)
        except Exception as exc:  # nbformat raises ValidationError for unreadable files
            failures.append(f"{path.name}: unreadable notebook ({exc})")
            print(f"FAIL {path.name}: unreadable notebook")
            continue
        client = NotebookClient(
            notebook,
            timeout=args.timeout,
            kernel_name="python3",
            resources={"metadata": {"path": str(path.parent)}},
        )
        try:
            client.execute()
        except Exception as exc:  # nbclient raises CellExecutionError and friends
            failures.append(f"{path.name}: {exc}")
            print(f"FAIL {path.name}: execution error")
            continue

        errors = [
            output
            for cell in notebook.cells
            if cell.cell_type == "code"
            for output in cell.get("outputs", [])
            if output.get("output_type") == "error"
        ]
        if errors:
            failures.append(f"{path.name}: {len(errors)} error output(s)")
            print(f"FAIL {path.name}: {errors[0].get('ename')}: {errors[0].get('evalue')}")
            continue

        if not args.check:
            nbformat.write(notebook, path)
        print(f"OK   {path.name}")

    if failures:
        print(f"\n{len(failures)} notebook(s) failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print(f"\n{len(paths)} notebook(s) executed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
