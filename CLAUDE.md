# CLAUDE.md

Operating instructions for AI coding sessions (Claude or otherwise) working in
this repository. Read this first.

Aegize is **infrastructure for autonomous AI agents** — the runtime layer between
an agent and the tools it uses (identity, policy, permissions, approvals, audit,
observability). Mission: **build the trust layer for autonomous AI.** Core idea:
*every meaningful AI action should pass through trusted runtime infrastructure
before reaching the outside world.*

## Before any major change, read the docs

The documents in `docs/` are the **source of truth** for this project. Before
making a non-trivial change, read:

- [`docs/vision.md`](./docs/vision.md) — thesis, problem, what Aegize is / is not.
- [`docs/principles.md`](./docs/principles.md) — the tie-breakers (default deny,
  runtime first, vendor neutral, simple beats clever, …).
- [`docs/decisions.md`](./docs/decisions.md) — decisions already made, and why.
- [`docs/roadmap.md`](./docs/roadmap.md) — where the project is and is going.

Also relevant: [`docs/architecture.md`](./docs/architecture.md),
[`docs/brand.md`](./docs/brand.md), [`docs/anti-goals.md`](./docs/anti-goals.md),
[`docs/questions.md`](./docs/questions.md), and the
[RFC process](./rfcs/README.md).

## How to work here

1. **Treat the docs as source of truth.** If code and docs disagree, the docs
   describe the intended state. Align to them, or change them deliberately.
2. **Flag conflicts; do not silently implement.** If a request conflicts with the
   vision, principles, decisions, or anti-goals, say so clearly and explain the
   conflict before proceeding. Surfacing the tension is the job — do not quietly
   pick a side.
3. **Keep language aligned with `brand.md`.** Lead with infrastructure and
   governance. Use the approved vocabulary; avoid the words-to-avoid list.
4. **Avoid security-first or AI-doom framing.** Security is one capability, not
   the brand. Never use fear-based or existential-risk messaging, and do not
   frame Aegize as an AI-safety nonprofit.
5. **Preserve the public API** unless the task is explicitly to change it. The
   public surface is what `src/aegize/__init__.py` exports. If a change is
   warranted, call it out, and for anything significant prefer an
   [RFC](./rfcs/README.md).
6. **Run tests and lint after code changes** (see below). Do not claim success
   without running them.
7. **Prefer small, focused changes.** One concern per change. Match the
   surrounding code's style and conventions. Readable beats clever — this is
   trust infrastructure.

## Repository layout

- `src/aegize/` — the Python SDK (the product). Core primitives:
  `AgentIdentity`, `ToolAction`, `PermissionPolicy`, `GuardedTool`,
  `GuardContext`, `AuditLog`, plus `@guarded_tool` / `guard()` and the exceptions.
- `tests/` — pytest suite. `examples/` — runnable examples.
- `docs/` — source-of-truth documents (read these). `rfcs/` — the RFC process.
- `web/` — the aegize.com site (Next.js 15, static export). Self-contained.
- `scripts/` — asset generators (demo GIF, montage, end card). `assets/` — images.

## Commands

Python SDK (run from the repo root, using the project's virtualenv):

```bash
python -m pytest        # full test suite — must pass
ruff check .            # lint — must be clean
```

Website (only when touching `web/`):

```bash
cd web
npm install             # first time
npm run build           # static export to web/out — must succeed
```

## Non-negotiable invariants

These reflect decisions in `decisions.md` and `principles.md`. Do not weaken them
without an explicit, recorded decision:

- **Default deny.** No matching allow rule means the action is denied. Unknown
  agent or tool → deny.
- **Deny wins** over approval and allow.
- **Gated and denied actions never execute** the wrapped function.
- **Audit-first:** the decision is recorded before execution is attempted; the
  result is recorded after.
- **Dependency-light core.** The SDK runtime depends on PyYAML and nothing else.
  New runtime dependencies are a hard sell and need justification.

## When in doubt

Ask, or write it down. If a question is bigger than the change in front of you,
add it to [`docs/questions.md`](./docs/questions.md) or open an
[RFC](./rfcs/README.md) rather than guessing in code.
