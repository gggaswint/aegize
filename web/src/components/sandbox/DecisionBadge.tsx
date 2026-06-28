import { DECISION_META, type Decision } from "@/lib/sandbox";

export function DecisionBadge({ decision }: { decision: Decision }) {
  const { label, color } = DECISION_META[decision];
  return (
    <span
      className="inline-flex shrink-0 items-center rounded-full border px-2 py-0.5 font-mono text-[0.68rem] leading-none"
      style={{
        color,
        borderColor: color,
        backgroundColor: "color-mix(in srgb, currentColor 12%, transparent)",
      }}
    >
      {label}
    </span>
  );
}
