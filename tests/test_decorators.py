"""Tests for the v0.2 @guarded_tool decorator, GuardContext, and guard()."""

from __future__ import annotations

import inspect

import pytest

from aegize import (
    AegizeError,
    ApprovalRequired,
    GuardContext,
    PolicyDenied,
    clear_default_context,
    guard,
    guarded_tool,
)


@pytest.fixture
def ctx(agent, policy, audit) -> GuardContext:
    return GuardContext(agent=agent, policy=policy, audit_log=audit)


@pytest.fixture(autouse=True)
def _reset_default_context():
    # Ensure no default context leaks between tests.
    clear_default_context()
    yield
    clear_default_context()


def _spy():
    state = {"ran": False}

    def fn(*args, **kwargs):
        state["ran"] = True
        return "ok"

    return fn, state


def test_decorator_allows_permitted_call(ctx):
    fn, state = _spy()
    tool = guarded_tool(tool_name="web_search", operation="search", risk_level="low")(fn)

    bound = guard(tool, context=ctx)
    assert bound("hello") == "ok"
    assert state["ran"] is True
    assert [r["event"] for r in ctx.audit_log.read_all()] == ["allowed", "execution_succeeded"]


def test_decorator_blocks_denied_call(ctx):
    fn, state = _spy()
    tool = guarded_tool(tool_name="shell", operation="rm", risk_level="critical")(fn)

    bound = guard(tool, context=ctx)
    with pytest.raises(PolicyDenied):
        bound("rm -rf /")
    assert state["ran"] is False
    assert [r["event"] for r in ctx.audit_log.read_all()] == ["denied"]


def test_decorator_raises_approval_required_before_execution(ctx):
    fn, state = _spy()
    tool = guarded_tool(tool_name="email", operation="send", risk_level="high")(fn)

    bound = guard(tool, context=ctx)
    with pytest.raises(ApprovalRequired):
        bound("a@b.com", body="hi")
    assert state["ran"] is False
    assert [r["event"] for r in ctx.audit_log.read_all()] == ["approval_required"]


def test_metadata_can_be_passed_per_call(ctx):
    @guarded_tool(tool_name="file_reader", operation="read")
    def file_reader(label: str) -> str:
        return f"read {label}"

    bound = guard(file_reader, context=ctx)

    # A path inside the allowlist (supplied per call) is permitted...
    assert bound("report", guard_metadata={"path": "./safe_data/report.txt"}) == "read report"

    # ...and the per-call metadata is recorded in the audit log.
    allowed = [r for r in ctx.audit_log.read_all() if r["event"] == "allowed"][-1]
    assert allowed["metadata"]["path"] == "./safe_data/report.txt"

    # A path outside the allowlist is denied.
    with pytest.raises(PolicyDenied):
        bound("report", guard_metadata={"path": "/etc/passwd"})


def test_guard_metadata_is_not_forwarded_to_wrapped_function(ctx):
    received = {}

    @guarded_tool(tool_name="web_search", operation="search")
    def web_search(query: str, **kwargs) -> str:
        received.update(kwargs)
        return query

    bound = guard(web_search, context=ctx)
    bound("hi", guard_metadata={"path": "x"})
    assert "guard_metadata" not in received


def test_default_context_allows_direct_call(ctx):
    fn, state = _spy()
    tool = guarded_tool(tool_name="web_search", operation="search")(fn)

    with ctx:
        assert tool("hello") == "ok"
    assert state["ran"] is True


def test_call_without_context_raises(ctx):
    @guarded_tool(tool_name="web_search", operation="search")
    def web_search(query: str) -> str:
        return query

    with pytest.raises(AegizeError):
        web_search("no context bound")


def test_with_block_restores_previous_default(agent, policy, audit):
    from aegize import get_default_context

    outer = GuardContext(agent=agent, policy=policy, audit_log=audit).activate()
    inner = GuardContext(agent=agent, policy=policy, audit_log=audit)
    assert get_default_context() is outer
    with inner:
        assert get_default_context() is inner
    assert get_default_context() is outer


def test_guard_preserves_signature_and_name(ctx):
    @guarded_tool(tool_name="web_search", operation="search")
    def web_search(query: str) -> str:
        """Search the web."""
        return query

    bound = guard(web_search, context=ctx)
    assert bound.__name__ == "web_search"
    assert bound.__doc__ == "Search the web."
    assert list(inspect.signature(bound).parameters) == ["query"]


def test_guard_rejects_undecorated_function(ctx):
    def plain(x):
        return x

    with pytest.raises(TypeError):
        guard(plain, context=ctx)


def test_context_guard_helper_binds(ctx):
    fn, state = _spy()
    tool = guarded_tool(tool_name="web_search", operation="search")(fn)

    bound = ctx.guard(tool)
    assert bound("hello") == "ok"
    assert state["ran"] is True
