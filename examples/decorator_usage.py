"""Example D: ergonomic, decorator-based usage (v0.2).

    python examples/decorator_usage.py

Tools are declared once with @guarded_tool. A GuardContext bundles the agent,
policy, and audit log. You can bind a tool to a context explicitly with
guard(...) (handy for tool registries / MCP servers) or enter a `with context:`
block and call decorated tools directly.
"""

from pathlib import Path

from aegize import (
    AgentIdentity,
    ApprovalRequired,
    AuditLog,
    GuardContext,
    PermissionPolicy,
    PolicyDenied,
    guard,
    guarded_tool,
)

HERE = Path(__file__).parent


@guarded_tool(tool_name="web_search", operation="search", risk_level="low")
def web_search(query: str) -> str:
    return f"searched: {query}"


@guarded_tool(tool_name="email", operation="send", risk_level="high")
def send_email(to: str, body: str) -> str:  # pragma: no cover - gated before run
    raise AssertionError("email should not send without approval")


@guarded_tool(tool_name="file_reader", operation="read", risk_level="low")
def file_reader(path: str) -> str:
    return f"contents of {path}"


def main() -> None:
    agent = AgentIdentity(
        agent_id="research_bot",
        name="Research Bot",
        owner="Geoffrey",
        environment="dev",
    )
    policy = PermissionPolicy.from_yaml(HERE / "aegize.yaml")
    audit = AuditLog(HERE / "audit.jsonl")
    ctx = GuardContext(agent=agent, policy=policy, audit_log=audit)

    # 1. Explicit binding -> a plain callable you can register with a tool server.
    #    e.g. server.add_tool(guard(send_email, context=ctx))
    safe_search = guard(web_search, context=ctx)
    print("search:", safe_search("Aegize runtime"))
    print("  (preserves name/signature for registries:", safe_search.__name__ + ")")

    # 2. Default context: call decorated tools directly inside the block.
    with ctx:
        try:
            send_email("ceo@example.com", "Q3 numbers")
        except ApprovalRequired as exc:
            print("email gated:", exc)

        # 3. Per-call metadata feeds the path allowlist (and lands in the audit log).
        print("read:", file_reader("./safe_data/report.txt"))
        try:
            file_reader("secret", guard_metadata={"path": "/etc/passwd"})
        except PolicyDenied as exc:
            print("blocked read:", exc)

    print("events:", [r["event"] for r in audit.read_all()])


if __name__ == "__main__":
    main()
