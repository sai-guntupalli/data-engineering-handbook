#!/usr/bin/env python3
"""
Prepare MkDocs source files from the repository Markdown content.

The repository keeps interview content in content/*.md. This script generates a
MkDocs-friendly source tree in .docs_src/ so the docs site can be built without
duplicating the content by hand.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
DOCS_SRC = ROOT / ".docs_src"
DOCS_ASSETS = ROOT / "docs_assets"
NOTEBOOKS_DIR = ROOT / "notebooks"

# Used for the "view on GitHub" and "open in Colab" links on the notebooks page.
# The git remote is read at build time when available, so forks get working links.
DEFAULT_REPO_SLUG = "sai-guntupalli/data-engineering-interview-questions"
DEFAULT_REPO_BRANCH = "master"
COLAB_BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

# (filename, title, what it drills, dependencies) for the standalone practice
# notebooks. The Python, SQL and Spark ones are also merged into the matching
# topic notebook by scripts/md_to_notebooks.py.
NOTEBOOKS: list[tuple[str, str, str, str]] = [
    (
        "01_python_basics.ipynb",
        "Python basics",
        "Classes and methods, dunder methods, properties, dataclasses, exceptions, context managers, "
        "generators, decorators, typing, datetime, and concurrency",
        "Python standard library",
    ),
    (
        "02_python_coding_problems.ipynb",
        "Python coding problems",
        "Interview coding problems with tests: dedupe, top-K, sliding windows, intervals, hash joins, "
        "sessionization, LRU cache, and retry",
        "Python standard library",
    ),
    (
        "03_sql_interview_questions.ipynb",
        "SQL interview questions",
        "Window functions, top-N per group, running totals, gaps and islands, cohorts, and dedupe against "
        "an in-memory SQLite database",
        "Python standard library (sqlite3)",
    ),
    (
        "04_pyspark_concepts.ipynb",
        "PySpark concepts",
        "Lazy evaluation, joins and shuffles, window functions, UDFs, partitioning, caching, AQE, and streaming",
        "PySpark + Java 17+ (skips gracefully without them)",
    ),
    (
        "05_interview_questions.ipynb",
        "Interview question bank",
        "Mixed questions across Python, SQL, Spark, modelling, lakehouse, orchestration, streaming, "
        "cloud, and behavioural",
        "Python standard library",
    ),
]


TOPIC_GROUPS: list[tuple[str, list[str]]] = [
    (
        "Core Pipeline Skills",
        [
            "python",
            "python-basics",
            "python-coding",
            "sql",
            "scala",
            "spark",
            "spark-tuning",
            "airflow",
            "dbt",
            "data-quality",
            "observability",
        ],
    ),
    (
        "Lakehouse And Formats",
        ["parquet", "delta", "iceberg", "hudi", "avro", "cdc", "data-modeling"],
    ),
    (
        "Cloud And Platforms",
        [
            "aws",
            "azure",
            "gcp",
            "bigquery",
            "redshift",
            "snowflake",
            "databricks",
            "trino",
            "clickhouse",
            "dynamodb",
            "bigtable",
        ],
    ),
    (
        "Streaming And Distributed Systems",
        ["kafka", "flink", "redis", "hadoop", "hive", "hbase", "cassandra", "kubernetes"],
    ),
    (
        "Warehousing, BI, And Governance",
        [
            "dwha",
            "system-design",
            "statistics",
            "data-governance",
            "cost-optimization",
            "tableau",
            "looker",
            "superset",
        ],
    ),
    (
        "AI And LLM Foundations",
        ["llm"],
    ),
    (
        "Additional Tools",
        [
            "mongo",
            "nifi",
            "flume",
            "greenplum",
            "impala",
            "elasticsearch",
            "docker",
            "data-structure",
        ],
    ),
]


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    source: Path
    target: Path
    question_count: int
    summary: str


# Display names for the study-path groups, kept in step with the labels used in the
# mkdocs.yml navigation so the sidebar and the pages read the same way.
GROUP_LABELS: dict[str, str] = {
    "Core Pipeline Skills": "Core pipeline skills",
    "Lakehouse And Formats": "Lakehouse and formats",
    "Cloud And Platforms": "Cloud and platforms",
    "Streaming And Distributed Systems": "Streaming and distributed systems",
    "Warehousing, BI, And Governance": "Warehousing, BI and governance",
    "AI And LLM Foundations": "AI and LLM foundations",
    "Additional Tools": "Additional tools",
    "Other Topics": "Other topics",
}


def _group_label(group: str) -> str:
    return GROUP_LABELS.get(group, group)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _topic_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback.replace("-", " ").title()


def _first_summary(text: str) -> str:
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped or stripped.startswith("#") or stripped.startswith("+ ["):
            continue
        if stripped.startswith("[Table of Contents]"):
            continue
        if len(stripped) > 180:
            return stripped[:177].rstrip() + "..."
        return stripped
    return "Practical questions, explanations, and examples for interview preparation."


def _question_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("## "))


def _clean_topic_markdown(text: str) -> str:
    lines = []
    seen_h1 = False
    seen_h2 = False
    skipping_leading_toc = False
    for line in text.splitlines():
        if line.startswith("## [Main title]"):
            continue
        if line.startswith("### [Interview questions]"):
            continue
        if line.strip() == "#":
            continue
        if seen_h1 and not seen_h2 and re.match(r"^##\s+Table of Contents\s*$", line, re.IGNORECASE):
            skipping_leading_toc = True
            continue
        if skipping_leading_toc and line.startswith("+ ["):
            continue
        if skipping_leading_toc and not line.strip():
            continue
        if skipping_leading_toc:
            skipping_leading_toc = False
        if re.match(r"^#\s+", line):
            seen_h1 = True
        if re.match(r"^##\s+", line):
            seen_h2 = True
        # The source files contain large hand-written TOCs with GitHub-style
        # anchors. MkDocs generates a better page TOC, and the old anchors
        # create noisy build warnings, so omit only the leading source TOC.
        if seen_h1 and not seen_h2 and line.startswith("+ ["):
            continue
        if line.startswith("[Table of Contents]"):
            continue
        lines.append(line)

    cleaned = "\n".join(lines).strip() + "\n"
    # Links between content files now live in the same topics/ directory.
    cleaned = cleaned.replace("../README.md", "../index.md")
    cleaned = cleaned.replace("full.md", "full.md")
    return cleaned


def _discover_topics() -> list[Topic]:
    topics: list[Topic] = []
    for source in sorted(CONTENT_DIR.glob("*.md")):
        if source.name == "full.md":
            continue
        slug = source.stem
        raw = _read(source)
        title = _topic_title(raw, slug)
        cleaned = _clean_topic_markdown(raw)
        target = DOCS_SRC / "topics" / source.name
        topics.append(
            Topic(
                slug=slug,
                title=title,
                source=source,
                target=target,
                question_count=_question_count(cleaned),
                summary=_first_summary(cleaned),
            )
        )
    return topics


def _group_topics(topics: list[Topic]) -> list[tuple[str, list[Topic]]]:
    by_slug = {topic.slug: topic for topic in topics}
    grouped: list[tuple[str, list[Topic]]] = []
    used: set[str] = set()

    for group_name, slugs in TOPIC_GROUPS:
        group_topics = [by_slug[slug] for slug in slugs if slug in by_slug]
        if group_topics:
            grouped.append((group_name, group_topics))
            used.update(topic.slug for topic in group_topics)

    remaining = [topic for topic in topics if topic.slug not in used]
    if remaining:
        grouped.append(("Other Topics", remaining))

    return grouped


def _topic_card(topic: Topic) -> str:
    return f"""
