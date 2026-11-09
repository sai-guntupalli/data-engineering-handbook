"use client";

import type { NotebookSummary } from "@/lib/notebooks";
import { CatalogTable } from "./CatalogTable";
import { useStarred } from "./starred";

/** The notebooks this browser has starred, in the order of the library. */
export function StarredList({ notebooks }: { notebooks: NotebookSummary[] }) {
  const starred = useStarred();
  const visible = notebooks.filter((notebook) => starred.has(notebook.repoPath));
  if (visible.length === 0) {
    return (
      <div className="empty-state">
        <h2>No starred notebooks yet</h2>
        <p>Star a notebook from its row or its page, and it stays here on this device.</p>
      </div>
    );
  }
  return <CatalogTable notebooks={visible} caption="Starred notebooks" />;
}
