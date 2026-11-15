#!/usr/bin/env python3
"""
Teaching-structure check for the notebooks (CONTRIBUTING.md, "The rules every notebook follows").

``audit_notebooks.py`` proves a notebook runs in Colab; this script checks that it teaches the house way:

- setup: a two-line setup cell (``# Setup:`` comment and one ``!pip install`` line), not the old ``PACKAGES`` cell
- lessons: examples show output instead of asserting it, at least one ``**What to notice:**`` note,
  ``## Check yourself``, ``## Key takeaways`` and a ``**Next:**`` link
- lessons, depth: notes in proportion to the examples (``notes-ratio``), at least two questions under Check
  yourself (``exercises``), three or more takeaways that do not repeat a Where it matters / Watch out for
  sentence (``takeaway-count``, ``takeaway-copied``), and those callouts under a topic heading rather than in
  Setup (``topic-callouts``)
- practice: a ``**Difficulty:**`` line under every exercise and a ``solution``-tagged answer cell for it
- every notebook: solution cells hold runnable code, not only ``print("<sentence>")`` (``prose-solution``), and
  no paragraph is pasted word for word across more than three notebooks in different folders (``boilerplate``)
- every notebook links onward with ``**Next:**`` except references

Presence alone is easy to satisfy: one note and a one-line Check yourself would pass on a 15,000-word notebook.
The depth rules exist so the check measures teaching, not formatting.

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
QUESTION_RE = re.compile(r"^(?:#{3,} |\d+\. |\*\*Q?\d+[.:)])", re.M)
CALLOUT_RE = re.compile(r"\*\*(?:Where it matters|Watch out for)\*\*")
EXEMPT_PARAGRAPH = re.compile(
    r"^(?:\*Author:|\[!\[Open In Colab|#+ |\*\*Next:\*\*"
    r"|\*\*(?:What to notice|Where it matters|Watch out for|Difficulty)\*\*:?$)"
)
BOILERPLATE_MIN_CHARS = 60
BOILERPLATE_MAX_NOTEBOOKS = 3


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


def paragraphs(markdown: str) -> list[str]:
    """Blank-line separated paragraphs long enough to count as copied prose."""
    out = []
    for block in re.split(r"\n\s*\n", markdown):
        block = block.strip()
        if len(block) >= BOILERPLATE_MIN_CHARS and not EXEMPT_PARAGRAPH.match(block):
            out.append(block)
    return out


def teaching_text(cells: list[dict]) -> str:
    """Markdown outside Check yourself, whose shared instructions ("Answer each question...") are conventions.

    A pasted Check yourself prompt is caught by the ``exercises`` rule instead.
    """
    located = sections(cells)
    return "\n\n".join(
        cell_source(c) for h, c in located if c.get("cell_type") == "markdown" and not h.startswith("Check yourself")
    )


def repeated_paragraphs(paths: list[Path]) -> set[str]:
    """Paragraphs found word for word in more than three notebooks spread over more than one folder.

    Repeats inside one folder are course conventions (the SQL course's "Write each query..." line); repeats across
    folders are templates pasted in place of notebook-specific teaching.
    """
    seen: dict[str, set[Path]] = {}
    for path in paths:
        cells = json.loads(path.read_text(encoding="utf-8")).get("cells") or []
        for paragraph in set(paragraphs(teaching_text(cells))):
            seen.setdefault(paragraph, set()).add(path)
    return {
        paragraph
        for paragraph, where in seen.items()
        if len(where) > BOILERPLATE_MAX_NOTEBOOKS and len({p.parent for p in where}) > 1
    }


def is_prose_solution(source: str) -> bool:
    """A solution cell that only prints string literals: an answer you cannot run against your own."""
    try:
        body = ast.parse(source).body
    except SyntaxError:
        return False
    return bool(body) and all(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "print"
        and all(isinstance(arg, ast.Constant) and isinstance(arg.value, str) for arg in node.value.args)
        for node in body
    )


def sections(cells: list[dict]) -> list[tuple[str, dict]]:
    """Each cell with the ``## `` heading it sits under (the heading's own cell included)."""
    heading = ""
    out = []
    for cell in cells:
        if cell.get("cell_type") == "markdown":
            for line in cell_source(cell).splitlines():
                if line.startswith("## "):
                    heading = line[3:].strip()
                    break
        out.append((heading, cell))
    return out


def is_example(cell: dict, heading: str, index: int) -> bool:
    """A code cell that teaches: not setup, not a solution, not exercise scaffolding, not comments only."""
    if cell.get("cell_type") != "code" or is_solution(cell) or heading.startswith("Check yourself"):
        return False
    source = cell_source(cell)
    if index == 0 and ("!pip" in source or source.lstrip().startswith("# Setup")):
        return False
    return any(line.strip() and not line.strip().startswith("#") for line in source.splitlines())


def section_markdown(located: list[tuple[str, dict]], heading: str) -> str:
    return "\n".join(cell_source(c) for h, c in located if h.startswith(heading) and c.get("cell_type") == "markdown")


def depth_warnings(cells: list[dict], markdown: str) -> list[str]:
    found: list[str] = []
    located = sections(cells)
    code_index = {id(c): i for i, c in enumerate(c for c in cells if c.get("cell_type") == "code")}
    examples = sum(1 for h, c in located if is_example(c, h, code_index.get(id(c), -1)))
    notes = markdown.count("**What to notice:**")
    needed = examples // 2
    if notes and notes < needed:
        found.append(f"notes-ratio: {notes} What to notice note(s) for {examples} examples; aim for at least {needed}")

    check = section_markdown(located, "Check yourself")
    if check:
        questions = len(QUESTION_RE.findall(check))
        if questions < 2:
            found.append(f"exercises: {questions} question(s) under Check yourself; add at least 2")

    takeaways = section_markdown(located, "Key takeaways")
    if takeaways:
        bullets = [b.strip() for b in re.findall(r"^\s*[-*] (.+)$", takeaways, re.M)]
        if len(bullets) < 3:
            found.append(f"takeaway-count: {len(bullets)} takeaway(s); summarise the lesson in at least 3")
        callouts = set()
        for cell in cells:
            if cell.get("cell_type") != "markdown":
                continue
            parts = re.split(r"\n\s*\n", cell_source(cell))
            for i, part in enumerate(parts[:-1]):
                if CALLOUT_RE.fullmatch(part.strip()):
                    callouts.add(parts[i + 1].strip())
        copied = sum(1 for b in bullets if b in callouts)
        if copied:
            found.append(f"takeaway-copied: {copied} takeaway(s) repeat a Where it matters / Watch out for paragraph")

    setup = section_markdown(located, "Setup and sample data")
    if CALLOUT_RE.search(setup):
        found.append("topic-callouts: move Where it matters / Watch out for from Setup to the topics they describe")
    return found


def warnings_for(path: Path, repeated: set[str] | None = None) -> list[str]:
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
        found.extend(depth_warnings(cells, markdown))

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

    prose = sum(1 for c in code if is_solution(c) and is_prose_solution(cell_source(c)))
    if prose:
        found.append(f"prose-solution: {prose} solution cell(s) only print a sentence; solve it in code")

    if repeated:
        copies = [p for p in paragraphs(teaching_text(cells)) if p in repeated]
        if copies:
            found.append(f"boilerplate: {len(copies)} paragraph(s) pasted across notebooks, e.g. {copies[0][:70]!r}")

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
    repeated = repeated_paragraphs(notebook_paths([]))  # boilerplate is judged against the whole handbook
    current = {key(p): warnings_for(p, repeated) for p in paths}

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
