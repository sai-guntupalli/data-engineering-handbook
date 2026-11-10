# Handbook site review — 2026-11-09

Senior data engineer review of https://sai-guntupalli.github.io/data-engineering-handbook/ — all 106 notebooks plus
the home, search and license pages. Published version with a sortable score table:
https://claude.ai/artifact/4Q3qctuPTyHfwxpGbDrxpR (private to the owner).

**Overall: 7.0 / 10.** A great-looking handbook with unusually broad, mostly accurate content that has not yet been
edited as a whole: topics repeat across notebooks, many runnable cells simulate the tool instead of running it,
about a third of tool pages lag 2025–26 releases, and only the Python, SQL and PySpark series link to a next notebook.

## Method

- Crawled all 109 sitemap URLs (all HTTP 200), internal links, the 106 Colab source files (all resolve), metadata and
  page weight.
- Reviewed the UI on desktop and mobile, dark and light, and tested search.
- Extracted every notebook's rendered text and code and reviewed it in five tracks. Python notebook code was executed;
  other tracks were reviewed by reading and targeted searches. Every item under "Verified errors" was re-checked
  against the notebook text.

## Scorecard

| Dimension | Score | Why |
|---|---|---|
| Appearance & visual design | 8.5 | Product-grade reader UI, coherent themes; mobile header and missing outputs hold it back |
| Depth & breadth | 8.0 | 43 topics from Python to LLMs; a few thin tool pages and missing topics |
| Content accuracy | 7.5 | Mostly correct, Python code runs; about a dozen errors or stale claims |
| Navigation & discoverability | 7.0 | Strong search and progress map; no pager on 39 pages, half the notebooks off-path |
| Freshness (2025–26) | 6.5 | Airflow, Databricks, Kafka, AWS current; Flink, NiFi, Hudi, Redshift, Cassandra, Azure, Redis lag |
| Order & flow | 6.0 | Python lessons pair with drills; SQL re-teaches topics; concepts and tools have no reading order |
| Hands-on / runnability | 6.0 | Asserted examples are a strength, but no outputs, many simulations, drills show answers |
| Consistency & duplication | 5.5 | Topics repeated up to 6×, four SQL engines, mixed numbering, copy-pasted setup |

| Track | Score | Notebook mean |
|---|---|---|
| Python (29) | 7.0 | 6.9 |
| SQL (17) | 7.0 | 7.2 |
| PySpark, engines & streaming (23) | 6.8 | 6.6 |
| Formats, warehouses & NoSQL (17) | 6.5 | 6.5 |
| Cloud, BI & concepts (20) | 7.0 | 7.5 |

Standouts: Airflow (9), Python coding problems (9), Kafka, AWS, Databricks, CDC (8.5), SQL 8 window functions (8.5),
PySpark coding challenges (8). Weakest: PySpark overview (4), Scala (4), data structures (4), Greenplum (4.5).

## Verified errors (P0)

All fixed on `fix/handbook-review-p0` (see PROGRESS.md for what changed in each notebook).

- [x] `pyspark-08`: Series `pandas_udf` `zscore` uses `s.mean()`/`s.std()`, computed per Arrow batch, not globally.
- [x] `scala`: build sets `scalaVersion := "2.13.15"` but snippets use Scala 3 `given`/`using`; Spark 3.5.3 vs the
      PySpark 4.0 pin.
- [x] `pyspark-06`: the only runnable streaming cell calls `batch_df.collect()` inside `foreachBatch`.
- [x] `bigquery`: time travel "up to 30 days for managed disaster recovery" — it is a 2–7 day window plus a 7-day
      fail-safe.
- [x] `elasticsearch`: license table lists "Elastic License 2.0 / SSPL" only; AGPL was added in 2024.
- [x] `pyspark-00`, `pyspark-08`, `pyspark-concepts-end-to-end`: stale filenames (`04_pyspark_concepts.ipynb`,
      `06_pyspark_coding_challenges.ipynb`, `03_sql_interview_questions.ipynb`); overview module table unlinked.
- [x] `flink`: `from pyflink.common import RestartStrategies` is Flink 1.x (removed in 2.0); no version stated.
- [x] `dbt`: YAML uses `tests:` instead of `data_tests:`; intro truncated with "…".
- [x] `python-interview-basics`: "the zoneinfo module need Python 3.10+" (it is 3.9+); stale "02 Python coding
      problems" style cross-references. `python-coding-problems` points at "01 Python basics".
