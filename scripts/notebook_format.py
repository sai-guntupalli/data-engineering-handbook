#!/usr/bin/env python3
"""
Put every notebook into the handbook's canonical, Colab-ready shape.

The formatter is idempotent and only touches presentation, never lesson content:

- The first cell opens with the ``# Title``, then the author credit line and an
  "Open in Colab" badge pointing at this exact file on the default branch.
- The old "How to use this notebook" boilerplate paragraph is removed.
- Outputs and execution counts are stripped: notebooks are meant to be run, and
  CI executes every one of them, so committed outputs are only diff noise.
- Notebook metadata is reduced to the kernelspec plus Colab's table of contents.
- Every cell gets a stable id (existing ids are kept).
- Files are serialized like nbformat does: indent 1, sorted keys, final newline.

Usage:
  python scripts/notebook_format.py            # format every notebook in place
  python scripts/notebook_format.py --check    # exit 1 if any notebook would change
  python scripts/notebook_format.py notebooks/topics/kafka.ipynb
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"

AUTHOR_NAME = "Sai Guntupalli"
AUTHOR_URL = "https://github.com/sai-guntupalli"
REPOSITORY = "sai-guntupalli/data-engineering-handbook"
BRANCH = "master"

CREDIT_LINE = f"*Author: [{AUTHOR_NAME}]({AUTHOR_URL}) · [{REPOSITORY}](https://github.com/{REPOSITORY}) · CC BY 4.0*"
COLAB_BADGE_IMAGE = "https://colab.research.google.com/assets/colab-badge.svg"
COLAB_BASE = f"https://colab.research.google.com/github/{REPOSITORY}/blob/{BRANCH}"

CANONICAL_METADATA = {
    "colab": {"provenance": [], "toc_visible": True},
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}

# Lines in the opening cell that the formatter owns and regenerates.
_OWNED_LINE = re.compile(r"^\s*(\*Author: \[|\[!\[Open In Colab\])")
_HOW_TO_USE = re.compile(r"^\*How to use this notebook\.\*[^\n]*(?:\n|$)", re.M)


def colab_url(relpath: str) -> str:
    return f"{COLAB_BASE}/{relpath}"


def colab_badge(relpath: str) -> str:
    return f"[![Open In Colab]({COLAB_BADGE_IMAGE})]({colab_url(relpath)})"


def cell_source(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def _as_source_lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def _format_opening_cell(text: str, relpath: str) -> str:
    """Title, credit line, badge, then the cell's own remaining content."""
    lines = [line for line in text.split("\n") if not _OWNED_LINE.match(line)]
    title_index = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if title_index is None:
        title = "# " + Path(relpath).stem.replace("_", " ").replace("-", " ").strip()
        body = lines
    else:
        title = lines[title_index].rstrip()
        body = lines[:title_index] + lines[title_index + 1 :]
    rest = "\n".join(body).strip()
    header = f"{title}\n\n{CREDIT_LINE}\n\n{colab_badge(relpath)}"
    return f"{header}\n\n{rest}\n" if rest else f"{header}\n"


def _stable_id(relpath: str, index: int, taken: set[str]) -> str:
    salt = 0
    while True:
        digest = hashlib.sha1(f"{relpath}:{index}:{salt}".encode()).hexdigest()[:8]
        if digest not in taken:
            return digest
        salt += 1


def format_notebook(notebook: dict, relpath: str) -> dict:
    """Return the canonical form of ``notebook``; ``relpath`` is repo-relative."""
    cells: list[dict] = []
    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type", "markdown")
        text = cell_source(cell)
        if cell_type == "markdown":
            text = _HOW_TO_USE.sub("", text).strip("\n")
            if not text.strip():
                continue
        formatted = {"cell_type": cell_type, "metadata": {}, "source": text}
        if "id" in cell:
            formatted["id"] = cell["id"]
        if cell_type == "code":
            formatted["execution_count"] = None
            formatted["outputs"] = []
        cells.append(formatted)

    if cells and cells[0]["cell_type"] == "markdown":
        cells[0]["source"] = _format_opening_cell(cells[0]["source"], relpath)
    else:
        title_cell = {"cell_type": "markdown", "metadata": {}, "source": ""}
        title_cell["source"] = _format_opening_cell("", relpath)
        cells.insert(0, title_cell)

    taken: set[str] = set()
    for index, cell in enumerate(cells):
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not cell_id or cell_id in taken:
            cell_id = _stable_id(relpath, index, taken)
        cell["id"] = cell_id
        taken.add(cell_id)
        cell["source"] = _as_source_lines(cell["source"].rstrip("\n"))

    return {
        "cells": cells,
        "metadata": json.loads(json.dumps(CANONICAL_METADATA)),
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def serialize(notebook: dict) -> str:
    return json.dumps(notebook, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def notebook_paths(args: list[str]) -> list[Path]:
    if args:
        return [Path(arg).resolve() for arg in args]
    return sorted(NOTEBOOKS_DIR.rglob("*.ipynb"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="notebooks to format (default: all)")
    parser.add_argument("--check", action="store_true", help="report unformatted notebooks; change nothing")
    args = parser.parse_args()

    changed: list[str] = []
    for path in notebook_paths(args.files):
        relpath = path.relative_to(ROOT).as_posix()
        original = path.read_text(encoding="utf-8")
        formatted = serialize(format_notebook(json.loads(original), relpath))
        if formatted == original:
            continue
        changed.append(relpath)
        if not args.check:
            path.write_text(formatted, encoding="utf-8")

    verb = "would reformat" if args.check else "reformatted"
    for relpath in changed:
        print(f"{verb} {relpath}")
    if args.check and changed:
        print(f"\n{len(changed)} notebook(s) need formatting: run `make format`.", file=sys.stderr)
        return 1
    print(f"{len(changed)} notebook(s) {verb}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
