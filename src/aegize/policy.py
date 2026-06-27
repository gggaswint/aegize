"""YAML-backed policy engine.

Design goals:

* **Default deny.** No matching ``allow`` rule means the action is denied.
* **Deny wins.** An explicit ``deny`` rule overrides ``require_approval`` and
  ``allow`` for the same tool/operation.
* **Readable rules.** Policies are plain YAML so they can live in version
  control and be reviewed like any other code.

Evaluation order for a given action:

1. ``deny``             -> :data:`Decision.DENY`
2. ``require_approval`` -> :data:`Decision.REQUIRE_APPROVAL`
3. ``allow``            -> :data:`Decision.ALLOW`
4. otherwise            -> default-deny
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .action import RISK_ORDER, ToolAction
from .exceptions import PolicyLoadError


class Decision(str, Enum):
    """The three possible policy outcomes."""

    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


@dataclass
class PolicyResult:
    """Outcome of evaluating a :class:`ToolAction` against a policy."""

    decision: Decision
    reason: str
    matched_rule: dict[str, Any] | None = None

    @property
    def allowed(self) -> bool:
        return self.decision is Decision.ALLOW


def _normalize_path(value: str) -> str:
    """Normalize a path for glob comparison (forward slashes, no leading ``./``)."""
    norm = value.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]
    return norm


def _path_matches(path: str, pattern: str) -> bool:
    """Return True if ``path`` matches the glob ``pattern``.

    ``**`` is treated like ``*`` (it matches across directory separators), which
    is sufficient for v0.1 allowlists such as ``./safe_data/**``.
    """
    return fnmatch.fnmatch(_normalize_path(path), _normalize_path(pattern))


def _tool_and_operation_match(rule: dict[str, Any], action: ToolAction) -> bool:
    """Match a rule on tool name and (optionally) operation.

    A rule with no ``operations`` list matches every operation for that tool.
    """
    if rule.get("tool") != action.tool_name:
        return False
    operations = rule.get("operations")
    if operations is None:
        return True
    return action.operation in operations


def _candidate_paths(action: ToolAction) -> list[str]:
    """Collect strings from the action that could represent a filesystem path."""
    candidates: list[str] = []
    explicit = action.metadata.get("path")
    if isinstance(explicit, str):
        candidates.append(explicit)
    for value in action.metadata.get("candidate_paths") or []:
        if isinstance(value, str):
            candidates.append(value)
    return candidates


def _path_rule_satisfied(rule: dict[str, Any], action: ToolAction) -> bool:
    """If a rule constrains paths, at least one candidate path must match."""
    patterns = rule.get("paths")
    if patterns is None:
        return True
    candidates = _candidate_paths(action)
    if not candidates:
        return False
    return any(_path_matches(c, p) for c in candidates for p in patterns)


def _risk_rule_satisfied(rule: dict[str, Any], action: ToolAction) -> bool:
    """If a rule sets ``risk_level_max``, the action's risk must not exceed it."""
    rmax = rule.get("risk_level_max")
    if rmax is None:
        return True
    if rmax not in RISK_ORDER:
        raise PolicyLoadError(f"invalid risk_level_max in policy: {rmax!r}")
    return RISK_ORDER[action.risk_level] <= RISK_ORDER[rmax]


class PermissionPolicy:
    """Evaluates :class:`ToolAction` objects against a set of per-agent rules."""

    def __init__(self, agents: dict[str, Any], *, source: str | None = None) -> None:
        self._agents = agents or {}
        self.source = source

    # -- construction ----------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, source: str | None = None) -> PermissionPolicy:
        if not isinstance(data, dict):
            raise PolicyLoadError("policy root must be a mapping")
        agents = data.get("agents")
        if agents is None:
            raise PolicyLoadError("policy is missing the top-level 'agents' key")
        if not isinstance(agents, dict):
            raise PolicyLoadError("'agents' must be a mapping of agent_id -> rules")
        return cls(agents, source=source)

    @classmethod
    def from_yaml(cls, path: str | Path) -> PermissionPolicy:
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise PolicyLoadError("PyYAML is required to load policies from YAML") from exc

        path = Path(path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise PolicyLoadError(f"could not read policy file: {path}") from exc
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise PolicyLoadError(f"could not parse policy YAML: {path}") from exc
        if data is None:
            raise PolicyLoadError(f"policy file is empty: {path}")
        return cls.from_dict(data, source=str(path))

    # -- evaluation ------------------------------------------------------

    def evaluate(self, action: ToolAction) -> PolicyResult:
        """Evaluate an action and return a :class:`PolicyResult`.

        Unknown agents and tools, and any action with no matching ``allow``
        rule, resolve to :data:`Decision.DENY`.
        """
        agent_rules = self._agents.get(action.agent_id)
        if agent_rules is None:
            return PolicyResult(
                Decision.DENY,
                reason=f"unknown agent '{action.agent_id}' (default deny)",
            )

        # 1. Explicit deny wins outright.
        for rule in agent_rules.get("deny", []) or []:
            if _tool_and_operation_match(rule, action):
                return PolicyResult(
                    Decision.DENY,
                    reason=f"denied by rule for tool '{action.tool_name}'",
                    matched_rule=rule,
                )

        # 2. Approval gate.
        for rule in agent_rules.get("require_approval", []) or []:
            if _tool_and_operation_match(rule, action):
                return PolicyResult(
                    Decision.REQUIRE_APPROVAL,
                    reason=f"approval required for tool '{action.tool_name}'",
                    matched_rule=rule,
                )

        # 3. Allow (subject to risk and path constraints).
        for rule in agent_rules.get("allow", []) or []:
            if not _tool_and_operation_match(rule, action):
                continue
            if not _risk_rule_satisfied(rule, action):
                continue
            if not _path_rule_satisfied(rule, action):
                continue
            return PolicyResult(
                Decision.ALLOW,
                reason=f"allowed by rule for tool '{action.tool_name}'",
                matched_rule=rule,
            )

        # 4. Default deny.
        return PolicyResult(
            Decision.DENY,
            reason=(
                f"no matching allow rule for tool '{action.tool_name}' "
                f"operation '{action.operation}' (default deny)"
            ),
        )
