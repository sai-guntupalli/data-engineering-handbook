/**
 * Canonical site origin used for metadata, sitemap and robots.
 *
 * The gallery has no fixed production URL yet, so it can be overridden with
 * `NEXT_PUBLIC_SITE_URL` at build time. The default matches `make serve`.
 */
export const siteUrl = (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000").replace(/\/+$/, "");