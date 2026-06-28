# Using Claude with this repo

Lightweight guidance for working on Aegize with Claude (or any AI coding
assistant). The goal is consistent, low-friction sessions — not context bloat.

The single source of operating instructions is [`CLAUDE.md`](../CLAUDE.md) at the
repo root, which points at the source-of-truth docs in [`docs/`](../docs). This
file just explains how to drive a session.

## How to start a session

- Ask Claude to **read `CLAUDE.md` first.** It is short and links the docs that
  define Aegize's direction, positioning, and design.
- You should not need to paste standing instructions each time — they live in
  `CLAUDE.md`. Point Claude at it instead.

## For major changes

- Ask Claude to **check the docs for conflicts before implementing.** For
  architectural, product, branding, or significant code changes, the relevant
  docs are `vision.md`, `principles.md`, `decisions.md`, `roadmap.md`,
  `brand.md`, and `architecture.md`.
- If a request conflicts with those, Claude should **point out the conflict
  first**, not silently implement it.
- For anything large or directional, prefer an [RFC](../rfcs/README.md) over a
  big unannounced change.

## Keep prompts narrow

- One concern per prompt. Small, focused changes are easier to review and safer
  for trust infrastructure.
- After code changes, expect tests and lint to run (`python -m pytest`,
  `ruff check .`). Docs-only changes don't need them.

## Why there's no heavy hook

We intentionally do **not** auto-inject the docs into every turn. That would bloat
context and cost without improving outcomes. Persistent guidance lives in
`CLAUDE.md`; Claude reads the specific docs it needs, when it needs them. Run
`python scripts/context_check.py` to confirm the docs are present.
