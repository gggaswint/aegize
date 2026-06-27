import {
  ApprovalIcon,
  AuditIcon,
  IdentityIcon,
  ObservabilityIcon,
  PermissionsIcon,
  PolicyIcon,
} from "./icons";
import { Reveal } from "./Reveal";
import { Section } from "./Section";

const FEATURES = [
  {
    icon: IdentityIcon,
    title: "Identity",
    body: "A durable, attributable identity for every agent — owner, environment, and metadata.",
  },
  {
    icon: PolicyIcon,
    title: "Policy Engine",
    body: "Declarative YAML policy, versioned in source control and enforced deterministically on every call.",
  },
  {
    icon: PermissionsIcon,
    title: "Permissions",
    body: "Scope each agent to the exact tools and operations it is allowed to use. Default deny.",
  },
  {
    icon: ApprovalIcon,
    title: "Approval Workflows",
    body: "Route high-impact actions to a human for review before they execute.",
  },
  {
    icon: AuditIcon,
    title: "Audit Logging",
    body: "An append-only record of every attempt and outcome — allowed, denied, gated, or failed.",
  },
  {
    icon: ObservabilityIcon,
    title: "Observability",
    body: "See what agents attempt, in real time, across every environment you operate.",
  },
];

export function Features() {
  return (
    <Section
      id="features"
      eyebrow="Capabilities"
      title="One runtime, the full governance surface."
    >
      <div className="mt-14 grid gap-px overflow-hidden rounded-2xl border border-border bg-border sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((f, i) => (
          <Reveal key={f.title} delay={(i % 3) * 80}>
            <article className="group h-full bg-surface/40 p-7 transition-colors duration-300 hover:bg-surface-2">
              <span className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-border-strong bg-bg text-accent transition-colors duration-300 group-hover:border-accent/40">
                <f.icon />
              </span>
              <h3 className="mt-5 text-lg font-medium tracking-tight text-fg">{f.title}</h3>
              <p className="mt-2.5 text-pretty text-sm leading-relaxed text-muted">{f.body}</p>
            </article>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
