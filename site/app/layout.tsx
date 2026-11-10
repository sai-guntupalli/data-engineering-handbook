import type { Metadata } from "next";
import { Instrument_Sans, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { PaletteProvider } from "@/components/palette";
import { PanelShortcuts } from "@/components/panels";
import { BOOT_SCRIPT } from "@/lib/boot";
import { authorHref, authorName, siteUrl } from "@/lib/site";

const instrumentSans = Instrument_Sans({
  variable: "--font-sans",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

const siteName = "Data Engineering Handbook";
const siteDescription =
  "An open handbook of runnable Jupyter notebooks for data engineering: Python, SQL, PySpark, lakehouse formats, streaming, cloud platforms, warehousing, AI foundations and more.";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: siteName,
    template: `%s | ${siteName}`,
  },
  description: siteDescription,
  authors: [{ name: authorName, url: authorHref }],
  creator: authorName,
  openGraph: {
    type: "website",
    siteName,
    title: siteName,
    description: siteDescription,
    images: [{ url: `${siteUrl}/og.png`, width: 1200, height: 630, alt: siteName }],
  },
  twitter: {
    card: "summary_large_image",
    title: siteName,
    description: siteDescription,
    images: [`${siteUrl}/og.png`],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    // The boot scripts may set data-theme, data-sidebar and data-toc before React hydrates.
    <html lang="en" className={`${instrumentSans.variable} ${jetbrainsMono.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: BOOT_SCRIPT }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
          "@context": "https://schema.org", "@type": "WebSite", name: siteName,
          url: `${siteUrl}/`, description: siteDescription,
          author: { "@type": "Person", name: authorName, url: authorHref },
        }).replace(/</g, "\\u003c") }} />
      </head>
      <body>
        <a href="#main-content" className="skip-link">
          Skip to content
        </a>
        <PaletteProvider>{children}</PaletteProvider>
        <PanelShortcuts />
      </body>
    </html>
  );
}
