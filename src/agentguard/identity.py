"""Agent identity primitive."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ._time import utcnow

Environment = str  # one of: "dev", "staging", "prod"

VALID_ENVIRONMENTS = ("dev", "staging", "prod")


@dataclass
class AgentIdentity:
    """Represents a single AI agent that wants to use tools.

    Every guarded tool call is attributed to one ``AgentIdentity``. The
    ``agent_id`` is the stable key that policies are written against.
    """

    agent_id: str
    name: str
    owner: str
    environment: Environment = "dev"
    created_at: datetime = field(default_factory=utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.agent_id:
            raise ValueError("agent_id must be a non-empty string")
        if self.environment not in VALID_ENVIRONMENTS:
            raise ValueError(
                f"environment must be one of {VALID_ENVIRONMENTS}, got {self.environment!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "owner": self.owner,
            "environment": self.environment,
            "created_at": self.created_at.isoformat(),
            "metadata": dict(self.metadata),
        }
