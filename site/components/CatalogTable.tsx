"use client";

import Link from "next/link";
import type { NotebookSummary } from "@/lib/notebooks";
import { toneStyle } from "@/lib/tone";
import { useProgress } from "./progress-store";
import { StarButton } from "./StarButton";
import { StatusPill } from "./StatusPill";

/** Notebooks as table rows: title and summary, type, size, reading status and a star. */
export function CatalogTable({ notebooks, caption }: { notebooks: NotebookSummary[]; caption: string }) {
  const progress = useProgress();
  return (
    <table className="rows">
      <caption className="sr-only">{caption}</caption>
      <thead>
        <tr>
          <th scope="col">Notebook</th>
          <th scope="col" className="hide-md">
            Type
          </th>
          <th scope="col" className="num hide-sm">
            Sections
          </th>
          <th scope="col" className="num hide-md">
            Time
          </th>
          <th scope="col">Status</th>
          <th scope="col" className="star-col">
            <span className="sr-only">Star</span>
          </th>
        </tr>
      </thead>
      <tbody>
        {notebooks.map((notebook) => (
          <tr key={notebook.repoPath}>
            <td>
              <Link className="nb" href={notebook.href}>
                <span className="mono-tile" style={toneStyle(notebook.tone, "--tile")} aria-hidden>
                  {notebook.monogram}
                </span>
                <span>
                  <strong>{notebook.title}</strong>
                  {notebook.description ? <small>{notebook.description}</small> : null}
                </span>
              </Link>
            </td>
            <td className="hide-md">{notebook.categoryLabel}</td>
            <td className="num hide-sm">{notebook.sectionCount}</td>
            <td className="num hide-md">{notebook.minutes} min</td>
            <td>
              <StatusPill entry={progress.notebooks[notebook.repoPath]} sectionCount={notebook.sectionCount} />
            </td>
            <td>
              <StarButton repoPath={notebook.repoPath} title={notebook.title} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
