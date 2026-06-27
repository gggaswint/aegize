"""Append-only JSONL audit log.

Every attempted action produces at least one audit record. Allowed actions
produce two: one when the action is authorized (before execution) and one for
the execution result (success or failure). The log is append-only and one JSON
object per line, so it is trivial to tail, grep, or ship to a SIEM.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from ._time import utcnow
from .action import ToolAction

# Canonical event names written to the audit log.
EVENT_ALLOWED = "allowed"
EVENT_DENIED = "denied"
EVENT_APPROVAL_REQUIRED = "approval_required"
EVENT_EXECUTION_SUCCEEDED = "execution_succeeded"
EVENT_EXECUTION_FAILED = "execution_failed"


class AuditLog:
    """Writes audit records to a JSONL file (one JSON object per line)."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        parent = self.path.parent
        if parent and not parent.exists():
            os.makedirs(parent, exist_ok=True)

    def record(
        self,
        action: ToolAction,
        event: str,
        *,
        reason: str | None = None,
        error: str | None = None,
        result_summary: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Append one audit entry and return the written record."""
        entry: dict[str, Any] = {
            "timestamp": utcnow().isoformat(),
            "event": event,
            "action_id": action.action_id,
            "agent_id": action.agent_id,
            "tool_name": action.tool_name,
            "operation": action.operation,
            "risk_level": action.risk_level,
            "input_summary": action.input_summary,
        }
        if reason is not None:
            entry["reason"] = reason
        if error is not None:
            entry["error"] = error
        if result_summary is not None:
            entry["result_summary"] = result_summary
        if extra:
            entry.update(extra)
        self._write(entry)
        return entry

    def _write(self, entry: dict[str, Any]) -> None:
        line = json.dumps(entry, default=str, ensure_ascii=False)
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        """Read every record back. Convenience for tests and small tools."""
        if not self.path.exists():
            return []
        records: list[dict[str, Any]] = []
        with open(self.path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