- [x] `azure`: exercises numbered "Try it 4, 5, 6, 8".
- [x] `redis`: no mention of Valkey or the 2024–25 license changes.
- [x] Typos: `hadoop` "Hive on TeX/Spark", `trino` "The coordinator renames tables", `data-structures` "doesnt",
      "a ordered collection".
- [x] `python-09`: watermark filter uses `<=` with no lookback, dropping late and tied rows; upsert uses `>=` but
      dedupe uses `>`.

## Structural issues

### Order and flow
- SQL ch1 already teaches joins, CASE and NULL, so ch4–6 re-teach them; recursive CTEs (ch2) come before joins.
- 39 standalone pages have no "next" link, including learning-path steps (Parquet → Delta → Iceberg, Airflow → Kafka →
  Flink).
- The learning path covers 56 of 106 notebooks; it says "PySpark 9 notebooks" while the overview says eight modules.
- Legacy tech (Flume, Impala, Hadoop, Greenplum, HBase) sits beside Kafka, Trino and dbt at similar length.
- Concepts have no reading order; data-modeling and data-warehousing are near-duplicates.

### Duplication
- NOT IN with NULLs is taught in 6 places; top-N in 4; dedup/upsert/SCD2 in 7.
- `sql-reference` covers all of `sql-14`; the question bank repeats both.
- PySpark 7, Spark tuning and concepts-end-to-end all re-teach skew, AQE, partitions and caching.
- `python-interview-basics` is about 70% a repeat of lessons 1–8.
- Data contracts are explained on 4 pages; freshness and alerting in both quality and observability.
- The same ~150-line Spark setup is in 8 notebooks; the same grader harness in 18.

### Hands-on reality
- No outputs are rendered on the site.
- Hudi, Cassandra, HBase, Greenplum, Scala, Flink, NiFi and Redshift cells are Python/DuckDB models of the tool.
- SQL 12 cannot run UPDATE/DELETE/MERGE on Spark temp views; PySpark 5 shows MERGE as text only.
- SQL 13 shows the expected result and the solution together; Python graders have 2–3 cases per exercise and the
  concurrency checks pass without a lock.

### Consistency and currency
- Four SQL engines with no stated rationale (Spark SQL, DuckDB, SQLite, Postgres in prose).
- Missing 2025–26 changes: Spark Connect, Kafka 4 (KIP-848, share groups), Flink 2, NiFi 2, Hudi 1.0, Iceberg v3,
  Cassandra 5, Redshift zero-ETL and data sharing, Snowflake Cortex/Polaris/Gen2, dbt microbatch.
- No "verified against version X" badges; the Python track never states a minimum Python version.
- Several topic pages still use interview-question headings ("What is the meaning of broker…", "Define graph?").

## Appearance and UX

Strong: consistent design, highlighted code with copy buttons, clear home hierarchy, section-level search, working
mobile reflow, no console errors, custom 404.

To improve:
- Mobile top bar wraps into two rows with an empty row and a large gap above the title.
- SQL cells are labelled "Python"; every lesson cell is labelled "Self-check" even plain demos.
- Search shows "Loading sections…" for about 2 s; notebook-level hits are thin.
- Pages average 347 KB of HTML (max 1 MB) because content ships twice (HTML + hydration payload).
- No `og:image`, canonical URL or JSON-LD.
- SQL 0 and PySpark 0 are 2-cell stubs; SQL 0 is mostly a changelog.

## Roadmap

| Pri | Work |
|---|---|
| P0 | Fix every verified error above; link the PySpark overview table; replace the SQL 0 changelog with a learner roadmap |
| P0 | Show outputs: execute notebooks in CI into a build-only copy and render the stored outputs |
| P1 | One canonical page per topic (NOT IN, top-N, dedup/SCD2, isolation, contracts, freshness, skew/AQE); merge modeling + warehousing and PySpark 7 + tuning; fold interview-basics into lessons |
| P1 | Fix SQL chapter order; add "Next in learning path" to standalone pages; put every notebook on a path or a Reference/Legacy shelf |
| P1 | Real practice: hidden solutions, difficulty tags, 6–10 edge-case tests per exercise, graders that catch the bug |
| P2 | Run real tools where Colab allows (Delta/Iceberg MERGE, Kafka source, dbt-duckdb, scala-cli, PyFlink); label remaining simulations |
| P2 | Freshness pass with version badges; new pages: table-format comparison, lakehouse catalogs, DuckDB, Postgres, orchestration patterns, contracts, semantic layer, security/IAM, CI/CD and IaC; Python typing, datetime, pytest, Polars |
| P2 | UX polish: mobile top bar, SQL cell labels, Solution cell type, pre-indexed search, og:image and canonical, lighter pages |

