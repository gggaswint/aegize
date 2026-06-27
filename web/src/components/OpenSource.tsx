import { GITHUB_URL } from "@/lib/links";
import { Button } from "./Button";
import { GitHubIcon } from "./icons";
import { Reveal } from "./Reveal";

export function OpenSource() {
  return (
    <section className="relative mx-auto w-full max-w-6xl px-6 py-24 md:py-28">
      <Reveal>
        <div className="relative overflow-hidden rounded-2xl border border-border bg-surface/40 px-8 py-14 text-center md:px-16 md:py-20">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-accent">Open source</p>
          <h2 className="mx-auto mt-4 max-w-2xl text-balance text-3xl font-medium tracking-tight text-fg md:text-4xl">
            Built in the open, for developers.
          </h2>
          <p className="mx-auto mt-5 max-w-xl text-pretty text-lg leading-relaxed text-muted">
            Aegize is open source and MIT licensed. Read the code, run it locally, and shape
            where the runtime goes next.
          </p>
          <div className="mt-9 flex justify-center">
            <Button href={GITHUB_URL} external>
              <GitHubIcon />
              View on GitHub
            </Button>
          </div>
        </div>
      </Reveal>
    </section>
  );
}
