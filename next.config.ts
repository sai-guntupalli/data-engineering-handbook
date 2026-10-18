import type { NextConfig } from "next";

// GitHub Pages project sites serve the app under the repository path:
//   https://sai-guntupalli.github.io/data-engineering-handbook/
// so the Pages build workflow sets NEXT_PUBLIC_BASE_PATH=/data-engineering-handbook.
// Local development (`make serve`) keeps working at the bare origin.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

const nextConfig: NextConfig = {
  agentRules: false,
  reactStrictMode: true,
  // The gallery is fully static in production: build-time file reads only, no
  // server features. Dev relaxes it so the [name] route still renders unknown
  // notebook slugs through the page — required for their notFound() to run
  // (with output: "export" Next dev 500s on params absent from
  // generateStaticParams instead) so retired slugs 404 cleanly mid-session.
  output: process.env.NODE_ENV === "development" ? undefined : "export",
  // Export every route as <route>/index.html so GitHub Pages and any static
  // file server resolve /search and /license without extension tricks.
  trailingSlash: true,
  ...(basePath ? { basePath } : {}),
};

export default nextConfig;