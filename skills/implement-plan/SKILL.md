---
name: implement-plan
description: Execute an approved implementation plan step-by-step with tight feedback loops, zero scope creep, invariant checks, diff cleanup, and full verification gates before handoff.
---

# Implement Plan

Use this skill when executing an approved plan (from the `plan` skill or user spec). Focus on clean, minimal, verified execution.

## 1. Confirm Baseline Before Editing
- Read the exact files listed in the plan so every edit matches the current code.
- Check `git status` and run the fastest relevant existing test so you know the starting baseline is green (or note pre-existing failures).

## 2. Execute Step-by-Step
- Implement one logical step of the plan at a time.
- Keep edits tightly scoped to the plan. Do not refactor unrelated code, rename unrelated symbols, or add unrequested features.
- Never silence checkers or weaken tests to get green (no new `@ts-ignore`, `eslint-disable`, `#[allow(...)]`, `.skip`/`#[ignore]`, deleted assertions, empty `catch {}`, or unimplemented stubs).
- After each step, run the narrowest test or typecheck that covers the changed code. Fix failures immediately before moving to the next step.
- If you hit a contradiction, missing prerequisite, or broken invariant that the plan did not anticipate, stop and tell the user rather than quietly hacking around it.

## 3. Sync Dependent Surfaces
- Check whether the change requires updating generated files, types (`.d.ts`), schemas/manifests, tests, or documentation in the repo. Update them in the same pass so nothing drifts.

## 4. Clean & Verify Before Reporting Done
1. Inspect `git diff`, run `simplify` if complex control flow accumulated, and run `code-unslop` to strip redundant comments, debug logs, and dead code.
2. Run every verification gate from the plan (unit tests, coverage, typecheck, build, size budget, E2E/browser checks). Do not re-run an already-passing check if no code changed since it ran.
3. Never claim a check passed without running it after the final edit.
4. Report concisely: files changed, verification commands run with pass/fail results, and any noticed-but-not-touched follow-up items outside the plan scope.
