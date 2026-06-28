"""Example A: an agent calls an allowed tool.

    python examples/basic_allow.py

`research_bot` is allowed to run `web_search` at low risk, so the call goes
through and two audit records are written (authorization + success).
"""

from pathlib import Path

from aegize import AgentIdentity, AuditLog, GuardedTool, PermissionPolicy

HERE = Path(__file__).parent


def web_search(query: str) -> str:
    return f"searched: {query}"


def main() -> None:
    agent = AgentIdentity(
        agent_id="research_bot",
        name="Research Bot",
        owner="Geoffrey",
        environment="dev",
    )
    policy = PermissionPolicy.from_yaml(HERE / "aegize.yaml")
    audit = AuditLog(HERE / "audit.jsonl")

    safe_web_search = GuardedTool(
        tool_name="web_search",
        operation="search",
        func=web_search,
        agent=agent,
        policy=policy,
        audit_log=audit,
        risk_level="low",
    )

    result = safe_web_search("Aegize runtime")
    print("Result:", result)
    print("Audit events:", [r["event"] for r in audit.read_all()])


if __name__ == "__main__":
    main()
