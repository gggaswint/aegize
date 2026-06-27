import type { ReactNode } from "react";
import { Reveal } from "./Reveal";

export function Section({
  id,
  eyebrow,
  title,
  intro,
  children,
  className = "",
}: {
  id?: string;
  eyebrow?: string;
  title?: string;
  intro?: ReactNode;
  children?: ReactNode;
  className?: string;
}) {
  return (
    <section
      id={id}
      aria-labelledby={id && title ? `${id}-heading` : undefined}
      className={`relative mx-auto w-full max-w-6xl scroll-mt-24 px-6 py-24 md:py-32 ${className}`}
    >
      {(eyebrow || title || intro) && (
        <Reveal className="mx-auto max-w-2xl">
          {eyebrow && (
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-accent">
              {eyebrow}
            </p>
          )}
          {title && (
            <h2
              id={id ? `${id}-heading` : undefined}
              className="mt-4 text-balance text-3xl font-medium leading-tight tracking-tight text-fg md:text-[2.6rem]"
            >
              {title}
            </h2>
          )}
          {intro && (
            <p className="mt-5 text-pretty text-lg leading-relaxed text-muted">{intro}</p>
          )}
        </Reveal>
      )}
      {children}
    </section>
  );
}
