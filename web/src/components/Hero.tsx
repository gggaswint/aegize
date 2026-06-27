import { DOCS_URL, GITHUB_URL } from "@/lib/links";
import { Button } from "./Button";
import { ArrowRight, GitHubIcon } from "./icons";
import { Logo } from "./Logo";

export function Hero() {
  return (
    <section
      id="top"
      className="relative mx-auto max-w-4xl px-6 pb-20 pt-20 text-center md:pb-28 md:pt-28"
    >
      <div className="rise flex justify-center" style={{ animationDelay: "0ms" }}>
        <Logo height={88} priority />
      </div>

      <p
        className="rise mt-11 font-mono text-xs uppercase tracking-[0.22em] text-accent"
        style={{ animationDelay: "90ms" }}
      >
        The trust layer for autonomous AI
      </p>

      <h1
        className="rise mt-6 text-balance text-4xl font-medium leading-[1.04] tracking-tight text-fg sm:text-5xl md:text-6xl"
        style={{ animationDelay: "170ms" }}
      >
        Infrastructure for
        <br className="hidden sm:block" /> autonomous AI agents.
      </h1>

      <p
        className="rise mx-auto mt-7 max-w-2xl text-pretty text-lg leading-relaxed text-muted"
        style={{ animationDelay: "250ms" }}
      >
        Aegize is the runtime layer between autonomous AI agents and the tools they use —
        providing identity, policy, permissions, approvals, audit logging, observability, and
        runtime governance for every AI action.
      </p>

      <div
        className="rise mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row"
        style={{ animationDelay: "330ms" }}
      >
        <Button href={GITHUB_URL} external>
          <GitHubIcon />
          View on GitHub
        </Button>
        <Button href={DOCS_URL} variant="secondary" external>
          Documentation
          <ArrowRight className="transition-transform duration-200 group-hover:translate-x-0.5" />
        </Button>
      </div>
    </section>
  );
}
