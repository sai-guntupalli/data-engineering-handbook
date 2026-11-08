import type { CSSProperties } from "react";

/** Inline style that points a tile (`--tile`) or dot (`--dot`) at a group's colour token. */
export function toneStyle(tone: string, property: "--tile" | "--dot"): CSSProperties {
  return { [property]: `var(--tone-${tone})` } as CSSProperties;
}
