"use client";

import Link from "next/link";
import { Flask, Play } from "@phosphor-icons/react";
import type { NotebookSummary } from "@/lib/notebooks";
import { countByStatus, recentInProgress } from "@/lib/progress";
import { useProgress } from "./progress-store";

type Start = Pick<NotebookSummary, "title" | "href">;

/**
 * First visit: what the handbook is and where to start. Returning reader: where
 * they left off. Progress is client-only, so the first-visit copy is what the
 * static HTML contains.
 */
export function HomeHero({
  notebooks,
  pythonStart,
  sqlStart,
  practiceHref,
}: {
  notebooks: NotebookSummary[];
  pythonStart: Start;
  sqlStart: Start;
  practiceHref: string;
}) {
  const progress = useProgress();
  const counts = countByStatus(progress);
  const latestPath = recentInProgress(progress, 1)[0];
  const latest = notebooks.find((notebook) => notebook.repoPath === latestPath);

  if (!latest && counts.done === 0) {
    return (
      <section className="page-head">
        <div>
          <h1>Learn data engineering by running it</h1>
          <p className="lead">
            Every topic is a notebook: read it here, then run it in Google Colab with nothing to install. Follow the
            learning path below, or search for the tool you need.
          </p>
        </div>
        <div className="actions">
          <Link className="btn" href={sqlStart.href} title={sqlStart.title}>
            Start the SQL path
          </Link>
          <Link className="btn btn-primary" href={pythonStart.href} title={pythonStart.title}>
            <Play size={15} weight="fill" aria-hidden />
            Start the Python path
          </Link>
        </div>
      </section>
    );
  }

  const doneText = `${counts.done} ${counts.done === 1 ? "notebook" : "notebooks"} done`;
  return (
    <section className="page-head">
      <div>
        <h1>Pick up where you left off</h1>
        <p className="lead">{latest ? `${doneText}. ${latest.title} is in progress.` : `${doneText}. Choose what to read next.`}</p>
      </div>
      <div className="actions">
        <Link className="btn" href={practiceHref}>
          <Flask size={15} aria-hidden />
          Open interview practice
        </Link>
        {latest ? (
          <Link className="btn btn-primary" href={latest.href}>
            <Play size={15} weight="fill" aria-hidden />
            Resume {latest.title}
          </Link>
        ) : null}
      </div>
    </section>
  );
}
