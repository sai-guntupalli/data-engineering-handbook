#!/usr/bin/env python3
"""
Teaching-structure check for the notebooks (CONTRIBUTING.md, "The rules every notebook follows").

``audit_notebooks.py`` proves a notebook runs in Colab; this script checks that it teaches the house way:

- setup: a two-line setup cell (``# Setup:`` comment and one ``!pip install`` line), not the old ``PACKAGES`` cell
- lessons: examples show output instead of asserting it, at least one ``**What to notice:**`` note,
  ``## Check yourself``, ``## Key takeaways`` and a ``**Next:**`` link
- practice: a ``**Difficulty:**`` line under every exercise and a ``solution``-tagged answer cell for it
- every notebook links onward with ``**Next:**`` except references

Older notebooks are migrated over time. ``scripts/standards_baseline.json`` lists the warnings each one had when
the check was introduced; the check fails when a notebook gains a warning that is not in the baseline, so the
handbook can only move towards the standard. Run with ``--update-baseline`` after migrating a notebook.

Usage:
  python scripts/notebook_standards.py                   # warnings beyond the baseline (CI)
  python scripts/notebook_standards.py --all             # every warning, baseline included
  python scripts/notebook_standards.py --update-baseline # rewrite the baseline from the current notebooks
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notebook_format import ROOT, cell_source, notebook_paths  # noqa: E402

BASELINE = ROOT / "scripts" / "standards_baseline.json"
ASSERT_RE = re.compile(r"^\s*assert\b", re.M)
EXERCISE_RE = re.compile(r"^##+ (?:Exercise|Problem|Q)\s*\d+", re.M)


def kind_of(path: Path) -> str:
    """What the notebook is, from its file name (mirrors ``categoryOf`` in site/lib/tools.ts)."""
    slug = path.stem
    if re.search(r"-00-|start-here", slug):
        return "start"
    if "reference" in slug or slug == "pyspark-concepts-end-to-end":
        return "reference" if "reference" in slug else "lesson"
    if re.search(r"drill|practice|challenge|coding-problems", slug):
        return "practice"
    if "interview" in slug:
        return "interview"
    return "lesson"


def learner_asserts(source: str) -> int:
    """Assert statements outside test helpers: inside ``def test_*`` or ``def assert_*`` the assert is the lesson."""
    try:
        tree = ast.parse("\n".join(line for line in source.splitlines() if not line.startswith("!")))
    except SyntaxError:
        return len(ASSERT_RE.findall(source))
    exempt: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith(("test_", "assert_")):
            exempt.update(id(child) for child in ast.walk(node))
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.Assert) and id(node) not in exempt)


def is_solution(cell: dict) -> bool:
    return "solution" in (cell.get("metadata") or {}).get("tags", [])


def warnings_for(path: Path) -> list[str]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells") or []
    code = [c for c in cells if c.get("cell_type") == "code"]
    markdown = "\n".join(cell_source(c) for c in cells if c.get("cell_type") == "markdown")
    kind = kind_of(path)
    found: list[str] = []

    if code:
        first = cell_source(code[0])
        if "PACKAGES" in first:
            found.append("long-setup: use the two-line setup cell")
        elif "!pip install" in first and not first.lstrip().startswith("# Setup"):
            found.append("setup-comment: start the setup cell with a '# Setup:' comment")

    asserts = sum(learner_asserts(cell_source(c)) for c in code if not is_solution(c))
    if asserts and kind in {"lesson", "start", "reference", "interview"}:
        found.append(f"asserts: {asserts} assert line(s) in learner cells; show output instead")

    if kind == "lesson":
        if len(code) > 2 and "**What to notice:**" not in markdown:
            found.append("what-to-notice: add a **What to notice:** note after examples")
        if not re.search(r"^## Check yourself", markdown, re.M):
            found.append("check-yourself: add a '## Check yourself' section")
        if not re.search(r"^## Key takeaways", markdown, re.M):
            found.append("takeaways: add a '## Key takeaways' section")

    if kind == "practice":
        exercises = EXERCISE_RE.findall(markdown)
        difficulties = len(re.findall(r"\*\*Difficulty:\*\*", markdown))
        solutions = sum(1 for c in code if is_solution(c))
        if exercises and difficulties < len(exercises):
            found.append(f"difficulty: {len(exercises) - difficulties} exercise(s) without a **Difficulty:** line")
        if exercises and solutions < len(exercises):
            found.append(f"solutions: {len(exercises) - solutions} exercise(s) without a solution-tagged cell")
        if "<summary>" in markdown and "Show solution" in markdown:
            found.append("details-solution: move answers from <details> blocks into solution-tagged code cells")

    if kind != "reference" and not re.search(r"\*\*Next:\*\*|^## (?:Where to go next|Next)", markdown, re.M):
        found.append("next: end with a **Next:** link")
    return found


def key(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="notebooks to check (default: all)")
    parser.add_argument("--all", action="store_true", help="print every warning, including baselined ones")
    parser.add_argument("--update-baseline", action="store_true", help="rewrite the baseline")
    args = parser.parse_args()

    paths = notebook_paths(args.files)
    current = {key(p): warnings_for(p) for p in paths}

    if args.update_baseline:
        baseline = {k: [w.split(":")[0] for w in v] for k, v in sorted(current.items()) if v}
        BASELINE.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
        print(f"Baseline: {len(baseline)} notebook(s) with known warnings.")
        return 0

    baseline = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    new = 0
    clean = 0
    for name, found in current.items():
        allowed = set(baseline.get(name, []))
        extra = [w for w in found if w.split(":")[0] not in allowed]
        shown = found if args.all else extra
        if not found:
            clean += 1
        if shown:
            print(name)
            for warning in shown:
                print(f"  - {warning}")
        new += len(extra)
    stale = sorted(k for k in baseline if k in current and not current[k])
    print(f"\n{clean} of {len(current)} notebook(s) meet the standard; {len(current) - clean} have known warnings.")
    if stale:
        print(f"{len(stale)} notebook(s) now pass: run --update-baseline to drop them from the baseline.")
    if new:
        print(f"{new} warning(s) beyond the baseline.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
