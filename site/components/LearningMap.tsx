"use client";

import Link from "next/link";
import { ArrowRight } from "@phosphor-icons/react";
import { nextUp, summarizeStep, type StepSummary } from "@/lib/learning-map";
import type { LearningPathView, PathStepView } from "@/lib/notebooks";
import { statusOf, type NotebookStatus } from "@/lib/progress";
import { useProgress } from "./progress-store";

const RADIUS = 7;
const RING = 2 * Math.PI * RADIUS;

/** Progress ring for a step: an arc for the share done, a check when finished. */
function StepRing({ summary }: { summary: StepSummary }) {
  if (summary.status === "done") {
    return (
      <svg className="ring is-done" viewBox="0 0 20 20" aria-hidden>
        <circle cx="10" cy="10" r={RADIUS + 1} />
        <path d="M6.6 10.2l2.3 2.3 4.5-4.7" />
      </svg>
    );
  }
  const fraction = summary.total > 0 ? summary.done / summary.total : 0;
  return (
    <svg className="ring" viewBox="0 0 20 20" aria-hidden>
      <circle className="ring-track" cx="10" cy="10" r={RADIUS} />
      {summary.status === "in-progress" ? (
        <circle
          className="ring-fill"
          cx="10"
          cy="10"
          r={RADIUS}
          strokeDasharray={`${Math.max(fraction * RING, 2.5)} ${RING}`}
          transform="rotate(-90 10 10)"
        />
      ) : null}
    </svg>
  );
}

function stepCaption(summary: StepSummary): string {
  if (summary.status === "done") return summary.total === 1 ? "Done" : `All ${summary.total} done`;
  if (summary.total === 1) return summary.status === "in-progress" ? "In progress" : "1 notebook";
  return summary.done > 0 || summary.status === "in-progress"
    ? `${summary.done} of ${summary.total} done`
    : `${summary.total} notebooks`;
}

/**
 * The learning path: stages in reading order, each step a track of notebooks with its
 * progress, and a "Next up" link to the first unfinished notebook. Progress lives in
 * this browser; before any reading the path reads as a plain syllabus.
 */
export function LearningMap({ path }: { path: LearningPathView }) {
  const progress = useProgress();
  const repoPaths = new Map(
    path.stages.flatMap((stage) => stage.steps.flatMap((step) => step.notebooks.map((notebook) => [notebook.slug, notebook]))),
  );
  const statusOfSlug = (slug: string): NotebookStatus => statusOf(progress.notebooks[repoPaths.get(slug)?.repoPath ?? ""]);
  const summaryOf = (step: PathStepView) => summarizeStep(step.notebooks.map((notebook) => statusOfSlug(notebook.slug)));

  const steps = path.stages.flatMap((stage) => stage.steps);
  const total = steps.reduce((sum, step) => sum + step.notebooks.length, 0);
  const done = steps.reduce((sum, step) => sum + summaryOf(step).done, 0);
  const next = nextUp(
    path.stages.map((stage) => ({ ...stage, steps: stage.steps.map((step) => ({ ...step, slugs: step.notebooks.map((n) => n.slug) })) })),
    statusOfSlug,
  );
  const nextNotebook = next ? repoPaths.get(next.slug) : undefined;
  const nextStep = next ? path.stages[next.stageIndex].steps[next.stepIndex] : undefined;
  const started = steps.some((step) => summaryOf(step).status !== "not-started");

  const summary = started
    ? `${done} of ${total} notebooks on the path done`
    : `${path.stages.length} stages and ${total} notebooks, from Python and SQL to streaming and interview practice. Each step tracks your progress as you read.`;

  return (
    <section className="panel map" aria-labelledby="map-title">
      <div className="map-head">
        <div>
          <h2 id="map-title">Learning path</h2>
          <p>{summary}</p>
        </div>
        <div className="legend" aria-hidden>
          <span>
            <i className="l-done" />
            Done
          </span>
          <span>
            <i className="l-running" />
            In progress
          </span>
          <span>
            <i className="l-idle" />
            Not started
          </span>
        </div>
      </div>

      {nextNotebook && nextStep && next ? (
        <div className="next-up">
          <div>
            <span className="next-label">{started ? "Next up" : "Start here"}</span>
            <strong>{nextNotebook.title}</strong>
            <small>
              Stage {next.stageIndex + 1}, {path.stages[next.stageIndex].title} · {nextStep.label}
            </small>
          </div>
          <Link className="btn btn-primary" href={nextNotebook.href}>
            {statusOfSlug(next.slug) === "in-progress" ? "Continue reading" : "Start reading"}
            <ArrowRight size={15} aria-hidden />
          </Link>
        </div>
      ) : (
        <div className="next-up is-finished">
          <div>
            <span className="next-label">Path complete</span>
            <strong>Every notebook on the path is done.</strong>
            <small>Pick any tool below to go deeper.</small>
          </div>
        </div>
      )}

      <ol className="path-stages">
        {path.stages.map((stage, stageIndex) => (
          <li key={stage.title} className="path-stage">
            <div className="stage-head">
              <span className="stage-num" aria-hidden>
                {stageIndex + 1}
              </span>
              <h3>{stage.title}</h3>
            </div>
            <p className="stage-purpose">{stage.purpose}</p>
            <ul className="path-steps">
              {stage.steps.map((step, stepIndex) => {
                const stepSummary = summaryOf(step);
                const isNext = next?.stageIndex === stageIndex && next.stepIndex === stepIndex;
                const resume = step.notebooks.find((notebook) => statusOfSlug(notebook.slug) !== "done");
                const href = step.notebooks.length === 1 ? step.notebooks[0].href : (resume?.href ?? step.toolHref);
                const caption = stepCaption(stepSummary);
                return (
                  <li key={step.id}>
                    <Link
                      className={`path-step is-${stepSummary.status}${isNext ? " is-next" : ""}`}
                      href={href}
                      aria-label={`${step.label}: ${caption}${isNext ? ", next up" : ""}`}
                    >
                      <StepRing summary={stepSummary} />
                      <span className="path-step-text">
                        <strong>{step.label}</strong>
                        <small>{caption}</small>
                      </span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </li>
        ))}
      </ol>
    </section>
  );
}
