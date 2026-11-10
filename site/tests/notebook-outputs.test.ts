import { describe, expect, it } from "vitest";
import { attachOutputs, parseNotebook, parseOutput, type RawNotebook } from "../lib/notebook-parse";

const SOURCE: RawNotebook = {
  cells: [
    { id: "t", cell_type: "markdown", source: "# Demo\n\nIntro paragraph long enough to count." },
    { id: "s", cell_type: "code", source: "# Setup: installs packages\nprint('ready')" },
    { id: "a", cell_type: "code", source: "print('hello')" },
    { id: "b", cell_type: "code", source: "1 + 1" },
    { id: "c", cell_type: "code", source: "x = 1" },
  ],
};

describe("parseOutput", () => {
  it("reads streams and keeps stderr apart", () => {
    expect(parseOutput({ output_type: "stream", name: "stdout", text: ["a\n", "b\n"] })).toEqual({
      type: "text",
      stream: "stdout",
      text: "a\nb\n",
    });
    expect(parseOutput({ output_type: "stream", name: "stderr", text: "warn" })).toMatchObject({ stream: "stderr" });
  });

  it("drops blank streams and outputs with nothing to show", () => {
    expect(parseOutput({ output_type: "stream", text: "\n" })).toBeNull();
    expect(parseOutput({ output_type: "display_data", data: { "text/html": "<b>x</b>" } })).toBeNull();
  });

  it("prefers an image over its text fallback", () => {
    const output = parseOutput({ output_type: "display_data", data: { "image/png": "iVBO\nRw==", "text/plain": "<Figure>" } });
    expect(output).toEqual({ type: "image", src: "data:image/png;base64,iVBORw==" });
  });

  it("reads results and errors", () => {
    expect(parseOutput({ output_type: "execute_result", data: { "text/plain": "2" } })).toEqual({
      type: "text",
      stream: "result",
      text: "2",
    });
    expect(parseOutput({ output_type: "error", ename: "ValueError", evalue: "bad" })).toEqual({
      type: "error",
      name: "ValueError",
      message: "bad",
    });
  });
});

describe("attachOutputs", () => {
  const executed: RawNotebook = {
    cells: [
      { id: "s", cell_type: "code", source: "# Setup: installs packages\nprint('ready')", outputs: [{ output_type: "stream", text: "ready\n" }] },
      { id: "a", cell_type: "code", source: "print('hello')", outputs: [{ output_type: "stream", name: "stdout", text: "hello\n" }] },
      { id: "b", cell_type: "code", source: "1 + 2", outputs: [{ output_type: "execute_result", data: { "text/plain": "3" } }] },
    ],
  };
  const cells = attachOutputs(parseNotebook(SOURCE, "demo").cells, executed);
  const byId = Object.fromEntries(cells.map((cell) => [cell.id, cell.outputs]));

  it("puts outputs under the matching cell", () => {
    expect(byId.a).toEqual([{ type: "text", stream: "stdout", text: "hello\n" }]);
  });

  it("skips a cell whose source changed since the run", () => {
    expect(byId.b).toEqual([]);
  });

  it("never shows setup output, and leaves cells missing from the run empty", () => {
    expect(byId.s).toEqual([]);
    expect(byId.c).toEqual([]);
  });

  it("starts every parsed cell with no outputs", () => {
    expect(parseNotebook(SOURCE, "demo").cells.every((cell) => cell.outputs.length === 0)).toBe(true);
  });
});
