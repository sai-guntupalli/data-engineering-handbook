"use client";

import Link from "next/link";
import { ArrowRight } from "@phosphor-icons/react";
import type { NotebookSummary } from "@/lib/notebooks";
import { toneStyle } from "@/lib/tone";
import { countByStatus, fractionOf, recentInProgress, weekActivity, type ProgressState } from "@/lib/progress";
import { useProgress } from "./progress-store";
import { useSearchIndex } from "./search-index";
import { StatusPill } from "./StatusPill";

export type Starter = { title: string; text: string; href: string; tone: string; group: string };

const RESUME_LIMIT = 2;

function WeekPanel({ progress }: { progress: ProgressState }) {
  const week = weekActivity(progress, new Date());
  const read = week.reduce((sum, day) => sum + day.count, 0);
  const peak = Math.max(1, ...week.map((day) => day.count));
  const summary = week.map((day) => `${day.weekday} ${day.count}`).join(", ");
  return (
    <div className="panel week">
      <h3>This week</h3>
      <div className="week-stats">
        <div>
          <strong>{read}</strong>
          <span>sections read</span>
        </div>
        <div>
          <strong>{countByStatus(progress).done}</strong>
          <span>notebooks done</span>
        </div>
      </div>
      <div>
        <div className="spark" role="img" aria-label={`Sections read per day: ${summary}`}>
          {week.map((day) => (
            <i
              key={day.key}
              className={day.count === 0 ? "is-empty" : undefined}
              style={{ height: `${Math.max(6, (day.count / peak) * 100)}%` }}
            />
          ))}
        </div>
        <div className="spark-days" aria-hidden>
          {week.map((day) => (
            <span key={day.key}>{day.weekday}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

/** Resume cards for notebooks in progress, or three places to start on a first visit. */
export function ContinueRow({ notebooks, starters }: { notebooks: NotebookSummary[]; starters: Starter[] }) {
  const progress = useProgress();
  const resume = recentInProgress(progress, RESUME_LIMIT).flatMap((repoPath) =>
    notebooks.filter((notebook) => notebook.repoPath === repoPath),
  );
  const { entries } = useSearchIndex(resume.length > 0);

  if (resume.length === 0) {
    return (
      <section className="continue" aria-label="Places to start">
        {starters.map((starter) => (
          <Link key={starter.href} className="panel starter" href={starter.href}>
            <span className="group-cell muted">
              <span className="dot" style={toneStyle(starter.tone, "--dot")} aria-hidden />
              {starter.group}
            </span>
            <h3>{starter.title}</h3>
            <p>{starter.text}</p>
            <span className="starter-foot">
              Start reading <ArrowRight size={14} weight="bold" aria-hidden />
            </span>
          </Link>
        ))}
      </section>
    );
  }

  return (
    <section className="continue" aria-label="Continue reading">
      {resume.map((notebook) => {
        const entry = progress.notebooks[notebook.repoPath];
        const read = new Set(entry?.read ?? []);
        const nextSection = entries?.find(
          (item) => item.kind === "section" && item.repoPath === notebook.repoPath && !read.has(item.href.split("#")[1]),
        );
        const left = Math.max(1, Math.round(notebook.minutes * (1 - fractionOf(entry))));
        return (
          <Link
            key={notebook.repoPath}
            className={resume.length === 1 ? "panel resume is-wide" : "panel resume"}
            href={nextSection?.href ?? notebook.href}
          >
            <div className="resume-top">
              <span>
                <span className="dot" style={toneStyle(notebook.tone, "--dot")} aria-hidden />
                {notebook.groupLabel}
              </span>
              <StatusPill entry={entry} />
            </div>
            <div>
              <h3>{notebook.title}</h3>
              <p className="next">{nextSection ? `Next section: ${nextSection.title}` : "Continue from your last section"}</p>
            </div>
            <div className="bar">
              <span style={{ width: `${Math.round(fractionOf(entry) * 100)}%` }} />
            </div>
            <div className="resume-foot">
              <span>
                {entry?.read.length ?? 0} of {notebook.sectionCount} sections
              </span>
              <span>About {left} min left</span>
            </div>
          </Link>
        );
      })}
      <WeekPanel progress={progress} />
    </section>
  );
}
