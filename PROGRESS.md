# Progress

## Python practice cleanup and local integrations — 2026-11-10

- Reviewed Python challenges 1–9, drills 1–9 and the coding-problems workbook. Questions and concrete sample
  inputs/outputs now precede exercise cells. Removed visible check blocks, scoring helpers, score headings and
  async test probes. Replaced dense test-helper expressions with readable examples for files, classes, retries,
  logging and coroutines. Solutions remain closed by default.
- Consolidated the coding workbook from 303 to 104 cells, retaining problem statements, examples and collapsed
  approach/implementation explanations. Corrected the null-aware average example and clarified materialized
  parsing memory costs and touching-interval conventions.
- Moved regression machinery into `tests/fixtures/practice-checks/`. The verifier uses the current notebook
  answers, executes the workbook regression cases and rejects wrong drill/challenge answers. Updated contribution
  guidance so future edits do not restore learner-facing scoreboards.
- Added local Delta update/delete/merge examples to PySpark 5 and SQL 12, a real file-source Structured Streaming
  window in PySpark 6, and a temporary dbt-duckdb seed/model/test project. Delta uses delta-rs, not Spark SQL DML.
- Added introductory notebooks for open table formats, catalogs, DuckDB, PostgreSQL, orchestration, semantic
  layers, security/IAM and CI/CD/IaC. DuckDB examples execute locally; PostgreSQL transaction illustration uses
  DuckDB and says so. Catalog, IAM, orchestration and compatibility examples are explicitly local models.
- Python lessons identify Python 3.12+ as their target; concurrency includes TaskGroup and timeout examples.

The wider P2 roadmap is **not complete**: real Iceberg DML,
Scala/PyFlink runtimes, per-chapter SQL dialect comparisons, pytest/Polars lesson expansion and deeper new-topic
coverage still require work. This batch does not claim production PostgreSQL, cloud IAM or deployed orchestration
validation. The tool freshness and reader/SEO updates from #73–#75 are merged and preserved.

