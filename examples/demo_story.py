"""AgentGuard demo: one agent, three tool calls, three outcomes.

    python examples/demo_story.py

An AI agent attempts three tool calls. AgentGuard:

  * ALLOWS   a web search,
  * REQUIRES APPROVAL for sending email,
  * DENIES   a shell command,

and writes an audit record for every attempt. The wrapped functions for the
gated and denied calls never run.
"""

from pathlib import Path

from agentguard import (
    AgentIdentity,
    ApprovalRequired,
    AuditLog,
    GuardedTool,
    PermissionPolicy,
    PolicyDenied,
)

HERE = Path(__file__).parent
POLICY_PATH = HERE / "demo_policy.yaml"
AUDIT_PATH = HERE / "demo_audit.jsonl"


# --- the agent's tools (plain functions) ------------------------------------


def web_search(query: str) -> str:
    return f"results for {query!r}"


def send_email(to: str, subject: str) -> str:  # pragma: no cover - gated before run
    raise AssertionError("email should not send without approval")


def run_shell(command: str) -> str:  # pragma: no cover - denied before run
    raise AssertionError("denied shell command should never execute")


# --- helpers ----------------------------------------------------------------


def attempt(step: int, label: str, tool: GuardedTool, *args) -> None:
    print(f"[{step}] {label}")
    try:
        result = tool(*args)
        print(f"    ALLOWED  -> {result}")
    except ApprovalRequired as exc:
        print("    APPROVAL REQUIRED  -> held for human review (not executed)")
        print(f"               reason: {exc}")
    except PolicyDenied as exc:
        print("    DENIED  -> blocked before execution")
        print(f"               reason: {exc}")
    print()


def main() -> None:
    # Start each run with a fresh audit log so the recording is clean.
    AUDIT_PATH.unlink(missing_ok=True)

    agent = AgentIdentity(
        agent_id="demo_agent",
        name="Demo Agent",
        owner="Geoffrey",
        environment="prod",
    )
    policy = PermissionPolicy.from_yaml(POLICY_PATH)
    audit = AuditLog(AUDIT_PATH)

    def guard(tool_name: str, operation: str, func, risk_level: str) -> GuardedTool:
        return GuardedTool(
            tool_name=tool_name,
            operation=operation,
            func=func,
            agent=agent,
            policy=policy,
            audit_log=audit,
            risk_level=risk_level,
        )

    print("AgentGuard demo — agent 'demo_agent' (prod) attempts three tool calls")
    print(f"Policy:    {POLICY_PATH}")
    print(f"Audit log: {AUDIT_PATH.resolve()}")
    print()

    attempt(1, "web_search.search   query='AI safety companies'",
            guard("web_search", "search", web_search, "low"),
            "AI safety companies")

    attempt(2, "email.send          to='ceo@example.com'",
            guard("email", "send", send_email, "high"),
            "ceo@example.com", "Q3 numbers")

    attempt(3, "shell.execute       cmd='rm -rf /var/data'",
            guard("shell", "execute", run_shell, "critical"),
            "rm -rf /var/data")

    # --- the audit trail ----------------------------------------------------
    records = audit.read_all()
    print("Audit trail:")
    for r in records:
        print(f"    {r['event']:<20} {r['tool_name']:<12} {r['operation']}")
    print()

    allowed = sum(1 for r in records if r["event"] == "allowed")
    approval = sum(1 for r in records if r["event"] == "approval_required")
    denied = sum(1 for r in records if r["event"] == "denied")
    print(
        f"3 actions attempted · {allowed} allowed · {approval} awaiting approval · "
        f"{denied} denied · {len(records)} audit records written"
    )
    print(f"Full audit log: {AUDIT_PATH.resolve()}")


if __name__ == "__main__":
    main()
