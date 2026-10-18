# Interactive Notebook Viewer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the handbook into a local interactive study tool: read a topic notebook, run its cells against a persistent Python kernel, and ask an LLM (OpenRouter / Ollama Cloud) to elaborate — without touching the public static export.

**Architecture:** Two local processes. The existing Next.js gallery gains a notebook viewer page (`app/topics/[name]/page.tsx`); a small FastAPI backend (`backend/`, port 8077) owns code execution (one persistent Python subprocess per notebook) and LLM streaming. The static export keeps `output: "export"`; viewer pages render statically as a reading view, and interactive calls degrade gracefully with a "run `make dev-local`" hint when the backend is absent.

**Tech Stack:** Next.js 16 (App Router, static export), React 19, Tailwind 4, `marked` for markdown; Python 3.12+/uv, FastAPI, uvicorn, httpx; `pytest` for backend tests, `vitest` + `@testing-library/react` (jsdom) for frontend smoke tests.

**Spec:** `docs/superpowers/specs/2026-10-17-interactive-notebook-viewer-design.md` — the plan argues from this spec; read both.

## Global Constraints

- Python tooling is `uv` with `pyproject.toml` as the single source of metadata; new Python deps go in a `interactive` extra (`uv sync --extra interactive`), pytest in `[dependency-groups]` `dev`.
- Public static export must keep building: `make site` (`next build` with `output: "export"`, `trailingSlash: true`) must pass unchanged. POST route handlers cannot exist under `output: "export"`, so the browser calls FastAPI directly.
- FastAPI listens on `127.0.0.1:8077` and its CORS allows only `localhost`/`127.0.0.1` origins (the backend executes arbitrary code; a random website in the author's browser must not be able to trigger it).
- Cell execution timeout: 60 s (spec). Tests override to seconds so they stay fast.
- LLM env keys: `OPENROUTER_API_KEY`, `OLLAMA_API_KEY`; backend base URLs fixed: OpenRouter `https://openrouter.ai/api/v1/chat/completions`, Ollama Cloud `https://ollama.com/v1/chat/completions`.
- `ILLUSTRATIVE` marker: cell source containing `# ILLUSTRATIVE` (matches `lib/notebooks.ts` and the audit script). These cells render read-only with a badge and are refused by `/execute`.
- Repo style: Phosphor icons, Tailwind classes in JSX plus semantic classes in `app/globals.css`; follow the existing pages' markup patterns.
- CLAUDE.md: feature branch (`feat/...`), PR at the end, `PROGRESS.md` updated, README updated.
- Elaborate system prompt (fixed string backend-side): "You are a data engineering tutor. Expand the notebook section the student is reading: teach the concept with one worked example and the common pitfalls."

## Review Focus

1. **Cross-origin execution trigger.** The backend runs arbitrary Python on the author's machine. A non-localhost origin must be denied; the server must bind `127.0.0.1`. Test: CORS preflight from an unknown origin is rejected (Task 2).
2. **Kernel state across cells.** A variable defined in one Run must exist in the next Run of the same notebook (that is the promise a reader relies on). Test: two sequential executes share a namespace (Task 1).
3. **Interrupted run leaves a usable kernel.** A cell that times out is interrupted (SIGINT) and the *next* execute succeeds without a kernel restart. Test: timeout, then run again (Task 1).
4. **Provider failure mid-stream.** Network error or non-200 from the LLM provider surfaces as an SSE `{"error": ...}` event and the chat input stays usable — no dead silent panel. Test: MockTransport returning 500 (Task 3).
5. **Malformed notebook cells.** A cell with no `source` (or a notebook hand-edited badly) must not crash the viewer or the parser. Test: cell without source is treated as empty (Task 4).
6. **Huge or non-UTF8 output.** PySpark can emit hundreds of thousands of stderr lines; output is truncated backend-side (20 000 chars per stream with a marker) so the page doesn't choke. Test: truncation marker present (Task 2).

---

### Task 1: Python deps + kernel subprocess protocol

**Files:**
- Modify: `pyproject.toml` (add `interactive` extra + `dev` dependency-group)
- Modify: `Makefile` (add `chat-install` target)
- Create: `backend/__init__.py`
- Create: `backend/kernel_proc.py`
- Create: `backend/kernel.py`
- Test: `backend/tests/test_kernel_proc.py` (+ `backend/tests/__init__.py`)

**Interfaces:**
- Produces: `Kernel` in `backend/kernel.py` —
  ```python
  class ExecResult(TypedDict):
      status: Literal["ok", "error", "interrupted"]
      stdout: str          # truncated to MAX_OUTPUT_CHARS (20000) with "\n... [truncated]" marker
      stderr: str
      traceback: str | None
      elapsed_seconds: float

  class Kernel:
      def __init__(self, timeout_seconds: float = 60.0) -> None
      def execute(self, code: str) -> ExecResult    # blocked run > timeout → SIGINT interrupt → status "interrupted"
      def alive(self) -> bool                       # subprocess still running
      def reset(self) -> None                       # kill + fresh subprocess (empty namespace)
      def close(self) -> None
  ```
  Protocol (line-delimited JSON on stdio of `backend/kernel_proc.py`): request `{"id": <int>, "code": <str>}` → response `{"id", "status", "stdout", "stderr", "traceback", "elapsed_seconds"}`; `KeyboardInterrupt` inside a run replies `status: "interrupted"`. Namespace persists across requests (one `dict`, `exec(code, ns)`).

- [ ] **Step 1: Write the failing tests** — one test class with: (a) state persistence: execute `x = 40`, then `print(x + 2)` → second result stdout `"42\n"`; (b) stdout/stderr capture: `print("out"); import sys; print("err", file=sys.stderr)`; (c) error traceback: execute `1 / 0` → `status == "error"`, traceback contains `ZeroDivisionError`; (d) timeout then recovery with `Kernel(timeout_seconds=0.5)`: execute `import time; time.sleep(5)` → `status == "interrupted"`, then execute `print("alive")` → status `"ok"` (no restart); (e) output truncation: `print("a" * 30000)` → stdout length ≤ 20000 and marker present.
- [ ] **Step 2: Run** `uv run --extra interactive pytest backend/tests/test_kernel_proc.py -v` — Expected: FAIL with `ModuleNotFoundError: backend.kernel`
- [ ] **Step 3: Implement** `kernel_proc.py` (loop: read JSON line → `exec` into persistent namespace with `contextlib.redirect_stdout/redirect_stderr` → write one JSON response line, flush) and `kernel.py` (spawn `sys.executable <kernel_proc.py>`; `execute` writes request, `json.loads`es the response line with a `threading`-based wait, on timeout `send_signal(SIGINT)`, on dead process return `status: "error"` with traceback `"kernel process exited"`).
- [ ] **Step 4: Run** `uv run --extra interactive pytest backend/tests -v` — Expected: PASS
- [ ] **Step 5: Commit** `feat: kernel subprocess with persistent namespace and interrupt`

### Task 2: FastAPI `/execute` + session registry

**Files:**
- Create: `backend/sessions.py`
- Create: `backend/main.py`
- Test: `backend/tests/test_execute_endpoint.py`

**Interfaces:**
- Consumes: `Kernel` (Task 1), `ExecResult`.
- Produces:
  ```python
  # backend/sessions.py
  def get_kernel(notebook: str) -> Kernel          # lazily created per notebook id; dead kernel replaced lazily
  def restart_kernel(notebook: str) -> Kernel
  def load_cell_source(notebook_path: str, index: int) -> tuple[str, bool]
      # (source, is_illustrative) from a repo-relative .ipynb path; raises KeyError if index out of range
  ```
  HTTP `POST /execute` body `{"notebook": "<slug>", "path": "<repo .ipynb path>"} ` plus exactly one of `{"cell_index": <int>}` or `{"code": "<str>"}`.
  Response `200` always (execution results travel in the body): `{"status": "ok"|"error"|"timeout"|"busy"|"illustrative"|"crashed", "stdout", "stderr", "traceback": str|null, "elapsed_seconds": float|null}`. `path` outside `notebooks/` → `404`. `cell_index` out of range or `path` unparseable → `400`. `POST /reset {"notebook": "<slug>"}` → `{"status": "ok"}`. `GET /health` → `{"status": "ok"}`.

- [ ] **Step 1: Write the failing tests** (FastAPI `TestClient`, each test uses notebook `notebooks/topics/spark.ipynb`): (a) good cell: `POST /execute {"notebook": "t1", "path": "notebooks/topics/spark.ipynb", "cell_index": <first non-ILLUSTRATIVE code cell index>}` → `status == "ok"`; (b) illustrative: pick an index whose source contains `# ILLUSTRATIVE` → `status == "illustrative"` and kernel not touched; (c) ad-hoc code persists in the session: `/execute {"code": "y = 7"}` then `/execute {"code": "print(y * 2)"}` → stdout `"14\n"`; (d) out-of-range index → `400`; (e) path outside `notebooks/` → `404`; (f) kernel crash recovery: get the session's kernel via `get_kernel`, `kill()` its subprocess, then `/execute` again → `status == "ok"` on a fresh kernel (outputs from previous cells stay in the browser; nothing on the server claims otherwise); (g) CORS: `OPTIONS` preflight with `Origin: http://evil.example` → no `Access-Control-Allow-Origin` header, and with `Origin: http://localhost:3000` → header present.
- [ ] **Step 2: Run** `uv run --extra interactive pytest backend/tests/test_execute_endpoint.py -v` — Expected: FAIL (`backend.main` missing)
- [ ] **Step 3: Implement** `sessions.py` (registry `dict[str, Kernel]`; `load_cell_source` parses the notebook JSON, joins `cell["source"]` lists like `lib/notebooks.ts` does, illustrative = `# ILLUSTRATIVE` in source; missing source key → empty string) and `main.py` (FastAPI, `CORSMiddleware` with `allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]`, explicit methods; `/execute` routes per the mapping above; each session guards execution with a `threading.Lock` acquired non-blocking — when a run already holds it, reply `status: "busy"` immediately; sync `def` endpoints so FastAPI's threadpool does not block the event loop).
- [ ] **Step 4: Run** `uv run --extra interactive pytest backend/tests -v` — Expected: PASS (Task 1 tests still green)
- [ ] **Step 5: Commit** `feat: /execute endpoint with per-notebook kernels`

### Task 3: Chat config + `/chat` SSE endpoint

**Files:**
- Modify: `.gitignore` (add `chat.config.yml`)
- Create: `chat.config.example.yml`
- Create: `backend/chat_config.py`
- Create: `backend/llm.py`
- Modify: `backend/main.py` (add endpoints)
- Test: `backend/tests/test_chat.py`

**Interfaces:**
- Consumes: nothing from Tasks 1–2.
- Produces:
  ```python
  # backend/chat_config.py
  PROVIDER_BASE_URLS: dict[str, str]  # {"openrouter": "https://openrouter.ai/api/v1/chat/completions",
                                      #  "ollama": "https://ollama.com/v1/chat/completions"}
  class MissingKeyError(Exception):   # .env_var attribute, message names the env var
  class ChatSettings(BaseModel):        # pydantic model: provider, model, max_tokens, temperature, api_key, base_url
  def load_chat_settings(root: Path) -> ChatSettings
      # chat.config.yml in root if present (provider, model, max_tokens, temperature); env overrides CHAT_PROVIDER/CHAT_MODEL;
      # key from OPENROUTER_API_KEY / OLLAMA_API_KEY; raises MissingKeyError when absent

  # backend/llm.py
  make_client() -> httpx.AsyncClient                    # module-level factory, monkeypatch target in tests
  def elaborate_messages(section_markdown: str, context_cells: list[str]) -> list[dict]
  def chat_messages(notebook_title: str, outline: list[str], visible_section: str,
                    history: list[dict], message: str) -> list[dict]
  async def stream_llm(settings: ChatSettings, messages: list[dict]) -> AsyncIterator[dict]
      # yields {"delta": str}; on HTTP/non-200 or network failure yields {"error": str} then stops;
      # parses provider SSE ("data: {json}\n\n", "[DONE]" sentinel, OpenAI shape: choices[0].delta.content)
  ```
  HTTP `POST /chat` (SSE `text/event-stream`) body `{"mode": "elaborate"|"chat", "settings"? omitted, "section_markdown": str, "context_cells": [str], "notebook_title": str, "outline": [str], "visible_section": str, "history": [{"role", "content"}], "message": str}`. Each event: `data: {"delta": str}\n\n`, terminal `data: {"done": true}\n\n`, or `data: {"error": str}\n\n`. Mode `elaborate` uses the fixed system prompt from Global Constraints + section markdown + up to 3 cells of context each side. `GET /chat/settings` → `{"provider", "model", "key_present": bool}`. Missing key → HTTP `400` with detail naming the env var.

- [ ] **Step 1: Write the failing tests**: (a) provider resolution: `load_chat_settings` with a temp `chat.config.yml` (`provider: ollama, model: gpt-oss-large`) → base_url == ollama URL, and env override `CHAT_MODEL` wins over file; (b) missing key: no env keys set → `MissingKeyError` with `env_var == "OPENROUTER_API_KEY"`; (c) `/chat` streaming via `TestClient` + `httpx.MockTransport` fake that emits one OpenAI-format SSE chunk then `[DONE]` → assembled text matches; (d) provider 500 → SSE payload contains an `error` event mentioning the provider; (e) missing key → HTTP `400`, detail contains `OPENROUTER_API_KEY`; (f) `GET /chat/settings` → `key_present` reflects env.
- [ ] **Step 2: Run** `uv run --extra interactive pytest backend/tests/test_chat.py -v` — Expected: FAIL with import error
- [ ] **Step 3: Implement** `chat_config.py`, `llm.py`, and the two endpoints plus the `MissingKeyError` exception handler in `main.py`. Commit `chat.config.example.yml` with `example: openrouter, anthropic/claude-sonnet-4.5`; add `chat.config.yml` to `.gitignore`.
- [ ] **Step 4: Run** `uv run --extra interactive pytest backend/tests -v` — Expected: PASS
- [ ] **Step 5: Commit** `feat: /chat SSE endpoint with provider-agnostic LLM streaming`

### Task 4: Frontend deps + notebook content parsing + markdown

**Files:**
- Modify: `package.json` (dep `marked`; devDeps `vitest`, `@vitejs/plugin-react`, `jsdom`, `@testing-library/react`; script `"test": "vitest run"`)
- Modify: `lib/notebooks.ts` (export `getNotebookSummaries(): NotebookSummary[]`)
- Create: `lib/markdown.ts`
- Create: `lib/notebook-content.ts`
- Create: `vitest.config.ts`
- Test: `lib/notebook-content.test.ts`

**Interfaces:**
- Produces:
  ```typescript
  // lib/markdown.ts
  export function renderMarkdown(md: string): string   // marked.parse inline mode, sanitized only by marked's defaults

  // lib/notebook-content.ts
  export type NotebookSectionBlock =
    | { kind: "markdown"; source: string; html: string }
    | { kind: "code"; source: string; illustrative: boolean; cellIndex: number };
  export type NotebookSection = { id: string; heading: string; blocks: NotebookSectionBlock[] };
  export type NotebookPage =
    { slug: string; repoPath: string; title: string; sections: NotebookSection[] };
  export function readNotebookPage(summary: NotebookSummary): NotebookPage
      // reads the .ipynb at summary.repoPath; blocks before the first "## " heading form the preamble section
      // (id "intro", heading = notebook title); "## " heading starts a new section, id = slugified heading;
      // missing/absent cell source → empty string; "# ILLUSTRATIVE" marker → illustrative: true
  ```
- [ ] **Step 1: Write the failing tests** (vitest, node env, build a small fake `.ipynb` JSON in `os.tmpdir()`): (a) first `##` heading splits sections and assigns ids; (b) blocks before the first heading land in the `intro` section; (c) a code cell's `cellIndex` is its index in the notebook's `cells` array; (d) cell with no `source` field renders as empty; (e) `# ILLUSTRATIVE` cell flagged; (f) `renderMarkdown` renders a markdown table into `<table>` and a fenced code block into `<pre>`; (g) a heading with the same text as another yields a distinct id (suffix index).
- [ ] **Step 2: Run** `npm test` — Expected: FAIL (files missing)
- [ ] **Step 3: Implement** `lib/markdown.ts` (marked), `lib/notebook-content.ts`, and export `getNotebookSummaries` in `lib/notebooks.ts`.
- [ ] **Step 4: Run** `npm test` — Expected: PASS
- [ ] **Step 5: Commit** `feat: notebook content parser and markdown rendering with vitest`

### Task 5: Viewer page + notebook viewer component

**Files:**
- Create: `lib/interactive-api.ts`
- Create: `app/topics/[name]/page.tsx`
- Create: `components/notebook-viewer.tsx`
- Modify: `components/NotebookCard.tsx` (add "Read" link to `/topics/<slug>`)
- Test: `components/notebook-viewer.test.tsx` (jsdom)

**Interfaces:**
- Consumes: `readNotebookPage` (Task 4), `GetNotebookSummaries` (Task 4).
- Produces:
  ```typescript
  // lib/interactive-api.ts
  export const BACKEND_URL: string        // process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8077"
  export type ExecResponse = { status: "ok"|"error"|"timeout"|"busy"|"illustrative"|"crashed";
                              stdout: string; stderr: string; traceback: string|null; elapsed_seconds: number|null }
  export function executeCell(notebook: string, path: string, cellIndex: number | null, code: string | null)
      // POST ${BACKEND_URL}/execute; network failure → { status: "crashed", ... with traceback hinting "make dev-local" }
  export function streamChat(body: ChatBody, onDelta: (text: string) => void): Promise<string | null>
      // POST ${BACKEND_URL}/chat, reads the SSE stream; returns the final error string (null = clean finish)
      // ChatBody = { mode: "elaborate"|"chat"; section_markdown?: string; context_cells?: string[];
      //              notebook_title: string; outline: string[]; visible_section?: string;
      //              history?: { role, content }[]; message?: string }
  export function fetchChatSettings(): Promise<{ provider: string; model: string; key_present: boolean }>
  ```
  Component `<NotebookViewer page={NotebookPage} />` (client): every markdown section gets an Elaborate button (Phosphor `Sparkle`) that opens a collapsible panel below the section and streams into it; every code cell renders as an editable monospace `<textarea>` with a Run button (Phosphor `Play`), an output area (stdout/stderr + red-framed traceback), and an `ILLUSTRATIVE` badge instead of Run when `illustrative: true`; kernel state hint shown under the first cell ("kernel persists top-to-bottom; `POST /reset` via reload").
  Page `app/topics/[name]/page.tsx`: `generateStaticParams` from `getNotebookSummaries()`, `params: Promise<{ name: string }>`, `notFound()` for unknown slugs, `SiteHeader` + TOC nav (from `page.sections` headings) + `<NotebookViewer>` + `<ChatPanel notebookTitle outline />` (Task 6 placeholder until Task 6 lands — render nothing instead: the page imports ChatPanel in Task 6).

- [ ] **Step 1: Write the failing component test** (jsdom; pass a one-section page with a markdown block, one code cell, one illustrative cell): (a) markdown HTML is present (`table` element), (b) Run button exists on the editable cell and is absent on the illustrative one which shows the badge text `ILLUSTRATIVE`, (c) clicking Run with `fetch` mocked to return a 200 `{status: "ok", stdout: "hi"}` shows `"hi"` in the output area, (d) when `fetch` rejects, the output area shows the `make dev-local` hint.
- [ ] **Step 2: Run** `npm test` — Expected: component test FAIL (module missing)
- [ ] **Step 3: Implement** `lib/interactive-api.ts`, `components/notebook-viewer.tsx`, `app/topics/[name]/page.tsx`, and the NotebookCard link.
- [ ] **Step 4: Run** `npm test && npm run lint` — Expected: PASS
- [ ] **Step 5: Run** `npm run build` — Expected: PASS (static export builds; confirms no POST route handler leaked into the tree)
- [ ] **Step 6: Commit** `feat: notebook viewer page with run + elaborate cells`

### Task 6: Chat panel

**Files:**
- Create: `components/chat-panel.tsx`
- Modify: `app/topics/[name]/page.tsx` (render `<ChatPanel>`)
- Test: `components/chat-panel.test.tsx`

**Interfaces:**
- Consumes: `streamChat`, `fetchChatSettings` (Task 5), `NotebookPage` (Task 4).
- Produces: `<ChatPanel notebookTitle={string} outline={string[]} visibleSection={string} />` (client): message list (user/assistant roles), input, Send button (Phosphor `PaperPlaneTilt`), streaming assistant messages via `streamChat` with `mode: "chat"` and history from `useState` (not persisted server-side); a small settings popover (Phosphor `Sliders`) showing provider/model from `fetchChatSettings` with a `key not set` warning when `key_present` is false. Empty history is allowed (Review Focus 4: provider errors surface as an error bubble, input stays enabled).

- [ ] **Step 1: Write the failing test** (jsdom, `fetch` mocked): (a) renders input and Send; (b) sending a message with a mocked SSE stream appends an assistant bubble whose text matches the streamed deltas; (c) when the stream yields an `error` event, an error bubble names the error and the input is still enabled.
- [ ] **Step 2: Run** `npm test` — Expected: FAIL (module missing)
- [ ] **Step 3: Implement** `components/chat-panel.tsx` and mount it in the page.
- [ ] **Step 4: Run** `npm test && npm run lint && npm run build` — Expected: PASS
- [ ] **Step 5: Commit** `feat: per-page chat panel with SSE streaming and settings popover`

### Task 7: `make dev-local` + docs + full verification

**Files:**
- Modify: `Makefile` (add `dev-local`, `test`)
- Create: `scripts/dev-local.sh`
- Modify: `README.md` (interactive section: setup, `make chat-install`, `make dev-local`, env keys, `chat.config.yml` example)
- Create: `PROGRESS.md` (root, per CLAUDE.md template)

**Interfaces:**
- Consumes: everything above.
- Produces: `make dev-local` — starts `uv run uvicorn backend.main:app --host 127.0.0.1 --port 8077` and `npm run dev -- --port 3000` concurrently via `scripts/dev-local.sh` (bash, `trap` kills both on exit, waits on PIDs); `make test` — `npm test` + `uv run --extra interactive pytest backend/tests -q`.

- [ ] **Step 1: Create** `scripts/dev-local.sh` and Make targets.
- [ ] **Step 2: Run** `bash -n scripts/dev-local.sh` — Expected: no output (syntax OK)
- [ ] **Step 3: Run the full verification loop**: `make test` and `make validate` (audit + sync-check + notebooks-check + lint + site build) — Expected: all PASS; static export unchanged in behavior.
- [ ] **Step 4: Update** `README.md` and create `PROGRESS.md` (Current Status / Completed / In Progress / Next Steps / Blockers).
- [ ] **Step 5: Commit** `feat: dev-local orchestration and docs`

## Rulings recorded in this plan (for the executor's ledger)

- `Ruling: browser → FastAPI direct, no Next /api/* route handlers` — the spec's architecture diagram shows `/api/*` route handlers, but `output: "export"` forbids POST route handlers at build time and the spec's own hard constraint is "the public static export continues to build exactly as today". Direct browser→FastAPI calls with a localhost-restricted CORS policy honor both; cost if wrong: same-origin proxying would need a real (non-export) server mode later.
- `Ruling: interrupt = SIGINT to the kernel subprocess` — a plain `exec` kernel cannot cancel a native (PySpark/JVM) call; SIGINT covers Python-level code, and a still-busy kernel answers `busy` instead of hanging. Cost if wrong: a wedged JVM call needs `POST /reset`, which the UI reaches via page state.
- `Ruling: chat history stays in React state` — spec marks `localStorage` optional; skipping it keeps Task 6 small. Cost if wrong: reloads lose chat (acceptable for a local study tool).
- `Ruling: viewer pages ship in the static export as a reading view` — the spec says the export is "not disturbed"; these pages add value statically and degrade with a hint when the backend is absent. Cost if wrong: a public reader sees Run buttons that explain themselves instead of a 404.