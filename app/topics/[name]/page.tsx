import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { BookOpen } from "@phosphor-icons/react/dist/ssr";
import { ChatPanel } from "@/components/chat-panel";
import { NotebookViewer } from "@/components/notebook-viewer";
import { SiteHeader } from "@/components/SiteHeader";
import { readNotebookPage } from "@/lib/notebook-content";
import { getNotebookSummaries, getSearchIndex } from "@/lib/notebooks";

/** One static page per notebook, folder-agnostic (the viewer's reading view). */
export function generateStaticParams() {
  return getNotebookSummaries().map((summary) => ({ name: summary.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ name: string }>;
}): Promise<Metadata> {
  const { name } = await params;
  const summary = getNotebookSummaries().find((candidate) => candidate.slug === name);
  return { title: summary?.title ?? "Notebook" };
}

export default async function TopicPage({ params }: { params: Promise<{ name: string }> }) {
  const { name } = await params;
  const summary = getNotebookSummaries().find((candidate) => candidate.slug === name);
  if (!summary) notFound();
  const page = readNotebookPage(summary);

  return (
    <>
      <SiteHeader index={getSearchIndex()} />
      <main id="main-content">
        <div className="content-shell page-top topic-shell">
          <p className="kicker">
            <BookOpen size={12} weight="bold" /> Interactive notebook
          </p>
          <h1 className="topic-title">{page.title}</h1>
          <p className="topic-links">
            <a href={summary.githubHref} target="_blank" rel="noreferrer">
              GitHub
            </a>
            <a href={summary.colabHref} target="_blank" rel="noreferrer">
              Open in Colab
            </a>
          </p>
          <div className="topic-layout">
            <nav className="toc" aria-label="Table of contents">
              <span className="toc-title">Contents</span>
              {page.sections.map((section) => (
                <a key={section.id} className="toc-link" href={`#${section.id}`}>
                  {section.heading}
                </a>
              ))}
            </nav>
            <article className="viewer-article">
              <NotebookViewer page={page} />
            </article>
            <ChatPanel notebookTitle={page.title} outline={page.sections.map((section) => section.heading)} />
          </div>
        </div>
      </main>
    </>
  );
}