# RFC 0005: Runtime Governance

- Status: Draft
- Date: 2026-06-27
- Related: [vision.md](../docs/vision.md), [principles.md](../docs/principles.md), [architecture.md](../docs/architecture.md), RFCs [0001](./0001-agent-identity.md)–[0004](./0004-approval-workflow.md)

## Summary

Define runtime governance as the umbrella concept that the other RFCs compose
into: the ordered pipeline every AI action passes through — identity → policy →
permissions → approval → execution → audit → observability → tools — and the
guarantees that pipeline upholds. This RFC names the contract, ratifies the
enforcement point, and scopes the path from a local SDK pipeline to networked,
multi-agent, organization-level governance.

## Motivation

Aegize's thesis is that *every meaningful AI action should pass through trusted
runtime infrastructure before reaching the outside world.* Identity, policy,
approval, and audit are the parts; runtime governance is the whole — the ordered,
deterministic pipeline and the invariants it guarantees. Naming it explicitly
gives the other RFCs a frame, defines the contract integrations must satisfy, and
sets the direction for governing actions beyond a single process (remote,
multi-agent, org-wide) without losing the local-first guarantees.

## Goals

- Define the governance pipeline as an ordered sequence of stages with a clear
  contract per stage.
- Ratify the enforcement point and the core invariants as guarantees, not
  incidental behavior.
- Provide a frame that composes RFCs 0001–0004 and the future observability stage.
- Keep the model coherent from the local SDK up to networked/multi-agent
  governance.

## Non-goals

- Re-specifying identity, policy, audit, or approval in detail (their own RFCs).
- Building the remote governance service or hosted dashboard (future direction).
- Defining multi-agent attribution mechanics (named as an open question here).

## Proposed design

- **The pipeline.** A governed action flows through ordered stages:
  `Identity → Policy Evaluation → Permission Check → Approval → Execution →
  Audit → Observability → Tools`. Each stage has a narrow contract; stages are
  composable and individually testable.
- **The enforcement point.** A single boundary (`GuardedTool`) runs the pipeline
  for a call: it builds the `ToolAction`, evaluates policy, audits the decision
  *before* execution, gates or denies, executes only if allowed, then audits the
  outcome. Governance lives in code that runs regardless of model output
  (principle: runtime first).
- **Invariants (guarantees).** Default deny; deny wins; gated and denied actions
  never execute; audit-first then outcome-appended; unknown agent/tool denies.
  These hold at every stage boundary and are not weakened without a recorded
  decision.
- **Observability stage.** Promote observability from an implicit byproduct of
  audit to a defined stage: a read model over governed actions (live and
  historical) that does not alter the control flow.
- **Composition.** RFC 0001 defines stage 1, RFC 0002 stages 2–3, RFC 0004 stage
  4, RFC 0003 stage 6; this RFC defines their ordering, the enforcement point, and
  the shared invariants.

## Current implementation

`GuardedTool` is the enforcement point and already runs the core pipeline:
identity (via `AgentIdentity` on the `ToolAction`), policy+permission evaluation
(`PermissionPolicy.evaluate`), audit-first recording, the approval/deny gate
(`ApprovalRequired` / `PolicyDenied`), execution of the wrapped function only when
allowed, and outcome auditing. `GuardContext` bundles agent, policy, and audit log;
`@guarded_tool` and `guard()` provide the ergonomic surface. The approval
*workflow* and a distinct *observability* surface are not yet built; everything
else in the pipeline exists and is tested.

## Future direction

- **Remote governance** — run the pipeline as (or behind) a service so actions can
  be governed across processes, with policy and audit centralized.
- **Multi-agent governance** — govern and attribute actions across agents acting
  on behalf of other agents or users.
- **Organization-level policy** — shared policy and inheritance across teams and
  environments.
- **Observability surface** — live and historical views over governed actions
  (later: a hosted dashboard).
- **Protocol** — standardize the action/decision/audit contract so the pipeline is
  an interoperable layer, not a single implementation.

## Open questions

- What parts of the pipeline should be standardized as an open protocol vs. remain
  implementation detail?
- How should multi-agent governance attribute actions and bound the authority of a
  chain of agents?
- Where is the right boundary for a remote/sidecar governance model without
  sacrificing the local-first guarantees?
- How are the invariants preserved when stages run across process or network
  boundaries?

## Alternatives considered

- **Per-integration, ad hoc enforcement.** Each framework wires its own checks.
  Rejected — inconsistent, unauditable, and not a layer; defeats the thesis.
- **Sidecar/proxy that intercepts tool traffic.** Attractive for language- and
  framework-neutral enforcement and worth exploring as a *deployment* of the
  pipeline, but it does not replace the in-process SDK and raises its own trust
  and coverage questions. Noted as future direction, not the core model.
- **Prompt/model-level governance only.** Rejected — advisory, non-deterministic,
  and unenforceable; contradicts runtime-first.
