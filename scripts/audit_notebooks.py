#!/usr/bin/env python3
"""
Structural gate for the notebooks: every one must open and run in Google Colab.

Checks per notebook:
- valid nbformat 4 JSON already in canonical form (``make format``)
- exactly one ``# Title`` heading, no skipped heading levels, balanced code fences
- no empty cells; relative links point at files that exist
- code cells are valid Python with no IPython magics, shell escapes or
  ``# ILLUSTRATIVE`` placeholders (illustrative code belongs in a markdown fence)
- code never talks to a local server (``localhost:<port>``): use a stand-in
- every third-party import is installed by the notebook's setup cell, a code
  cell that assigns ``PACKAGES = {"import_name": "pip-spec", ...}``

Execution is handled separately by ``scripts/run_notebooks.py``.

Usage:
  python scripts/audit_notebooks.py           # inventory + failures
  python scripts/audit_notebooks.py --quiet   # failures and summary only
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notebook_format import ROOT, cell_source, format_notebook, notebook_paths, serialize  # noqa: E402

MAGIC_RE = re.compile(r"^\s*(?:%%|%[A-Za-z]|![A-Za-z])", re.M)
LOCALHOST_RE = re.compile(r"(?:localhost|127\.0\.0\.1):\d+")
FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SETUP_NAME = "PACKAGES"


def markdown_headings(text: str) -> list[int]:
    """Heading levels in a markdown cell, ignoring lines inside code fences."""
    levels: list[int] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        match = None if in_fence else HEADING_RE.match(line)
        if match:
            levels.append(len(match.group(1)))
    return levels


def setup_packages(code_cells: list[str]) -> dict[str, str] | None:
    """The ``PACKAGES`` mapping from the setup cell, or None when there is none."""
    for source in code_cells:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == SETUP_NAME for target in node.targets
            ):
                value = ast.literal_eval(node.value)
                if isinstance(value, dict):
                    return {str(key): str(spec) for key, spec in value.items()}
    return None


def third_party_imports(source: str) -> set[str]:
    """Top-level module names imported by ``source`` that are not stdlib."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            modules.add(node.module.split(".")[0])
    return {name for name in modules if name not in sys.stdlib_module_names}


def setup_cell_index(cells: list[dict]) -> int | None:
    """Index of the code cell that declares ``PACKAGES``, or None."""
    for index, cell in enumerate(cells):
        if cell.get("cell_type") == "code" and setup_packages([cell_source(cell)]) is not None:
            return index
    return None


def broken_links(text: str, notebook_path: Path) -> list[str]:
    broken = []
    for target in LINK_RE.findall(text):
        parsed = urlparse(target)
        if parsed.scheme or target.startswith("#") or not parsed.path:
            continue
        if not (notebook_path.parent / unquote(parsed.path)).exists():
            broken.append(target)
    return broken


def audit(path: Path) -> tuple[list[str], dict[str, int]]:
    relpath = path.relative_to(ROOT).as_posix()
    try:
        raw = path.read_text(encoding="utf-8")
        notebook = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"unreadable notebook: {exc}"], {}

    errors: list[str] = []
    if serialize(format_notebook(notebook, relpath)) != raw:
        errors.append("not in canonical form (run: make format)")

    cells = notebook.get("cells") or []
    code_sources = [cell_source(cell) for cell in cells if cell.get("cell_type") == "code"]
    declared = {name.split(".")[0] for name in setup_packages(code_sources) or {}}
    setup_index = setup_cell_index(cells)

    counts = {"markdown": 0, "code": 0, "asserts": 0}
    h1_count = 0
    previous_level = 0
    missing_imports: set[str] = set()

    for index, cell in enumerate(cells):
        cell_type = cell.get("cell_type")
        source = cell_source(cell)
        if not source.strip():
            errors.append(f"cell {index} is empty")
        if cell_type == "markdown":
            counts["markdown"] += 1
            if sum(1 for line in source.splitlines() if FENCE_RE.match(line)) % 2:
                errors.append(f"cell {index} has unbalanced code fences")
            for level in markdown_headings(source):
                h1_count += level == 1
                if previous_level and level > previous_level + 1:
                    errors.append(f"cell {index} skips from heading level {previous_level} to {level}")
                previous_level = level
            for target in broken_links(source, path):
                errors.append(f"cell {index} links to a missing file: {target}")
        elif cell_type == "code":
            counts["code"] += 1
            counts["asserts"] += len(re.findall(r"\bassert\b", source))
            if MAGIC_RE.search(source):
                errors.append(f"cell {index} uses an IPython magic or shell escape")
                continue
            if "# ILLUSTRATIVE" in source:
                errors.append(f"cell {index} is marked ILLUSTRATIVE: move it into a markdown code fence")
            if LOCALHOST_RE.search(source):
                errors.append(f"cell {index} connects to a local server: use an in-process stand-in")
            try:
                ast.parse(source)
            except SyntaxError as exc:
                errors.append(f"cell {index} has a Python syntax error: {exc.msg} (line {exc.lineno})")
                continue
            if index != setup_index:  # the setup cell installs packages, so its own imports are exempt
                missing_imports |= third_party_imports(source) - declared
        else:
            errors.append(f"cell {index} has unexpected type {cell_type!r}")

    if h1_count != 1:
        errors.append(f"expected exactly one '# Title' heading, found {h1_count}")
    if missing_imports:
        errors.append(
            f"third-party imports missing from the setup cell's {SETUP_NAME}: {', '.join(sorted(missing_imports))}"
        )
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="notebooks to audit (default: all)")
    parser.add_argument("--quiet", action="store_true", help="only print failures and the summary")
    args = parser.parse_args()

    paths = notebook_paths(args.files)
    failures = 0
    totals = {"markdown": 0, "code": 0, "asserts": 0}
    for path in paths:
        errors, counts = audit(path)
        relpath = path.relative_to(ROOT)
        if errors:
            failures += 1
            print(f"FAIL {relpath}", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            continue
        for key in totals:
            totals[key] += counts[key]
        if not args.quiet:
            print(f"OK   {relpath} markdown={counts['markdown']} code={counts['code']} asserts={counts['asserts']}")

    if failures:
        print(f"\n{failures} of {len(paths)} notebook(s) failed audit.", file=sys.stderr)
        return 1
    print(
        f"Audited {len(paths)} notebook(s): {totals['markdown'] + totals['code']} cells, "
        f"{totals['code']} code cells, {totals['asserts']} asserts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
