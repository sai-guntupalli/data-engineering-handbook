# Progress

## Current Status

`feat/spark-story` (stacked on `feat/sql-duckdb`): the shared sample-data section is in
`topics/spark.ipynb` Part 2 (customers/orders/order_items/events seed with explicit
schemas, show()s and a sanity-check assert cell) and 13 data-shaping lesson cells now run
on it as runnable cells (joins, aggregations, windows, the dates/tz/nulls/flags/dedupe
cookbook). Verified by a real local Spark 4.2 run of the whole topic notebook, `make
check`, sync-check, both test suites, lint + site build, and a live-viewer smoke.

## Completed

- [x] 2026-10-18 — Shared sample data for the spark notebook lessons (report
  `.superpowers/sdd/spark-seed-report.md`): new "Sample data: the tables every lesson below
  runs on" section in Part 2 of `notebooks/topics/spark.ipynb` (12 cells: intro, session
  bootstrap, four seeded tables with explicit schemas + committed `show()`/`printSchema()`
  outputs, row-count sanity cell with per-order ledger reconciliation asserts); 13
  illustrative lesson cells re-wired to run on the seed (joins 85/87/90,
  aggregations 94/96, windows 102/108, cookbook 114/116/120/124/130/135); old
  `main.bronze.orders` binder cell removed; Part headers + section intros updated;
  merged region + practice notebook untouched (byte-verified). Gates: full real-Spark
  nbclient run of the topic notebook (illustrative cells skipped per the viewer's
  read-only contract; merged region ran live), `make check`, sync-check, vitest 54,
  backend pytest 46 (test_execute_endpoint.py now locates its two pinned cells by
  marker instead of hardcoded indexes), lint + site build, live-viewer smoke of the
  seed section + join lesson (java shim-symlinked into `.venv/bin/java` for the running
  backend).
- [x] 2026-10-18 — Spark story restructure complete (plan `docs/superpowers/plans/2026-10-18-spark-notebook-story.md` committed first, report in `.superpowers/sdd/2026-10-18-spark-notebook-story/spark-story-report.md`):
  - [x] Task 1 (75dbf10): practice notebook `04` restructured — five part headers with connective prose, intro rewritten to a five-part map, six two-idea markdown cells split, two statefulness bugs fixed (depth-check used `spark` before the session cell; join-plan comparison used `customers` before the inputs cell — both NameErrors under a real Spark runtime, invisible in CI where Java is absent), self-check 3's row count corrected 5→4 (paid x3 + shipped x1). Verified: `run_notebooks.py --check` green with AND without Java (Spark 4.2 via homebrew openjdk@21); outputs saved; audit 183 md / 81 code / 73 asserts (code and asserts unchanged).
  - [x] Task 2 (14fa340): merged tail of `topics/spark.ipynb` rebuilt verbatim by `scripts/sync_merged_copies.py` (never hand-edited); `--check` green.
  - [x] Task 3 (2c8dc6a): topic-authored arc rebuilt into the five-part story — intro section condensed into three labelled cells, RDD-vs-DataFrame prose to orientation with its two illustrative one-liners moved to Part 2, new "When you would NOT use PySpark" section, bold one-idea cookbook leads, performance already split into labelled lessons, use cases + interview-answer structure as Part 5, closing pointer into the merged workbook. All 23 original sections and all 67 authored code cells survive; illustrative/runnable statuses unchanged (code=148, asserts=77); markdown words 18458→19243 (+4.2%). Viewer smoke: bootstrap probe, session-creation and DataFrame cells ran in the live browser kernel with zero errors and a clean console.
  - [x] Task 4: `make validate` green (audit + sync-check + notebooks-check + lint + site build).
