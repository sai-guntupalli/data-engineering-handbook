# Interview Practice Notebooks

Three kinds of notebooks live here:

| Path | What it is |
|---|---|
| [`topics/`](topics/) | One notebook per `content/*.md` document, including `content/full.md` |
| [`from-md/`](from-md/) | One notebook for each tracked repository Markdown file outside `content/` |
| [`05_interview_questions.ipynb`](05_interview_questions.ipynb) | A standalone question bank for mock interviews |

## Topic notebooks

Every tracked Markdown doc is converted by [`scripts/md_to_notebooks.py`](../scripts/md_to_notebooks.py):

- every `##` section becomes a markdown cell,
- every Python/PySpark fence becomes a code cell,
- shell fences become executable `%%bash` cells,
- SQL fences become executable `%%sql` cells when `ipython-sql` is installed,
- each generated notebook starts with Colab usage notes, detected dependency hints, and a lightweight environment check,
- YAML, Scala, JSON and other snippets stay formatted when a Colab Python kernel cannot execute them directly,
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
make notebook-audit         # validate every notebook and count markdown/code/assert cells
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

The generated notebooks are interactive reading material: their Python, PySpark, SQL and shell cells are executable
where dependencies and backing data exist, but many examples still refer to real tables, cloud services, credentials,
or platform runtimes. They are intentionally not part of `make notebooks`, which executes only the hand-written
self-checking practice notebooks.

## Running in Google Colab

Click the **Open in Colab** badges on the documentation site's Notebooks page, or browse
`github.com/sai-guntupalli/data-engineering-interview-questions/tree/master/notebooks/topics` and open any notebook
with Colab's *GitHub* tab. Nothing needs to be installed locally.

- The Python and SQL notebooks use only the standard library and run as-is.
- The Spark notebook needs PySpark: add a cell with `!pip install pyspark`, run it, then choose
  **Runtime -> Restart session** and run all cells. Colab already provides Java.
- Topic notebooks contain snippets in several languages; Python/PySpark, SQL and shell blocks are code cells, while
  platform-specific snippets that Colab cannot execute directly are preserved as formatted reference blocks.

## Notes

- `05_interview_questions.ipynb` is self-contained: 63 questions with model answers plus runnable checks.
- Outputs are committed so the notebooks are readable on GitHub without running them. Re-run `make notebooks` after
  editing the practice notebooks.
- The notebooks are also listed on the documentation site under **Notebooks**.
