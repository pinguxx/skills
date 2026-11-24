---
name: plan
description: Scope and plan non-trivial engineering changes before writing code. Produces a concise, file-level implementation plan with invariants, edge cases, and explicit verification gates. Invoke before large refactors, new features, or architectural changes.
---

# Implementation Planning

Use this skill before editing code on any task that touches multiple files, changes a public API, alters state/data flow, or carries regression risk. Keep plans short, concrete, and grounded in the actual codebase.

## 1. Read First, Ask Only What You Cannot Observe
- Inspect the relevant files, tests, build config, and git history before proposing changes.
- Do not guess file paths, symbols, or CLI scripts. Verify them in the repo.
- Ask the user only when requirements or tradeoffs are genuinely ambiguous. Keep questions to 1 to 3 concrete choices.

## 2. Structure the Plan
Keep the plan tight enough to scan in 60 seconds:

1. **Goal**: One or two sentences stating the exact behavior change and what is out of scope.
2. **Files to Change**: List exact file paths with one bullet per file describing the concrete edit.
3. **Invariants & Edge Cases**: List the rules that must not break (backwards compatibility, accessibility, dark mode, concurrency/races, bundle size, zero new runtime deps, security boundaries).
4. **Verification Gates**: List the exact commands to run after implementation (unit tests, coverage, typecheck, build, E2E/browser checks, size budgets).

## 3. Execution Rules
- Follow the simplest design that satisfies the requirements. Do not invent abstractions for one-off use cases.
- Break work into small, verifiable steps. Run the fastest relevant test after each step instead of waiting until the end.
- If a real bug or constraint surfaces mid-execution that invalidates the plan, stop and revise the plan before continuing.
- Before finishing, remove dead code, verify every item in the verification gates passes, and report exact command outcomes.
