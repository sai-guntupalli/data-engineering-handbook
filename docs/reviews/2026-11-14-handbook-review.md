# Handbook review — 2026-11-14

A senior data engineer's review of the whole handbook: the `master` branch at `8a14ce2` (142 notebooks) and the live
site at <https://sai-guntupalli.github.io/data-engineering-handbook/>. It covers coverage, depth, grouping, notebook
standards, learning flow and a proposed redesign. It reviews the handbook as it is today and does not rely on the
earlier review (`docs/reviews/2026-11-09-site-review.md`), though it notes where that review's items are still open.

## Executive summary

**Overall: 6.5 / 10.** The handbook has two very different halves.

- **The rebuilt half is strong.** PySpark 1–14 and Data modeling 1–10 (24 lessons) are among the best free material
  on these subjects: one shared dataset per course, a short "where it matters / watch out for" frame per topic, an
  example whose output is shown, a "What to notice" note, then check yourself, key takeaways and a next link. The
  PySpark coding challenges, SQL 13 drills and the data-modeling drills have hidden solutions that CI verifies.
- **The other half has not been brought up to that bar.** 83 of 142 notebooks still teach with assertions (2,586
  `assert` lines in learner-facing cells). 50 still use the old 30-line `PACKAGES` setup cell. Only 27 notebooks have
  any "What to notice" note, 34 a "Check yourself" section, 26 key takeaways and 40 a "Next" link. Most tool pages
  (Kafka, Flink, BigQuery, Redshift, HBase, Bigtable, ...) are long interview FAQs with headings like "What is the
  meaning of broker in Apache Kafka?" rather than lessons.
