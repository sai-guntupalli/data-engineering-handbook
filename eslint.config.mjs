import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

/** @type {import("eslint").Linter.Config} */
const config = [
  ...nextCoreWebVitals,
  ...nextTypescript,
  {
    // Global ignores: build output, dependencies and non-JS environments.
    ignores: [".next/**", "out/**", "node_modules/**", ".venv/**", "scripts/**"],
  },
];

export default config;