"""Unit tests for the notebook formatter and the Colab-runnability audit."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SITE_CONFIG = ROOT / "site" / "lib" / "site.ts"
sys.path.insert(0, str(SCRIPTS))

import audit_notebooks  # noqa: E402
import notebook_format  # noqa: E402
import run_notebooks  # noqa: E402

RELPATH = "notebooks/example/example.ipynb"


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
        assert "watermark" not in result["metadata"]
        assert "kernelspec" in result["metadata"]
        assert result["nbformat_minor"] == 5

    def test_solution_tag_is_kept_and_other_cell_metadata_is_dropped(self):
        tagged = code("assert 1 == 1", metadata={"tags": ["solution"], "collapsed": True})
        result = notebook_format.format_notebook(notebook(md("# T"), tagged), RELPATH)
        assert result["cells"][1]["metadata"] == {"tags": ["solution"]}

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

    def test_broken_links_ignore_urls_and_anchors(self, tmp_path):
        (tmp_path / "exists.ipynb").write_text("{}")
        text = "[a](exists.ipynb) [b](missing.ipynb) [c](https://x.org) [d](#top)"
        assert audit_notebooks.broken_links(text, tmp_path / "nb.ipynb") == ["missing.ipynb"]


def write_formatted(tmp_path: Path, monkeypatch, *cells: dict) -> Path:
    monkeypatch.setattr(audit_notebooks, "ROOT", tmp_path)
    path = tmp_path / "notebooks" / "example" / "example.ipynb"
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

    def test_setup_cell_may_import_the_packages_it_installs(self, tmp_path, monkeypatch):
        setup = 'import importlib.util\nPACKAGES = {"duckdb": "duckdb>=1.0"}\nimport packaging'
        path = write_formatted(tmp_path, monkeypatch, md("# T"), code(setup))
        errors, _ = audit_notebooks.audit(path)
        assert errors == []

    def test_notebook_with_leftover_outputs_is_reported(self, tmp_path, monkeypatch):
        path = write_formatted(tmp_path, monkeypatch, md("# T"), code("print(1)"))
        dirty = notebook_format.format_notebook(notebook(md("# T"), code("print(1)")), RELPATH)
        dirty["cells"][1]["outputs"] = [{"output_type": "stream", "name": "stdout", "text": ["1\n"]}]
        path.write_text(json.dumps(dirty, indent=1), encoding="utf-8")
        errors, _ = audit_notebooks.audit(path)
        assert any("make format" in error for error in errors)


def site_constant(name: str) -> str:
    """Value of ``export const <name> = "..."`` in the site's shared config."""
    match = re.search(rf'export const {name} = "([^"]+)";', SITE_CONFIG.read_text(encoding="utf-8"))
    assert match, f"{name} is not declared in site/lib/site.ts"
    return match.group(1)


def test_python_and_site_agree_on_repository_branch_and_author():
    # The formatter writes these into every notebook; the site links to them. Drift breaks Colab links.
    assert notebook_format.REPOSITORY == site_constant("repository")
    assert notebook_format.BRANCH == site_constant("branch")
    assert notebook_format.AUTHOR_NAME == site_constant("authorName")


class TestPipInstallLines:
    def test_pip_install_declares_the_package_it_names(self, tmp_path, monkeypatch):
        path = write_formatted(
            tmp_path, monkeypatch, md("# T"), code("!pip install -q pyspark"), code("import pyspark")
        )
        errors, _ = audit_notebooks.audit(path)
        assert errors == []

    def test_other_imports_are_still_reported_next_to_a_pip_line(self, tmp_path, monkeypatch):
        path = write_formatted(tmp_path, monkeypatch, md("# T"), code("!pip install -q pyspark"), code("import duckdb"))
        errors, _ = audit_notebooks.audit(path)
        assert any("duckdb" in error for error in errors), errors


