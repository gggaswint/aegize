# Changelog

All notable changes to Aegize are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-06-29

### Added

- **`aegize` command-line interface** with its first subcommand,
  `aegize policy test <policy_file> <test_file>`. It evaluates declarative test
  cases against a policy and reports pass/fail, exiting `0` when every case
  passes, `1` on any mismatch, and `2` on a missing or malformed file. It only
  runs policy evaluation — it never executes a tool — and is built on the stdlib
  (argparse) to keep the package dependency-light. This is the first step of the
  policy-as-code lifecycle ([RFC 0008](./rfcs/0008-policy-as-code-lifecycle.md)).
- `examples/policy_tests.yaml` — runnable policy tests for `examples/aegize.yaml`.
- "Policy tests" section in the README.

### Notes

- No changes to the existing public Python API; the CLI is additive and reachable
  via the new `aegize` console script.

## [0.2.0] - 2026-06-27

### Added

- `@guarded_tool` decorator, `GuardContext`, and the `guard()` adapter for
  signature-preserving integration with tool registries and MCP.
- Per-call metadata (e.g. `path`) for allowlist matching.

## [0.1.0]

### Added

- Initial SDK: `AgentIdentity`, `ToolAction`, `PermissionPolicy`, `GuardedTool`,
  and `AuditLog`.
- Default-deny policy engine (`deny → require_approval → allow → default-deny`),
  `risk_level_max` ceilings, glob path allowlists, and append-only JSONL audit.

[0.3.0]: https://github.com/gggaswint/aegize/releases/tag/v0.3.0
[0.2.0]: https://github.com/gggaswint/aegize/releases/tag/v0.2.0
[0.1.0]: https://github.com/gggaswint/aegize/releases/tag/v0.1.0
