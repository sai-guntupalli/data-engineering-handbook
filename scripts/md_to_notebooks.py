#!/usr/bin/env python3
"""
Convert the topic documents in content/*.md into Jupyter notebooks.

Each `##` section of a document becomes a markdown cell, every ```python block
becomes an executable code cell, and fences in other languages (sql, bash, yaml,
scala, ...) stay as formatted markdown blocks because they need their own engine.

A few topics also have a hand-written practice notebook under notebooks/; those
notebooks are merged into the matching topic notebook so the material lives in one
place (see MERGES below).

Usage:
  python3 scripts/md_to_notebooks.py            # regenerate notebooks/topics/*.ipynb
  python3 scripts/md_to_notebooks.py --check    # fail if the notebooks are out of date
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
NOTEBOOKS_DIR = ROOT / "notebooks"
TOPICS_DIR = NOTEBOOKS_DIR / "topics"

PYTHON_LANGS = {"python", "py", "python3"}

# Topic slug -> practice notebooks (in notebooks/) merged into that topic notebook.
MERGES: dict[str, list[tuple[str, str]]] = {
    "python": [
        ("01_python_basics.ipynb", "Python basics"),
        ("02_python_coding_problems.ipynb", "Python coding problems"),
    ],
    "sql": [
        ("03_sql_interview_questions.ipynb", "SQL interview questions"),
    ],
    "spark": [
        ("04_pyspark_concepts.ipynb", "PySpark concepts"),
    ],
}

KERNELSPEC = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
LANGUAGE_INFO = {"name": "python", "version": "3.13"}

INTRO = (
    "*Converted from `content/{slug}.md`.* Every `##` section of the source document is a markdown cell and every "
    "Python code block is a code cell. Snippets in SQL, PySpark, shell, YAML, Scala and other languages stay as "
    "formatted blocks because they need a specific engine to run, and the code is illustrative: check library and "
    "version requirements before running it."
)


def markdown_cell(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.strip("\n").splitlines(keepends=True)}


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip("\n").splitlines(keepends=True),
    }


def _as_cell_list(cell: dict) -> dict:
    """Normalise an existing notebook cell to the list-of-lines source form."""
    source = cell.get("source", "")
    if isinstance(source, str):
        cell["source"] = source.splitlines(keepends=True)
    return cell


def _is_house_style_noise(line: str) -> bool:
    return (
        line.startswith("## [Main title]")
        or line.startswith("### [Interview questions]")
        or line.startswith("+ [")
        or line.startswith("[Table of Contents]")
        or line.startswith("**Notebook:**")  # the notebook does not need to link itself
    )


def parse_document(text: str, slug: str) -> tuple[str, list[dict]]:
    """Return (title, cells) for one content document."""
    title = slug.replace("-", " ").title()
    cells: list[dict] = []
    buffer: list[str] = []
    title_seen = False

    def flush() -> None:
        block = "\n".join(buffer).strip("\n")
        buffer.clear()
        if block.strip():
            cells.append(markdown_cell(block))

    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]

        if line.startswith("```"):
            fence = line
            language = line[3:].strip().lower()
            body: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                body.append(lines[index])
                index += 1
            index += 1  # closing fence (or EOF)
            flush()
            code = "\n".join(body)
            if language in PYTHON_LANGS:
                cells.append(code_cell(code))
            else:
                cells.append(markdown_cell(f"```{language}\n{code}\n```"))
            continue

        if _is_house_style_noise(line):
            index += 1
            continue

        if not title_seen and line.startswith("# "):
            title = line[2:].strip()
            title_seen = True
            index += 1
            continue

        if line.startswith("## ") or line.startswith("### "):
            # One markdown cell per section and subsection, so a long topic
            # document becomes a scannable outline instead of huge text cells.
            flush()
            buffer.append(line)
            index += 1
            continue

        buffer.append(line)
        index += 1

    flush()
    return title, cells


def header_cells(title: str, slug: str) -> list[dict]:
    return [
        markdown_cell(f"# {title}\n\n{INTRO.format(slug=slug)}"),
    ]


def merge_practice_cells(slug: str, cells: list[dict]) -> list[dict]:
    """Append the practice notebook cells listed in MERGES for this slug."""
    merged: list[dict] = []
    for filename, label in MERGES.get(slug, []):
        path = NOTEBOOKS_DIR / filename
        if not path.exists():
            print(f"  note: {filename} not found, skipping merge into {slug}", file=sys.stderr)
            continue
        notebook = json.loads(path.read_text(encoding="utf-8"))
        merged.append(
            markdown_cell(
                f"---\n\n# Practice notebook: {label}\n\n"
                f"The cells below are the exercises from `notebooks/{filename}`, merged here so the topic notebook "
                "is self-contained. They are self-checking: run them top to bottom and the assertions will confirm "
                "your answers."
            )
        )
        for cell in notebook.get("cells", []):
            merged.append(_as_cell_list(cell))
    return cells + merged


def build_notebook(slug: str) -> dict:
    source = CONTENT_DIR / f"{slug}.md"
    text = source.read_text(encoding="utf-8")
    title, cells = parse_document(text, slug)
    cells = header_cells(title, slug) + cells
    cells = merge_practice_cells(slug, cells)
    # nbformat 4.5 requires a stable cell id; derive it from the slug and position.
    for position, cell in enumerate(cells):
        cell.setdefault("id", f"{slug[:50]}-{position:04d}")
        cell.setdefault("metadata", {})
    return {
        "cells": cells,
        "metadata": {"kernelspec": KERNELSPEC, "language_info": LANGUAGE_INFO},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def _slugs() -> list[str]:
    return [
        path.stem
        for path in sorted(CONTENT_DIR.glob("*.md"))
        if path.name != "full.md"
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify notebooks are up to date without writing")
    args = parser.parse_args()

    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    slugs = _slugs()
    failures = 0
    written = 0

    for slug in slugs:
        notebook = build_notebook(slug)
        target = TOPICS_DIR / f"{slug}.ipynb"
        payload = json.dumps(notebook, indent=1, ensure_ascii=False) + "\n"

        if args.check:
            if not target.exists():
                print(f"MISS {target.relative_to(ROOT)}")
                failures += 1
            elif target.read_text(encoding="utf-8") != payload:
                print(f"STALE {target.relative_to(ROOT)}")
                failures += 1
            continue

        target.write_text(payload, encoding="utf-8")
        written += 1

    if args.check:
        if failures:
            print(f"\n{failures} notebook(s) out of date. Run: python3 scripts/md_to_notebooks.py", file=sys.stderr)
            return 1
        print(f"All {len(slugs)} topic notebooks are up to date.")
        return 0

    print(f"Wrote {written} topic notebooks to {TOPICS_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
