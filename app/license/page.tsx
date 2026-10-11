import type { Metadata } from "next";
import Link from "next/link";
import {
  BookOpen,
  CheckCircle,
  Copyright,
  GraduationCap,
  Handshake,
  Lightning,
  PuzzlePiece,
} from "@phosphor-icons/react/dist/ssr";
import { Attribution } from "@/components/Attribution";
import { SiteHeader } from "@/components/SiteHeader";
import { getSearchIndex } from "@/lib/notebooks";
import {
  authorHref,
  authorName,
  licenseFileHref,
  licenseHref,
  licenseName,
  licenseNameLong,
  repository,
  repositoryHref,
} from "@/lib/site";

export const metadata: Metadata = {
  title: "License",
  description: `The Data Engineering Handbook by ${authorName} is licensed under ${licenseNameLong} — reuse is free, crediting the author is required.`,
};

const ATTRIBUTION_TEXT = `© ${authorName}. The Data Engineering Handbook\n${repositoryHref} · ${licenseName} · https://creativecommons.org/licenses/by/4.0/`;

const permissions = [
  { icon: Copyright, text: "Use it commercially — in your work, your team, your product" },
  { icon: GraduationCap, text: "Teach with it — courses, workshops, interview prep groups" },
  { icon: PuzzlePiece, text: "Adapt it — remix, translate, extend the notebooks" },
  { icon: BookOpen, text: "Share it — copy the notebooks, host them elsewhere" },
];

const attributionDuties = [
  <>
    <strong>Credit the author</strong> — name {authorName} and link to{" "}
    <a href={repositoryHref} target="_blank" rel="noreferrer">
      {repository}
    </a>
    .
  </>,
  <>
    <strong>Name the license</strong> — a link to{" "}
    <a href={licenseHref} target="_blank" rel="noreferrer">
      {licenseName}
    </a>{" "}
    satisfies this.
  </>,
  <>
    <strong>Link back</strong> to the source you used, where reasonably possible.
  </>,
  <>
    <strong>Mark changes</strong> — if you modified the material, say so.
  </>,
];

export default function LicensePage() {
  return (
    <>
      <SiteHeader index={getSearchIndex()} />
      <main id="main-content" className="search-page">
        <div className="content-shell page-top search-shell license-shell">
          <h1>License</h1>
          <p className="results-meta search-summary">
            Written and maintained by{" "}
            <a href={authorHref} target="_blank" rel="noreferrer">
              {authorName}
            </a>
            .
          </p>

          <section className="license-panel" aria-labelledby="license-terms">
            <h2 id="license-terms">
              <Handshake size={20} weight="bold" /> {licenseNameLong} ({licenseName})
            </h2>
            <p>
              Every notebook in this handbook is © {authorName}, released under{" "}
              <a href={licenseHref} target="_blank" rel="noreferrer">
                {licenseName}
              </a>
              . Reuse is free for everyone — the single rule is that <strong>you must give credit</strong>{" "}
              when you use, share, teach from, or build on this material.
            </p>
          </section>

          <section className="license-section" aria-labelledby="license-freedoms">
            <h2 id="license-freedoms">You are free to</h2>
            <ul className="license-list">
              {permissions.map(({ icon: Icon, text }) => (
                <li key={text}>
                  <Icon size={18} weight="bold" aria-hidden />
                  {text}
                </li>
              ))}
            </ul>
          </section>

          <section className="license-section" aria-labelledby="license-attribution">
            <h2 id="license-attribution">
              <CheckCircle size={20} weight="bold" /> The one requirement: credit
            </h2>
            <p>
              Attribution is the core condition of {licenseName}. Wherever you share or use this
              handbook, the credit must appear with it — a lesson, a slide deck, a fork, a blog post.
            </p>
            <ul className="license-list">
              {attributionDuties.map((duty, index) => (
                <li key={index}>
                  <CheckCircle size={18} weight="bold" aria-hidden />
                  {duty}
                </li>
              ))}
            </ul>
            <p>Copy-paste credit that satisfies all of the above:</p>
            <Attribution text={ATTRIBUTION_TEXT} />
          </section>

          <section className="license-section" aria-labelledby="license-details">
            <h2 id="license-details">Details</h2>
            <div className="license-links">
              <a className="button secondary" href={repositoryHref} target="_blank" rel="noreferrer">
                Repository <Lightning size={16} weight="bold" />
              </a>
              <a className="button secondary" href={licenseFileHref} target="_blank" rel="noreferrer">
                Full legal code (LICENSE)
              </a>
              <a className="button secondary" href={licenseHref} target="_blank" rel="noreferrer">
                {licenseName} at Creative Commons
              </a>
              <Link className="button primary" href="/search?q=">
                Browse the notebooks
              </Link>
            </div>
            <p className="results-meta">
              Each notebook also carries this license inside its <code>metadata.watermark</code> block,
              so the credit travels with the file even when it leaves this repository. Provided as-is,
              without warranty of any kind — see Section 5 of the legal code.
            </p>
          </section>
        </div>
      </main>
    </>
  );
}