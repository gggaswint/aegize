import type { Metadata } from "next";
import { SandboxPage } from "@/components/SandboxPage";

export const metadata: Metadata = {
  title: "Sandbox",
  description:
    "Try the Aegize runtime — a safe, local simulation of how an AI action passes through identity, policy, permissions, approval, execution, and audit before it reaches a tool.",
};

export default function Page() {
  return <SandboxPage />;
}
