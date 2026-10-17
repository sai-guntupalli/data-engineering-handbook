import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

/** Minimal scaffold: React plugin for the upcoming jsdom component tests;
 *  node environment (the default) suits the lib tests. */
export default defineConfig({
  plugins: [react()],
  test: {
    globals: false,
  },
});