"use client";

import { useState } from "react";

export function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard unavailable */
    }
  }

  return (
    <button
      type="button"
      onClick={copy}
      className="font-mono text-xs text-faint transition-colors hover:text-fg"
      aria-label={copied ? "Copied" : "Copy code"}
    >
      {copied ? "copied" : "copy"}
    </button>
  );
}
