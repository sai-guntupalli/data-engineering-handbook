import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { TOOLS, anchorFor, categoryOf, compareSubtopics } from "../lib/tools";

const TOPICS_DIR = path.resolve(__dirname, "../../notebooks/topics");

describe("notebook categories", () => {
  it("reads the category from the file name, with overrides for the exceptions", () => {
    expect(categoryOf("python-01-values-and-types")).toBe("lesson");
    expect(categoryOf("python-02-practice-collections")).toBe("drill");
    expect(categoryOf("sql-13-interview-drills")).toBe("drill");
    expect(categoryOf("python-challenges-01-arrays-and-hashing")).toBe("challenge");
    expect(categoryOf("02_python_coding_problems")).toBe("challenge");
    expect(categoryOf("05_interview_questions")).toBe("interview");
    expect(categoryOf("01_python_basics")).toBe("interview");
    expect(categoryOf("pyspark-08-real-world-and-interviews")).toBe("lesson");
    expect(categoryOf("sql")).toBe("reference");
    expect(categoryOf("04_pyspark_concepts")).toBe("reference");
  });

  it("lists lessons before drills, challenges and interview questions", () => {
    const slugs = ["05_interview_questions", "python-02-practice-collections", "python-10-extra", "python-02-collections"];
    const sorted = slugs.map((slug) => ({ slug })).sort(compareSubtopics).map((entry) => entry.slug);
    expect(sorted).toEqual(["python-02-collections", "python-10-extra", "python-02-practice-collections", "05_interview_questions"]);
  });

  it("opens a tool with its overview notebook", () => {
    const slugs = ["pyspark-01-foundations", "spark-tuning", "spark"];
    expect(slugs.map((slug) => ({ slug })).sort(compareSubtopics)[0].slug).toBe("spark");
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
});
