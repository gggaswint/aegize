"use client";

import { useEffect, useState } from "react";

const STAGES = [
  "AI Agent",
  "Identity",
  "Policy",
  "Permissions",
  "Approval",
  "Execution",
  "Audit",
  "Tools",
] as const;

type Status = "flow" | "allow" | "approval" | "deny";

type Scenario = {
  call: string;
  verdict: string;
  status: Status;
  target: number; // last stage the pulse reaches
  pauseAt: number | null; // stage where it holds (approval)
};

const SCENARIOS: Scenario[] = [
  { call: "web_search()", verdict: "allowed", status: "allow", target: 7, pauseAt: null },
  { call: "send_email()", verdict: "approval required", status: "approval", target: 4, pauseAt: 4 },
  { call: "execute_shell()", verdict: "denied", status: "deny", target: 2, pauseAt: null },
];

const ROW = 64;
const RAIL_X = 23;
const STEP_MS = 360;
const AUDIT_INDEX = 6;

const COLOR: Record<Status, string> = {
  flow: "var(--color-accent)",
  allow: "var(--color-allow)",
  approval: "var(--color-approval)",
  deny: "var(--color-deny)",
};

export function RuntimePipeline() {
  const [active, setActive] = useState(-1);
  const [status, setStatus] = useState<Status>("flow");
  const [scenario, setScenario] = useState<Scenario>(SCENARIOS[0]);
  const [verdict, setVerdict] = useState<{ label: string; status: Status } | null>(null);
  const [auditBlip, setAuditBlip] = useState(false);
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (mq.matches) {
      setReduced(true);
      setActive(7);
      setStatus("allow");
      setVerdict({ label: "governed", status: "allow" });
      return;
    }

    let cancelled = false;
    const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

    async function run() {
      let s = 0;
      while (!cancelled) {
        const sc = SCENARIOS[s % SCENARIOS.length];
        setScenario(sc);
        setVerdict(null);
        setAuditBlip(false);
        setActive(-1);
        setStatus("flow");
        await sleep(520);
        if (cancelled) return;

        for (let i = 0; i <= sc.target; i++) {
          setActive(i);
          if (i === sc.pauseAt) {
            setStatus("approval");
            await sleep(1250);
          } else {
            await sleep(STEP_MS);
          }
          if (cancelled) return;
        }

        setStatus(sc.status);
        await sleep(260);
        if (cancelled) return;
        setAuditBlip(true); // every decision is recorded
        setVerdict({ label: sc.verdict, status: sc.status });
        await sleep(1650);
        if (cancelled) return;
        setAuditBlip(false);
        await sleep(680);
        s += 1;
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, []);

  const pulseTop = active >= 0 ? active * ROW + ROW / 2 : ROW / 2;
  const progressH = active > 0 ? active * ROW : 0;
  const pulseColor = COLOR[status];

  return (
    <div className="mx-auto w-full max-w-md">
      {/* caption */}
      <div className="mb-6 flex items-center justify-between gap-3 font-mono text-sm">
        <span className="truncate">
          <span className="text-faint">agent</span>{" "}
          <span className="text-faint">&#9656;</span>{" "}
          <span className="text-fg">{scenario.call}</span>
        </span>
        <span
          className="shrink-0 rounded-full border px-2.5 py-1 text-xs transition-all duration-500"
          style={{
            color: verdict ? COLOR[verdict.status] : "var(--color-faint)",
            borderColor: verdict ? COLOR[verdict.status] : "var(--color-border)",
            opacity: verdict ? 1 : 0.35,
            backgroundColor: verdict ? "color-mix(in srgb, currentColor 10%, transparent)" : "transparent",
          }}
        >
          {verdict ? verdict.label : "evaluating"}
        </span>
      </div>

      {/* pipeline */}
      <div
        className="relative rounded-2xl border border-border bg-surface/40 px-6 py-7"
        role="img"
        aria-label="Aegize runtime pipeline: an AI agent's action flows through identity, policy, permissions, approval, execution, audit, and tools. Approval pauses; a denied action stops."
      >
        <div className="relative" style={{ height: ROW * STAGES.length }}>
          {/* rail */}
          <div
            className="absolute w-px bg-border-strong"
            style={{ left: RAIL_X, top: ROW / 2, bottom: ROW / 2 }}
          />
          {/* progress */}
          <div
            className="absolute w-px transition-[height] duration-300 ease-out"
            style={{
              left: RAIL_X,
              top: ROW / 2,
              height: progressH,
              background: `linear-gradient(to bottom, var(--color-accent), ${pulseColor})`,
              opacity: 0.85,
            }}
          />
          {/* pulse */}
          <div
            className="absolute transition-all duration-300 ease-out"
            style={{
              left: RAIL_X,
              top: pulseTop,
              transform: "translate(-50%, -50%)",
              opacity: active >= 0 ? 1 : 0,
            }}
            aria-hidden
          >
            <span
              className="block h-2.5 w-2.5 rounded-full"
              style={{
                color: pulseColor,
                backgroundColor: pulseColor,
                animation: reduced ? "none" : "pulse-glow 1.6s ease-in-out infinite",
              }}
            />
          </div>

          {/* nodes */}
          <ul className="relative">
            {STAGES.map((stage, i) => {
              const lit = i <= active;
              const isActive = i === active;
              const isAuditBlip = auditBlip && i === AUDIT_INDEX;
              const markColor = isActive || isAuditBlip ? pulseColor : lit ? "var(--color-accent)" : "var(--color-border-strong)";
              return (
                <li key={stage} className="relative flex items-center" style={{ height: ROW }}>
                  {/* marker */}
                  <span
                    className="absolute transition-all duration-300"
                    style={{ left: RAIL_X, top: "50%", transform: "translate(-50%, -50%)" }}
                    aria-hidden
                  >
                    <span
                      className="block rounded-full border transition-all duration-300"
                      style={{
                        width: isActive || isAuditBlip ? 13 : 9,
                        height: isActive || isAuditBlip ? 13 : 9,
                        borderColor: markColor,
                        backgroundColor: isActive || isAuditBlip ? markColor : lit ? "color-mix(in srgb, var(--color-accent) 22%, transparent)" : "var(--color-bg)",
                        boxShadow: isActive || isAuditBlip ? `0 0 14px 1px ${markColor}` : "none",
                      }}
                    />
                  </span>

                  {/* label */}
                  <div className="flex w-full items-center justify-between pl-12">
                    <span
                      className="font-mono text-[0.92rem] transition-colors duration-300"
                      style={{
                        color: isActive
                          ? "var(--color-fg)"
                          : lit
                            ? "var(--color-fg)"
                            : "var(--color-faint)",
                      }}
                    >
                      {stage}
                    </span>
                    <span className="font-mono text-[0.7rem] tabular-nums text-faint">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      </div>

      {/* legend */}
      <div className="mt-5 flex items-center justify-center gap-5 font-mono text-[0.72rem] text-muted">
        <Legend color="var(--color-allow)" label="allowed" />
        <Legend color="var(--color-approval)" label="approval" />
        <Legend color="var(--color-deny)" label="denied" />
      </div>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: color }} />
      {label}
    </span>
  );
}
