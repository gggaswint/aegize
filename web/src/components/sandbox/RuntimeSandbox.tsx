"use client";

import { useEffect, useRef, useState } from "react";
import {
  AGENT_ID,
  type AuditEntry,
  OUTCOME,
  STAGES,
  TOOLS,
  type ToolDef,
} from "@/lib/sandbox";
import { AuditLog } from "./AuditLog";
import { PipelineStage, ROW_H, type StageStatus } from "./PipelineStage";
import { ToolButton } from "./ToolButton";

type Phase = "idle" | "running" | "resolved";

const START_MS = 380;
const STAGE_MS = 300;
const RESOLVE_MS = 260;

function nowTime(): string {
  const d = new Date();
  return [d.getHours(), d.getMinutes(), d.getSeconds()]
    .map((n) => String(n).padStart(2, "0"))
    .join(":");
}

export function RuntimeSandbox() {
  const [tool, setTool] = useState<ToolDef | null>(null);
  const [active, setActive] = useState(-1);
  const [phase, setPhase] = useState<Phase>("idle");
  const [audit, setAudit] = useState<AuditEntry[]>([]);

  const timers = useRef<number[]>([]);
  const auditId = useRef(0);

  const clearTimers = () => {
    timers.current.forEach((t) => clearTimeout(t));
    timers.current = [];
  };

  useEffect(() => clearTimers, []);

  function run(next: ToolDef) {
    if (phase === "running") return;
    clearTimers();
    setTool(next);
    setActive(-1);
    setPhase("running");

    const stop = next.stopIndex;
    let i = 0;
    const tick = () => {
      setActive(i);
      if (i >= stop) {
        timers.current.push(
          window.setTimeout(() => {
            setPhase("resolved");
            auditId.current += 1;
            const entry: AuditEntry = {
              id: auditId.current,
              time: nowTime(),
              agent: AGENT_ID,
              target: `${next.tool}.${next.operation}`,
              decision: next.decision,
              reason: next.reason,
            };
            setAudit((prev) => [entry, ...prev].slice(0, 8));
          }, RESOLVE_MS),
        );
        return;
      }
      i += 1;
      timers.current.push(window.setTimeout(tick, STAGE_MS));
    };
    timers.current.push(window.setTimeout(tick, START_MS));
  }

  function stageStatus(i: number): StageStatus {
    if (!tool || active < 0) return "idle";
    if (i > active) return "idle";
    if (i < active) return "passed";
    // i === active
    if (phase === "resolved" && i === tool.stopIndex) {
      if (tool.decision === "denied") return "blocked";
      if (tool.decision === "approval_required") return "pause";
      return "done";
    }
    return "active";
  }

  function sublabel(i: number): string | undefined {
    if (phase === "resolved" && tool && i === active && i === tool.stopIndex) {
      return OUTCOME[tool.decision].text;
    }
    return undefined;
  }

  const progressH = active >= 0 ? active * ROW_H : 0;
  const progressColor =
    phase === "resolved" && tool ? OUTCOME[tool.decision].color : "var(--color-accent)";

  const status =
    phase === "idle"
      ? { text: "Choose a tool to begin.", color: "var(--color-faint)" }
      : phase === "running"
        ? { text: "Evaluating…", color: "var(--color-accent)" }
        : tool
          ? OUTCOME[tool.decision]
          : { text: "", color: "var(--color-faint)" };

  return (
    <div className="rounded-2xl border border-border bg-surface/30 p-4 sm:p-6">
      <div className="grid grid-cols-1 gap-5 md:grid-cols-[200px_minmax(0,1fr)_220px]">
        {/* Left — AI Agent */}
        <div className="order-1 min-w-0 rounded-xl border border-border bg-surface/40 p-4">
          <div className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" aria-hidden />
            <span className="font-mono text-xs uppercase tracking-[0.14em] text-muted">
              AI Agent
            </span>
          </div>
          <p className="mt-3 font-mono text-sm text-fg">{AGENT_ID}</p>
          <p className="mt-2 text-xs leading-relaxed text-muted">
            An autonomous agent is requesting permission to use a tool.
          </p>
          {tool && (
            <div className="mt-4 rounded-md border border-border bg-bg/60 p-2.5">
              <p className="font-mono text-[0.68rem] uppercase tracking-wider text-faint">
                requesting
              </p>
              <code className="mt-1 block break-all font-mono text-xs text-accent">
                {tool.call}
              </code>
            </div>
          )}
        </div>

        {/* Center — runtime pipeline */}
        <div className="order-3 min-w-0 md:order-2">
          <p className="mb-3 font-mono text-xs uppercase tracking-[0.14em] text-muted">Runtime</p>
          <div className="relative" style={{ minHeight: ROW_H * STAGES.length }}>
            <div
              className="absolute w-px bg-border-strong"
              style={{ left: 16, top: ROW_H / 2, bottom: ROW_H / 2 }}
            />
            <div
              className="absolute w-px transition-all duration-300 ease-out"
              style={{ left: 16, top: ROW_H / 2, height: progressH, background: progressColor }}
            />
            <ul className="relative">
              {STAGES.map((s, i) => (
                <PipelineStage key={s} label={s} status={stageStatus(i)} sublabel={sublabel(i)} />
              ))}
            </ul>
          </div>
          <p
            className="mt-2 pl-10 font-mono text-xs transition-colors duration-300"
            style={{ color: status.color }}
            aria-live="polite"
          >
            {status.text}
          </p>
        </div>

        {/* Right — tools */}
        <div className="order-2 min-w-0 md:order-3">
          <p className="mb-3 font-mono text-xs uppercase tracking-[0.14em] text-muted">Tools</p>
          <div className="space-y-2">
            {TOOLS.map((t) => (
              <ToolButton
                key={t.id}
                tool={t}
                onClick={() => run(t)}
                disabled={phase === "running"}
                active={tool?.id === t.id}
                resolved={phase === "resolved"}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Bottom — audit log */}
      <div className="mt-5">
        <AuditLog entries={audit} />
      </div>
    </div>
  );
}
