"use client";

import { ArrowUpRight, Star } from "@phosphor-icons/react";
import type { NotebookListItem } from "@/lib/notebooks";
import { toggleStar, useStarred } from "./starred";

/** One notebook as a ruled list entry: title and summary, then its two links and a star. */
export function NotebookRow({
  notebook,
  position,
  showGroup = false,
}: {
  notebook: NotebookListItem;
  /** 1-based place in its group, shown as an index number. */
  position?: number;
  showGroup?: boolean;
}) {
  const starred = useStarred();
  const isStarred = starred.has(notebook.repoPath);

  return (
    <li className="notebook-row" data-starred={isStarred || undefined}>
      <div className="notebook-body">
        {position !== undefined ? (
          <span className="notebook-index" aria-hidden>
            {String(position).padStart(2, "0")}
          </span>
        ) : null}
        <div className="notebook-text">
          {showGroup ? <span className="notebook-group">{notebook.groupLabel}</span> : null}
          <h3 className="notebook-title">{notebook.title}</h3>
          {notebook.description ? <p className="notebook-description">{notebook.description}</p> : null}
        </div>
      </div>
      <div className="notebook-actions">
        <a
          className="notebook-open"
          href={notebook.colabHref}
          target="_blank"
          rel="noreferrer"
          title="Opens this notebook in Google Colab, a hosted Jupyter that runs the cells with no local setup"
        >
          Open in Colab
          <ArrowUpRight size={14} weight="bold" aria-hidden />
        </a>
        <a className="notebook-source" href={notebook.githubHref} target="_blank" rel="noreferrer">
          Source
        </a>
        <button
          type="button"
          className={isStarred ? "star-button is-starred" : "star-button"}
          onClick={() => toggleStar(notebook.repoPath)}
          aria-pressed={isStarred}
          aria-label={isStarred ? `Unstar ${notebook.title}` : `Star ${notebook.title}`}
          title={isStarred ? "Starred: click to remove" : "Star this notebook"}
        >
          <Star size={16} weight={isStarred ? "fill" : "regular"} aria-hidden />
        </button>
      </div>
    </li>
  );
}
