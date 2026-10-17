import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

/** Minimal scaffold: React plugin for the upcoming jsdom component tests;
 *  node environment (the default) suits the lib tests. The alias mirrors
 *  tsconfig's "@/*" so tests can load components that import "@/lib/...". */
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL(".", import.meta.url)),
    },
  },
  test: {
    globals: false,
  },
});