/**
 * Canonical site URL, including any base path, used for metadata, sitemap and robots.
 *
 * The default is the GitHub Pages project URL, which includes the repository path.
 * Deploying elsewhere means setting two build-time variables together:
 * - `NEXT_PUBLIC_SITE_URL`: the full public URL including the path, with no trailing slash.
 * - `NEXT_PUBLIC_BASE_PATH` (see next.config.ts): the same path without the origin,
 *   e.g. `/data-engineering-handbook`, or unset when the site is served from the root.
 */
export const siteUrl = (
  process.env.NEXT_PUBLIC_SITE_URL ?? "https://sai-guntupalli.github.io/data-engineering-handbook"
).replace(/\/+$/, "");

/** GitHub repository the handbook lives in (safe for client components). */
export const repository = "sai-guntupalli/data-engineering-handbook";
export const repositoryHref = `https://github.com/${repository}`;
export const branch = "master";

/** Author of the handbook; matches the credit line in every notebook's first cell. */
export const authorName = "Sai Guntupalli";
export const authorHref = `https://github.com/sai-guntupalli`;

/** The handbook is licensed CC BY 4.0: attribution is required on reuse. */
export const licenseName = "CC BY 4.0";
export const licenseNameLong = "Creative Commons Attribution 4.0 International";
export const licenseHref = "https://creativecommons.org/licenses/by/4.0/";
export const licenseFileHref = `${repositoryHref}/blob/${branch}/LICENSE`;