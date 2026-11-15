# Review implementation progress — handover

This document tracks the work that implements `docs/reviews/2026-11-14-handbook-review.md` (the review). It is
written so another engineer or AI agent can pick up where this stopped. Read the review first; section and
recommendation numbers below refer to it.

- **Branch:** `improve/handbook-review-implementation`, cut from `origin/master` at `8a14ce2`. Not pushed.
- **State when handed over:** 95 of 143 notebooks meet the teaching standard (was 24 of 142); the other 48 are
  listed in `scripts/standards_baseline.json`.

## How to check the current state

```bash
uv sync --extra notebooks
uv run --no-project python scripts/notebook_standards.py --all   # every remaining warning, per notebook
uv run --no-project python scripts/audit_notebooks.py --quiet    # Colab-runnability rules
uv run pytest -q
uv run --extra notebooks python scripts/verify_practice_answers.py
JAVA_HOME=$(brew --prefix openjdk@17) uv run --extra notebooks python scripts/verify_challenge_answers.py
JAVA_HOME=$(brew --prefix openjdk@17) uv run --extra notebooks python scripts/run_notebooks.py --jobs 4 <notebooks>
```

`make check` now runs the standards check too. It fails only when a notebook gains a warning that is not in the
baseline. After migrating a notebook, run `scripts/notebook_standards.py --update-baseline` and commit the smaller
baseline.

Node.js was not available on the machine this was done on, so **the site tests (`npm --prefix site test`), lint
and build were not run** for the `site/lib/tools.ts` and `site/lib/learning-map.ts` changes. CI runs them; check
the first CI run.

## Done (commits on the branch)

| Commit | Review item | What changed |
|---|---|---|
| `aa48a67` | — | The review document itself |
| `2938b4c` | P0-2, P0-3, P1-8 | `scripts/notebook_standards.py` (+ tests, baseline, `make check`); dbt moved to a new **Transformation** category; "NoSQL and search" renamed **Databases and search**; README/CONTRIBUTING drift fixed (notebook count, PySpark modules, `PACKAGES` checklist, missing `notebook-groups.ts`) |
| `fefc22c` | P0-1 | The eight stubs rewritten as full lessons: `duckdb`, `postgres` (runs on DuckDB; PostgreSQL-only commands as syntax), `concepts/open-table-formats` (delta-rs and pyiceberg side by side), `lakehouse-catalogs`, `orchestration-patterns`, `semantic-layer`, `security-and-iam`, `cicd-and-iac`. `duckdb` bumped to `>=2.0` |
| `9bbf049` | P1-7, P2-13 | Learning path reordered (`site/lib/learning-map.ts`): Foundations → **Store** → Process at scale → Model and test → Orchestrate and stream → **Run in production** → Interview practice; drills interleaved after their lessons; capstone step; 107 of 142 notebooks on the path. Difficulty lines for 21 PySpark drill exercises; Next links; PySpark 11 links to Kafka; data-modeling lesson asserts replaced by notes |
| `0739632` | P1-4 | SQL 0–14 and reference migrated: two-line setup, asserts → shown results, What to notice notes (from the values the asserts checked), Check yourself with hidden solution cells, Key takeaways, Next; SQL 1 previews marked; SQL 11 bridges to data modeling |
| `1623fa7` | P1-5, P1-6 | Python 1–9 migrated the same way; Python practice answers moved from `<details>` markdown to `solution`-tagged code cells; `verify_practice_answers.py` updated (all 19 pass); coding problems got exercise cells and Difficulty lines |
| `65edc32` | P2-13 | What to notice notes for PySpark 12 (9) and 13 (13) |
| (this commit) | P2-10 (started) | `dataframes/` folder and `DataFrames 1: pandas essentials and traps` (pandas 3); tool registered in `tools.ts`; this handover; helper scripts |

Every changed notebook was executed after editing, and each What to notice note was checked against that run.

## Not done yet (in priority order)

1. **DataFrames track** (review §1, P2-10). Planned: `dataframes-02-polars`, `dataframes-03-arrow`,
   `dataframes-04-choosing-an-engine` (same task in pandas, Polars, DuckDB with timing and memory). When added,
   change the Next link at the end of `dataframes-01-pandas` (currently points to DuckDB) and add a learning-path
   step. Polars 2.1 resolves with the current lock.
2. **Core tool courses** (P2-9):
   - **Kafka** course `kafka-01`…`kafka-05` (log and partitions, producers, consumers and groups, delivery and
     transactions, Connect and Schema Registry). No broker runs in Colab, so cells must stay clearly labelled models;
     keep `kafka.ipynb` as the overview/reference or retire it via `site/lib/retired.ts`.
   - **dbt** course (models and `ref`, tests and contracts, incremental and microbatch, snapshots) using
     `dbt-core` + `dbt-duckdb` (already dependencies; see how `dbt/dbt.ipynb` runs its build).
   - **Airflow**: real DAGs with `dag.test()` were recommended. Not yet tested whether `apache-airflow` 3 resolves
     with the lock and installs in reasonable CI time; test that before writing.
   - **Stream processing concepts** notebook (time, windows, watermarks, state, guarantees) in `concepts/`.
