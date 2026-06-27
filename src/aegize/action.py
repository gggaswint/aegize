"""Tool action primitive."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from ._time import utcnow

RISK_LEVELS = ("low", "medium", "high", "critical")

# Numeric ordering so that risk levels can be compared (e.g. risk_level_max).
RISK_ORDER: dict[str, int] = {level: i for i, level in enumerate(RISK_LEVELS)}


@dataclass
class ToolAction:
    """A single attempted tool call, evaluated against policy and audited.

    ``ToolAction`` is normally constructed for you by :class:`GuardedTool`, but
    it is a plain dataclass so it can be built and inspected directly in tests
    or custom integrations.
    """

    agent_id: str
    tool_name: str
    operation: str
    input_summary: str = ""
    risk_level: str = "low"
    action_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(
                f"risk_level must be one of {RISK_LEVELS}, got {self.risk_level!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "agent_id": self.agent_id,
            "tool_name": self.tool_name,
            "operation": self.operation,
            "input_summary": self.input_summary,
            "risk_level": self.risk_level,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }
