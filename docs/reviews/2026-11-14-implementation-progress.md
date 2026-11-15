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

Node became available during the follow-up. The site passed all 85 tests, ESLint, and its production build.

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

## Current status and remaining work

1. **DataFrames track complete** (P2-10). Added Polars, Arrow, and the engine comparison. All four notebooks ran cleanly and passed the standards check. The learning path includes the track and pandas links to Polars. The baseline remains at 48 notebooks (98 of 146 meet the standard).
2. **Core tool courses started and runnable** (P2-9). Added five explicitly labeled Kafka models, four dbt/DuckDB labs, a real Airflow 3 TaskFlow DAG, and a streaming-concepts lesson. Airflow 3.4.0 resolved and installed in about nine seconds in the isolated local test. Its DAG returned success and 2000 cents. Follow-up labs run bounded event-time batches through dbt/DuckDB, record a real Airflow asset event, and replay daily data intervals locally. The dbt lab uses explicit bounds with a merge. The Airflow labs use dag.test to exercise task execution and metadata without a scheduler.
3. **Ingestion and data quality complete for the planned introductory lessons** (P2-10). Added a replayable batch cursor, HTTPX mock pagination and retry, Moto S3 manifests, a dlt-to-DuckDB load, and Pandera validation. The dlt and Pandera dependencies are now in the notebook extra.
4. **Working environment and capstones** (P2-10, P3-16). Added a Git and shell lab, a real Delta batch publication lab, and small streaming replay and CDC-to-SCD2 capstones. The latter two are in-memory models.
5. **Standards migration** (P2-11, P2-12). All 42 eligible baseline entries were cleared. The check now reports 168 of 169 notebooks meeting the standard. The LLM notebook is the sole baseline exception and remains on its separate branch. The migrated material retains the existing examples and topic depth. Many longer lessons still have room for more per-example explanations and a shorter topic sequence beyond the lint requirements.
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
