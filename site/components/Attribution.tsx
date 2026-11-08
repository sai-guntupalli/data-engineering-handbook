"use client";

import { useState } from "react";
import { Check, Copy } from "@phosphor-icons/react";

/** Copy-to-clipboard for the ready-made credit line on the license page.
 *  Attribution should never be a typing exercise. */
export function Attribution({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      // clipboard unavailable (permissions/insecure context): the pre stays
      // selectable so users can copy manually.
    }
  }

  return (
    <div className="attribution">
      <pre className="attribution-pre">{text}</pre>
      <button type="button" className="copy-button" onClick={() => void copy()}>
        {copied ? <Check size={14} weight="bold" /> : <Copy size={14} weight="bold" />}
        {copied ? "Copied — paste it wherever you share this" : "Copy the credit"}
      </button>
    </div>
  );
}