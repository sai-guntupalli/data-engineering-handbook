"use client";

import { useEffect, useState } from "react";
import { Check } from "@phosphor-icons/react";
import type { Section } from "@/lib/notebook-parse";
import { fractionOf } from "@/lib/progress";
import { TocToggle } from "./panels";
import { recordSectionRead, useProgress } from "./progress-store";
import { useUrlHash } from "./url-state";

/** A heading counts as reached once its top passes this share of the viewport height. */
const REACHED_AT = 0.35;
const END_SENTINEL_ID = "notebook-end";
/** A fast scroll can pass two short sections in one frame; a bigger jump is a link, not reading. */
const MAX_SCROLL_STEP = 2;

type TocSection = Pick<Section, "id" | "title">;

/**
 * Tracks reading as the page scrolls: a section is read once the reader scrolls
 * on into the next heading (or reaches the end of the last one), and the current
 * section is highlighted. Renders the "On this page" list and the progress card.
 */
export function ReaderToc({
  repoPath,
  sections,
  minutes,
}: {
  repoPath: string;
  sections: TocSection[];
  minutes: number;
}) {
  const progress = useProgress();
  const entry = progress.notebooks[repoPath];
  const read = new Set(entry?.read ?? []);
  const [current, setCurrent] = useState(-1);

  // A client-side navigation to /notebooks/x/#section renders the page before
  // the URL carries the fragment, so Next never jumps to the heading. Follow
  // the fragment instead and jump whenever it names a heading on this page.
  const hash = useUrlHash();
  useEffect(() => {
    // Instant, so the jump is one step and does not count the sections it passes as read.
    if (hash) document.getElementById(hash)?.scrollIntoView({ block: "start", behavior: "instant" });
  }, [hash, repoPath]);

  useEffect(() => {
    if (sections.length === 0) return;
    let frame = 0;
    // Sections count as read only when the reader scrolls from one heading into
    // the next. Jumping ahead through a link or the table of contents skips the
    // sections in between without marking them.
    let previous: number | null = null;
    const measure = () => {
      frame = 0;
      const line = window.innerHeight * REACHED_AT;
      let reached = -1;
      sections.forEach((section, index) => {
        const heading = document.getElementById(section.id);
        if (heading && heading.getBoundingClientRect().top < line) reached = index;
      });
      setCurrent(reached);
      if (previous !== null && previous >= 0 && reached > previous && reached - previous <= MAX_SCROLL_STEP) {
        for (let index = previous; index < reached; index += 1) {
          recordSectionRead(repoPath, sections[index].id, sections.length);
        }
      }
      previous = reached;
      const end = document.getElementById(END_SENTINEL_ID);
      const last = sections.length - 1;
      if (reached === last && end && end.getBoundingClientRect().top < window.innerHeight) {
        recordSectionRead(repoPath, sections[last].id, sections.length);
      }
    };
    const onScroll = () => {
      if (!frame) frame = window.requestAnimationFrame(measure);
    };
    measure();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, [repoPath, sections]);

  const fraction = fractionOf(entry);
  const left = Math.max(0, Math.round(minutes * (1 - fraction)));

  return (
    <>
      <div className="read-progress" aria-hidden>
        <span style={{ width: `${fraction * 100}%` }} />
      </div>
      <details className="toc-narrow" aria-label="On this page">
        <summary>On this page · {sections.length} sections</summary>
        <ol>
          {sections.map((section, index) => (
            <li key={section.id}>
              <a href={`#${section.id}`} aria-current={index === current ? "true" : undefined}>
                {section.title}
              </a>
            </li>
          ))}
        </ol>
      </details>
      <aside className="toc" aria-label="On this page">
        <div className="toc-head">
          <p className="toc-title">On this page</p>
          <TocToggle />
        </div>
        <div className="toc-body" id="toc-body">
          <ol>
            {sections.map((section, index) => (
              <li key={section.id}>
                <a
                  href={`#${section.id}`}
                  className={read.has(section.id) ? "is-read" : undefined}
                  aria-current={index === current ? "true" : undefined}
                >
                  <span className="state" aria-hidden>
                    {read.has(section.id) ? <Check size={9} weight="bold" /> : null}
                  </span>
                  {section.title}
                </a>
              </li>
            ))}
          </ol>
          <div className="toc-card">
            <strong>
              {read.size} of {sections.length} sections read
            </strong>
            <div className={fraction >= 1 ? "bar is-done" : "bar"}>
              <span style={{ width: `${fraction * 100}%` }} />
            </div>
            <small>{fraction >= 1 ? "Finished" : `About ${left} minutes left`}</small>
          </div>
        </div>
      </aside>
    </>
  );
}

export function EndSentinel() {
  return <div id={END_SENTINEL_ID} aria-hidden />;
}
