# Contributing to AgentGuard

Thanks for your interest in improving AgentGuard. It's a small, focused
project and we'd like to keep it that way: a clean policy and audit layer that
teams can read in an afternoon and trust in production.

## Project scope and principles

AgentGuard deliberately stays small. Before proposing a change, it helps to know
what we optimize for:

- **Default deny, always.** Anything not explicitly allowed is denied. Changes
  must not weaken this.
- **Minimal dependencies.** The runtime depends on PyYAML and nothing else.
  New runtime dependencies are a hard sell.
- **Readable over clever.** This is security-adjacent code. Clarity wins.
- **Easy to extend, slow to expand.** We'd rather ship a clean extension point
  than a built-in for every use case. A web dashboard, external services, and
  framework-specific magic are intentionally out of scope for now.

If you're planning something larger than a bug fix or small improvement, please
open an issue first so we can agree on the approach before you write code.

## Development setup

```bash
git clone https://github.com/gggaswint/agentguard
cd agentguard
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Before you open a pull request

Run the same checks CI runs, and make sure they're green:

```bash
ruff check .     # lint + import order
pytest           # full test suite
```

A change is ready to review when:

1. **Tests pass and lint is clean.** No exceptions.
2. **New behavior has tests.** Bug fixes include a regression test; features
   include tests for the allow / deny / approval paths they touch.
3. **Security posture is preserved.** Denied and approval-gated actions must
   never execute the wrapped function, and every attempt must be audited. If a
   change touches enforcement, call that out explicitly in the PR description.
4. **Public API changes are intentional.** If you add or change something in
   `agentguard/__init__.py`, update the README and note it in the PR.
5. **Type hints are present** on new public functions and classes.

## Commit and PR style

- Keep commits focused; a small, well-described PR is easier to merge than a
  large one.
- Describe the *why*, not just the *what*. For enforcement changes, describe the
  threat model or behavior you're protecting.

## Reporting bugs

Open an issue with a minimal reproduction: the policy YAML (or dict), the tool
call, what you expected, and what happened. For anything that looks like a
security vulnerability, do **not** open a public issue — follow
[SECURITY.md](./SECURITY.md) instead.

## License

By contributing, you agree that your contributions are licensed under the
project's [MIT License](./LICENSE).
