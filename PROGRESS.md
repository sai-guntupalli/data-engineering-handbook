# Progress

## Current Status

The interactive notebook viewer is implemented; the final-review fix wave and two live-verification fixes are done (grid blowout at ≥1200px, code-cell auto-fit crop) — suites green (pytest 46, vitest 34), awaiting PR merge.

## Completed

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

## In Progress

- Nothing — implementation, review fixes and verification are complete.

## Next Steps

1. Open a PR for `feat/interactive-notebook-viewer` (review → merge to `master` per the GitHub workflow).
2. Run `make dev-local` for a live hands-on smoke: run a non-Spark and a Spark cell, and one chat turn (needs `OPENROUTER_API_KEY` or `OLLAMA_API_KEY` in the environment); visually check the viewer + chat panel at browser widths.
3. Wire CI for the two test suites into `.github/workflows/repo-checks.yml` (vitest via `npm test`, backend via `uv run --extra interactive pytest backend/tests`) — final-review recommendation.
4. Optional polish (deferred, minor; the cleanup list lives in `.superpowers/sdd/2026-10-17-interactive-notebook-viewer/progress.md` while that workspace exists): persist chat history across reloads (currently React state only, per plan ruling); a same-origin `/api/*` proxy would require dropping `output: "export"` — revisit only if the viewer ever needs a non-local deployment.

## Blockers

None.
