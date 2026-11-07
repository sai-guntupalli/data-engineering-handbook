"""Unit tests for the notebook formatter and the Colab-runnability audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import audit_notebooks  # noqa: E402
import notebook_format  # noqa: E402

RELPATH = "notebooks/topics/example.ipynb"


def md(text: str, **extra) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text, **extra}


def code(text: str, **extra) -> dict:
    return {"cell_type": "code", "metadata": {}, "source": text, "outputs": [], "execution_count": None, **extra}


def notebook(*cells: dict) -> dict:
    return {"cells": list(cells), "metadata": {"watermark": {"author": "x"}}, "nbformat": 4, "nbformat_minor": 4}


SETUP = 'PACKAGES = {"duckdb": "duckdb>=1.0"}\nprint("ready")'


class TestFormatNotebook:
    def test_opening_cell_gets_title_credit_and_colab_badge(self):
        result = notebook_format.format_notebook(notebook(md("# Kafka\n\nIntro text.")), RELPATH)
        opening = "".join(result["cells"][0]["source"])
        lines = opening.split("\n")
        assert lines[0] == "# Kafka"
        assert notebook_format.CREDIT_LINE in opening
        assert notebook_format.colab_url(RELPATH) in opening
        assert opening.rstrip().endswith("Intro text.")

    def test_old_credit_line_is_replaced_not_duplicated(self):
        old = "# Kafka\n\n*Author: [Someone](https://example.com) · [repo](https://example.com)*\n\nBody"
        result = notebook_format.format_notebook(notebook(md(old)), RELPATH)
        opening = "".join(result["cells"][0]["source"])
        assert opening.count("*Author: [") == 1
        assert "Someone" not in opening

    def test_title_cell_is_inserted_when_notebook_starts_with_code(self):
        result = notebook_format.format_notebook(notebook(code("x = 1")), RELPATH)
        assert result["cells"][0]["cell_type"] == "markdown"
        assert "".join(result["cells"][0]["source"]).startswith("# example")

    def test_outputs_counts_and_metadata_are_stripped(self):
        dirty = code("print(1)", outputs=[{"output_type": "stream", "text": "1"}], execution_count=7)
        dirty["metadata"] = {"collapsed": True}
        result = notebook_format.format_notebook(notebook(md("# T"), dirty), RELPATH)
        cell = result["cells"][1]
        assert cell["outputs"] == [] and cell["execution_count"] is None and cell["metadata"] == {}
        assert result["metadata"] == notebook_format.CANONICAL_METADATA
        assert result["nbformat_minor"] == 5

    def test_how_to_use_boilerplate_cell_is_removed(self):
        boiler = md("*How to use this notebook.* Read the cells and run them.")
        result = notebook_format.format_notebook(notebook(md("# T"), boiler, md("Real content")), RELPATH)
        sources = ["".join(cell["source"]) for cell in result["cells"]]
        assert len(sources) == 2 and sources[1] == "Real content"

    def test_ids_are_stable_unique_and_existing_ones_kept(self):
        nb = notebook(md("# T"), code("a = 1", id="keepme"), code("b = 2", id="keepme"))
        first = notebook_format.format_notebook(nb, RELPATH)
        second = notebook_format.format_notebook(nb, RELPATH)
        ids = [cell["id"] for cell in first["cells"]]
        assert ids == [cell["id"] for cell in second["cells"]]
        assert ids[1] == "keepme" and len(set(ids)) == 3

    def test_formatting_is_idempotent(self):
        once = notebook_format.format_notebook(notebook(md("# T\n\nIntro"), code("x = 1")), RELPATH)
        twice = notebook_format.format_notebook(json.loads(notebook_format.serialize(once)), RELPATH)
        assert notebook_format.serialize(once) == notebook_format.serialize(twice)


class TestAuditHelpers:
    def test_headings_inside_code_fences_are_ignored(self):
        text = "## Real\n```bash\n# a shell comment\n```\n### Sub"
        assert audit_notebooks.markdown_headings(text) == [2, 3]

    def test_setup_packages_reads_the_mapping(self):
        assert audit_notebooks.setup_packages(["import os", SETUP]) == {"duckdb": "duckdb>=1.0"}
        assert audit_notebooks.setup_packages(["import os"]) is None

    def test_third_party_imports_skip_stdlib_and_relative(self):
        source = "import json, duckdb\nfrom pyspark.sql import functions\nfrom . import local\nimport os.path"
        assert audit_notebooks.third_party_imports(source) == {"duckdb", "pyspark"}

    def test_local_modules_written_by_the_notebook_count_as_provided(self):
        assert audit_notebooks.local_modules(['Path("orders.py").write_text(code)']) == {"orders"}

    def test_broken_links_ignore_urls_and_anchors(self, tmp_path):
        (tmp_path / "exists.ipynb").write_text("{}")
        text = "[a](exists.ipynb) [b](missing.ipynb) [c](https://x.org) [d](#top)"
        assert audit_notebooks.broken_links(text, tmp_path / "nb.ipynb") == ["missing.ipynb"]


def write_formatted(tmp_path: Path, monkeypatch, *cells: dict) -> Path:
    monkeypatch.setattr(audit_notebooks, "ROOT", tmp_path)
    path = tmp_path / "notebooks" / "topics" / "example.ipynb"
    path.parent.mkdir(parents=True)
    formatted = notebook_format.format_notebook(notebook(*cells), RELPATH)
    path.write_text(notebook_format.serialize(formatted), encoding="utf-8")
    return path


class TestAudit:
    def test_clean_notebook_passes(self, tmp_path, monkeypatch):
        path = write_formatted(tmp_path, monkeypatch, md("# T"), code(SETUP), md("## Use"), code("import duckdb"))
        errors, counts = audit_notebooks.audit(path)
        assert errors == []
        assert counts["code"] == 2

    @pytest.mark.parametrize(
        ("cells", "expected"),
        [
            ((md("# T"), code("import duckdb")), "missing from the setup cell"),
            ((md("# T"), code("# ILLUSTRATIVE - needs Kafka\nx = 1")), "ILLUSTRATIVE"),
            ((md("# T"), code('url = "localhost:9200"')), "local server"),
            ((md("# T"), code("%pip install duckdb")), "magic"),
            ((md("# T"), md("# Second title")), "exactly one"),
            ((md("# T"), md("#### Too deep")), "skips from heading level 1 to 4"),
            ((md("# T"), md("```python\nx = 1")), "unbalanced code fences"),
            ((md("# T"), code("def broken(:")), "syntax error"),
        ],
    )
    def test_rule_violations_are_reported(self, tmp_path, monkeypatch, cells, expected):
        path = write_formatted(tmp_path, monkeypatch, *cells)
        errors, _ = audit_notebooks.audit(path)
        assert any(expected in error for error in errors), errors

    def test_unformatted_notebook_is_reported(self, tmp_path, monkeypatch):
        path = write_formatted(tmp_path, monkeypatch, md("# T"))
        path.write_text(path.read_text().replace('"nbformat_minor": 5', '"nbformat_minor": 4'))
        errors, _ = audit_notebooks.audit(path)
        assert any("make format" in error for error in errors)
