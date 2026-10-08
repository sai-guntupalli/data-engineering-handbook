import type { NextConfig } from "next";

// GitHub Pages project pages serve the site under the repository path;
// local development keeps working at the bare origin. Set at build time:
//   NEXT_PUBLIC_BASE_PATH=/data-engineering-interview-questions
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

const nextConfig: NextConfig = {
  agentRules: false,
  reactStrictMode: true,
  // The gallery is fully static: build-time file reads only, no server features.
  output: "export",
  ...(basePath ? { basePath, trailingSlash: true } : {}),
};

export default nextConfig;