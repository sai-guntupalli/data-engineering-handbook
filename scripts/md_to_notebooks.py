#!/usr/bin/env python3
"""
Convert every tracked Markdown document into a Google Colab friendly notebook.

The repository keeps Markdown as the authoring source, but notebooks are the
execution surface. Generated notebooks mirror the Markdown path:

  content/spark.md       -> notebooks/topics/spark.ipynb
  content/full.md        -> notebooks/topics/full.ipynb
  README.md              -> notebooks/from-md/README.ipynb
  CONTRIBUTING.md        -> notebooks/from-md/CONTRIBUTING.ipynb
  notebooks/README.md    -> notebooks/from-md/notebooks/README.ipynb

Python/PySpark fences become code cells. Shell fences become %%bash cells. SQL
fences become %%sql cells and the generated setup cell loads ipython-sql against
an in-memory SQLite database. Platform-specific snippets may still need tables,
credentials, Spark, Databricks, AWS, or another runtime, but the notebook cells
are executable Colab cells instead of an app wrapper.

Usage:
  python3 scripts/md_to_notebooks.py            # regenerate generated notebooks
  python3 scripts/md_to_notebooks.py --check    # fail if notebooks are stale
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
NOTEBOOKS_DIR = ROOT / "notebooks"
TOPICS_DIR = NOTEBOOKS_DIR / "topics"
FROM_MD_DIR = NOTEBOOKS_DIR / "from-md"
REPO_URL = "https://github.com/sai-guntupalli/data-engineering-interview-questions"

PYTHON_LANGS = {"python", "py", "python3", "pyspark"}
SHELL_LANGS = {"bash", "sh", "shell", "zsh"}
SQL_LANGS = {"sql"}

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

DEPENDENCY_HINTS: dict[str, list[str]] = {
    "airflow": ["apache-airflow"],
    "aws": ["boto3", "pyspark"],
    "azure": ["pyspark"],
    "databricks": ["pyspark"],
    "delta": ["delta-spark", "pyspark"],
    "gcp": ["google-cloud-storage", "pyspark"],
    "hudi": ["pyspark"],
    "iceberg": ["pyspark"],
    "parquet": ["pandas", "pyarrow", "pyspark"],
    "spark": ["pyspark"],
    "spark-tuning": ["pyspark"],
}

INTRO = (
    "*Generated from `{source_path}` for Google Colab.* Markdown explanations are preserved, and fenced examples are "
    "converted into executable notebook cells wherever a Python kernel can run them. Some cells still require the "
    "right data, tables, credentials, Java runtime, Spark runtime, or cloud account before they can succeed."
)


def markdown_cell(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.strip("\n").splitlines(keepends=True)}


def markdown_cells(source: str) -> list[dict]:
    """Split prose into small notebook-friendly markdown cells."""
    source = source.strip("\n")
    if not source.strip():
        return []

    blocks: list[str] = []
    current: list[str] = []
    for line in source.splitlines():
        if line.strip():
            current.append(line)
            continue
        if current:
            blocks.append("\n".join(current))
            current = []
    if current:
        blocks.append("\n".join(current))

    split_blocks: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) > 1 and re.match(r"^#{1,6}\s+", lines[0]):
            split_blocks.append(lines[0])
            rest = "\n".join(lines[1:]).strip()
            if rest:
                split_blocks.append(rest)
        else:
            split_blocks.append(block)

    return [markdown_cell(block) for block in split_blocks if block.strip()]


def code_cell(source: str, metadata: dict | None = None) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": metadata or {},
        "outputs": [],
        "source": source.strip("\n").splitlines(keepends=True),
    }


def _as_cell_list(cell: dict) -> dict:
    source = cell.get("source", "")
    if isinstance(source, str):
        cell["source"] = source.splitlines(keepends=True)
    cell.setdefault("metadata", {})
    cell["execution_count"] = None if cell.get("cell_type") == "code" else cell.get("execution_count")
    if cell.get("cell_type") == "code":
        cell["outputs"] = []
    return cell


def tracked_markdown_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "*.md"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        files = [ROOT / line for line in result.stdout.splitlines() if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = [
            path
            for path in ROOT.rglob("*.md")
            if "node_modules" not in path.parts and ".next" not in path.parts and "site" not in path.parts
        ]
    return sorted(files)


def notebook_target(source: Path) -> Path:
    rel = source.relative_to(ROOT)
    if rel.parts[0] == "content":
        return TOPICS_DIR / f"{source.stem}.ipynb"
    return FROM_MD_DIR / rel.with_suffix(".ipynb")


def colab_url(target: Path) -> str:
    rel = target.relative_to(ROOT).as_posix()
    return f"https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/{rel}"


def _is_house_style_noise(line: str) -> bool:
    return (
        line.startswith("## [Main title]")
        or line.startswith("### [Interview questions]")
        or line.startswith("[Table of Contents]")
        or line.startswith("**Notebook:**")
        or line.startswith("+ [")
    )


def fence_to_cell(language: str, code: str) -> dict:
    language = language.split()[0].lower() if language else ""
    if language in PYTHON_LANGS:
        return code_cell(code)
    if language in SHELL_LANGS:
        return code_cell(f"%%bash\n{code}", {"tags": ["shell"]})
    if language in SQL_LANGS:
        return code_cell(f"%%sql\n{code}", {"tags": ["sql"]})
    return markdown_cells(f"```{language}\n{code}\n```")[0]


def parse_document(text: str, source: Path) -> tuple[str, list[dict]]:
    title = source.stem.replace("-", " ").replace("_", " ").title()
    cells: list[dict] = []
    buffer: list[str] = []
    title_seen = False

    def flush() -> None:
        block = "\n".join(buffer).strip("\n")
        buffer.clear()
        if block.strip():
            cells.extend(markdown_cells(block))

    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]

        if line.startswith("```"):
            language = line[3:].strip()
            body: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                body.append(lines[index])
                index += 1
            index += 1
            flush()
            cells.append(fence_to_cell(language, "\n".join(body)))
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
            flush()
            buffer.append(line)
            index += 1
            continue

        buffer.append(line)
        index += 1

    flush()
    return title, cells


def infer_dependencies(slug: str, cells: list[dict]) -> list[str]:
    dependencies = set(DEPENDENCY_HINTS.get(slug, []))
    source = "\n".join("".join(cell.get("source", [])) for cell in cells if cell.get("cell_type") == "code")
    if "%%sql" in source:
        dependencies.add("ipython-sql")
    if "pyspark" in source or "SparkSession" in source or "spark." in source:
        dependencies.add("pyspark")
    if "import pandas" in source or "from pandas" in source:
        dependencies.add("pandas")
    if "pyarrow" in source:
        dependencies.add("pyarrow")
    if "boto3" in source:
        dependencies.add("boto3")
    return sorted(dependencies)


def setup_cell(dependencies: list[str]) -> dict:
    packages = ", ".join(repr(dep) for dep in dependencies)
    installable = [dep for dep in dependencies if dep not in {"sqlite3"}]
    install_line = " ".join(installable)
    install_hint = f"!pip -q install {install_line}" if installable else "# No pip installs detected."
    module_names = {
        "apache-airflow": "airflow",
        "delta-spark": "delta",
        "google-cloud-storage": "google.cloud.storage",
        "ipython-sql": "sql",
    }
    module_map = ", ".join(f"{package!r}: {module!r}" for package, module in module_names.items())
    source = f"""# Colab setup: run this cell first.
