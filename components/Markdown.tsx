import Link from "next/link";
import ReactMarkdown from "react-markdown";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";

type Props = {
  markdown: string;
};

function resolveHref(href: string | undefined) {
  if (!href) return "#";
  if (href.startsWith("http") || href.startsWith("#") || href.startsWith("/")) return href;
  if (href.startsWith("../notebooks/")) return href.replace("..", "");
  if (href.endsWith(".md")) return `/topics/${href.replace(/\.md$/, "")}`;
  const mdAnchor = href.match(/^(.+?)\.md#(.+)$/);
  if (mdAnchor) return `/topics/${mdAnchor[1]}#${mdAnchor[2]}`;
  return href;
}

function resolveImage(src: unknown) {
  if (typeof src !== "string" || !src) return "";
  if (src.startsWith("http") || src.startsWith("/")) return src;
  return `/asset-files/${src.replace(/^\.\.\//, "").replace(/^\.?\//, "")}`;
}

export function Markdown({ markdown }: Props) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeSlug, [rehypeAutolinkHeadings, { behavior: "wrap" }]]}
      components={{
        a({ href, children }) {
          const resolved = resolveHref(href);
          if (resolved.startsWith("http")) {
            return (
              <a href={resolved} target="_blank" rel="noreferrer">
                {children}
              </a>
            );
          }
          return <Link href={resolved}>{children}</Link>;
        },
        img({ src, alt }) {
          return <img src={resolveImage(src)} alt={alt ?? ""} loading="lazy" />;
        },
      }}
    >
      {markdown}
    </ReactMarkdown>
  );
}
