/** Browser → FastAPI client for the interactive viewer (backend/main.py, :8077).
 *
 *  The static export cannot host POST route handlers, so the browser calls the
 *  local backend directly (CORS-restricted to the dev origin). `make dev-local`
 *  (Task 7) starts it; every failure mode degrades to something the viewer can
 *  show inline instead of throwing into the console.
 */

export const BACKEND_URL: string = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8077";

/** One /execute result; mirrors backend/kernel.py's ExecResult mapped by
 *  backend/main.py ("interrupted" arrives here as "timeout"). */
export type ExecResponse = {
  status: "ok" | "error" | "timeout" | "busy" | "illustrative" | "crashed";
  stdout: string;
  stderr: string;
  traceback: string | null;
  elapsed_seconds: number | null;
};

export type ChatMessage = { role: string; content: string };

/** One /chat request; both modes share the body, each uses its own subset. */
export type ChatBody = {
  mode: "elaborate" | "chat";
  section_markdown?: string;
  context_cells?: string[];
  notebook_title: string;
  outline: string[];
  visible_section?: string;
  history?: ChatMessage[];
  message?: string;
};

export type ChatSettings = { provider: string; model: string; key_present: boolean };

/** FastAPI errors carry {detail}; the missing-key 400 names the env var. */
async function errorDetail(response: Response): Promise<string> {
  try {
    return String(((await response.json()) as { detail?: unknown }).detail ?? "");
  } catch {
    return ""; // A non-JSON error body still gets the status line.
  }
}

/** A result that never ran code: nothing elapsed, no captured output, the
 *  traceback (if any) is the viewer-side hint. */
function terminalExec(status: ExecResponse["status"], traceback: string | null = null): ExecResponse {
  return { status, stdout: "", stderr: "", traceback, elapsed_seconds: null };
}

function offlineTraceback(reason: string): string {
  return (
    `Could not reach the execution backend at ${BACKEND_URL} (${reason}).\n` +
    `Run "make dev-local" to start the backend on :8077, then Reload to reset the kernel.`
  );
}

/**
 * Run one cell (its `cell_index` in the notebook's cells array) or ad-hoc
 * `code` on the notebook's kernel. Exactly one of the two must be non-null
 * (the backend validates the same rule). Network failure returns a "crashed"
 * result whose traceback tells the reader how to start the backend, so the
 * cell's output area explains itself on the static export too.
 */
export async function executeCell(
  notebook: string,
  path: string,
  cellIndex: number | null,
  code: string | null,
): Promise<ExecResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notebook, path, cell_index: cellIndex, code }),
    });
    if (!response.ok) {
      // A refusal (bad path, not a code cell, ...) ran nothing but is not a
      // kernel crash — "crashed" stays reserved for transport failure only.
      const detail = await errorDetail(response);
      return terminalExec(
        "error",
        `The backend refused the request (HTTP ${response.status})${detail ? `: ${detail}` : ""}.`,
      );
    }
    const parsed = (await response.json()) as Partial<ExecResponse>;
    return {
      status: parsed.status ?? "error",
      stdout: parsed.stdout ?? "",
      stderr: parsed.stderr ?? "",
      traceback: parsed.traceback ?? null,
      elapsed_seconds: parsed.elapsed_seconds ?? null,
    };
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    return terminalExec("crashed", offlineTraceback(reason));
  }
}

/**
 * Wipe the notebook's kernel namespace by POSTing `/reset` (the promise the
 * viewer makes: reloading the page also resets, because the mount calls this).
 * Resolves to null when the backend is absent — a reset that cannot happen
 * must not become a visible failure on top of whatever else is on screen.
 */
export async function resetKernel(notebook: string): Promise<ExecResponse | null> {
  try {
    const response = await fetch(`${BACKEND_URL}/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notebook }),
    });
    if (!response.ok) {
      return terminalExec(
        "error",
        `The backend refused the reset (HTTP ${response.status}): ${await errorDetail(response)}.`,
      );
    }
    const parsed = (await response.json()) as Partial<ExecResponse>;
    return { ...terminalExec("ok"), status: parsed.status ?? "ok" };
  } catch {
    return null; // No backend, no kernel to reset; the viewer degrades quietly.
  }
}

/**
 * POST one /chat request and read its SSE stream
 * (``data: {"delta": str}`` / ``{"error": str}`` / ``{"done": true}``). Each
 * delta is handed to `onDelta` as it arrives. Resolves to the error string
 * when the stream reported one (or the transport itself failed) and to null
 * on a clean finish — callers render the error inline, not via an exception.
 */
export async function streamChat(
  body: ChatBody,
  onDelta: (text: string) => void,
): Promise<string | null> {
  let response: Response;
  try {
    response = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
      body: JSON.stringify(body),
    });
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    return `Could not reach the chat backend at ${BACKEND_URL} (${reason}). Run "make dev-local" and try again.`;
  }
  if (!response.ok) {
    const detail = await errorDetail(response);
    return `chat request failed (HTTP ${response.status})${detail ? `: ${detail}` : ""}`;
  }
  if (!response.body) {
    return "chat response carried no stream";
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffered = "";
  for (;;) {
    let batch: ReadableStreamReadResult<Uint8Array>;
    try {
      batch = await reader.read();
    } catch (error) {
      const reason = error instanceof Error ? error.message : String(error);
      return `chat stream interrupted (${reason})`;
    }
    if (batch.done) break;
    buffered += decoder.decode(batch.value, { stream: true });
    const events = buffered.split("\n\n");
    buffered = events.pop() ?? "";
    const error = deliver(events, onDelta);
    if (error !== null) return error;
  }
  return deliver(buffered.split("\n\n"), onDelta);
}

/** Hand a batch of complete SSE events to the caller; null means keep reading. */
function deliver(events: string[], onDelta: (text: string) => void): string | null {
  for (const event of events) {
    const dataLine = event.split("\n").find((line) => line.startsWith("data:"));
    if (!dataLine) continue;
    const payload = dataLine.slice("data:".length).trim();
    if (!payload || payload === "[DONE]") continue;
    let chunk: { delta?: unknown; error?: unknown; done?: unknown };
    try {
      chunk = JSON.parse(payload) as { delta?: unknown; error?: unknown; done?: unknown };
    } catch {
      continue; // non-protocol line inside an otherwise complete event
    }
    if (typeof chunk.error === "string") return chunk.error;
    if (typeof chunk.delta === "string" && chunk.delta) onDelta(chunk.delta);
    if (chunk.done === true) return null;
  }
  return null;
}

/**
 * Read the chat configuration summary (provider/model and whether the API key
 * is set). Network failures propagate — the chat panel decides how a missing
 * backend should look, the same way it handles a missing key.
 */
export async function fetchChatSettings(): Promise<ChatSettings> {
  const response = await fetch(`${BACKEND_URL}/chat/settings`);
  if (!response.ok) {
    throw new Error(`chat settings request failed (HTTP ${response.status})`);
  }
  const parsed = (await response.json()) as Partial<ChatSettings>;
  return {
    provider: parsed.provider ?? "unknown",
    model: parsed.model ?? "unknown",
    key_present: parsed.key_present === true,
  };
}