import { Markdown } from "@/components/Markdown";
import { getAllQuestionsMarkdown, getAllTopics } from "@/lib/topics";

export const metadata = {
  title: "All Questions",
};

export default function QuestionsPage() {
  const topics = getAllTopics();
  const questionCount = topics.reduce((sum, topic) => sum + topic.questionCount, 0);

  return (
    <main className="article-layout single-column">
      <article className="markdown-body">
        <div className="page-heading inline-heading">
          <p className="kicker">Question bank</p>
          <h1>All questions.</h1>
          <p>{questionCount.toLocaleString()} questions grouped by topic. Use browser search or the app search to jump fast.</p>
        </div>
        <Markdown markdown={getAllQuestionsMarkdown()} />
      </article>
    </main>
  );
}
