"use client";

import { useEffect, useSyncExternalStore } from "react";
import { CaretDoubleRight, ListBullets, SidebarSimple } from "@phosphor-icons/react";
import { PANEL_KEY_PREFIX, type Panel } from "@/lib/boot";

const PANEL_EVENT = "de-handbook:panelchange";
const SHORTCUTS: Record<string, Panel> = { "[": "sidebar", "]": "toc" };

function subscribe(callback: () => void) {
  window.addEventListener(PANEL_EVENT, callback);
  return () => window.removeEventListener(PANEL_EVENT, callback);
}

/** Whether a panel is collapsed. Expanded during server rendering; the boot script has the real value. */
export function usePanelCollapsed(panel: Panel): boolean {
  return useSyncExternalStore(
    subscribe,
    () => document.documentElement.dataset[panel] === "collapsed",
    () => false,
  );
}

export function togglePanel(panel: Panel) {
  const root = document.documentElement;
  const collapse = root.dataset[panel] !== "collapsed";
  if (collapse) {
    root.dataset[panel] = "collapsed";
  } else {
    delete root.dataset[panel];
  }
  try {
    window.localStorage.setItem(`${PANEL_KEY_PREFIX}${panel}`, collapse ? "collapsed" : "expanded");
  } catch {
    // Storage blocked: the panel still toggles for this page view.
  }
  window.dispatchEvent(new Event(PANEL_EVENT));
}

function isTyping(target: EventTarget | null): boolean {
  const element = target as HTMLElement | null;
  return !!element && (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.isContentEditable);
}

/** [ toggles the sidebar and ] the table of contents, unless the reader is typing. */
export function PanelShortcuts() {
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const panel = SHORTCUTS[event.key];
      if (!panel || event.metaKey || event.ctrlKey || event.altKey || isTyping(event.target)) return;
      event.preventDefault();
      togglePanel(panel);
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, []);
  return null;
}

/** Top-bar button that collapses the sidebar to an icon rail. */
export function SidebarToggle() {
  const collapsed = usePanelCollapsed("sidebar");
  const label = collapsed ? "Expand sidebar" : "Collapse sidebar";
  return (
    <button
      type="button"
      className="btn btn-ghost btn-icon sidebar-toggle"
      onClick={() => togglePanel("sidebar")}
      aria-controls="app-sidebar"
      aria-expanded={!collapsed}
      aria-label={label}
      title={`${label} ( [ )`}
    >
      <SidebarSimple size={18} aria-hidden />
    </button>
  );
}

/** Button at the top of the table of contents that folds it into a narrow rail. */
export function TocToggle() {
  const collapsed = usePanelCollapsed("toc");
  const label = collapsed ? "Show table of contents" : "Hide table of contents";
  return (
    <button
      type="button"
      className="btn btn-ghost btn-icon btn-sm toc-toggle"
      onClick={() => togglePanel("toc")}
      aria-controls="toc-body"
      aria-expanded={!collapsed}
      aria-label={label}
      title={`${label} ( ] )`}
    >
      {collapsed ? <ListBullets size={16} aria-hidden /> : <CaretDoubleRight size={14} aria-hidden />}
    </button>
  );
}
