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
        md("## Check yourself\n\n1. Why?"),
        md("## Key takeaways\n\n- One."),
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