- [x] 2026-10-18 — Elaborate only on sections worth explaining (0f95791, from user feedback on the data-warehouse-architecture notebook): the intro (title/author/how-to) and pure-navigation sections ("Contents"/"Table of Contents"/"Outline"/"Index" headings, or code-less sections whose link-stripped prose is under 400 chars) no longer render an Elaborate button; the gate is `isElaboratable` in the client-safe `lib/section-elaborate.ts` (re-exported from `lib/notebook-content.ts`) — a runtime import from `notebook-content.ts` itself would drag its `node:fs` into the client bundle and break the Turbopack build. Panel plumbing unchanged; 6 new lib tests + 1 viewer gating test (54 vitest)
- [x] 2026-10-18 — `dev-local` loads a git-ignored `.env` (215070b): `scripts/dev-local.sh` runs `set -a; source ./.env 2>/dev/null || true; set +a` before uvicorn, so `OPENROUTER_API_KEY`/`OLLAMA_API_KEY`/`CHAT_PROVIDER`/`CHAT_MODEL` persist across sessions (shell exports still work); `.env` gitignored, README's interactive section documents the flow, snippet verified standalone with a throwaway .env (since removed)

- [x] 2026-10-18 — Plan written (`.superpowers/sdd/2026-10-18-sql-notebook-duckdb/`, plan doc committed first)
- [x] 2026-10-18 — Task 1: `duckdb>=1.0` in the `notebooks` extra (`uv lock`); setup rewritten — `duckdb.connect(":memory:")`, same `run`/`show` signatures, DuckDB-native `DATE`/`TIMESTAMP` columns, helpers + seed asserted; mechanical dialect swaps keep the bank runnable
- [x] 2026-10-18 — Task 2: Q1–Q22 ported (date/timestamp asserts, strftime months, `date_diff`, Q7 `UPDATE ... FROM` check, Q17 real `PIVOT`/`UNPIVOT` + CASE, Q18 `median()`/`quantile_cont` + portable window version, Q22 `COUNT(DISTINCT) OVER`)
- [x] 2026-10-18 — Task 3: Part 7 "DuckDB skills that SQLite could not teach" (QUALIFY, PIVOT/UNPIVOT, ASOF JOIN with a new `fx_rates` seed, LIST/STRUCT, EXPLAIN/EXPLAIN ANALYZE); T1/T2/T4/T5/T9/T13/T14 + closing refreshed
- [x] 2026-10-18 — Task 4: `make watermark` + audit; merged `notebooks/topics/sql.ipynb` grown to the new cell set and sync'd (108 code cells + topic bonuses, sync-check green); `make validate` green; live viewer smoke (setup cells + Q1 ran in the browser kernel, duckdb 1.5.6)
- [x] 2026-10-18 — Review-fix wave: Q9's expected count (11, not 12), Part 5 intro credits DuckDB's `median()`, seed summary now states the real three tied salary pairs + two duplicate email pairs, Q2's tie check ordered deterministically, Q5's second delete compares within the scratch table itself, RANGE-frame / ASOF-cast / `updated_at` wording corrected
- [x] 2026-10-18 — Task 5: retired `notebooks/topics/sql.ipynb` (hands-on practice notebook is canonical; the identical merged copy is redundant to maintain) — removed the sync CONFIG entry, the "sql" slug from `lib/notebook-groups.ts`, README's group-table row and count (54 → 53), and CONTRIBUTING's merged-copies mention; all gates green (audit 58 notebooks, vitest 35, pytest 46, `make validate`)

