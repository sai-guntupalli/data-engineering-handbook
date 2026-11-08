/**
 * Display preferences saved in the browser, and the inline script that applies
 * them before first paint. This module must stay free of "use client": the root
 * layout (a server component) inlines BOOT_SCRIPT, and a string exported from a
 * client module would reach the server as a client reference, not as text.
 */

export const THEME_KEY = "de-handbook:theme";
export const PANEL_KEY_PREFIX = "de-handbook:";

/** The panels a reader can collapse: the navigation sidebar and the reader's table of contents. */
export type Panel = "sidebar" | "toc";
export const PANELS: Panel[] = ["sidebar", "toc"];

/**
 * Sets <html data-theme>, data-sidebar and data-toc from saved preferences, so
 * the first paint already has the right theme and panel layout.
 */
export const BOOT_SCRIPT = `(function(){try{var d=document.documentElement;var t=localStorage.getItem(${JSON.stringify(THEME_KEY)});if(t==="light"||t==="dark")d.dataset.theme=t;${JSON.stringify(PANELS)}.forEach(function(p){if(localStorage.getItem(${JSON.stringify(PANEL_KEY_PREFIX)}+p)==="collapsed")d.dataset[p]="collapsed"})}catch(e){}})();`;
