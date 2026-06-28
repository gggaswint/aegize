# RFC 0006: Resource-Scoped Permissions (Capability Model)

- Status: Draft
- Date: 2026-06-28
- Origin: community architecture feedback (2026-06)
- Related: [RFC 0002 (Policy Engine)](./0002-policy-engine.md), [questions.md](../docs/questions.md) ("What is a capability?"), [RFC 0001 (Agent Identity)](./0001-agent-identity.md)

> Draft for discussion. This RFC captures a direction; it does **not** assume the
> proposal is accepted.

## Summary

Explore moving the unit of permission from a `(tool, operation)` pair toward a
**resource-scoped capability**: a permission that also constrains *which*
resources and *which* argument values an action may touch. The question is not
only "can this agent call `send_email`?" but "to whom, with what attachment,
using which account, in which workspace?" — and the equivalent for shell,
databases, cloud APIs, and payments.

## Motivation

Tool names are coarse. In real deployments, the meaningful boundary is at the
*resource*, not the tool:

- `send_email` → which recipients/domains, which sending account, what attachment.
- `shell` → which commands, which paths, which hosts.
- `database` → which tables, read vs write, which schema.
- `cloud` → which services, which projects/regions.
- `payments` → which account, what amount ceiling, which counterparties.

A policy that says "agent may call `database.write`" is far too broad to be a
trust boundary. Governance that developers can rely on needs to express limits at
the granularity that actually bounds blast radius.

## Current limitations

Today `PermissionPolicy` matches on `tool` + `operation`, with two early forms of
scoping already present:

- `risk_level_max` — a coarse risk ceiling on an allow rule.
- `paths` — a glob allowlist matched against string arguments / `metadata["path"]`.

`paths` is, in effect, a single hard-coded resource constraint (filesystem). There
is no general mechanism to constrain arbitrary arguments or resources — recipients,
accounts, tables, services, amounts — and no defined way to normalize a tool's
arguments before matching.

## Proposed direction

Treat a capability as `(tool, operation, constraints)`, where `constraints` are
declarative predicates over **normalized** action arguments and resources. Sketch:

```yaml
allow:
  - tool: email
    operations: ["send"]
    constraints:
      to_domain: ["acme.com"]        # recipient domain allowlist
      account: ["support@acme.com"]  # which sending identity
  - tool: database
    operations: ["read"]
    constraints:
      table: ["public.reports/**"]   # resource glob
  - tool: payments
    operations: ["charge"]
    constraints:
      amount_max: 100                # ceiling
```

Principles to preserve:

- **Default deny** — a capability matches only if tool, operation, *and* all
  constraints are satisfied; otherwise the action falls through to deny.
- **YAML authoring** — constraints stay declarative and reviewable (see RFC 0002).
- **Normalization first** — constraints match against a normalized view of the
  action's arguments, so policy is not coupled to each tool's call signature.
  `paths` and `risk_level_max` become special cases of the constraint vocabulary.
- **Small core vocabulary + extension** — a minimal built-in set (glob, allowlist,
  numeric ceiling, domain) plus a hook for tool-specific constraints.

## Open questions

- What is the smallest constraint vocabulary that is expressive enough without
  becoming a general policy language (the "simple beats clever" tension)?
- How are tool-specific arguments **normalized** into a stable shape policy can
  match, without Aegize needing to understand every tool?
- How do constraints compose with `risk_level_max`, `paths`, and `deny` rules?
- What is the performance and authoring cost at scale?
- How do capabilities **attenuate** under delegation (a sub-agent should not gain
  scope its parent lacks — see [RFC 0001](./0001-agent-identity.md) and the
  multi-agent question)?

## Alternatives considered

- **Keep `(tool, operation)` + per-tool custom validators in host code.** Simple,
  but pushes the trust boundary back into imperative code that isn't reviewable as
  data — against the declarative-policy principle.
- **Adopt OPA/Rego or Cedar.** Expressive and standard, but heavy for the
  local-first, dependency-light core, and less approachable than YAML for the
  common case (already weighed in RFC 0002).
- **Argument allowlists only (no resource model).** Cheaper, but doesn't capture
  resource identity (account, workspace, table) cleanly.

## Backwards compatibility

Must be **additive**. Existing `(tool, operation)` rules — and `risk_level_max` /
`paths` — keep working unchanged; a rule with no `constraints` behaves exactly as
today. No breaking change to the public API is required if constraints are an
optional extension of the rule schema. Argument normalization must default to a
pass-through that preserves current `paths` behavior.

## Future work

- Constraints as a dimension of **blast radius** (see [RFC 0007](./0007-mutating-action-safety.md)).
- Capability **attenuation/inheritance** under delegation and multi-agent chains.
- Standardizing the constraint schema as part of a portable policy/protocol surface.
- Policy **tests** that assert capability behavior (see [RFC 0008](./0008-policy-as-code-lifecycle.md)).
