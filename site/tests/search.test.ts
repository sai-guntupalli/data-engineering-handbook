import { describe, expect, it } from "vitest";
import { highlightParts, matchNotebooks, searchEntries, type SearchEntry } from "../lib/search";

function entry(kind: SearchEntry["kind"], title: string, snippet = "", notebookTitle = title): SearchEntry {
  return {
    kind,
    repoPath: `notebooks/topics/tool/${notebookTitle.toLowerCase()}.ipynb`,
    title,
    notebookTitle,
    toolLabel: "Data Engineering",
    tone: "core",
    monogram: "XX",
    snippet,
    href: "/notebooks/x/",
    colabHref: "https://colab.example",
  };
}

const ENTRIES = [
  entry("notebook", "Spark Tuning", "AQE, skew and partition sizing"),
  entry("notebook", "PySpark", "Lazy evaluation and shuffles"),
  entry("section", "Partition pruning in Spark SQL", "Skip directories that cannot match.", "PySpark"),
  entry("section", "Hidden partitioning", "Partition transforms live in metadata.", "Apache Iceberg"),
  entry("section", "Joins", "Combine rows from two tables.", "SQL"),
];

describe("searchEntries", () => {
  it("returns nothing for a blank query", () => {
    expect(searchEntries(ENTRIES, "   ", { notebooks: 5, sections: 5 })).toEqual({
      notebooks: [],
      sections: [],
      total: 0,
    });
  });

  it("ranks title matches above snippet matches and splits by kind", () => {
    const results = searchEntries(ENTRIES, "partition", { notebooks: 5, sections: 5 });
    expect(results.sections.map((result) => result.title)).toEqual([
      "Partition pruning in Spark SQL",
      "Hidden partitioning",
    ]);
    expect(results.notebooks.map((result) => result.title)).toEqual(["Spark Tuning"]);
    expect(results.total).toBe(3);
  });

  it("needs every word, in any field", () => {
    const results = searchEntries(ENTRIES, "pruning spark", { notebooks: 5, sections: 5 });
    expect(results.sections.map((result) => result.title)).toEqual(["Partition pruning in Spark SQL"]);
  });

  it("caps each list", () => {
    expect(searchEntries(ENTRIES, "partition", { notebooks: 5, sections: 1 }).sections).toHaveLength(1);
  });
});

describe("matchNotebooks", () => {
  const notebooks = [
    { repoPath: "a", title: "Apache Kafka", description: "Topics and partitions", toolLabel: "Streaming" },
    { repoPath: "b", title: "Kafka Connect", description: "", toolLabel: "Streaming" },
    { repoPath: "c", title: "Flink", description: "Reads from Kafka", toolLabel: "Streaming" },
  ];

  it("prefers titles that start with the query", () => {
    expect(matchNotebooks(notebooks, "kafka").map((notebook) => notebook.repoPath)).toEqual(["b", "a", "c"]);
  });
});

describe("highlightParts", () => {
  it("marks each query word, case-insensitively", () => {
    expect(highlightParts("Partition pruning in Spark", "spark PART")).toEqual([
      { text: "Part", match: true },
      { text: "ition pruning in ", match: false },
      { text: "Spark", match: true },
    ]);
  });

  it("escapes regular-expression characters", () => {
    expect(highlightParts("a (b) c", "(b)")).toEqual([
      { text: "a ", match: false },
      { text: "(b)", match: true },
      { text: " c", match: false },
    ]);
  });
});
