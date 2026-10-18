// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";

import { NotebookExplorer, type ExplorerGroup } from "./NotebookExplorer";
import type { CardNotebook } from "./NotebookCard";

// The gallery no longer reorders by stars; the stub keeps a starred set that
// would have floated two cards to the top under the old sort.
vi.mock("./starred", () => ({
  useStarred: () => new Set(["/notebooks/bravo.ipynb", "/notebooks/echo.ipynb"]),
  toggleStar: () => {},
}));

const card = (title: string): CardNotebook => ({
  repoPath: `/notebooks/${title.toLowerCase()}.ipynb`,
  slug: title.toLowerCase(),
  title,
  description: "",
  codeCells: 1,
  assertCount: 0,
  tryItBlocks: 0,
  illustrativeCells: 0,
  readingMinutes: 1,
  mergedCodeCells: 0,
  mergedAsserts: 0,
  groupLabel: "g",
  githubHref: "",
  colabHref: "",
});

const groups: ExplorerGroup[] = [
  { label: "Warehouse", notebooks: [card("Alpha"), card("Bravo"), card("Charlie")] },
  { label: "Streaming", notebooks: [card("Delta"), card("Echo")] },
];

describe("NotebookExplorer", () => {
  afterEach(cleanup);

  it("keeps the declared group order even when notebooks are starred", () => {
    const { container } = render(<NotebookExplorer groups={groups} />);

    const titles = container.querySelectorAll("article.topic-card strong");
    expect([...titles].map((el) => el.textContent)).toEqual([
      "Alpha",
      "Bravo",
      "Charlie",
      "Delta",
      "Echo",
    ]);
    // headings also stay in declared order
    const headings = container.querySelectorAll(".section-heading h2");
    expect([...headings].map((el) => el.textContent)).toEqual(["Warehouse", "Streaming"]);
  });

  it("still marks starred cards, but only as a card marker", () => {
    render(<NotebookExplorer groups={groups} />);
    expect(screen.getByRole("button", { name: "Unstar Bravo" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Unstar Echo" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Star Alpha" })).toBeTruthy();
  });
});