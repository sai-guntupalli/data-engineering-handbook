"use client";

import { useMemo } from "react";
import { anchorFor } from "@/lib/notebook-groups";
import { NotebookCard, type CardNotebook } from "./NotebookCard";
import { useStarred } from "./starred";

export type ExplorerGroup = {
  label: string;
  notebooks: CardNotebook[];
};

/**
 * The browse-mode gallery: every group in declared order, always unfiltered.
 * Search lives in the header suggestions panel and the /search page.
 */
export function NotebookExplorer({ groups }: { groups: ExplorerGroup[] }) {
  const starred = useStarred();

  const sections = useMemo(
    () =>
      groups.map((group) => ({
        ...group,
        notebooks: [...group.notebooks].sort(
          (a, b) => Number(starred.has(b.repoPath)) - Number(starred.has(a.repoPath)),
        ),
      })),
    [groups, starred],
  );

  return (
    <div className="explorer">
      {starred.size > 0 ? (
        <p className="results-meta">
          <span className="starred-hint" title="Starred notebooks float to the top of each group">
            ★ {starred.size} starred
          </span>{" "}
          — starred notebooks float to the top of their group
        </p>
      ) : null}
      {sections.map((group) => (
        <section key={group.label} className="topic-group" id={anchorFor(group.label)}>
          <div className="section-heading">
            <h2>{group.label}</h2>
            <p>
              {group.notebooks.length} {group.notebooks.length === 1 ? "notebook" : "notebooks"}
            </p>
          </div>
          <div className="topic-grid">
            {group.notebooks.map((notebook) => (
              <NotebookCard key={notebook.repoPath} notebook={notebook} />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}