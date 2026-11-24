---
name: code-unslop
description: Clean up code diffs before committing by removing redundant comments, section banners, filler docstrings, dead wrappers, and unnecessary defensive checks without changing behavior.
---

# Code Unslop Pass

Run on `git diff` or target files before committing. Behavior must stay 100% identical, and all tests, typechecks, and size budgets must continue to pass.

## Remove
1. **Comments that restate the next line** (e.g. `// Close on Escape` right above `if (e.key === 'Escape') close()`).
2. **ASCII section banners** (`// ================ Helpers ================`).
3. **History narration comments** (`// Updated to fix...`, `// Added per request...`). Git history owns this.
4. **Filler JSDoc or docstrings** that only repeat parameter or function names without adding types, units, or behavioral constraints.
5. **Dead one-caller wrappers** that add indirection without clarifying intent or isolating a boundary.
6. **Defensive checks for impossible internal states** that add dead branches and bloat bundle size.

## Keep
1. **Why comments** that explain a non-obvious browser quirk, protocol edge case, race condition, or invariant.
2. **Public API docs** that document real contracts, defaults, thrown errors, or emitted events.
3. **Boundary validation** on untrusted external input (user input, network payloads, CLI flags, environment variables).

## Verify
After cleaning the diff, re-run the repo's test suite and typecheck to confirm zero behavior changes.
