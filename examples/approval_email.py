"""Example C: an agent attempts to send email and is gated for approval.

    python examples/approval_email.py

`email` / `send` is configured as `require_approval`. Aegize raises
`ApprovalRequired` and the underlying function is never executed.
"""

from pathlib import Path

from aegize import AgentIdentity, ApprovalRequired, AuditLog, GuardedTool, PermissionPolicy

HERE = Path(__file__).parent


def send_email(to: str, subject: str, body: str) -> str:
    # This must never run until a human approves the action.
    raise AssertionError("email should not send without approval")


def main() -> None:
    agent = AgentIdentity(
        agent_id="research_bot",
        name="Research Bot",
        owner="Geoffrey",
        environment="dev",
    )
    policy = PermissionPolicy.from_yaml(HERE / "aegize.yaml")
    audit = AuditLog(HERE / "audit.jsonl")

    guarded_email = GuardedTool(
        tool_name="email",
        operation="send",
        func=send_email,
        agent=agent,
        policy=policy,
        audit_log=audit,
        risk_level="high",
    )

    try:
        guarded_email("ceo@example.com", "Q3 numbers", "See attached.")
    except ApprovalRequired as exc:
        print("Needs human approval:", exc)
    else:
        print("ERROR: email was sent without approval")

    print("Audit events:", [r["event"] for r in audit.read_all()])


if __name__ == "__main__":
    main()
