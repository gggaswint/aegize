# Open Questions

A living list of unresolved product and architecture questions. The goal is to
make our uncertainty explicit so it can be discussed, prototyped, and eventually
resolved — ideally through an [RFC](../rfcs/README.md) and recorded in
[decisions.md](./decisions.md).

These are open on purpose. Where we have a leaning, it is noted as *current
thinking*, not a commitment. Nothing here is settled until it moves to a decision.

---

## Identity

### What is an AI identity?

What, precisely, does an `AgentIdentity` represent? A process? A deployed agent
config? A (model, system-prompt, toolset) tuple? An instance vs. a class of
agents? The answer shapes how policy is written, how audit attributes actions,
and how identity composes in multi-agent systems.

*Current thinking:* today identity is a declared `agent_id` plus owner,
environment, and metadata — a stable, human-assigned handle. The open question is
how much of an agent's actual configuration should be bound into its identity.

### Should identity be cryptographic?

Should an agent's identity be a verifiable, signed credential rather than a
self-declared string? Cryptographic identity would let a policy or audit consumer
*verify* who acted, not just trust the claim. What is the key model, who issues
credentials, and what is the rotation/revocation story?

*Current thinking:* signed identity is on the long-term roadmap; the open
questions are issuance, trust roots, and whether to adopt an existing standard
rather than invent one.

### How should agents authenticate?

When an agent presents an identity to Aegize (or to a future remote policy
service), how is that claim authenticated? In-process trust is sufficient today,
but a networked deployment needs an answer: tokens, mTLS, signed assertions,
workload identity?

---

## Permissions & policy

### How do agents inherit permissions?

When an agent spawns or delegates to a sub-agent, or acts on behalf of a user,
how do permissions flow? Is it strict attenuation (a child can never exceed its
parent)? Role-based? Does the acting-on-behalf-of principal's scope bound the
agent's? Inheritance is central to multi-agent governance and is currently
undefined.

### What is a capability?

Is the right unit of permission a (tool, operation) pair (today's model), or a
finer-grained, composable *capability* (e.g. "read files under ./data",
"send email to internal domains")? A capability model could be more expressive
and more portable, but also more complex. What is the smallest model that is
expressive enough?

### Should policies remain YAML?

YAML is readable, diff-able, and lives in version control — good properties for
policy. But it lacks types, composition, and validation guarantees, and it can
get unwieldy at scale. Do we keep YAML as the authoring format and add schema +
validation, introduce a typed policy language, or support a programmatic API?

*Current thinking:* keep YAML as the default authoring format and invest in a
schema validator / linter before considering anything heavier.

---

## Approval

### How should approval delegation work?

`require_approval` is a decision today, but a real approval *workflow* raises
questions: who can approve what, how is approval authority delegated, how is an
approved action re-issued safely, how do approvals expire, and how do we prevent
an agent from approving its own actions? What is the trust model for the approver?

---

## Audit

### How should audit logs become tamper-evident?

The audit log is append-only JSONL with host-level integrity today. To be
trustworthy as evidence it should be tamper-evident: hash-chaining, signing, or
an external anchor. What scheme balances integrity, performance, and the
local-first, dependency-light principle? How is the chain verified, and by whom?

---

## Protocol & ecosystem

### What should be standardized as protocol?

If "every meaningful AI action passes through trusted runtime infrastructure" is
to become a norm, parts of it likely need to be an open protocol rather than one
implementation. What is the right surface to standardize — the action/decision
schema, the audit record format, the identity credential, the policy interface —
and what should stay implementation detail?

### How should multi-agent governance work?

When agents act on behalf of other agents, coordinate, or form chains, how is the
whole interaction governed and audited? How do we attribute an action to the
right principal, bound the authority of a chain, and reconstruct "who caused
what" across agents? This is the hardest open area and the most important for the
long-term thesis.

---

## How to use this document

- Add a question when you hit a real fork that we cannot yet answer.
- When a question gets serious enough to act on, open an [RFC](../rfcs/README.md).
- When it is resolved, record it in [decisions.md](./decisions.md) and remove it
  here (or link the decision).
