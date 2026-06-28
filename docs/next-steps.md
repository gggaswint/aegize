# Next Steps — 2-Week Execution Plan

The working plan to get Aegize from "almost launched" to "quietly launched and
learning." It is intentionally short and strict. Companion to the
[launch checklist](./launch-checklist.md); ordered by [roadmap](./roadmap.md) and
[principles](./principles.md).

_Plan date: 2026-06-27._

**Legend:** `[ ]` todo · `[~]` in progress · `[x]` done

---

## The one rule

> **No new major SDK features before the launch foundation is complete.**

The SDK is enough to launch (v0.2: identity, policy, permissions, approval
decision, audit, decorator + `guard()`/MCP-ready adapter, examples, tests, lint).
Until the foundation below is done and the project is quietly launched, the only
code changes allowed are: bug fixes, docs, and anything required to ship the
launch itself. Resist scope. Shipping and learning beats building more.

---

## Today

Small, finishable, unblock-the-launch items.

- [x] Set the GitHub repo **homepage URL** to https://aegize.com.
- [ ] Connect **www.aegize.com** in Cloudflare (custom domain or redirect to apex). Apex already serves; `www` does not resolve.
- [~] Finalize the three existing announcement drafts (LinkedIn, Show HN, X) — refresh for current positioning/URLs and save them somewhere durable. Do **not** publish yet.

## This week

Complete the launch foundation and do a quiet launch.

- [~] **GitHub profile** — exists with an Aegize-branded profile README. Remaining (web UI): fix the bio (still says "AgentGuard" → "Aegize"), set the website field to https://aegize.com, and pin the `aegize` repo. Priority #2.
- [~] **Record the 60-second video** from the existing package (`docs/launch-video.md` + the demo GIF / montage / end-card assets). Keep it simple; the assets are ready.
- [ ] **Final foundation pass** — read the README top-to-bottom as a newcomer; fix any rough edge. Confirm all links resolve (site, docs, badges, architecture SVG, demo GIF).
- [ ] **Publish quietly first** — soft launch: share the repo + site with a small, friendly audience (a few peers / one community), not the front page of anything. Priority #9.
- [ ] **Gather feedback** — open a lightweight channel (GitHub Discussions or issues) and ask the soft-launch audience two questions: is it clear what Aegize is, and would you wire it into a real agent? Priority #10.

## Before public launch

The gate before any broad announcement. Everything here must be green.

- [ ] Launch checklist's **GitHub** and **Website** sections fully `[x]` (tests, ruff, license, security, contributing, CTAs, responsive, no fake claims).
- [ ] Fresh-machine smoke test: `pip install -e .` (or the documented install), then run every example end to end.
- [ ] Site verified on real mobile + desktop; both apex and `www` resolve with valid TLS.
- [ ] Announcement posts finalized, each leading with infrastructure (not security/AI-doom) per [brand.md](./brand.md), with correct URLs.
- [ ] Decide the single primary launch surface (likely Show HN) and the support cast (LinkedIn, X, Reddit, email).

## Immediately after launch

Be present and responsive; do not start building.

- [ ] Watch the launch surfaces and **respond to every comment** for the first day or two — calm, technical, non-defensive.
- [ ] Triage incoming issues: label, reproduce, fix only what is small and clearly correct. Park feature requests in [questions.md](./questions.md) / as RFC candidates.
- [ ] Write down what people actually asked for and where they got confused. This is the most valuable output of launch.
- [ ] Fix only **blocking** bugs and doc gaps. No new features in the launch window.

## Later (after the launch foundation, only once quietly launched)

Resume real engineering — driven by the [RFCs](../rfcs/README.md) and feedback,
in roadmap order. None of this begins before the foundation is done.

- [ ] Promote an RFC to Accepted and implement it — likely **RFC 0002 (policy schema + CLI validator)**: low-risk, high-leverage, already on the roadmap.
- [ ] **MCP adapter** (RFC-tracked) — the first protocol integration.
- [ ] **Tamper-evident audit logs** (RFC 0003) and **approval workflow** (RFC 0004) as v1.0 work.
- [ ] Pluggable audit sinks and per-environment policy overlays (v0.4).

---

## Do NOT do yet

Explicitly out of scope until well after launch. If a task pulls toward one of
these, stop — it is a distraction from shipping and learning.

- ❌ **Hosted dashboard** — later, not now ([decision 011](./decisions.md), roadmap "future platform").
- ❌ **Enterprise features** — org-level policy, SSO, RBAC consoles. Not before there are users.
- ❌ **Pricing / commercialization** — open source first ([decision 006](./decisions.md)); no pricing page, no paid tier.
- ❌ **Complex auth system** — no PKI/credential service build-out; identity stays declared (see [RFC 0001](../rfcs/0001-agent-identity.md)).
- ❌ **Multi-agent protocol implementation** — it's an open question and an RFC at most, not code.
- ❌ **Large refactors** — no rewrites or architecture churn before launch; small, focused changes only.

---

## Priority map

How the ten current priorities sit against this plan:

| # | Priority | Status |
| - | -------- | ------ |
| 1 | Finish rename to Aegize | `[x]` done |
| 2 | Finish GitHub profile | `[~]` exists; bio/website/pin remaining |
| 3 | Finish repo README | `[x]` done |
| 4 | Add website link | `[x]` README, pyproject, and repo homepage all set |
| 5 | Add architecture diagram | `[x]` done (`assets/architecture.svg`) |
| 6 | Add demo GIF | `[x]` done (`assets/demo.gif`) |
| 7 | Launch aegize.com | `[~]` apex live; `www` pending (today) |
| 8 | Prepare announcement posts | `[~]` 3 of 5 drafted; finalize this week, publish at launch |
| 9 | Publish quietly first | `[ ]` this week |
| 10 | Gather feedback | `[ ]` this week |
