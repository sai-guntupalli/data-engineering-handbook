import { describe, expect, it } from "vitest";
import { ALL_GROUPS, LEARNING_GROUPS, PRACTICE_GROUPS, anchorFor } from "../lib/notebook-groups";

describe("the group registry", () => {
  it("lists every learning group before any practice group", () => {
    const sections = ALL_GROUPS.map((group) => group.section);
    const firstPractice = sections.indexOf("practice");
    expect(firstPractice).toBeGreaterThan(0);
    expect(sections.slice(firstPractice).every((section) => section === "practice")).toBe(true);
  });

  it("keeps the two sections in ALL_GROUPS in sync with their own lists", () => {
    expect(ALL_GROUPS).toEqual([...LEARNING_GROUPS, ...PRACTICE_GROUPS]);
    expect(LEARNING_GROUPS.every((group) => group.section === "learn")).toBe(true);
    expect(PRACTICE_GROUPS.every((group) => group.section === "practice")).toBe(true);
  });

  it("gives every group a unique label, short label and anchor", () => {
    const unique = (values: string[]) => new Set(values).size === values.length;
    expect(unique(ALL_GROUPS.map((group) => group.label))).toBe(true);
    expect(unique(ALL_GROUPS.map((group) => group.shortLabel))).toBe(true);
    expect(unique(ALL_GROUPS.map((group) => anchorFor(group.label)))).toBe(true);
  });

  it("lists the practice groups by what they train", () => {
    expect(PRACTICE_GROUPS.map((group) => group.label)).toEqual([
      "Python drills",
      "Python coding challenges",
      "Interview questions",
      "SQL interview drills",
      "PySpark interview practice",
    ]);
  });
});
