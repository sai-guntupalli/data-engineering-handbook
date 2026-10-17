import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterAll, describe, expect, it } from "vitest";

import { getNotebookSummaries, type NotebookSummary } from "./notebooks";
import { readNotebookPage } from "./notebook-content";
import { renderMarkdown } from "./markdown";

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "notebook-content-"));

afterAll(() => {
  fs.rmSync(tempRoot, { recursive: true, force: true });
});

/** A summary with all the card statistics zeroed; the parser only needs repoPath (and title). */
function summaryFor(title: string, cells: object[]): NotebookSummary {
  const file = path.join(tempRoot, "fake.ipynb");
  fs.writeFileSync(
    file,
    JSON.stringify({ cells: cells.map((cell) => ({ metadata: {}, ...cell })) }),
  );
  return {
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
  };
}

const markdownCell = (lines: string[]) => ({ cell_type: "markdown", source: lines });
const codeCell = (lines: string[]) => ({ cell_type: "code", source: lines });

describe("readNotebookPage", () => {
  it("splits sections at ## headings with slugified ids", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [
        markdownCell(["# Spark Basics", "\n", "Intro paragraph."]),
        markdownCell(["## Getting Started", "\n", "First steps."]),
        markdownCell(["## Data Frames", "\n", "The API."]),
      ]),
    );
    expect(page.sections.map((section) => section.id)).toEqual([
      "intro",
      "getting-started",
      "data-frames",
    ]);
    expect(page.sections[1].heading).toBe("Getting Started");
    expect(page.title).toBe("Spark Basics");
  });

  it("lands blocks before the first ## heading in the intro section", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [
        markdownCell(["# Spark Basics", "\n", "Intro paragraph."]),
        codeCell(["spark.read"]),
        markdownCell(["## Getting Started"]),
      ]),
    );
    const intro = page.sections[0];
    expect(intro.id).toBe("intro");
    expect(intro.heading).toBe("Spark Basics");
    expect(intro.blocks).toHaveLength(2);
    expect(intro.blocks[0]).toMatchObject({ kind: "markdown", source: "# Spark Basics\nIntro paragraph." });
    expect(intro.blocks[1]).toEqual({
      kind: "code",
      source: "spark.read",
      illustrative: false,
      cellIndex: 1,
    });
  });

  it("keeps the raw cells-array index on code blocks", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [
        markdownCell(["## One"]),
        codeCell(["print(1)"]),
        markdownCell(["## Two"]),
        codeCell(["print(2)"]),
      ]),
    );
    const codeIndexes = page.sections.flatMap((section) =>
      section.blocks.filter((block) => block.kind === "code").map((block) => block.cellIndex),
    );
    expect(codeIndexes).toEqual([1, 3]);
  });

  it("treats a cell with no source field as empty", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [{ cell_type: "markdown" }, { cell_type: "code" }]),
    );
    expect(page.sections[0].blocks).toEqual([
      { kind: "markdown", source: "", html: "" },
      { kind: "code", source: "", illustrative: false, cellIndex: 1 },
    ]);
  });

  it("flags code cells carrying the # ILLUSTRATIVE marker", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [
        codeCell(["# ILLUSTRATIVE", "spark = SparkSession.builder.getOrCreate()"]),
        codeCell(["print(1)"]),
      ]),
    );
    const codeBlocks = page.sections[0].blocks.map((block) =>
      block.kind === "code" ? block.illustrative : undefined,
    );
    expect(codeBlocks).toEqual([true, false]);
  });

  it("keeps a ## line inside a fenced block as ordinary fence content", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [
        markdownCell(["## Config\n", "Set it up:\n", "```python\n", "# setup\n", "## comment\n", "x = 1\n", "```"]),
      ]),
    );
    expect(page.sections.map((section) => section.id)).toEqual(["intro", "config"]);
    expect(page.sections[1].blocks).toHaveLength(1);
    const block = page.sections[1].blocks[0];
    if (block.kind !== "markdown") throw new Error("expected a markdown block");
    expect(block.source).toBe("Set it up:\n```python\n# setup\n## comment\nx = 1\n```");
    expect(block.html).toContain('<code class="language-python">');
  });

  it("does not resuffix an id whose suffixed form is already taken", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [
        markdownCell(["## Notes"]),
        markdownCell(["## Notes 2"]),
        markdownCell(["## Notes"]),
      ]),
    );
    expect(page.sections.map((section) => section.id)).toEqual([
      "intro",
      "notes",
      "notes-2",
      "notes-3",
    ]);
  });

  it("keeps the hardcoded intro id unique against a ## Intro heading", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [markdownCell(["## Intro"])]),
    );
    expect(page.sections.map((section) => section.id)).toEqual(["intro", "intro-2"]);
  });

  it("gives repeated headings distinct ids with a numeric suffix", () => {
    const page = readNotebookPage(
      summaryFor("Spark Basics", [
        markdownCell(["## Notes"]),
        markdownCell(["## Notes"]),
        markdownCell(["## Notes"]),
      ]),
    );
    expect(page.sections.map((section) => section.id)).toEqual([
      "intro",
      "notes",
      "notes-2",
      "notes-3",
    ]);
  });
});

describe("renderMarkdown", () => {
  it("renders a markdown table into <table>", () => {
    const html = renderMarkdown("| a | b |\n|---|---|\n| 1 | 2 |\n");
    expect(html).toContain("<table>");
    expect(html).toContain("<td>1</td>");
  });

  it("renders a fenced code block into <pre>", () => {
    const html = renderMarkdown("```python\nprint(1)\n```\n");
    expect(html).toContain("<pre>");
    expect(html).toContain('<code class="language-python">');
  });
});

describe("getNotebookSummaries", () => {
  it("returns one summary per notebook in the repository", () => {
    const summaries = getNotebookSummaries();
    expect(summaries.length).toBeGreaterThan(0);
    expect(new Set(summaries.map((summary) => summary.repoPath)).size).toBe(summaries.length);
    for (const summary of summaries) {
      expect(summary.repoPath).toMatch(/^notebooks\/[\w/-]+\.ipynb$/);
    }
  });
});
