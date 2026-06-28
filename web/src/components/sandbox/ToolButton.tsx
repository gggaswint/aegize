import type { ToolDef } from "@/lib/sandbox";
import { DecisionBadge } from "./DecisionBadge";

export function ToolButton({
  tool,
  onClick,
  disabled,
  active,
  resolved,
}: {
  tool: ToolDef;
  onClick: () => void;
  disabled: boolean;
  active: boolean;
  resolved: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={`Simulate ${tool.label}: ${tool.call}`}
      className="group w-full rounded-lg border bg-surface/50 px-3.5 py-2.5 text-left transition-colors duration-200 enabled:hover:bg-surface-2 disabled:cursor-not-allowed disabled:opacity-60"
      style={{ borderColor: active ? "var(--color-accent)" : "var(--color-border-strong)" }}
    >
      <div className="flex items-center justify-between gap-2">
        <span className="text-sm font-medium text-fg">{tool.label}</span>
        {active && resolved ? (
          <DecisionBadge decision={tool.decision} />
        ) : (
          <span
            className="font-mono text-[0.7rem] text-faint transition-colors group-enabled:group-hover:text-muted"
            aria-hidden
          >
            run
          </span>
        )}
      </div>
      <code className="mt-1 block truncate font-mono text-xs text-faint">{tool.call}</code>
    </button>
  );
}
