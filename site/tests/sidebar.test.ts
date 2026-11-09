import { describe, expect, it } from "vitest";
import { isGroupExpanded, parseGroupState, toolStarKey } from "../lib/sidebar";

describe("sidebar groups", () => {
  it("opens only the group that holds the current tool by default", () => {
    expect(isGroupExpanded({}, "languages", ["python", "sql"], "sql")).toBe(true);
    expect(isGroupExpanded({}, "cloud", ["aws"], "sql")).toBe(false);
    expect(isGroupExpanded({}, "languages", ["python"])).toBe(false);
  });

  it("prefers the reader's stored choice over the default", () => {
    expect(isGroupExpanded({ languages: false }, "languages", ["python"], "python")).toBe(false);
    expect(isGroupExpanded({ cloud: true }, "cloud", ["aws"], "python")).toBe(true);
  });

  it("parses stored state and drops anything that is not a boolean", () => {
    expect(parseGroupState('{"cloud": true, "bi": "yes", "sql": false}')).toEqual({ cloud: true, sql: false });
    expect(parseGroupState("not json")).toEqual({});
    expect(parseGroupState("[true]")).toEqual({});
    expect(parseGroupState(null)).toEqual({});
  });

  it("keys tool stars apart from notebook paths", () => {
    expect(toolStarKey("kafka")).toBe("tool:kafka");
  });
});