- **Eight notebooks are stubs that are advertised as starting points.** `duckdb`, `postgres`, and six `concepts/`
  pages (`open-table-formats`, `lakehouse-catalogs`, `orchestration-patterns`, `semantic-layer`, `security-and-iam`,
  `cicd-and-iac`) are 150–220 words each, follow an identical template ("Decisions and trade-offs / Worked example /
  Practice"), and the site lists them as "About 1 min" lessons. The README calls them "new starting points".
- **Coverage is broad on tools but thin where it matters for the job.** Kafka, Airflow, dbt, Flink, Delta, Iceberg
  and Parquet each get one notebook, while BigQuery gets 49 sections and Snowflake 41. There is no single-node
  dataframe track (pandas, Polars, PyArrow), no ingestion track (APIs, files, Kafka Connect, Debezium as a tool,
  dlt/Airbyte), no stream-processing concepts notebook, no OLTP/database internals beyond a stub, no Git/shell, no
  hands-on data-quality tool, and no capstone outside PySpark.
- **The learning path covers 71 of 142 notebooks and teaches some prerequisites after they are used**: Delta Lake
  (stage 4) after the Delta-based data-modeling course (stage 3) and PySpark 10's Delta merges (stage 2); Kafka
  (stage 5) after PySpark 11 reads from Kafka (stage 2).

The top five actions, detailed in [Recommendations](#prioritized-recommendations):

1. Expand or unpublish the eight stub notebooks, and stop advertising them in the README.
2. Migrate the SQL course (16 notebooks) and the Python lessons (9) to the current standard; they are on the learning
   path's first stage and are the first thing a new reader sees.
3. Turn the core streaming and orchestration tools (Kafka, Airflow, dbt, Flink) into short courses with real
   execution where Colab allows, and rewrite tool FAQs into lessons.
4. Fix the learning path order (table formats before modeling, Kafka before Spark streaming) and put every
   notebook on a path or an explicit shelf.
5. Add a standards lint (warnings first) that measures the notebook structure, so migration is tracked by CI
   rather than by memory.

### Scorecard

| Dimension | Score | One-line reason |
|---|---:|---|
| Coverage (breadth) | 7 | 46 topics; missing single-node dataframes, ingestion, streaming concepts, OLTP, Git/shell, DQ tools |
| Depth per concept | 6 | PySpark and data modeling deep; most tools are one FAQ notebook; 8 stubs |
| Grouping | 6 | Categories mostly sensible; PostgreSQL in "NoSQL", dbt in "Orchestration", Concepts is a catch-all |
| Standards / consistency | 4 | 3 generations of notebook structure; only 24 lessons meet the documented standard |
| Flow | 5.5 | Strong inside PySpark and data modeling; path order inverts prerequisites; half the notebooks off-path |
| Site UI | 8 | Fast, calm reader; outputs shown; search works; mobile header still wraps; heavy pages |

## Method

- Created a worktree from `origin/master` (`8a14ce2`, "Merge pull request #92") and read `README.md`,
  `CONTRIBUTING.md`, `PROGRESS.md`, `PRODUCT.md`, `site/lib/tools.ts`, `site/lib/learning-map.ts`,
  `site/lib/retired.ts` and `scripts/`.
- Scripted an inventory of all 142 notebooks: folder, title, cell counts, setup-cell form, `##`/`###` headings,
  counts of `**What to notice**`, "where it matters", "watch out", Check yourself / Key takeaways / Next sections,
  `**Difficulty:**` lines, `solution`-tagged cells, and `assert` statements in non-solution code cells. The full
  table is in the [appendix](#appendix-notebook-inventory). Counts come from regexes over the notebook JSON, so a
  heading phrased differently (for example SQL's "Where you'll use it") is called out separately below.
- Ran `scripts/audit_notebooks.py --quiet`: it passes ("Audited 142 notebook(s): 7717 cells, 2189 code cells, 2592
  asserts"). The audit checks Colab-runnability, not teaching structure.
- Analysed links between notebooks (relative `.ipynb` links in markdown).
- Sample-read notebooks in every folder: Python 2, 3 and drills 2; Python challenges 1; Python coding problems; SQL
  0, 2, 5; PySpark 6, 12, drills 12; Data modeling 0, 3; Kafka; Airflow; LLM; interview question bank; data
  structures; DuckDB; semantic layer; open table formats, plus the `##` outline of every notebook.
- Walked the live site in a browser: home page and learning map, the Concepts tool page, DuckDB, PySpark 6 and SQL 2
  reader pages, search (`slowly changing`, `polars`), a retired-notebook redirect, and PySpark 6 at 375 px width.
  Fetched all 142 notebook pages from the sitemap and checked every one of their 324 distinct internal links.
- Not done: notebooks were not executed for this review (CI runs them on every change), and no notebook was opened
  in Colab.

## 1. Coverage

### What is well covered

| Area | Where | Comment |
|---|---|---|
| Distributed batch processing | `pyspark/` (16 lessons, 11 drills, 36 challenges, capstone, reference) | Complete for interview and job use, Spark 4 aware (Connect, VARIANT, Python Data Source API) |
| Dimensional modeling | `data-modeling/` (11 lessons, drills, reference) | Grain, SCD, chasm/fan traps, bridges, Data Vault, loading, physical design, tests |
| SQL | `sql/` (14 chapters, drills, concepts, reference) | Complete topic list, including time series, dedup, MERGE |
| Python | `python/learning` (9), `python/practice` (19) | Good DE angle in Python 9 (watermarks, upserts, retries, atomic writes) |
| Cloud warehouses | Snowflake, BigQuery, Redshift, ClickHouse, Databricks | Broad and current (Gen2, Cortex, Polaris, Lakeflow, zero-ETL) |
| Cloud platforms | AWS, GCP, Azure | Broad service maps including Fabric and S3 Tables |
| Governance, cost, CDC, quality, observability | `concepts/` | Long, mostly accurate FAQ notebooks |

### Missing or thin (by importance to a working data engineer)

| Severity | Gap | Evidence | What good looks like |
|---|---|---|---|
| High | **Single-node dataframes**: pandas, Polars, PyArrow, DuckDB's Python API | No tool folder; search for `polars` returns "0 notebooks and 0 sections match"; Polars is mentioned in 3 notebooks, `duckdb/duckdb.ipynb` is a stub | A 3–4 notebook track: pandas essentials and pitfalls, Polars lazy API, Arrow as the interchange format, DuckDB on Parquet; when to leave a laptop for Spark |
| High | **Ingestion** (batch extraction) | No notebook on extracting from REST APIs (pagination, rate limits, incremental cursors), files landing in object storage, JDBC incremental pulls, or ELT tools (Airbyte 0 mentions, Fivetran 1, dlt 1) | An "Ingestion patterns" track: API extraction with retries and cursors, file landing + manifest, JDBC incremental with high-water marks, managed ELT trade-offs, a real `dlt` pipeline into DuckDB |
| High | **Kafka as a course** | `kafka/kafka.ipynb` is one FAQ notebook with 6 code cells, all pure-Python models; Kafka Connect and Schema Registry appear only inside it and `avro` | 4–5 notebooks: log and partitions, producers (acks, idempotence, batching), consumers and groups, delivery semantics and transactions, Connect + Schema Registry + Debezium |
| High | **Stream-processing concepts** independent of an engine | Event time, watermarks, state, exactly-once are split between PySpark 11, `flink` and `kafka`, with Flink's FAQ repeating itself ("What are event time, processing time, and watermarks in Flink?" and later "What is a watermark?") | One concepts notebook (time, windows, watermarks, state, delivery guarantees, joins), then engines |
| High | **Orchestration in practice** | `airflow/airflow.ipynb` models Airflow with `graphlib.TopologicalSorter`; no real DAG is executed; Dagster and Prefect appear only as mentions; `concepts/orchestration-patterns` is a stub | Airflow 3 DAGs run with `dag.test()` in Colab (Airflow pip-installs), assets/data-aware scheduling, backfills; one comparison notebook with Dagster |
| High | **dbt depth** | One notebook (`dbt/dbt.ipynb`, 8 code cells) for the most-used transformation tool | 3–4 notebooks on dbt-duckdb: models and `ref`, tests and contracts, incremental and microbatch, snapshots, semantic layer/metrics |
| High | **OLTP databases** | `postgres/postgres.ipynb` is a 212-word stub; isolation levels appear in 4 notebooks; B-tree indexes in passing | Postgres as a source: indexes and plans, transactions and isolation anomalies, logical replication for CDC, bulk loading (`COPY`) |
| Medium | **Data quality tooling** | Concepts are covered; no hands-on Great Expectations (3 mentions), Soda (2) or pandera (0) | One notebook running pandera or GX against the shared dataset, contracts in dbt |
| Medium | **Lineage and catalogs** | OpenLineage 3 mentions, DataHub 1; `lakehouse-catalogs` is a stub | Lineage events from a pipeline, catalog concepts (Unity, Polaris, Glue) |
| Medium | **Git, shell, Linux** | 0 notebooks | A short "working environment" notebook: git branching and PRs for data code, shell text tools, cron, environment variables |
| Medium | **Infrastructure as code / CI for data** | `concepts/cicd-and-iac` is a stub; Terraform 4 mentions | Terraform for a bucket + warehouse, CI that runs dbt build and data diffs, blue/green and write-audit-publish |
| Medium | **Table format comparison and newer formats** | `concepts/open-table-formats` is a stub; Paimon mentioned twice; ORC has no home | A real comparison notebook (Delta vs Iceberg vs Hudi on the same table), with file formats (CSV, JSON, Avro, Parquet, ORC, Arrow) in one track |
| Medium | **Capstone projects** | Only `pyspark-concepts-end-to-end` | Two or three end-to-end builds: batch lakehouse (ingest → dbt → quality → BI), streaming (Kafka model → Spark → Delta), CDC (Postgres → Debezium model → SCD2) |
| Low | **LLM data engineering** | `llm/llm.ipynb` is terminology (transformers, tokenisation, decoding) with a numpy attention demo; vector databases mentioned once | Reframe around DE work: document ingestion and chunking, embedding pipelines, vector indexes (pgvector/LanceDB), evaluation data, PII in training data |
| Low | Alternative streaming platforms | Pulsar 1 mention, Redpanda 0, Kinesis/Pub/Sub only in cloud notebooks | A short section in the Kafka course on Kafka-compatible and cloud alternatives |

### Content that does not belong or is over-weighted

| Severity | Item | Evidence |
|---|---|---|
| Medium | `concepts/data-structures.ipynb` | 81 `##` sections of generic CS quiz questions ("We apply binary search algorithm to a sorted linked list why?", "Define a stack?"), with grammar errors such as "It must rich enough in structure..." (cell 5). 6,637 words, 697 KB page. Overlaps the nine Python challenge notebooks. |
| Low | `concepts/statistics.ipynb` | Useful but analyst-oriented; belongs in an appendix rather than "Data concepts" beside governance and CDC |
| Low | Six legacy tools at full length | Flume, Greenplum, Hadoop, HBase, Impala (each 5,700–8,700 words) — marked Legacy, which is good, but each is as long as Kafka's notebook |

## 2. Depth per topic

Rating: **A** deep and well taught, **B** good content with structure or example gaps, **C** broad but FAQ-style or
simulated, **D** thin or a stub.

| Topic | Rating | Notes and evidence |
|---|---|---|
| PySpark 1–14 | A | 9–14 "What to notice" notes per lesson, outputs shown, plans read (`explain("formatted")`), Spark 4 features. Gaps: PySpark 12 has only 2 What-to-notice notes across 9 topics and PySpark 13 has 3 across 11, so the internals and tuning lessons rely on prose more than shown evidence. |
| PySpark drills, challenges, capstone | A– | 36 challenges with tagged solutions and CI-verified outputs. `pyspark-drills-12-execution-and-production` has no `**Difficulty:**` lines and no Next link (every other PySpark drill has 4–5 and a Next). |
| PySpark 15, reference | B | Markdown only (0 code cells), which suits interview concepts and a reference card. |
| Data modeling 1–10, drills, reference | A | Same standard as PySpark; Delta does real merges, constraints, time travel. `data-modeling-reference` has no Next link. |
| SQL 1–12 | B | Thorough topic coverage, a shared dataset, "Where you'll use it" notes. But every example asserts its result (SQL 1 has 54 asserts) and often runs the query twice (SQL 2 cell 9: `.show()` then `assert spark.sql(q).collect() == [...]`). Practice answers are visible directly under the questions. SQL 11 re-teaches grain, star schema and SCD2, now covered properly by Data modeling 1–3. |
| SQL 13, 14, reference | B+ | SQL 13 has 22 drills with tagged solutions. SQL 14 and the reference overlap the interview question bank. |
| Python 1–9 | B | Good explanations and DE examples, but taught entirely through asserts (Python 2 has 112), answers visible, no Next links, and the lessons never link to their drills (the drills link back). |
| Python drills, challenges | B+ | Difficulty lines on every exercise; solutions hidden in markdown `<details>` instead of `solution`-tagged cells (see Standards). |
| Python coding problems | B– | 14 rich problems and 12,721 words, but 0 code cells: the reader cannot attempt a problem in the notebook, and there are no Difficulty lines. |
| Interview question bank | B | Good model answers; 73 asserts; repeats SQL 14 and PySpark 15. |
| Snowflake, BigQuery, Redshift, ClickHouse, Databricks | B/C | Current and broad. BigQuery (49 sections) and Redshift (38) are FAQ-ordered ("What is the difference between VACUUM and ANALYZE commands in Redshift?"). Runnable cells are DuckDB stand-ins or arithmetic with asserts. |
| AWS, GCP, Azure | B | Good mental-model framing and current services. Very long (8,500–10,000 words each), no exercises with solutions. |
| Kafka, Flink, Airflow | C | Accurate and current, but FAQ-ordered and simulated. Kafka opens with "What is the traditional method of transferring messages?"; Flink repeats topics (see Coverage). Airflow is one of the better-written tool pages but runs no Airflow code. |
| dbt | C+ | One notebook covering 27 FAQ questions; the dbt-duckdb build is the right direction but deserves a course. |
| Delta, Iceberg, Hudi, Parquet, Avro | B/C | Real libraries (`deltalake`, `pyiceberg`, PyArrow) in places, but FAQ headings ("What is Apache Iceberg?") and 40–50 asserts each. Delta’s second section is "How do you create a Delta table in Databricks Unity Catalog with PySpark?", which cannot run locally. |
| Cassandra, HBase, Bigtable, DynamoDB, MongoDB, Redis, Elasticsearch | B/C | Real stand-ins where available (`mongomock`, `fakeredis`, `moto`); otherwise models. FAQ structure; DynamoDB and Redis are the strongest. |
| Docker, Kubernetes | B | Topic-ordered (not FAQ), practical; no Docker "Last reviewed" line. |
| Looker, Superset, Tableau | B | Topic-ordered with practice scenarios; Superset and Tableau have no "Last reviewed" line. |
| Scala | C | One notebook, 6 code cells for a language; Scala cannot run in this Python kernel, so most code is in markdown. |
| Concepts: CDC, governance, cost, quality, observability, system design | B | Long FAQs with good real-world sections; assert-based examples; no Next links. |
| Concepts: 6 new pages, DuckDB, PostgreSQL | **D** | 150–220 words, one code cell of asserts, a generic "Practice" prompt ("Add a failure case, explain the expected outcome before running it..."). `duckdb` and `semantic-layer` install `dbt-core` and `dbt-duckdb` without using them. |
| LLM | C | Terminology, not data engineering (see Coverage). |
| Data structures | D | See Coverage. |

## 3. Grouping

### Tool categories (`site/lib/tools.ts`)

| Severity | Finding | Evidence | Suggestion |
|---|---|---|---|
| Medium | **PostgreSQL is filed under "NoSQL and search"** | `{ folder: "postgres", ... category: "databases" }`; the `databases` category label is "NoSQL and search"; home page lists PostgreSQL between MongoDB and Redis | Rename the category "Databases (OLTP, NoSQL and search)" or add an "Operational databases" category |
| Medium | **dbt is filed under "Orchestration"** | `category: "orchestration"` beside Airflow | Add "Transformation" (dbt, later SQLMesh) or rename to "Orchestration and transformation" |
| Medium | **"Concepts" is a catch-all** | Holds data concepts (14), data modeling (13) and LLMs (1); "Data concepts" itself mixes architecture (system design), process (governance), statistics and CS quiz material | Split into "Architecture and design", "Quality, governance and operations"; move statistics and data structures to an appendix |
| Low | **Practice lives in two places** | "Interview prep" holds one notebook; Python, SQL, PySpark and data-modeling drills live in their tool folders. The Python topic shows 28 notebooks, 19 of them practice | Fine to keep drills next to lessons, but make the Interview prep page an index of all practice |
| Low | Streaming engines split | Flink is a "Processing engine", Kafka "Streaming and ingestion", Spark streaming inside PySpark | Acceptable; a streaming concepts page would tie them together |
| Low | Hive under "Processing engines", Hudi/Iceberg/Delta under "File and table formats" | Hive is partly a metastore/catalog topic | Mention the metastore under a catalogs topic |

### Learning-map stages (`site/lib/learning-map.ts`)

The six stages (Foundations, Process at scale, Model and test, Store, Orchestrate and stream, Interview practice) are
meaningful as a story, but:

| Severity | Finding | Evidence |
|---|---|---|
| High | **Prerequisites taught after use** | Stage 3 `data-modeling-*` runs on `delta-spark` and Stage 2 `pyspark-10-batch-pipelines` has "Merge into a Delta table, version by version", but Delta Lake is Stage 4. Stage 2 `pyspark-11-structured-streaming` has "Read from Kafka", but Kafka is Stage 5. `pyspark-04` teaches Parquet before Stage 4's Parquet notebook. |
| High | **Half the handbook is off-path** | 71 of 142 notebooks are on the path. Not on it: all PySpark drills (11) and coding challenges, data-modeling drills and reference, Python challenges (9) and coding problems, SQL reference, every warehouse, cloud, NoSQL, BI and infrastructure notebook, and 12 of 14 concepts. |
| Medium | **A capstone is filed as "Question bank"** | The "Question bank" step is `["interview-question-bank", "pyspark-concepts-end-to-end"]`; the README calls the latter the batch-pipeline capstone, and `tools.ts` overrides its category to `"reference"`. |
| Medium | **Lesson-path step includes interview material** | `pyspark-15-interview-concepts` is the last step of "Process at scale", while SQL's interview concepts sit in the Interview practice stage. |
| Low | Missing stages | No stage for ingestion, cloud/warehouse platforms, or quality/operations beyond two notebooks. |
| Low | Two entry points | The home hero offers "Start the SQL path" and "Start the Python path"; the map's "Start here" card is Python 1, while SQL has a "start here" notebook and Python does not. |

## 4. Standards

CONTRIBUTING.md defines the standard: two-line setup cell; short setup and sample data; topic sections; examples
that show output with a `**What to notice:**` note and no learner-facing asserts; hidden `solution`-tagged answers;
`**Difficulty:**` under each exercise; "Last reviewed" on tool pages. The PySpark and data-modeling lessons add
"where it matters / watch out for", Check yourself, Key takeaways and a Next link.

### Generations of notebook structure

| Generation | Notebooks | Setup | Teaching | Practice | Ending |
|---|---|---|---|---|---|
| **Current standard** | PySpark 1–14, Data modeling 1–10 (24) | two-line | output + What to notice; where it matters / watch out | Check yourself; drills with tagged solutions | Key takeaways, Next |
| **Practice, current** | PySpark drills (11), PySpark challenges, data-modeling drills, SQL 13 | two-line (SQL 13: long) | — | Difficulty + tagged solutions | Next on most |
| **Practice, older** | Python drills (9), Python challenges (9) | none (stdlib) | — | Difficulty + `<details>` markdown solutions | none |
| **Lesson, older** | SQL 1–12, 14, reference; Python 1–9 | long (SQL) / none (Python) | asserts; "Where you'll use it" | visible "Practice questions / Answers" | Interview notes; no Next |
| **Tool / concept pages** (FAQ-style in most; Docker, Kubernetes and BI are topic-ordered) | 37 tool and 8 concept notebooks | long (25) / none (stdlib) | FAQ headings; asserts; "Where you'll use it" in some | "<Tool> exercises" or "Practice scenarios" | none |
| **Stub template** | 6 concepts, `duckdb`, `postgres` | long | one assert cell | generic prompt | none |

### Deviations, by rule

| Rule | Severity | Deviating notebooks |
|---|---|---|
| **Two-line setup cell** | Medium | 50 notebooks still use the long `PACKAGES` cell: all of `sql/` except SQL 0 (16), `avro`, `aws`, `azure`, `bigquery`, `clickhouse`, `databricks`, `dbt`, `delta`, `docker`, `duckdb`, `dynamodb`, `gcp`, `greenplum`, `hive`, `iceberg`, `impala`, `kubernetes`, `llm`, `looker`, `mongodb`, `parquet`, `postgres`, `redis`, `redshift`, `snowflake`, `superset`, `tableau`, `trino`, and concepts `change-data-capture`, `cost-optimization`, `data-governance`, `data-observability`, `data-quality`, `semantic-layer`, `statistics`. (52 notebooks have no setup cell; that is correct for stdlib-only and markdown-only notebooks.) |
| **No learner-facing asserts** | High | 83 notebooks, 2,586 asserts. Largest: Python 2 (112), Python 1 (78), Python 5 (75), interview question bank (73), Python 3 (67), data structures (65), Elasticsearch (56), statistics (55), SQL 1 (54), Redis (52), Parquet (50). SQL 0 still tells readers "every result is asserted, so a wrong answer fails loudly". The site labels these cells "checked example". |
| **What to notice after examples** | High | Present in only 27 notebooks (the 24 current-standard lessons, PySpark 0, capstone, data-modeling 0). Thin within the standard: PySpark 12 (2 notes / 9 topics), PySpark 13 (3 / 11). |
| **Where it matters / Watch out for** | Medium | Only the 24 current-standard lessons. 32 older notebooks use "Where you'll use it" (SQL, Python, Kafka, Airflow, ...), which covers the first half; none of them has "watch out for". Snowflake uses "watch out" 38 times in its own format. |
| **Check yourself** | Medium | Missing from all SQL, Python, tool notebooks except Airflow, Kafka, dbt, Redis, and concepts CDC, observability, quality, system design, data structures. |
| **Key takeaways** | Medium | Only in the 24 current-standard lessons plus PySpark 15 and the capstone. |
| **Next link** | Medium | 40 notebooks have one. Missing from every Python lesson, every SQL chapter except SQL 8, every tool and concept notebook except Kafka, `data-modeling-reference`, `pyspark-drills-12`. The site pager compensates, but 68 notebooks have no in-text link to any other notebook, and 53 are never linked from another notebook (including all nine Python drills: lessons never point to them). |
| **Hidden solutions as `solution`-tagged cells** | Medium | Python drills (9) and challenges (9) and `python-coding-problems` hide answers in markdown `<details>` blocks, so the answers cannot be run, the site's solution panel and `verify_challenge_answers.py` do not see them, and Python practice is verified by a separate script (`verify_practice_answers.py`). SQL 1–12 and Python 1–9 print answers openly under "Answers". |
| **Difficulty lines** | Low | `pyspark-drills-12-execution-and-production` (0 of 6 exercises), `python-coding-problems` (0 of 14 problems), SQL 1–12 practice questions. |
| **Exercise cells** | Medium | `python-coding-problems` has 0 code cells: no place to attempt the 14 problems. |
| **Last reviewed line on tool pages** | Low | Missing on `docker`, `flume`, `hadoop`, `impala`, `llm`, `postgres`, `duckdb`, `scala`, `superset`, `tableau`, and all concepts. |
| **Lean, topic-ordered headings** | Medium | FAQ headings in most tool notebooks; some have 30–49 `##` sections (BigQuery 49, Flink 47, Snowflake 41, Redshift 38, AWS 36, Kafka 33). `data-structures` has 81. |
| **Sample data cell after setup** | Low | Older notebooks create data inline per example; the newer standard has one "Setup and sample data" section. |

### Documentation and tooling drift

| Severity | File | Problem |
|---|---|---|
| Medium | `README.md` line 99 | "103 notebooks in total"; there are 142. |
| Medium | `README.md` lines 64–67 | "The eight modules teach the individual concepts" — PySpark now has 16 lessons. |
| Low | `README.md` line 61 | `.venv/bin/python scripts/verify_practice_answers.py`; elsewhere it uses `uv run --extra notebooks python`. |
| Medium | `README.md` lines 13–16 | Advertises the eight stubs as "New starting points". |
| Medium | `CONTRIBUTING.md` commit checklist | "New packages are in both the notebook's `PACKAGES`..." (old setup form) and "New notebooks are listed in `site/lib/notebook-groups.ts`" — that file does not exist. |
| Low | `scripts/audit_notebooks.py` docstring | Says the setup cell "assigns `PACKAGES = {...}`"; the two-line form is the documented standard. |
| Low | `PRODUCT.md` | Still describes a stateless site (PROGRESS.md "Next Steps" item 8 notes this). |
| Medium | Audit coverage | The audit passes with 2,592 asserts and none of the teaching structure; nothing in CI measures the standard. |

## 5. Flow

### Within notebooks

- **PySpark and data modeling**: good. Each lesson states prerequisites, builds on one dataset, and ends with
  drills and the next lesson. PySpark 6 ends "Practise this module in PySpark drills 6: joins, then continue with
  PySpark 7"; the site's pager, however, goes straight to PySpark 7 because drills are not on the path (minor
  mismatch).
- **SQL**: SQL 1 still previews joins, CASE and NULL (sections 9–11) before chapters 2–4 teach them; SQL 0's table
  says so explicitly. SQL 11 duplicates Data modeling 1–3 and should become a short bridge to that course.
- **Tool FAQs**: question order is arbitrary. Kafka puts "What is the maximum size of a message" (§5) before
  partitions and offsets; Flink asks "What is Flink and how is a job structured?" third, after event time and
  watermarks; BigQuery explains storage and processing (§4) after cost control (§3).
- **Stubs**: no flow; a single assert cell.

### Across the handbook

| Severity | Finding | Evidence |
|---|---|---|
| High | Table formats after their use | See Grouping: Delta in stage 4, used in stages 2 and 3 |
| High | Kafka after Spark's Kafka source | Stage 5 vs PySpark 11 in stage 2 |
| Medium | Repetition of SCD Type 2 | Search for "slowly changing" returns DM 3, PySpark 10 "Keep history with a slowly changing dimension", SQL 11 §3, PySpark challenge 33, data-quality's real-world case, dbt snapshots. DM 3 should be canonical; others should link to it. |
| Medium | Repetition of interview concepts | SQL 14, PySpark 15, the interview question bank and the SQL reference overlap. |
| Medium | Python lessons do not lead to drills | The drills link back to lessons; no lesson links forward. |
| Low | Concepts have no reading order | The Concepts tool page sorts alphabetically: CDC, CI/CD (1 min), cost, governance, observability, quality, data structures (57 min), ... |

## 6. Site UI findings

| Severity | Finding | Evidence |
|---|---|---|
| Medium | Stubs presented as lessons | `/tools/concepts/` lists six pages as "Lesson · 3 sections · 1 min" beside 30-minute lessons; no "draft" marker |
| Medium | Mobile header wraps to two rows with a gap | `/notebooks/pyspark-06-joins/` at 375×812: row 1 logo + Library + Starred, row 2 search/theme/GitHub icons, then about 90 px of empty space above the title. No horizontal scroll (`scrollWidth` = 375). The 2026-11-09 review marked "compact mobile top bar" as done; it still wraps. |
| Medium | Page weight | Average notebook page 322 KB of HTML; largest `pyspark-coding-challenges` 959 KB, `snowflake` 765 KB, `data-structures` 697 KB, `interview-question-bank` 685 KB, `elasticsearch` 643 KB, `bigquery` 576 KB |
| Low | "checked example" label rewards asserts | SQL 2 shows 48 "checked example" labels; under the new standard these should be plain examples with output |
| Low | Pager skips drills | PySpark 6 pager: "Next on the learning path: PySpark 7" while the text says do drills 6 first |
| OK | Links | All 142 notebook pages return 200; all 324 distinct internal links resolve (one transient 503 on `/files/redshift.ipynb` returned 200 on retry). The retired URL `/notebooks/data-modeling/` serves the "Moved" page. |
| OK | Outputs | Executed outputs render under cells (SQL 2: 18 output blocks; DuckDB stub shows `[(1, 30), (2, 5)]`) |
| OK | Search | `slowly changing` returns 1 notebook and 17 sections with good snippets |

## Prioritized recommendations

**P0 — this week (credibility)**

1. **Stubs**: expand the eight stubs to the current standard, or hide them (remove from the README and mark them
   "Draft" on tool pages) until they are. Start with DuckDB and PostgreSQL, which the redesign depends on.
2. **Docs drift**: fix README counts and the PySpark "eight modules" text; fix the CONTRIBUTING checklist
   (`PACKAGES`, `notebook-groups.ts`); update the audit docstring and SQL 0's "every result is asserted".
3. **Categories**: move PostgreSQL out of "NoSQL and search"; give dbt a "Transformation" home.

**P1 — next (the learning path's first stages)**

4. **SQL course migration** (16 notebooks): two-line setup, one "Setup and sample data" section, output instead of
   asserts, What to notice, where it matters / watch out for, Check yourself, Key takeaways, Next; move answers to
   tagged solutions; cut SQL 1's previews; turn SQL 11 into a bridge to Data modeling.
5. **Python lessons migration** (9): same structure; link each lesson to its drill.
6. **Python practice**: convert `<details>` answers to `solution`-tagged cells so one verifier and one reader panel
   cover all practice; add exercise cells and Difficulty lines to `python-coding-problems`.
7. **Learning path**: move "Store" (Parquet, Delta, Iceberg) before "Model and test" or add a short "table formats"
   prerequisite step; put Kafka before PySpark 11 or add a Kafka primer to PySpark 11; add drills and the capstone as
   path steps; move PySpark 15 to Interview practice; add a shelf for everything else so no notebook is orphaned.
8. **Standards lint**: add an audit mode that reports per-notebook structure (the appendix's columns) as warnings,
   with an allow-list that shrinks as notebooks migrate.

**P2 — content depth**

9. Core tools as short courses with real execution: Kafka (4–5), Airflow (3, real `dag.test()`), dbt (3–4,
   dbt-duckdb), Flink/stream concepts (2–3). Then table-format comparison on one dataset.
10. New tracks: single-node dataframes (pandas, Polars, Arrow, DuckDB), ingestion patterns, OLTP/Postgres, data
    quality tooling, Git/shell, IaC/CI.
11. Rewrite tool FAQs into topic-ordered lessons with a fixed template (see redesign); cap at about 12 sections;
    move pure interview Q&A into the question bank.
12. Cut `data-structures` to a DE-focused page (hashing, heaps, sorting, bloom filters, HyperLogLog) or move it to the
    appendix; move `statistics` to an appendix; reframe `llm` around data work.
13. Finish PySpark 12/13 What-to-notice notes and `pyspark-drills-12` Difficulty lines and Next link.

**P3 — polish**

14. Mobile header to one row; reduce page payload (content ships twice).
15. "Last reviewed" on the remaining tool pages; a Draft/Legacy badge in search results.
16. Capstones: batch lakehouse, streaming, CDC.

## Proposed redesign

If I built the handbook from scratch, I would organise it as **tracks of short lessons, each paired with practice**,
with tools taught inside the track where they are used, and a shared fictional business (the data-modeling shop)
across all tracks so later notebooks reuse earlier tables.

### Principles

- **One notebook = one lesson of 20–30 minutes**, 6–12 topics, current template. A tool that matters gets a course,
  not a 10,000-word FAQ.
- **Every lesson has a paired drill notebook**; interview questions live in one bank per track, not in lessons.
- **Run the real thing where Colab allows** (Spark, Delta, Iceberg, DuckDB, dbt-duckdb, Airflow `dag.test()`,
  an embedded Postgres package where one runs in Colab, `dlt`, pandera); label models clearly.
- **One shared dataset** (shop: customers, orders, lines, payments, events, CRM change log) seeded by a tiny
  importable script, so setup stays two cells.
- **Shelves**: Path (ordered), Reference (cards), Practice (drills, challenges, interview bank), Platforms (vendor
  pages using one template), Legacy, Appendix.

### Lesson template

```text
# <Track> <N>: <subject>
Intro: the problem in one paragraph · Prerequisites · Last reviewed (tools)
## Setup and sample data         (two-line install + one cell)
## <Topic>                        x 6-12
   explanation · Where it matters · Watch out for
   example (shows output) · **What to notice:**
## Check yourself                 (3-5 questions, answers collapsed)
## Key takeaways
**Next:** drill N, then lesson N+1
```

Platform pages (warehouses, clouds) use a fixed outline: architecture → storage and layout → loading → compute and
cost → performance tuning → security → when not to use it → migration notes → practice scenarios.

### Outline

| # | Track | Notebooks (lessons; each with a drill) | Source today |
|---|---|---|---|
| 0 | **Start here** | How the handbook works and how to run notebooks; the shop dataset; the learning map | SQL 0, PySpark 0, DM 0 merged |
| 1 | **Working environment** | 1 Shell and files · 2 Git for data code · 3 Python packaging, venvs, uv | new |
| 2 | **Python for data engineering** | 1 Values and types · 2 Collections · 3 Functions · 4 Iterators/generators · 5 Classes and dataclasses · 6 Files and formats · 7 Errors, logging, testing (pytest) · 8 Concurrency · 9 DE patterns | `python/learning` migrated |
| 3 | **SQL** | 1 Select and filter · 2 Aggregation · 3 Joins · 4 NULLs · 5 CASE and pivots · 6 Subqueries and CTEs · 7 Set operations · 8 Types, dates, JSON · 9 Windows · 10 Dedup and top-N · 11 Time series · 12 DML and MERGE · 13 Query plans and indexes (dialect notes in every chapter; DuckDB engine, Spark SQL notes) | `sql/` migrated; SQL 11 modeling part moved to track 5 |
| 4 | **Data on one machine** | 1 pandas essentials and traps · 2 Polars (lazy, expressions) · 3 Arrow and Parquet with PyArrow · 4 DuckDB for pipelines · 5 When to move to Spark | new + `duckdb`, `parquet` |
| 5 | **Storage** | 1 OLTP with Postgres (indexes, transactions, isolation) · 2 File formats (CSV, JSON, Avro, Parquet, ORC) · 3 Object storage and layout · 4 Delta Lake · 5 Iceberg · 6 Hudi and Paimon · 7 Table format comparison · 8 Catalogs (Hive metastore, Glue, Unity, Polaris) | `postgres`, `avro`, `parquet`, `delta`, `iceberg`, `hudi`, stubs |
| 6 | **Data modeling** | current DM 1–10 unchanged | `data-modeling/` |
| 7 | **Distributed processing with Spark** | current PySpark 1–14 (Delta now taught in track 5 first) | `pyspark/` |
| 8 | **Ingestion** | 1 Batch ingestion patterns (full, incremental, high-water marks) · 2 APIs (pagination, rate limits, retries) · 3 Files and object-store landing · 4 CDC concepts and Debezium · 5 Managed ELT and `dlt` | new + `change-data-capture` |
| 9 | **Streaming** | 1 Stream concepts (time, windows, watermarks, state, guarantees) · 2 Kafka log and partitions · 3 Producers · 4 Consumers and groups · 5 Transactions and exactly-once · 6 Connect and Schema Registry · 7 Spark Structured Streaming (PySpark 11) · 8 Flink | `kafka`, `flink`, `avro`, PySpark 11 |
| 10 | **Transformation** | 1 dbt models and `ref` · 2 Tests and contracts · 3 Incremental and microbatch · 4 Snapshots · 5 Semantic layer and metrics | `dbt`, `semantic-layer` |
| 11 | **Orchestration** | 1 Scheduling concepts (intervals, idempotency, backfills) · 2 Airflow 3 DAGs (`dag.test()`) · 3 Assets and data-aware scheduling · 4 Orchestration patterns and alternatives (Dagster, Prefect) | `airflow`, `orchestration-patterns` |
| 12 | **Quality, observability and governance** | 1 Data quality checks (pandera/GX) · 2 Contracts · 3 Observability and SLAs · 4 Lineage (OpenLineage) · 5 Governance and catalogs · 6 Security, IAM and privacy | `concepts/` quality, observability, governance, security |
| 13 | **Platforms** | Warehouses: Snowflake, BigQuery, Redshift, ClickHouse, Databricks · Clouds: AWS, GCP, Azure · Serving stores: DynamoDB, MongoDB, Cassandra, Redis, Elasticsearch, Bigtable · BI: Looker, Superset, Tableau (platform template) | existing tool pages rewritten |
| 14 | **Infrastructure and delivery** | 1 Docker · 2 Kubernetes for data jobs · 3 Terraform basics · 4 CI/CD for data (write-audit-publish, data diffs) | `docker`, `kubernetes`, `cicd-and-iac` |
| 15 | **Architecture** | 1 Lakehouse and medallion · 2 Batch vs streaming design · 3 Cost and FinOps · 4 System design method + 6 cases | `system-design`, `cost-optimization`, DM 6 |
| 16 | **Capstones** | 1 Batch lakehouse (ingest → Delta → dbt → quality → BI extract) · 2 Streaming orders (Kafka model → Spark → Delta) · 3 CDC to SCD2 (Postgres → change log → DM 3 patterns) | `pyspark-concepts-end-to-end` + new |
| 17 | **Interview practice** | Python, SQL, PySpark, modeling drills and challenges; one question bank per track; system design cases; a mock-interview plan | existing practice notebooks |
| 18 | **AI data engineering** | 1 LLM vocabulary for data engineers · 2 Document ingestion and chunking · 3 Embedding pipelines and vector indexes · 4 Evaluation datasets and PII | `llm` reframed |
| — | **Legacy shelf** | Hadoop, Hive, HBase, Impala, Flume, Greenplum, NiFi — each cut to "what it is, what replaced it, what you will meet in old estates" (about 2,000 words) | existing |
| — | **Appendix** | Data structures for DE, statistics for DE, Scala for Spark readers | `data-structures`, `statistics`, `scala` |

**Learning path** (the home map): Start here → Working environment → Python → SQL → Data on one machine → Storage →
Data modeling → Spark → Ingestion → Streaming → Transformation → Orchestration → Quality and governance → Capstone 1
→ Interview practice. Platforms, Infrastructure, Architecture, AI and Legacy are shelves the reader dips into.

**Folder layout**: `notebooks/<track>/<track>-NN-<subject>.ipynb` with `notebooks/<track>/practice/` for drills, so
the folder is the track, not the tool. Tools that span tracks (Kafka, Delta) are found through tool tags and search,
which `tools.ts` can keep as metadata rather than folders.

### Migration order

1. Lint + docs drift + categories (P0) — a day.
2. SQL and Python migrations — the first two path stages.
3. Storage track (Delta/Iceberg/Parquet rewritten, Postgres and table-format comparison) so modeling and Spark
   build on it.
4. Streaming, transformation and orchestration courses.
5. Single-node and ingestion tracks; quality tooling; capstones.
6. Platform-template rewrites and the Legacy shelf trim; appendix moves.

## Appendix: notebook inventory

Columns: code cells; setup form (`two-line`, `long` = `PACKAGES` cell, `none` = no install cell); number of `##`
sections; `**What to notice**` notes; Check yourself / Key takeaways / Next present; `**Difficulty:**` lines;
`solution`-tagged cells; `assert` lines in non-solution code cells; markdown words. Python practice hides answers in
markdown `<details>`, so its tagged-solution count is 0 by design.

| Folder | Notebook | Code cells | Setup | `##` | What to notice | Check yourself | Takeaways | Next | Difficulty | Tagged solutions | Learner asserts | Words |
|---|---|---:|---|---:|---:|:-:|:-:|:-:|---:|---:|---:|---:|
| airflow | `airflow` | 8 | none | 30 | 0 | ✓ | – | – | 0 | 0 | 17 | 9537 |
| avro | `avro` | 20 | long | 22 | 0 | – | – | – | 0 | 0 | 44 | 4703 |
| aws | `aws` | 17 | long | 36 | 0 | – | – | – | 0 | 0 | 37 | 8561 |
| azure | `azure` | 12 | long | 24 | 0 | – | – | – | 0 | 0 | 40 | 10096 |
| bigquery | `bigquery` | 14 | long | 49 | 0 | – | – | – | 0 | 0 | 25 | 12890 |
| bigtable | `bigtable` | 14 | none | 32 | 0 | – | – | – | 0 | 0 | 43 | 7428 |
| cassandra | `cassandra` | 13 | none | 28 | 0 | – | – | – | 0 | 0 | 37 | 7965 |
| clickhouse | `clickhouse` | 15 | long | 25 | 0 | – | – | – | 0 | 0 | 33 | 6971 |
| concepts | `change-data-capture` | 7 | long | 24 | 0 | ✓ | – | – | 0 | 0 | 11 | 5659 |
| concepts | `cicd-and-iac` | 1 | none | 3 | 0 | – | – | – | 0 | 0 | 3 | 173 |
| concepts | `cost-optimization` | 19 | long | 20 | 0 | – | – | – | 0 | 0 | 39 | 6322 |
| concepts | `data-governance` | 14 | long | 23 | 0 | – | – | – | 0 | 0 | 34 | 4296 |
| concepts | `data-observability` | 8 | long | 14 | 0 | ✓ | – | – | 0 | 0 | 12 | 3568 |
| concepts | `data-quality` | 14 | long | 17 | 0 | ✓ | – | – | 0 | 0 | 25 | 3825 |
| concepts | `data-structures` | 58 | none | 81 | 0 | ✓ | – | – | 0 | 0 | 65 | 6637 |
| concepts | `lakehouse-catalogs` | 1 | none | 3 | 0 | – | – | – | 0 | 0 | 1 | 175 |
| concepts | `open-table-formats` | 1 | none | 3 | 0 | – | – | – | 0 | 0 | 2 | 219 |
| concepts | `orchestration-patterns` | 1 | none | 3 | 0 | – | – | – | 0 | 0 | 1 | 162 |
| concepts | `security-and-iam` | 1 | none | 3 | 0 | – | – | – | 0 | 0 | 3 | 168 |
| concepts | `semantic-layer` | 2 | long | 3 | 0 | – | – | – | 0 | 0 | 2 | 165 |
| concepts | `statistics` | 27 | long | 11 | 0 | – | – | – | 0 | 0 | 55 | 2466 |
| concepts | `system-design` | 22 | none | 15 | 0 | ✓ | – | – | 0 | 0 | 37 | 7736 |
| data-modeling | `data-modeling-00-start-here` | 6 | two-line | 6 | 2 | – | – | – | 0 | 0 | 0 | 1233 |
| data-modeling | `data-modeling-01-grain-facts-and-dimensions` | 15 | two-line | 9 | 7 | ✓ | ✓ | ✓ | 0 | 0 | 1 | 2657 |
| data-modeling | `data-modeling-02-star-schema-design` | 13 | two-line | 10 | 7 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2624 |
| data-modeling | `data-modeling-03-slowly-changing-dimensions` | 17 | two-line | 11 | 8 | ✓ | ✓ | ✓ | 0 | 0 | 1 | 3089 |
| data-modeling | `data-modeling-04-relationships-and-double-counting` | 13 | two-line | 8 | 6 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2118 |
| data-modeling | `data-modeling-05-normalized-and-operational-models` | 11 | two-line | 9 | 4 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2214 |
| data-modeling | `data-modeling-06-warehouse-architectures` | 8 | two-line | 10 | 4 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2269 |
| data-modeling | `data-modeling-07-loading-and-late-data` | 12 | two-line | 10 | 6 | ✓ | ✓ | ✓ | 0 | 0 | 1 | 2601 |
| data-modeling | `data-modeling-08-physical-design-and-performance` | 9 | two-line | 11 | 5 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2719 |
| data-modeling | `data-modeling-09-testing-metrics-and-change` | 15 | two-line | 9 | 6 | ✓ | ✓ | ✓ | 0 | 0 | 2 | 2366 |
| data-modeling | `data-modeling-10-interview-case-studies` | 7 | two-line | 9 | 4 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2493 |
| data-modeling | `data-modeling-drills` | 20 | two-line | 9 | 0 | – | – | ✓ | 8 | 8 | 0 | 1697 |
| data-modeling | `data-modeling-reference` | 16 | two-line | 7 | 0 | – | – | – | 0 | 0 | 0 | 1886 |
| databricks | `databricks` | 19 | long | 28 | 0 | – | – | – | 0 | 0 | 42 | 6463 |
| dbt | `dbt` | 8 | long | 27 | 0 | ✓ | – | – | 0 | 0 | 17 | 4998 |
| delta | `delta` | 20 | long | 13 | 0 | – | – | – | 0 | 0 | 46 | 5042 |
| docker | `docker` | 7 | long | 15 | 0 | – | – | – | 0 | 0 | 13 | 2365 |
| duckdb | `duckdb` | 2 | long | 3 | 0 | – | – | – | 0 | 0 | 1 | 147 |
| dynamodb | `dynamodb` | 30 | long | 18 | 0 | – | – | – | 0 | 0 | 46 | 6392 |
| elasticsearch | `elasticsearch` | 18 | none | 27 | 0 | – | – | – | 0 | 0 | 56 | 6586 |
| flink | `flink` | 13 | none | 47 | 0 | – | – | – | 0 | 0 | 27 | 8631 |
| flume | `flume` | 12 | none | 8 | 0 | – | – | – | 0 | 0 | 29 | 5749 |
| gcp | `gcp` | 14 | long | 34 | 0 | – | – | – | 0 | 0 | 35 | 9176 |
| greenplum | `greenplum` | 12 | long | 12 | 0 | – | – | – | 0 | 0 | 33 | 7349 |
| hadoop | `hadoop` | 13 | none | 8 | 0 | – | – | – | 0 | 0 | 39 | 6175 |
| hbase | `hbase` | 10 | none | 27 | 0 | – | – | – | 0 | 0 | 41 | 8740 |
| hive | `hive` | 15 | long | 9 | 0 | – | – | – | 0 | 0 | 37 | 7842 |
| hudi | `hudi` | 16 | none | 22 | 0 | – | – | – | 0 | 0 | 38 | 5657 |
| iceberg | `iceberg` | 22 | long | 28 | 0 | – | – | – | 0 | 0 | 40 | 5587 |
| impala | `impala` | 14 | long | 9 | 0 | – | – | – | 0 | 0 | 32 | 6980 |
| interview-questions | `interview-question-bank` | 59 | none | 10 | 0 | – | – | – | 0 | 0 | 73 | 10814 |
| kafka | `kafka` | 6 | none | 33 | 0 | ✓ | – | ✓ | 0 | 0 | 11 | 5606 |
| kubernetes | `kubernetes` | 9 | long | 17 | 0 | – | – | – | 0 | 0 | 18 | 3856 |
| llm | `llm` | 15 | long | 9 | 0 | – | – | – | 0 | 0 | 38 | 3204 |
| looker | `looker` | 7 | long | 15 | 0 | – | – | – | 0 | 0 | 10 | 3058 |
| mongodb | `mongodb` | 20 | long | 23 | 0 | – | – | – | 0 | 0 | 48 | 9022 |
| nifi | `nifi` | 12 | none | 8 | 0 | – | – | – | 0 | 0 | 25 | 6002 |
| parquet | `parquet` | 22 | long | 16 | 0 | – | – | – | 0 | 0 | 50 | 4749 |
| postgres | `postgres` | 2 | long | 3 | 0 | – | – | – | 0 | 0 | 2 | 212 |
| pyspark | `pyspark-00-start-here` | 0 | none | 5 | 1 | – | – | ✓ | 0 | 0 | 0 | 731 |
| pyspark | `pyspark-01-how-spark-runs` | 12 | two-line | 11 | 9 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2606 |
| pyspark | `pyspark-02-dataframe-essentials` | 14 | two-line | 14 | 12 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2909 |
| pyspark | `pyspark-03-types-functions-and-nulls` | 11 | two-line | 11 | 9 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2175 |
| pyspark | `pyspark-04-reading-and-writing-data` | 13 | two-line | 13 | 9 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2597 |
| pyspark | `pyspark-05-spark-sql-and-the-catalog` | 12 | two-line | 12 | 9 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2224 |
| pyspark | `pyspark-06-joins` | 11 | two-line | 9 | 8 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2096 |
| pyspark | `pyspark-07-aggregations-and-windows` | 17 | two-line | 15 | 14 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 3051 |
| pyspark | `pyspark-08-nested-and-semi-structured-data` | 12 | two-line | 12 | 10 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2205 |
| pyspark | `pyspark-09-python-udfs-and-pandas` | 14 | two-line | 13 | 11 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2441 |
| pyspark | `pyspark-10-batch-pipelines` | 12 | two-line | 12 | 9 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2557 |
| pyspark | `pyspark-11-structured-streaming` | 11 | two-line | 11 | 8 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2548 |
| pyspark | `pyspark-12-internals-and-monitoring` | 14 | two-line | 12 | 2 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2800 |
| pyspark | `pyspark-13-performance-tuning` | 27 | two-line | 16 | 3 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 3985 |
| pyspark | `pyspark-14-production-pyspark` | 9 | two-line | 12 | 7 | ✓ | ✓ | ✓ | 0 | 0 | 3 | 2444 |
| pyspark | `pyspark-15-interview-concepts` | 0 | none | 8 | 0 | – | ✓ | ✓ | 0 | 0 | 0 | 1972 |
| pyspark | `pyspark-coding-challenges` | 110 | two-line | 37 | 0 | – | – | – | 36 | 36 | 0 | 9660 |
| pyspark | `pyspark-concepts-end-to-end` | 17 | two-line | 11 | 6 | ✓ | ✓ | ✓ | 0 | 0 | 0 | 2087 |
| pyspark | `pyspark-drills-02-dataframe-essentials` | 24 | two-line | 8 | 0 | – | – | ✓ | 5 | 7 | 0 | 848 |
| pyspark | `pyspark-drills-03-types-functions-and-nulls` | 24 | two-line | 8 | 0 | – | – | ✓ | 5 | 7 | 0 | 835 |
| pyspark | `pyspark-drills-04-reading-and-writing-data` | 24 | two-line | 8 | 0 | – | – | ✓ | 5 | 7 | 0 | 716 |
| pyspark | `pyspark-drills-05-spark-sql-and-the-catalog` | 21 | two-line | 7 | 0 | – | – | ✓ | 5 | 6 | 0 | 686 |
| pyspark | `pyspark-drills-06-joins` | 21 | two-line | 7 | 0 | – | – | ✓ | 5 | 6 | 0 | 898 |
| pyspark | `pyspark-drills-07-aggregations-and-windows` | 24 | two-line | 8 | 0 | – | – | ✓ | 5 | 7 | 0 | 957 |
| pyspark | `pyspark-drills-08-nested-and-semi-structured-data` | 21 | two-line | 7 | 0 | – | – | ✓ | 5 | 6 | 0 | 808 |
| pyspark | `pyspark-drills-09-python-udfs-and-pandas` | 21 | two-line | 7 | 0 | – | – | ✓ | 5 | 6 | 0 | 712 |
| pyspark | `pyspark-drills-10-batch-pipelines` | 24 | two-line | 8 | 0 | – | – | ✓ | 5 | 7 | 0 | 1105 |
| pyspark | `pyspark-drills-11-structured-streaming` | 18 | two-line | 6 | 0 | – | – | ✓ | 4 | 5 | 0 | 540 |
| pyspark | `pyspark-drills-12-execution-and-production` | 20 | two-line | 6 | 0 | – | – | – | 0 | 6 | 0 | 615 |
| pyspark | `pyspark-reference` | 0 | none | 13 | 0 | – | – | – | 0 | 0 | 0 | 1613 |
| python/learning | `python-01-values-and-types` | 15 | none | 11 | 0 | – | – | – | 0 | 0 | 78 | 1529 |
| python/learning | `python-02-collections` | 27 | none | 12 | 0 | – | – | – | 0 | 0 | 112 | 3042 |
| python/learning | `python-03-control-flow-and-functions` | 20 | none | 16 | 0 | – | – | – | 0 | 0 | 67 | 1856 |
| python/learning | `python-04-iterators-and-generators` | 13 | none | 10 | 0 | – | – | – | 0 | 0 | 42 | 1314 |
| python/learning | `python-05-classes-and-dataclasses` | 22 | none | 20 | 0 | – | – | – | 0 | 0 | 75 | 2268 |
| python/learning | `python-06-files-and-formats` | 16 | none | 13 | 0 | – | – | – | 0 | 0 | 36 | 1350 |
| python/learning | `python-07-errors-logging-and-testing` | 13 | none | 10 | 0 | – | – | – | 0 | 0 | 39 | 1323 |
| python/learning | `python-08-concurrency` | 10 | none | 12 | 0 | – | – | – | 0 | 0 | 21 | 1463 |
| python/learning | `python-09-data-engineering` | 12 | none | 12 | 0 | – | – | – | 0 | 0 | 30 | 1543 |
| python/practice | `python-challenges-01-arrays-and-hashing` | 5 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1232 |
| python/practice | `python-challenges-02-two-pointers-and-sliding-window` | 5 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1313 |
| python/practice | `python-challenges-03-stacks-and-monotonic-stacks` | 5 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1279 |
| python/practice | `python-challenges-04-binary-search` | 5 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1396 |
| python/practice | `python-challenges-05-linked-lists` | 6 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1212 |
| python/practice | `python-challenges-06-binary-trees` | 6 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1118 |
| python/practice | `python-challenges-07-graphs-and-grids` | 5 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1624 |
| python/practice | `python-challenges-08-dynamic-programming` | 5 | none | 5 | 0 | – | – | – | 5 | 0 | 0 | 1159 |
| python/practice | `python-challenges-09-backtracking-heaps-intervals-design` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 1528 |
| python/practice | `python-coding-problems` | 0 | none | 17 | 0 | – | – | – | 0 | 0 | 0 | 12721 |
| python/practice | `python-drills-01-values-and-types` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 685 |
| python/practice | `python-drills-02-collections` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 715 |
| python/practice | `python-drills-03-control-flow-and-functions` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 776 |
| python/practice | `python-drills-04-iterators-and-generators` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 750 |
| python/practice | `python-drills-05-classes-and-dataclasses` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 834 |
| python/practice | `python-drills-06-files-and-formats` | 6 | none | 7 | 0 | – | – | – | 6 | 0 | 0 | 743 |
| python/practice | `python-drills-07-errors-logging-and-testing` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 732 |
| python/practice | `python-drills-08-concurrency` | 6 | none | 6 | 0 | – | – | – | 6 | 0 | 0 | 883 |
| python/practice | `python-drills-09-data-engineering` | 7 | none | 7 | 0 | – | – | – | 7 | 0 | 0 | 1010 |
| redis | `redis` | 20 | long | 26 | 0 | ✓ | – | – | 0 | 0 | 52 | 3792 |
| redshift | `redshift` | 13 | long | 38 | 0 | – | – | – | 0 | 0 | 27 | 10424 |
| scala | `scala` | 6 | none | 17 | 0 | – | – | – | 0 | 0 | 14 | 2796 |
| snowflake | `snowflake` | 16 | long | 41 | 0 | – | – | – | 0 | 0 | 36 | 16789 |
| sql | `sql-00-start-here` | 0 | none | 3 | 0 | – | – | – | 0 | 0 | 0 | 601 |
| sql | `sql-01-basics` | 40 | long | 16 | 0 | – | – | – | 0 | 0 | 54 | 3503 |
| sql | `sql-02-joins` | 30 | long | 14 | 0 | – | – | – | 0 | 0 | 36 | 2525 |
| sql | `sql-03-null-handling` | 29 | long | 11 | 0 | – | – | – | 0 | 0 | 34 | 2191 |
| sql | `sql-04-case-expressions` | 25 | long | 10 | 0 | – | – | – | 0 | 0 | 22 | 1883 |
| sql | `sql-05-aggregations-and-ctes` | 29 | long | 10 | 0 | – | – | – | 0 | 0 | 30 | 2857 |
| sql | `sql-06-set-operations` | 24 | long | 9 | 0 | – | – | – | 0 | 0 | 37 | 2445 |
| sql | `sql-07-types-functions-and-json` | 34 | long | 10 | 0 | – | – | – | 0 | 0 | 39 | 2513 |
| sql | `sql-08-window-functions` | 30 | long | 13 | 0 | – | – | ✓ | 0 | 0 | 36 | 4035 |
| sql | `sql-09-deduplication` | 18 | long | 10 | 0 | – | – | – | 0 | 0 | 21 | 2236 |
| sql | `sql-10-time-series` | 27 | long | 12 | 0 | – | – | – | 0 | 0 | 23 | 2874 |
| sql | `sql-11-modeling-and-optimization` | 24 | long | 11 | 0 | – | – | – | 0 | 0 | 28 | 2616 |
| sql | `sql-12-views-and-changing-data` | 25 | long | 11 | 0 | – | – | – | 0 | 0 | 25 | 2443 |
| sql | `sql-13-interview-drills` | 48 | long | 10 | 0 | – | – | – | 22 | 22 | 0 | 7901 |
| sql | `sql-14-interview-concepts` | 28 | long | 8 | 0 | – | – | – | 0 | 0 | 41 | 4112 |
| sql | `sql-reference` | 28 | long | 14 | 0 | – | – | – | 0 | 0 | 45 | 5322 |
| superset | `superset` | 8 | long | 11 | 0 | – | – | – | 0 | 0 | 12 | 2234 |
| tableau | `tableau` | 14 | long | 13 | 0 | – | – | – | 0 | 0 | 16 | 3020 |
| trino | `trino` | 16 | long | 24 | 0 | – | – | – | 0 | 0 | 37 | 6212 |
