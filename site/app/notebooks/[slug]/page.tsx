import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  ArrowLeft,
  ArrowRight,
  ArrowSquareOut,
  CheckCircle,
  Code,
  DownloadSimple,
  GithubLogo,
  Package,
} from "@phosphor-icons/react/dist/ssr";
import { AppShell, catalogHref } from "@/components/AppShell";
import { CopyCodeButton, CopyLinkButton, MarkDonePanel } from "@/components/ReaderControls";
import { EndSentinel, ReaderToc } from "@/components/ReaderToc";
import { StarButton } from "@/components/StarButton";
import { anchorFor } from "@/lib/notebook-groups";
import type { ParsedCell } from "@/lib/notebook-parse";
import { getNotebook, getNotebookSlugs, type NotebookDetail } from "@/lib/notebooks";
import { highlightCode, renderMarkdown } from "@/lib/render";
import { toneStyle } from "@/lib/tone";

type Params = { params: Promise<{ slug: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return getNotebookSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const notebook = getNotebook((await params).slug);
  return notebook ? { title: notebook.title, description: notebook.description || undefined } : {};
}

function CodeCell({ cell, number }: { cell: ParsedCell; number: number }) {
  const lines = cell.source.replace(/\n+$/, "").split("\n").length;
  const gutter = Array.from({ length: lines }, (_, index) => index + 1).join("\n");
  const body = (
    <div className="cell-body">
      <span className="gutter" aria-hidden>
        {gutter}
      </span>
      <pre>
        <code dangerouslySetInnerHTML={{ __html: highlightCode(cell.source.replace(/\n+$/, "")) }} />
      </pre>
    </div>
  );

  if (cell.kind === "setup") {
    return (
      <details className="setup-cell cell" id={`cell-${cell.index}`}>
        <summary>
          <Package size={15} aria-hidden />
          Setup cell: installs this notebook&apos;s packages in Colab
        </summary>
        {body}
      </details>
    );
  }

  return (
    <div className="cell" id={`cell-${cell.index}`}>
      <div className="cell-bar">
        <span className="left">
          <span className="exec">Cell {number}</span>
          {cell.kind === "check" ? (
            <span className="cell-kind is-check">
              <CheckCircle size={14} weight="bold" aria-hidden />
              Self-check
            </span>
          ) : (
            <span className="cell-kind">
              <Code size={14} aria-hidden />
              Python
            </span>
          )}
        </span>
        <CopyCodeButton />
      </div>
      {body}
    </div>
  );
}

function CellMap({ cells, checks }: { cells: ParsedCell[]; checks: number }) {
  const shown = cells.filter((cell) => cell.kind !== "setup");
  const label = (cell: ParsedCell) =>
    cell.kind === "check" ? "self-check" : cell.kind === "code" ? "code" : "explanation";
  return (
    <section className="panel cellmap" aria-labelledby="cellmap-title">
      <div className="cellmap-head">
        <strong id="cellmap-title">
          {shown.length} cells, {checks} self-checks
        </strong>
        <span>Each tick jumps to its cell</span>
      </div>
      <nav className="ticks" aria-label="Cells">
        {shown.map((cell, position) => (
          <a
            key={cell.index}
            href={`#cell-${cell.index}`}
            className={cell.kind === "check" ? "t-check" : cell.kind === "code" ? "t-code" : undefined}
            aria-label={`Cell ${position + 1}, ${label(cell)}`}
            title={`Cell ${position + 1}: ${label(cell)}`}
          />
        ))}
      </nav>
      <div className="legend" aria-hidden>
        <span>
          <i className="l-check" />
          Self-check
        </span>
        <span>
          <i className="l-code" />
          Code
        </span>
        <span>
          <i className="l-text" />
          Explanation
        </span>
      </div>
    </section>
  );
}

type RenderedCell = { cell: ParsedCell; html: string; number: number };

/**
 * Markdown to HTML, with section ids handed out in document order, and a
 * running number for each code cell (the setup cell is not counted).
 */
function renderCells(notebook: NotebookDetail): RenderedCell[] {
  let nextSection = 0;
  const nextSectionId = () => notebook.sections[nextSection++]?.id ?? `section-${nextSection}`;
  let codeNumber = 0;
  return notebook.cells.map((cell) => {
    if (cell.kind === "markdown") return { cell, html: renderMarkdown(cell.source, nextSectionId), number: 0 };
    if (cell.kind !== "setup") codeNumber += 1;
    return { cell, html: "", number: codeNumber };
  });
}

export default async function NotebookPage({ params }: Params) {
  const notebook = getNotebook((await params).slug);
  if (!notebook) notFound();

  const groupHref = catalogHref(anchorFor(notebook.groupLabel));
  const tocSections = notebook.sections.map(({ id, title }) => ({ id, title }));

  return (
    <AppShell
      crumbs={[
        { label: "Library", href: "/" },
        { label: notebook.groupLabel, href: groupHref },
        { label: notebook.title },
      ]}
    >
      <div className="reader">
        <article className="article">
          <header>
            <Link className="kicker" href={groupHref}>
              <span className="dot" style={toneStyle(notebook.tone, "--dot")} aria-hidden />
              {notebook.groupLabel}
            </Link>
            <h1>{notebook.title}</h1>
            {notebook.intro || notebook.description ? <p className="lead">{notebook.intro || notebook.description}</p> : null}
            <div className="meta-row">
              <StarButton repoPath={notebook.repoPath} title={notebook.title} labelled />
              <a className="btn" href={notebook.colabHref} target="_blank" rel="noreferrer">
                <ArrowSquareOut size={15} aria-hidden />
                Open in Colab
              </a>
              <a className="btn" href={notebook.downloadHref} download={`${notebook.slug}.ipynb`}>
                <DownloadSimple size={15} aria-hidden />
                Download notebook
              </a>
              <a className="btn btn-ghost" href={notebook.githubHref} target="_blank" rel="noreferrer">
                <GithubLogo size={15} aria-hidden />
                Source
              </a>
              <CopyLinkButton />
            </div>
            <div className="meta-row">
              <span className="tag">{notebook.sectionCount} sections</span>
              <span className="tag">About {notebook.minutes} min</span>
              <span className="tag">{notebook.checks} self-checks</span>
            </div>
          </header>

          <CellMap cells={notebook.cells} checks={notebook.checks} />

          <div className="notebook-body">
            {renderCells(notebook).map(({ cell, html, number }) =>
              cell.kind === "markdown" ? (
                <div
                  key={cell.index}
                  id={`cell-${cell.index}`}
                  className="prose"
                  dangerouslySetInnerHTML={{ __html: html }}
                />
              ) : (
                <CodeCell key={cell.index} cell={cell} number={number} />
              ),
            )}
          </div>
          <EndSentinel />

          <MarkDonePanel repoPath={notebook.repoPath} total={notebook.sectionCount} />

          {notebook.previous || notebook.next ? (
            <nav className="pager" aria-label="Previous and next notebook">
              {notebook.previous ? (
                <Link href={notebook.previous.href}>
                  <small>
                    <ArrowLeft size={13} aria-hidden />
                    Previous
                  </small>
                  <strong>{notebook.previous.title}</strong>
                </Link>
              ) : null}
              {notebook.next ? (
                <Link href={notebook.next.href} className="next">
                  <small>
                    Next in {notebook.groupLabel}
                    <ArrowRight size={13} aria-hidden />
                  </small>
                  <strong>{notebook.next.title}</strong>
                </Link>
              ) : null}
            </nav>
          ) : null}
        </article>

        <ReaderToc repoPath={notebook.repoPath} sections={tocSections} minutes={notebook.minutes} />
      </div>
    </AppShell>
  );
}
