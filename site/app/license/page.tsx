import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowRight,
  BookOpen,
  CheckCircle,
  Copyright,
  GraduationCap,
  Handshake,
  PuzzlePiece,
} from "@phosphor-icons/react/dist/ssr";
import { Attribution } from "@/components/Attribution";
import { AppShell } from "@/components/AppShell";
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

const ATTRIBUTION_TEXT = `© ${authorName}. The Data Engineering Handbook\n${repositoryHref} · ${licenseName} · ${licenseHref}`;

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
    <AppShell crumbs={[{ label: "Library", href: "/" }, { label: "License" }]}>
      <div className="prose-page">
        <header>
          <h1>Free to use, with one condition: credit.</h1>
          <p className="lead">
            Written and maintained by{" "}
            <a className="text-link" href={authorHref} target="_blank" rel="noreferrer">
              {authorName}
            </a>
            .
          </p>
        </header>

        <section className="prose-section" aria-labelledby="license-terms">
          <h2 id="license-terms">
            <Handshake size={20} weight="bold" aria-hidden /> {licenseNameLong} ({licenseName})
          </h2>
          <p>
            Every notebook in this handbook is © {authorName}, released under{" "}
            <a className="text-link" href={licenseHref} target="_blank" rel="noreferrer">
              {licenseName}
            </a>
            . Reuse is free for everyone. The single rule is that <strong>you must give credit</strong> when you use,
            share, teach from, or build on this material.
          </p>
        </section>

        <section className="prose-section" aria-labelledby="license-freedoms">
          <h2 id="license-freedoms">You are free to</h2>
          <ul className="check-list">
            {permissions.map(({ icon: Icon, text }) => (
              <li key={text}>
                <Icon size={18} weight="bold" aria-hidden />
                <span>{text}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="prose-section" aria-labelledby="license-attribution">
          <h2 id="license-attribution">
            <CheckCircle size={20} weight="bold" aria-hidden /> The one requirement: credit
          </h2>
          <p>
            Attribution is the core condition of {licenseName}. Wherever you share or use this handbook, the credit must
            appear with it: a lesson, a slide deck, a fork, a blog post.
          </p>
          <ul className="check-list">
            {attributionDuties.map((duty, index) => (
              <li key={index}>
                <CheckCircle size={18} weight="bold" aria-hidden />
                <span>{duty}</span>
              </li>
            ))}
          </ul>
          <p>Copy this credit, which meets all of the above:</p>
          <Attribution text={ATTRIBUTION_TEXT} />
        </section>

        <section className="prose-section" aria-labelledby="license-details">
          <h2 id="license-details">Details</h2>
          <div className="actions">
            <a className="btn" href={repositoryHref} target="_blank" rel="noreferrer">
              Repository
            </a>
            <a className="btn" href={licenseFileHref} target="_blank" rel="noreferrer">
              Full legal code (LICENSE)
            </a>
            <a className="btn" href={licenseHref} target="_blank" rel="noreferrer">
              {licenseName} at Creative Commons
            </a>
            <Link className="btn btn-primary" href="/search/">
              Browse the notebooks
              <ArrowRight size={16} weight="bold" aria-hidden />
            </Link>
          </div>
          <p className="fine-print">
            Each notebook opens with an author credit line, so the credit travels with the file even when it leaves this
            repository. Provided as-is, without warranty of any kind. See Section 5 of the legal code.
          </p>
        </section>
      </div>
    </AppShell>
  );
}
