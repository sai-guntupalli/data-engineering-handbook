import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { LEARNING_PATH, nextUp, summarizeStep, validatePath, type PathStage } from "../lib/learning-map";
import type { NotebookStatus } from "../lib/progress";

const TOPICS_DIR = path.resolve(__dirname, "../../notebooks/topics");
const walk = (dir: string): string[] =>
  fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : entry.name.endsWith(".ipynb") ? [entry.name.slice(0, -".ipynb".length)] : [];
  });
const registered = new Set(walk(TOPICS_DIR));

describe("the curated learning path", () => {
  it("only names registered notebooks, each once", () => {
    expect(validatePath(LEARNING_PATH, registered)).toEqual([]);
  });

  it("starts with the first Python lesson", () => {
    expect(nextUp(LEARNING_PATH, () => "not-started")).toEqual({ stageIndex: 0, stepIndex: 0, slug: "python-01-values-and-types" });
  });
});

describe("validatePath", () => {
  it("reports unknown and repeated notebooks, repeated ids and empty steps", () => {
    const stages: PathStage[] = [
      { title: "A", purpose: "", steps: [{ id: "a", label: "A", toolHref: "/", slugs: ["one", "ghost"] }] },
      {
        title: "B",
        purpose: "",
        steps: [
          { id: "a", label: "B", toolHref: "/", slugs: ["one"] },
          { id: "empty", label: "E", toolHref: "/", slugs: [] },
        ],
      },
      { title: "C", purpose: "", steps: [] },
    ];
    expect(validatePath(stages, new Set(["one"]))).toEqual([
      "ghost is not a registered notebook",
      'step id "a" is used twice',
      "one appears more than once",
      'step "empty" has no notebooks',
      'stage "C" has no steps',
    ]);
  });
});

describe("summarizeStep", () => {
  it("is done only when every notebook is done", () => {
    expect(summarizeStep(["done", "done"])).toEqual({ done: 2, total: 2, status: "done" });
    expect(summarizeStep(["done", "not-started"])).toEqual({ done: 1, total: 2, status: "in-progress" });
    expect(summarizeStep(["in-progress", "not-started"])).toEqual({ done: 0, total: 2, status: "in-progress" });
    expect(summarizeStep(["not-started"])).toEqual({ done: 0, total: 1, status: "not-started" });
  });
});

describe("nextUp", () => {
  const stages: PathStage[] = [
    { title: "A", purpose: "", steps: [{ id: "a", label: "A", toolHref: "/", slugs: ["a1", "a2"] }] },
    { title: "B", purpose: "", steps: [{ id: "b", label: "B", toolHref: "/", slugs: ["b1"] }] },
  ];
  const statuses = (map: Record<string, NotebookStatus>) => (slug: string) => map[slug] ?? "not-started";

  it("points at the first unfinished notebook, including one in progress", () => {
    expect(nextUp(stages, statuses({ a1: "done", a2: "in-progress" }))).toEqual({ stageIndex: 0, stepIndex: 0, slug: "a2" });
    expect(nextUp(stages, statuses({ a1: "done", a2: "done" }))).toEqual({ stageIndex: 1, stepIndex: 0, slug: "b1" });
  });

  it("returns null when the whole path is done", () => {
    expect(nextUp(stages, () => "done")).toBeNull();
  });
});
