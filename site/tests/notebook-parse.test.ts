import { describe, expect, it } from "vitest";
import {
  cellKindOf,
  createIdAllocator,
  estimateMinutes,
  monogram,
  outlineOf,
  parseNotebook,
  splitIntro,
  stripTitleBlock,
  titleFromMarkdown,
  type RawNotebook,
} from "../lib/notebook-parse";

const TITLE_CELL = [
  "# 04 - PySpark Concepts\n",
  "\n",
  "*Author: [Sai](https://github.com/sai) · CC BY 4.0*\n",
  "\n",
  "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.example)\n",
  "\n",
  "How Spark turns your code into a distributed plan, with runnable checks.\n",
];

function notebook(cells: RawNotebook["cells"]): RawNotebook {
  return { cells };
}

describe("titleFromMarkdown", () => {
  it("drops a leading index and inline markdown", () => {
    expect(titleFromMarkdown("# 05 — Interview `Question` Bank", "x")).toBe("Interview Question Bank");
  });

  it("falls back to the file name", () => {
    expect(titleFromMarkdown("no heading here", "02_python_coding")).toBe("python coding");
  });
});

describe("stripTitleBlock", () => {
  it("removes the title, credit line and Colab badge but keeps the intro", () => {
    expect(stripTitleBlock(TITLE_CELL.join(""))).toBe(
      "How Spark turns your code into a distributed plan, with runnable checks.",
    );
  });
});

describe("splitIntro", () => {
  it("takes a leading plain paragraph", () => {
    expect(splitIntro("First `para`\nwraps here.\n\n## Next")).toEqual({ intro: "First para wraps here.", rest: "## Next" });
  });

  it("leaves a cell that opens with a heading or list alone", () => {
    expect(splitIntro("## Heading\n\ntext")).toEqual({ intro: "", rest: "## Heading\n\ntext" });
    expect(splitIntro("- item")).toEqual({ intro: "", rest: "- item" });
  });
});

describe("outlineOf", () => {
  it("ignores headings inside fenced code", () => {
    const outline = outlineOf("## Real heading\n\nA paragraph that explains it.\n\n```\n## not a heading\n```\n");
    expect(outline).toEqual([
      { type: "heading", title: "Real heading" },
      { type: "paragraph", text: "A paragraph that explains it." },
    ]);
  });
});

describe("createIdAllocator", () => {
  it("makes repeated titles unique in document order", () => {
    const allocate = createIdAllocator();
    expect([allocate("Joins"), allocate("Joins"), allocate("What's next?")]).toEqual([
      "joins",
      "joins-2",
      "what-s-next",
    ]);
  });
});

describe("cellKindOf", () => {
  it("classifies setup, check and plain code cells", () => {
    expect(cellKindOf("code", "# Setup: installs packages\nimport sys")).toBe("setup");
    expect(cellKindOf("code", "result = 1\nassert result == 1")).toBe("check");
    expect(cellKindOf("code", "reassert = 2")).toBe("code");
    expect(cellKindOf("markdown", "assert this")).toBe("markdown");
  });
});

describe("parseNotebook", () => {
  const parsed = parseNotebook(
    notebook([
      { cell_type: "markdown", source: TITLE_CELL },
      { cell_type: "code", source: "# Setup: install\nimport sys" },
      { cell_type: "markdown", source: "## Lazy evaluation\n\nTransformations build a plan; actions run it." },
      { cell_type: "code", source: "df = spark.range(3)\nassert df.count() == 3" },
      { cell_type: "markdown", source: "" },
      { cell_type: "markdown", source: "## Lazy evaluation\n\n```python\nx = 1\n```" },
      { cell_type: "code", source: "print('hi')" },
    ]),
    "spark",
  );

  it("reads the title and description", () => {
    expect(parsed.title).toBe("PySpark Concepts");
    expect(parsed.description).toBe("How Spark turns your code into a distributed plan, with runnable checks.");
  });

  it("collects sections with unique ids and a snippet", () => {
    expect(parsed.sections).toEqual([
      { id: "lazy-evaluation", title: "Lazy evaluation", snippet: "Transformations build a plan; actions run it." },
      { id: "lazy-evaluation-2", title: "Lazy evaluation", snippet: "" },
    ]);
  });

  it("lifts the opening paragraph out as the intro", () => {
    expect(parsed.intro).toBe("How Spark turns your code into a distributed plan, with runnable checks.");
  });

  it("drops empty cells (including a title cell left empty) and keeps original indexes", () => {
    expect(parsed.cells.map((cell) => [cell.index, cell.kind])).toEqual([
      [1, "setup"],
      [2, "markdown"],
      [3, "check"],
      [5, "markdown"],
      [6, "code"],
    ]);
    expect(parsed.checks).toBe(1);
  });

  it("estimates at least one minute", () => {
    expect(parsed.minutes).toBe(1);
  });
});

describe("estimateMinutes", () => {
  it("adds reading and code time", () => {
    expect(estimateMinutes(2200, 300)).toBe(20);
  });
});

describe("monogram", () => {
  it.each([
    ["Apache Iceberg", "Ic"],
    ["Data Quality", "DQ"],
    ["dbt", "Db"],
    ["Change Data Capture (CDC)", "CD"],
    ["AWS", "AW"],
  ])("%s -> %s", (title, expected) => {
    expect(monogram(title)).toBe(expected);
  });
});
