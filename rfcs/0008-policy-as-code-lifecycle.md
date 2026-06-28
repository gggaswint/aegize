# RFC 0008: Policy-as-Code Lifecycle

- Status: Draft
- Date: 2026-06-28
- Origin: community architecture feedback (2026-06)
- Related: [RFC 0002 (Policy Engine)](./0002-policy-engine.md), [RFC 0006 (Resource-Scoped Permissions)](./0006-resource-scoped-permissions.md), [questions.md](../docs/questions.md) ("Should policies remain YAML?")

> Draft for discussion. This RFC captures a direction; it does **not** assume the
> proposal is accepted.

## Summary

Explore the **operational lifecycle** of policy: testing, versioning, review,
staged rollout, and rollback — and the longer question of how far YAML carries
before organizations need full policy-as-code. Where RFC 0006 is about what policy
can *express*, this RFC is about how policy is *managed and shipped safely*.

## Motivation

Once teams rely on Aegize, **untested policy drift becomes its own risk.** A policy
change is a production change to a security-relevant boundary, and it deserves the
same lifecycle as code. Concretely, operators want to assert things like:

- "Agent A can read this table but cannot write it."
- "Agent B can restart this service but cannot touch the auth, db, or backup
  services."

Without tests, those invariants are hope, not guarantees — and they erode silently
as policies grow.

## Current limitations

- Policy is YAML in version control (good: diff-able, reviewable) — but there is
  **no test harness**: no way to assert that a given agent + action yields the
  expected `allow` / `deny` / `require_approval`.
- The planned CLI validator (roadmap v0.3) checks *shape*, not *behavior*.
- Decision records do not surface a **policy version**, so "which policy made this
  call?" can't be reconstructed later (see also RFC 0003).
- There is no notion of staged rollout (beyond planned `dev`/`staging`/`prod`
  overlays) or rollback for policy.

## Proposed direction

Incremental, smallest-useful-thing first:

- **Policy tests (near-term).** A declarative test format — *given* an agent and an
  action, *expect* a decision — plus an `aegize policy test` runner. This pairs
  naturally with the v0.3 schema validator and CLI.
  ```yaml
  # policy_tests.yaml (illustrative)
  - agent: research_bot
    action: { tool: database, operation: write, table: reports }
    expect: deny
  - agent: ops_bot
    action: { tool: shell, operation: execute, target: restart auth-service }
    expect: deny
  ```
- **Policy versioning in decisions.** Surface a policy version/hash on every
  decision record so audits can tie an action to the exact policy that judged it
  (coordinate with RFC 0003).
- **Review + staged rollout (later).** Treat policy changes as reviewable, and
  explore staged rollout and rollback — initially via the planned per-environment
  overlays, later via a remote policy service.
- **Keep YAML; add tooling around it** before reaching for a heavier policy
  language.

## Open questions

- What is the right policy-test format, and how does it stay readable as policies
  grow (and as capabilities from RFC 0006 are added)?
- How should a policy version be referenced in audit records — content hash, a
  declared version field, or both?
- What does "staged rollout" and "rollback" mean for a **local-first SDK** versus a
  future **remote policy service**? Much of the lifecycle only fully exists once
  policy is distributed.
- Where is the line before YAML+tooling should give way to a typed/programmatic
  policy-as-code (the long-term question the community raised)?

## Alternatives considered

- **Schema validation only.** Catches malformed policy, not wrong *behavior*.
  Necessary but not sufficient.
- **Adopt an external engine (OPA/Cedar) for its test tooling.** Inherits a mature
  ecosystem, at the cost of weight and approachability (see RFC 0002).
- **Programmatic policy with host-language unit tests.** Flexible, but policy is no
  longer reviewable as data and is harder to distribute.

## Backwards compatibility

Additive. Tests and policy-version surfacing do not change enforcement; existing
YAML policies run unchanged. A policy with no tests simply has no test coverage.

## Future work

- Policy **registry / distribution** (remote policy service) with review gates and
  rollback automation.
- Tests over **capabilities** (RFC 0006) and over **delegation/attenuation**.
- CI integration so policy changes are tested like code before merge.
