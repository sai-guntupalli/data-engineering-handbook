# Interview Practice Notebooks

Two kinds of notebooks live here:

| Path | What it is |
|---|---|
| [`topics/`](topics/) | One notebook per topic document, generated from `content/*.md` |
| [`05_interview_questions.ipynb`](05_interview_questions.ipynb) | A standalone question bank for mock interviews |

## Topic notebooks

Every topic doc is converted by [`scripts/md_to_notebooks.py`](../scripts/md_to_notebooks.py):

- every `##` section becomes a markdown cell,
- every ```python block becomes a code cell,
- fences in SQL, shell, YAML, Scala and other languages stay as formatted markdown blocks (they need their own
  engine),
- the house-style header, hand-written TOC and per-section `[Table of Contents]` footers are removed.

The Python, SQL and Spark topic notebooks also contain the hands-on practice exercises, merged in at the end. The
standalone practice notebooks below stay in this directory as the merge sources and remain independently runnable:

| Merged topic notebook | Contains |
|---|---|
| [`topics/python.ipynb`](topics/python.ipynb) | `content/python.md` + `01_python_basics.ipynb` + `02_python_coding_problems.ipynb` |
| [`topics/sql.ipynb`](topics/sql.ipynb) | `content/sql.md` + `03_sql_interview_questions.ipynb` |
| [`topics/spark.ipynb`](topics/spark.ipynb) | `content/spark.md` + `04_pyspark_concepts.ipynb` |

Regenerate them after editing any `content/*.md`:

```bash
make topic-notebooks        # rewrite notebooks/topics/*.ipynb
make topic-notebooks-check  # CI-safe: fails when the notebooks are out of date
```

## Setup

Install the notebook tooling:

```bash
uv sync --extra notebooks      # or: make setup-notebooks
```

Add Spark support (the PySpark notebook runs in "skip" mode without it):

```bash
uv sync --extra notebooks --extra notebooks-spark   # or: make setup-spark
```

PySpark also needs a Java runtime; install Java 17 or newer and check with `java -version`.

Without `uv`, install directly:

```bash
pip install jupyterlab nbformat nbclient ipykernel
pip install pyspark pandas        # optional, for the Spark notebook
```

## Running

```bash
make notebooks          # execute the practice notebooks and save their outputs
make notebooks-check    # execute without writing outputs (useful in CI)
jupyter lab notebooks/  # open them interactively
```

Or run a single notebook:

```bash
.venv/bin/python scripts/run_notebooks.py notebooks/05_interview_questions.ipynb
```

The `topics/` notebooks are reading material: their Python cells are runnable, but many snippets use PySpark,
pandas or another engine, so they are not part of `make notebooks`.

## Running in Google Colab

Click the **Open in Colab** badges on the documentation site's Notebooks page, or browse
`github.com/sai-guntupalli/data-engineering-interview-questions/tree/master/notebooks/topics` and open any notebook
with Colab's *GitHub* tab. Nothing needs to be installed locally.

- The Python and SQL notebooks use only the standard library and run as-is.
- The Spark notebook needs PySpark: add a cell with `!pip install pyspark`, run it, then choose
  **Runtime -> Restart session** and run all cells. Colab already provides Java.
- Topic notebooks contain snippets in several languages; only the Python blocks are executable cells.

## Notes

- `05_interview_questions.ipynb` is self-contained: 63 questions with model answers plus runnable checks.
- Outputs are committed so the notebooks are readable on GitHub without running them. Re-run `make notebooks` after
  editing the practice notebooks.
- The notebooks are also listed on the documentation site under **Notebooks**.
