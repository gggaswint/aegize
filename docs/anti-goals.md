# Anti-goals

What Aegize is deliberately **not**. This document exists to keep the project
focused. The space around "infrastructure for autonomous AI agents" is crowded
with adjacent products; naming what we are not is the fastest way to stay clear
about what we are.

Aegize is the runtime layer between autonomous AI agents and the tools they use.
It governs *actions*. The categories below are things it is routinely mistaken
for, and is not.

---

## Aegize is not an LLM wrapper

We do not call models, manage prompts, or sit in the request/response path to an
LLM. Aegize governs what an agent is allowed to *do* with the tools it has, not
what it says or how it is prompted. You bring the model; we govern the action.

## Aegize is not a chatbot

There is no conversational surface, no assistant, no end-user chat product.
Aegize is infrastructure that other software integrates, not an application a
person talks to.

## Aegize is not an agent framework

We do not orchestrate agents, manage their control flow, plan their steps, or
define how they reason. Frameworks (LangGraph, CrewAI, the OpenAI Agents SDK,
custom loops) sit *above* Aegize and send actions *through* it. We integrate with
frameworks; we do not compete to be one.

## Aegize is not a prompt-engineering tool

We do not optimize, template, test, or version prompts. Prompt-level techniques
are advisory and live with the model. Aegize enforces at runtime, in code, which
is a different layer with a different guarantee.

## Aegize is not a model host

We do not serve, fine-tune, route, or run inference for models. Aegize is
model-agnostic by design and runs alongside whatever models a system already
uses.

## Aegize is not a vector database

We do not store embeddings, do retrieval, or manage memory or knowledge. Aegize's
state is the policy and the audit log — what an agent may do and what it did — not
the data an agent reasons over.

## Aegize is not a workflow-automation app

We are not a no-code/low-code automation builder, a job scheduler, or an
integration platform that wires apps together. Aegize governs the actions that
flow through it; it does not author or own the workflow.

## Aegize is not an AI safety nonprofit

Aegize is operational infrastructure for the actions agents take today, built and
run as a serious engineering project. It is not an advocacy organization, a
research lab, or a policy body, and it makes no claims about model alignment.

## Aegize is not a fear-based AI-doom product

We do not sell dread. The reason to adopt Aegize is control, clarity, and
confidence in deployment — the same reasons you give identities, permissions, and
audit to human operators and service accounts. We make no claims about preventing
existential risk, and our messaging never leans on catastrophe.

---

### Why this matters

Each anti-goal protects a principle from [principles.md](./principles.md):
staying out of the model path keeps us **vendor neutral**; refusing to become a
framework or an app keeps us **infrastructure over applications**; rejecting
doom-and-safety-nonprofit framing keeps **security a capability, not the brand**.
When a proposed feature pulls Aegize toward one of these categories, that is a
strong signal to reconsider it.
