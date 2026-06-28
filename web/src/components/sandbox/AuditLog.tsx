import type { AuditEntry } from "@/lib/sandbox";
import { DecisionBadge } from "./DecisionBadge";

export function AuditLog({ entries }: { entries: AuditEntry[] }) {
  return (
    <div className="rounded-xl border border-border bg-surface/40">
      <div className="flex items-center justify-between border-b border-border px-4 py-2.5">
        <span className="font-mono text-xs uppercase tracking-[0.16em] text-muted">Audit log</span>
        <span className="font-mono text-[0.7rem] text-faint">append-only</span>
      </div>

      {entries.length === 0 ? (
        <p className="px-4 py-6 text-center font-mono text-xs text-faint">
          No actions yet — choose a tool to record an entry.
        </p>
      ) : (
        <ul>
          {entries.map((e) => (
            <li
              key={e.id}
              className="flex flex-wrap items-center gap-x-3 gap-y-1.5 border-b border-border/60 px-4 py-2.5 font-mono text-xs last:border-b-0"
            >
              <span className="tabular-nums text-faint">{e.time}</span>
              <span className="text-muted">{e.agent}</span>
              <span className="text-fg">{e.target}</span>
              <DecisionBadge decision={e.decision} />
              <span className="text-faint">{e.reason}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
