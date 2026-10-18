# Progress

## Current Status

`feat/sql-duckdb` (stacked on `feat/interactive-notebook-viewer`): the SQL interview notebook (03) is deep-rewritten from in-memory sqlite3 to in-memory DuckDB (engine + helpers, Q1–Q22 ported, new Part 7 with five DuckDB-only lessons, theory cards refreshed), the merged topics/sql copy retired, `make validate` green and the viewer smoke ran cells against the live kernel; viewer polish follow-ups applied (Elaborate gated to real sections, dev-local sources a git-ignored `.env`).

## Completed

- [x] 2026-10-18 — Elaborate only on sections worth explaining (0f95791, from user feedback on the data-warehouse-architecture notebook): the intro (title/author/how-to) and pure-navigation sections ("Contents"/"Table of Contents"/"Outline"/"Index" headings, or code-less sections whose link-stripped prose is under 400 chars) no longer render an Elaborate button; the gate is `isElaboratable` in the client-safe `lib/section-elaborate.ts` (re-exported from `lib/notebook-content.ts`) — a runtime import from `notebook-content.ts` itself would drag its `node:fs` into the client bundle and break the Turbopack build. Panel plumbing unchanged; 7 new lib tests + 1 viewer gating test (54 vitest)
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

- Nothing — implementation, review fixes and verification are complete.

## Next Steps

1. Open a PR for `feat/interactive-notebook-viewer` (review → merge to `master` per the GitHub workflow).
2. Run `make dev-local` for a live hands-on smoke: run a non-Spark and a Spark cell, and one chat turn (needs `OPENROUTER_API_KEY` or `OLLAMA_API_KEY` in the environment); visually check the viewer + chat panel at browser widths.
3. Wire CI for the two test suites into `.github/workflows/repo-checks.yml` (vitest via `npm test`, backend via `uv run --extra interactive pytest backend/tests`) — final-review recommendation.
4. Optional polish (deferred, minor; the cleanup list lives in `.superpowers/sdd/2026-10-17-interactive-notebook-viewer/progress.md` while that workspace exists): persist chat history across reloads (currently React state only, per plan ruling); a same-origin `/api/*` proxy would require dropping `output: "export"` — revisit only if the viewer ever needs a non-local deployment.

## Blockers

None.
