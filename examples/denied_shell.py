"""Example B: an agent attempts a denied shell command.

    python examples/denied_shell.py

`shell` with operation `rm` is explicitly denied. The wrapped function is never
executed and a `denied` record is written to the audit log.
"""

from pathlib import Path

from agentguard import AgentIdentity, AuditLog, GuardedTool, PermissionPolicy, PolicyDenied

HERE = Path(__file__).parent


def run_shell(command: str) -> str:
    # This must never run for a denied operation.
    raise AssertionError("denied command should not execute")


def main() -> None:
    agent = AgentIdentity(
        agent_id="research_bot",
        name="Research Bot",
        owner="Geoffrey",
        environment="dev",
    )
    policy = PermissionPolicy.from_yaml(HERE / "agentguard.yaml")
    audit = AuditLog(HERE / "audit.jsonl")

    dangerous_rm = GuardedTool(
        tool_name="shell",
        operation="rm",
        func=run_shell,
        agent=agent,
        policy=policy,
        audit_log=audit,
        risk_level="critical",
    )

    try:
        dangerous_rm("rm -rf /")
    except PolicyDenied as exc:
        print("Blocked:", exc)
    else:
        print("ERROR: command was not blocked")

    print("Audit events:", [r["event"] for r in audit.read_all()])


if __name__ == "__main__":
    main()
