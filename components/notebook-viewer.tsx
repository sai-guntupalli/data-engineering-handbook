"use client";

import { CircleNotch, Play, Sparkle, X } from "@phosphor-icons/react";
import { useEffect, useLayoutEffect, useRef, useState } from "react";

import { executeCell, resetKernel, streamChat, type ExecResponse } from "@/lib/interactive-api";
import type {
  CodeSectionBlock,
  NotebookPage,
  NotebookSection,
} from "@/lib/notebook-content";

/** The one-line kernel contract, shown once under the first code cell. */
const KERNEL_HINT =
  "The kernel persists top-to-bottom — variables stay between Runs. Reload resets it.";

const STATUS_NOTES: Partial<Record<ExecResponse["status"], string>> = {
  timeout: "The cell ran past the 60 s limit and was stopped.",
  busy: "The kernel is still busy with an earlier cell. Wait for it, or Reload to reset.",
  illustrative: "This cell was refused — it is marked ILLUSTRATIVE and never runs here.",
};

type ElaborateState = {
  open: boolean;
  busy: boolean;
  started: boolean;
  text: string;
  error: string | null;
};

const ELABORATE_CLOSED: ElaborateState = { open: false, busy: false, started: false, text: "", error: null };

/**
 * Reading view of a parsed notebook: markdown sections carry an Elaborate
 * panel, code cells are editable and runnable. All interactivity talks to the
 * local FastAPI backend through lib/interactive-api; when it is absent the
 * output areas explain themselves instead of crashing the page.
 */
export function NotebookViewer({ page }: { page: NotebookPage }) {
  const outline = page.sections.map((section) => section.heading);
  const kernelHintSectionId = page.sections.find((section) =>
    section.blocks.some((block) => block.kind === "code"),
  )?.id;
  // Make "Reload resets it" true: a fresh page load starts the notebook's
  // kernel empty. Fire-and-forget once per page load (the ref guard keeps
  // React's dev double-invoke from resetting twice).
  const resetFired = useRef(false);
  useEffect(() => {
    if (resetFired.current) return;
    resetFired.current = true;
    void resetKernel(page.slug);
  }, [page.slug]);

  return (
    <div className="viewer">
      {page.sections.map((section, index) => (
        <NotebookSectionView
          key={section.id}
          section={section}
          notebook={page.slug}
          notebookTitle={page.title}
          repoPath={page.repoPath}
          outline={outline}
          neighbors={surroundingCellSources(page.sections, index)}
          showKernelHint={kernelHintSectionId === section.id}
        />
      ))}
    </div>
  );
}

/** Up to three cell sources on each side of the section, for the tutor's context. */
function surroundingCellSources(sections: NotebookSection[], index: number): string[] {
  const before: string[] = [];
  for (let position = index - 1; position >= 0 && before.length < 3; position--) {
    before.unshift(...sections[position].blocks.map((block) => block.source));
  }
  const after: string[] = [];
  for (let position = index + 1; position < sections.length && after.length < 3; position++) {
    after.push(...sections[position].blocks.map((block) => block.source));
  }
  return [...before.slice(-3), ...after.slice(0, 3)];
}