<a class="topic-card" href="topics/{topic.slug}/">
  <span class="topic-card__eyebrow">{topic.question_count} sections</span>
  <strong>{topic.title}</strong>
  <span>{topic.summary}</span>
</a>
""".strip()


def _index_markdown(grouped: list[tuple[str, list[Topic]]]) -> str:
    total_topics = sum(len(items) for _group, items in grouped)
    total_sections = sum(topic.question_count for _group, items in grouped for topic in items)
    topic_notebooks = len(list((NOTEBOOKS_DIR / "topics").glob("*.ipynb")))
    practice_notebooks = sum(1 for filename, *_ in NOTEBOOKS if (NOTEBOOKS_DIR / filename).exists())
    notebook_count = topic_notebooks + practice_notebooks
    cards = "\n".join(
        f"### {_group_label(group)}\n\n<div class=\"topic-grid\">\n"
        + "\n".join(_topic_card(topic) for topic in topics)
        + "\n</div>"
        for group, topics in grouped
    )

    return f"""# Data Engineering Interview Guide

Practical interview notes for data engineers, covering PySpark, SQL, lakehouse table formats, cloud platforms,
data modeling, CDC, orchestration, observability, BI, and AI foundations.

<div class="hero-panel">
  <div>
    <p class="eyebrow">Start with a path, then go deep</p>
    <h2>Learn the concept, then learn how to use it.</h2>
    <p>Every topic explains the idea, shows real code, names the trade-offs, and ends with interview-ready answers.</p>
  </div>
  <div class="hero-stats">
    <span><strong>{total_topics}</strong> topics</span>
    <span><strong>{total_sections}</strong> questions</span>
    <span><strong>{notebook_count}</strong> notebooks</span>
  </div>
