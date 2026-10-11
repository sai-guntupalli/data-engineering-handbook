/**
 * Canonical site origin used for metadata, sitemap and robots.
 *
 * The handbook is public and served by GitHub Pages at the default origin
 * below. Deploying elsewhere? Set `NEXT_PUBLIC_SITE_URL` at build time.
 */
export const siteUrl = (
  process.env.NEXT_PUBLIC_SITE_URL ?? "https://sai-guntupalli.github.io/data-engineering-handbook"
).replace(/\/+$/, "");

/** GitHub repository the handbook lives in (safe for client components). */
export const repository = "sai-guntupalli/data-engineering-handbook";
export const repositoryHref = `https://github.com/${repository}`;

/** Author of the handbook; matches AUTHOR in scripts/watermark_notebooks.py. */
export const authorName = "Sai Guntupalli";
export const authorHref = `https://github.com/sai-guntupalli`;

/** The handbook is licensed CC BY 4.0: attribution is required on reuse. */
export const licenseName = "CC BY 4.0";
export const licenseNameLong = "Creative Commons Attribution 4.0 International";
export const licenseHref = "https://creativecommons.org/licenses/by/4.0/";
export const licenseFileHref = `${repositoryHref}/blob/master/LICENSE`;