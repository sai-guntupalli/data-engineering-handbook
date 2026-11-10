/**
 * Which notebooks the reader's pager links to. A notebook on the learning path
 * follows the path (Parquet -> Delta Lake -> Iceberg), even across tools. Any
 * other notebook follows its tool, and a tool with a single notebook follows its
 * category, so every page has somewhere to go next.
 */
export type ReadingOrder = {
  /** Shown after "Next", e.g. "on the learning path" or "in PySpark". */
  label: string;
  slugs: string[];
};

export type PagerChoice = { previous: string | null; next: string | null; label: string };

export function pickNeighbours(slug: string, orders: ReadingOrder[]): PagerChoice | null {
  for (const order of orders) {
    const at = order.slugs.indexOf(slug);
    if (at === -1 || order.slugs.length < 2) continue;
    return { previous: order.slugs[at - 1] ?? null, next: order.slugs[at + 1] ?? null, label: order.label };
  }
  return null;
}
