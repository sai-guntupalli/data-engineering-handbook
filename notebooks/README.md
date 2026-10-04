# Interview Practice Notebooks

Runnable Jupyter notebooks for drilling the Python, SQL and PySpark concepts used in data-engineering interviews.
Every notebook executes top to bottom, contains self-checking `assert`s, and ends with a bank of interview
questions and model answers.

| Notebook | What it drills | Dependencies | Run in Colab |
|---|---|---|---|
| [01_python_basics.ipynb](01_python_basics.ipynb) | Classes and methods, dunder methods, properties, dataclasses, exceptions, context managers, generators, decorators, typing, datetime, concurrency | Python standard library | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/01_python_basics.ipynb) |
| [02_python_coding_problems.ipynb](02_python_coding_problems.ipynb) | Interview coding problems with tests: dedupe, top-K, sliding windows, intervals, hash joins, sessionization, LRU cache, retry | Python standard library | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/02_python_coding_problems.ipynb) |
| [03_sql_interview_questions.ipynb](03_sql_interview_questions.ipynb) | SQL against an in-memory SQLite database: window functions, top-N per group, running totals, gaps and islands, cohorts, dedupe | Python standard library (`sqlite3`) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/03_sql_interview_questions.ipynb) |
| [04_pyspark_concepts.ipynb](04_pyspark_concepts.ipynb) | PySpark concepts: lazy evaluation, joins and shuffles, window functions, UDFs, partitioning, caching, AQE, streaming | PySpark + Java 17+ (skips gracefully without them) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/04_pyspark_concepts.ipynb) |
| [05_interview_questions.ipynb](05_interview_questions.ipynb) | Mixed question bank across Python, SQL, Spark, modelling, lakehouse, orchestration, streaming, cloud and behavioural | Python standard library | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/05_interview_questions.ipynb) |

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
pip install pyspark pandas        # optional, for notebook 04
```

## Running

```bash
make notebooks          # execute every notebook and save its outputs
make notebooks-check    # execute without writing outputs (useful in CI)
jupyter lab notebooks/  # open them interactively
```

Or run a single notebook:

```bash
.venv/bin/python scripts/run_notebooks.py notebooks/03_sql_interview_questions.ipynb
```

## Running in Google Colab

Click the **Open in Colab** badge in the table above; Colab loads the notebook straight from
`github.com/sai-guntupalli/data-engineering-interview-questions`. Nothing needs to be installed locally.

- Notebooks 01, 02, 03 and 05 use only the Python standard library and run as-is.
- Notebook 04 needs PySpark: add a cell with `!pip install pyspark`, run it, then choose
  **Runtime -> Restart session** and run all cells. Colab already provides Java.
- Colab may use a different Python minor version than the repository virtualenv. Notebook 02 includes a fallback
  for `itertools.batched`, which requires Python 3.12+.

## Notes

- Notebooks 01, 02, 03 and 05 need only the Python standard library, so they run anywhere.
- Notebook 04 detects PySpark and Java at the top and prints setup instructions when either is missing; Spark cells
  are skipped instead of failing, and the expected results are documented in markdown above each cell.
- Outputs are committed so the notebooks are readable on GitHub without running them. Re-run `make notebooks` after
  editing to refresh them.
- The notebooks are also listed on the documentation site under **Practice Notebooks**.
