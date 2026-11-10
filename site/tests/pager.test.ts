import { describe, expect, it } from "vitest";
import { pickNeighbours, type ReadingOrder } from "../lib/pager";

const PATH: ReadingOrder = { label: "on the learning path", slugs: ["parquet", "delta", "iceberg", "airflow"] };
const SQL: ReadingOrder = { label: "in SQL", slugs: ["sql-12", "sql-13", "sql-14"] };
const AVRO_TOOL: ReadingOrder = { label: "in Apache Avro", slugs: ["avro"] };
const FORMATS: ReadingOrder = { label: "in File and table formats", slugs: ["avro", "delta", "hudi", "iceberg", "parquet"] };

describe("pickNeighbours", () => {
  it("follows the learning path across tools", () => {
    expect(pickNeighbours("delta", [PATH, FORMATS])).toEqual({ previous: "parquet", next: "iceberg", label: "on the learning path" });
  });

  it("uses the tool order for notebooks off the path", () => {
    expect(pickNeighbours("sql-13", [PATH, SQL])).toEqual({ previous: "sql-12", next: "sql-14", label: "in SQL" });
  });

  it("falls back to the category when the tool has one notebook", () => {
    expect(pickNeighbours("avro", [PATH, AVRO_TOOL, FORMATS])).toEqual({
      previous: null,
      next: "delta",
      label: "in File and table formats",
    });
  });

  it("returns null when no order has a neighbour", () => {
    expect(pickNeighbours("solo", [{ label: "in X", slugs: ["solo"] }])).toBeNull();
    expect(pickNeighbours("missing", [PATH])).toBeNull();
  });
});
