import { describe, expect, it } from "vitest";
import {
  EMPTY_PROGRESS,
  countByStatus,
  dayKey,
  fractionOf,
  markSectionRead,
  parseProgress,
  recentInProgress,
  setDone,
  statusOf,
  weekActivity,
} from "../lib/progress";

const NOW = new Date(2026, 10, 7, 12, 0, 0);
const SPARK = "notebooks/topics/spark.ipynb";
const DELTA = "notebooks/topics/delta.ipynb";

describe("statusOf and fractionOf", () => {
  it("is not started without an entry", () => {
    expect(statusOf(undefined)).toBe("not-started");
    expect(fractionOf(undefined)).toBe(0);
  });

  it("is in progress part way and done when every section is read", () => {
    expect(statusOf({ read: ["a"], total: 3, updatedAt: 0 })).toBe("in-progress");
    expect(fractionOf({ read: ["a"], total: 4, updatedAt: 0 })).toBe(0.25);
    expect(statusOf({ read: ["a", "b"], total: 2, updatedAt: 0 })).toBe("done");
  });

  it("is done when marked by hand", () => {
    expect(statusOf({ read: [], total: 5, done: true, updatedAt: 0 })).toBe("done");
    expect(fractionOf({ read: [], total: 5, done: true, updatedAt: 0 })).toBe(1);
  });
});

describe("markSectionRead", () => {
  it("records the section and today's activity", () => {
    const state = markSectionRead(EMPTY_PROGRESS, SPARK, "lazy", 10, NOW);
    expect(state.notebooks[SPARK]).toEqual({ read: ["lazy"], total: 10, updatedAt: NOW.getTime() });
    expect(state.days[dayKey(NOW)]).toBe(1);
  });

  it("ignores a section that is already read", () => {
    const once = markSectionRead(EMPTY_PROGRESS, SPARK, "lazy", 10, NOW);
    expect(markSectionRead(once, SPARK, "lazy", 10, NOW)).toBe(once);
  });

  it("forgets activity older than sixty days", () => {
    const old = { ...EMPTY_PROGRESS, days: { "2026-01-01": 4 } };
    expect(markSectionRead(old, SPARK, "lazy", 10, NOW).days).toEqual({ [dayKey(NOW)]: 1 });
  });
});

describe("setDone", () => {
  it("marks done and clears", () => {
    const done = setDone(EMPTY_PROGRESS, SPARK, true, 10, NOW);
    expect(statusOf(done.notebooks[SPARK])).toBe("done");
    expect(setDone(done, SPARK, false, 10, NOW).notebooks[SPARK]).toBeUndefined();
  });
});

describe("recentInProgress and countByStatus", () => {
  it("lists in-progress notebooks newest first", () => {
    let state = markSectionRead(EMPTY_PROGRESS, SPARK, "a", 10, new Date(2026, 10, 1));
    state = markSectionRead(state, DELTA, "a", 10, new Date(2026, 10, 5));
    state = setDone(state, "notebooks/topics/dbt.ipynb", true, 4, NOW);
    expect(recentInProgress(state, 5)).toEqual([DELTA, SPARK]);
    expect(recentInProgress(state, 1)).toEqual([DELTA]);
    expect(countByStatus(state)).toEqual({ done: 1, "in-progress": 2, "not-started": 0 });
  });
});

describe("weekActivity", () => {
  it("returns seven days ending today", () => {
    const state = { ...EMPTY_PROGRESS, days: { [dayKey(NOW)]: 3, "2026-11-01": 2 } };
    const week = weekActivity(state, NOW);
    expect(week).toHaveLength(7);
    expect(week[6]).toMatchObject({ key: "2026-11-07", count: 3 });
    expect(week[0]).toMatchObject({ key: "2026-11-01", count: 2 });
  });
});

describe("parseProgress", () => {
  it("reads valid JSON and drops malformed parts", () => {
    const raw = JSON.stringify({
      notebooks: { [SPARK]: { read: ["a", 3], total: 4, updatedAt: 9 }, bad: { read: "x" } },
      days: { "2026-11-07": 2, nope: 1 },
    });
    expect(parseProgress(raw)).toEqual({
      notebooks: { [SPARK]: { read: ["a"], total: 4, done: undefined, updatedAt: 9 } },
      days: { "2026-11-07": 2 },
    });
  });

  it("treats garbage as empty", () => {
    expect(parseProgress("{not json")).toBe(EMPTY_PROGRESS);
    expect(parseProgress(null)).toBe(EMPTY_PROGRESS);
  });
});
