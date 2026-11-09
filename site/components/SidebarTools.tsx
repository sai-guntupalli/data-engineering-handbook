"use client";

import Link from "next/link";
import { useSyncExternalStore } from "react";
import { CaretRight, Star } from "@phosphor-icons/react";
import { SIDEBAR_GROUPS_KEY, isGroupExpanded, parseGroupState, toolStarKey, type GroupState } from "@/lib/sidebar";
import { toneStyle } from "@/lib/tone";
import { toggleStar, useStarred } from "./starred";

export type SidebarTool = { folder: string; label: string; href: string; tone: string; count: number };
export type SidebarCategory = { id: string; label: string; tools: SidebarTool[] };

const GROUPS_EVENT = "de-handbook:sidebargroupschange";
const EMPTY_STATE: GroupState = {};

let groupsRaw: string | null | undefined;
let groupsCache: GroupState = EMPTY_STATE;

function subscribeGroups(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener(GROUPS_EVENT, callback);
  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener(GROUPS_EVENT, callback);
  };
}

function getGroupsSnapshot(): GroupState {
  let raw: string | null;
  try {
    raw = window.localStorage.getItem(SIDEBAR_GROUPS_KEY);
  } catch {
    return groupsCache;
  }
  if (raw !== groupsRaw) {
    groupsRaw = raw;
    groupsCache = parseGroupState(raw);
  }
  return groupsCache;
}

function setGroupExpanded(categoryId: string, expanded: boolean) {
  const next = { ...getGroupsSnapshot(), [categoryId]: expanded };
  try {
    window.localStorage.setItem(SIDEBAR_GROUPS_KEY, JSON.stringify(next));
  } catch {
    // Storage blocked: keep the choice for this page view only.
    groupsRaw = JSON.stringify(next);
    groupsCache = next;
  }
  window.dispatchEvent(new Event(GROUPS_EVENT));
}

function ToolRow({ tool, starred, current }: { tool: SidebarTool; starred: boolean; current: boolean }) {
  const action = starred ? `Unstar the ${tool.label} tool` : `Star the ${tool.label} tool`;
  return (
    <div className={starred ? "nav-row is-starred" : "nav-row"}>
      <Link className="nav-link" data-tip={tool.label} href={tool.href} aria-current={current ? "page" : undefined}>
        <span className="dot" style={toneStyle(tool.tone, "--dot")} aria-hidden />
        <span className="nav-text">{tool.label}</span>
        <span className="nav-count">{tool.count}</span>
      </Link>
      <button
        type="button"
        className="nav-star"
        onClick={() => toggleStar(toolStarKey(tool.folder))}
        aria-pressed={starred}
        aria-label={action}
        title={action}
      >
        <Star size={13} weight={starred ? "fill" : "regular"} aria-hidden />
      </button>
    </div>
  );
}

/**
 * Tools in the sidebar: starred tools first, then one collapsible group per category.
 * Groups remember their state in this browser. On narrow screens and in the icon rail
 * every tool shows, because there is no room for group headers.
 */
export function SidebarTools({ categories, currentTool }: { categories: SidebarCategory[]; currentTool?: string }) {
  const starred = useStarred();
  const groups = useSyncExternalStore(subscribeGroups, getGroupsSnapshot, () => EMPTY_STATE);
  const starredTools = categories.flatMap((category) => category.tools).filter((tool) => starred.has(toolStarKey(tool.folder)));

  return (
    <>
      {starredTools.length > 0 ? (
        <div className="nav-group is-starred-group">
          <div className="nav-label">Starred tools</div>
          {starredTools.map((tool) => (
            <ToolRow key={tool.folder} tool={tool} starred current={tool.folder === currentTool} />
          ))}
        </div>
      ) : null}

      {categories.map((category) => {
        const folders = category.tools.map((tool) => tool.folder);
        const expanded = isGroupExpanded(groups, category.id, folders, currentTool);
        const itemsId = `nav-group-${category.id}`;
        return (
          <div key={category.id} className="nav-group" data-expanded={expanded}>
            <button
              type="button"
              className="nav-group-toggle"
              aria-expanded={expanded}
              aria-controls={itemsId}
              onClick={() => setGroupExpanded(category.id, !expanded)}
            >
              <CaretRight size={11} weight="bold" className="nav-caret" aria-hidden />
              <span>{category.label}</span>
              <span className="nav-group-count">{category.tools.length}</span>
            </button>
            <div className="nav-group-items" id={itemsId}>
              {category.tools.map((tool) => (
                <ToolRow
                  key={tool.folder}
                  tool={tool}
                  starred={starred.has(toolStarKey(tool.folder))}
                  current={tool.folder === currentTool}
                />
              ))}
            </div>
          </div>
        );
      })}
    </>
  );
}
