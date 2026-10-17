# Progress

## Current Status

Tasks 1–7 of the interactive notebook viewer are implemented, tested and verified: a FastAPI chat/backend on `127.0.0.1:8077`, a notebook viewer + chat panel in the gallery, `make dev-local` to run both, and docs — awaiting review and PR merge.

## Completed

- [x] 2026-10-17 — Spec written (`.superpowers/sdd/2026-10-17-interactive-notebook-viewer/`)
- [x] 2026-10-17 — Plan written with recorded rulings (browser → FastAPI direct, SIGINT interrupt, chat in React state, static reading view)
- [x] 2026-10-17 — Task 1: pyproject `interactive` extra (fastapi, uvicorn, httpx, pytest-httpx, pyyaml) and `make chat-install`
- [x] 2026-10-17 — Task 2: `backend/chat_config.py` — provider/model config (`chat.config.yml` + `OPENROUTER_API_KEY`/`OLLAMA_API_KEY`, `CHAT_PROVIDER`/`CHAT_MODEL` overrides)
- [x] 2026-10-17 — Task 3: `backend/kernel_proc.py` + `backend/kernel.py` — kernel subprocess with SIGINT interrupt, 60 s execute timeout, `POST /execute`, `POST /reset`, `GET /health` on `127.0.0.1:8077`
- [x] 2026-10-17 — Task 4: `backend/llm.py` + `backend/main.py` — `POST /chat` SSE streaming (OpenRouter/Ollama), `GET /chat/settings`, CORS restricted to `localhost:3000`/`127.0.0.1:3000`
- [x] 2026-10-17 — Task 5: notebook content parser (`lib/notebook-content.ts`), markdown rendering (`lib/markdown.ts`), vitest suites (26/26)
- [x] 2026-10-17 — Task 6: topic viewer page (`app/topics/[name]/page.tsx`), `components/notebook-viewer.tsx` (Run/Elaborate cells), `components/chat-panel.tsx` (SSE settings popover), `lib/interactive-api.ts` client
- [x] 2026-10-17 — Task 7: `scripts/dev-local.sh` (uvicorn first, /health-poll readiness, `trap` kills both), `make dev-local` + `make test`, README "Interactive local viewer" section, this PROGRESS.md. Note: `make test`/`make dev-local` name all three uv extras because `uv run`/`uv sync` prune any extra not listed — first `make test` run with only `--extra interactive` stripped `notebooks` from the venv and broke `make validate`'s sync-check.
- [x] 2026-10-17 — Verification loop: `make test` (vitest 26/26 + pytest 44 passed) and `make validate` (audit + sync-check + notebooks-check + lint + site build) all green

## In Progress

- Nothing — implementation and verification are complete.

## Next Steps

1. Open a PR for `feat/interactive-notebook-viewer` (review → merge to `master` per the GitHub workflow).
2. Run `make dev-local` for a live hands-on smoke: run a non-Spark and a Spark cell, and one chat turn (needs `OPENROUTER_API_KEY` or `OLLAMA_API_KEY` in the environment).
3. Optional polish (deferred, minor): persist chat history across reloads (currently React state only, per plan ruling); a same-origin `/api/*` proxy would require dropping `output: "export"` — revisit only if the viewer ever needs a non-local deployment.

## Blockers

None.