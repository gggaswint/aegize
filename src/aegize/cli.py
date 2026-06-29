"""Aegize command-line interface.

Currently exposes one command:

    aegize policy test <policy_file> <test_file>

It evaluates declarative test cases against a policy and reports pass/fail. It
only runs policy evaluation — it never executes any tool. Built on the stdlib
(argparse) to stay dependency-light.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from .action import RISK_LEVELS, ToolAction
from .exceptions import AegizeError, PolicyLoadError
from .policy import PermissionPolicy

EXPECTED_DECISIONS = ("allow", "deny", "require_approval")


class PolicyTestError(AegizeError):
    """Raised when a policy test file is missing, unparseable, or malformed."""


def _load_test_cases(path: Path) -> list[dict[str, Any]]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise PolicyTestError("PyYAML is required to load policy tests") from exc

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolicyTestError(f"could not read test file: {path}") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise PolicyTestError(f"could not parse test YAML: {path}") from exc

    if not isinstance(data, dict) or "tests" not in data:
        raise PolicyTestError(
            f"test file must have a top-level 'tests' list: {path}"
        )
    cases = data["tests"]
    if not isinstance(cases, list) or not cases:
        raise PolicyTestError("'tests' must be a non-empty list")
    return cases


def _case_to_action(case: dict[str, Any], index: int) -> tuple[str, str, ToolAction]:
    """Validate one test case and turn it into (label, expected, ToolAction)."""
    if not isinstance(case, dict):
        raise PolicyTestError(f"test #{index + 1} must be a mapping")

    label = str(case.get("name") or f"test #{index + 1}")

    for field in ("agent", "tool", "operation", "expect"):
        if field not in case:
            raise PolicyTestError(f"{label}: missing required field '{field}'")

    expected = case["expect"]
    if expected not in EXPECTED_DECISIONS:
        raise PolicyTestError(
            f"{label}: 'expect' must be one of {list(EXPECTED_DECISIONS)}, got {expected!r}"
        )

    risk_level = case.get("risk_level", "low")
    if risk_level not in RISK_LEVELS:
        raise PolicyTestError(
            f"{label}: invalid risk_level {risk_level!r} (one of {list(RISK_LEVELS)})"
        )

    metadata = case.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise PolicyTestError(f"{label}: 'metadata' must be a mapping")

    action = ToolAction(
        agent_id=str(case["agent"]),
        tool_name=str(case["tool"]),
        operation=str(case["operation"]),
        risk_level=str(risk_level),
        metadata=dict(metadata),
    )
    return label, str(expected), action


def run_policy_test(policy_file: str, test_file: str, out=None) -> int:
    """Evaluate test cases against a policy. Returns an exit code.

    0 = all passed; 1 = one or more failed. Raises ``PolicyLoadError`` or
    ``PolicyTestError`` for invalid inputs (the caller maps these to exit code 2).
    """
    if out is None:
        out = sys.stdout
    policy = PermissionPolicy.from_yaml(policy_file)
    cases = _load_test_cases(Path(test_file))

    passed = 0
    failed = 0
    for index, case in enumerate(cases):
        label, expected, action = _case_to_action(case, index)
        result = policy.evaluate(action)
        actual = result.decision.value
        if actual == expected:
            passed += 1
            print(f"PASS  {label}  (expected {expected})", file=out)
        else:
            failed += 1
            print(
                f"FAIL  {label}  (expected {expected}, got {actual} — {result.reason})",
                file=out,
            )

    print(file=out)
    print(f"{passed} passed, {failed} failed", file=out)
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aegize",
        description="Aegize — runtime governance for autonomous AI agents.",
    )
    sub = parser.add_subparsers(dest="command")

    policy_parser = sub.add_parser("policy", help="work with Aegize policies")
    policy_sub = policy_parser.add_subparsers(dest="policy_command")

    test_parser = policy_sub.add_parser(
        "test", help="evaluate policy test cases against a policy file"
    )
    test_parser.add_argument("policy_file", help="path to an Aegize policy YAML file")
    test_parser.add_argument("test_file", help="path to a policy test YAML file")

    args = parser.parse_args(argv)

    if args.command == "policy" and args.policy_command == "test":
        try:
            return run_policy_test(args.policy_file, args.test_file)
        except (PolicyLoadError, PolicyTestError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
