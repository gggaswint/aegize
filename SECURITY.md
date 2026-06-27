# Security Policy

AgentGuard is a policy and audit layer used to constrain what AI agents can do.
A vulnerability in it can translate directly into an agent doing something it
should not. We take that seriously and appreciate reports from the community.

## Supported versions

AgentGuard is pre-1.0 and under active development. Security fixes are applied to
the latest released version on the `main` branch. Please make sure you can
reproduce an issue against the latest version before reporting.

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a vulnerability

**Please report suspected vulnerabilities privately. Do not open a public
GitHub issue, pull request, or discussion for a security problem.**

Use either of these channels:

- **GitHub Security Advisories** (preferred): open a private report via the
  repository's **Security → Report a vulnerability** tab. This keeps the
  discussion private until a fix is ready.
- **Email:** ggaswint@gmail.com with the subject line `AgentGuard security`.

To help us triage quickly, please include:

- A description of the issue and its impact (what can an attacker or a
  misbehaving agent achieve?).
- A minimal reproduction: the relevant policy, the tool call, and the observed
  behavior.
- The AgentGuard version and Python version.
- Any suggested remediation, if you have one.

## What to expect

- **Acknowledgment** within 3 business days.
- **An initial assessment** (severity and whether we can reproduce it) within 7
  business days.
- **Coordinated disclosure.** We'll work with you on a fix and a disclosure
  timeline. We aim to release a fix promptly and will credit you in the release
  notes unless you prefer to remain anonymous.

Please give us a reasonable opportunity to address the issue before any public
disclosure.

## Scope

Examples of issues we consider security-relevant:

- A policy decision that returns `allow` (or executes the wrapped function) when
  it should `deny` or `require_approval`.
- A denied or approval-gated action that executes the underlying function anyway.
- An attempted action that is not written to the audit log.
- A way to bypass policy evaluation entirely (e.g. via crafted arguments,
  metadata, or path patterns).
- Policy-loading behavior that could be exploited (e.g. unsafe deserialization).

Out of scope:

- Vulnerabilities in your own tool implementations or in how you write your
  policy. AgentGuard enforces the policy you give it; it cannot make an
  intentionally permissive policy safe.
- Issues requiring a trusted operator to deliberately misconfigure the system.

Thank you for helping keep AgentGuard and its users safe.