3. **Ingestion track** (P2-10): `ingestion-01-batch-patterns`, `-02-apis` (`httpx.MockTransport` for pagination,
   429/Retry-After, retries), `-03-object-storage` (`moto` S3 landing, manifests), `-04-dlt` (dlt into DuckDB).
   `pandera>=0.24` and `dlt[duckdb]>=1.10` resolved cleanly in a trial (`uv add --optional notebooks ...`) but were
   **not** added, because nothing uses them yet.
4. **Data quality tooling** notebook with pandera; **Git and shell** working-environment notebook; **capstones**
   (batch lakehouse, streaming orders, CDC to SCD2) (P2-10, P3-16).
5. **The 48 notebooks still in the baseline** (P2-11, P2-12): tool and concept FAQ notebooks (Kafka, Flink,
   Airflow, BigQuery, Redshift, Snowflake, clouds, NoSQL, formats, BI, legacy tools, concepts), the interview
   question bank, `data-structures`, `statistics`, `llm`, SQL 13 (setup only). Each needs: two-line setup, asserts
   turned into shown output, What to notice notes, Check yourself, Key takeaways, Next — and, per the review, FAQ
   headings rewritten into topic-ordered lessons (about 12 sections each). Also cut `data-structures` to a
   data-engineering page and move `statistics` to an appendix.
   - **`llm/llm.ipynb` is being changed on another branch (`improve/llm-ai-handbook`)** in the main checkout. Do not
     edit it here; coordinate.
6. **Concepts split** (review §3): divide the "Concepts" category into architecture/design and
   quality/governance/operations in `tools.ts`.
7. **Site UI** (P3-14/15): mobile header still wraps into two rows; average page 322 KB; Draft/Legacy badge in
   search; "Last reviewed" on the remaining tool pages. Needs Node to test.
8. **SQL "Watch out for" blocks** (review §4): the SQL and Python lessons use "Where you'll use it" but not
   "Watch out for"; the standards check does not require it. Optional.
9. **Folder redesign** (review "Proposed redesign"): not started; it changes URLs, so every move needs an entry in
   `site/lib/retired.ts`.

## How the work was done (reusable helpers)

One-off helpers are saved in `docs/reviews/2026-11-migration-tools/`. Paths inside them point at the scratch
worktree they were written in; change `REPO`/`ROOT`/`S` at the top before using them.

- `nbtools.py` — `build(relpath, SPEC)` writes a notebook from a compact spec (`%% md`, `%% code`, `%% solution`
  separators) and runs the formatter; `run(relpath)` executes it and prints each code cell's output, so notes can be
  checked against real results. `specs/` holds the specs of every new notebook (rebuild with `python specs/x.py`).
- `convert.py` — SQL migration: `PACKAGES` → two-line setup, drop asserts that re-check a shown query, turn others
  into output (`finish`, `all_asserts_to_prints`).
- `pyconvert.py` — Python migration: each assert → a `print(f"{expr = }")` of the checked value (whole comparison
  when both sides are expressions).
- `restructure.py` — Practice questions/Answers/Summary → Check yourself (empty cell + hidden solution per
  question), Key takeaways, Next. `add_notes` inserts notes after code cells matched by substring.
- `notes/apply_idx.py` — inserts notes after code cells by index with an expected-substring guard. Prefer this to
  substring matching: substring keys matched the wrong cell several times.
- `inventory.py` — the per-notebook inventory used by the review.

Workflow per notebook: migrate mechanically → run it → read the output → write notes from the output → run again →
`notebook_standards.py --all <file>` → update the baseline → commit.

## Gotchas found on the way

- **DuckDB 2.0**: relations have no `fetchone()`; `.arrow()` returns a record batch reader (use `to_arrow_table()`);
  `con.execute()` leaves a result open that must be consumed before the next statement on that connection; a relation
  cannot be read from another connection; write conflicts fail at the second `UPDATE`, not at commit.
- **pandas 3**: copy-on-write always on; chained assignment silently does nothing (warning); text columns are the
  `str` dtype; `Series.apply` on scalars is fast, so demonstrate slowness with `apply(axis=1)`.
- **pyiceberg 0.12**: a stale overwrite fails with `ValidationException` after a catalog retry; add partition specs
  with `update_spec()` rather than passing field ids to `create_table`.
- **Shell heredocs**: an unquoted `<<EOF` runs backticks in markdown as commands. Write Python helpers to files.
- **Formatter**: run `scripts/notebook_format.py` after any edit; the audit fails on non-canonical notebooks and on
  links to notebooks that do not exist yet.
