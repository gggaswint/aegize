# RFC 0007: Mutating-Action Safety

- Status: Draft
- Date: 2026-06-28
- Origin: community architecture feedback (2026-06)
- Related: [RFC 0002 (Policy Engine)](./0002-policy-engine.md), [RFC 0006 (Resource-Scoped Permissions)](./0006-resource-scoped-permissions.md), [RFC 0004 (Approval Workflow)](./0004-approval-workflow.md)

> Draft for discussion. This RFC captures a direction; it does **not** assume the
> proposal is accepted.

## Summary

Explore whether Aegize should treat **mutating (write) actions** differently from
read actions — recognizing that the cost of a wrong write is categorically higher
than a wrong read. Concepts to weigh: blast-radius classification, dry-run support,
idempotency keys, and rollback notes.

## Motivation

A denied or mis-issued *read* is cheap. A *write* — a deleted table, a sent email,
a charged card, a restarted auth service — is not. Uniform treatment of all tool
calls under-serves exactly the actions that matter most. Governance should be able
to ask for more assurance before a high-blast-radius write proceeds.

There is an important boundary to settle here: **Aegize governs and records; it
does not implement tool semantics.** Idempotency, dry-run execution, and rollback
are properties of the *tool*. Aegize's role is to *require*, *record*, and
*verify the presence of* these properties via policy — not to implement them. This
RFC is partly about drawing that line cleanly.

## Current limitations

- Aegize treats every tool call uniformly: `allow` / `deny` / `require_approval`.
- `risk_level` is a coarse, self-declared hint, not a notion of effect.
- There is no concept of read vs write vs destructive, no blast-radius signal, no
  dry-run gate, and no place to record idempotency keys or rollback notes.

## Proposed direction

A few composable, optional ideas — not all are necessarily adopted:

- **Effect / blast-radius classification.** An action can carry an effect
  (`read` / `write` / `destructive`) and a blast-radius hint (e.g. single record vs
  whole table vs service). Declared by the tool, or by policy, or inferred — TBD.
- **Policy can demand more for risky writes.** A capability (see RFC 0006) could
  require `require_approval`, or require a successful **dry-run** first, for
  high-blast-radius writes.
- **Record safety metadata.** When a tool supports them, the **idempotency key**
  and a **rollback note** are captured in the decision/audit record, so "what
  could be undone, and how" is auditable after the fact.
- **Verify, don't implement.** Aegize checks that required safety properties are
  present/declared; the tool implements them.

## Open questions

- Where exactly is the boundary between Aegize (govern + record) and the tool
  (implement idempotency / dry-run / rollback)? Can Aegize meaningfully *enforce*
  dry-run-before-commit, or only require evidence of it?
- How is blast radius determined — declared by the tool, asserted by policy, or
  inferred from arguments? Inference risks being wrong in dangerous ways.
- Does effect classification belong in the capability model (RFC 0006) rather than
  here?
- How does this avoid becoming tool-specific knowledge baked into Aegize (a
  vendor-neutrality and "governs the action, not the tool" concern)?

## Alternatives considered

- **Leave it entirely to tools.** Simplest, and consistent with "governs the
  action, not the tool" — but then policy can't express "be more careful with
  destructive writes," which is a real operator need.
- **`risk_level` only.** Already exists, but it's a single self-declared scalar,
  not tied to effect or resource.
- **A separate "safety" layer outside Aegize.** Possible, but fragments the trust
  boundary that Aegize exists to consolidate.

## Backwards compatibility

Additive. Effect/blast-radius and safety metadata are optional; an action without
them behaves exactly as today. No change to the existing `allow` / `deny` /
`require_approval` flow or the public API is required.

## Future work

- Integration with the capability model (RFC 0006) — blast radius as a constraint
  dimension.
- Interaction with staged rollout / rollback at the policy level (RFC 0008).
- Approval flows specialized for destructive actions (RFC 0004).
