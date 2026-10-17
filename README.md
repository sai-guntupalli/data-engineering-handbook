# Data Engineering Handbook

A private handbook of runnable Jupyter notebooks for data engineering. There is no separate prose
documentation: every topic is a notebook, so the explanation and the code that proves it live in the same place.

- **Practice notebooks** (`notebooks/01..05`) are hands-on: run them top to bottom and the `assert`s check your answers.
- **Topic notebooks** (`notebooks/topics/*.ipynb`) cover one subject each, from Python basics to Snowflake, Kafka and LLMs.

## Browse them

| Where | How |
|---|---|
| **Live** | <https://sai-guntupalli.github.io/data-engineering-handbook/> — deployed from `master` by [GitHub Actions](.github/workflows) |
| Gallery app | `npm install` then `make serve` → <http://localhost:3000> — header search with suggestions (press <kbd>/</kbd>), a dedicated search page (`/search?q=…`), star your go-to notebooks |
| Jupyter locally | `make setup-notebooks` then `jupyter lab notebooks/` |
| GitHub | open any file under [`notebooks/`](notebooks) — runnable cells keep their committed output; platform-only snippets are marked `# ILLUSTRATIVE`. Every gallery card also has an **Open in Colab** button that runs the notebook in a hosted Jupyter — no local setup |

> The repository is private, so notebook links open only for collaborators. Google Colab cannot open private
> repositories; use Jupyter locally instead.

## Interactive local viewer

Topic pages can also run notebook cells and stream an LLM chat — all locally. One command starts
both servers:

```bash
make setup          # base deps (uv sync + npm install)
make chat-install   # interactive backend deps (fastapi, uvicorn, httpx)
make dev-local      # chat backend on http://127.0.0.1:8077 + gallery on http://localhost:3000
```

Two things about extras (`uv` installs exactly what a command names and removes the rest):
`make chat-install` alone means no PySpark — Spark topics need `make setup-spark` too — while
`make dev-local` and `make test` name all three extras (`notebooks`, `notebooks-spark`,
`interactive`), so they never strip packages the notebook tooling needs.

- Chat needs an API key in the environment: `OPENROUTER_API_KEY` (default provider) or
  `OLLAMA_API_KEY` for local models. `CHAT_PROVIDER` and `CHAT_MODEL` override the defaults; copy
  [`chat.config.example.yml`](chat.config.example.yml) to `chat.config.yml` (gitignored) for
  other options.
- On a topic page: **Run** executes a cell against a live kernel (each run gets 60 seconds), **Elaborate**
  asks the LLM to expand a section inline, and the chat panel streams answers over SSE.
- The kernel is per notebook, not per tab: the same notebook open in two browser tabs shares one
  server-side kernel, so variables interleave across tabs — loading (or reloading) the page resets
  it to an empty namespace.
- The backend binds to 127.0.0.1 and only allows browser calls from `localhost:3000`
  (`127.0.0.1:3000` too), so keep the gallery on its default port; it is never part of the published
  site — the static export still builds exactly as before, and viewer pages ship in it as a static
  reading view (Run buttons explain themselves when the backend is absent).

## What is inside

| Group | Notebooks |
|---|---|
| Hands-on practice | `01_python_basics`, `02_python_coding_problems`, `03_sql_interview_questions`, `04_pyspark_concepts`, `05_interview_questions` |
| Core pipeline skills | Python, Python basics, Python coding problems, SQL, Scala, Spark, Spark tuning, Airflow, dbt, Data quality, Observability |
| Lakehouse and formats | Parquet, Delta Lake, Apache Iceberg, Apache Hudi, Avro, Change data capture, Data modeling |
| Cloud and platforms | AWS, Azure, GCP, BigQuery, Redshift, Snowflake, Databricks, Trino and Presto, ClickHouse, DynamoDB, Bigtable |
| Streaming and distributed systems | Kafka, Flink, Redis, Hadoop, Hive, HBase, Cassandra, Kubernetes |
| Warehousing, BI and governance | Data warehousing, System design, Statistics, Data governance, Cost optimization, Tableau, Looker, Superset |
| AI and LLM foundations | LLM and AI terminology |
| Additional tools | MongoDB, Apache NiFi, Flume, Greenplum, Impala, Elasticsearch, Docker, Data structures |

## Layout

```text
notebooks/
  01_python_basics.ipynb ... 05_interview_questions.ipynb   practice notebooks
  topics/<topic>.ipynb                                       54 topic notebooks
app/                    Next.js gallery: searchable grouped cards with GitHub links
lib/notebooks.ts        reads the notebooks and builds the gallery data
lib/notebook-groups.ts  which notebook belongs to which group
scripts/                audit_notebooks.py, run_notebooks.py, sync_merged_copies.py, watermark_notebooks.py
```

Every notebook carries an author watermark — `metadata.watermark` (author, repository, and a permalink
to the file) plus a visible credit line under the title — stamped by
`scripts/watermark_notebooks.py` and enforced by `make check`.

## Checks

```bash
make check            # notebook structure audit (incl. the author watermark)
make watermark        # stamp the author watermark into all notebooks
make sync-check       # merged copies match their practice notebooks
make notebooks-check  # execute the practice notebooks (no writes)
make lint             # lint the gallery app
make test             # gallery unit tests + interactive backend tests
make validate         # audit + sync + execution + app lint + gallery build
make stats            # notebook counts
```

CI: [repo-checks](.github/workflows/repo-checks.yml) runs `validate` on every push and PR. The
[deploy workflow](.github/workflows/deploy-pages.yml) builds the app with `NEXT_PUBLIC_BASE_PATH`
and publishes `out/` to GitHub Pages on every push to `master`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: edit or add a notebook, add its slug to
`lib/notebook-groups.ts`, then run `make validate`.

## License

© [Sai Guntupalli](https://github.com/sai-guntupalli) — [Creative Commons Attribution 4.0
International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Reuse, remixing and
teaching are free; the one requirement is **giving credit** (author name, repository link, license,
and a note of any modifications). The full legal text is in [LICENSE](LICENSE), the human-friendly
summary with a copyable credit line is the gallery's `/license` page, and every notebook carries the
license inside its `metadata.watermark` block.