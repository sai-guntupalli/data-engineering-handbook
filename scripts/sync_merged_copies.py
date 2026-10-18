#!/usr/bin/env python3
"""
Keep the self-contained merged copies inside topic notebooks in sync with the
practice notebooks they were merged from.

Three topic notebooks carry a copy of a practice notebook at the bottom so the
handbook reads as one self-contained notebook per subject for single-file viewers:

    notebooks/topics/python.ipynb  <- 01_python_basics, 02_python_coding_problems
    notebooks/topics/spark.ipynb   <- 04_pyspark_concepts

Each merged region starts with a note cell that says "merged here so this
notebook is self-contained" and names the source notebook in backticks. This script:

- "sync" mode (default): pair the region's code cells with the source's code cells
  in order and copy code text and committed outputs across, so the copy executes
  and reads exactly like the original. Markdown cells are left alone: merged
  copies intentionally re-express prose in the topic's Q&A style. A few trailing
  cells that only exist in the merged copy (bonus exercises) are allowed, but
  must carry committed outputs.
- "rebuild" mode: if a merged copy has drifted away from its source, the region
  after the note cell is replaced with the source notebook's cells verbatim
  (markdown, code and outputs).

Usage:
  python3 scripts/sync_merged_copies.py             # apply
  python3 scripts/sync_merged_copies.py --check     # verify only; exit 1 on drift
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MERGE_NOTE = "merged here so this notebook is self-contained"

# topic notebook -> {source notebook: mode}; anything unlisted defaults to "sync"
CONFIG: dict[str, dict[str, str]] = {
    "notebooks/topics/python.ipynb": {
        "notebooks/01_python_basics.ipynb": "sync",
        "notebooks/02_python_coding_problems.ipynb": "sync",
    },
    "notebooks/topics/spark.ipynb": {
        "notebooks/04_pyspark_concepts.ipynb": "rebuild",
    },
}

try:
    import nbformat
except ImportError:
    print("nbformat is missing: uv sync --extra notebooks", file=sys.stderr)
    raise SystemExit(1)


def text_of(cell) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else (source or "")


def merge_regions(cells) -> list[tuple[int, int]]:
    """(note_cell_index, region_end_index) for every merged copy in a notebook."""
    starts = [
        i
        for i, cell in enumerate(cells)
        if cell.get("cell_type") == "markdown" and MERGE_NOTE in text_of(cell)
    ]
    ends = starts[1:] + [len(cells)]
    return list(zip(starts, ends))


def source_rel_from_note(note_cell) -> str | None:
    match = re.search(r"`(notebooks/[\w.-]+\.ipynb)`", text_of(note_cell))
    return match.group(1) if match else None


def sync_region(label, cells, region, source_cells, source_rel, check, problems) -> None:
    """Pair code cells in order; copy text + outputs; leave merged markdown alone."""
    start, end = region
    body = [cell for cell in cells[start + 1 : end] if cell.get("cell_type") == "code"]
    src_code = [cell for cell in source_cells if cell.get("cell_type") == "code"]

    if len(body) < len(src_code):
        problems.append(f"{label}: copy has fewer code cells than source ({len(body)} < {len(src_code)})")
        return

    drifted = [k for k, (dst, src) in enumerate(zip(body, src_code)) if text_of(dst) != text_of(src)]

    if check:
        if drifted:
            problems.append(
                f"{label}: {len(drifted)} code cells drifted from source (first at {drifted[0]})"
            )
            return
        missing = [
            k
            for k, (dst, src) in enumerate(zip(body, src_code))
            if src.get("outputs") and not dst.get("outputs")
        ]
        if missing:
            problems.append(
                f"{label}: {len(missing)} merged code cells lack committed outputs (first at {missing[0]})"
            )
            return
        for k, cell in enumerate(body[len(src_code) :]):
            if not cell.get("outputs"):
                problems.append(f"{label}: trailing merged-only code cell {k} has no committed output")
                return
        print(f"ok      {label}: {len(src_code)} code cells in sync, outputs present")
        return

    for dst, src in zip(body, src_code):
        dst["source"] = text_of(src)
        dst["outputs"] = copy.deepcopy(src.get("outputs", []))
        dst["execution_count"] = src.get("execution_count")
    print(f"synced  {label}: {len(src_code)} code cells refreshed from source")


def rebuild_region(label, cells, region, source_cells, check, problems) -> None:
    start, end = region
    if check:
        if [text_of(cell) for cell in cells[start + 1 : end]] != [text_of(cell) for cell in source_cells]:
            problems.append(f"{label}: merged copy drifted from source (rebuild needed)")
        else:
            print(f"ok      {label}: merged copy matches source verbatim")
        return
    cells[start + 1 : end] = copy.deepcopy(source_cells)
    print(f"rebuilt {label}: region [{start + 1}:{end}] replaced verbatim ({len(source_cells)} cells)")


def process(topic_rel: str, check: bool, problems: list[str]) -> None:
    theme_path = ROOT / topic_rel
    notebook = nbformat.read(theme_path, as_version=4)
    cells = notebook.cells
    regions = merge_regions(cells)
    if not regions:
        problems.append(f"{topic_rel}: no merged regions found")
        return

    for region in regions:
        start, _ = region
        source_rel = source_rel_from_note(cells[start])
        if not source_rel:
            problems.append(f"{topic_rel}: merge note at cell {start} does not name its source notebook")
            continue
        source_path = ROOT / source_rel
        if not source_path.exists():
            problems.append(f"{topic_rel}: merged source {source_rel} does not exist")
            continue
        source_nb = nbformat.read(source_path, as_version=4)
        mode = CONFIG[topic_rel].get(source_rel, "sync")
        label = f"{topic_rel} <- {source_rel}"
        if mode == "rebuild":
            rebuild_region(label, cells, region, source_nb.cells, check, problems)
        else:
            sync_region(label, cells, region, source_nb.cells, source_rel, check, problems)

    if not check and not problems:
        nbformat.write(notebook, theme_path)
        print(f"wrote   {topic_rel}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify only; exit 1 on drift")
    args = parser.parse_args()

    problems: list[str] = []
    for topic_rel in CONFIG:
        if not (ROOT / topic_rel).exists():
            problems.append(f"{topic_rel}: file missing")
            continue
        process(topic_rel, args.check, problems)

    # lib/notebooks.ts subtracts merged-copy cells from the gallery stats for
    # ANY notebook carrying the merge-note marker, but sync/rebuild above only
    # run for CONFIG entries. Fail loudly when the two scopes disagree, so a
    # new merged copy outside CONFIG cannot silently skew the gallery numbers.
    for notebook_path in sorted((ROOT / "notebooks").rglob("*.ipynb")):
        notebook_rel = notebook_path.relative_to(ROOT).as_posix()
        if notebook_rel in CONFIG:
            continue
        if MERGE_NOTE in notebook_path.read_text(encoding="utf-8", errors="ignore"):
            problems.append(
                f"{notebook_rel}: contains {MERGE_NOTE!r} but is not registered in "
                "CONFIG, so this script neither syncs nor checks it"
            )

    if problems:
        for problem in problems:
            print(f"DRIFT  {problem}", file=sys.stderr)
        print(f"\n{len(problems)} problem(s) found.", file=sys.stderr)
        return 1
    if args.check:
        print("All merged copies are in sync with their practice notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())