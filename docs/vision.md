# Vision

## Mission

Build the trust layer for autonomous AI.

## Product positioning

Aegize is infrastructure for autonomous AI agents. It is the runtime layer
between an agent and the tools it uses, providing identity, policy, permissions,
approvals, audit logging, observability, and runtime governance for every AI
action.

## The problem

For most of its history, software answered questions. You asked, it responded,
and a human decided what to do with the answer. AI is now crossing a line that
software has never crossed at this scale: it *takes actions*.

Modern agents can already:

- execute code
- send emails
- modify databases
- call APIs
- access files
- deploy infrastructure
- spend money
- coordinate with other agents

Each of these is a real action with real consequences, and the decision to take
it is made by a non-deterministic model. The model is, in effect, the thing
standing between intent and the outside world. That is a poor place to put the
boundary. It cannot be reviewed, scoped, or audited the way every other actor in
a production system can.

The bottleneck for autonomous AI will not be capability. Models are getting more
capable quickly. The bottleneck will be **trust** — an organization's ability to
let an agent act without giving up control or visibility.

## The thesis

> Every meaningful AI action should pass through trusted runtime infrastructure
> before reaching the outside world.

Trust is not a property of a model. It is a property of the system the model
operates in. You earn it the same way you earn it for human operators and
service accounts: give every actor an identity, scope what it is permitted to
do, require a human in the loop for high-impact actions, and keep a complete
record of what happened.

Aegize makes that layer concrete. It sits at the boundary where an agent's
decisions become actions, and it governs the crossing.

## Why now

Three things are true at the same time, for the first time:

1. **Agents are leaving the chat window.** Tool use, function calling, and
   protocols like MCP have made "an AI that does things" the default shape of
   new products, not a research demo.
2. **The controls are missing.** Teams are wiring models directly to shells,
   inboxes, and databases, and substituting the model's own judgment for the
   permissioning and audit they would never skip for a human or a script.
3. **The cost of getting it wrong is now operational, not hypothetical.** A
   wrong action is a deleted table, a sent email, or a charged card — concrete,
   attributable, and reviewable. Concrete problems want infrastructure, not
   exhortation.

The window to define this layer — the way it should work, what its primitives
are, and how it integrates — is open now.

## What Aegize is

- A **runtime governance layer** for AI actions: identity, policy, permissions,
  approvals, audit, and observability.
- **Vendor-neutral.** It governs the *action*, not the model. It is designed to
  work across OpenAI, Anthropic, Google, open-source models, and AI systems that
  do not exist yet.
- **Developer-first and open source.** A small, readable SDK you can adopt in an
  afternoon and reason about in production.
- **Deterministic where the model is not.** Policy is declared, versioned, and
  enforced the same way every time.

## What Aegize is not

- It is **not an AI safety organization** and makes no claims about preventing
  existential risk. It is operational infrastructure for the actions agents take
  today.
- It is **not a model, a guardrail prompt, or a content filter.** It does not try
  to change what a model thinks; it governs what a model is allowed to do.
- It is **not a security product first.** Security is one outcome of running
  good infrastructure. Operability, reviewability, and confidence in deployment
  are equally the point.
- It is **not tied to any one framework or vendor**, and it will not become so.

## Core principles

1. **The boundary belongs in infrastructure, not in the model.** Trust comes
   from the system around the model.
2. **Default deny.** If nothing explicitly allows an action, it does not happen.
3. **Every attempt is on the record.** Allowed, denied, gated, or failed — it is
   audited before execution is attempted.
4. **Declarative over clever.** Policy lives in version control and is reviewed
   like any other code.
5. **Vendor-neutral by construction.** Govern the action, never depend on the
   model.
6. **Readable beats impressive.** This is infrastructure people must trust;
   clarity is a feature.
7. **Honest about maturity.** We describe what exists, not what we hope to ship.

## Long-term ambition

The long arc is to become the standard, vendor-neutral layer that AI actions
pass through — the place where an organization defines what its agents may do,
sees what they are doing, and keeps the record of what they did. It begins as a
local SDK, grows into integrations and observability, and matures into runtime
governance that can be operated across teams, environments, and fleets of
agents.

If we succeed, "what is this agent allowed to do, and what has it done?" will
have a precise, infrastructural answer — the same way that question already does
for every human and service account in a serious system.

## One-sentence summary

Aegize is the runtime trust layer for autonomous AI: every meaningful AI action
passes through identity, policy, permissions, approval, and audit before it
reaches the outside world.