class TestTrimOutputs:
    @staticmethod
    def trimmed(*outputs: dict, source: str = "print(1)") -> list[dict]:
        cell = code(source, outputs=list(outputs))
        return run_notebooks.trim_outputs(notebook(cell))["cells"][0]["outputs"]

    def test_setup_cell_outputs_are_dropped(self):
        stream = {"output_type": "stream", "name": "stdout", "text": "Installing duckdb\n"}
        assert self.trimmed(stream, source="# Setup: installs packages\nprint(1)") == []

    def test_html_is_dropped_in_favour_of_plain_text(self):
        result = {
            "output_type": "execute_result",
            "execution_count": 3,
            "data": {"text/html": "<table></table>", "text/plain": "   a\n0  1"},
            "metadata": {"x": 1},
        }
        assert self.trimmed(result) == [
            {
                "output_type": "execute_result",
                "execution_count": 3,
                "data": {"text/plain": "   a\n0  1"},
                "metadata": {},
            }
        ]

    def test_long_text_is_cut_and_says_how_much(self):
        text = "".join(f"row {n}\n" for n in range(run_notebooks.MAX_OUTPUT_LINES + 5))
        [stream] = self.trimmed({"output_type": "stream", "name": "stdout", "text": text})
        assert stream["text"].count("\n") == run_notebooks.MAX_OUTPUT_LINES + 1
        assert stream["text"].endswith("… output trimmed (5 more lines)\n")

    def test_ansi_colour_codes_are_removed_and_blank_streams_dropped(self):
        coloured = {"output_type": "stream", "name": "stderr", "text": "\x1b[31mWARN\x1b[0m slow\n"}
        blank = {"output_type": "stream", "name": "stdout", "text": "\n"}
        assert self.trimmed(coloured, blank) == [{"output_type": "stream", "name": "stderr", "text": "WARN slow\n"}]

    def test_errors_keep_name_and_message_without_traceback(self):
        error = {"output_type": "error", "ename": "ValueError", "evalue": "bad", "traceback": ["\x1b[0;31m..."]}
        assert self.trimmed(error) == [
            {"output_type": "error", "ename": "ValueError", "evalue": "bad", "traceback": []}
        ]

    def test_oversized_image_falls_back_to_text(self):
        big = "A" * (run_notebooks.MAX_IMAGE_BASE64_CHARS + 1)
        display = {"output_type": "display_data", "data": {"image/png": big, "text/plain": "<Figure>"}, "metadata": {}}
        assert self.trimmed(display)[0]["data"] == {"text/plain": "<Figure>"}

    def test_short_text_is_unchanged(self):
        assert run_notebooks.truncate_text("ok\n") == "ok\n"


def test_run_one_saves_an_executed_copy_with_trimmed_outputs(tmp_path, monkeypatch):
    pytest.importorskip("nbclient")
    pytest.importorskip("ipykernel")
    source = tmp_path / "notebooks" / "demo.ipynb"
    source.parent.mkdir()
    cells = [md("# Demo"), code("# Setup: installs packages\nprint('installing')"), code("print('hello')\n1 + 1")]
    for index, cell in enumerate(cells):
        cell["id"] = f"c{index}"
    source.write_text(json.dumps({**notebook(*cells), "nbformat_minor": 5}))
    monkeypatch.setattr(run_notebooks, "ROOT", tmp_path)

    relpath, error, _ = run_notebooks.run_one(source, timeout=60, output_dir=tmp_path / "out")

    assert error is None
    saved = json.loads((tmp_path / "out" / relpath).read_text())
    assert saved["cells"][1]["outputs"] == []
    assert [o["output_type"] for o in saved["cells"][2]["outputs"]] == ["stream", "execute_result"]
    assert json.loads(source.read_text())["cells"][2]["outputs"] == []


def test_jvm_log_noise_is_dropped_from_stderr_only():
    noisy = (
        "Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties\n"
        "26/11/10 04:08:53 WARN Utils: Your hostname, box.local, resolves to a loopback address\n"
        '{"ts": "2026-11-10 04:09:00.000", "level": "ERROR", "logger": "SQLQueryContextLogger", "msg": "x"}\n'
        "[Stage 3:>        (0 + 2) / 2]\r                \r"
        "UserWarning: real warning\n"
    )
    stderr = {"output_type": "stream", "name": "stderr", "text": noisy}
    stdout = {"output_type": "stream", "name": "stdout", "text": "26/11/10 04:08:53 WARN printed on purpose\n"}
    result = TestTrimOutputs.trimmed(stderr, stdout)
    assert result[0]["text"] == "UserWarning: real warning\n"
    assert result[1]["text"] == stdout["text"]


def test_empty_dataframe_results_are_dropped():
    empty = {
        "output_type": "execute_result",
        "execution_count": 1,
        "data": {"text/plain": "DataFrame[]"},
        "metadata": {},
    }
    schema = {**empty, "data": {"text/plain": "DataFrame[id: bigint]"}}
    assert [o["data"]["text/plain"] for o in TestTrimOutputs.trimmed(empty, schema)] == ["DataFrame[id: bigint]"]
