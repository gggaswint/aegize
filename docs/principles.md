# Principles

The engineering and product principles that guide how Aegize is built. They are
deliberately few and deliberately opinionated. When a decision is unclear, these
are the tie-breakers. They are downstream of the [vision](./vision.md) and should
stay consistent with the [brand](./brand.md).

---

## Default deny

Nothing runs unless it is explicitly allowed. Absence is denial. This is the only
safe default for a system on the critical path of real-world actions: it fails
closed, and it makes policy auditable, because anything not enumerated is denied
by construction. Unknown agents and unknown tools resolve to deny.

## Runtime first

Trust is enforced in code that runs, not in advice the model may ignore.
Prompt-level guidance is non-deterministic and unreviewable; a trust boundary
must hold regardless of what the model decides. Aegize composes with prompt-level
techniques but never depends on them for its guarantees.

## Vendor neutral

Aegize governs the *action*, not the model. It must work across OpenAI,
Anthropic, Google, open-source models, and systems that do not exist yet. We do
not couple the core to any single provider, framework, or runtime. Vendor names
appear as integration targets, never as dependencies of the core.

## Open source first

Infrastructure that sits between an agent and the outside world must be
inspectable. Developers should not — and will not — route their actions through a
black box. The open-source core comes before any hosted or commercial surface,
and any such surface is built on top of it, not in place of it.

## Developer-first

The primary user is an engineer integrating Aegize into a real system. Optimize
for their experience: a small API, readable source, honest docs, and working
examples. If a feature cannot be explained to a developer in a few sentences, it
is probably the wrong feature or the wrong shape.

## Simple beats clever

This is security-adjacent infrastructure that people have to trust. Clarity is a
feature. Prefer the obvious implementation over the impressive one, the readable
abstraction over the powerful-but-opaque one. Cleverness that cannot be reviewed
is a liability.

## Protocols over proprietary APIs

Where a standard or open protocol exists (e.g. MCP), integrate with it rather
than inventing a closed interface. The goal is to be the layer actions pass
through, which means meeting agents and tools where they already are. Favor
interoperability over lock-in, including our own.

## Trust before automation

The point of Aegize is not to make agents act faster; it is to make their actions
trustworthy. When trust and automation conflict, trust wins: prefer a human gate,
an explicit allow, and a recorded decision over silent convenience. Automation is
earned by understanding and control, not assumed.

## Audit everything meaningful

Every attempted action that crosses the boundary is recorded — allowed, denied,
gated, or failed — before execution is attempted, with the outcome appended
after. "What did this agent try to do, and what happened?" must always have a
precise answer, including the attempts that were blocked. Audit is part of the
control loop, not a side effect.

## Security is a capability, not the brand

Good infrastructure produces security as one of several outcomes — alongside
operability, reviewability, and confidence in deployment. We do not lead with the
word "security," and we do not position Aegize as a security product first.
Identity, policy, approvals, audit, and observability deliver security *and* the
rest; collapsing all of that into "security" undersells it.

## Infrastructure over applications

Aegize is a layer, not an app. We build primitives and extension points, not
end-user features or workflows on top of them. We would rather ship one clean
boundary that many systems can build on than a vertical product that serves one
use case. Dashboards, workflows, and integrations are layers above the core —
later, and optional.
