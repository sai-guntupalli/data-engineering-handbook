/**
 * Canonical site origin used for metadata, sitemap and robots.
 *
 * Published to GitHub Pages at the repository URL; override with
 * `NEXT_PUBLIC_SITE_URL` at build time if the site ever moves.
 */
export const siteUrl = (
  process.env.NEXT_PUBLIC_SITE_URL ?? "https://sai-guntupalli.github.io/data-engineering-interview-questions"
).replace(/\/+$/, "");