import importlib.util
import sys

required_packages = [{packages}]
package_modules = {{{module_map}}}
print("Python:", sys.version.split()[0])

for package in required_packages:
    module = package_modules.get(package, package.split("-")[0])
    status = "available" if importlib.util.find_spec(module) else "missing"
    print(f"{{package:22}} {{status}}")

print("\\nIf a required package is missing, run:")
print({install_hint!r})

if "ipython-sql" in required_packages:
    try:
        get_ipython().run_line_magic("load_ext", "sql")
    except Exception:
        print("Install ipython-sql, restart the runtime if needed, then rerun this setup cell.")
    else:
        get_ipython().run_line_magic("sql", "sqlite://")
        print("SQL magic connected to an in-memory SQLite database.")
"""
    return code_cell(source, {"tags": ["colab-setup"]})


def header_cells(title: str, source: Path, target: Path, cells: list[dict]) -> list[dict]:
    markdown_count = sum(1 for cell in cells if cell.get("cell_type") == "markdown")
    code_count = sum(1 for cell in cells if cell.get("cell_type") == "code")
    dependencies = infer_dependencies(source.stem, cells)
    dependency_text = ", ".join(f"`{dep}`" for dep in dependencies) if dependencies else "standard library only"
    source_path = source.relative_to(ROOT).as_posix()
    return [
        markdown_cell(
            f"# {title}\n\n"
            f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url(target)})"
        ),
        markdown_cell(INTRO.format(source_path=source_path)),
        markdown_cell("## How to run"),
        markdown_cell(
            "- Open this notebook in Google Colab using the badge above.\n"
            "- Run the setup cell first.\n"
            "- Run cells one by one and replace sample table names, file paths, credentials, and cloud resources with your own.\n"
            "- SQL cells use `%%sql` with an in-memory SQLite connection unless you configure another database.\n"
            "- PySpark cells need `pyspark` and Java. Colab usually has Java; install PySpark from the setup hint if missing."
        ),
        markdown_cell(
            f"Notebook inventory: **{markdown_count} markdown cells**, **{code_count} code cells**. "
            f"Detected dependencies: {dependency_text}."
        ),
        setup_cell(dependencies),
    ]


def merge_practice_cells(slug: str, cells: list[dict]) -> list[dict]:
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
                f"The cells below are from `notebooks/{filename}` and are merged here so this Colab notebook is "
                "self-contained. Run them top to bottom; assertions confirm the expected behavior."
            )
        )
        for cell in notebook.get("cells", []):
            merged.append(_as_cell_list(cell))
    return cells + merged


def build_notebook(source: Path, target: Path) -> dict:
    title, cells = parse_document(source.read_text(encoding="utf-8"), source)
    if source.parent == CONTENT_DIR:
        cells = merge_practice_cells(source.stem, cells)
    cells = header_cells(title, source, target, cells) + cells
    slug = target.stem
    for position, cell in enumerate(cells):
        cell.setdefault("id", f"{slug[:45]}-{position:04d}")
        cell.setdefault("metadata", {})
    return {
        "cells": cells,
        "metadata": {
            "colab": {
                "name": target.name,
                "toc_visible": True,
                "provenance": [],
            },
            "kernelspec": KERNELSPEC,
            "language_info": LANGUAGE_INFO,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def generated_pairs() -> list[tuple[Path, Path]]:
    return [(source, notebook_target(source)) for source in tracked_markdown_files()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify notebooks are up to date without writing")
    args = parser.parse_args()

    failures = 0
    written = 0
    for source, target in generated_pairs():
        notebook = build_notebook(source, target)
        payload = json.dumps(notebook, indent=1, ensure_ascii=False) + "\n"

        if args.check:
            if not target.exists():
                print(f"MISS {target.relative_to(ROOT)}")
                failures += 1
            elif target.read_text(encoding="utf-8") != payload:
                print(f"STALE {target.relative_to(ROOT)}")
                failures += 1
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
        written += 1

    if args.check:
        if failures:
            print(f"\n{failures} notebook(s) out of date. Run: python3 scripts/md_to_notebooks.py", file=sys.stderr)
            return 1
        print(f"All {len(generated_pairs())} generated Markdown notebooks are up to date.")
        return 0

    print(f"Wrote {written} generated Markdown notebook(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
