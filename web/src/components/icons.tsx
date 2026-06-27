import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

const base = {
  width: 20,
  height: 20,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.6,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export function GitHubIcon(props: IconProps) {
  return (
    <svg width={18} height={18} viewBox="0 0 24 24" fill="currentColor" aria-hidden {...props}>
      <path d="M12 1.5A10.5 10.5 0 0 0 1.5 12a10.5 10.5 0 0 0 7.18 9.96c.52.1.71-.23.71-.5v-1.9c-2.92.63-3.54-1.25-3.54-1.25-.48-1.21-1.17-1.54-1.17-1.54-.95-.65.07-.64.07-.64 1.06.08 1.62 1.09 1.62 1.09.94 1.6 2.46 1.14 3.06.87.1-.68.37-1.14.67-1.4-2.33-.27-4.78-1.17-4.78-5.18 0-1.15.41-2.08 1.08-2.82-.11-.27-.47-1.34.1-2.79 0 0 .88-.28 2.88 1.07a9.96 9.96 0 0 1 5.24 0c2-1.35 2.88-1.07 2.88-1.07.57 1.45.21 2.52.1 2.79.67.74 1.08 1.67 1.08 2.82 0 4.02-2.46 4.9-4.8 5.16.38.33.71.97.71 1.96v2.9c0 .28.19.61.72.5A10.5 10.5 0 0 0 22.5 12 10.5 10.5 0 0 0 12 1.5Z" />
    </svg>
  );
}

export function ArrowRight(props: IconProps) {
  return (
    <svg {...base} width={16} height={16} aria-hidden {...props}>
      <path d="M5 12h14M13 6l6 6-6 6" />
    </svg>
  );
}

export function ArrowDown(props: IconProps) {
  return (
    <svg {...base} aria-hidden {...props}>
      <path d="M12 5v14M6 13l6 6 6-6" />
    </svg>
  );
}

/* ---- feature icons (minimal line work) ---- */

export function IdentityIcon(props: IconProps) {
  return (
    <svg {...base} aria-hidden {...props}>
      <circle cx="12" cy="9" r="3.2" />
      <path d="M5.5 19a6.5 6.5 0 0 1 13 0" />
      <path d="M3 7V5.5A2.5 2.5 0 0 1 5.5 3H7M17 3h1.5A2.5 2.5 0 0 1 21 5.5V7" />
    </svg>
  );
}

export function PolicyIcon(props: IconProps) {
  return (
    <svg {...base} aria-hidden {...props}>
      <path d="M12 3 4 6v5c0 4.5 3.2 7.8 8 9.5 4.8-1.7 8-5 8-9.5V6l-8-3Z" />
      <path d="m9 11.5 2 2 4-4.5" />
    </svg>
  );
}

export function PermissionsIcon(props: IconProps) {
  return (
    <svg {...base} aria-hidden {...props}>
      <circle cx="8" cy="12" r="3" />
      <path d="M11 12h9l-2.2 2.2M16 12v3" />
    </svg>
  );
}

export function ApprovalIcon(props: IconProps) {
  return (
    <svg {...base} aria-hidden {...props}>
      <path d="M5 12.5 10 17l9-10" />
      <path d="M3 8.5v8A2.5 2.5 0 0 0 5.5 19h13" opacity="0.4" />
    </svg>
  );
}

export function AuditIcon(props: IconProps) {
  return (
    <svg {...base} aria-hidden {...props}>
      <rect x="4" y="3.5" width="16" height="17" rx="2" />
      <path d="M8 8h8M8 12h8M8 16h5" />
    </svg>
  );
}

export function ObservabilityIcon(props: IconProps) {
  return (
    <svg {...base} aria-hidden {...props}>
      <path d="M3 12h3l2.5-6 4 13L15 8l2 4h4" />
    </svg>
  );
}
