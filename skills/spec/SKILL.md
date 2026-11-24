---
name: spec
description: Write a concrete specification before planning or coding when requirements are ambiguous, greenfield, or span multiple modules. Covers assumption checks, measurable success criteria, boundaries, capability maps, and delta specs.
---

# Specification authoring

Use this skill for new features, greenfield projects, ambiguous asks, or multi-module initiatives. Skip it for single-line fixes or unambiguous edits, and go straight to `plan`.

## 1. Check assumptions and clarify
- List explicit assumptions in an **Assumptions** block before drafting so the user can correct them early.
- If intent is still unclear across user, outcome, binding constraint, or success metric, ask **one question at a time with your best guess attached** (`Q:` and `GUESS:`) instead of a multi-question survey. Stop once you can predict the user's answers.

## 2. Capability map (multi-module asks only)
When one request bundles multiple independently testable domains, propose a compact module table before writing per-module specs:
- Columns: `Module id` (stable kebab-case), `Responsibility`, `Depends on` (one-way dependencies, no cycles), and `Build order`.
- Get user approval on module boundaries and build order before writing individual specs.

## 3. Spec structure
Keep the document concise and testable:
- **Title with version:** `# Spec: <Name> (V1)`.
- **Objective and user:** Who benefits and what problem this solves.
- **Tech stack, commands, and layout:** Include only for greenfield projects; in existing repositories, observe them directly.
- **Success criteria:** Reframe vague goals ("faster", "cleaner") into measurable conditions with concrete numbers or pass/fail checks.
- **Boundaries:**
  - **Always:** Non-negotiable checks such as running tests and validating external input.
  - **Ask first:** High-impact changes such as schema migrations, new runtime dependencies, or CI config edits.
  - **Never:** Hard prohibitions such as committing secrets or weakening tests.
- **Out of scope (deferred):** Capture V2 or mid-build ideas explicitly so V1 scope does not grow.
- **Open questions:** Unresolved decisions needing human input.

## 4. Delta specs for shipped features
When changing an already-shipped spec, write a focused delta spec instead of editing the shipped spec mid-flight:
- Include `Status: proposed`, **Objective**, **Current behavior**, **New behavior**, **Success criteria** (including what must not change), and **Boundary deltas**.
- Fold the outcome into the original spec and mark `Status: implemented` after shipping.

## 5. Approval gate
1. Save the spec to the repository (or present it for review) and list any **Open questions**.
2. Ask for explicit user approval.
3. **Stop the turn.** Do not invoke `plan` or write code in the same turn.
