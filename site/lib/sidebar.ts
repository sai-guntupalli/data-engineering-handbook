/**
 * Rules for the sidebar's tool groups, kept pure so they can be unit-tested.
 * Group state is stored per category as an explicit choice; a category the reader
 * never toggled falls back to the default: open when it holds the current tool.
 */

/** Stored choices: category id -> expanded. */
export type GroupState = Record<string, boolean>;

export const SIDEBAR_GROUPS_KEY = "de-handbook:sidebar-groups";

/** Key used in the shared star store for a tool, so it never collides with a notebook path. */
export function toolStarKey(folder: string): string {
  return `tool:${folder}`;
}

/** Whether a category is open: the reader's stored choice, else open only when it holds the current tool. */
export function isGroupExpanded(state: GroupState, categoryId: string, toolFolders: string[], currentTool?: string): boolean {
  if (categoryId in state) return state[categoryId];
  return currentTool !== undefined && toolFolders.includes(currentTool);
}

/** Parse stored group state, ignoring anything that is not an object of booleans. */
export function parseGroupState(raw: string | null): GroupState {
  if (!raw) return {};
  try {
    const value: unknown = JSON.parse(raw);
    if (!value || typeof value !== "object" || Array.isArray(value)) return {};
    return Object.fromEntries(Object.entries(value).filter(([, open]) => typeof open === "boolean")) as GroupState;
  } catch {
    return {};
  }
}
