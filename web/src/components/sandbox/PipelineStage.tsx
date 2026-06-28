export type StageStatus = "idle" | "active" | "passed" | "pause" | "blocked" | "done";

const COLOR: Record<StageStatus, string> = {
  idle: "var(--color-border-strong)",
  active: "var(--color-accent)",
  passed: "var(--color-accent)",
  pause: "var(--color-approval)",
  blocked: "var(--color-deny)",
  done: "var(--color-allow)",
};

export const ROW_H = 54;

export function PipelineStage({
  label,
  status,
  sublabel,
}: {
  label: string;
  status: StageStatus;
  sublabel?: string;
}) {
  const color = COLOR[status];
  const reached = status !== "idle";
  const focus =
    status === "active" || status === "pause" || status === "blocked" || status === "done";

  return (
    <li className="relative flex items-center" style={{ height: ROW_H }}>
      <span
        className="absolute"
        style={{ left: 16, top: "50%", transform: "translate(-50%, -50%)" }}
        aria-hidden
      >
        <span
          className="block rounded-full border transition-all duration-300"
          style={{
            width: focus ? 14 : 10,
            height: focus ? 14 : 10,
            color,
            borderColor: color,
            backgroundColor: focus
              ? color
              : reached
                ? "color-mix(in srgb, var(--color-accent) 28%, transparent)"
                : "var(--color-bg)",
            boxShadow: focus ? `0 0 12px ${color}` : "none",
            animation: status === "active" ? "pulse-glow 1.5s ease-in-out infinite" : "none",
          }}
        />
      </span>

      <div className="flex min-w-0 items-baseline gap-2 pl-10">
        <span
          className="font-mono text-sm transition-colors duration-300"
          style={{ color: reached ? "var(--color-fg)" : "var(--color-faint)" }}
        >
          {label}
        </span>
        {sublabel && (
          <span className="truncate font-mono text-xs" style={{ color }}>
            {sublabel}
          </span>
        )}
      </div>
    </li>
  );
}
