import { describe, expect, it } from "vitest";
import {
  LEARNING_MAP_COLUMNS,
  LEARNING_MAP_EDGES,
  MAP_GEOMETRY,
  layoutMap,
  validateMap,
  type MapColumn,
} from "../lib/learning-map";
import { ALL_GROUPS } from "../lib/notebook-groups";

const registered = new Set(ALL_GROUPS.flatMap((group) => group.slugs));

describe("the curated learning map", () => {
  it("only uses registered notebooks and valid edges", () => {
    expect(validateMap(LEARNING_MAP_COLUMNS, LEARNING_MAP_EDGES, registered)).toEqual([]);
  });

  it("routes every edge", () => {
    expect(layoutMap(LEARNING_MAP_COLUMNS, LEARNING_MAP_EDGES).edges).toHaveLength(LEARNING_MAP_EDGES.length);
  });
});

describe("validateMap", () => {
  const columns: MapColumn[] = [
    { title: "A", nodes: [{ slug: "a1", label: "a1" }, { slug: "a2", label: "a2" }, { slug: "a3", label: "a3" }] },
    { title: "B", nodes: [{ slug: "b1", label: "b1" }] },
    { title: "C", nodes: [{ slug: "c1", label: "c1" }] },
  ];
  const known = new Set(["a1", "a2", "a3", "b1", "c1"]);

  it("rejects unknown slugs, skipped columns, backward and non-adjacent edges", () => {
    const problems = validateMap(
      [...columns, { title: "D", nodes: [{ slug: "ghost", label: "ghost" }] }],
      [
        ["a1", "c1"],
        ["b1", "a1"],
        ["a1", "a3"],
        ["a1", "missing"],
      ],
      known,
    );
    expect(problems).toEqual([
      "ghost is not a registered notebook",
      "edge a1 -> c1 must join neighbours in a column or move one column right",
      "edge b1 -> a1 must join neighbours in a column or move one column right",
      "edge a1 -> a3 must join neighbours in a column or move one column right",
      "edge a1 -> missing names a node that is not on the map",
    ]);
  });
});

describe("layoutMap", () => {
  const columns: MapColumn[] = [
    { title: "A", nodes: [{ slug: "a1", label: "a1" }, { slug: "a2", label: "a2" }] },
    { title: "B", nodes: [{ slug: "b1", label: "b1" }] },
  ];
  const layout = layoutMap(columns, [
    ["a1", "a2"],
    ["a1", "b1"],
  ]);
  const g = MAP_GEOMETRY;

  it("centres a short column", () => {
    const b1 = layout.nodes.find((node) => node.slug === "b1")!;
    expect(b1.y).toBe(g.top + g.rowPitch / 2);
    expect(b1.x).toBe(g.left + g.columnWidth);
  });

  it("draws a vertical line within a column and a curve across columns", () => {
    expect(layout.edges[0].d).toBe(`M95 ${g.top + g.nodeHeight} L95 ${g.top + g.rowPitch}`);
    expect(layout.edges[1].d.startsWith(`M${g.left + g.nodeWidth} ${g.top + g.nodeHeight / 2} C`)).toBe(true);
  });

  it("sizes the canvas to fit", () => {
    expect(layout.width).toBe(g.left * 2 + g.columnWidth + g.nodeWidth);
  });
});
