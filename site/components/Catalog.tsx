"use client";

import { useMemo, useState } from "react";
import { type GroupSection, anchorFor } from "@/lib/notebook-groups";
import type { NotebookGroupView } from "@/lib/notebooks";
import { CatalogTable } from "./CatalogTable";
import { useStarred } from "./starred";
import { setUrlParam, useUrlParam } from "./url-state";

const PREVIEW_ROWS = 12;
const SECTION_ROWS: { value: GroupSection; label: string }[] = [
  { value: "learn", label: "Learn" },
  { value: "practice", label: "Practice" },
];

type FilterOption = { value: string; label: string; count: number; section?: GroupSection };

/** One labelled row of filter buttons. Each row is its own group for screen readers. */
function FilterRow({
  label,
  options,
  filter,
  isAll,
  onSelect,
}: {
  label: string;
  options: FilterOption[];
  filter: string;
  isAll: boolean;
  onSelect: (value: string) => void;
}) {
  if (options.length === 0) return null;
  return (
    <div className="filter-row">
      <span className="filter-label" aria-hidden>
        {label}
      </span>
      <div className="segmented" role="group" aria-label={`Filter: ${label}`}>
        {options.map((option) => (
          <button
            key={option.label}
            type="button"
            aria-pressed={(isAll ? "" : filter) === option.value}
            onClick={() => onSelect(option.value)}
          >
            {option.label} <span className="count">{option.count}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
const STARRED = "starred";

/** Every notebook as a filterable table. The filter lives in ?group= so sidebar links can set it. */
export function Catalog({ groups }: { groups: NotebookGroupView[] }) {
  const filter = useUrlParam("group");
  const starred = useStarred();
  const [expanded, setExpanded] = useState(false);

  const all = useMemo(() => groups.flatMap((group) => group.notebooks), [groups]);
  const activeGroup = groups.find((group) => anchorFor(group.label) === filter);
  const visible = filter === STARRED ? all.filter((notebook) => starred.has(notebook.repoPath)) : (activeGroup?.notebooks ?? all);
  const isAll = filter !== STARRED && !activeGroup;
  const shown = isAll && !expanded ? visible.slice(0, PREVIEW_ROWS) : visible;

  const options: FilterOption[] = [
    { value: "", label: "All", count: all.length },
    { value: STARRED, label: "Starred", count: starred.size },
    ...groups.map((group) => ({
      value: anchorFor(group.label),
      label: group.shortLabel,
      count: group.notebooks.length,
      section: group.section,
    })),
  ];
  const select = (value: string) => {
    setUrlParam("group", value);
    setExpanded(false);
  };
  const caption = filter === STARRED ? "Starred notebooks" : (activeGroup?.label ?? "All notebooks");

  return (
    <section className="panel catalog" aria-labelledby="catalog-title">
      <h2 id="catalog-title" className="sr-only">
        Catalog
      </h2>
      <div className="catalog-tools">
        <FilterRow label="Show" options={[options[0], options[1]]} filter={filter} isAll={isAll} onSelect={select} />
        {SECTION_ROWS.map((row) => (
          <FilterRow
            key={row.value}
            label={row.label}
            options={options.slice(2).filter((option) => option.section === row.value)}
            filter={filter}
            isAll={isAll}
            onSelect={select}
          />
        ))}
      </div>

      {shown.length > 0 ? (
        <CatalogTable notebooks={shown} caption={caption} />
      ) : (
        <div className="empty-state">
          <h2>No starred notebooks yet</h2>
          <p>Star a notebook from its row or its page, and it stays here on this device.</p>
        </div>
      )}

      {isAll && visible.length > PREVIEW_ROWS ? (
        <div className="catalog-foot">
          <span>
            Showing {shown.length} of {visible.length}
          </span>
          <button type="button" className="btn btn-sm" onClick={() => setExpanded((value) => !value)}>
            {expanded ? "Show fewer" : `Show all ${visible.length} notebooks`}
          </button>
        </div>
      ) : null}
    </section>
  );
}
