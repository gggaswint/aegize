# Launch Kit

The complete launch package for Aegize — drafts and checklists, ready for review.
**Nothing here is published.** Tone throughout: honest, technical, calm,
developer-first; no hype, no overclaiming. See [brand.md](./brand.md).

Facts to keep accurate: open source (MIT), **v0.2.0**, a Python SDK, **not on
PyPI yet** (install from source), enforcement + audit work today, the full
approval *workflow* and observability surface are still ahead.

---

## 1. LinkedIn launch post

For most of its history, software answered questions. You asked, it responded,
and a person decided what to do next.

That's changing. AI agents now take *actions* — they run code, send email, query
databases, call APIs, move money. The decision to act is made by a model, in a
place that's hard to review, scope, or audit.

I've been building agents that touch real systems, and the same gap kept showing
up: the model had quietly become the control boundary. That's a hard place to put
your trust.

So I started building **Aegize** — infrastructure for autonomous AI agents. It's
the runtime layer between an agent and the tools it uses. Every action passes
through it before reaching the outside world:

• **Identity** — every action is attributed to a named agent and environment.
• **Policy** — what an agent may do is declared in YAML, in version control.
• **Permissions** — scoped to specific tools and operations. Default deny.
• **Approval** — high-impact actions can require a human before they run.
• **Audit** — every attempt, allowed or not, is written to an append-only log.
• **Governance** — deterministic enforcement at the boundary, not prompt-level hope.

These are the same controls we already give human operators and service accounts.
Aegize applies them to agents.

It's early and open source (MIT). The mission behind it: build the trust layer for
autonomous AI — so teams can let agents act without giving up control or
visibility.

If you're building with agents, I'd genuinely value your read on the model and
where it should go next.

🔗 Website: https://aegize.com
💻 GitHub: https://github.com/gggaswint/aegize

What would you need to see before routing an agent's actions through something
like this?

---

## 2. Hacker News — Show HN

**Title:** `Show HN: Aegize – Infrastructure for autonomous AI agents`

**Body:**

Aegize is an open-source runtime layer that sits between an AI agent and the
tools it calls. Before a tool runs, the action gets an identity, is checked
against a policy you write, can be gated for human approval, and is written to an
append-only audit log.

Why I built it: I kept wiring agents directly into shells, email, and internal
APIs and realized the model itself had become the thing deciding what was safe to
do — which is hard to review, scope, or audit. I wanted that boundary in
deterministic code I control, not in a prompt.

What it does today (v0.2, Python):

- Wrap any function with `GuardedTool(...)` or a `@guarded_tool` decorator.
- Policy is per-agent YAML: `allow` / `deny` / `require_approval`. Default deny;
  deny wins; an unknown agent or tool is denied.
- Denied and approval-gated actions never execute the wrapped function.
- Audit-first: the decision is recorded before execution; the result after. JSONL,
  one event per line.
- `guard()` returns a signature-preserving callable, so it drops into tool
  registries (e.g. MCP).
- One runtime dependency (PyYAML), typed, tested, MIT. Not on PyPI yet — it's a
  `pip install -e .` from the repo for now.

What it isn't: not a model, not a prompt guardrail, not an agent framework. It
governs the action, not the model, so it's vendor-neutral.

