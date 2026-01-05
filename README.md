## 🧠 Hello Agent — Week 1 Agentic AI MVP

**Hello Agent** is a minimal, educational CLI project that demonstrates the core mechanics of **agentic AI** in practice.

The agent reads a `TODO` comment from a Python file, uses an LLM to generate a code patch, applies the change, runs tests, and reports success or failure — forming a complete **intent → action → observation** loop.

This repository is intentionally simple and vendor-agnostic, focusing on **how agents actually work**, not hype or frameworks.


┌───────────┐
│ TODO Scan │
└─────┬─────┘
      ↓
┌───────────┐
│ Planner   │ (LLM)
└─────┬─────┘
      ↓
┌───────────┐
│ Executor  │ → Docker sandbox
└─────┬─────┘
      ↓
┌───────────┐
│ Verifier  │ → classify failures
└─────┬─────┘
      ↓
┌───────────┐
│ Metrics   │ → JSON logs
└───────────┘

---
---

### ✨ What this project demonstrates

* Intent capture from source code (`# TODO`)
* LLM-powered code generation
* Autonomous file modification (code patching)
* Test execution and result observation
* Provider-agnostic model integration (Anthropic, Groq, OpenRouter)

---

### 🛠️ Supported LLM Providers

* **Anthropic** (Claude 3.5 Sonnet)
* **Groq** (Llama 3.1)
* **OpenRouter** (multi-model gateway)

The agent architecture allows easy switching between providers without changing core logic.

---

### 🎯 Why this repo exists

This project serves as a **“hello world” for agentic AI**, aligned with real-world engineering practices:

* No frameworks
* No magic abstractions
* No vendor lock-in
* Clear, inspectable control flow

It is the foundation for more advanced agent capabilities such as retries, verification loops, PR automation, and multi-agent orchestration.

---

### 🚀 Roadmap

* Retry loop on test failure
* Verifier / critic agent
* Diff-based patching
* Git commit automation
* PR agent (future weeks)