**Current Status**: All P0 and P1 items from the 2026-11-09 site review are merged (#67-#73): verified errors fixed,
results shown on the site, a pager on every page, 103 notebooks after merges with redirects for old URLs, SQL chapters
in dependency order, a Legacy shelf, stronger practice checks with difficulty tags, a PySpark capstone, and reader/SEO
polish. The P2 freshness pass is on `feat/review-p2-freshness` (33 tool pages); real engines, new topics and
payload size are next. Notebooks are Colab-runnable, executed by
CI on PySpark 4.0 (JDK 17), and stored in `notebooks/topics/<tool>/`; the site lists 43 tools.

## Completed

- 2026-11-10: P2 freshness pass (`feat/review-p2-freshness`). 33 tool pages updated for 2025-26 releases, each with
  a `*Last reviewed: November 2026, against <tool/version>.*` line; new version facts were checked against official
  docs or release notes, and five surprising ones re-checked by hand (Spark 4.3, Kafka 4.4, dbt v2 GA, Dataplex ->
  Knowledge Catalog, Cloud Composer -> Managed Service for Apache Airflow).
  - Spark and streaming: Spark Connect, VARIANT and Python Data Source cells (runnable on 4.0),
    `transformWithStateInPandas`; Kafka 4.x (ZooKeeper removed, KIP-848, share groups and DLQ) and an error-handling
    consumer loop; Flink 2.x and Flink CDC; NiFi 2.x and Python processors; Hive 4 with Iceberg and the metastore as
    a catalog; Trino release numbering and corrected connector write support.
  - Formats: Delta table features with liquid clustering first; Iceberg format v3 and neutral catalogs (REST,
    Polaris, S3 Tables); Hudi 1.x and an explicit "this is a model" note; Parquet page index, bloom filters,
    encodings, field IDs, encryption and new types, with two runnable pyarrow cells (`pyarrow>=26`).
  - Warehouses: Redshift AUTO keys, AQUA status, Serverless, zero-ETL, data sharing, streaming, Iceberg; Snowflake
    Gen2, Cortex, Open Catalog/Polaris, hybrid tables; BigQuery editions, managed Iceberg, search and vector indexes,
    continuous queries; ClickHouse JSON type, lightweight updates, SharedMergeTree; Greenplum status and Cloudberry.
  - NoSQL and search: Cassandra 5.0 and Accord status; Elasticsearch ES|QL, logsdb, `semantic_text`, OpenSearch at
    the Linux Foundation; MongoDB Search/Vector Search and Queryable Encryption; DynamoDB global tables and zero-ETL;
    Bigtable SQL and continuous materialized views; Bigtable/HBase cross-links.
  - Cloud and orchestration: Azure rebuilt around Microsoft Fabric/OneLake with Synapse as the existing path and a
    migration section; Databricks Lakehouse Federation and UCX; AWS S3 Tables and IaC; GCP editions, Knowledge
    Catalog, Dataform; Looker vs Data Studio; dbt v2, microbatch, Mesh and the Semantic Layer; Airflow 3 framing,
    AssetWatcher and HITL; Kubernetes batch schedulers.
  Verified: all 33 changed notebooks run top to bottom (PySpark 4.0.5, JDK 17); format check and audit pass on all
  103; pytest (44), vitest (81), ESLint and `next build` pass.
- 2026-11-10: P2 reader and search.
  On `feat/review-p2-reader`, based on master after #72:
  - Label Spark/DuckDB SQL wrappers accurately and describe assertion-bearing cells as checked examples.
  - Render the section index with the search page; warm and cache the palette index before the first search.
  - Keep mobile top-bar controls in a non-wrapping 48px row.
  - Add canonical URLs on home, topic, notebook and search pages, a 1200×630 PNG social image (SVG source retained),
    large-image Twitter metadata and WebSite JSON-LD.
  - Measured completed Pages run 42829280321: notebook outputs took 7m10s (13:58:05–14:05:15 UTC);
    build job 8m38s and total workflow about 10m40s. This is a post-change baseline, not a proven regression versus
    the old workflow; earlier runs need a comparable dataset before attributing a timing difference.
  Verified: site tests (81), ESLint, TypeScript and static production build; browser review of SQL labels and immediate
  search results. No notebook content changed in this batch. The wider P2 tool freshness pass, real-tool examples,
  new topics, Python additions, SQL translations, shared-code deduplication and HTML payload reduction remain pending.
- 2026-11-10: Practice verification.
  Completed the interrupted P1 practice work on `feat/review-p1-practice`:
  - Python challenges 1–9 and drills 1–9 now have difficulty estimates and 6–10 labelled checks per exercise.
    The binary-search explanation compares the middle value with the right boundary. Pipeline-context notes connect
    the algorithm challenges to data work.
  - File drills test replacement and partial-write failures: original content survives and temporary files are removed.
    The reference atomic writer cleans up in `finally`. Retry drills reject non-positive attempt counts.
  - Concurrency drills test result order, bounded concurrency, cancellation and errors. Instrumented lock scopes reject
    unlocked counter and queue implementations on five repeated trials. The queue exercise explicitly explains that
    CPython list append is atomic; scheduler timing is not used to claim a guaranteed race.
  - Data-engineering drill 7 implements canonical JSON SHA-256 upserts, timestamp/hash tie-breaking, stale-row rejection,
    immutable inputs and idempotent replay. Newer unchanged payloads advance version metadata.
  - SQL 13 and all 34 PySpark challenges have difficulty estimates. The 46-cell PySpark capstone replaces repeated
    lessons with a batch pipeline and 12 interview questions; it links to modules 1–8.
  - Added `scripts/verify_practice_answers.py`: nbclient executes temporary notebook copies with reference answers,
    checks scores and rejects wrong answers without storing outputs in source notebooks.
  Verification: all 21 changed notebooks execute cleanly (PySpark 4.0 with Java 17); notebook format/audit pass for all
  103 notebooks; Python tests (44), site tests (79), ruff, ESLint, TypeScript and production build pass.
  The broader P2 freshness, new-topic and site-performance roadmap remains pending; this entry covers the P1 practice work.
- 2026-11-10: Review P1, SQL chapter order and the Legacy shelf (`feat/review-p1-sql-order`, stacked on #70).
  - SQL chapters renumbered into dependency order: 1 basics, 2 joins, 3 NULL handling, 4 CASE, 5 aggregations and CTEs,
    6 set operations, 7 types, functions and JSON, then 8-14 unchanged. Six files renamed (`sql-06-joins` ->
    `sql-02-joins`, `sql-04-null-handling` -> `sql-03-…`, `sql-05-case-expressions` -> `sql-04-…`,
    `sql-02-aggregations-and-ctes` -> `sql-05-…`, `sql-07-set-operations` -> `sql-06-…`,
    `sql-03-types-functions-and-json` -> `sql-07-…`). Titles, links and every "[SQL N…]" label across the notebooks
    now match the file they point to. SQL 0's table and reading advice follow the new order, and SQL 1 calls its
    join, CASE and NULL sections previews. The six old URLs redirect (entries in `site/lib/retired.ts`), and saved
    progress and stars move.
  - Legacy shelf: Flume, Greenplum, Hadoop, HBase and Impala carry a `legacy` note in `site/lib/tools.ts` that names
    what new pipelines use instead. They sort after the active tools in their category (`compareTools`), show a
    "Legacy" label on the home page cards, and a note on their tool and notebook pages.
  Verified: the 11 changed SQL notebooks run top to bottom on PySpark 4.0.5; format check and audit pass; vitest (79),
  tsc, eslint and `next build` pass; the old SQL URLs redirect; checked in the browser.
- 2026-11-10: Review P1, merged notebooks and one home per topic (`feat/review-p1-merge-notebooks`). 106 notebooks
  became 103:
  - `data-warehousing` merged into `data-modeling`, now "Data modeling and warehousing" (13.5K -> 11.6K words, 13
    exercises, one model shared by all examples; closed `BETWEEN` SCD2 and point-in-time code dropped in favour of the
    half-open versions).
  - `pyspark-tuning` merged into `pyspark-07-monitoring-and-performance`, now "PySpark 7: monitoring, performance and
    tuning" (all eight "Try it" exercises kept; module 7's weaker duplicates dropped). The PySpark overview and the
    Databricks salting link point to it.
  - `python-interview-basics` retired: type hints moved to Python 3, dates and time zones to Python 1, modules and
    `__main__` to Python 7, MRO, `NamedTuple`, container dunders and class context managers to Python 5, and 18
    interview questions to Python coding problems (Q13-Q30). The rest repeated the lessons.
  - Old URLs keep working: `site/lib/retired.ts` lists the retired notebooks, the build writes a redirect page at each
    old `/notebooks/<slug>/`, and saved progress and stars move to the new notebook (`migrateProgress`,
    `migrateStarred`). The build fails if a retired notebook still exists or its target is missing.
  - One home per repeated topic: NOT IN with NULLs in SQL 4, top-N in SQL 8, keep-latest in SQL 9, isolation, indexes,
    TRUNCATE and ACID in SQL 14; SQL 1, 2, 13, 14 and the SQL reference keep short summaries with links, and the
    reference reads as a cheat sheet. Data contracts live in data-governance, checks and freshness in data-quality,
    lineage, SLOs and alerting in data-observability, idempotency, backfills and replay in system-design; near-duplicate
    sections inside system-design, cost-optimization and change-data-capture were merged.
  - The learning path drops the retired notebooks (Process at scale is the PySpark track).
  Verified: all 23 changed notebooks run top to bottom on PySpark 4.0.5 with JDK 17; format check and audit pass on
  all 103; pytest, vitest, ruff, eslint, tsc and `next build` pass; the three redirect pages point at the right notebooks.
- 2026-11-10: Review P1, navigation and drills (`feat/review-p1-navigation`, PR #69, merged). The reader's pager now follows the
  learning path first (Parquet -> Delta Lake -> Iceberg, Airflow -> Kafka -> Flink, Python 9 -> SQL 0), then the
  notebook's tool, then its category, so single-notebook tools such as Avro link onward. Before, 39 pages had no pager;
  now all 106 do, and the 12 without a "next" link are last in their order. Rules are in `site/lib/pager.ts`
  (`pickNeighbours`), with unit tests. SQL 13's 22 answer cells are tagged `solution`, so the reader keeps them closed
  until opened, and the intro says to write the query first. Verified: SQL 13 runs on PySpark 4.0.5, vitest (72),
  tsc, lint, the notebook audit and `next build` pass; checked in the browser.
- 2026-11-09: Results on the site (`feat/site-rendered-outputs`). The reader now shows each code cell's output under
  it. Notebooks stay output-free in git: `scripts/run_notebooks.py --output-dir build/executed` (`make outputs`) saves a
  copy of each notebook that runs cleanly, with trimmed outputs (no setup-cell noise, no HTML, no ANSI colour, text
  cut at 60 lines or 6,000 characters, PNG charts up to about 300 KB, errors as name and message). The site build
  reads those copies when `NOTEBOOK_OUTPUTS_DIR` is set and matches outputs to cells by id, only while the source is
  unchanged (`attachOutputs` in `site/lib/notebook-parse.ts`). The header note says where results come from. The
  Pages workflow installs Java 17 and the notebook packages, runs `make outputs` (a failure there publishes that
  notebook without results instead of blocking the deploy) and builds with the copies. `make build-with-outputs`
  does the same locally. Tests: 10 pytest cases (trimming, log-noise filtering and a real `run_one` execution), 8 vitest cases for parsing
  and matching.
- 2026-11-09: Site review and P0 fixes (`fix/handbook-review-p0`, PR #67, merged). A full review of the site (106 notebooks, home,
  search) is in `docs/reviews/2026-11-09-site-review.md`: overall 7.0/10, scores per dimension, track and notebook,
  and a P0/P1/P2 roadmap. Fixed the verified errors: the per-batch `pandas_udf` z-score in PySpark 8 (now a global
  aggregate broadcast back, plus a note on reusing training stats); `collect()` inside `foreachBatch` in PySpark 6
  (now an idempotent per-batch Parquet write); the Scala Spark job rewritten in Scala 2.13 to match the build, which
  now uses Spark 4.0.1; BigQuery time-travel window (2-7 days plus a 7-day fail-safe); Elasticsearch AGPL licence;
  Flink restart strategy via configuration (`RestartStrategies` was removed in 2.0); dbt intro added and `tests:` keys
  renamed `data_tests:` in dbt, data-quality and data-observability; Azure "Try it" numbering; a Redis licensing and
  Valkey section; the zoneinfo version claim; stale `0N_*.ipynb` references in the PySpark overview, PySpark 8,
  concepts-end-to-end, the SQL reference, the question bank and both Python practice notebooks; typos in Hadoop, Trino
  and data structures. Python 9 gains a lookback-window section for late and tied rows. SQL 0 replaces its changelog
  with a learner guide (who it is for, how to use it, the Spark SQL dialect). The PySpark overview links its practice
  notebooks and states prerequisites. Verified: all 22 changed notebooks run top to bottom on PySpark 4.0.5 with JDK 17,
  the format check and audit pass, pytest (34), vitest (60), lint and `next build` pass.
- 2026-11-09: PySpark coding challenges expanded (`feat/pyspark-coding-challenges`): 19 new problems join the five
  first-edition ones, 24 in total in `notebooks/topics/pyspark/pyspark-coding-challenges.ipynb`. Part one covers
  DataFrame manipulation (when/otherwise, nulls, strings, dates, explode, pivot and stack, UDF vs built-ins), joins
  (semi and anti, broadcast with a plan check, self join, full outer reconciliation, non-equi), window functions
  (rank family, lag and lead, row and range frames, top-N with ties, first and last frames) and aggregations (null
  semantics, rollup). Every problem has a statement, sample input and expected output; each solution is a code cell
  tagged `solution`. The reader shows solutions as closed panels, and the formatter keeps cell tags. Verified: the
  notebook runs top to bottom on PySpark 4.0.5 with JDK 17 (`scripts/run_notebooks.py`), `audit_notebooks.py`
  passes, pytest passes with new tests for the tag, and the site passes vitest (new solution-kind tests), lint and
  `next build`. The prerendered reader has 24 solution panels, none open.
- 2026-11-09: "Tools" renamed to "Topics" in the UI (`feat/learning-path`): the home page section, the sidebar
  label, the starred group and page, star labels and empty-state text. Concepts and Interview prep are not tools, and
  the folders already live in `notebooks/topics/`. URLs stay `/tools/<folder>/` so existing links keep working.
- 2026-11-09: Learning path replaces the learning map (`feat/learning-path`). The old map pointed each node at a single
  notebook (the "PySpark" node was a one-minute overview), covered 14 of 106 notebooks, scrolled sideways on phones and
  never said what to read next. The path has six stages (Foundations, Process at scale, Model and test, Store,
  Orchestrate and stream, Interview practice). Each step is a whole track, for example all nine Python lessons, and shows
  "2 of 9 done" with a progress ring. A "Next up" card links to the first unfinished notebook on the path. Stages wrap
  into a grid, with no sideways scrolling. The path covers 56 notebooks. Rules (`summarizeStep`, `nextUp`,
  `validatePath`) are in `site/lib/learning-map.ts`, with unit tests. The build fails if a step names an unknown notebook.

- 2026-11-09: Collapsible, starrable sidebar groups (`feat/collapsible-sidebar`): each tool category in the sidebar is a
  collapsible group. The group holding the current tool opens by default, and open or closed choices are saved in the
  browser. Each tool row has a star; starred tools are pinned in a "Starred tools" group at the top of the sidebar and
  listed on `/starred/` with starred notebooks. The icon rail and the phone strip show every tool without headers. The
  phone strip no longer stretches on short pages. "Orchestration and transformation" is shortened to "Orchestration".
  Rules are in `site/lib/sidebar.ts`, with unit tests.

- 2026-11-09: Tool categories (`feat/tool-categories`): the sidebar and the home page group the 43 tools under 12
  categories: Languages, Processing engines, Streaming and ingestion, Orchestration and transformation, File and table
  formats, Data warehouses, NoSQL and search, Cloud platforms, BI and dashboards, Containers and infrastructure, Concepts
  and Interview prep. Each tool in `site/lib/tools.ts` has a `category`. Inside a category, tools sort without their
  "Apache" or "Amazon" prefix.

- 2026-11-09: Notebook names standardized (`chore/standardize-notebook-names`): 31 files renamed to lowercase kebab-case that
  starts with the tool name. Examples: `01_python_basics` became `python-interview-basics`, `03_sql_interview_questions` became
  `sql-00-start-here`, `python-01-practice-*` became `python-drills-01-*`, and `dwha` became `data-warehousing`. The `spark/`
  folder is now `pyspark/`, with `pyspark-00-overview` first, and `mongo/` is now `mongodb/`. Series titles follow
  `<Series> <N>: <subject>`, and other titles use sentence case without "for Data Engineers" (66 titles). The 14 SQL
  notebooks use the standard setup cell instead of `!pip install`, and all 14 run cleanly. The naming rules are in
  CONTRIBUTING.md. Reader URLs changed for the renamed notebooks.

- 2026-11-08: Notebooks grouped by tool (`refactor/topics-tool-folders`): every notebook moved into
  `notebooks/topics/<tool>/`, 43 tool folders in all. Python is split into `python/learning/` (9 lessons) and
  `python/practice/` (drills, coding challenges and interview basics). Non-tool subjects such as data modeling and CDC sit
  in `concepts/`. Links and Colab badges were rewritten for the new paths. The site now lists tools in the sidebar and as
  cards on the home page. Each tool has a page at `/tools/<tool>/` that lists its subtopics in order (lessons, then
  drills, challenges and interview questions), with one section per subfolder. `site/lib/tools.ts` replaces the group
  registry, and the build fails when a folder and the registry disagree. Starred notebooks moved to `/starred/`. Reading
  progress and stars are keyed by file path, so progress saved before the move does not carry over.

- 2026-11-08: Review fixes (`fix/review-usability`): the reader counts `check(...)` calls as self-checks (it counted only
  `assert` before), so practice pages no longer show "0 self-checks". The catalog filter is split into Learn and Practice
  rows that wrap instead of scrolling. Four titles were clarified (`01_python_basics`, `04_pyspark_concepts`,
  `05_interview_questions`, `hadoop`). Every notebook page says results are not stored. The "How to use this notebook"
  box in 18 practice notebooks is collapsed by default. On screens up to 1100px, a collapsible "On this page" list
  sits above the text, because the sidebar section list was hidden there. The practice chips use full names.
- 2026-11-08: PySpark split into modules (`fix/pyspark-modules`): `topics/spark.ipynb` is now an overview that links to
  eight notebooks, `pyspark-01-foundations` through `pyspark-08-real-world-and-interviews`. The existing lessons moved
  unchanged, with a new intro, key takeaways and a next link in each module. Each module runs on its own: it repeats the
  setup and sample tables, and shared helpers (`plan_of`, `daily_revenue`, `raw_customers`, `bronze_orders_raw`) are
  carried into the modules that use them. Each module runs top to bottom on PySpark 4.0 with OpenJDK 17.

- 2026-11-08: Site review fixes (`fix/site-header-and-groups`): the sidebar has two sections, "Learn" and "Practice".
  Practice groups sit together after the learning groups, and each one names the topic it trains. The group registry
  exports `LEARNING_GROUPS` and `PRACTICE_GROUPS` with a `section` field, and `repoPathFor` resolves a notebook's file,
  including per-notebook `folderOverrides`. A test checks the order and uniqueness of labels. The nine algorithm
  notebooks are renamed `python-challenges-01-…` through `python-challenges-09-…` and titled "Python coding challenges",
  so no site or repo text names a third-party problem site. On phones the top-bar search collapses to an icon so the
  GitHub link and theme toggle fit, and the learning map shows a "Swipe sideways" hint.

- 2026-11-08: Every Python coding challenge exercise now has two worked examples (input and output, generated by running the notebook's own solution) and a 💡 tip in a collapsed block. The hint lines were replaced by these tips.

- 2026-11-08: Python coding challenges (`feat/leetcode-practice-notebooks`): nine notebooks,
  `python-challenges-01-arrays-and-hashing` through `python-challenges-09-backtracking-heaps-intervals-design`, 46 problems
  in all. Problem choice follows common interview topics. Statements are paraphrased and solutions were written fresh. Each solution is annotated with its approach, complexity, inline comments and a tip. Each exercise has a check cell and a collapsed solution. Registered
  as the "Python coding challenges" group.

- 2026-11-08: Hands-on Python practice notebooks (`feat/python-collections-deep-dive`): one per chapter,
  `python-01-practice-values-and-types` through `python-09-practice-data-engineering`. Each has six exercises with
  a question, a code cell to fill in, and a check cell. Checks print `pass` or `todo` and never stop the run, so every
  notebook still runs top to bottom in CI. The last cell prints the score. The notebooks are registered in the site
  as a "Python practice" group. Each solution sits in a collapsed "Show solution" block under its check cell (a `<details>` element), so the answer is one click away. Each solution was checked against its exercise.

- 2026-11-08: All Python chapters rewritten in the collections style (`feat/python-collections-deep-dive`):
  `python-01` to `python-09` each define a rule before using it, show it in an assert-checked example, and name where
  it shows up in data work. Assert count across the eight chapters other than collections rose from 213 to 343. New coverage includes:
  Decimal quantize and integer cents, bytes versus text and encodings, truthiness and `None`, `match`, the LEGB scope
  rule and late-binding closures, `functools.wraps` and decorators with arguments, `itertools` (`accumulate`,
  `zip_longest`, `product`), generator `yield from`, custom iterables, class `__eq__` and `__hash__`, composition, ABCs,
  `__post_init__`, `order=True`, `enum.auto`, BOM handling with `utf-8-sig`, JSON `default=`, exception hierarchy and
  `finally` after `return`, logging with lazy `%s` formatting, table-driven tests, `queue.Queue`, `as_completed`,
  `asyncio.wait_for`, and `gather(return_exceptions=True)`. The data-engineering chapter drops the `__import__` hack
  and names its constants. Every code cell runs on Python 3.13 with no failures.

- 2026-11-08: Python collections explained from first principles (`feat/python-collections-deep-dive`):
  `python-02-collections` now defines each rule before using it and shows it in an assert-checked example. Sorting
  explains `key=` and stability with a worked tie (equal keys keep input order), multi-field sorts, and `None` in sorts.
  New sections cover list slices and copies, removing items during iteration, `enumerate` and `zip(strict=True)`,
  tuple unpacking and `namedtuple`, set algebra and `frozenset`, dict views and merges, comprehensions (filter versus
  choose, nested `for`), safe nested lookups, mutable default arguments, `deque` with `maxlen`, and `ChainMap`. Practice
  has four questions with answers. All 27 code cells run on Python 3.13.

- 2026-11-07: SQL path explained from first principles (`feat/sql-path-explanations`): all 14 chapters `sql-01` to
  `sql-14` reviewed. Terms are defined before use, rules that were only stated now have hand-worked examples and
  asserts (SQL path asserts rose from about 100 to about 490), every concept section has a "Where you'll use it" note,
  and practice questions that copied the worked examples were replaced. Factual fixes: `INSERT OVERWRITE` on a
  partitioned table replaces the whole table in Spark's default static mode (sql-12); Spark prunes partition columns
  even through a function (sql-11, sql-14); the SCD2 overlap check missed equal start dates (sql-11); the "strictly
  newer" dedup wording contradicted its query (sql-09). No `##` heading was renamed, so saved reading progress is kept.

- 2026-11-07: Content widens when panels collapse (`feat/wide-content-collapsed`): with the sidebar collapsed the page
  grows to `--content-wide` (1480px), and with either panel collapsed the reader's article fills its column instead
  of keeping its 740px reading width. Measured at 1600px: article 740 (both open), 984 (sidebar collapsed), 1056
  (contents collapsed), 1220 (both collapsed).

- 2026-11-07: Collapsible sidebars (`feat/collapsible-sidebars`, PR #45): the sidebar folds into a 68px icon rail with hover and
  focus labels (top-bar button or <kbd>[</kbd>), and the reader's table of contents folds into a button (<kbd>]</kbd>).
  Both states are saved in localStorage and applied before first paint; phones keep their existing layout. Fixed a
  bug on master: the theme boot script was exported from a `"use client"` module, so the layout inlined a client
  reference instead of the script, which threw a syntax error and never restored a saved theme. The script now lives
  in `site/lib/boot.ts` with a vitest that runs it in a sandbox. Verified in the browser at 1360px (collapse, expand,
  reload persistence, labels, clean console) and 375px.

- 2026-11-07: Collections grouping and counting explained (`fix/python-collections-explained`): the section in
  `python-02-collections` now has one subsection per method with a worked example and assertions: the manual `if`
  check, `dict.setdefault`, `defaultdict(list)` and `defaultdict(int)`, `Counter`, `most_common`, `update`, `+`/`-`,
  `subtract`, `elements` and `total`. Interview notes cover setdefault's per-call default and defaultdict's read-inserts.

- 2026-11-07: Site rebuilt from the mockups (`feat/app-pipeline-redesign`, PR #44). Design tokens, Instrument Sans and a
  light/dark toggle in `site/app/globals.css` and `components/theme.tsx`; app shell with a group sidebar
  (`components/AppShell.tsx`). Home: learning map drawn from `lib/learning-map.ts` (validated against the registry),
  resume cards and weekly activity, and a catalog table filtered by `?group=` (sidebar links set it). New reader at
  `/notebooks/<slug>/`: markdown via `marked`, code highlighted at build time with highlight.js, a cell map
  (explanation, code, self-check), a table of contents that marks a section read when you scroll from it into the next
  heading (jumps do not count), mark-as-done, previous/next. Each `.ipynb` is served at `/files/<slug>.ipynb` for
  downloading. ⌘K / Ctrl+K / `/` open a search palette over notebooks and section headings, loaded from
  `/search-index.json`; `/search?q=` lists everything. Progress lives in localStorage like stars. Tailwind removed (it
  was unused). 43 vitest tests for the pure data layer in `site/tests/`, run by `make test`. Verified with lint,
  typecheck, a Pages-style build (80 notebook pages) and browser checks at 1360px and 375px in light and dark.

- 2026-11-07: Design mockups (`feat/handbook-mockups`, PR #43): static HTML in `docs/mockups/` with no build step.
  Library with a learning map drawn as a DAG (green passed, amber in progress, hollow not started), resume cards and a
  catalog table; notebook reader with a cell map, stage diagram, rendered DataFrame output, takeaways and self-checks;
  a search palette with a live preview and arrow-key navigation; an index with live thumbnails. Shared tokens in
  `styles.css` (Instrument Sans, lagoon accent), light/dark toggle in `theme.js`, focus styles and reduced motion.
  Checked at 1360px and 375px in light and dark. The mockups assume per-reader progress tracking and show section
  counts and reading time, which the `feat/redesign-site` direction removed; that needs a product decision.
- 2026-11-07: Mockups ship to GitHub Pages at `/data-engineering-handbook/mockups/` (`feat/handbook-mockups`, PR #43).
  New Makefile targets `mockups` (serve locally) and `mockups-bundle` (copy into `site/out/mockups`); `make build` and
  the Pages workflow both bundle them. Pages are `noindex`. `tests/test_mockups.py` checks that local links are relative
  and resolve. Verified with a Pages-style build (`NEXT_PUBLIC_BASE_PATH=/data-engineering-handbook make build`) served
  under the prefix: the site and all mockup routes return 200 and render. Goes live once PR #43 merges, because only
  `master` may deploy to the `github-pages` environment.

- 2026-11-07: SQL topic engine labels and site configuration docs (`fix/sql-topic-engine-labels`): six engine-specific
  SQL sections are marked *(engine-specific)* with a legend in the intro, and the Dialect differences table is named as
  the syntax reference. README has a Site URLs section on `NEXT_PUBLIC_BASE_PATH` and `NEXT_PUBLIC_SITE_URL`, and the
  `site.ts` comment says when both must be set. Removed leftover merge-conflict markers from PROGRESS.md.

- 2026-11-07: Notebook depth and real-world coverage (`feat/real-world-sections`): the classes chapter starts from
  what a class is and how to create one; chapters 3, 6 and 8 define decorators, context managers and threads or
  coroutines; every Python and SQL concept section has a "Where you'll use it" section. Seven topic notebooks (docker,
  kubernetes, llm, looker, scala, superset, tableau) gained one per main part. Airflow, Kafka and dbt have one per
  question. Spark, Delta and Iceberg are in progress.

- 2026-11-07: Restyled the site (`feat/site-cool-palette`): a cool, light-first palette with one blue accent, Geist for
  headings instead of the serif, drawn-out kicker labels removed, primary buttons in the accent, and matching dark theme.
  Layout, content and behaviour are unchanged. The design detector reports no findings. `PRODUCT.md` records the product
  context for future design work.

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

- None.

## Next Steps

Remaining roadmap from `docs/reviews/2026-11-09-site-review.md` (P2), in priority order:

1. Freshness pass: done on `feat/review-p2-freshness` for 33 tool pages. Tool pages not yet carrying a
   "Last reviewed" line (concepts, BI, Docker, Scala, Flume, Impala, Hadoop, SQL/Python tracks) are next in line.
2. Run real tools instead of simulations where Colab allows: Delta/Iceberg MERGE in PySpark 5 and SQL 12, a real
   streaming source and windowed aggregation in PySpark 6, a dbt-duckdb project, scala-cli for Scala, a local PyFlink
   cell; label the remaining simulated cells.
3. New pages: open table format comparison, lakehouse and catalogs, DuckDB, Postgres, orchestration patterns,
   semantic layer, security/IAM, CI/CD and IaC for data.
4. Python track: state a 3.12 baseline; real pytest in Python 7; `asyncio.TaskGroup`/`timeout` in Python 8; Polars or
   PyArrow. Concepts: cut data-structures to its DE tail, move statistics to an appendix, give the LLM page a DE angle.
5. SQL: a dialect note or translation table (Postgres, Snowflake, BigQuery) in each chapter.
6. Shared code: the Spark setup repeated across PySpark modules and the grader harness in 18 practice notebooks.
7. HTML payload: pages average about 350 KB because content ships twice (HTML and the hydration payload).
8. `PRODUCT.md` still describes a stateless site; update it for reading progress, outputs and the reader.
9. Run one SQL notebook in a real Colab runtime with "Run all" (needs the owner's Google sign-in); Colab's Java is
   not verified.
10. The main checkout (`docs/interactive-viewer-spec`) has uncommitted site edits from an older layout (`app/`,
    `components/`); the owner should decide whether to keep or discard them.

## Blockers

- None.
