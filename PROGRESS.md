# Progress

**Current Status**: 68 notebooks are Colab-runnable and executed by CI. PR #28 (Colab restructure) and PR #29 (PySpark
coding challenges) are merged. The SQL learning path (10 Spark SQL notebooks) is in PR #30, rebased onto master and
awaiting review and merge.

## Completed

- 2026-11-07: SQL path review (feedback round): dropped the filtering-and-grouping notebook. Added `sql-01-basics`, a
  book-style notebook covering tables, SELECT, WHERE, sorting, aggregates, GROUP BY, HAVING, joins, CASE and NULL,
  with ten practice questions and answers. Reworked `sql-05-joins` in the same style. Both install PySpark with
  `!pip install -q pyspark` and run on Spark 4.0.2 (Colab's version) and locally. The other SQL notebooks still use
  the earlier style and await feedback. The audit now accepts `!pip install` lines.
- 2026-11-07: Added `notebooks/06_pyspark_coding_challenges.ipynb`: five interview-style PySpark problems
  (latest-record dedupe, grain-aware joins, SCD as-of join, sessionization, salted skew join) with fixtures, reference
  solutions and 19 asserts; runs locally in 13s. Recovered from the old WIP in `notebooks/04_pyspark_concepts.ipynb`.
- 2026-11-07: SQL learning path split (`feat/sql-notebook-split`):
  - `03_sql_interview_questions` is now the index/navigation page; its DuckDB content moved into ten notebooks in
    `topics/sql-01…sql-10`: filtering and grouping, WHERE vs HAVING, NULL handling, CASE, joins, window functions,
    deduplication, time-series, modeling and optimization, and interview drills.
  - Every teaching notebook explains its topic first, then runs examples with asserted expected results. The drills
    port all 22 coding problems and 14 concept questions to Spark SQL, after the teaching material.
  - Execution backend is PySpark SQL on temporary views. The setup cell installs PySpark when it is missing, and a
    bootstrap cell detects PySpark and Java (`SPARK_AVAILABLE`). Without Java, every example prints `SKIPPED`.
  - Verified: audit passes on 67 notebooks; the 10 new notebooks execute end to end with Spark 3.5 on JDK 21; all 10
    run to completion with Spark unavailable; `make lint` and the Next.js build pass with the new gallery group.
- 2026-11-07: Verified PR #28: GitHub Checks green (all 57 notebooks executed on Linux + Java 17, 2m32s);
  smoke-tested in a real Google Colab runtime with "Run all": `topics/dynamodb` (30/30 cells), `topics/spark`
  (51/51, setup cell installed PySpark), `topics/iceberg` (22/22) — no errors.
- 2026-11-07: Colab-runnable restructure (PR #28, merged):
  - Merged the open per-notebook cleanup PRs (#1–#22) and the notebook parts of #26 (DuckDB SQL) and #27
    (PySpark story); the interactive viewer (#24/#25) was intentionally dropped.
  - Moved the Next.js gallery into `site/`; upgraded Next.js to 16.4.5 (critical advisory on ≤16.4.0); fixed the
    Topics menu links ignoring the GitHub Pages base path.
  - Removed bloat: merged practice copies inside topics/python, sql, spark (~1,000 duplicated cells) and
    `sync_merged_copies.py`; the watermark tooling and per-notebook metadata (incl. email); the duplicate
    `topics/python-basics` and `topics/python-coding` notebooks (unique content folded into 01/02); committed
    outputs; "How to use" boilerplate; repeated prose (21,532 → 5,467 cells; many notebooks 40–80% fewer words).
  - Every `# ILLUSTRATIVE` cell became runnable code on an in-process stand-in or a markdown code fence.
  - Each notebook with third-party imports starts with a version-aware setup cell (`PACKAGES`), so Colab installs
    or upgrades exactly what it needs.
  - New tooling: `notebook_format.py`, Colab-rule `audit_notebooks.py`, parallel `run_notebooks.py`, pytest suite,
    ruff, Makefile `install/dev/test/lint/format/check/notebooks/build/validate`; CI runs every notebook with Java 17.
- 2026-10-17/18: Per-notebook dedupe sweep and DuckDB/PySpark rewrites (open PRs #1–#27, now folded in).

## In Progress

- SQL learning path: PR #30 rebased onto master for review (https://github.com/sai-guntupalli/data-engineering-handbook/pull/30); CI not yet confirmed.

## Next Steps

1. Review and merge PR #30 (`feat/sql-notebook-split`), after CI is green.
2. Run one SQL notebook in a real Colab runtime with "Run all" (requires the user's Google sign-in). Colab's bundled
   Java version is not verified; if Colab has no Java, the examples print `SKIPPED` there.
3. Decide on the older DuckDB reference `topics/sql.ipynb` (61K words, 74 cells). It overlaps the new path, so it is
   a candidate to trim or to link from the index.
4. Reconcile the uncommitted WIP in the main checkout: `notebooks/03_sql_interview_questions.ipynb` (a SQLite-based
   split), `notebooks/04_pyspark_concepts.ipynb` (exercise edits), and untracked `scripts/split_sql_notebooks.py`,
   `scripts/add_core_sql_topics.py` and `topics/sql-*` drafts. None of them are on master.
5. Review PR #29 (PySpark coding challenges, `feat/pyspark-coding-problems`).
6. Optional deeper trims: `04_pyspark_concepts` (12.9K words), `snowflake` (13.1K), `bigquery` (12.3K),
   `02_python_coding_problems` (12K).

## Blockers

- None.
