"""Shared fixtures for the AgentGuard test suite."""

from __future__ import annotations

import pytest

from agentguard import AgentIdentity, AuditLog, PermissionPolicy

POLICY_DICT = {
    "agents": {
        "research_bot": {
            "allow": [
                {"tool": "web_search", "operations": ["search"], "risk_level_max": "medium"},
                {"tool": "file_reader", "operations": ["read"], "paths": ["./safe_data/**"]},
            ],
            "require_approval": [
                {"tool": "email", "operations": ["send"]},
                {"tool": "shell", "operations": ["execute"]},
            ],
            "deny": [
                {"tool": "payments", "operations": ["charge"]},
                {"tool": "shell", "operations": ["rm", "delete"]},
            ],
        }
    }
}

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


@pytest.fixture
def agent() -> AgentIdentity:
    return AgentIdentity(
        agent_id="research_bot",
        name="Research Bot",
        owner="Geoffrey",
        environment="dev",
    )


@pytest.fixture
def policy() -> PermissionPolicy:
    return PermissionPolicy.from_dict(POLICY_DICT)


@pytest.fixture
def audit(tmp_path) -> AuditLog:
    return AuditLog(tmp_path / "audit.jsonl")
