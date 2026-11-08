import type { Metadata } from "next";
import { Instrument_Sans, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { PaletteProvider } from "@/components/palette";
import { THEME_BOOT_SCRIPT } from "@/components/theme";
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
  },
  twitter: {
    card: "summary",
    title: siteName,
    description: siteDescription,
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    // The boot script may set data-theme before React hydrates.
    <html lang="en" className={`${instrumentSans.variable} ${jetbrainsMono.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_BOOT_SCRIPT }} />
      </head>
      <body>
        <a href="#main-content" className="skip-link">
          Skip to content
        </a>
        <PaletteProvider>{children}</PaletteProvider>
      </body>
    </html>
  );
}
