import { Section } from "./Section";
import { Reveal } from "./Reveal";

export function DemoSection() {
  return (
    <Section
      id="demo"
      eyebrow="See it run"
      title="The same policy, in your terminal."
      intro="One agent makes three tool calls. Aegize allows the search, holds the email for approval, blocks the shell command — and writes an audit record for every attempt."
    >
      <Reveal className="mt-12" delay={80}>
        <figure className="mx-auto max-w-3xl overflow-hidden rounded-xl border border-border-strong bg-[#0d1117] shadow-2xl shadow-black/40">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3">
            <span className="h-3 w-3 rounded-full bg-[#ff5f56]" />
            <span className="h-3 w-3 rounded-full bg-[#ffbd2e]" />
            <span className="h-3 w-3 rounded-full bg-[#27c93f]" />
            <span className="ml-2 font-mono text-xs text-faint">aegize — agent session</span>
          </div>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/demo.gif"
            alt="Aegize terminal demo: an agent makes three tool calls — web search allowed, email approval required, shell command denied — each governed and audited."
            width={1000}
            height={500}
            loading="lazy"
            decoding="async"
            className="block h-auto w-full"
          />
        </figure>
      </Reveal>
    </Section>
  );
}