Honest about maturity: approval is a real gate today (the function doesn't run),
but the full approval *workflow* (durable queue, out-of-band grant) and a proper
observability surface are still ahead. It's early.

Direction: tamper-evident audit logs, an MCP adapter, a policy schema + CLI
validator, pluggable approval backends and audit sinks. The roadmap and RFCs are
in the repo.

Feedback I'm after: does the policy model hold up for real agent setups? Is
default-deny + YAML the right default, or do you want a capability model? Where
would this break in your stack?

Repo: https://github.com/gggaswint/aegize · Site + playground: https://aegize.com
(There's a small in-browser sandbox on the site that simulates the
allow/approval/deny flow — no backend, purely illustrative.)

---

## 3. X / Twitter thread

**1/** AI is changing shape. For years it answered questions. Now it takes
actions — running code, sending email, moving money, calling APIs.

**2/** When an agent can act, the model becomes the thing deciding what's safe to
do. That's a strange place to put your trust: non-deterministic, hard to review,
hard to audit.

**3/** We already solved this for people and services. They don't get raw access
to production — they get an identity, scoped permissions, approvals for big
actions, and an audit trail.

**4/** Agents deserve the same. Not a smarter prompt — infrastructure: a layer
every action passes through before it reaches the outside world.

**5/** That's what I'm building: **Aegize**, the runtime trust layer between an
agent and its tools. Identity, policy, permissions, approval, audit —
deterministic, in code you control.

**6/** The bet: the limiting factor for autonomous AI won't be capability. It'll
be *trust* — whether an organization can let agents act without losing control or
visibility.

**7/** It's early and open source. If you're building agents that do real things,
I'd love your take.
https://github.com/gggaswint/aegize

---

## 4. Reddit posts (adapted per subreddit)

### r/Python

**Title:** Aegize – a small default-deny policy + audit layer for AI agent tool calls (open source)

I built an open-source Python SDK that governs what an AI agent is allowed to do
when it calls tools. Wrap a function with `@guarded_tool` (or `GuardedTool(...)`),
declare per-agent policy in YAML (`allow` / `deny` / `require_approval`), and
every attempt is written to an append-only JSONL audit log. Default-deny, so
denied and approval-gated calls never execute.

It's deliberately small: one runtime dependency (PyYAML), fully typed, pytest +
ruff, MIT. Not on PyPI yet — `pip install -e .` from the repo. I'd love feedback
on the API shape and the policy model.

Repo: https://github.com/gggaswint/aegize

### r/MachineLearning

**Title:** [P] Aegize – runtime governance for AI agent actions (identity, policy, approval, audit)

As agents move from answering to acting (tool use, MCP), the decision to take an
action is made by the model and is hard to review or audit. Aegize is an
open-source runtime layer that enforces per-agent policy on tool calls
deterministically (default-deny), gates high-impact actions for human approval,
and records every attempt. It governs the action, not the model, so it's
vendor-neutral.

Early (v0.2, Python). Honest scope: enforcement + audit work today; a durable
approval workflow and an observability surface are still ahead. I'm curious
whether people see this as the right layer, and how you'd want multi-agent
governance (agents acting on behalf of agents) to work.

Repo: https://github.com/gggaswint/aegize

### r/artificial

**Title:** I built an open-source "trust layer" for autonomous AI agents

AI is shifting from software that answers questions to software that takes
actions — running code, sending email, calling APIs. When an agent can act, you
want the same controls you give people: identity, permissions, approvals, and an
audit trail.

Aegize is an open-source layer that every agent action passes through before it
reaches the outside world. It's early, and I'm building it in the open. Would
love thoughts on the idea — what would make you trust an agent enough to let it
act?

Site: https://aegize.com · Repo: https://github.com/gggaswint/aegize

### r/programming

**Title:** Aegize – infrastructure between AI agents and the tools they use (open source)

The engineering problem: agents are being wired straight into shells, email, and
internal APIs, with a non-deterministic model deciding what's safe. I wanted that
boundary in deterministic code, not a prompt.

Aegize wraps tool calls with identity, a YAML policy engine (default-deny:
allow / deny / require_approval), human approval gates, and append-only audit
logs. It governs the action rather than the model, so it's vendor-neutral. One
dependency, MIT, early but usable. Design feedback welcome.

Repo: https://github.com/gggaswint/aegize

---

## 5. Launch checklist (verify before publishing)

Pre-publish verification. (Complements [launch-checklist.md](./launch-checklist.md).)

- [ ] **Website** — `aegize.com` loads, hero + sections render, no console errors.
- [ ] **README** — renders on GitHub in **both** light and dark; logo, badges,
  GIF, and architecture SVG all display; links resolve.
- [ ] **Playground** — `aegize.com/playground` works; all five tools resolve
      (allowed / approval / denied) and write audit rows.
- [ ] **Architecture SVG** — `assets/architecture.svg` renders correctly in the
      README and on the site.
- [ ] **Demo GIF** — plays in the README and the website demo section.
- [ ] **Documentation** — `docs/` links resolve from the README; RFCs present.
- [ ] **Examples** — every script in `examples/` runs end to end.
- [ ] **Tests** — `pytest` green.
- [ ] **Lint** — `ruff check .` clean.
- [ ] **License** — `LICENSE` (MIT) present and referenced.
- [ ] **GitHub profile** — bio, logo, website link, and a pinned `aegize` repo.
- [ ] **Social preview** — uploaded to the repo (Settings → Social preview).
- [ ] **`pip install` story** — README install matches reality (from source, or
      PyPI if published).

## 6. Asset checklist

Everything that should accompany the launch (all committed unless noted):

- ✓ Logo — `assets/logo.png` (full), `assets/logo-light.png` / `assets/logo-dark.png` (theme-aware)
- ✓ Favicon — `web/src/app/icon.png`
- ✓ Architecture SVG — `assets/architecture.svg` (canonical)
- ✓ README GIF / demo GIF — `assets/demo.gif`
- ✓ Social preview image — `assets/social-preview.png` (1280×640)
- ✓ OG / link image — `web/public/og.png` (end card, 1920×1080)
- ✓ Capability montage — `assets/capability_montage.gif` (video shot 2)
- ✓ End card — `assets/end_card.png` (video shot 9)
- ✓ 60-second video package — `docs/launch-video.md` + the assets above
  (final recorded cut: **not yet produced**)
- ☐ Homepage screenshot — capture from `aegize.com` (see review §8 / report list)
- ☐ Playground screenshot — capture from `aegize.com/playground`
- ☐ README hero screenshot — capture from GitHub (light + dark)
- ☐ Code-example screenshot — capture the README code block or the site

## 7. Social preview image

**File:** `assets/social-preview.png` (1280×640) — regenerate with
`python scripts/generate_social_preview.py`.

Design: dark canvas, the Aegize mark centered, a thin accent rule, the tagline
**"Infrastructure for autonomous AI agents."**, and **aegize.com**. No clutter.
It is GitHub's recommended social-preview size and a clean 2:1 for link cards.

How to use:
- **GitHub:** repo → Settings → Social preview → upload `assets/social-preview.png`.
- **LinkedIn / X:** they pull the site's Open Graph image (`og.png`); attach
  `social-preview.png` directly to posts where you want the branded card.

## 8. Website review checklist (manual QA)

Walk `aegize.com` (and `/playground`) through each before launch.

**Desktop (≥1280px)**
- [ ] Hero spacing, logo, headline, CTAs aligned and centered.
- [ ] Runtime pipeline animates and loops; verdict colors correct.
- [ ] Sandbox: all five tools resolve; audit log accumulates.
- [ ] Architecture diagram renders crisply.
- [ ] Footer columns and links aligned.

**Tablet (~768–1024px)**
- [ ] Sections reflow; no awkward gaps or cramped grids.
- [ ] Sandbox 3-column layout degrades cleanly.

**Mobile (~375–414px)**
- [ ] No horizontal scroll anywhere (hero, sandbox, footer).
- [ ] Tap targets (buttons, tools) are large enough.
- [ ] Sandbox reflows: agent → tools → pipeline → audit.

**Dark / light**
- [ ] Site is dark-first; the architecture SVG and README adapt in both GitHub themes.

**Links**
- [ ] GitHub, Docs, Website, Playground, footer (License, Contact) all resolve.
- [ ] `www.aegize.com` resolves (currently apex only — fix before launch).

**Performance**
- [ ] Lighthouse ≥ 90 (perf/a11y/best-practices/SEO).
- [ ] Images sized; no layout shift; fonts load without flash.

**Accessibility**
- [ ] Keyboard-navigable; visible focus states.
- [ ] Color contrast passes; `prefers-reduced-motion` respected.
- [ ] Alt text on images; semantic landmarks.

**Typos / copy**
- [ ] Read every line aloud; consistent terminology (infrastructure / trust layer).
- [ ] No placeholder text, no broken markdown, correct URLs.
