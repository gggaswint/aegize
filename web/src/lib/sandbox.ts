// Data model for the runtime sandbox — a safe, local-only simulation.
// Nothing here executes real commands, sends email, or calls any service.

export const AGENT_ID = "research_bot";

export const STAGES = [
  "Identity",
  "Policy",
  "Permissions",
  "Approval",
  "Execution",
  "Audit",
] as const;

export type Stage = (typeof STAGES)[number];

export type Decision = "allowed" | "approval_required" | "denied";

export interface ToolDef {
  id: string;
  label: string; // category shown on the button (Web Search, Email, …)
  call: string; // the simulated call, shown as code
  tool: string; // audit tool name
  operation: string; // audit operation
  decision: Decision;
  reason: string;
  /** Index in STAGES where the action resolves (full pass = last stage). */
  stopIndex: number;
}

// Stage indices, for readability.
const POLICY = 1;
const PERMISSIONS = 2;
const APPROVAL = 3;
const AUDIT = 5;

export const TOOLS: ToolDef[] = [
  {
    id: "web_search",
    label: "Web Search",
    call: 'web_search("Aegize runtime")',
    tool: "web_search",
    operation: "search",
    decision: "allowed",
    reason: "Risk level within policy",
    stopIndex: AUDIT,
  },
  {
    id: "email",
    label: "Email",
    call: 'send_email("customer@example.com", "Quarterly update")',
    tool: "email",
    operation: "send",
    decision: "approval_required",
    reason: "High-impact action requires human approval",
    stopIndex: APPROVAL,
  },
  {
    id: "shell",
    label: "Shell",
    call: 'execute_shell("rm -rf /")',
    tool: "shell",
    operation: "execute",
    decision: "denied",
    reason: "Destructive command denied by policy",
    stopIndex: POLICY,
  },
  {
    id: "filesystem",
    label: "Filesystem",
    call: 'read_file("./safe_data/report.md")',
    tool: "filesystem",
    operation: "read",
    decision: "allowed",
    reason: "Path within the allowlist",
    stopIndex: AUDIT,
  },
  {
    id: "payments",
    label: "Payments",
    call: 'charge_payment("$500")',
    tool: "payments",
    operation: "charge",
    decision: "denied",
    reason: "Payments not permitted for this agent",
    stopIndex: PERMISSIONS,
  },
];

export interface AuditEntry {
  id: number;
  time: string; // HH:MM:SS
  agent: string;
  target: string; // tool.operation
  decision: Decision;
  reason: string;
}

export const DECISION_META: Record<Decision, { label: string; color: string }> = {
  allowed: { label: "allowed", color: "var(--color-allow)" },
  approval_required: { label: "approval required", color: "var(--color-approval)" },
  denied: { label: "denied", color: "var(--color-deny)" },
};

/** Final status line shown when a run resolves. */
export const OUTCOME: Record<Decision, { text: string; color: string }> = {
  allowed: { text: "Executed", color: "var(--color-allow)" },
  approval_required: { text: "Waiting for human approval", color: "var(--color-approval)" },
  denied: { text: "Blocked by policy", color: "var(--color-deny)" },
};
