import type { ReactNode } from "react";

type Variant = "primary" | "secondary";

const styles: Record<Variant, string> = {
  primary:
    "bg-fg text-bg hover:bg-white border border-transparent shadow-sm",
  secondary:
    "bg-surface/60 text-fg border border-border-strong hover:border-faint hover:bg-surface-2",
};

export function Button({
  href,
  children,
  variant = "primary",
  external = false,
}: {
  href: string;
  children: ReactNode;
  variant?: Variant;
  external?: boolean;
}) {
  const rel = external ? "noreferrer noopener" : undefined;
  const target = external ? "_blank" : undefined;
  return (
    <a
      href={href}
      target={target}
      rel={rel}
      className={`group inline-flex items-center justify-center gap-2 rounded-lg px-5 py-2.5 text-sm font-medium tracking-tight transition-colors duration-200 ${styles[variant]}`}
    >
      {children}
    </a>
  );
}
