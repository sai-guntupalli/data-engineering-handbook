# Data Engineering Handbook

An open handbook of **runnable Jupyter notebooks** for data engineering. Every topic is one notebook: a short
explanation, a small example right below it, and `assert`s that prove the point. Every notebook opens in
**Google Colab** and runs top to bottom with no local setup — CI executes all of them on every change.

**Browse:** <https://sai-guntupalli.github.io/data-engineering-handbook/> — read any notebook on the site, or open it
in Colab to run it.

## The site

- **Library**: a learning map that draws the core notebooks as a pipeline DAG, resume cards for what you were
  reading, and a catalog of every notebook you can filter by group or by your stars.
- **Notebook reader**: each notebook rendered as a page (`/notebooks/<slug>/`) with highlighted code, a cell map of
  explanations, code and self-checks, a table of contents that ticks off sections as you scroll past them, and
  buttons to open it in Colab or download the `.ipynb`.
- **Search**: press <kbd>⌘K</kbd>, <kbd>Ctrl+K</kbd> or <kbd>/</kbd> anywhere to search every notebook title and
  section heading, with a preview of the match. `/search?q=…` lists all results.
- **Collapsible panels**: fold the sidebar into an icon rail with the button at the left of the top bar (or press
  <kbd>[</kbd>), and fold a notebook's table of contents with the button above it (or press <kbd>]</kbd>). The page and the
  article widen into the space a collapsed panel frees.
- **Progress, stars and display choices** (theme, collapsed panels) stay in your browser (localStorage) and apply
  before the page paints; there are no accounts. Light and dark themes follow your system, with a toggle in the top bar.

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

Every notebook lives in the folder of the tool it teaches, under `notebooks/topics/`. The site lists the tools; choosing one shows its subtopics.

| Folder | What it holds |
|---|---|
| `python/learning/` | Python lessons from values and types to data-engineering patterns |
| `python/practice/` | Python drills, coding challenges and interview basics |
| `sql/` | SQL lessons from SELECT to window functions, interview drills and a reference |
| `spark/` | Spark overview, eight PySpark modules, Spark tuning and PySpark interview practice |
| `interview-questions/` | Questions across Python, SQL and Spark, with model answers and runnable checks |
| `concepts/` | Data concepts that apply to any stack: modeling, quality, governance, CDC, cost and design |
| `llm/` | Terminology and data-engineering ideas for language models |
| One folder per tool | Airflow, Avro, AWS, Azure, BigQuery, Bigtable, Cassandra, ClickHouse, Databricks, dbt, Delta Lake, Docker, DynamoDB, Elasticsearch, Flink, Flume, Google Cloud, Greenplum, Hadoop, HBase, Hive, Hudi, Iceberg, Impala, Kafka, Kubernetes, Looker, MongoDB, NiFi, Parquet, Redis, Redshift, Scala, Snowflake, Superset, Tableau and Trino |

## Layout

```text
notebooks/topics/          the product: one folder per tool (106 notebooks in total)
scripts/
  notebook_format.py       canonical form: credit line, Open in Colab badge, no outputs, stable cell ids
  audit_notebooks.py       Colab-runnability rules (setup cell, no live servers, one title, links...)
  run_notebooks.py         executes notebooks like Colab's "Run all" (--jobs N for parallel)
tests/                     unit tests for the tooling (pytest)
site/                      Next.js static site (GitHub Pages); reads ../notebooks at build time
  lib/notebook-parse.ts    notebook JSON -> title, sections, cells, reading time (pure, unit-tested)
  lib/notebooks.ts         reads the files, checks the registry, builds summaries and the search index
  lib/tools.ts             the tool registry: one entry per notebooks/topics/ folder, with labels, colour and categories
  lib/learning-map.ts      the curated DAG on the home page, validated against the registry
  lib/progress.ts          reading-progress rules (stored in the browser)
  app/tools/[tool]/        one page per tool, listing its subtopics
  app/notebooks/[slug]/    the reader; app/files/ serves each .ipynb; app/search-index.json feeds search
  tests/                   vitest unit tests for lib/
docs/mockups/              static design mockups the site is built from
```

## Commands

```bash
make install     # notebook packages + dev tools (uv) and site dependencies (npm)
make format      # format notebooks and Python tooling
make check       # audit every notebook
make notebooks   # execute every notebook (PySpark ones need Java 8-21; JOBS=4 by default)
make test        # unit tests: tooling (pytest) and site data layer (vitest)
make lint        # ruff + eslint
make dev         # serve the gallery at http://localhost:3000
make build       # static site into site/out
make validate    # everything CI runs
```

CI: [Checks](.github/workflows/repo-checks.yml) runs `make validate` (with Java 17) on every PR and on `master`.
[Deploy](.github/workflows/deploy-pages.yml) publishes `site/out` to GitHub Pages on every push to `master`.

## Site URLs

The gallery is served from a path on GitHub Pages (`/data-engineering-handbook`). Two build-time variables must agree:

| Variable | Set to | Used for |
| --- | --- | --- |
| `NEXT_PUBLIC_BASE_PATH` | `/data-engineering-handbook` (the Pages build sets it; leave unset locally) | Asset and route paths (`site/next.config.ts`) |
| `NEXT_PUBLIC_SITE_URL` | `https://sai-guntupalli.github.io/data-engineering-handbook` (the default) | Canonical URLs, sitemap and robots (`site/lib/site.ts`) |

Deploying to another host or repository means changing both; the sitemap is built from `NEXT_PUBLIC_SITE_URL`, so a stale value there produces wrong sitemap URLs.

## Design mockups

The site's design started as static HTML mockups in [`docs/mockups/`](docs/mockups): a library with a learning map,
a notebook reader, and a search palette. They need no build step and are kept as the design reference.

| Where | How |
| --- | --- |
| **Live** | <https://sai-guntupalli.github.io/data-engineering-handbook/mockups/>, published with the site on every push to `master` |
| Locally | `make mockups`, then <http://localhost:8000> |

`make build` copies them into `site/out/mockups`, and the Pages workflow runs `make mockups-bundle` after the site build.
The pages are marked `noindex`, so search engines skip them. Each screen has a light/dark toggle and works at phone
width. `tests/test_mockups.py` checks that every link between them is relative and resolves. The live site in `site/`
implements them with real notebook data; the mockups' sample progress and output tables are illustrations only.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): the setup-cell shape, the stand-in rules, and the commit checklist.

## License

© [Sai Guntupalli](https://github.com/sai-guntupalli) — [Creative Commons Attribution 4.0 International
(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Reuse, remixing and teaching are free; the one
requirement is **giving credit** (author name, repository link, license, and a note of any modifications). Every
notebook opens with a credit line. The full legal text is in [LICENSE](LICENSE).
