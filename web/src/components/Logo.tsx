import Image from "next/image";

const RATIO = 3154 / 1874; // intrinsic logomark aspect

export function Logo({
  height = 26,
  withWordmark = false,
  priority = false,
}: {
  height?: number;
  withWordmark?: boolean;
  priority?: boolean;
}) {
  const width = Math.round(height * RATIO);
  return (
    <span className="inline-flex items-center gap-2.5 align-middle">
      <Image
        src="/logomark.png"
        alt={withWordmark ? "" : "Aegize"}
        width={width}
        height={height}
        priority={priority}
        aria-hidden={withWordmark || undefined}
      />
      {withWordmark && (
        <span className="font-mono text-[0.98rem] font-medium tracking-tight text-fg">
          aegize
        </span>
      )}
    </span>
  );
}
