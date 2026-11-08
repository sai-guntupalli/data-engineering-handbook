"use client";

import { Star } from "@phosphor-icons/react";
import { toggleStar, useStarred } from "./starred";

/** Star toggle: an icon button in tables, a labelled button on the reader. */
export function StarButton({ repoPath, title, labelled = false }: { repoPath: string; title: string; labelled?: boolean }) {
  const starred = useStarred().has(repoPath);
  const label = starred ? `Unstar ${title}` : `Star ${title}`;
  return (
    <button
      type="button"
      className={labelled ? `btn${starred ? " is-starred" : ""}` : "star-btn"}
      onClick={() => toggleStar(repoPath)}
      aria-pressed={starred}
      aria-label={labelled ? undefined : label}
      title={label}
    >
      <Star size={labelled ? 15 : 16} weight={starred ? "fill" : "regular"} aria-hidden />
      {labelled ? (starred ? "Starred" : "Star") : null}
    </button>
  );
}
