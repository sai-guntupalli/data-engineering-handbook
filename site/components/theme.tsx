"use client";

import { Moon, Sun } from "@phosphor-icons/react";

const THEME_KEY = "de-handbook:theme";

/** Runs in <head> before first paint so a saved theme never flashes the other one. */
export const THEME_BOOT_SCRIPT = `(function(){try{var t=localStorage.getItem("${THEME_KEY}");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}})();`;

function isDark(): boolean {
  const chosen = document.documentElement.dataset.theme;
  if (chosen) return chosen === "dark";
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

/** Switches between light and dark and remembers the choice. Icons swap in CSS, so no hydration flicker. */
export function ThemeToggle() {
  function toggle() {
    const next = isDark() ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try {
      window.localStorage.setItem(THEME_KEY, next);
    } catch {
      // Storage blocked: the theme still changes for this page view.
    }
  }

  return (
    <button type="button" className="btn btn-ghost btn-icon theme-toggle" onClick={toggle} aria-label="Switch colour theme">
      <Moon size={17} className="i-moon" aria-hidden />
      <Sun size={17} className="i-sun" aria-hidden />
    </button>
  );
}
