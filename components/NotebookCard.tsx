"use client";

import Link from "next/link";
import { Star } from "@phosphor-icons/react";
import { toggleStar, useStarred } from "./starred";

/** A notebook as rendered on a gallery card (plus the group it sits in). */
export type CardNotebook = {
  repoPath: string;
  slug: string;
  title: string;
  description: string;
  codeCells: number;
  assertCount: number;
  tryItBlocks: number;
  illustrativeCells: number;
  readingMinutes: number;
  /** Cells/asserts that sit inside merged copies of practice notebooks within
   *  this file; the card subtracts them (zero for practice notebooks) so the
   *  numbers match the hero stats and no notebook is counted twice. */
  mergedCodeCells: number;
  mergedAsserts: number;
  groupLabel: string;
  githubHref: string;
  /** Opens this notebook in Google Colab (repository must stay public). */
  colabHref: string;
};

export function NotebookCard({ notebook }: { notebook: CardNotebook }) {
  const starred = useStarred();
  const isStarred = starred.has(notebook.repoPath);
  const runCells = notebook.codeCells - notebook.mergedCodeCells;
  const runChecks = notebook.assertCount - notebook.mergedAsserts;
  const mergedTitle =
    notebook.mergedCodeCells > 0 || notebook.mergedAsserts > 0
      ? `Excludes the practice copies merged into this topic (${notebook.mergedCodeCells} code cells, ${notebook.mergedAsserts} checks).`
      : undefined;

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
      <p className="notebook-meta" title={mergedTitle}>
        {runCells} code cells · {runChecks} checks ·{" "}
        {notebook.tryItBlocks > 0
          ? `${notebook.tryItBlocks} ${notebook.tryItBlocks === 1 ? "exercise" : "exercises"} · `
          : ""}
        ~{notebook.readingMinutes} min
        {notebook.illustrativeCells > 0 ? (
          <span
            className="meta-pill"
            title="Cells marked # ILLUSTRATIVE need an external platform (Spark, Kafka, a cloud SDK); they will not run in plain Jupyter."
          >
            {notebook.illustrativeCells} illustrative
          </span>
        ) : null}
      </p>
      <div className="notebook-links">
        <Link
          href={`/topics/${notebook.slug}`}
          title="Read and run this notebook right here in the site viewer"
        >
          Read
        </Link>
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