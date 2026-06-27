# RFC 0003: Audit Format

- Status: Draft
- Date: 2026-06-27
- Related: [questions.md](../docs/questions.md) (audit), [architecture.md](../docs/architecture.md), [decisions.md](../docs/decisions.md) (010 audit everything)

## Summary

Define the audit record: its event types, its field schema, and how it evolves.
This RFC stabilizes the current append-only JSONL format as a versioned schema,
defines pluggable sinks, and scopes the path to tamper-evidence — so the audit
log can serve as trustworthy evidence of what an agent attempted and what
happened.

## Motivation

Audit is part of the control loop, not a side effect (decision 010). "What did
this agent try to do, and what happened?" must always have a precise answer,
including blocked and gated attempts. For the log to be useful downstream and
trustworthy as evidence, its shape needs to be stable and versioned, it needs to
be shippable to systems beyond a local file, and — eventually — it needs to be
tamper-evident. None of these should compromise the simple, greppable JSONL that
makes the format pleasant today.

## Goals

- A documented, versioned schema for audit records.
- A fixed, named set of event types covering the full lifecycle of an attempt.
- A pluggable sink interface so records can go beyond a local JSONL file.
- A clear path to tamper-evidence that respects the dependency-light principle.

## Non-goals

- Building the hosted dashboard or query layer (future; this RFC is the format).
- Defining policy (RFC 0002) or the approval workflow (RFC 0004).
- Mandating a specific external standard (considered, not required).

## Proposed design

- **Event lifecycle.** A fixed vocabulary: `allowed`, `denied`,
  `approval_required` (the decision, written before execution), then
  `execution_succeeded` or `execution_failed` (the outcome, appended after). An
  allowed action produces two records; a denied or gated action produces one.
- **Versioned schema.** Each record carries a schema version and the core fields:
  timestamp, event, action id, agent id, tool, operation, risk level, input
  summary, decision reason, and call-time metadata. Additive changes bump a minor
  version; consumers ignore unknown fields.
- **Audit-first ordering** is part of the contract: the decision record is
  written before execution is attempted; the outcome is appended after.
- **Pluggable sinks.** A small writer interface so records can be emitted to
  stdout, syslog, object storage, or a SIEM, in addition to local JSONL. The
  default stays local-first.
- **Redaction hook.** Because inputs may contain sensitive data, define where
  callers can summarize/redact before a record is written (the input summary is
  already a summary, not the raw payload).

## Current implementation

`AuditLog` writes append-only JSONL — one self-contained JSON object per line. It
records the five lifecycle events above, with the decision written before
execution and the outcome appended after. Each record carries identity, tool,
operation, risk level, input summary, the decision reason, and call-time
metadata. Integrity is host-level (file permissions); there is no signing or
chaining yet. The format is intentionally trivial to tail, grep, or ship.

## Future direction

- **Tamper-evident logs** — hash-chaining and/or signing so records cannot be
  altered or dropped without detection, with an offline verification path.
- **Distributed sinks** — first-class adapters for syslog, object storage, and
  SIEM, with batching/backpressure.
- **Structured query** — local inspection tooling, and later a hosted surface.
- Optional alignment with a wire standard (e.g. OpenTelemetry logs / CloudEvents)
  for interoperability, without making the local format depend on it.

## Open questions

- What tamper-evidence scheme best balances integrity, performance, and the
  dependency-light constraint (hash chain vs. signatures vs. external anchor)?
- How is the chain verified, and by whom — is verification a CLI, a library, or a
  service concern?
- How should schema versioning and forward/backward compatibility be guaranteed?
- How much should the format align with an existing standard vs. stay purpose-
  built and minimal?

## Alternatives considered

- **OpenTelemetry logs / CloudEvents as the native format.** Strong
  interoperability, but heavier and less greppable than line-delimited JSON for
  the local-first default. Better as an optional export target than the core
  format.
- **Database-backed audit.** Queryable, but adds a dependency and a service to the
  core and undercuts local-first. Deferred to a sink/future-platform concern.
- **Log only successful/denied actions.** Rejected — hides exactly the attempts
  that matter most (gated and failed). Audit-everything is a decision (010).
