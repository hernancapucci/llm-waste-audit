# llm-waste-audit

Detect and reduce avoidable LLM waste.

> Most AI cost isn’t model pricing. It’s design failure.

---

## What is this?

`llm-waste-audit` is a lightweight audit tool that detects **avoidable waste patterns** in LLM usage.

It focuses on real, common problems:

- prompts that break caching
- context that is too large or redundant
- tool definitions that inflate every request

This is **not a wrapper**.  
This is a **diagnostic layer**.

---

## Current scope (v0.1)

Implemented:

- **W1 — Context Bloat**
- **W2 — Cache Breaker**

Planned:

- W3 — Redundant Reasoning
- W4 — Model Overkill
- W5 — Output Excess
- W6 — Retrieval Waste
- W7 — Session Memory Failure
- W8 — Unsafe Semantic Reuse

---

## Quick example

```bash
llm-waste-audit scan examples/langfuse/sample_trace.json --markdown
