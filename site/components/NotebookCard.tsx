"use client";

import { Star } from "@phosphor-icons/react";
import type { NotebookListItem } from "@/lib/notebooks";
import { toggleStar, useStarred } from "./starred";

export function NotebookCard({ notebook }: { notebook: NotebookListItem }) {
  const starred = useStarred();
  const isStarred = starred.has(notebook.repoPath);

  return (
    <article className="topic-card">
      <button
        type="button"
        className={isStarred ? "star-button starred" : "star-button"}
        onClick={() => toggleStar(notebook.repoPath)}
        aria-pressed={isStarred}
        aria-label={isStarred ? `Unstar ${notebook.title}` : `Star ${notebook.title}`}
        title={isStarred ? "Starred — click to remove" : "Star this notebook"}
      >
        <Star size={16} weight={isStarred ? "fill" : "regular"} />
      </button>
      <strong>{notebook.title}</strong>
      {notebook.description ? <p>{notebook.description}</p> : null}
      <p className="notebook-meta">
        {notebook.codeCells} code cells · {notebook.assertCount} checks ·{" "}
        {notebook.tryItBlocks > 0
          ? `${notebook.tryItBlocks} ${notebook.tryItBlocks === 1 ? "exercise" : "exercises"} · `
          : ""}
        ~{notebook.readingMinutes} min
      </p>
      <div className="notebook-links">
        <a
          href={notebook.colabHref}
          target="_blank"
          rel="noreferrer"
          title="Opens this notebook in Google Colab — a hosted Jupyter that runs the cells without any local setup"
        >
          Open in Colab
        </a>
        <a href={notebook.githubHref} target="_blank" rel="noreferrer">
          GitHub
        </a>
      </div>
    </article>
  );
}