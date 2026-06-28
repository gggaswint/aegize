"""GuardedTool: the enforcement point that wraps any callable."""

from __future__ import annotations

from typing import Any, Callable

from .action import ToolAction
from .audit import (
    EVENT_ALLOWED,
    EVENT_APPROVAL_REQUIRED,
    EVENT_DENIED,
    EVENT_EXECUTION_FAILED,
    EVENT_EXECUTION_SUCCEEDED,
    AuditLog,
)
from .exceptions import ApprovalRequired, PolicyDenied
from .identity import AgentIdentity
from .policy import Decision, PermissionPolicy

_SUMMARY_LIMIT = 200

# Reserved keyword for attaching per-call metadata. It is stripped from the
# arguments before the wrapped function is invoked, so the function never sees
# it. Used to drive path allowlists and to enrich audit records at call time.
GUARD_METADATA_KWARG = "guard_metadata"

# Internal bookkeeping keys that should not be echoed back into the audit log.
_INTERNAL_METADATA_KEYS = frozenset({"candidate_paths"})


def _truncate(text: str, limit: int = _SUMMARY_LIMIT) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _summarize_inputs(args: tuple, kwargs: dict[str, Any]) -> str:
    parts: list[str] = [repr(a) for a in args]
    parts += [f"{k}={v!r}" for k, v in kwargs.items()]
    return _truncate(", ".join(parts))


def _string_inputs(args: tuple, kwargs: dict[str, Any]) -> list[str]:
    """Strings from the call that may represent paths (for path allowlists)."""
    candidates = [a for a in args if isinstance(a, str)]
    candidates += [v for v in kwargs.values() if isinstance(v, str)]
    return candidates


class GuardedTool:
    """Wrap a callable so every invocation is permissioned, gated, and audited.

    The wrapper is itself callable, so a ``GuardedTool`` is a drop-in
    replacement for the function it guards::

        safe_search = GuardedTool(
            tool_name="web_search",
            operation="search",
            func=web_search,
            agent=agent,
            policy=policy,
            audit_log=audit,
            risk_level="low",
        )
        result = safe_search("Aegize runtime")

    Order of operations on every call:

    1. Build a :class:`ToolAction` describing the attempt.
    2. Evaluate it against the :class:`PermissionPolicy`.
    3. Audit the decision **before** any execution.
    4. Deny -> raise :class:`PolicyDenied` (function never runs).
       Approval -> raise :class:`ApprovalRequired` (function never runs).
       Allow -> run the function, then audit success or failure.
    """

    def __init__(
        self,
        *,
        tool_name: str,
        operation: str,
        func: Callable[..., Any],
        agent: AgentIdentity,
        policy: PermissionPolicy,
        audit_log: AuditLog,
        risk_level: str = "low",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.tool_name = tool_name
        self.operation = operation
        self.func = func
        self.agent = agent
        self.policy = policy
        self.audit_log = audit_log
        self.risk_level = risk_level
        self.metadata = dict(metadata or {})

    def build_action(
        self,
        args: tuple,
        kwargs: dict[str, Any],
        *,
        extra_metadata: dict[str, Any] | None = None,
    ) -> ToolAction:
        metadata = dict(self.metadata)
        if extra_metadata:
            metadata.update(extra_metadata)
        metadata.setdefault("environment", self.agent.environment)
        # Surface string arguments so path allowlists can be enforced.
        candidates = list(metadata.get("candidate_paths") or [])
        candidates += _string_inputs(args, kwargs)
        metadata["candidate_paths"] = candidates
        return ToolAction(
            agent_id=self.agent.agent_id,
            tool_name=self.tool_name,
            operation=self.operation,
            input_summary=_summarize_inputs(args, kwargs),
            risk_level=self.risk_level,
            metadata=metadata,
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        call_metadata = kwargs.pop(GUARD_METADATA_KWARG, None)
        action = self.build_action(args, kwargs, extra_metadata=call_metadata)
        audit_extra = {"metadata": self._audit_metadata(action)}
        result = self.policy.evaluate(action)

        if result.decision is Decision.DENY:
            # Audit the denial before refusing. Function never runs.
            self.audit_log.record(action, EVENT_DENIED, reason=result.reason, extra=audit_extra)
            raise PolicyDenied(result.reason, reason=result.reason, action=action)

        if result.decision is Decision.REQUIRE_APPROVAL:
            # Audit the gate before refusing. Function never runs.
            self.audit_log.record(
                action, EVENT_APPROVAL_REQUIRED, reason=result.reason, extra=audit_extra
            )
            raise ApprovalRequired(result.reason, reason=result.reason, action=action)

        # Allowed: audit the authorization *before* executing the function.
        self.audit_log.record(action, EVENT_ALLOWED, reason=result.reason, extra=audit_extra)
        try:
            value = self.func(*args, **kwargs)
        except Exception as exc:
            self.audit_log.record(
                action, EVENT_EXECUTION_FAILED, error=repr(exc), extra=audit_extra
            )
            raise
        self.audit_log.record(
            action,
            EVENT_EXECUTION_SUCCEEDED,
            result_summary=_truncate(repr(value)),
            extra=audit_extra,
        )
        return value

    @staticmethod
    def _audit_metadata(action: ToolAction) -> dict[str, Any]:
        """User-facing metadata for the audit log (internal keys stripped)."""
        return {k: v for k, v in action.metadata.items() if k not in _INTERNAL_METADATA_KEYS}
