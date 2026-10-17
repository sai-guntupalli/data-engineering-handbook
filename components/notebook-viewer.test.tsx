// @vitest-environment jsdom
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { StrictMode } from "react";
import { afterAll, afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";

import { readNotebookPage, type NotebookPage } from "../lib/notebook-content";
import { BACKEND_URL } from "../lib/interactive-api";
import { NotebookViewer } from "./notebook-viewer";

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "notebook-viewer-"));

afterAll(() => {
  fs.rmSync(tempRoot, { recursive: true, force: true });
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

/** A summary with all card statistics zeroed; the parser only needs repoPath (and title). */
function pageFromCells(title: string, cells: object[]): NotebookPage {
  const file = path.join(tempRoot, "fake.ipynb");
  fs.writeFileSync(file, JSON.stringify({ cells: cells.map((cell) => ({ metadata: {}, ...cell })) }));
  return readNotebookPage({
    repoPath: file,
    slug: "fake",
    title,
    description: "",
    markdownCells: 0,
    codeCells: 0,
    assertCount: 0,
    tryItBlocks: 0,
    illustrativeCells: 0,
    readingMinutes: 0,
    mergedCodeCells: 0,
    mergedAsserts: 0,
    githubHref: "",
    colabHref: "",
  });
}

/** One section with a markdown table, an editable code cell and an illustrative one. */
function oneSectionPage(): NotebookPage {
  return pageFromCells("Viewer Fixture", [
    { cell_type: "markdown", source: "# Viewer Fixture" },
    {
      cell_type: "markdown",
      source: "| a | b |\n|---|---|\n| 1 | 2 |\n",
    },
    { cell_type: "code", source: ["print(\"counting\")"] },
    { cell_type: "code", source: ["# ILLUSTRATIVE", "\n", "boto3.client(\"s3\")"] },
  ]);
}

/** Two-headed sections so heading anchors, the kernel-hint placement and the
 *  elaborate context cells are exercised. */
function sectionsPage(): NotebookPage {
  return pageFromCells("Viewer Fixture", [
    { cell_type: "markdown", source: "# Viewer Fixture\n\nIntro." },
    { cell_type: "markdown", source: "## Load" },
    { cell_type: "code", source: "print(\"a\")" },
    { cell_type: "markdown", source: "Load notes." },
    { cell_type: "markdown", source: "## Notes" },
    { cell_type: "code", source: "print(\"b\")" },
    { cell_type: "markdown", source: "Note detail." },
  ]);
}

const execResult = (stdout: string) => ({
  ok: true,
  status: 200,
  json: async () => ({
    status: "ok",
    stdout,
    stderr: "",
    traceback: null,
    elapsed_seconds: 0.02,
  }),
});

/** A fetch mock with the signature the viewer calls it with, so mock.calls
 *  stay fully typed. */
const mockFetch = (stdout = "hi") => vi.fn(async (_url: string, _init: RequestInit) => execResult(stdout));

/** A fetch mock answering one SSE response with the given event chunks. */
const mockSse = (chunks: string[]) =>
  vi.fn(async (_url: string, _init: RequestInit) => sseResponse(chunks, "text/event-stream"));

/** The JSON body of one recorded call (any mock shape; the init is the viewer's). */
function sentBody(mock: { mock: { calls: unknown[][] } }, call = 0): unknown {
  const init = mock.mock.calls[call]![1] as RequestInit;
  return JSON.parse(String(init.body));
}

/** A fake SSE response whose body hands out the chunks one read() at a time. */
function sseResponse(chunks: string[], contentType: string) {
  const encode = (text: string) => Uint8Array.from(text, (char) => char.charCodeAt(0));
  let index = 0;
  return {
    ok: true,
    status: 200,
    headers: new Headers({ "content-type": contentType }),
    body: {
      getReader: () => ({
        read: async () =>
          index < chunks.length
            ? { done: false, value: encode(chunks[index++]) }
            : { done: true, value: undefined },
      }),
    },
  };
}

describe("NotebookViewer", () => {
  it("fires exactly one kernel reset for the page on mount, even under React StrictMode's double-invoke", () => {
    const fetch = mockFetch();
    vi.stubGlobal("fetch", fetch);
    render(
      <StrictMode>
        <NotebookViewer page={oneSectionPage()} />
      </StrictMode>,
    );

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch.mock.calls[0]![0]).toBe(`${BACKEND_URL}/reset`);
    expect(sentBody(fetch)).toEqual({ notebook: "fake" });
  });

  it("renders markdown HTML, a Run button on the editable cell, and only the ILLUSTRATIVE badge on the read-only one", () => {
    const { container } = render(<NotebookViewer page={oneSectionPage()} />);
    expect(container.querySelector("table")).not.toBeNull();

    const runButtons = screen.getAllByRole("button", { name: /^Run$/ });
    expect(runButtons).toHaveLength(1);

    const badge = screen.getByText("ILLUSTRATIVE");
    expect(badge).not.toBeNull();
    const illustrativeCell = badge.closest(".nb-cell") as HTMLElement;
    expect(within(illustrativeCell).queryByRole("button")).toBeNull();
    expect(illustrativeCell.querySelector("textarea")).not.toBeNull();
  });

  it("runs the untouched cell by its index and shows captured stdout", async () => {
    const fetch = mockFetch();
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={oneSectionPage()} />);
    fetch.mockClear(); // ignore the mount-reset probe

    fireEvent.click(screen.getByRole("button", { name: /^Run$/ }));

    expect(await screen.findByText("hi")).not.toBeNull();
    expect(fetch).toHaveBeenCalledTimes(1);
    const init = fetch.mock.calls[0]![1];
    expect(fetch.mock.calls[0]![0]).toBe(`${BACKEND_URL}/execute`);
    expect(init.method).toBe("POST");
    expect(sentBody(fetch)).toEqual({
      notebook: "fake",
      path: expect.any(String),
      cell_index: 2,
      code: null,
    });
  });

  it("runs an edited cell as ad-hoc code instead of its index", async () => {
    const fetch = mockFetch("edited");
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={oneSectionPage()} />);

    const textarea = screen.getByLabelText(/editable code cell/i) as HTMLTextAreaElement;
    expect(textarea.value).toBe("print(\"counting\")");
    fetch.mockClear(); // ignore the mount-reset probe
    fireEvent.change(textarea, { target: { value: "print(\"edited\")" } });
    fireEvent.click(screen.getByRole("button", { name: /^Run$/ }));

    expect(await screen.findByText("edited")).not.toBeNull();
    expect(sentBody(fetch)).toEqual({
      notebook: "fake",
      path: expect.any(String),
      cell_index: null,
      code: "print(\"edited\")",
    });
  });

  it("shows the make dev-local hint when the backend is unreachable", async () => {
    const fetch = vi.fn(async (_url: string, _init: RequestInit) => {
      throw new TypeError("fetch failed");
    });
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={oneSectionPage()} />);

    fireEvent.click(screen.getByRole("button", { name: /^Run$/ }));

    expect(await screen.findByText(/make dev-local/)).not.toBeNull();
  });

  it("streams an elaboration into a collapsible panel under the section", async () => {
    const fetch = mockSse([
      "data: {\"delta\": \"Hello\"}\n\n",
      "data: {\"delta\": \" world\"}\n\n",
      "data: {\"done\": true}\n\n",
    ]);
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={oneSectionPage()} />);
    fetch.mockClear(); // ignore the mount-reset probe

    fireEvent.click(screen.getByRole("button", { name: /Elaborate/ }));

    expect(await screen.findByText(/Hello world/)).not.toBeNull();
    expect(fetch.mock.calls[0]![0]).toBe(`${BACKEND_URL}/chat`);
    const body = sentBody(fetch) as {
      mode: string;
      notebook_title: string;
      section_markdown: string;
      context_cells: string[];
    };
    expect(body.mode).toBe("elaborate");
    expect(body.notebook_title).toBe("Viewer Fixture");
    expect(body.section_markdown).toContain("| a | b |");
    expect(body.context_cells).toEqual([]);
  });

  it("sends up to three surrounding cell sources with an elaborate request", async () => {
    const fetch = mockSse(["data: {\"delta\": \"ok\"}\n\n", "data: {\"done\": true}\n\n"]);
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={sectionsPage()} />);

    // Sections render in order: intro, load, notes — the middle one is "load".
    const buttons = screen.getAllByRole("button", { name: /Elaborate/ });
    expect(buttons).toHaveLength(3);
    fetch.mockClear(); // ignore the mount-reset probe
    fireEvent.click(buttons[1]!);

    expect(await screen.findByText("ok")).not.toBeNull();
    const body = sentBody(fetch) as { context_cells: string[]; outline: string[] };
    expect(body.context_cells).toEqual([
      "# Viewer Fixture\n\nIntro.",
      "print(\"b\")",
      "Note detail.",
    ]);
    expect(body.outline).toEqual(["Viewer Fixture", "Load", "Notes"]);
  });

  it("surfaces a stream error inside the elaborate panel", async () => {
    const fetch = mockSse(["data: {\"error\": \"openrouter request failed with HTTP 500\"}\n\n"]);
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={oneSectionPage()} />);

    fireEvent.click(screen.getByRole("button", { name: /Elaborate/ }));

    expect(await screen.findByText(/openrouter request failed with HTTP 500/)).not.toBeNull();
  });

  it("re-requests the elaboration after a failed stream instead of replaying the error", async () => {
    // First /chat errored, second /chat answers properly.
    const responses = [
      ["data: {\"error\": \"openrouter request failed with HTTP 500\"}\n\n"],
      ["data: {\"delta\": \"Second\"}\n\n", "data: {\"done\": true}\n\n"],
    ];
    let responseIndex = 0;
    const fetch = vi.fn(async (url: string, _init: RequestInit) =>
      String(url).endsWith("/chat")
        ? sseResponse(responses[responseIndex++] ?? [], "text/event-stream")
        : execResult("ok", ""),
    );
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={oneSectionPage()} />);
    fetch.mockClear(); // ignore the mount-reset probe

    fireEvent.click(screen.getByRole("button", { name: /Elaborate/ }));
    expect(await screen.findByText(/openrouter request failed with HTTP 500/)).not.toBeNull();

    // The failed stream is not cached: the re-click re-requests.
    fireEvent.click(screen.getByRole("button", { name: /Elaborate/ }));
    expect(await screen.findByText("Second")).not.toBeNull();
    const chatCalls = fetch.mock.calls.filter(([url]) => String(url).endsWith("/chat"));
    expect(chatCalls).toHaveLength(2);
  });

  it("names the missing env key when the chat request is refused", async () => {
    const fetch = vi.fn(async (_url: string, _init: RequestInit) => ({
      ok: false,
      status: 400,
      json: async () => ({ detail: "OPENROUTER_API_KEY is not set" }),
    }));
    vi.stubGlobal("fetch", fetch);
    render(<NotebookViewer page={oneSectionPage()} />);

    fireEvent.click(screen.getByRole("button", { name: /Elaborate/ }));

    expect(await screen.findByText(/OPENROUTER_API_KEY/)).not.toBeNull();
  });

  it("anchors each section with its id and shows the kernel hint once, under the first code cell", () => {
    const { container } = render(<NotebookViewer page={sectionsPage()} />);

    expect(container.querySelector("section#intro")).not.toBeNull();
    const headings = screen.getAllByRole("heading", { level: 2 });
    expect(headings.map((heading) => heading.textContent)).toEqual(["Load", "Notes"]);
    expect(headings[0].closest("section")?.id).toBe("load");
    expect(headings[1].closest("section")?.id).toBe("notes");

    const hint = screen.getAllByText(/kernel persists top-to-bottom/i);
    expect(hint).toHaveLength(1);
    const hintedCell = hint[0].closest(".nb-cell") as HTMLElement;
    const hintedTextarea = hintedCell.querySelector("textarea") as HTMLTextAreaElement;
    expect(hintedTextarea.value).toBe("print(\"a\")");
  });
});
