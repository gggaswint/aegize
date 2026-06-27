"use client";

import { useEffect, useRef } from "react";

/**
 * The runtime pipeline animation.
 *
 * One AI action flows through the runtime as an SVG pulse. Each stage lights up
 * as it is reached. Approval pauses the flow; a denied policy stops it; an
 * allowed action runs to the filesystem. It loops forever.
 *
 * Motion is driven imperatively with requestAnimationFrame (SVG attributes are
 * mutated directly) so there are no React re-renders during the animation — a
 * smooth 60fps with no layout thrash. With JavaScript disabled, the SVG still
 * renders as a complete, labelled diagram of the runtime.
 */

const STAGES = [
  "AI Agent",
  "Identity",
  "Policy",
  "Permissions",
  "Approval",
  "Execution",
  "Audit",
  "Filesystem",
] as const;

// geometry (SVG user units)
const W = 300;
const TOP = 30;
const GAP = 68;
const COUNT = STAGES.length;
const BOTTOM = TOP + GAP * (COUNT - 1);
const H = BOTTOM + 30;
const RAIL_X = 46;
const TOTAL = BOTTOM - TOP;

// palette (matches the site tokens)
const BG = "#07090e";
const DIM_RING = "#283042";
const DIM_LABEL = "#8b97a8";
const LIT_LABEL = "#e9eef5";
const ACCENT = "#5b9dff";
const GREEN = "#46c25a";
const AMBER = "#e0a93b";
const RED = "#f0685f";

const SPEED = 118; // user-units per second

type Kind = "allowed" | "approval" | "denied";
type Scenario = {
  kind: Kind;
  call: string;
  stopIdx: number;
  pauseIdx: number | null;
};

const SCENARIOS: Scenario[] = [
  { kind: "allowed", call: "web_search()", stopIdx: 7, pauseIdx: null },
  { kind: "approval", call: "send_email()", stopIdx: 7, pauseIdx: 4 },
  { kind: "denied", call: "execute_shell()", stopIdx: 2, pauseIdx: null },
];

const yAt = (i: number) => TOP + i * GAP;

