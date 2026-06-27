# RFC 0004: Approval Workflow

- Status: Draft
- Date: 2026-06-27
- Related: [questions.md](../docs/questions.md) (approval), [architecture.md](../docs/architecture.md) (approval model), [roadmap.md](../docs/roadmap.md) (v1.0)

## Summary

Turn approval from a *decision* into a *workflow*. Today `require_approval` is a
first-class policy outcome that blocks execution and raises `ApprovalRequired`,
but there is no durable way to grant approval out of band and re-issue the
approved action. This RFC proposes an approval request abstraction, pluggable
approval backends, and a safe re-issue path — while keeping the strong guarantee
that gated actions never execute automatically.

## Motivation

The human-in-the-loop gate is one of Aegize's most valuable capabilities and a
direct expression of "trust before automation." Right now the gate is real but
the *workflow* is left entirely to the caller: there is no notion of an approval
request, an approver, expiry, or replay-safe execution after approval. To make
high-impact actions both safe and operable, the gate needs a defined lifecycle
that integrates with the human processes teams already use (chat, ticketing,
webhooks) without weakening the guarantee.

## Goals

- A defined approval lifecycle: requested → approved/denied → (if approved)
  executed, or expired.
- Pluggable approval **backends** (e.g. chat, webhook, queue) behind one interface.
- A **safe re-issue path**: an approved action runs once, as approved, without
  the agent being able to alter it after the fact.
- Preserve the invariant: a gated action never executes until explicitly approved.

## Non-goals

- Building a hosted approval UI (future platform).
- Defining who is *allowed* to approve at an org level (depends on identity and
  permission inheritance; see RFC 0001 and the multi-agent question).
- Changing the policy model (RFC 0002) or audit format (RFC 0003), beyond emitting
  approval lifecycle events.

## Proposed design

- **Approval request.** When policy returns `require_approval`, Aegize produces a
  durable approval request capturing the full `ToolAction` (identity, tool,
  operation, inputs, risk) and a stable request id. The wrapped function does not
  run.
- **Backends.** A small interface — submit a request, await/receive a decision —
  with adapters for common channels (webhook, queue, chat). The default remains
  the exception (`ApprovalRequired`) so today's callers are unaffected.
- **Grant + re-issue.** An approval authorizes *that specific action* (bound to
  the request id and a hash of the action), with an expiry. Re-issuing runs the
  original action; the agent cannot substitute different inputs after approval.
- **Anti-self-approval.** The approver principal must differ from the acting
  agent; this is enforced, not advisory.
- **Audit.** Every step emits audit events: `approval_required` (today), plus
  `approval_granted` / `approval_denied` / `approval_expired`, then the normal
  execution outcome on re-issue.

## Current implementation

`require_approval` is a policy decision. On that outcome, `GuardedTool` writes an
`approval_required` audit record and raises `ApprovalRequired`; the underlying
function does **not** execute. The integration point is the exception — callers
route it to whatever human process they have. There is no durable request,
backend, expiry, or re-issue mechanism yet. The guarantee (no automatic
execution of gated actions) already holds.

## Future direction

- **Durable approval queues** with persistence and backpressure.
- **Delegation** — approval authority that can be granted and attenuated, tied to
  identity and permission inheritance.
- **Organization-level approval policy** — who may approve what, by environment.
- **Notifications and SLAs** — reminders, timeouts, and escalation.

## Open questions

- How is approval authority delegated, and what is the trust model for an approver?
- How do we make re-issue replay-safe and idempotent (single-use grants, action
  hashing, expiry windows)?
- Should approval state live in Aegize, in the backend, or both, for the
  local-first case vs. a networked deployment?
- How do approvals interact with multi-agent chains (who approves an action an
  agent takes on behalf of another)?

## Alternatives considered

- **Exception-only (status quo).** Simple and unopinionated, but pushes all
  lifecycle, durability, and safety concerns onto every caller. Kept as the
  default path; this RFC layers a workflow on top rather than replacing it.
- **Embed a general workflow engine.** Powerful but heavy and against
  infrastructure-over-applications; Aegize should define the gate and integrate
  with external systems, not become a workflow product.
- **Allow the agent to self-approve under a threshold.** Rejected — undermines the
  purpose of the gate and the anti-self-approval property.
