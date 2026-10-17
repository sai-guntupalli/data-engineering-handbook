# Interactive Notebook Viewer — Design

Date: 2026-10-17
Status: proposed

## Goal

Turn the data engineering handbook from a static page-turner into an interactive
study tool: **read a topic → run its code → ask AI to elaborate**, locally and
privately, without disturbing the public GitHub Pages site.

## Decisions (from brainstorming)

| Question | Decision |
|---|---|
| Audience | Just the author, local/private. No auth, no multi-tenancy. |
| Execution | Real Python + PySpark + pandas (full fidelity), via a local backend. |
| AI shape | Per-section **Elaborate** button + per-page **chat panel** with follow-ups. |
| LLM backend | OpenRouter and Ollama Cloud (both OpenAI-compatible), configurable per provider/model. |
| Cloud cells | `ILLUSTRATIVE` cells (boto3 / gcloud / azure SDK calls) are read-only in the app. |

## Architecture

Two processes on the author's machine; the public static export is untouched.

```
Browser ─────────────────────────────┐
  │ Next.js app (dev mode, :3000)    │  existing gallery + new notebook viewer pages
  └──► /api/* route handlers ──► FastAPI backend (:8077, uv run)
                                    ├── POST /execute  {notebook, cell_index|code}  ──► Python kernel (subprocess)
                                    └── POST /chat     {page context, messages}     ──► OpenRouter or Ollama Cloud
```

- **Frontend**: extends the existing Next.js gallery. The public static export
  (`make site`, `output: "export"`) continues to build exactly as today —
  interactive pages and API routes are only used in local dev.
- **Backend**: small FastAPI app in Python, matching the repo's `uv` tooling.
  It owns two things: code execution and LLM calls.

## Components

### 1. Notebook viewer page (`app/topics/[name]/page.tsx`)

- Renders a topic notebook cell-by-cell: markdown as styled HTML (tables,
  code blocks, headings with anchors), code cells with a monospace block,
  a **Run** button, and an output area.
- Each `##` section gets an **Elaborate** button (top-right of the section).
- Right sidebar: chat panel scoped to the notebook page.
- Table of contents pane from the notebook's headings.

### 2. Execution endpoint (`POST /api/execute` → backend `/execute`)

- Backend keeps one long-lived Python process per session (the repo venv with
  the `notebooks-spark` extra: Python 3.13, pandas, PySpark).
- Request: notebook id + cell index (or ad-hoc code from an edited cell).
- Execution via `nbclient`-style isolated runs against a shared kernel so
  earlier cells' variables persist across later runs of the same notebook
  page (matches how a reader works top-to-bottom).
- Response: captured stdout, stderr, and any error traceback, plus elapsed
  time; rendered in the cell's output area.
- `ILLUSTRATIVE` cells (cloud SDK calls) are rendered with a read-only badge
  and no Run button — they name external systems and are not executed.
- Timeout: 60 s per cell (shorter than the 600 s CI runner — interactive use
  needs faster failure); interrupt cancels the running cell without killing
  the kernel.

### 3. Elaborate + chat endpoint (`POST /api/chat` → backend `/chat`)

- Backend builds a provider-agnostic request and forwards it to the
  configured OpenAI-compatible endpoint:
  - **OpenRouter**: `https://openrouter.ai/api/v1/chat/completions`
  - **Ollama Cloud**: `https://ollama.com/v1/chat/completions`
  - API keys from env (`OPENROUTER_API_KEY`, `OLLAMA_API_KEY`); provider and
    model chosen in a small `chat.config.yml` (or env overrides), e.g.
    `provider: openrouter`, `model: anthropic/claude-sonnet-4.5`.
- **Elaborate** sends: the section's markdown + the last N surrounding cells
  as context, with a fixed system prompt ("data engineering tutor, expand
  with one worked example and common pitfalls"). Response streams back and
  renders as a collapsible panel under the section.
- **Chat** sends: notebook title + headings outline + current visible section
  + message history (kept client-side per page). Streaming via SSE back to the
  browser.

### 4. Settings

- `chat.config.yml` (git-ignored values via env): provider, model, max tokens,
  temperature. UI settings popover reflects the active provider/model.

## Data flow

1. User opens a topic page → server component parses the notebook JSON,
   renders cells statically.
2. User clicks **Run** → `POST /api/execute` → backend executes against the
   notebook's kernel → output appears under the cell; kernel state persists
   for the page so top-to-bottom execution works.
3. User clicks **Elaborate** or sends a chat message → `POST /api/chat` →
   backend → LLM provider → streamed response renders inline / in the panel.
4. Nothing is persisted server-side except nothing at all; chat history lives
   in the page (optionally `localStorage`).

## Error handling

- Execution timeout → "timed out after 60s" output, kernel reset for that page.
- Execution exception → traceback rendered in a red-framed output block.
- Missing LLM key or unreachable provider → clear inline error telling which
  env var to set; chat input stays usable for retry.
- Kernel crash (e.g. PySpark native failure) → kernel restarted lazily on the
  next request; previous cell outputs remain displayed.

## Testing

- Backend: `pytest` with a stubbed LLM provider (fake OpenAI-compatible
  server via `httpx.MockTransport`) and real stdlib execution tests.
- Frontend: existing lint (`make lint`/`eslint`) plus component smoke tests
  for the cell renderer.
- Verification loop: `make validate` (audit + sync-check + practice-notebook
  execution + lint + site build) must keep passing; the static export must not
  regress.

## Make targets

```
make dev-local      # next dev + uvicorn together (single command)
make chat-install   # uv sync --extra interactive (fastapi, uvicorn, httpx, pytest-httpx)
```

## Non-goals

- No public deployment of the interactive app.
- No execution of cloud-SDK (ILLUSTRATIVE) cells.
- No accounts, persistence, analytics, or sharing.
