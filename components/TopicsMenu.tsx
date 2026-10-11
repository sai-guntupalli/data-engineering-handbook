"use client";

import { useEffect, useRef, useState } from "react";
import { CaretDown } from "@phosphor-icons/react";
import { PRACTICE_GROUP, TOPIC_GROUPS, anchorFor } from "@/lib/notebook-groups";

/**
 * Header dropdown listing every group (hands-on practice + the topic groups)
 * with real notebook counts. Closes on Escape, outside click, and navigation.
 */
export function TopicsMenu() {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    const onPointerDown = (event: PointerEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener("keydown", onKeyDown);
    document.addEventListener("pointerdown", onPointerDown);
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.removeEventListener("pointerdown", onPointerDown);
    };
  }, [open]);

  const groups = [PRACTICE_GROUP, ...TOPIC_GROUPS];

  return (
    <div className="topics-menu" ref={rootRef}>
      <button
        type="button"
        className="topics-trigger"
        aria-haspopup="true"
        aria-expanded={open}
        onClick={() => setOpen((value) => !value)}
      >
        Topics
        <CaretDown size={13} weight="bold" className="topics-caret" aria-hidden />
      </button>
      {open ? (
        <div className="topics-panel" aria-label="All notebook groups">
          {groups.map((group) => (
            <a
              key={group.label}
              href={`/#${anchorFor(group.label)}`}
              onClick={() => setOpen(false)}
            >
              <span>{group.label}</span>
              <span className="topics-count">{group.slugs.length}</span>
            </a>
          ))}
        </div>
      ) : null}
    </div>
  );
}