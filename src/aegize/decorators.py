"""The ``@guarded_tool`` decorator and the ``guard()`` adapter.

These are pure ergonomics on top of :class:`GuardedTool`. Decorate a function
once with its policy coordinates, then bind it to a :class:`GuardContext` when
you have one::

    @guarded_tool(tool_name="email", operation="send", risk_level="high")
    def send_email(to: str, body: str) -> str:
        ...

    # later, with a context in hand:
    server.add_tool(guard(send_email, context=ctx))

The object returned by ``guard()`` is a signature-preserving callable, so tool
registries (including MCP servers) that introspect ``__name__`` and the function
signature keep working.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from typing import Any, Callable

from .context import GuardContext, get_default_context
from .exceptions import AegizeError
from .guarded_tool import GuardedTool


@dataclass
class GuardSpec:
    """The policy coordinates captured by ``@guarded_tool`` at decoration time."""

    tool_name: str
    operation: str
    risk_level: str = "low"
    metadata: dict[str, Any] = field(default_factory=dict)


class GuardedFunction:
    """A function tagged with a :class:`GuardSpec` by ``@guarded_tool``.

    Calling it directly enforces policy using the active default context (set
    via ``with context:`` or :meth:`GuardContext.activate`). To bind it to a
    specific context explicitly, use :func:`guard` or :meth:`bind`.
    """

    def __init__(
        self,
        func: Callable[..., Any],
        spec: GuardSpec,
        context: GuardContext | None = None,
    ) -> None:
        functools.update_wrapper(self, func)
        self.__wrapped__ = func
        self.spec = spec
        self.context = context

    def bind(self, context: GuardContext) -> GuardedTool:
        """Build a :class:`GuardedTool` for this function bound to ``context``."""
        return GuardedTool(
            tool_name=self.spec.tool_name,
            operation=self.spec.operation,
            func=self.__wrapped__,
            agent=context.agent,
            policy=context.policy,
            audit_log=context.audit_log,
            risk_level=self.spec.risk_level,
            metadata=self.spec.metadata,
        )

    def _resolve_context(self) -> GuardContext:
        context = self.context or get_default_context()
        if context is None:
            raise AegizeError(
                "no GuardContext is active for this guarded tool; bind one with "
                "guard(fn, context=...), enter a `with context:` block, or install "
                "a default via context.activate()"
            )
        return context

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.bind(self._resolve_context())(*args, **kwargs)


def guarded_tool(
    *,
    tool_name: str,
    operation: str,
    risk_level: str = "low",
    metadata: dict[str, Any] | None = None,
) -> Callable[[Callable[..., Any]], GuardedFunction]:
    """Decorator that tags a function with its Aegize policy coordinates."""

    def decorator(func: Callable[..., Any]) -> GuardedFunction:
        spec = GuardSpec(
            tool_name=tool_name,
            operation=operation,
            risk_level=risk_level,
            metadata=dict(metadata or {}),
        )
        return GuardedFunction(func, spec)

    return decorator


def guard(
    fn: Callable[..., Any],
    *,
    context: GuardContext | None = None,
) -> Callable[..., Any]:
    """Bind a ``@guarded_tool`` function to a context, returning a callable.

    The returned callable preserves the original function's name, docstring, and
    signature, so it is a drop-in replacement that tool registries can introspect.
    """
    if not isinstance(fn, GuardedFunction):
        raise TypeError(
            "guard() expects a function decorated with @guarded_tool; "
            f"got {type(fn).__name__}"
        )

    resolved = context or fn.context or get_default_context()
    if resolved is None:
        raise AegizeError(
            "guard() requires a GuardContext; pass context=... or install a "
            "default via context.activate()"
        )

    guarded = fn.bind(resolved)

    @functools.wraps(fn.__wrapped__)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return guarded(*args, **kwargs)

    # Expose the underlying objects for introspection / advanced use.
    wrapper.guarded_tool = guarded  # type: ignore[attr-defined]
    wrapper.guard_spec = fn.spec  # type: ignore[attr-defined]
    return wrapper
