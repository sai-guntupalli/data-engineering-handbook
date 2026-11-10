import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { TOOL_CATEGORIES, TOOLS, anchorFor, categoryOf, compareSubtopics, compareTools, toolSortName } from "../lib/tools";

const TOPICS_DIR = path.resolve(__dirname, "../../notebooks/topics");

describe("notebook categories", () => {
  it("reads the category from the file name, with overrides for the exceptions", () => {
    expect(categoryOf("python-01-values-and-types")).toBe("lesson");
    expect(categoryOf("python-02-practice-collections")).toBe("drill");
    expect(categoryOf("sql-13-interview-drills")).toBe("drill");
    expect(categoryOf("python-challenges-01-arrays-and-hashing")).toBe("challenge");
    expect(categoryOf("python-drills-01-values-and-types")).toBe("drill");
    expect(categoryOf("python-coding-problems")).toBe("challenge");
    expect(categoryOf("interview-question-bank")).toBe("interview");
    expect(categoryOf("python-interview-basics")).toBe("interview");
    expect(categoryOf("sql-00-start-here")).toBe("lesson");
    expect(categoryOf("pyspark-08-real-world-and-interviews")).toBe("lesson");
    expect(categoryOf("sql-reference")).toBe("reference");
    expect(categoryOf("pyspark-concepts-end-to-end")).toBe("reference");
  });

  it("lists lessons before drills, challenges and interview questions", () => {
    const slugs = ["python-interview-basics", "python-drills-02-collections", "python-10-extra", "python-02-collections"];
    const sorted = slugs.map((slug) => ({ slug })).sort(compareSubtopics).map((entry) => entry.slug);
    expect(sorted).toEqual(["python-02-collections", "python-10-extra", "python-drills-02-collections", "python-interview-basics"]);
  });

  it("opens a tool with its overview notebook", () => {
    const slugs = ["pyspark-01-foundations", "pyspark-tuning", "pyspark-00-overview"];
    expect(slugs.map((slug) => ({ slug })).sort(compareSubtopics)[0].slug).toBe("pyspark-00-overview");
  });
});

describe("the tool registry", () => {
  it("has one entry per notebooks folder, and no folder without an entry", () => {
    const folders = fs
      .readdirSync(TOPICS_DIR, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort();
    expect(TOOLS.map((tool) => tool.folder).sort()).toEqual(folders);
  });

  it("gives every tool a unique label and anchor", () => {
    const unique = (values: string[]) => new Set(values).size === values.length;
    expect(unique(TOOLS.map((tool) => tool.label))).toBe(true);
    expect(unique(TOOLS.map((tool) => anchorFor(tool.label)))).toBe(true);
  });

  it("puts every tool in a category, and leaves no category empty", () => {
    const ids = TOOL_CATEGORIES.map((category) => category.id);
    expect(TOOLS.every((tool) => ids.includes(tool.category))).toBe(true);
    for (const id of ids) expect(TOOLS.some((tool) => tool.category === id)).toBe(true);
  });

  it("sorts tool names without their vendor prefix", () => {
    expect(toolSortName("Apache Kafka")).toBe("kafka");
    expect(toolSortName("Amazon Redshift")).toBe("redshift");
    expect(toolSortName("dbt")).toBe("dbt");
  });
});

describe("compareTools", () => {
  const tool = (label: string, legacy?: string) => ({ folder: label, label, description: "", tone: "other" as const, category: "processing" as const, legacy });
  it("puts legacy tools after active ones, by name within each group", () => {
    const sorted = [tool("Hadoop", "old"), tool("Trino"), tool("Apache Impala", "old"), tool("Apache Flink")].sort(compareTools);
    expect(sorted.map((t) => t.label)).toEqual(["Apache Flink", "Trino", "Hadoop", "Apache Impala"]);
  });

  it("marks exactly the five legacy tools", () => {
    expect(TOOLS.filter((t) => t.legacy).map((t) => t.folder).sort()).toEqual(["flume", "greenplum", "hadoop", "hbase", "impala"]);
  });
});