## Per-notebook scores

| Notebook | Score | Verdict |
|---|---|---|
| `python-01-values-and-types` | 7.5 | Floats, Decimal and encodings done well. No datetime anywhere in the track; one assert can never fail. |
| `python-02-collections` | 8.0 | Sorting stability, Counter and views. No heapq or bisect; no Python version baseline. |
| `python-03-control-flow-and-functions` | 8.0 | wraps, late binding, mutable defaults, match. No typing in a functions chapter. |
| `python-04-iterators-and-generators` | 8.5 | Clear on single-use iterators and batching. Missing send/close and itertools.batched. |
| `python-05-classes-and-dataclasses` | 8.0 | Full ladder from __init__ to ABCs and enums. No __slots__ or StrEnum. |
| `python-06-files-and-formats` | 8.5 | pathlib, BOM, JSONL and atomic writes. No Parquet or Arrow. |
| `python-07-errors-logging-and-testing` | 6.5 | Testing is thin: no pytest, fixtures or mocks. Logging config is shallow. |
| `python-08-concurrency` | 7.5 | Rule of thumb is right. ProcessPool never runs; no TaskGroup or asyncio.timeout. |
| `python-09-data-engineering` | 8.0 | Best lesson (idempotency, quarantine, backoff). Watermark drops late rows and ties. |
| `python-drills-01-values-and-types` | 7.0 | Best grader coverage (21 checks); a few exercises repeat the lesson. |
| `python-drills-02-collections` | 7.0 | Good Counter and stability exercises; rotate is generic. |
| `python-drills-03-control-flow-and-functions` | 6.5 | FizzBuzz is below level; decorator exercise is good. |
| `python-drills-04-iterators-and-generators` | 7.5 | Infinite-stream checks force real laziness. |
| `python-drills-05-classes-and-dataclasses` | 7.0 | Covers each topic once; hash/eq exercise is the highlight. |
| `python-drills-06-files-and-formats` | 6.0 | About one check per exercise; the atomic-write check can't detect a non-atomic write. |
| `python-drills-07-errors-logging-and-testing` | 7.0 | Chaining and retry exercises are good; no pytest practice. |
| `python-drills-08-concurrency` | 6.5 | Thread checks pass even without a lock (nondeterministic grader). |
| `python-drills-09-data-engineering` | 7.0 | Right topics, but no upsert or hash-diff drill. |
| `python-challenges-01-arrays-and-hashing` | 6.0 | Standard LeetCode-style set; 2–3 checks per exercise. |
| `python-challenges-02-two-pointers-and-sliding-window` | 6.0 | Minimum Window Substring is a big early difficulty jump. |
| `python-challenges-03-stacks-and-monotonic-stacks` | 6.0 | Largest Rectangle is too hard this early. |
| `python-challenges-04-binary-search` | 6.5 | Good binary search on the answer (Koko). |
| `python-challenges-05-linked-lists` | 5.0 | Low DE relevance. |
| `python-challenges-06-binary-trees` | 5.0 | Low DE relevance. |
| `python-challenges-07-graphs-and-grids` | 6.0 | Course Schedule is topological sort, but never tied to DAGs or lineage. |
| `python-challenges-08-dynamic-programming` | 5.5 | Fine basics; little DE value. |
| `python-challenges-09-backtracking-heaps-intervals-design` | 6.0 | Only 7 checks; duplicates coding-problems P6 and P14. |
| `python-coding-problems` | 9.0 | Best in track: 14 problems framed as DE tasks, with edge-case tests. 124 KB in one page. |
| `python-interview-basics` | 6.5 | About 70% repeats the lessons; wrong zoneinfo version; mismatched cross-references. |
| `sql-00-start-here` | 6.0 | Mostly a maintainer changelog; no audience, prerequisites or time estimate. |
| `sql-01-basics` | 7.0 | Teaches logical evaluation order well; also teaches joins, CASE and NULL, which later chapters repeat. |
| `sql-02-aggregations-and-ctes` | 7.5 | GROUPING() and correlated subqueries; recursive CTEs too early; Spark 4-only syntax. |
| `sql-03-types-functions-and-json` | 7.0 | Useful, but Spark-only functions presented as general SQL. |
| `sql-04-null-handling` | 8.0 | Excellent three-valued logic; claims NULLS LAST works 'on every engine'. |
| `sql-05-case-expressions` | 7.0 | FILTER and the ELSE 0 trap; thin; PIVOT is Spark syntax. |
| `sql-06-joins` | 8.0 | Cardinality and ON vs WHERE are strong; arrives after joins are already in use. |
| `sql-07-set-operations` | 7.0 | Tidy rules; thin for a whole notebook. |
| `sql-08-window-functions` | 8.5 | Strongest SQL chapter: ROWS vs RANGE, named WINDOW, notes Spark has no QUALIFY. |
| `sql-09-deduplication` | 8.0 | Deterministic tie-breaking; overlaps sql-12 and sql-13. |
| `sql-10-time-series` | 8.0 | UTC sessions, spines, gaps and islands, cohorts. |
| `sql-11-modeling-and-optimization` | 6.5 | Mixes data modeling with Spark plan reading. |
| `sql-12-views-and-changing-data` | 7.5 | Honest about Spark limits, but its core DML can't run. |
| `sql-13-interview-drills` | 7.5 | 22 realistic problems, but answers are shown with the problem. |
| `sql-14-interview-concepts` | 6.0 | Index and isolation topics can't be demonstrated in Spark; overlaps the reference. |
| `sql-reference` | 6.5 | Broad and flags engine-specific syntax, but runs on DuckDB unlike the rest of the track. |
| `interview-question-bank` | 6.5 | Concise model answers; a fourth engine (SQLite); repeats the folklore that GROUP BY beats DISTINCT. |
| `pyspark-00-overview` | 4.0 | Stub with stale filenames and an unlinked module table. |
| `pyspark-01-foundations` | 7.5 | Catalyst, Tungsten and lazy plans; heavy setup boilerplate. |
| `pyspark-02-reading-sql-and-cleaning` | 7.0 | Explicit schemas; little on read modes (PERMISSIVE/FAILFAST). |
| `pyspark-03-joins-and-aggregations` | 7.5 | Fan-out checks and a verified broadcast plan; no other join hints. |
| `pyspark-04-windows-and-nested-data` | 8.0 | Best PySpark module: frames, time zones, ANSI mode vs try_cast. |
| `pyspark-05-writing-pipelines-and-quality` | 6.5 | MERGE, schema evolution and time travel shown as text only. |
| `pyspark-06-structured-streaming` | 5.5 | One runnable cell, and it uses collect() inside foreachBatch. |
| `pyspark-07-monitoring-and-performance` | 6.5 | Spark UI lesson with the UI disabled; duplicates the tuning notebook. |
| `pyspark-08-real-world-and-interviews` | 5.5 | pandas_udf zscore bug; stale link; generic interview section. |
| `pyspark-tuning` | 7.5 | Measure-first discipline and 8 exercises; exercises are arithmetic, not Spark. |
| `pyspark-concepts-end-to-end` | 6.0 | 108 KB that re-teaches modules 1–7; stale cross-references. |
| `pyspark-coding-challenges` | 8.0 | 34 problems with hidden solutions; problems 25–34 are bare stubs. |
| `scala` | 4.0 | No Scala actually runs; Scala 3 syntax on a 2.13 build. |
| `flink` | 7.0 | Good decision rules; Flink 1.x APIs; no runnable PyFlink. |
| `hadoop` | 6.5 | HA, erasure coding and YARN; 'TeX' typo; too much history. |
| `hive` | 6.5 | Solid metastore coverage; little on Hive 4 or Iceberg. |
| `impala` | 6.0 | Accurate but 59 KB for a niche engine. |
| `trino` | 7.5 | Federation, dynamic filtering, FTE; 'renames tables' typo. |
| `flume` | 5.0 | Sound but legacy; should be a short appendix. |
| `kafka` | 8.5 | KRaft, idempotence, transactions, Connect; only 6 code cells; no KIP-848. |
| `nifi` | 5.5 | No NiFi 2.x; no runnable flow. |
| `airflow` | 9.0 | Current Airflow 3: Assets, deferrable operators, Deadline Alerts. Intro still says 2.x. |
| `dbt` | 7.0 | Slim CI, contracts, unit tests; old tests: key; truncated intro. |
| `avro` | 7.5 | Real fastavro, byte-level detail, schema evolution. |
| `delta` | 7.0 | Runnable delta-rs; Z-order still dominates over liquid clustering. |
| `hudi` | 5.5 | Pure-Python simulation; nothing on Hudi 1.0. |
| `iceberg` | 7.5 | Real pyiceberg; no v3, Puffin or S3 Tables. |
| `parquet` | 7.0 | Runnable pyarrow; thin on bloom filters, page index, encodings. |
| `bigquery` | 6.0 | 93 KB of prose; wrong time-travel window; no editions tiers. |
| `clickhouse` | 7.0 | ReplacingMergeTree, projections, MVs; no runnable ClickHouse DDL. |
| `greenplum` | 4.5 | Wall of prose; status under Broadcom and the Cloudberry fork missing. |
| `redshift` | 5.5 | Leans on AQUA and interleaved sort keys; no zero-ETL or data sharing. |
| `snowflake` | 6.5 | Good cost detail; no Cortex, Polaris or Gen2; 107 KB. |
| `bigtable` | 6.5 | Good key design; leftover interview headings; no link to HBase. |
| `cassandra` | 6.0 | Simulation only; nothing on Cassandra 5 (SAI, Accord). |
| `dynamodb` | 8.0 | Best NoSQL page: moto-backed boto3 that actually runs. |
| `elasticsearch` | 6.5 | Good ES/OpenSearch framing; license table outdated. |
| `hbase` | 5.5 | Hadoop-era; duplicates Bigtable. |
| `mongodb` | 7.5 | mongomock pipelines run; no Atlas Search or Vector Search. |
| `redis` | 7.0 | Practical fakeredis recipes; no licensing or Valkey. |
| `aws` | 8.5 | Strongest cloud page; long; no IaC. |
| `azure` | 6.0 | Synapse-centric; Fabric barely mentioned; exercise numbering bug. |
| `gcp` | 8.0 | BigQuery internals, Beam watermarks; light on Dataplex and BigLake. |
| `databricks` | 8.5 | Current: serverless, Lakeflow, liquid clustering, Asset Bundles. |
| `looker` | 7.5 | Symmetric aggregates reproduced in DuckDB; no Looker vs Looker Studio note. |
| `superset` | 7.0 | Datasets, RLS, caching; thinnest BI page. |
| `tableau` | 8.0 | Grain-first approach, LOD vs SQL; best-organized BI page. |
| `docker` | 8.0 | Practical DE Dockerfiles and Compose; no multi-stage builds or uv. |
| `kubernetes` | 8.0 | Accurate and data-focused; no Kueue, Volcano or YuniKorn. |
| `change-data-capture` | 8.5 | Debezium, slot bloat, outbox, SCD2 from CDC; repetitive Q&A. |
| `cost-optimization` | 7.5 | Good numeric exercises; overlaps cost sections elsewhere. |
| `data-governance` | 8.0 | Broad: RBAC/ABAC, tags, GDPR; contracts repeated on other pages. |
| `data-modeling` | 8.0 | Clean Kimball, runnable SCD2; duplicates data-warehousing. |
| `data-observability` | 7.0 | Real OpenLineage code; overlaps data-quality. |
| `data-quality` | 7.5 | Runnable checks and GE; check the code against GX 1.x. |
| `data-structures` | 4.0 | Copied textbook trivia with typos; the useful DE tail is buried at the end. |
| `data-warehousing` | 7.5 | Medallion and SCD 3/6; same ground as data-modeling. |
| `statistics` | 6.5 | Competent A/B and percentiles material; better as an appendix. |
| `system-design` | 8.0 | Best synthesis page; four near-duplicate cost/failure sections. |
| `llm` | 7.0 | Offline RAG demo; little on the DE role (embedding pipelines, reindexing). |
