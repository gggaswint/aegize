import { Reveal } from "./Reveal";
import { Section } from "./Section";

const CAPABILITIES = [
  "execute code",
  "call APIs",
  "modify databases",
  "access files",
  "send email",
];

export function Why() {
  return (
    <Section
      id="why"
      eyebrow="Why"
      title="AI agents are evolving from conversations to actions."
    >
      <Reveal className="mt-10 max-w-2xl" delay={60}>
        <p className="text-pretty text-lg leading-relaxed text-muted">
          Modern agents no longer just answer questions. They take actions in the systems you
          run:
        </p>

        <ul className="mt-7 flex flex-wrap gap-2.5">
          {CAPABILITIES.map((c) => (
            <li
              key={c}
              className="rounded-full border border-border-strong bg-surface/50 px-3.5 py-1.5 font-mono text-sm text-fg"
            >
              {c}
            </li>
          ))}
        </ul>

        <p className="mt-8 text-pretty text-lg leading-relaxed text-fg">
          As they become increasingly capable, organizations need a runtime layer they can
          trust — one that decides what every agent is allowed to do, and keeps a record of it.
        </p>
      </Reveal>
    </Section>
  );
}
