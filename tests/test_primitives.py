"""Tests for the AgentIdentity / ToolAction / AuditLog primitives."""

from __future__ import annotations

import pytest

from agentguard import AgentIdentity, AuditLog, ToolAction


def test_agent_identity_defaults():
    agent = AgentIdentity(agent_id="a", name="A", owner="o")
    assert agent.environment == "dev"
    assert agent.created_at is not None
    assert agent.metadata == {}


def test_agent_identity_rejects_bad_environment():
    with pytest.raises(ValueError):
        AgentIdentity(agent_id="a", name="A", owner="o", environment="production")


def test_agent_identity_rejects_empty_id():
    with pytest.raises(ValueError):
        AgentIdentity(agent_id="", name="A", owner="o")


def test_tool_action_rejects_bad_risk_level():
    with pytest.raises(ValueError):
        ToolAction(agent_id="a", tool_name="t", operation="op", risk_level="extreme")


def test_tool_action_generates_unique_ids():
    a = ToolAction(agent_id="a", tool_name="t", operation="op")
    b = ToolAction(agent_id="a", tool_name="t", operation="op")
    assert a.action_id != b.action_id


def test_audit_log_roundtrip(tmp_path):
    log = AuditLog(tmp_path / "nested" / "audit.jsonl")
    action = ToolAction(agent_id="a", tool_name="t", operation="op")
    log.record(action, "allowed", reason="ok")
    log.record(action, "execution_succeeded", result_summary="'done'")

    records = log.read_all()
    assert len(records) == 2
    assert records[0]["event"] == "allowed"
    assert records[0]["reason"] == "ok"
    assert records[1]["result_summary"] == "'done'"
    assert all("timestamp" in r for r in records)


def test_audit_log_is_append_only(tmp_path):
    path = tmp_path / "audit.jsonl"
    action = ToolAction(agent_id="a", tool_name="t", operation="op")
    AuditLog(path).record(action, "allowed")
    AuditLog(path).record(action, "denied")
    assert [r["event"] for r in AuditLog(path).read_all()] == ["allowed", "denied"]
