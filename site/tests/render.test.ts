import { describe, expect, it } from "vitest";
import { notebookHref, renderMarkdown } from "../lib/render";

describe("notebookHref", () => {
  it("turns a sibling notebook file into its reader URL", () => {
    expect(notebookHref("pyspark-drills-02-dataframe-essentials.ipynb", "")).toBe(
      "/notebooks/pyspark-drills-02-dataframe-essentials/",
    );
  });

  it("keeps the anchor and drops the folder", () => {
    expect(notebookHref("../pyspark/pyspark-01-how-spark-runs.ipynb#sample-data", "/handbook")).toBe(
      "/handbook/notebooks/pyspark-01-how-spark-runs/#sample-data",
    );
  });

  it("leaves external, absolute and in-page links alone", () => {
    for (const href of [
      "https://colab.research.google.com/github/x/blob/master/a.ipynb",
      "/notebooks/a/",
      "#setup",
      "notes.md",
    ]) {
      expect(notebookHref(href, "")).toBe(href);
    }
  });
});

describe("renderMarkdown", () => {
  it("renders notebook links as reader URLs", () => {
    const html = renderMarkdown("Next: [PySpark 3](pyspark-03-types-functions-and-nulls.ipynb).", () => "s");
    expect(html).toContain('href="/notebooks/pyspark-03-types-functions-and-nulls/"');
  });
});
