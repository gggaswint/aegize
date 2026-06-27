# RFC 0001: Agent Identity

- Status: Draft
- Date: 2026-06-27
- Related: [questions.md](../docs/questions.md) (identity), [architecture.md](../docs/architecture.md), [decisions.md](../docs/decisions.md)

## Summary

Define what an agent identity *is* in Aegize: what it represents, what it binds,
and how it is presented and (eventually) verified. Identity is the first stage of
the runtime flow and the key that policy is written against and audit is
attributed to. This RFC proposes keeping today's declared identity as the
foundation and giving it a clear conceptual definition and a path toward
verifiable, signed identity — without coupling the core to any provider.

## Motivation

Every governed action begins with "who is acting?" Policy keys on it, audit
attributes to it, and future multi-agent governance depends on it. Today identity
is a self-declared `agent_id` plus owner, environment, and metadata. That is
enough for in-process trust but leaves real questions unanswered: is identity an
instance or a class of agents? How much of an agent's configuration is part of
its identity? Can a consumer *verify* the claim, or only trust it? Settling the
concept now prevents churn in policy and audit later.

## Goals

- A precise, documented definition of what `AgentIdentity` represents.
- A stable identity key that policy and audit can rely on across versions.
- A design that allows verifiable (signed) identity later without breaking the
  declared-identity path.
- Vendor-neutral: no dependency on any model provider's identity system.

## Non-goals

- Building issuance, PKI, or a credential service in this RFC.
- Authenticating identity over a network (a future networked deployment concern).
- Defining permission inheritance or delegation (see RFC 0004 and the multi-agent
  question; identity is the prerequisite, not the mechanism).

## Proposed design

Treat identity as a small, stable **claim** about the actor, separate from the
mechanism that authenticates it:

- An identity is the tuple `(agent_id, owner, environment)` plus open `metadata`.
  `agent_id` is the stable, human-assigned key; it identifies a *logical agent*
  (a deployed role), not a single process instance. Instance/run information lives
  in `metadata` or on the `ToolAction`, not in the identity key.
- Identity is **declared** by default and trusted at the host boundary (consistent
  with the current threat model). Verification is layered on top, not required.
- Reserve room for an optional **verifiable identity**: a signed credential that
  carries the same logical `agent_id` and can be checked by a policy or audit
  consumer. The declared form is the always-available baseline; the signed form is
  an enhancement that does not change how policy is authored.

This keeps policy authoring stable (rules key on `agent_id`) while allowing trust
in the claim to increase over time.

## Current implementation

`AgentIdentity` is a dataclass with `agent_id`, `name`, `owner`, `environment`
(`dev`/`staging`/`prod`), `created_at`, and a free-form `metadata` dict. It is
attached to every `ToolAction` and written into every audit record. Identity is
self-declared and trusted within the host process; there is no signing or
external verification today. This is sufficient for the local-first SDK and
matches the documented trust assumptions.

## Future direction

- **Signed agent identity** — a verifiable credential binding `agent_id` (and
  optionally a configuration fingerprint) to a key, checkable offline.
- **Authentication** — when identity crosses a process or network boundary
  (remote policy/audit), define how the claim is authenticated (tokens, mTLS,
  workload identity).
- **Configuration binding** — optionally bind parts of an agent's setup (model,
  toolset, version) into identity or attach them as verifiable attributes.
- Consider adopting an existing standard (e.g. a SPIFFE/OIDC-style workload
  identity) rather than inventing one.

## Open questions

- Is identity ultimately a class (a role/config) or an instance (a run)? Where is
  the line drawn between identity and per-action context?
- Should identity become cryptographic, and if so, who issues credentials and what
  are the trust roots, rotation, and revocation stories?
- How should an agent authenticate its identity to a remote Aegize component?
- How much agent configuration belongs *in* identity vs. *attached to* it?

## Alternatives considered

- **Anonymous / no identity.** Govern by tool only. Rejected: breaks attribution
  and per-agent policy, which are core.
- **Per-call ephemeral tokens as identity.** Rejected: conflates authentication
  with identity and makes policy authoring unstable.
- **Adopt a full external identity system now (OIDC/SPIFFE).** Deferred: too heavy
  for the local-first core; revisit when networked deployment is real. The design
  above leaves room to adopt one later.
