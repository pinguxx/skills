---
name: simplify
description: Simplify working code for readability and lower structural complexity without changing behavior. Complements `code-unslop` by targeting nesting, control flow, naming, and speculative abstractions.
---

# Code simplification

Apply this skill to working, tested code whose structure is harder to read or maintain than it needs to be. Run `code-unslop` for comment and wrapper cleanup; use `simplify` for structural clarity.

## 1. Scope and behavior preservation
- Preserve inputs, outputs, side effects, ordering, and error behavior identically. If any existing test must be modified to pass, behavior changed; revert immediately.
- Apply Chesterton's Fence: read callers, tests, and `git blame` before removing non-obvious logic.
- Scope edits strictly to recently modified or explicitly requested files. Make zero drive-by refactors in unrelated files.
- Respect `simplify-ignore` annotations and explicit performance or invariant comments; never rewrite protected blocks.

## 2. Structural targets
- Flatten `3+` levels of nesting using guard clauses and early returns.
- Replace nested ternaries with `if/else`, `switch`, or lookup maps.
- Replace positional boolean flags (`fn(true, false, true)`) with options objects or separate named functions.
- Extract repeated conditional expressions into named predicate functions.
- Split multi-responsibility functions (`50+` lines) into focused helpers.
- Remove redundant shapes: unnecessary `async` or `return await` wrappers, `if (cond) return true; return false`, redundant type casts, and speculative single-use abstractions (single-strategy patterns, factory-for-a-factory).
- Rename generic or misleading identifiers (`data`, `val`, `temp`, or `get*` functions that mutate state).

## 3. Anti-over-simplification guardrails
- Optimize for comprehension speed, not fewer lines.
- Keep helper functions whose names document a non-obvious domain concept.
- Do not trade clear loops or `if/else` blocks for dense chained `.reduce()` calls or clever one-liners.
- Do not simplify performance-critical paths if the simpler version is measurably slower.
- Reject refactors that only relocate complexity without reducing the number of concepts a reader must hold.

## 4. Scale and verification
- **Rule of 500:** For mechanical simplifications spanning `500+` lines, write a script or codemod rather than editing by hand.
- Keep simplification commits separate from feature or bugfix commits.
- Run existing tests, typechecks, and linters unmodified after each incremental change.