export function HeroPipeline() {
  const pulseRef = useRef<SVGGElement>(null);
  const coreRef = useRef<SVGCircleElement>(null);
  const haloRef = useRef<SVGCircleElement>(null);
  const trailRef = useRef<SVGLineElement>(null);
  const ringsRef = useRef<(SVGCircleElement | null)[]>([]);
  const dotsRef = useRef<(SVGCircleElement | null)[]>([]);
  const labelsRef = useRef<(SVGTextElement | null)[]>([]);
  const callRef = useRef<HTMLSpanElement>(null);
  const chipRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const status = (sm: State, sc: Scenario): string => {
      if (sm.phase === "pause") return AMBER;
      if (sm.phase === "done" || sm.phase === "reset")
        return sc.kind === "denied" ? RED : GREEN;
      return ACCENT;
    };

    const setChip = (text: string, color: string, on: boolean) => {
      const el = chipRef.current;
      if (!el) return;
      el.textContent = text;
      el.style.color = on ? color : DIM_LABEL;
      el.style.borderColor = on ? color : "var(--color-border)";
      el.style.opacity = on ? "1" : "0.4";
      el.style.backgroundColor = on
        ? "color-mix(in srgb, currentColor 12%, transparent)"
        : "transparent";
    };

    const paint = (sm: State) => {
      const sc = SCENARIOS[sm.scenario];
      const color = status(sm, sc);
      const len = Math.max(0, sm.len);
      const shown = len > 1 && sm.phase !== "reset";

      // pulse
      if (pulseRef.current) {
        pulseRef.current.setAttribute("transform", `translate(${RAIL_X} ${TOP + len})`);
        pulseRef.current.style.opacity = shown ? "1" : "0";
      }
      coreRef.current?.setAttribute("fill", color);
      haloRef.current?.setAttribute("fill", color);

      // trail (lit rail)
      if (trailRef.current) {
        trailRef.current.style.strokeDashoffset = String(TOTAL - len);
        trailRef.current.setAttribute("stroke", sm.phase === "flow" ? ACCENT : color);
      }

      // nodes
      const active = Math.min(COUNT - 1, Math.round(len / GAP));
      for (let i = 0; i < COUNT; i++) {
        const reached = len >= i * GAP - GAP * 0.18;
        const isActive = shown && i === active;
        const isTerminal = sm.phase === "done" && i === sc.stopIdx;
        const focus = isActive || isTerminal;
        const c = focus ? color : reached ? ACCENT : DIM_RING;

        const ring = ringsRef.current[i];
        const dot = dotsRef.current[i];
        const label = labelsRef.current[i];
        if (ring) {
          ring.setAttribute("stroke", c);
          ring.setAttribute("r", focus ? "6.5" : "5");
          ring.style.filter = focus ? "url(#glow)" : "none";
        }
        if (dot) {
          dot.setAttribute("fill", focus ? c : reached ? ACCENT : BG);
          dot.style.opacity = reached ? "1" : "0";
        }
        label?.setAttribute("fill", reached ? LIT_LABEL : DIM_LABEL);
      }
    };

    type Phase = "flow" | "pause" | "done" | "reset";
    type State = {
      scenario: number;
      len: number;
      phase: Phase;
      t0: number;
      paused: boolean;
      last: number;
      capStr: string;
      chipStr: string;
    };

    const sm: State = {
      scenario: 0,
      len: 0,
      phase: "flow",
      t0: 0,
      paused: false,
      last: 0,
      capStr: "",
      chipStr: "",
    };

    // static, complete diagram when motion is reduced
    if (reduce) {
      sm.len = TOTAL;
      sm.phase = "done";
      paint({ ...sm, scenario: 0 });
      if (callRef.current) callRef.current.textContent = "every action, governed";
      setChip("audited", GREEN, true);
      return;
    }

    let raf = 0;

    const syncText = (sm: State) => {
      const sc = SCENARIOS[sm.scenario];
      if (sm.capStr !== sc.call && callRef.current) {
        callRef.current.textContent = sc.call;
        sm.capStr = sc.call;
      }
      let chip = "evaluating";
      let color = DIM_LABEL;
      let on = false;
      if (sm.phase === "pause") {
        chip = "approval required";
        color = AMBER;
        on = true;
      } else if (sm.phase === "done" || sm.phase === "reset") {
        on = true;
        if (sc.kind === "denied") {
          chip = "denied";
          color = RED;
        } else {
          chip = "allowed";
          color = GREEN;
        }
      }
      const key = `${chip}|${on}`;
      if (sm.chipStr !== key) {
        setChip(chip, color, on);
        sm.chipStr = key;
      }
    };

    const frame = (t: number) => {
      if (!sm.last) sm.last = t;
      const dt = Math.min(0.05, (t - sm.last) / 1000);
      sm.last = t;
      const sc = SCENARIOS[sm.scenario];
      const stopLen = sc.stopIdx * GAP;
      const pauseLen = sc.pauseIdx != null ? sc.pauseIdx * GAP : null;

      if (sm.phase === "flow") {
        sm.len += SPEED * dt;
        if (pauseLen != null && !sm.paused && sm.len >= pauseLen) {
          sm.len = pauseLen;
          sm.phase = "pause";
          sm.t0 = t;
        } else if (sm.len >= stopLen) {
          sm.len = stopLen;
          sm.phase = "done";
          sm.t0 = t;
        }
      } else if (sm.phase === "pause") {
        if (t - sm.t0 > 1250) {
          sm.paused = true;
          sm.phase = "flow";
        }
      } else if (sm.phase === "done") {
        if (t - sm.t0 > (sc.kind === "denied" ? 1500 : 1350)) {
          sm.phase = "reset";
          sm.t0 = t;
        }
      } else if (sm.phase === "reset") {
        if (t - sm.t0 > 460) {
          sm.scenario = (sm.scenario + 1) % SCENARIOS.length;
          sm.len = 0;
          sm.paused = false;
          sm.phase = "flow";
        }
      }

      syncText(sm);
      paint(sm);
      raf = requestAnimationFrame(frame);
    };

    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, []);

  return (
    <div className="mx-auto w-full max-w-md">
      <div className="mb-5 flex items-center justify-between gap-3 font-mono text-sm">
        <span className="truncate">
          <span className="text-faint">agent</span>{" "}
          <span className="text-faint">&#9656;</span>{" "}
          <span ref={callRef} className="text-fg">
            web_search()
          </span>
        </span>
        <span
          ref={chipRef}
          className="shrink-0 rounded-full border px-2.5 py-1 text-xs transition-colors duration-300"
          style={{ color: DIM_LABEL, borderColor: "var(--color-border)", opacity: 0.4 }}
        >
          evaluating
        </span>
      </div>

      <div className="rounded-2xl border border-border bg-surface/40 px-3 py-2">
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="h-auto w-full"
          role="img"
          aria-label="Aegize runtime pipeline. An AI action flows in order through AI Agent, Identity, Policy, Permissions, Approval, Execution, Audit, and Filesystem. Approval pauses the flow; a denied policy stops it; an allowed action runs to completion. Every step is recorded."
        >
          <defs>
            <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
              <feGaussianBlur stdDeviation="2.6" result="b" />
              <feMerge>
                <feMergeNode in="b" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* dim full rail */}
          <line
            x1={RAIL_X}
            y1={TOP}
            x2={RAIL_X}
            y2={BOTTOM}
            stroke={DIM_RING}
            strokeWidth={1}
          />
          {/* lit trail */}
          <line
            ref={trailRef}
            x1={RAIL_X}
            y1={TOP}
            x2={RAIL_X}
            y2={BOTTOM}
            stroke={ACCENT}
            strokeWidth={2}
            strokeLinecap="round"
            style={{ strokeDasharray: TOTAL, strokeDashoffset: TOTAL }}
          />

          {/* nodes */}
          {STAGES.map((stage, i) => (
            <g key={stage}>
              <circle
                ref={(el) => {
                  ringsRef.current[i] = el;
                }}
                cx={RAIL_X}
                cy={yAt(i)}
                r={5}
                fill={BG}
                stroke={DIM_RING}
                strokeWidth={1.5}
              />
              <circle
                ref={(el) => {
                  dotsRef.current[i] = el;
                }}
                cx={RAIL_X}
                cy={yAt(i)}
                r={2.3}
                fill={BG}
                style={{ opacity: 0 }}
              />
              <text
                ref={(el) => {
                  labelsRef.current[i] = el;
                }}
                x={RAIL_X + 24}
                y={yAt(i)}
                dominantBaseline="central"
                fontSize={12.5}
                fill={DIM_LABEL}
                style={{ fontFamily: "var(--font-mono)" }}
              >
                {stage}
              </text>
              <text
                x={W - 6}
                y={yAt(i)}
                textAnchor="end"
                dominantBaseline="central"
                fontSize={9}
                fill="#5a6478"
                style={{ fontFamily: "var(--font-mono)" }}
              >
                {String(i + 1).padStart(2, "0")}
              </text>
            </g>
          ))}

          {/* pulse */}
          <g ref={pulseRef} style={{ opacity: 0 }} aria-hidden>
            <circle ref={haloRef} r={9} fill={ACCENT} opacity={0.18} />
            <circle ref={coreRef} r={4} fill={ACCENT} />
          </g>
        </svg>
      </div>

      <div className="mt-4 flex items-center justify-center gap-5 font-mono text-[0.72rem] text-muted">
        <Legend color={GREEN} label="allowed" />
        <Legend color={AMBER} label="approval" />
        <Legend color={RED} label="denied" />
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
