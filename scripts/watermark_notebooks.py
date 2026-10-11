#!/usr/bin/env python3
"""
Stamp an author watermark into every notebook under notebooks/.

Notebooks are the source of truth for the handbook and get shared as single
files (Colab, the Jupyter viewer, chat links), so each one carries its own
provenance in two layers:

1. Machine-readable watermark in `metadata.watermark`:

       {
         "author": {"name": ..., "github": ..., "email": ...},
         "repository": "sai-guntupalli/data-engineering-handbook",
         "source": "https://github.com/<repo>/blob/master/<path>",
         "license": "CC BY 4.0",
       }

   `source` is a permalink to this file on the default branch, so a notebook
   copied anywhere still states who wrote it, where it lives, and under what
   license reusers must credit the author (see the LICENSE file).

2. A visible credit line right under the title in the opening markdown cell,
   rendered by GitHub, Colab and Jupyter without any viewer-side changes.

The stamp is idempotent. It only touches `metadata.watermark` and the opening
cell's markdown; everything else is re-serialized with the exact parameters
nbformat uses (indent 1, sorted keys, trailing newline), so the diff is one
metadata block plus one markdown line per file.

Usage:
  python3 scripts/watermark_notebooks.py          # stamp missing watermarks
  python3 scripts/watermark_notebooks.py --check  # verify only; exit 1 on drift
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"

# Single source of truth: scripts/audit_notebooks.py imports these constants and
# enforces exactly what this script stamps. Change authorship only via this file.
AUTHOR = {
    "name": "Sai Guntupalli",
    "github": "sai-guntupalli",
    "email": "sai.guntupalli.tech@gmail.com",
}
REPOSITORY = "sai-guntupalli/data-engineering-handbook"
BRANCH = "master"
# The whole handbook (notebooks included) is licensed CC BY 4.0: reusing it
# anywhere requires crediting the author. Full text: the LICENSE file.
LICENSE = "CC BY 4.0"

CREDIT_LINE = (
    f"*Author: [{AUTHOR['name']}](https://github.com/{AUTHOR['github']}) · "
    f"[{REPOSITORY}](https://github.com/{REPOSITORY})*"
)


def expected_watermark(rel_path: str) -> dict:
    """The `metadata.watermark` block for a repository-relative notebook path."""
    return {
        "author": AUTHOR,
        "repository": REPOSITORY,
        "source": f"https://github.com/{REPOSITORY}/blob/{BRANCH}/{rel_path}",
        "license": LICENSE,
    }


def first_cell_source(notebook: dict) -> str:
    cells = notebook.get("cells") or []
    if not cells:
        return ""
    source = cells[0].get("source", "")
    if isinstance(source, list):
        return "".join(source)
    return source or ""


def with_credit(source: str) -> str | None:
    """Insert the credit line under the title heading; None if it is already
    present or the cell has no `# ` title to anchor it."""
    if CREDIT_LINE in source:
        return None
    lines = source.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("# "):
            head, tail = lines[: index + 1], lines[index + 1 :]
            while tail and not tail[0].strip():
                tail = tail[1:]
            return "".join(head + ["\n", CREDIT_LINE + "\n", "\n"] + tail)
    return None


def process(path: Path, apply: bool) -> list[str]:
    """Stamp (or, in check mode, measure) the watermark. Returns the list of
    fixes applied — or needed — for this notebook."""
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    rel = path.relative_to(ROOT).as_posix()
    expected = expected_watermark(rel)
    fixes: list[str] = []

    metadata = notebook.setdefault("metadata", {})
    if metadata.get("watermark") != expected:
        fixes.append("metadata.watermark")
        metadata["watermark"] = expected

    cells = notebook.get("cells") or []
    if not cells:
        if "metadata.watermark" not in fixes:
            fixes.append("no cells to carry the credit line")
        return fixes
    updated = with_credit(first_cell_source(notebook))
    if updated is not None:
        fixes.append("credit line")
        if apply:
            cells[0]["source"] = updated.splitlines(keepends=True)

    if apply and fixes:
        text = json.dumps(notebook, indent=1, separators=(",", ": "), sort_keys=True, ensure_ascii=False)
        path.write_text(text + "\n", encoding="utf-8")
    return fixes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify only; exit 1 on drift")
    args = parser.parse_args()

    notebooks = sorted(NOTEBOOKS_DIR.rglob("*.ipynb"))
    if not notebooks:
        print(f"No notebooks found in {NOTEBOOKS_DIR}", file=sys.stderr)
        return 1

    stamped = current = 0
    for path in notebooks:
        fixes = process(path, apply=not args.check)
        rel = path.relative_to(ROOT)
        if fixes:
            stamped += 1
            print(f"{'DRIFT' if args.check else 'stamp'} {rel}: {'; '.join(fixes)}")
        else:
            current += 1
            print(f"ok   {rel}")

    print()
    if args.check:
        if stamped:
            print(
                f"{stamped} notebook(s) missing the author watermark; "
                "run: make watermark",
                file=sys.stderr,
            )
            return 1
        print(f"All {current} notebook(s) carry the author watermark.")
    else:
        print(f"Watermarked {stamped} notebook(s); {current} already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())