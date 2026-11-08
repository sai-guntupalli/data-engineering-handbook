"use client";

import Link from "next/link";
import { MAP_GEOMETRY } from "@/lib/learning-map";
import type { LearningMapView } from "@/lib/notebooks";
import { fractionOf, statusOf, type NotebookStatus } from "@/lib/progress";
import { useProgress } from "./progress-store";

const RING = 2 * Math.PI * 6;
const EDGE_STAGGER_SECONDS = 0.08;

function StatusGlyph({ status, fraction }: { status: NotebookStatus; fraction: number }) {
  if (status === "done") {
    return (
      <>
        <circle className="s-done" cx="18" cy="20" r="7" />
        <path className="s-check" d="M14.8 20.2l2.2 2.2 4.2-4.4" />
      </>
    );
  }
  if (status === "in-progress") {
    return (
      <>
        <circle className="s-track" cx="18" cy="20" r="6" />
        <circle
          className="s-arc"
          cx="18"
          cy="20"
          r="6"
          strokeDasharray={`${Math.max(fraction * RING, 2)} ${RING}`}
          transform="rotate(-90 18 20)"
        />
      </>
    );
  }
  return <circle className="s-idle" cx="18" cy="20" r="6" />;
}

/** The core path as a DAG. Nodes are coloured by this browser's reading progress. */
export function LearningMap({ map }: { map: LearningMapView }) {
  const progress = useProgress();
  const g = MAP_GEOMETRY;

  const entryOf = (slug: string) => progress.notebooks[map.targets[slug].repoPath];
  const statuses = Object.fromEntries(map.nodes.map((node) => [node.slug, statusOf(entryOf(node.slug))]));
  const done = map.nodes.filter((node) => statuses[node.slug] === "done").length;

  // The highlighted node: the most recently read notebook on the map, else the first one not started.
  const inProgress = map.nodes
    .filter((node) => statuses[node.slug] === "in-progress")
    .sort((a, b) => (entryOf(b.slug)?.updatedAt ?? 0) - (entryOf(a.slug)?.updatedAt ?? 0));
  const current = inProgress[0]?.slug ?? map.nodes.find((node) => statuses[node.slug] === "not-started")?.slug;

  const summary =
    done + inProgress.length === 0
      ? `A suggested order through ${map.nodes.length} core notebooks. Start anywhere; the map fills in as you read.`
      : `${done} of ${map.nodes.length} notebooks done on the core path`;

  return (
    <section className="panel map" aria-labelledby="map-title">
      <div className="map-head">
        <div>
          <h2 id="map-title">Learning map</h2>
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
      <div className="map-scroll">
        <svg viewBox={`0 0 ${map.width} ${map.height}`} role="group" aria-label="Learning map of the core notebooks">
          {map.headers.map((header) => (
            <text key={header.title} className="col-h" x={header.x} y={g.headerY}>
              {header.title}
            </text>
          ))}
          {map.edges.map((edge, index) => (
            <path
              key={`${edge.from}-${edge.to}`}
              className={statuses[edge.from] === "done" ? "edge is-done" : "edge"}
              style={{ "--delay": `${(index * EDGE_STAGGER_SECONDS).toFixed(2)}s` } as React.CSSProperties}
              d={edge.d}
            />
          ))}
          {map.nodes.map((node) => {
            const status = statuses[node.slug];
            const entry = entryOf(node.slug);
            const sub =
              status === "done"
                ? "Done"
                : status === "in-progress"
                  ? `${entry?.read.length ?? 0} of ${entry?.total ?? 0} sections`
                  : "Not started";
            const isCurrent = node.slug === current;
            return (
              <Link
                key={node.slug}
                href={map.targets[node.slug].href}
                className={isCurrent ? "node is-current" : "node"}
                aria-label={`${map.targets[node.slug].title}: ${sub}`}
              >
                <g transform={`translate(${node.x} ${node.y})`}>
                  {isCurrent ? (
                    <rect className="halo" x="-3" y="-3" width={g.nodeWidth + 6} height={g.nodeHeight + 6} rx="12" />
                  ) : null}
                  <rect className="frame" width={g.nodeWidth} height={g.nodeHeight} rx="9" />
                  <StatusGlyph status={status} fraction={fractionOf(entry)} />
                  <text className="n-title" x="34" y="18">
                    {node.label}
                  </text>
                  <text className="n-sub" x="34" y="31">
                    {sub}
                  </text>
                </g>
              </Link>
            );
          })}
        </svg>
      </div>
    </section>
  );
}
