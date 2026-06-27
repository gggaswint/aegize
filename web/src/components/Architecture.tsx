import { ArrowDown } from "./icons";
import { Reveal } from "./Reveal";
import { Section } from "./Section";

const RUNTIME_LAYERS = [
  "identity",
  "policy",
  "permissions",
  "approval",
  "audit",
  "observability",
];

function Layer({
  label,
  items,
  accent = false,
}: {
  label: string;
  items: string[];
  accent?: boolean;
}) {
  return (
    <div
      className={`w-full rounded-xl border px-6 py-6 text-center ${
        accent
          ? "border-accent/40 bg-accent/[0.06] shadow-[0_0_40px_-12px_rgba(91,157,255,0.4)]"
          : "border-border-strong bg-surface/40"
      }`}
    >
      <p
        className={`font-mono text-xs uppercase tracking-[0.18em] ${
          accent ? "text-accent" : "text-muted"
        }`}
      >
        {label}
      </p>
      <div className="mt-3 flex flex-wrap items-center justify-center gap-x-3 gap-y-1.5 font-mono text-sm text-faint">
        {items.map((item, i) => (
          <span key={item} className="inline-flex items-center gap-3">
            {i > 0 && <span className="text-border-strong">·</span>}
            <span className={accent ? "text-fg" : undefined}>{item}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

export function Architecture() {
  return (
    <Section
      id="architecture"
      eyebrow="Architecture"
      title="A single layer, between frameworks and tools."
    >
      <Reveal className="mx-auto mt-14 max-w-lg" delay={60}>
        <div className="flex flex-col items-center">
          <Layer label="AI Frameworks" items={["LangChain", "MCP", "custom agents"]} />
          <ArrowDown className="my-3 text-faint" />
          <Layer label="Aegize Runtime" items={RUNTIME_LAYERS} accent />
          <ArrowDown className="my-3 text-faint" />
          <Layer label="Tools" items={["shell", "email", "databases", "APIs", "payments"]} />
        </div>
      </Reveal>
    </Section>
  );
}
