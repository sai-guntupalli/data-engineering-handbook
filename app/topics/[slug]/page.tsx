import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, DownloadSimple, Notebook } from "@phosphor-icons/react/dist/ssr";
import { Markdown } from "@/components/Markdown";
import { allTopicSlugs, getTopic, getTopicMarkdown } from "@/lib/topics";

export function generateStaticParams() {
  return allTopicSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  if (!allTopicSlugs().includes(slug)) return {};
  const topic = getTopic(slug);
  return {
    title: topic.title,
    description: topic.summary,
  };
}

export default async function TopicPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  if (!allTopicSlugs().includes(slug)) notFound();
  const topic = getTopic(slug);
  const markdown = getTopicMarkdown(slug);

  return (
    <main className="article-layout">
      <aside className="article-sidebar">
        <Link href="/topics" className="back-link">
          <ArrowLeft size={16} weight="bold" /> Topics
        </Link>
        <dl>
          <div>
            <dt>Group</dt>
            <dd>{topic.group}</dd>
          </div>
          <div>
            <dt>Questions</dt>
            <dd>{topic.questionCount}</dd>
          </div>
          <div>
            <dt>Code blocks</dt>
            <dd>{topic.codeBlockCount}</dd>
          </div>
        </dl>
        {topic.notebookColabPath ? (
          <a href={topic.notebookColabPath} target="_blank" rel="noreferrer" className="notebook-link">
            <Notebook size={18} weight="bold" /> Open in Colab
          </a>
        ) : null}
        {topic.notebookDownloadPath ? (
          <Link href={topic.notebookDownloadPath} className="notebook-link secondary">
            <DownloadSimple size={18} weight="bold" /> Download .ipynb
          </Link>
        ) : null}
      </aside>
      <article className="markdown-body">
        <Markdown markdown={markdown} />
      </article>
    </main>
  );
}
