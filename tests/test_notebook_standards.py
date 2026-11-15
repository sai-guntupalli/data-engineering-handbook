"""Unit tests for the teaching-structure check (scripts/notebook_standards.py)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import notebook_standards  # noqa: E402


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def code(text: str, tags: list[str] | None = None) -> dict:
    meta = {"tags": tags} if tags else {}
    return {"cell_type": "code", "metadata": meta, "source": text, "outputs": [], "execution_count": None}


def write(tmp_path: Path, name: str, *cells: dict) -> Path:
    path = tmp_path / f"{name}.ipynb"
    path.write_text(json.dumps({"cells": list(cells), "metadata": {}, "nbformat": 4, "nbformat_minor": 4}))
    return path


SETUP = code("# Setup: installs packages.\n!pip install -q duckdb")


def codes(warnings: list[str]) -> set[str]:
    return {w.split(":")[0] for w in warnings}


def test_a_lesson_that_follows_the_standard_has_no_warnings(tmp_path):
    path = write(
        tmp_path,
        "tool-01-basics",
        md("# Tool 1: basics"),
        SETUP,
        code("print(1)"),
        code("print(2)"),
        md("**What to notice:** the 1."),
        md("## Check yourself\n\n1. Why?\n2. Why not?"),
        md("## Key takeaways\n\n- One.\n- Two.\n- Three."),
        md("**Next:** [Tool 2](tool-02.ipynb)"),
    )
    assert notebook_standards.warnings_for(path) == []


def test_old_setup_asserts_and_missing_sections_are_reported(tmp_path):
    path = write(
        tmp_path,
        "tool",
        md("# Tool"),
        code('PACKAGES = {"duckdb": "duckdb"}'),
        code("x = 1\nassert x == 1"),
        code("print(x)"),
    )
    assert codes(notebook_standards.warnings_for(path)) == {
        "long-setup",
        "asserts",
        "what-to-notice",
        "check-yourself",
        "takeaways",
        "next",
    }


def test_asserts_inside_test_functions_are_the_lesson(tmp_path):
    path = write(tmp_path, "tool", md("# Tool"), code("def test_total():\n    assert 1 + 1 == 2\n\ntest_total()"))
    assert "asserts" not in codes(notebook_standards.warnings_for(path))


def test_practice_needs_difficulty_and_tagged_solutions(tmp_path):
    path = write(
        tmp_path,
        "tool-drills",
        md("# Tool drills"),
        md("## Exercise 1: one\n\n**Difficulty:** Easy · about 5 min"),
        code("# your code"),
        code("print(1)", tags=["solution"]),
        md("## Exercise 2: two"),
        code("# your code"),
        md("<details>\n<summary>Show solution</summary>\n\n```python\nx\n```\n</details>"),
    )
    assert codes(notebook_standards.warnings_for(path)) == {"difficulty", "solutions", "details-solution", "next"}


def test_kind_follows_the_file_name():
    assert notebook_standards.kind_of(Path("sql-00-start-here.ipynb")) == "start"
    assert notebook_standards.kind_of(Path("sql-reference.ipynb")) == "reference"
    assert notebook_standards.kind_of(Path("pyspark-drills-06-joins.ipynb")) == "practice"
    assert notebook_standards.kind_of(Path("sql-14-interview-concepts.ipynb")) == "interview"
    assert notebook_standards.kind_of(Path("kafka-02-producers.ipynb")) == "lesson"


THREE = "- One.\n- Two.\n- Three."


def lesson(tmp_path: Path, *body: dict, name: str = "tool-01-basics", takeaways: str = THREE) -> Path:
    """A lesson that passes every rule apart from what ``body`` changes."""
    return write(
        tmp_path,
        name,
        md("# Tool 1: basics"),
        SETUP,
        *body,
        md("## Check yourself\n\n### Exercise 1\n\nOne?"),
        code("# Try it here."),
        code("print(sum([1, 2]))", tags=["solution"]),
        md("### Exercise 2\n\nTwo?"),
        md(f"## Key takeaways\n\n{takeaways}"),
        md("**Next:** [Tool 2](tool-02.ipynb)"),
    )


def test_notes_must_keep_up_with_the_examples(tmp_path):
    examples = [code(f"print({i})") for i in range(8)]
    sparse = lesson(tmp_path, md("## Topic"), *examples, md("**What to notice:** one note."))
    assert "notes-ratio" in codes(notebook_standards.warnings_for(sparse))
    dense = [cell for i, ex in enumerate(examples) for cell in ([ex, md("**What to notice:** x.")] if i % 2 else [ex])]
    path = lesson(tmp_path, md("## Topic"), *dense, name="tool-02-dense")
    assert "notes-ratio" not in codes(notebook_standards.warnings_for(path))


def test_check_yourself_needs_two_questions(tmp_path):
    path = write(
        tmp_path,
        "tool-01-basics",
        md("# Tool"),
        md("## Check yourself\n\nChoose a worked example and change its filter."),
        md("## Key takeaways\n\n- One.\n- Two.\n- Three."),
        md("**Next:** [x](x.ipynb)"),
    )
    assert "exercises" in codes(notebook_standards.warnings_for(path))


def test_takeaways_need_three_bullets_that_are_not_copied_callouts(tmp_path):
    callout = "Store results under deterministic keys."
    path = lesson(
        tmp_path,
        md(f"## Caching\n\nText.\n\n**Where it matters**\n\n{callout}"),
        takeaways=f"- {callout}",
    )
    assert {"takeaway-count", "takeaway-copied"} <= codes(notebook_standards.warnings_for(path))


def test_callouts_belong_under_topics_not_setup(tmp_path):
    path = lesson(tmp_path, md("## Setup and sample data\n\n**Where it matters**\n\nEverywhere."))
    assert "topic-callouts" in codes(notebook_standards.warnings_for(path))
    path = lesson(tmp_path, md("## Setup and sample data\n\nData."), md("## Joins\n\n**Where it matters**\n\nReports."))
    assert "topic-callouts" not in codes(notebook_standards.warnings_for(path))


def test_solution_cells_must_be_code_not_a_printed_sentence(tmp_path):
    assert notebook_standards.is_prose_solution('print("No. The filter assumes ordered input.")')
    assert not notebook_standards.is_prose_solution("print(committed[0])")
    assert not notebook_standards.is_prose_solution('total = 1 + 2\nprint("total", total)')
    path = write(
        tmp_path,
        "tool-drills",
        md("# Drills"),
        md("## Exercise 1\n\n**Difficulty:** Easy"),
        code('print("It depends.")', tags=["solution"]),
        md("**Next:** [x](x.ipynb)"),
    )
    assert codes(notebook_standards.warnings_for(path)) == {"prose-solution"}


def test_boilerplate_is_a_paragraph_pasted_across_folders(tmp_path):
    pasted = "Each runnable example declares its input alongside the operation it illustrates, in fenced text."
    paths = []
    for folder in ("a", "b", "c", "d"):
        (tmp_path / folder).mkdir()
        paths.append(write(tmp_path / folder, "tool", md(f"# {folder}\n\n{pasted}")))
    assert notebook_standards.repeated_paragraphs(paths) == {pasted}
    warnings = notebook_standards.warnings_for(paths[0], {pasted})
    assert "boilerplate" in codes(warnings)

    (tmp_path / "course").mkdir()
    same_folder = [write(tmp_path / "course", f"sql-0{i}", md(f"# {i}\n\n{pasted}")) for i in range(5)]
    assert notebook_standards.repeated_paragraphs(same_folder) == set()


def test_shared_check_yourself_instructions_are_not_boilerplate(tmp_path):
    line = "Answer each question in your own words before reading the answer that follows it."
    paths = []
    for folder in ("a", "b", "c", "d"):
        (tmp_path / folder).mkdir()
        paths.append(write(tmp_path / folder, "tool", md(f"## Check yourself\n\n{line}")))
    assert notebook_standards.repeated_paragraphs(paths) == set()
