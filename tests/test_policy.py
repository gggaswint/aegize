"""Unit tests for the PermissionPolicy engine."""

from __future__ import annotations

import pytest

from agentguard import Decision, PermissionPolicy, PolicyLoadError, ToolAction
from agentguard.policy import _path_matches

POLICY_YAML = """
agents:
  research_bot:
    allow:
      - tool: web_search
        operations: ["search"]
        risk_level_max: medium
      - tool: file_reader
        operations: ["read"]
        paths:
          - "./safe_data/**"
    require_approval:
      - tool: email
        operations: ["send"]
      - tool: shell
        operations: ["execute"]
    deny:
      - tool: payments
        operations: ["charge"]
      - tool: shell
        operations: ["rm", "delete"]
"""


def _action(tool, operation, *, risk="low", agent_id="research_bot", metadata=None):
    return ToolAction(
        agent_id=agent_id,
        tool_name=tool,
        operation=operation,
        risk_level=risk,
        metadata=metadata or {},
    )


def test_allow_rule_matches(policy):
    result = policy.evaluate(_action("web_search", "search"))
    assert result.decision is Decision.ALLOW


def test_deny_rule_matches(policy):
    result = policy.evaluate(_action("shell", "rm", risk="critical"))
    assert result.decision is Decision.DENY


def test_require_approval_rule_matches(policy):
    result = policy.evaluate(_action("email", "send", risk="high"))
    assert result.decision is Decision.REQUIRE_APPROVAL


def test_no_match_is_default_deny(policy):
    result = policy.evaluate(_action("web_search", "delete_everything"))
    assert result.decision is Decision.DENY


def test_unknown_agent_default_deny(policy):
    result = policy.evaluate(_action("web_search", "search", agent_id="ghost"))
    assert result.decision is Decision.DENY
    assert "unknown agent" in result.reason


def test_risk_level_max_enforced(policy):
    # web_search allows up to medium; high should fall through to deny.
    ok = policy.evaluate(_action("web_search", "search", risk="medium"))
    assert ok.decision is Decision.ALLOW

    too_risky = policy.evaluate(_action("web_search", "search", risk="high"))
    assert too_risky.decision is Decision.DENY


def test_path_allowlist_allows_matching_path(policy):
    result = policy.evaluate(
        _action("file_reader", "read", metadata={"path": "./safe_data/report.txt"})
    )
    assert result.decision is Decision.ALLOW


def test_path_allowlist_denies_outside_path(policy):
    result = policy.evaluate(
        _action("file_reader", "read", metadata={"path": "/etc/passwd"})
    )
    assert result.decision is Decision.DENY


def test_path_allowlist_denies_when_no_path_provided(policy):
    result = policy.evaluate(_action("file_reader", "read"))
    assert result.decision is Decision.DENY


def test_deny_takes_precedence_over_approval_and_allow():
    policy = PermissionPolicy.from_dict(
        {
            "agents": {
                "bot": {
                    "allow": [{"tool": "shell", "operations": ["run"]}],
                    "require_approval": [{"tool": "shell", "operations": ["run"]}],
                    "deny": [{"tool": "shell", "operations": ["run"]}],
                }
            }
        }
    )
    result = policy.evaluate(_action("shell", "run", agent_id="bot"))
    assert result.decision is Decision.DENY


def test_from_yaml_loads(tmp_path):
    path = tmp_path / "policy.yaml"
    path.write_text(POLICY_YAML, encoding="utf-8")
    policy = PermissionPolicy.from_yaml(path)
    assert policy.evaluate(_action("web_search", "search")).decision is Decision.ALLOW


def test_from_yaml_missing_file_raises():
    with pytest.raises(PolicyLoadError):
        PermissionPolicy.from_yaml("/nonexistent/policy.yaml")


def test_from_dict_missing_agents_key_raises():
    with pytest.raises(PolicyLoadError):
        PermissionPolicy.from_dict({"not_agents": {}})


def test_from_yaml_invalid_yaml_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("agents: [unclosed", encoding="utf-8")
    with pytest.raises(PolicyLoadError):
        PermissionPolicy.from_yaml(path)


@pytest.mark.parametrize(
    "path,pattern,expected",
    [
        ("./safe_data/a.txt", "./safe_data/**", True),
        ("safe_data/nested/a.txt", "./safe_data/**", True),
        ("/etc/passwd", "./safe_data/**", False),
        ("../safe_data/a.txt", "./safe_data/**", False),
    ],
)
def test_path_matches(path, pattern, expected):
    assert _path_matches(path, pattern) is expected