</div>

## Start here

<div class="path-grid">
  <a href="notebooks/">Notebooks <span>Run the concepts with self-checking exercises, locally or in Google Colab</span></a>
  <a href="topics/">Topic index <span>All {total_topics} topics grouped by study path</span></a>
  <a href="topics/full/">All questions <span>Scan every question and jump straight to the answer</span></a>
</div>

## Study paths

Pick the path that matches the role you are interviewing for, then work through the topics in order.

<div class="path-grid">
  <a href="topics/python/">Core pipeline path <span>Python -> SQL -> Spark -> Spark tuning -> Airflow -> dbt</span></a>
  <a href="topics/iceberg/">Lakehouse path <span>Parquet -> Delta -> Iceberg -> CDC -> Data modeling</span></a>
  <a href="topics/kafka/">Streaming path <span>Kafka -> Flink -> Redis -> CDC -> Observability</span></a>
  <a href="topics/aws/">Cloud path <span>AWS / GCP / Azure -> Databricks / Snowflake -> Cost -> Governance</span></a>
  <a href="topics/dwha/">Analytics path <span>Data warehousing -> dbt -> BI tools and statistics</span></a>
  <a href="topics/llm/">AI path <span>LLM terminology -> RAG -> evaluations and guardrails</span></a>
</div>

## Browse by topic group

