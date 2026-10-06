import fs from "node:fs";
import path from "node:path";
import { topicNotebookColabHref, topicNotebookDownloadHref } from "@/lib/notebooks";

export type Topic = {
  slug: string;
  title: string;
  summary: string;
  group: string;
  questionCount: number;
  codeBlockCount: number;
  notebookPath: string | null;
  notebookDownloadPath: string | null;
  notebookColabPath: string | null;
};

export type TopicGroup = {
  label: string;
  slugs: string[];
};

export const topicGroups: TopicGroup[] = [
  {
    label: "Core Pipeline Skills",
    slugs: [
      "python",
      "python-basics",
      "python-coding",
      "sql",
      "scala",
      "spark",
      "spark-tuning",
      "airflow",
      "dbt",
      "data-quality",
      "observability",
    ],
  },
  {
    label: "Lakehouse And Formats",
    slugs: ["parquet", "delta", "iceberg", "hudi", "avro", "cdc", "data-modeling"],
  },
  {
    label: "Cloud And Platforms",
    slugs: [
      "aws",
      "azure",
      "gcp",
      "bigquery",
      "redshift",
      "snowflake",
      "databricks",
      "trino",
      "clickhouse",
      "dynamodb",
      "bigtable",
    ],
  },
  {
    label: "Streaming And Distributed Systems",
    slugs: ["kafka", "flink", "redis", "hadoop", "hive", "hbase", "cassandra", "kubernetes"],
  },
  {
    label: "Warehousing, BI, And Governance",
    slugs: [
      "dwha",
      "system-design",
      "statistics",
      "data-governance",
      "cost-optimization",
      "tableau",
      "looker",
      "superset",
    ],
  },
  {
    label: "AI And LLM Foundations",
    slugs: ["llm"],
  },
  {
    label: "Additional Tools",
    slugs: ["mongo", "nifi", "flume", "greenplum", "impala", "elasticsearch", "docker", "data-structure"],
  },
];

const root = process.cwd();
const contentDir = path.join(root, "content");
const notebooksDir = path.join(root, "notebooks", "topics");

function readTopicFile(slug: string) {
  return fs.readFileSync(path.join(contentDir, `${slug}.md`), "utf8");
}

export function cleanMarkdown(markdown: string) {
  const lines = markdown.split(/\r?\n/);
  const output: string[] = [];
  let seenH1 = false;
  let seenH2 = false;
  let skippingLeadingToc = false;

  for (const line of lines) {
    if (line.startsWith("## [Main title]")) continue;
    if (line.startsWith("### [Interview questions]")) continue;
    if (line.trim() === "#") continue;
    if (line.startsWith("**Notebook:**")) continue;
    if (seenH1 && !seenH2 && /^##\s+Table of Contents\s*$/i.test(line)) {
      skippingLeadingToc = true;
      continue;
    }
    if (skippingLeadingToc && line.startsWith("+ [")) continue;
    if (skippingLeadingToc && !line.trim()) continue;
    if (skippingLeadingToc) skippingLeadingToc = false;
    if (/^#\s+/.test(line)) seenH1 = true;
    if (/^##\s+/.test(line)) seenH2 = true;
    if (seenH1 && !seenH2 && line.startsWith("+ [")) continue;
    if (line.startsWith("[Table of Contents]")) continue;
    output.push(line);
  }

  return output.join("\n").trim() + "\n";
}

function titleFromMarkdown(markdown: string, fallback: string) {
  const match = markdown.match(/^#\s+(.+?)\s*$/m);
  return match?.[1]?.trim() ?? fallback.replaceAll("-", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function summaryFromMarkdown(markdown: string) {
  let inCode = false;
  for (const line of markdown.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (trimmed.startsWith("```")) {
      inCode = !inCode;
      continue;
    }
    if (inCode || !trimmed || trimmed.startsWith("#") || trimmed.startsWith("+ [")) continue;
    if (trimmed.startsWith("|")) continue;
    if (trimmed.length > 190) return `${trimmed.slice(0, 187).trim()}...`;
    return trimmed;
  }
  return "Practical interview questions, explanations, and examples.";
}

function groupForSlug(slug: string) {
  return topicGroups.find((group) => group.slugs.includes(slug))?.label ?? "Other Topics";
}

export function allTopicSlugs() {
  return fs
    .readdirSync(contentDir)
    .filter((file) => file.endsWith(".md") && file !== "full.md")
    .map((file) => file.replace(/\.md$/, ""))
    .sort();
}

export function getTopic(slug: string): Topic {
  const raw = readTopicFile(slug);
  const markdown = cleanMarkdown(raw);
  const notebook = path.join(notebooksDir, `${slug}.ipynb`);
  return {
    slug,
    title: titleFromMarkdown(markdown, slug),
    summary: summaryFromMarkdown(markdown),
    group: groupForSlug(slug),
    questionCount: markdown.split(/\r?\n/).filter((line) => line.startsWith("## ")).length,
    codeBlockCount: (markdown.match(/```/g) ?? []).length / 2,
    notebookPath: fs.existsSync(notebook) ? topicNotebookDownloadHref(slug) : null,
    notebookDownloadPath: fs.existsSync(notebook) ? topicNotebookDownloadHref(slug) : null,
    notebookColabPath: fs.existsSync(notebook) ? topicNotebookColabHref(slug) : null,
  };
}

export function getAllTopics() {
  const topics = allTopicSlugs().map(getTopic);
  const known = new Set(topicGroups.flatMap((group) => group.slugs));
  return [
    ...topicGroups.flatMap((group) => group.slugs.map((slug) => topics.find((topic) => topic.slug === slug)).filter(Boolean) as Topic[]),
    ...topics.filter((topic) => !known.has(topic.slug)),
  ];
}

export function getGroupedTopics() {
  const topicsBySlug = new Map(getAllTopics().map((topic) => [topic.slug, topic]));
  const used = new Set<string>();
  const grouped = topicGroups
    .map((group) => {
      const topics = group.slugs.map((slug) => topicsBySlug.get(slug)).filter(Boolean) as Topic[];
      topics.forEach((topic) => used.add(topic.slug));
      return { ...group, topics };
    })
    .filter((group) => group.topics.length > 0);
  const leftovers = getAllTopics().filter((topic) => !used.has(topic.slug));
  if (leftovers.length > 0) grouped.push({ label: "Other Topics", slugs: leftovers.map((topic) => topic.slug), topics: leftovers });
  return grouped;
}

export function getTopicMarkdown(slug: string) {
  return cleanMarkdown(readTopicFile(slug));
}

export function getAllQuestionsMarkdown() {
  const full = fs.readFileSync(path.join(contentDir, "full.md"), "utf8");
  return cleanMarkdown(full);
}
