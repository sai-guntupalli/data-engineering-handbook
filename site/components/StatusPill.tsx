import { fractionOf, statusOf, type NotebookProgress } from "@/lib/progress";

const LABELS = { done: "Done", "in-progress": "In progress", "not-started": "Not started" } as const;
const CLASSES = { done: "pill is-done", "in-progress": "pill is-running", "not-started": "pill is-idle" } as const;

/** Done, in progress (with sections read) or not started, as a coloured pill. */
export function StatusPill({ entry, sectionCount }: { entry: NotebookProgress | undefined; sectionCount?: number }) {
  const status = statusOf(entry);
  const label =
    status === "in-progress" && sectionCount
      ? `${Math.round(fractionOf(entry) * sectionCount)} of ${sectionCount}`
      : LABELS[status];
  return (
    <span className={CLASSES[status]}>
      <span className="dot" aria-hidden />
      {label}
    </span>
  );
}
