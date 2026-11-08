import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { describe, expect, it } from "vitest";
import { BOOT_SCRIPT, PANEL_KEY_PREFIX, THEME_KEY } from "../lib/boot";

/** Run the boot script against a fake document and storage; return the resulting data-* attributes. */
function boot(stored: Record<string, string>, throwOnRead = false): Record<string, string> {
  const dataset: Record<string, string> = {};
  const localStorage = {
    getItem: (key: string) => {
      if (throwOnRead) throw new Error("storage blocked");
      return stored[key] ?? null;
    },
  };
  vm.runInNewContext(BOOT_SCRIPT, { document: { documentElement: { dataset } }, localStorage });
  return dataset;
}

describe("BOOT_SCRIPT", () => {
  it("is a plain string, so the server layout can inline it", () => {
    expect(typeof BOOT_SCRIPT).toBe("string");
    const source = fs.readFileSync(path.join(__dirname, "../lib/boot.ts"), "utf8");
    expect(source).not.toMatch(/^["']use client["']/m);
  });

  it("applies a saved theme and collapsed panels", () => {
    expect(
      boot({ [THEME_KEY]: "dark", [`${PANEL_KEY_PREFIX}sidebar`]: "collapsed", [`${PANEL_KEY_PREFIX}toc`]: "collapsed" }),
    ).toEqual({ theme: "dark", sidebar: "collapsed", toc: "collapsed" });
  });

  it("ignores unknown or expanded values", () => {
    expect(boot({ [THEME_KEY]: "sepia", [`${PANEL_KEY_PREFIX}sidebar`]: "expanded" })).toEqual({});
  });

  it("does nothing when storage is blocked", () => {
    expect(boot({}, true)).toEqual({});
  });
});
