import { describe, expect, it } from "vitest";

import { detectLanguage } from "./markdown";

describe("detectLanguage", () => {
  it("reads a first-line CREATE TABLE cell as SQL", () => {
    expect(detectLanguage("CREATE TABLE employees (\n  id INTEGER\n)")).toBe("sql");
  });

  it("is case-insensitive on the leading SQL keyword", () => {
    expect(detectLanguage("select * from employees")).toBe("sql");
    expect(detectLanguage("WITH hourly AS (SELECT 1) SELECT * FROM hourly")).toBe("sql");
    expect(detectLanguage("explain select count(*) from employees")).toBe("sql");
  });

  it("stays python when the keyword wording sits mid-line, not at line start", () => {
    expect(detectLanguage('conn.sql("create a view of the customers")')).toBe("python");
  });

  it("skips python comment and blank lines before deciding", () => {
    expect(detectLanguage("# create a view of the customers\nprint('ok')")).toBe("python");
    expect(detectLanguage("\n\n  \nimport duckdb")).toBe("python");
  });

  it("skips leading SQL comments, then reads the first real statement", () => {
    expect(detectLanguage("-- comment line\nSELECT * FROM employees")).toBe("sql");
    expect(detectLanguage("/* block comment */\nDELETE FROM employees")).toBe("sql");
  });

  it("defaults to python for empty or ordinary python cells", () => {
    expect(detectLanguage("")).toBe("python");
    expect(detectLanguage("print('hello')")).toBe("python");
  });
});