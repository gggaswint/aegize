"""Exception hierarchy for AgentGuard.

All AgentGuard errors derive from :class:`AgentGuardError`, so callers can catch
the whole family with a single ``except`` clause while still being able to
distinguish a hard policy denial from an approval gate.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .action import ToolAction


class AgentGuardError(Exception):
    """Base class for every error raised by AgentGuard."""


class PolicyLoadError(AgentGuardError):
    """Raised when a policy file cannot be read, parsed, or validated."""


class _DecisionError(AgentGuardError):
    """Shared base for errors that carry the offending action and a reason."""

    def __init__(
        self,
        message: str,
        *,
        reason: str | None = None,
        action: ToolAction | None = None,
    ) -> None:
        super().__init__(message)
        self.reason = reason
        self.action = action


class PolicyDenied(_DecisionError):
    """Raised when policy explicitly (or by default-deny) blocks an action.

    The underlying tool function is never executed.
    """


class ApprovalRequired(_DecisionError):
    """Raised when an action needs human approval before it may run.

    The underlying tool function is never executed. A human (or an out-of-band
    approval workflow) must authorize the action and re-issue it.
    """
