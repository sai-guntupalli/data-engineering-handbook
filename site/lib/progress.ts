/**
 * Reading progress, kept per browser (localStorage) like stars. Pure functions
 * only; components/progress-store.tsx wires them to storage and React.
 *
 * A section counts as read once the reader scrolls past it. A notebook is done
 * when every section is read, or when the reader marks it done.
 */

export type NotebookProgress = {
  /** Ids of the sections read so far. */
  read: string[];
  /** Sections in the notebook when progress was last saved. */
  total: number;
  /** Set when the reader marks the notebook done by hand. */
  done?: boolean;
  /** Epoch milliseconds of the last change. */
  updatedAt: number;
};

export type ProgressState = {
  notebooks: Record<string, NotebookProgress>;
  /** Sections read per local day, keyed YYYY-MM-DD. */
  days: Record<string, number>;
};

export type NotebookStatus = "done" | "in-progress" | "not-started";

export const EMPTY_PROGRESS: ProgressState = { notebooks: {}, days: {} };

const DAYS_KEPT = 60;

export function dayKey(date: Date): string {
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${date.getFullYear()}-${month}-${day}`;
}

export function statusOf(entry: NotebookProgress | undefined): NotebookStatus {
  if (!entry) return "not-started";
  if (entry.done || (entry.total > 0 && entry.read.length >= entry.total)) return "done";
  return entry.read.length > 0 ? "in-progress" : "not-started";
}

/** Share of sections read, 0..1. Done notebooks are 1. */
export function fractionOf(entry: NotebookProgress | undefined): number {
  if (!entry) return 0;
  if (statusOf(entry) === "done") return 1;
  return entry.total > 0 ? Math.min(1, entry.read.length / entry.total) : 0;
}

function pruneDays(days: Record<string, number>, now: Date): Record<string, number> {
  const oldest = new Date(now);
  oldest.setDate(oldest.getDate() - DAYS_KEPT);
  const cutoff = dayKey(oldest);
  return Object.fromEntries(Object.entries(days).filter(([key]) => key >= cutoff));
}

/** Record one section as read. Reading the same section again changes nothing. */
export function markSectionRead(
  state: ProgressState,
  repoPath: string,
  sectionId: string,
  total: number,
  now: Date,
): ProgressState {
  const current = state.notebooks[repoPath];
  if (current?.read.includes(sectionId)) return state;
  const entry: NotebookProgress = {
    ...current,
    read: [...(current?.read ?? []), sectionId],
    total,
    updatedAt: now.getTime(),
  };
  const today = dayKey(now);
  return {
    notebooks: { ...state.notebooks, [repoPath]: entry },
    days: pruneDays({ ...state.days, [today]: (state.days[today] ?? 0) + 1 }, now),
  };
}

/** Mark a notebook done, or clear its progress entirely. */
export function setDone(state: ProgressState, repoPath: string, done: boolean, total: number, now: Date): ProgressState {
  const notebooks = { ...state.notebooks };
  if (done) {
    notebooks[repoPath] = { read: notebooks[repoPath]?.read ?? [], total, done: true, updatedAt: now.getTime() };
  } else {
    delete notebooks[repoPath];
  }
  return { ...state, notebooks };
}

/** Notebooks in progress, most recently touched first. */
export function recentInProgress(state: ProgressState, limit: number): string[] {
  return Object.entries(state.notebooks)
    .filter(([, entry]) => statusOf(entry) === "in-progress")
    .sort(([, a], [, b]) => b.updatedAt - a.updatedAt)
    .slice(0, limit)
    .map(([repoPath]) => repoPath);
}

export function countByStatus(state: ProgressState): Record<NotebookStatus, number> {
  const counts: Record<NotebookStatus, number> = { done: 0, "in-progress": 0, "not-started": 0 };
  for (const entry of Object.values(state.notebooks)) counts[statusOf(entry)] += 1;
  return counts;
}

/** Sections read on each of the last seven days, oldest first, ending today. */
export function weekActivity(state: ProgressState, today: Date): { key: string; count: number; weekday: string }[] {
  return Array.from({ length: 7 }, (_, offset) => {
    const date = new Date(today);
    date.setDate(date.getDate() - (6 - offset));
    const key = dayKey(date);
    return {
      key,
      count: state.days[key] ?? 0,
      weekday: date.toLocaleDateString("en", { weekday: "narrow" }),
    };
  });
}

/** Parse stored JSON defensively: anything malformed reads as empty progress. */
export function parseProgress(raw: string | null): ProgressState {
  if (!raw) return EMPTY_PROGRESS;
  try {
    const value = JSON.parse(raw) as Partial<ProgressState>;
    if (typeof value !== "object" || value === null) return EMPTY_PROGRESS;
    const notebooks: Record<string, NotebookProgress> = {};
    for (const [key, entry] of Object.entries(value.notebooks ?? {})) {
      if (entry && Array.isArray(entry.read) && typeof entry.total === "number") {
        notebooks[key] = {
          read: entry.read.filter((id): id is string => typeof id === "string"),
          total: entry.total,
          done: entry.done === true || undefined,
          updatedAt: typeof entry.updatedAt === "number" ? entry.updatedAt : 0,
        };
      }
    }
    const days: Record<string, number> = {};
    for (const [key, count] of Object.entries(value.days ?? {})) {
      if (/^\d{4}-\d{2}-\d{2}$/.test(key) && typeof count === "number") days[key] = count;
    }
    return { notebooks, days };
  } catch {
    return EMPTY_PROGRESS;
  }
}

/**
 * Progress saved under a retired notebook's path moves to the notebook that
 * replaced it. When both have progress, the newer entry wins and "done" sticks.
 */
export function migrateProgress(state: ProgressState, renames: ReadonlyMap<string, string>): ProgressState {
  if (!Object.keys(state.notebooks).some((key) => renames.has(key))) return state;
  const notebooks: Record<string, NotebookProgress> = {};
  for (const [key, entry] of Object.entries(state.notebooks)) {
    if (!renames.has(key)) notebooks[key] = entry;
  }
  for (const [key, entry] of Object.entries(state.notebooks)) {
    const target = renames.get(key);
    if (!target) continue;
    const current = notebooks[target];
    if (!current) {
      notebooks[target] = entry;
      continue;
    }
    const newer = entry.updatedAt > current.updatedAt ? entry : current;
    notebooks[target] = { ...newer, done: current.done || entry.done || undefined };
  }
  return { ...state, notebooks };
}

