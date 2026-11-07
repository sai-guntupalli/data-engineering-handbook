# Data Engineering Handbook

An open handbook of **runnable Jupyter notebooks** for data engineering. Every topic is one notebook: a short
explanation, a small example right below it, and `assert`s that prove the point. Every notebook opens in
**Google Colab** and runs top to bottom with no local setup — CI executes all of them on every change.

**Browse:** <https://sai-guntupalli.github.io/data-engineering-handbook/> — every card has an *Open in Colab* button.

## Run a notebook

| Where | How |
|---|---|
| **Google Colab** | Click the *Open in Colab* badge at the top of any notebook, then *Runtime → Run all*. The first code cell installs what that notebook needs. |
| **Locally** | `make install`, then `uv run --extra notebooks jupyter lab notebooks/` |

No notebook talks to a real server or cloud account. External systems are replaced with in-process stand-ins:
DuckDB for warehouse SQL (BigQuery, Snowflake, Redshift, Trino, Hive...), PySpark SQL and local mode (the SQL learning path), `deltalake`,
`pyiceberg` with a SQLite catalog, `fakeredis`, `mongomock`, `moto` for AWS, and small pure-Python simulations
for Kafka, Flink, Airflow, Cassandra, HBase and friends. Platform-only snippets (YAML, Scala, cloud SDK calls)
are shown in markdown code blocks.

## What is inside

| Group | Notebooks |
|---|---|
| Hands-on practice | `01_python_basics`, `02_python_coding_problems`, `03_sql_interview_questions` (start of the SQL path), `04_pyspark_concepts`, `05_interview_questions`, `06_pyspark_coding_challenges` (interview problems) |
| SQL learning path | SQL basics, WHERE vs HAVING, NULL handling, CASE, Joins, Window functions, Deduplication, Time-series, Modeling and optimization, Interview drills (Spark SQL) |
| Core pipeline skills | Python, SQL, Scala, Spark, Spark tuning, Airflow, dbt, Data quality, Observability |
| Lakehouse and formats | Parquet, Delta Lake, Iceberg, Hudi, Avro, Change data capture, Data modeling |
| Cloud and platforms | AWS, Azure, GCP, BigQuery, Redshift, Snowflake, Databricks, Trino, ClickHouse, DynamoDB, Bigtable |
| Streaming and distributed systems | Kafka, Flink, Redis, Hadoop, Hive, HBase, Cassandra, Kubernetes |
| Warehousing, BI and governance | Data warehousing, System design, Statistics, Data governance, Cost optimization, Tableau, Looker, Superset |
| AI and LLM foundations | LLM and AI terminology (fully offline) |
| Additional tools | MongoDB, NiFi, Flume, Greenplum, Impala, Elasticsearch, Docker, Data structures |

## Layout

```text
notebooks/                 the product: 6 practice notebooks + topics/<topic>.ipynb (68 total)
scripts/
  notebook_format.py       canonical form: credit line, Open in Colab badge, no outputs, stable cell ids
  audit_notebooks.py       Colab-runnability rules (setup cell, no live servers, one title, links...)
  run_notebooks.py         executes notebooks like Colab's "Run all" (--jobs N for parallel)
tests/                     unit tests for the tooling
site/                      Next.js static gallery (GitHub Pages); reads ../notebooks at build time
```

## Commands

```bash
make install     # notebook packages + dev tools (uv) and site dependencies (npm)
make format      # format notebooks and Python tooling
make check       # audit every notebook
make notebooks   # execute every notebook (PySpark ones need Java 8-21; JOBS=4 by default)
make test        # tooling unit tests
make lint        # ruff + eslint
make dev         # serve the gallery at http://localhost:3000
make build       # static site into site/out
make validate    # everything CI runs
```

CI: [Checks](.github/workflows/repo-checks.yml) runs `make validate` (with Java 17) on every PR and on `master`.
[Deploy](.github/workflows/deploy-pages.yml) publishes `site/out` to GitHub Pages on every push to `master`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): the setup-cell shape, the stand-in rules, and the commit checklist.

## License

© [Sai Guntupalli](https://github.com/sai-guntupalli) — [Creative Commons Attribution 4.0 International
(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Reuse, remixing and teaching are free; the one
requirement is **giving credit** (author name, repository link, license, and a note of any modifications). Every
notebook opens with a credit line. The full legal text is in [LICENSE](LICENSE).