- [x] 2026-10-17 — Spec written (`.superpowers/sdd/2026-10-17-interactive-notebook-viewer/`)
- [x] 2026-10-17 — Plan written with recorded rulings (browser → FastAPI direct, SIGINT interrupt, chat in React state, static reading view)
- [x] 2026-10-17 — Task 1: pyproject `interactive` extra (fastapi, uvicorn, httpx, pyyaml) and `make chat-install`
- [x] 2026-10-17 — Task 2: `backend/chat_config.py` — provider/model config (`chat.config.yml` + `OPENROUTER_API_KEY`/`OLLAMA_API_KEY`, `CHAT_PROVIDER`/`CHAT_MODEL` overrides)
- [x] 2026-10-17 — Task 3: `backend/kernel_proc.py` + `backend/kernel.py` — kernel subprocess with SIGINT interrupt, 60 s execute timeout, `POST /execute`, `POST /reset`, `GET /health` on `127.0.0.1:8077`
- [x] 2026-10-17 — Task 4: `backend/llm.py` + `backend/main.py` — `POST /chat` SSE streaming (OpenRouter/Ollama), `GET /chat/settings`, CORS restricted to `localhost:3000`/`127.0.0.1:3000`
- [x] 2026-10-17 — Task 5: notebook content parser (`lib/notebook-content.ts`), markdown rendering (`lib/markdown.ts`), vitest suites
- [x] 2026-10-17 — Task 6: topic viewer page (`app/topics/[name]/page.tsx`), `components/notebook-viewer.tsx` (Run/Elaborate cells), `components/chat-panel.tsx` (SSE settings popover), `lib/interactive-api.ts` client
- [x] 2026-10-17 — Task 7: `scripts/dev-local.sh` (uvicorn first, /health-poll readiness, `trap` kills both), `make dev-local` + `make test`, README "Interactive local viewer" section, this PROGRESS.md. Note: `make test`/`make dev-local` name all three uv extras because `uv run`/`uv sync` prune any extra not listed — first `make test` run with only `--extra interactive` stripped `notebooks` from the venv and broke `make validate`'s sync-check.
- [x] 2026-10-17 — Verification loop: `make test` (vitest + pytest) and `make validate` (audit + sync-check + notebooks-check + lint + site build) all green
- [x] 2026-10-17 — Final review (`.superpowers/sdd/final-review.md`) and fix wave:
  - FINAL-1/FINAL-3: `resetKernel` POSTs `/reset` and `NotebookViewer` fires it once on mount (ref-guarded, StrictMode-safe), so "Reload resets it" is true; a kernel whose interrupt grace expires reports `interrupted` (HTTP `timeout`) and auto-resets instead of staying wedged (`backend/kernel.py`)
  - FINAL-2: `ChatPanel` receives `sectionIds`, observes `data-nb-section-id` rows with an IntersectionObserver (first section is the fallback), and sends the live `visible_section` in chat requests
  - FINAL-9: a failed Elaborate stream clears its `started` flag so the next click re-requests
  - FINAL-4/FINAL-6: non-dict notebook JSON is a 400 (`backend/sessions.py`); HTTP refusals map to status `error` with the detail in the traceback, "crashed" reserved for transport failure (`lib/interactive-api.ts`)
  - FINAL-5/FINAL-8: dead `pytest-httpx` dependency removed (pyproject, Makefile help, uv.lock); EOF newlines added to seven files; README notes the per-notebook (shared-across-tabs) kernel
  - FINAL-11: `RUNNABLE_CELL_INDEX` is computed from the notebook at test time, no longer hardcoded
- [x] 2026-10-18 — Grid blowout at ≥1200px (cb38d8f, found by live browser verification): the article column could not shrink below min-content and slid under the sticky chat panel; fixed with `minmax(0, 1fr)` grid tracks + `min-width: 0`, plus scrolling tables and `overflow-wrap` on inline code
- [x] 2026-10-18 — Code cells auto-fit their content (6989afa, found by the user's report, verified live — 114/114 code cells fit with no crop): code cell textareas auto-grow to content via `useLayoutEffect` + `scrollHeight`, soft-wrap with `overflow-wrap: anywhere`, and the resize grip was removed
- [x] 2026-10-18 — Syntax highlighting for pristine code cells (highlight.js, python/sql via `detectLanguage`, json/bash/plaintext registered): untouched cells render highlighted `<pre><code class="hljs">` (pre-wrap, no crop); an Edit button swaps the one cell into the textarea, Revert restores the pristine source; Run keeps the cell_index/ad-hoc exactly-one-of contract
- [x] 2026-10-18 — Starring no longer reorders the explore gallery (groups render in declared order, hint line removed); stars stay a pure card marker (search page keeps its starred-first behavior)

## In Progress

- Nothing — sample-data seed complete and all gates green.

## Next Steps

1. Add the sample-data commit to PR #27 (`feat/spark-story`); it lands on top of 07f851d.
2. Wire CI for the two test suites into `.github/workflows/repo-checks.yml` (vitest via `npm test`, backend via `uv run --extra interactive pytest backend/tests`) — final-review recommendation.
3. Note that CI's `run_notebooks.py --check` has no Java: the Spark-shaped guards only really evaluate where a JDK exists. A follow-up could add a Java install to the repo-checks workflow so order-bugs like the two fixed here fail in CI too.

## Blockers

None.
