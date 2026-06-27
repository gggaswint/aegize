"""Behavioral tests for the GuardedTool enforcement point."""

from __future__ import annotations

import pytest

from agentguard import ApprovalRequired, GuardedTool, PolicyDenied


def _calls(record):
    """A spy function that records whether it ran."""
    record["ran"] = False

    def fn(*args, **kwargs):
        record["ran"] = True
        return "ok"

    return fn


def test_allowed_action_executes(agent, policy, audit):
    record = {}
    tool = GuardedTool(
        tool_name="web_search",
        operation="search",
        func=_calls(record),
        agent=agent,
        policy=policy,
        audit_log=audit,
        risk_level="low",
    )

    assert tool("hello") == "ok"
    assert record["ran"] is True

    events = [r["event"] for r in audit.read_all()]
    assert events == ["allowed", "execution_succeeded"]


def test_denied_action_does_not_execute(agent, policy, audit):
    record = {}
    tool = GuardedTool(
        tool_name="shell",
        operation="rm",
        func=_calls(record),
        agent=agent,
        policy=policy,
        audit_log=audit,
        risk_level="critical",
    )

    with pytest.raises(PolicyDenied):
        tool("rm -rf /")

    assert record["ran"] is False
    events = [r["event"] for r in audit.read_all()]
    assert events == ["denied"]


def test_approval_required_does_not_execute(agent, policy, audit):
    record = {}
    tool = GuardedTool(
        tool_name="email",
        operation="send",
        func=_calls(record),
        agent=agent,
        policy=policy,
        audit_log=audit,
        risk_level="high",
    )

    with pytest.raises(ApprovalRequired):
        tool("a@b.com", subject="hi", body="x")

    assert record["ran"] is False
    events = [r["event"] for r in audit.read_all()]
    assert events == ["approval_required"]


def test_failed_execution_is_logged_and_reraised(agent, policy, audit):
    def boom(query):
        raise RuntimeError("kaboom")

    tool = GuardedTool(
        tool_name="web_search",
        operation="search",
        func=boom,
        agent=agent,
        policy=policy,
        audit_log=audit,
        risk_level="low",
    )

    with pytest.raises(RuntimeError, match="kaboom"):
        tool("hello")

    records = audit.read_all()
    events = [r["event"] for r in records]
    assert events == ["allowed", "execution_failed"]
    assert "kaboom" in records[-1]["error"]


def test_audit_written_for_every_outcome(agent, policy, audit):
    """allowed, denied, and approval_required each produce audit records."""
    GuardedTool(
        tool_name="web_search",
        operation="search",
        func=lambda q: "ok",
        agent=agent,
        policy=policy,
        audit_log=audit,
    )("q")

    with pytest.raises(PolicyDenied):
        GuardedTool(
            tool_name="payments",
            operation="charge",
            func=lambda: "ok",
            agent=agent,
            policy=policy,
            audit_log=audit,
        )()

    with pytest.raises(ApprovalRequired):
        GuardedTool(
            tool_name="shell",
            operation="execute",
            func=lambda: "ok",
            agent=agent,
            policy=policy,
            audit_log=audit,
        )()

    events = [r["event"] for r in audit.read_all()]
    assert "allowed" in events
    assert "execution_succeeded" in events
    assert "denied" in events
    assert "approval_required" in events


def test_unknown_agent_defaults_to_deny(policy, audit):
    from agentguard import AgentIdentity

    stranger = AgentIdentity(agent_id="stranger", name="X", owner="nobody")
    record = {}
    tool = GuardedTool(
        tool_name="web_search",
        operation="search",
        func=_calls(record),
        agent=stranger,
        policy=policy,
        audit_log=audit,
    )

    with pytest.raises(PolicyDenied):
        tool("q")
    assert record["ran"] is False


def test_unknown_tool_defaults_to_deny(agent, policy, audit):
    record = {}
    tool = GuardedTool(
        tool_name="totally_new_tool",
        operation="do_thing",
        func=_calls(record),
        agent=agent,
        policy=policy,
        audit_log=audit,
    )

    with pytest.raises(PolicyDenied):
        tool("q")
    assert record["ran"] is False
