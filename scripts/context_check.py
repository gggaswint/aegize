#!/usr/bin/env python3
"""Check that Aegize's source-of-truth documents exist.

These documents guide Claude and project decisions (see CLAUDE.md). Run this
before significant changes — or in CI — to catch a missing or renamed doc early.

    python scripts/context_check.py

Exits non-zero if any required document is missing.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The operating guide plus the source-of-truth docs it points at.
REQUIRED = [
    "CLAUDE.md",
    "docs/vision.md",
    "docs/principles.md",
    "docs/decisions.md",
    "docs/roadmap.md",
    "docs/brand.md",
    "docs/architecture.md",
]

REMINDER = (
    "These are the source of truth for Aegize — they guide Claude and project\n"
    "decisions. Read them before architectural, product, branding, or significant\n"
    "code changes. See CLAUDE.md."
)


def main() -> int:
    found = [rel for rel in REQUIRED if (ROOT / rel).is_file()]
    missing = [rel for rel in REQUIRED if rel not in found]

    for rel in REQUIRED:
        mark = "✅" if rel in found else "❌"
        suffix = "" if rel in found else "  (missing)"
        print(f"  {mark} {rel}{suffix}")

    print()
    print(REMINDER)

    if missing:
        print()
        print(f"Missing {len(missing)} required document(s). Aborting.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
