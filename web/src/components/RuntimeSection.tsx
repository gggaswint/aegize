import { HeroPipeline } from "./HeroPipeline";
import { Reveal } from "./Reveal";

const VERDICTS = [
  { call: "web_search", verdict: "allowed", color: "var(--color-allow)" },
  { call: "send_email", verdict: "approval required", color: "var(--color-approval)" },
  { call: "execute_shell", verdict: "denied", color: "var(--color-deny)" },
];

export function RuntimeSection() {
  return (
    <section
      id="runtime"
      aria-labelledby="runtime-heading"
      className="relative mx-auto w-full max-w-6xl scroll-mt-24 px-6 py-24 md:py-32"
    >
      <div className="grid items-center gap-14 md:grid-cols-2 md:gap-20">
        <Reveal>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-accent">Runtime</p>
          <h2
            id="runtime-heading"
            className="mt-4 text-balance text-3xl font-medium leading-tight tracking-tight text-fg md:text-[2.6rem]"
          >
            Every action passes through Aegize before it runs.
          </h2>
          <p className="mt-5 text-pretty text-lg leading-relaxed text-muted">
            Identity, policy, permissions, approval, execution, audit — in order, on every call.
            Allowed actions proceed. High-impact actions wait for a human. Denied actions never
            execute. All of it is recorded.
          </p>

          <ul className="mt-8 space-y-3">
            {VERDICTS.map((v) => (
              <li key={v.call} className="flex items-center gap-3 font-mono text-sm">
                <span
                  className="h-1.5 w-1.5 shrink-0 rounded-full"
                  style={{ backgroundColor: v.color }}
                />
                <span className="text-fg">{v.call}</span>
                <span className="text-faint">&rarr;</span>
                <span style={{ color: v.color }}>{v.verdict}</span>
              </li>
            ))}
          </ul>
        </Reveal>

        <Reveal delay={120}>
          <HeroPipeline />
        </Reveal>
      </div>
    </section>
  );
}
