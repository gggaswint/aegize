import { Reveal } from "./Reveal";
import { Section } from "./Section";

export function Architecture() {
  return (
    <Section
      id="architecture"
      eyebrow="Architecture"
      title="A single layer, between frameworks and tools."
      intro="AI frameworks send tool calls into Aegize. Only allowed actions reach the tools they use — every AI action passes through Aegize first."
    >
      <Reveal className="mt-12" delay={60}>
        {/* Canonical diagram — assets/architecture.svg, mirrored into public/. */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="/architecture.svg"
          alt="How Aegize fits into an AI agent stack: AI frameworks send tool calls into the Aegize runtime (identity, policy engine, permissions, approval workflows, audit logging, observability); only allowed actions reach tools. Every AI action passes through Aegize before reaching the outside world."
          width={1400}
          height={988}
          loading="lazy"
          decoding="async"
          className="mx-auto block h-auto w-full max-w-4xl rounded-xl border border-border-strong"
        />
      </Reveal>
    </Section>
  );
}
