import { Reveal } from "./Reveal";
import { RuntimeSandbox } from "./sandbox/RuntimeSandbox";
import { Section } from "./Section";

export function TryTheRuntime() {
  return (
    <Section
      id="try-the-runtime"
      eyebrow="Sandbox"
      title="Try the runtime."
      intro="Choose an action and watch it pass through Aegize before it reaches a tool."
    >
      <Reveal className="mt-10" delay={60}>
        <p className="mb-6 font-mono text-xs text-faint">
          This is a local simulation. No real commands, emails, payments, or API calls are executed.
        </p>
        <RuntimeSandbox />
        <div className="mt-6 text-center">
          <a
            href="/playground"
            className="inline-flex items-center gap-1.5 font-mono text-sm text-accent transition-opacity hover:opacity-80"
          >
            Open the full playground &rarr;
          </a>
        </div>
      </Reveal>
    </Section>
  );
}