function NotebookSectionView({
  section,
  notebook,
  notebookTitle,
  repoPath,
  outline,
  neighbors,
  showKernelHint,
}: {
  section: NotebookSection;
  notebook: string;
  notebookTitle: string;
  repoPath: string;
  outline: string[];
  neighbors: string[];
  showKernelHint: boolean;
}) {
  const [elaborate, setElaborate] = useState<ElaborateState>(ELABORATE_CLOSED);
  const firstCodeBlockIndex = section.blocks.findIndex((block) => block.kind === "code");
  const sectionMarkdown = section.blocks
    .filter((block) => block.kind === "markdown")
    .map((block) => block.source)
    .join("\n\n");

  /** First click streams; with a cached result a re-click collapses (re-opening
   *  replays it), but a failed stream is not cached — its re-click re-requests
   *  so the failure is tryable. */
  const toggleElaborate = () => {
    if (elaborate.busy) return;
    if (elaborate.open && elaborate.started) {
      setElaborate((state) => ({ ...state, open: false }));
      return;
    }
    setElaborate((state) => ({ ...state, open: true }));
    if (elaborate.started) return;
    setElaborate((state) => ({ ...state, started: true, busy: true, text: "", error: null }));
    void streamChat(
      {
        mode: "elaborate",
        section_markdown: sectionMarkdown,
        context_cells: neighbors,
        notebook_title: notebookTitle,
        outline,
      },
      (text) => setElaborate((state) => ({ ...state, text: state.text + text })),
    ).then((error) =>
      setElaborate((state) => ({ ...state, busy: false, error, started: error === null })),
    );
  };

  return (
    <section id={section.id} className="nb-section" data-nb-section-id={section.id}>
      <div className="nb-section-header">
        {section.id === "intro" ? null : <h2>{section.heading}</h2>}
        {sectionMarkdown ? (
          <button
            type="button"
            className="elaborate-button"
            onClick={toggleElaborate}
            disabled={elaborate.busy}
            aria-expanded={elaborate.open}
            title="Streams a tutor explanation of this section from the local backend"
          >
            {elaborate.busy ? (
              <CircleNotch size={16} className="cell-spin" />
            ) : (
              <Sparkle size={16} weight="bold" />
            )}
            {elaborate.busy ? "Elaborating" : "Elaborate"}
          </button>
        ) : null}
      </div>
      <div className="nb-blocks">
        {section.blocks.map((block, blockIndex) => {
          if (block.kind === "markdown") {
            return (
              <div
                key={`markdown-${blockIndex}`}
                className="nb-markdown"
                dangerouslySetInnerHTML={{ __html: block.html }}
              />
            );
          }
          return (
            <CodeCellView
              key={block.cellIndex}
              block={block}
              notebook={notebook}
              repoPath={repoPath}
              withHint={showKernelHint && blockIndex === firstCodeBlockIndex}
            />
          );
        })}
      </div>
      {elaborate.open ? (
        <div className="elaborate-panel" role="region" aria-label={`Tutor notes on ${section.heading}`}>
          <div className="elaborate-panel-head">
            <span className="elaborate-title">Tutor notes</span>
            <button
              type="button"
              className="elaborate-close"
              onClick={() => setElaborate((state) => ({ ...state, open: false }))}
              aria-label="Collapse elaboration"
            >
              <X size={14} />
            </button>
          </div>
          {elaborate.text ? <p className="elaborate-text">{elaborate.text}</p> : null}
          {elaborate.error ? <p className="elaborate-error">{elaborate.error}</p> : null}
          {elaborate.busy && !elaborate.text ? (
            <p className="elaborate-text muted">Waiting for the tutor…</p>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}

/** A code area that never crops: grown to its content on every change
 *  (auto → scrollHeight), soft-wrapped, no inner scrolling and no resize grip.
 *  resize/overflow stay inline because the fit contract lives here — the
 *  stylesheet cannot express "matches this element's measured height". */
function CodeTextarea({
  value,
  onChange,
  ariaLabel,
}: {
  value: string;
  onChange?: (next: string) => void;
  ariaLabel: string;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${el.scrollHeight}px`;
  }, [value]);
  return (
    <textarea
      ref={ref}
      className="cell-textarea"
      value={value}
      onChange={onChange ? (event) => onChange(event.target.value) : undefined}
      readOnly={!onChange}
      spellCheck={false}
      style={{ resize: "none", overflow: "hidden" }}
      aria-label={ariaLabel}
    />
  );
}

function CodeCellView({
  block,
  notebook,
  repoPath,
  withHint,
}: {
  block: CodeSectionBlock;
  notebook: string;
  repoPath: string;
  withHint: boolean;
}) {
  const [source, setSource] = useState(block.source);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<ExecResponse | null>(null);

  /** An untouched cell runs by its notebook index (so the backend's
   *  ILLUSTRATIVE guard stays active); an edited cell runs as ad-hoc code. */
  const run = () => {
    const edited = source !== block.source;
    setRunning(true);
    void executeCell(notebook, repoPath, edited ? null : block.cellIndex, edited ? source : null)
      .then((response) => setResult(response))
      .finally(() => setRunning(false));
  };

  if (block.illustrative) {
    return (
      <div className="nb-cell">
        <CodeTextarea value={block.source} ariaLabel={`Illustrative code cell ${block.cellIndex} (read-only)`} />
        <div className="cell-toolbar">
          <span
            className="illustrative-badge"
            title="Needs an external platform (a cloud SDK, a broker); the backend refuses it too."
          >
            ILLUSTRATIVE
          </span>
          <span className="cell-note">Read-only — needs an external platform.</span>
        </div>
        {withHint ? <p className="kernel-hint">{KERNEL_HINT}</p> : null}
      </div>
    );
  }

  return (
    <div className="nb-cell">
      <CodeTextarea value={source} onChange={setSource} ariaLabel={`Editable code cell ${block.cellIndex}`} />
      <div className="cell-toolbar">
        <button
          type="button"
          className="cell-run"
          onClick={run}
          disabled={running}
          title="Runs on the page kernel — earlier Runs stay in scope"
        >
          {running ? <CircleNotch size={16} className="cell-spin" /> : <Play size={16} weight="bold" />}
          {running ? "Running" : "Run"}
        </button>
        {result?.elapsed_seconds != null ? (
          <span className="output-meta">{elapsedLabel(result.elapsed_seconds)}</span>
        ) : null}
      </div>
      {result !== null ? <CellOutput result={result} /> : null}
      {withHint ? <p className="kernel-hint">{KERNEL_HINT}</p> : null}
    </div>
  );
}

/** stdout / stderr / traceback, red-framed whenever anything went wrong. */
function CellOutput({ result }: { result: ExecResponse }) {
  const failed = result.traceback !== null || result.status !== "ok";
  const firstLine = firstOutputLine(result);
  return (
    <div className={failed ? "cell-output cell-output-error" : "cell-output"}>
      {firstLine ? <pre className="output-stdout">{firstLine}</pre> : null}
      {result.stderr ? <pre className="output-stderr">{result.stderr}</pre> : null}
      {result.traceback ? <pre className="output-traceback">{result.traceback}</pre> : null}
    </div>
  );
}

/** Captured stdout, or a status note when nothing ran (timeout, busy, ...). */
function firstOutputLine(result: ExecResponse): string {
  if (result.stdout) return result.stdout;
  return STATUS_NOTES[result.status] ?? "";
}

/** Sub-second runs (the common case) read better as milliseconds. */
function elapsedLabel(seconds: number): string {
  return seconds < 0.1 ? `${Math.round(seconds * 1000)}ms` : `${seconds.toFixed(2)}s`;
}
