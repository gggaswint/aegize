# RFC 0002: Policy Engine

- Status: Draft
- Date: 2026-06-27
- Related: [questions.md](../docs/questions.md) (policy, capabilities), [architecture.md](../docs/architecture.md), [decisions.md](../docs/decisions.md) (009 default-deny)

## Summary

Define the policy engine: how policy is authored, how it is evaluated, and what
guarantees it provides. This RFC ratifies the current default-deny, ordered
evaluation model and YAML authoring format, and proposes the next steps —
schema validation and a CLI validator — while scoping the longer question of a
richer capability model and remote policy distribution.

## Motivation

Policy is where an operator declares what each agent may do. It must be readable,
reviewable, deterministic, and safe by default. The current model delivers this
for simple cases, but it has no formal schema (typos fail silently or
surprisingly), and its expressiveness — (tool, operation) pairs with risk and
path constraints — may not scale to finer-grained needs. We want to lock in the
guarantees, harden the authoring experience, and chart the path to a more
expressive model without breaking the simple case.

## Goals

- Ratify and document the default-deny, ordered evaluation model as a guarantee.
- Make policy authoring safe: a schema and a validator that catch errors before
  runtime.
- Keep YAML as the default, version-controllable authoring format.
- Preserve determinism: the same action and policy always yield the same decision.

## Non-goals

- Replacing YAML with a new policy language in this RFC.
- Building the remote policy service (future; this RFC keeps policy local).
- Defining the approval *workflow* (RFC 0004) or the audit format (RFC 0003).

## Proposed design

Three layers, smallest first:

1. **Ratified evaluation model.** Per-agent rules in three lists — `deny`,
   `require_approval`, `allow` — evaluated in that order, then default-deny.
   Explicit deny wins; unknown agent/tool denies. Allow rules may constrain
   `risk_level_max` and `paths` (glob allowlists). This is a stable contract.
2. **Schema + validation.** A documented schema for policy files and a validator
   that reports precise, friendly errors (unknown keys, invalid risk levels,
   malformed globs, shadowed rules). Surfaced as an `aegize` CLI command
   (`aegize policy validate`) and usable programmatically.
3. **Capability direction (scoped, not built here).** Investigate whether the
   permission unit should evolve from (tool, operation) toward composable
   *capabilities* (e.g. "read files under `./data`", "email internal domains").
   Any such change must keep the simple case simple and remain default-deny.

## Current implementation

`PermissionPolicy` loads per-agent YAML via `from_yaml` / `from_dict` and
exposes `evaluate(action) -> PolicyResult` with a `Decision` of `allow`, `deny`,
or `require_approval`. Evaluation is the ordered model above. Allow rules support
`operations`, `risk_level_max`, and `paths` constraints; path matching uses glob
allowlists against call inputs and metadata. There is no formal schema validation
yet — malformed policy is caught only as far as YAML parsing and rule shape allow.
PyYAML is the only runtime dependency.

## Future direction

- **CLI validator** and schema, with helpful diagnostics.
- **Per-environment overlays** (`dev`/`staging`/`prod`) composed deterministically.
- **Capability model** if the (tool, operation) unit proves too coarse.
- **Remote policy service** — centralized, versioned distribution and
  organization-level policy with inheritance, layered on top of the local engine.

## Open questions

- Should policies remain YAML, gain a typed/programmatic option, or both?
- What is the smallest capability model that is expressive enough without becoming
  a general policy language?
- How should organization-level and per-environment policies compose, and what is
  the precedence model?
- Should we adopt an existing policy engine (see alternatives) or keep a purpose-
  built one?

## Alternatives considered

- **Adopt OPA/Rego or Cedar.** Powerful and standard, but heavy for the
  local-first, dependency-light core and less approachable than YAML for the
  common case. Deferred; revisit if expressiveness demands it.
- **Programmatic-only policy (Python).** Maximally flexible but not reviewable as
  data and harder to distribute. Rejected as the default; may be offered as an
  advanced escape hatch.
- **Allow-by-default with denylist.** Rejected outright — violates default-deny
  (decision 009), the project's most important invariant.