{cards}
"""


def _topics_index_markdown(grouped: list[tuple[str, list[Topic]]]) -> str:
    total = sum(len(topics) for _group, topics in grouped)
    body = [
        "# Topic index",
        "",
        f"All {total} topics, grouped by study path. Each topic page has the questions, answers, code examples, and "
        "real-world scenarios.",
        "",
    ]
    for group, topics in grouped:
        body.append(f"## {_group_label(group)}")
        body.append("")
        for topic in topics:
            body.append(f"- [{topic.title}]({topic.slug}.md) - {topic.question_count} questions")
        body.append("")
    return "\n".join(body).rstrip() + "\n"


def _full_index_markdown(grouped: list[tuple[str, list[Topic]]]) -> str:
    """Render the "All questions" page.

    content/full.md is the generated question index: one section per topic with a link
    per question, so its relative links resolve to the topic pages when copied here.
    """
    source = CONTENT_DIR / "full.md"
    total_questions = sum(topic.question_count for _group, items in grouped for topic in items)

    if not source.exists():
        body = [
            "# All questions",
            "",
            "A scan-friendly checklist of every question in the guide.",
            "",
        ]
        for group, topics in grouped:
            body.append(f"## {_group_label(group)}")
            body.append("")
            for topic in topics:
                body.append(f"- [{topic.title}]({topic.slug}.md) - {topic.question_count} questions")
            body.append("")
        return "\n".join(body).rstrip() + "\n"

    cleaned = _clean_topic_markdown(_read(source)).strip()
    return (
        "# All questions\n\n"
        f"Every question in the guide ({total_questions:,} links), grouped by topic. Jump to a topic with the list "
        "below, or use the search box to find a specific question.\n\n"
        f"{cleaned}\n"
    )


def _copy_assets() -> None:
    if (ROOT / "img").exists():
        shutil.copytree(ROOT / "img", DOCS_SRC / "img", dirs_exist_ok=True)
    if DOCS_ASSETS.exists():
        shutil.copytree(DOCS_ASSETS, DOCS_SRC / "assets", dirs_exist_ok=True)


def _git_output(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True, timeout=10
        )
    except (OSError, subprocess.SubprocessError):
        return None
    value = result.stdout.strip()
    return value or None


def _repo_slug() -> str:
    url = _git_output("remote", "get-url", "origin") or ""
    match = re.search(r"github\.com[:/](?P<slug>[^/\s]+/[^/\s]+?)(?:\.git)?$", url)
    return match.group("slug") if match else DEFAULT_REPO_SLUG


def _repo_branch() -> str:
    return _git_output("rev-parse", "--abbrev-ref", "HEAD") or DEFAULT_REPO_BRANCH


def _notebook_code_cells(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0
    return sum(1 for cell in data.get("cells", []) if cell.get("cell_type") == "code")


def _notebook_title(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return path.stem.replace("-", " ").title()
    for cell in data.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        match = re.match(r"^#\s+(.+?)\s*$", source.strip())
        if match:
            return match.group(1).strip()
    return path.stem.replace("-", " ").title()


def _copy_notebooks() -> list[str]:
    copied: list[str] = []
    if not NOTEBOOKS_DIR.exists():
        return copied
    target_dir = DOCS_SRC / "notebooks"
    for source in sorted(NOTEBOOKS_DIR.rglob("*.ipynb")):
        relative = source.relative_to(NOTEBOOKS_DIR)
        target = target_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(str(relative))
    return copied


def _notebooks_markdown() -> str:
    slug = _repo_slug()
    branch = _repo_branch()
    github_base = f"https://github.com/{slug}/blob/{branch}/notebooks"
    colab_base = f"https://colab.research.google.com/github/{slug}/blob/{branch}/notebooks"

    rows: list[str] = []
    for filename, title, description, dependencies in NOTEBOOKS:
        path = NOTEBOOKS_DIR / filename
        if not path.exists():
            continue
        code_cells = _notebook_code_cells(path)
        rows.append(
            f"| [{title}](notebooks/{filename}) | {description} | {code_cells} | {dependencies} | "
            f"[![Open in Colab]({COLAB_BADGE})]({colab_base}/{filename}) | [GitHub]({github_base}/{filename}) |"
        )

    table = "\n".join(rows) if rows else "| _No notebooks found yet._ | | | | | |"

    topic_rows: list[tuple[str, list[str]]] = []
    by_slug = {path.stem: path for path in (NOTEBOOKS_DIR / "topics").glob("*.ipynb")}
    grouped_slugs: set[str] = set()
    for group_name, slugs in TOPIC_GROUPS:
        rows_for_group: list[str] = []
        for slug in slugs:
            path = by_slug.get(slug)
            if path is None:
                continue
            relative = path.relative_to(NOTEBOOKS_DIR)
            grouped_slugs.add(slug)
            rows_for_group.append(
                f"| [{_notebook_title(path)}](notebooks/{relative}) | {_notebook_code_cells(path)} | "
                f"[![Open in Colab]({COLAB_BADGE})]({colab_base}/{relative}) | [GitHub]({github_base}/{relative}) |"
            )
        if rows_for_group:
            topic_rows.append((group_name, rows_for_group))

    leftovers = [
        (slug, path) for slug, path in sorted(by_slug.items()) if slug not in grouped_slugs
    ]
    if leftovers:
        topic_rows.append(
            (
                "Other topics",
                [
                    f"| [{_notebook_title(path)}](notebooks/{path.relative_to(NOTEBOOKS_DIR)}) | "
                    f"{_notebook_code_cells(path)} | "
                    f"[![Open in Colab]({COLAB_BADGE})]({colab_base}/{path.relative_to(NOTEBOOKS_DIR)}) | "
                    f"[GitHub]({github_base}/{path.relative_to(NOTEBOOKS_DIR)}) |"
                    for _slug, path in leftovers
                ],
            )
        )

    topics_sections = "\n\n".join(
        f"### {_group_label(group)}\n\n| Topic notebook | Code cells | Run in Colab | View |\n|---|---|---|---|\n"
        + "\n".join(rows)
        for group, rows in topic_rows
    )
    topic_count = sum(len(rows) for _group, rows in topic_rows)

    return f"""# Notebooks

