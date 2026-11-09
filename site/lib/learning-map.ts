/**
 * The learning map on the home page: a curated path through the notebooks,
 * drawn as a pipeline DAG. Columns run left to right; an edge means "read this
 * first". The build fails if a node names a notebook the registry does not list.
 */

export type MapNode = { slug: string; label: string };
export type MapColumn = { title: string; nodes: MapNode[] };
export type MapEdge = readonly [from: string, to: string];

export const LEARNING_MAP_COLUMNS: MapColumn[] = [
  {
    title: "Foundations",
    nodes: [
      { slug: "python-01-values-and-types", label: "Python basics" },
      { slug: "python-02-collections", label: "Python collections" },
      { slug: "sql-01-basics", label: "SQL basics" },
    ],
  },
  {
    title: "Process and model",
    nodes: [
      { slug: "sql-08-window-functions", label: "Window functions" },
      { slug: "pyspark-00-overview", label: "PySpark" },
      { slug: "data-modeling", label: "Data modeling" },
    ],
  },
  {
    title: "Orchestrate and test",
    nodes: [
      { slug: "airflow", label: "Airflow" },
      { slug: "dbt", label: "dbt" },
      { slug: "data-quality", label: "Data quality" },
    ],
  },
  {
    title: "Store",
    nodes: [
      { slug: "parquet", label: "Parquet" },
      { slug: "delta", label: "Delta Lake" },
      { slug: "iceberg", label: "Apache Iceberg" },
    ],
  },
  {
    title: "Stream",
    nodes: [
      { slug: "kafka", label: "Kafka" },
      { slug: "flink", label: "Flink" },
    ],
  },
];

export const LEARNING_MAP_EDGES: MapEdge[] = [
  ["python-01-values-and-types", "python-02-collections"],
  ["python-02-collections", "pyspark-00-overview"],
  ["sql-01-basics", "sql-08-window-functions"],
  ["sql-01-basics", "data-modeling"],
  ["sql-08-window-functions", "pyspark-00-overview"],
  ["pyspark-00-overview", "airflow"],
  ["data-modeling", "dbt"],
  ["dbt", "data-quality"],
  ["airflow", "parquet"],
  ["dbt", "delta"],
  ["parquet", "delta"],
  ["delta", "iceberg"],
  ["delta", "kafka"],
  ["iceberg", "flink"],
  ["kafka", "flink"],
];

export const MAP_GEOMETRY = {
  left: 20,
  top: 50,
  columnWidth: 200,
  nodeWidth: 150,
  nodeHeight: 40,
  rowPitch: 70,
  headerY: 32,
  bottomPadding: 15,
} as const;

export type PlacedNode = MapNode & { column: number; row: number; x: number; y: number };
export type PlacedEdge = { from: string; to: string; d: string };
export type MapLayout = {
  width: number;
  height: number;
  headers: { title: string; x: number }[];
  nodes: PlacedNode[];
  edges: PlacedEdge[];
};

/** Place nodes on a grid (short columns are centred) and route each edge. */
export function layoutMap(columns: MapColumn[], edges: readonly MapEdge[]): MapLayout {
  const g = MAP_GEOMETRY;
  const maxRows = Math.max(...columns.map((column) => column.nodes.length));
  const nodes: PlacedNode[] = columns.flatMap((column, columnIndex) => {
    const offset = ((maxRows - column.nodes.length) * g.rowPitch) / 2;
    return column.nodes.map((node, row) => ({
      ...node,
      column: columnIndex,
      row,
      x: g.left + columnIndex * g.columnWidth,
      y: g.top + offset + row * g.rowPitch,
    }));
  });
  const bySlug = new Map(nodes.map((node) => [node.slug, node]));

  const placedEdges = edges.flatMap(([from, to]) => {
    const a = bySlug.get(from);
    const b = bySlug.get(to);
    if (!a || !b) return [];
    if (a.column === b.column) {
      const x = a.x + g.nodeWidth / 2;
      const [top, bottom] = a.y < b.y ? [a, b] : [b, a];
      return [{ from, to, d: `M${x} ${top.y + g.nodeHeight} L${x} ${bottom.y}` }];
    }
    const x1 = a.x + g.nodeWidth;
    const y1 = a.y + g.nodeHeight / 2;
    const x2 = b.x;
    const y2 = b.y + g.nodeHeight / 2;
    const mid = (x1 + x2) / 2;
    const d = y1 === y2 ? `M${x1} ${y1} L${x2} ${y2}` : `M${x1} ${y1} C${mid} ${y1} ${mid} ${y2} ${x2} ${y2}`;
    return [{ from, to, d }];
  });

  return {
    width: g.left * 2 + (columns.length - 1) * g.columnWidth + g.nodeWidth,
    height: g.top + maxRows * g.rowPitch - (g.rowPitch - g.nodeHeight) + g.bottomPadding,
    headers: columns.map((column, index) => ({ title: column.title, x: g.left + 2 + index * g.columnWidth })),
    nodes,
    edges: placedEdges,
  };
}

/** Problems that would draw a broken map; empty when the map is valid. */
export function validateMap(columns: MapColumn[], edges: readonly MapEdge[], knownSlugs: Set<string>): string[] {
  const problems: string[] = [];
  const position = new Map<string, { column: number; row: number }>();
  columns.forEach((column, columnIndex) =>
    column.nodes.forEach((node, row) => {
      if (position.has(node.slug)) problems.push(`${node.slug} appears more than once`);
      if (!knownSlugs.has(node.slug)) problems.push(`${node.slug} is not a registered notebook`);
      position.set(node.slug, { column: columnIndex, row });
    }),
  );
  for (const [from, to] of edges) {
    const a = position.get(from);
    const b = position.get(to);
    if (!a || !b) {
      problems.push(`edge ${from} -> ${to} names a node that is not on the map`);
      continue;
    }
    const sameColumnNeighbours = a.column === b.column && Math.abs(a.row - b.row) === 1;
    const nextColumn = b.column === a.column + 1;
    if (!sameColumnNeighbours && !nextColumn) {
      problems.push(`edge ${from} -> ${to} must join neighbours in a column or move one column right`);
    }
  }
  return problems;
}
