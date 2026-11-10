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
  Eye,
  GithubLogo,
  Package,
  Terminal,
  WarningCircle,
} from "@phosphor-icons/react/dist/ssr";
import { AppShell } from "@/components/AppShell";
import { CopyCodeButton, CopyLinkButton, MarkDonePanel } from "@/components/ReaderControls";
import { EndSentinel, ReaderToc } from "@/components/ReaderToc";
import { StarButton } from "@/components/StarButton";
import type { CellOutput, ParsedCell } from "@/lib/notebook-parse";
import { getNotebook, getNotebookSlugs, type NotebookDetail } from "@/lib/notebooks";
import { RETIRED_BY_SLUG, RETIRED_NOTEBOOKS, type RetiredNotebook } from "@/lib/retired";
import { highlightCode, renderMarkdown } from "@/lib/render";
import { toneStyle } from "@/lib/tone";

type Params = { params: Promise<{ slug: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return [...getNotebookSlugs(), ...RETIRED_NOTEBOOKS.map((retired) => retired.slug)].map((slug) => ({ slug }));
}

// Plain URLs (the meta refresh) are not rewritten by Next, so they carry the base path themselves.
const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

/** A merged notebook's old URL: a redirect to the notebook that now holds its content. */
function MovedPage({ retired }: { retired: RetiredNotebook }) {
  const target = getNotebook(retired.movedTo);
  const href = `/notebooks/${retired.movedTo}/`;
  return (
    <AppShell crumbs={[{ label: "Library", href: "/" }, { label: "Moved" }]}>
      <meta httpEquiv="refresh" content={`0; url=${BASE_PATH}${href}`} />
      <article className="article moved-page">
        <h1>This notebook has moved</h1>
        <p className="lead">{retired.note}</p>
        <p>
          <Link className="btn btn-primary" href={href}>
            Go to {target?.title ?? retired.movedTo}
            <ArrowRight size={15} aria-hidden />
          </Link>
        </p>
      </article>
    </AppShell>
  );
}

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { slug } = await params;
  if (RETIRED_BY_SLUG.has(slug)) return { title: "Moved", robots: { index: false } };
  const notebook = getNotebook(slug);
  return notebook ? { title: notebook.title, description: notebook.description || undefined } : {};
}

function OutputBlock({ output, number }: { output: CellOutput; number: number }) {
  if (output.type === "image") {
    // eslint-disable-next-line @next/next/no-img-element -- inline data URI from the executed notebook
    return <img className="cell-output-image" src={output.src} alt={`Chart produced by cell ${number}`} />;
  }
  if (output.type === "error") {
    return (
      <pre className="cell-output-text is-error">
        <WarningCircle size={14} weight="bold" aria-hidden /> {output.name}: {output.message}
      </pre>
    );
  }
  return <pre className={`cell-output-text${output.stream === "stderr" ? " is-stderr" : ""}`}>{output.text.replace(/\n+$/, "")}</pre>;
}

function CellOutputs({ cell, number }: { cell: ParsedCell; number: number }) {
  if (cell.outputs.length === 0) return null;
  return (
    <div className="cell-output" role="group" aria-label={`Output of cell ${number}`}>
      <div className="cell-output-label">
        <Terminal size={13} aria-hidden />
        Output
      </div>
      {cell.outputs.map((output, position) => (
        <OutputBlock key={position} output={output} number={number} />
      ))}
    </div>
  );
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

  if (cell.kind === "solution") {
    return (
      <details className="solution-cell cell" id={`cell-${cell.index}`}>
        <summary>
          <Eye size={15} aria-hidden />
          Solution for cell {number}: open it after you have tried the problem
        </summary>
        {body}
        <CellOutputs cell={cell} number={number} />
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
      <CellOutputs cell={cell} number={number} />
    </div>
  );
}

function CellMap({ cells, checks, solutions }: { cells: ParsedCell[]; checks: number; solutions: number }) {
  const shown = cells.filter((cell) => cell.kind !== "setup");
  const label = (cell: ParsedCell) =>
    cell.kind === "check"
      ? "self-check"
      : cell.kind === "solution"
        ? "solution"
        : cell.kind === "code"
          ? "code"
          : "explanation";
  const tickClass = (cell: ParsedCell) =>
    cell.kind === "check" ? "t-check" : cell.kind === "solution" ? "t-solution" : cell.kind === "code" ? "t-code" : undefined;
  return (
    <section className="panel cellmap" aria-labelledby="cellmap-title">
      <div className="cellmap-head">
        <strong id="cellmap-title">
          {shown.length} cells{checks > 0 ? `, ${checks} self-checks` : ""}
          {solutions > 0 ? `, ${solutions} hidden solutions` : ""}
        </strong>
        <span>Each tick jumps to its cell</span>
      </div>
      <nav className="ticks" aria-label="Cells">
        {shown.map((cell, position) => (
          <a
            key={cell.index}
            href={`#cell-${cell.index}`}
            className={tickClass(cell)}
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
          <i className="l-solution" />
          Solution
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
  const { slug } = await params;
  const retired = RETIRED_BY_SLUG.get(slug);
  if (retired) return <MovedPage retired={retired} />;
  const notebook = getNotebook(slug);
  if (!notebook) notFound();

  const toolHref = `/tools/${notebook.toolFolder}/`;
  const tocSections = notebook.sections.map(({ id, title }) => ({ id, title }));

  return (
    <AppShell
      tool={notebook.toolFolder}
      crumbs={[
        { label: "Library", href: "/" },
        { label: notebook.toolLabel, href: toolHref },
        { label: notebook.title },
      ]}
    >
      <div className="reader">
        <article className="article">
          <header>
            <Link className="kicker" href={toolHref}>
              <span className="dot" style={toneStyle(notebook.tone, "--dot")} aria-hidden />
              {notebook.toolLabel}
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
              {notebook.checks > 0 ? <span className="tag">{notebook.checks} self-checks</span> : null}
              {notebook.solutions > 0 ? <span className="tag">{notebook.solutions} hidden solutions</span> : null}
            </div>
            <p className="output-note">
              {notebook.hasOutputs
                ? "Results under each cell come from an automated run of this notebook. Open it in Colab to change the code and run it yourself."
                : "Results are not stored with the notebook. Run it in Colab, or run the cells in order, to see the output."}
            </p>
          </header>

          <CellMap cells={notebook.cells} checks={notebook.checks} solutions={notebook.solutions} />

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
                    Next in {notebook.toolLabel}
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
