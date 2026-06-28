import { GITHUB_URL } from "@/lib/links";
import { Footer } from "./Footer";
import { GitHubIcon } from "./icons";
import { Logo } from "./Logo";
import { RuntimeSandbox } from "./sandbox/RuntimeSandbox";

export function SandboxPage() {
  return (
    <>
      <header className="sticky top-0 z-40 border-b border-border/70 bg-bg/70 backdrop-blur-xl">
        <nav className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <a href="/" aria-label="Aegize, home" className="shrink-0">
            <Logo withWordmark height={22} priority />
          </a>
          <div className="flex items-center gap-4">
            <a
              href="/"
              className="font-mono text-[0.72rem] uppercase tracking-[0.14em] text-muted transition-colors hover:text-fg"
            >
              Home
            </a>
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-lg border border-border-strong bg-surface/60 px-3 py-1.5 text-sm text-fg transition-colors hover:border-faint hover:bg-surface-2"
            >
              <GitHubIcon />
              <span className="hidden sm:inline">GitHub</span>
            </a>
          </div>
        </nav>
      </header>

      <main id="main" className="mx-auto max-w-6xl px-6 py-16 md:py-20">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-accent">Sandbox</p>
        <h1 className="mt-4 text-balance text-4xl font-medium tracking-tight text-fg md:text-5xl">
          Try the runtime.
        </h1>
        <p className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-muted">
          Choose an action and watch it pass through Aegize before it reaches a tool.
        </p>
        <p className="mt-3 font-mono text-xs text-faint">
          This is a local simulation. No real commands, emails, payments, or API calls are executed.
        </p>

        <div className="mt-10">
          <RuntimeSandbox />
        </div>
      </main>

      <Footer />
    </>
  );
}
