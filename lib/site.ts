/**
 * Canonical site origin used for metadata, sitemap and robots.
 *
 * The handbook lives in a private repository, so there is no public origin.
 * Set `NEXT_PUBLIC_SITE_URL` at build time if you ever deploy the gallery
 * (GitHub Pages for a private repository needs GitHub Pro or above).
 */
export const siteUrl = (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000").replace(/\/+$/, "");