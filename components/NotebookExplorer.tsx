"use client";

import { anchorFor } from "@/lib/notebook-groups";
import { NotebookCard, type CardNotebook } from "./NotebookCard";

export type ExplorerGroup = {
  label: string;
  notebooks: CardNotebook[];
};

/**
 * The browse-mode gallery: every group and notebook in declared order, always
 * unfiltered. Starring is a pure marker on the card (NotebookCard) — it does
 * not reorder anything here.
 */
export function NotebookExplorer({ groups }: { groups: ExplorerGroup[] }) {
  return (
    <div className="explorer">
      {groups.map((group) => (
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