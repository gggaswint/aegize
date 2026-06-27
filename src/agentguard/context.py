"""GuardContext: bundles the agent, policy, and audit log together.

A ``GuardContext`` is the "who + rules + ledger" needed to enforce any tool
call. It lets you stop threading ``agent`` / ``policy`` / ``audit_log`` through
every :class:`GuardedTool` or decorated function.

It can also be installed as the *default* context — either explicitly via
:meth:`GuardContext.activate` or temporarily with a ``with`` block — so that
``@guarded_tool``-decorated functions can be called directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .audit import AuditLog
from .identity import AgentIdentity
from .policy import PermissionPolicy

# Explicitly-installed default (via activate()), plus a stack for `with` blocks.
_default_context: GuardContext | None = None
_context_stack: list[GuardContext] = []


@dataclass
class GuardContext:
    """The agent, policy, and audit log required to guard a tool call."""

    agent: AgentIdentity
    policy: PermissionPolicy
    audit_log: AuditLog

    def guard(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        """Bind a ``@guarded_tool``-decorated function to this context.

        Returns a plain callable (signature-preserving) suitable for handing to
        a tool registry, e.g. ``server.add_tool(ctx.guard(send_email))``.
        """
        from .decorators import guard

        return guard(fn, context=self)

    def activate(self) -> GuardContext:
        """Install this context as the process-wide default. Returns self."""
        set_default_context(self)
        return self

    def __enter__(self) -> GuardContext:
        _context_stack.append(self)
        return self

    def __exit__(self, *exc: Any) -> bool:
        if _context_stack and _context_stack[-1] is self:
            _context_stack.pop()
        return False


def set_default_context(context: GuardContext | None) -> None:
    """Install (or clear, with ``None``) the process-wide default context."""
    global _default_context
    _default_context = context


def get_default_context() -> GuardContext | None:
    """Return the active context: the innermost ``with`` block, else the default."""
    if _context_stack:
        return _context_stack[-1]
    return _default_context


def clear_default_context() -> None:
    """Remove the process-wide default context."""
    set_default_context(None)