Every topic in this guide is also a Jupyter notebook. The **practice notebooks** are self-checking exercises you can
run top to bottom; the **topic notebooks** are one-to-one conversions of the topic pages, grouped the same way as
the rest of the site.

## Practice notebooks

Start here if you learn by running code. Each one executes top to bottom against a small self-contained dataset,
checks itself with assertions, and ends with interview questions and model answers.

| Practice notebook | What it drills | Code cells | Dependencies | Run in Colab | View |
|---|---|---|---|---|---|
{table}

The Python, SQL and Spark exercises are also merged into the matching topic notebooks, so each of those is
self-contained.

## Topic notebooks

One notebook per topic document ({topic_count} in total), generated from `content/*.md` by
`scripts/md_to_notebooks.py`. Every `##` section becomes a markdown cell, every Python block becomes a code cell,
and fences in other languages stay as formatted blocks because they need their own engine.

{topics_sections}

## Run them locally

```bash
make setup-notebooks      # uv sync --extra notebooks
make notebooks            # execute the practice notebooks and refresh their outputs
make notebooks-check      # execute without writing outputs
make topic-notebooks      # regenerate notebooks/topics/*.ipynb from content/*.md
jupyter lab notebooks/    # or open them interactively
```

The Spark notebook needs Spark support:

```bash
make setup-spark          # uv sync --extra notebooks --extra notebooks-spark
```

PySpark also requires a Java runtime (Java 17 or newer). Without it, the PySpark notebook prints setup
instructions and skips the Spark cells instead of failing.

## Run them in Google Colab

Colab opens a notebook straight from GitHub, so there is nothing to install locally: use the **Open in Colab**
badges above, or go to [colab.research.google.com](https://colab.research.google.com/) and choose *GitHub*.

+ The Python and SQL notebooks use only the standard library and run in Colab as-is.
+ The Spark notebook needs PySpark: run `!pip install pyspark` in a new Colab cell, then pick
  **Runtime -> Restart session** and run all cells. Colab already provides Java.
+ The topic notebooks contain illustrative snippets in several languages; the Python blocks are runnable cells and
  the rest are formatted blocks that need their own engine.
"""


def _nav_slugs() -> set[str]:
    """Slugs currently referenced by the explicit nav in mkdocs.yml."""
    try:
        text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    except OSError:
        return set()
    return set(re.findall(r"topics/([a-z0-9-]+)\.md", text))


def _missing_from_nav(topics: list[Topic]) -> list[str]:
    covered = _nav_slugs()
    return [topic.slug for topic in topics if topic.slug not in covered]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-nav",
        action="store_true",
        help="fail when a topic document is missing from the nav in mkdocs.yml",
    )
    args = parser.parse_args(argv)

    if DOCS_SRC.exists():
        shutil.rmtree(DOCS_SRC)
    DOCS_SRC.mkdir(parents=True)

    topics = _discover_topics()
    grouped = _group_topics(topics)

    for topic in topics:
        _write(topic.target, _clean_topic_markdown(_read(topic.source)))

    _write(DOCS_SRC / "topics" / "full.md", _full_index_markdown(grouped))
    _write(DOCS_SRC / "index.md", _index_markdown(grouped))
    _write(DOCS_SRC / "topics" / "index.md", _topics_index_markdown(grouped))
    _write(DOCS_SRC / "notebooks.md", _notebooks_markdown())
    copied_notebooks = _copy_notebooks()
    _copy_assets()

    missing = _missing_from_nav(topics)
    if missing:
        message = (
            "these topics are not in the mkdocs.yml nav, so they will not appear in the sidebar: "
            + ", ".join(sorted(missing))
        )
        if args.strict_nav:
            print(f"error: {message}", file=sys.stderr)
            return 1
        print(f"warning: {message}", file=sys.stderr)

    print(
        f"Prepared MkDocs source in {DOCS_SRC.relative_to(ROOT)} "
        f"({len(topics)} topics, {len(copied_notebooks)} notebooks)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
