# Progress

**Current Status**: All notebooks are Colab-runnable and executed by CI on PySpark 4.0 (JDK 17). The 14-chapter SQL path is on master (PR #34).
The website has been redesigned as an editorial library (`feat/redesign-site`) and is awaiting review; it no longer shows
notebook, cell or check counts.

## Completed

- 2026-11-07: Notebook depth and real-world coverage (`feat/real-world-sections`): the classes chapter starts from
  what a class is and how to create one; chapters 3, 6 and 8 define decorators, context managers and threads or
  coroutines; every Python and SQL concept section has a "Where you'll use it" section. Seven topic notebooks (docker,
  kubernetes, llm, looker, scala, superset, tableau) gained one per main part. Airflow, Kafka and dbt have one per
  question. Spark, Delta and Iceberg are in progress.

<<<<<<< HEAD
- 2026-11-07: Restyled the site (`feat/site-cool-palette`): a cool, light-first palette with one blue accent, Geist for
  headings instead of the serif, drawn-out kicker labels removed, primary buttons in the accent, and matching dark theme.
  Layout, content and behaviour are unchanged. The design detector reports no findings. `PRODUCT.md` records the product
  context for future design work.
=======
- 2026-11-07: Real-world coverage (`feat/python-learning-path`): seven topic notebooks that had no use-case section
  (docker, kubernetes, llm, looker, scala, superset, tableau) gained a "Where you'll use it" section for each main
  part. Every SQL chapter 14 question now has one, and chapter 13 has one for its concept block. The other topic
  notebooks already had a notebook-level "Real world use cases" section; their question-by-question sections are not
  yet written.

- 2026-11-07: Notebook depth pass (`feat/python-learning-path`): the classes chapter now starts from what a class is,
  how to define one, `__init__`, methods, `__repr__`, `__eq__`, class versus instance attributes, properties,
  inheritance, dataclasses by hand and with `@dataclass`, and enums. Chapters 3, 6 and 8 gained short definitions of
  decorators, context managers and threads or coroutines. Every Python and SQL concept section now has a
  "Where you'll use it" section with real-world uses. The other topic notebooks have not been done yet.
>>>>>>> 7937c35 (Add real-world sections to the remaining notebooks)

- 2026-11-07: Python learning path (`feat/python-learning-path`): the single `topics/python` notebook is replaced by nine
  chapters, following the SQL path. Chapters 1-8 cover values and types, collections, control flow and functions,
  iterators and generators, classes and dataclasses, files and formats, errors, logging and testing, and concurrency.
  Chapter 9 covers data-engineering patterns with the standard library only: config, validation and quarantine,
  idempotent upserts, watermarks, retries with backoff, partitioned output, content hashes, deduplication and run
  summaries. Each chapter runs top to bottom on Python 3.13 and passes the audit. The old notebook's Parquet and pandas
  content is not carried over; see the Parquet and Data quality notebooks.

- 2026-11-07: Library listing fixes (`fix/library-listing`): the practice group is now "Interview practice" (its six
  notebooks are interview prep kept outside the topic folders); descriptions read whole paragraphs, so they no longer
  stop mid-sentence; leading index numbers are dropped from titles; topic groups renamed to Data Engineering, Lakehouse
  Formats, Cloud Platforms, Streaming and Distributed Systems, Warehousing and BI, AI Foundations and Other Tools; the SQL
  index says fourteen chapters. Site builds, lint passes.

- 2026-11-07: Fixed the failing notebook run in CI (`fix/pyspark-4-recursive-cte`). The CI extra pinned PySpark below 4,
  so CI ran Spark 3.5, which has no recursive CTEs and failed `sql-02`. The extra and the six PySpark setup cells now pin
  `pyspark>=4.0,<4.1`, the version Colab installs. Spark 4.0.x fails to plan a recursive CTE (an internal `UnionLoop`
  error, seen on 4.0.0 through 4.0.5), so `sql-02` shows that query as reference and walks the hierarchy with a self-join.
  This corrects the earlier "all pass on 4.0.2" note for that query. `sql-02`'s ROLLUP query now sorts through a subquery.
  `spark` uses `try_cast` for the malformed cast, because ANSI mode is on by default in 4.0. `spark-tuning` reads Spark 4
  event logs, which are a directory of files, and writes them uncompressed. All 72 notebooks pass with PySpark 4.0.5 on
  JDK 17, the CI setup. Recursive CTE execution is verified only on 4.1.0 (in a sandbox probe).

- 2026-11-07: Redesigned the website (`feat/redesign-site`): an editorial look (warm paper, serif display type, one
  burnt-sienna accent) with dark mode. The home page has a hero with a static notebook preview, a Read / Run / Check
  strip and a library with a sticky topic index. Notebook rows replace the cards. Removed all counts (notebooks, code
  cells, checks, reading time) from the UI and the data layer. Header search, starring, /search and the license page
  keep their behaviour. The topics dropdown is gone; the topic index replaces it. Verified with lint, typecheck, the
  static build, and visual checks at desktop and phone width in light and dark themes.
- 2026-11-07: SQL path extended to 14 chapters (`feat/sql-missing-topics`): new `sql-03` types, functions, dates and
  JSON; `sql-07` set operations; `sql-12` views and changing data (INSERT, INSERT OVERWRITE, UPDATE/DELETE/MERGE as
  reference for table formats); `sql-14` interview concepts. Added GROUPING() and CUBE, RIGHT JOIN, LEAD, moving averages,
  FIRST_VALUE, LAST_VALUE, NTILE, WINDOW, time-zone setting, and an interview-notes section per chapter. Fixed the
  drills' DuckDB demos and stale Part 7 references. All 15 notebooks pass on Spark 4.0.2. Delta Lake could not be
  verified here (Maven is unreachable from the sandbox), so UPDATE, DELETE and MERGE are shown as reference SQL.

- 2026-11-07: Merged the WHERE vs HAVING notebook into `sql-01-basics` (new section 7). Replaced it with
  `sql-02-aggregations-and-ctes`: more aggregates, `ROLLUP`, subqueries, CTEs and a recursive CTE, with five practice
  questions and answers. Both run on Spark 4.0.2.
- 2026-11-07: Untangled the non-notebook code (`chore/untangle-codebase`):
  - One registry: each group in `site/lib/notebook-groups.ts` declares its folder. The build fails on a missing or
    unregistered notebook (the "Other notebooks" fallback is gone).
  - One repository identity: `site/lib/site.ts` holds the branch, author and license URL; a test keeps the Python
    formatter's copies in step with it.
  - One notebook list and one search rule: `site/lib/search.ts` defines what matches; header suggestions and /search
    share it, so they agree on the fields searched.
  - Removed dead special cases: the "How to use" boilerplate removal, the `.py`-module allowance in the audit, the
    hard-coded setup-helper list (the setup cell is now exempt from the import check), and the description prefixes.
  - CI runs `make validate`, the same target as local development.
  - Comments that restated the code were removed; tests that checked implementation details were rewritten to check
    behaviour.
  - Rendered gallery text is unchanged versus master. Intended change: header suggestions also match description text.

- 2026-11-07: SQL path review (feedback round): dropped the filtering-and-grouping notebook. Added `sql-01-basics`, a
  book-style notebook covering tables, SELECT, WHERE, sorting, aggregates, GROUP BY, HAVING, joins, CASE and NULL,
  with ten practice questions and answers. Reworked `sql-05-joins` in the same style. Both install PySpark with
  `!pip install -q pyspark` and run on Spark 4.0.2 (Colab's version) and locally. The audit now accepts
  `!pip install` lines. The approved style is then applied to every SQL notebook: plain Spark SQL cells, no setup
  helpers, each chapter ends with practice questions and answers. Drills keep their 22 checked answers. All SQL
  notebooks pass on Spark 4.0.2 from a clean install.
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

- Website redesign: branch `feat/redesign-site`, PR awaiting review. Visual check in a real browser on GitHub Pages
  after merge.

## Next Steps

1. Review and merge the website redesign PR (`feat/redesign-site`) once CI is green, then confirm the GitHub Pages deploy
   renders the new home page, search and license pages.
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
