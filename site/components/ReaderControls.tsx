"use client";

import { useState } from "react";
import { Check, CheckCircle, Copy, LinkSimple } from "@phosphor-icons/react";
import { statusOf } from "@/lib/progress";
import { recordDone, useProgress } from "./progress-store";

const COPIED_MS = 1800;

async function copyText(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Clipboard blocked (insecure context or permissions): the text stays selectable.
    return false;
  }
}

function useCopied(): [boolean, (text: string) => void] {
  const [copied, setCopied] = useState(false);
  const copy = (text: string) => {
    void copyText(text).then((ok) => {
      if (!ok) return;
      setCopied(true);
      window.setTimeout(() => setCopied(false), COPIED_MS);
    });
  };
  return [copied, copy];
}

export function CopyLinkButton() {
  const [copied, copy] = useCopied();
  return (
    <button type="button" className="btn btn-ghost" onClick={() => copy(window.location.href.split("#")[0])}>
      {copied ? <Check size={15} aria-hidden /> : <LinkSimple size={15} aria-hidden />}
      {copied ? "Link copied" : "Copy link"}
    </button>
  );
}

/** Copies the code of the cell it sits in, read from the page so the source is not sent twice. */
export function CopyCodeButton() {
  const [copied, copy] = useCopied();
  return (
    <button
      type="button"
      className="btn btn-ghost btn-sm"
      onClick={(event) => {
        const code = event.currentTarget.closest(".cell")?.querySelector("pre")?.textContent ?? "";
        copy(code);
      }}
    >
      {copied ? <Check size={14} aria-hidden /> : <Copy size={14} aria-hidden />}
      {copied ? "Copied" : "Copy"}
    </button>
  );
}

/** End-of-notebook panel: mark the notebook done, or undo it. */
export function MarkDonePanel({ repoPath, total }: { repoPath: string; total: number }) {
  const progress = useProgress();
  const done = statusOf(progress.notebooks[repoPath]) === "done";
  return (
    <section className="panel reader-done" aria-label="Notebook status">
      <div>
        <strong>{done ? "You finished this notebook" : "Finished reading?"}</strong>
        <p>
          {done
            ? "It shows as done on the learning map and in the catalog, on this device."
            : "Mark it done to fill it in on the learning map. Progress stays in this browser."}
        </p>
      </div>
      <button type="button" className={done ? "btn is-done" : "btn btn-primary"} onClick={() => recordDone(repoPath, !done, total)}>
        <CheckCircle size={16} weight={done ? "fill" : "regular"} aria-hidden />
        {done ? "Marked done" : "Mark as done"}
      </button>
    </section>
  );
}
