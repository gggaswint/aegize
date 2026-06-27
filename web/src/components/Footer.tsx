import { CONTACT_EMAIL, DOCS_URL, GITHUB_URL, LICENSE_URL } from "@/lib/links";
import { Logo } from "./Logo";

const COLUMNS = [
  {
    heading: "Product",
    links: [
      { label: "GitHub", href: GITHUB_URL, external: true },
      { label: "Documentation", href: DOCS_URL, external: true },
    ],
  },
  {
    heading: "Project",
    links: [
      { label: "License", href: LICENSE_URL, external: true },
      { label: "Contact", href: CONTACT_EMAIL, external: false },
    ],
  },
];

export function Footer() {
  return (
    <footer className="relative border-t border-border">
      <div className="mx-auto grid max-w-6xl gap-12 px-6 py-16 sm:grid-cols-2 md:grid-cols-[1.5fr_1fr_1fr]">
        <div className="max-w-xs">
          <Logo withWordmark height={24} />
          <p className="mt-4 text-pretty text-sm leading-relaxed text-muted">
            Infrastructure for autonomous AI agents.
          </p>
          <p className="mt-2 font-mono text-xs text-faint">The trust layer for autonomous AI.</p>
        </div>

        {COLUMNS.map((col) => (
          <nav key={col.heading} aria-label={col.heading}>
            <h2 className="font-mono text-xs uppercase tracking-[0.16em] text-faint">
              {col.heading}
            </h2>
            <ul className="mt-4 space-y-3">
              {col.links.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    target={link.external ? "_blank" : undefined}
                    rel={link.external ? "noreferrer" : undefined}
                    className="text-sm text-muted transition-colors hover:text-fg"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        ))}
      </div>

      <div className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-3 border-t border-border px-6 py-6 font-mono text-xs text-faint sm:flex-row sm:items-center">
        <span>© {new Date().getFullYear()} Aegize</span>
        <span>MIT licensed · Built in the open</span>
      </div>
    </footer>
  );
}
