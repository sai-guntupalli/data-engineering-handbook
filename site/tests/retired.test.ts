import { describe, expect, it } from "vitest";
import { migrateProgress, type ProgressState } from "../lib/progress";
import { RETIRED_NOTEBOOKS, migrateStarred } from "../lib/retired";

const RENAMES = new Map([["old.ipynb", "new.ipynb"]]);

describe("migrateProgress", () => {
  it("moves progress from a retired path to its replacement", () => {
    const state: ProgressState = { notebooks: { "old.ipynb": { read: ["a"], total: 3, updatedAt: 5 } }, days: { "2026-11-01": 1 } };
    expect(migrateProgress(state, RENAMES)).toEqual({
      notebooks: { "new.ipynb": { read: ["a"], total: 3, updatedAt: 5 } },
      days: { "2026-11-01": 1 },
    });
  });

  it("keeps the newer entry and lets done stick when both exist", () => {
    const state: ProgressState = {
      notebooks: {
        "old.ipynb": { read: ["a"], total: 3, done: true, updatedAt: 1 },
        "new.ipynb": { read: ["x", "y"], total: 9, updatedAt: 2 },
      },
      days: {},
    };
    expect(migrateProgress(state, RENAMES).notebooks).toEqual({ "new.ipynb": { read: ["x", "y"], total: 9, done: true, updatedAt: 2 } });
  });

  it("returns the same object when nothing needs moving", () => {
    const state: ProgressState = { notebooks: { "other.ipynb": { read: [], total: 1, updatedAt: 0 } }, days: {} };
    expect(migrateProgress(state, RENAMES)).toBe(state);
  });
});

describe("retired notebooks", () => {
  it("maps stars onto the replacement and drops duplicates", () => {
    expect([...migrateStarred(["old.ipynb", "new.ipynb", "keep.ipynb"], RENAMES)]).toEqual(["new.ipynb", "keep.ipynb"]);
  });

  it("never points one retired notebook at another", () => {
    const slugs = new Set(RETIRED_NOTEBOOKS.map((retired) => retired.slug));
    for (const retired of RETIRED_NOTEBOOKS) expect(slugs.has(retired.movedTo)).toBe(false);
  });
});
