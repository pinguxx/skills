---
name: javascript-review
description: Reviews JavaScript, TypeScript, Web Components, reactive signals, async flows, Shadow DOM CSS, accessibility, and security boundaries. Invoke when reviewing JS/TS files, diffs, or PRs on any project.
---

# JavaScript & Web Engineering Code Review

Audit changes across the 6 areas below. Categorize every finding as **Blocking**, **Important**, or **Nit** with exact `file:line` references and concrete fixes. Skip praise and filler; report real defects and risks.

---

## 1. Modern JS & Cross-Platform Idioms
- **Modules (Blocking):** Enforce ES module syntax (`import`/`export`) with explicit extensions where the runtime requires them. Flag unintended CommonJS (`require`, `module.exports`).
- **Windows-Safe ESM Paths (Blocking):** Never use `new URL(import.meta.url).pathname` for filesystem paths or CLI entry detection (returns `/C:/...` on Windows). Use `fileURLToPath(import.meta.url)` and `fs.realpathSync`.
- **Bindings & Equality (Important):** Prefer `const` by default, `let` only when reassigned, never `var`. Flag loose equality (`==`, `!=`) unless explicitly checking `== null`.
- **Safe Access (Nit):** Prefer optional chaining (`?.`) and nullish coalescing (`??`) over `||` fallbacks that break on valid falsy values (`0`, `""`, `false`).
- **Cross-Realm DOM Checks (Important):** Prefer `typeof val?.nodeType === 'number'` over `val instanceof Node` so code works across `happy-dom`, `jsdom`, iframes, and browsers.

---

## 2. Reactivity & Asynchronous Flows
- **Stale Reactive Reads (Blocking):** Flag template or render bindings that unwrap a reactive value once at mount instead of subscribing or passing a reactive getter/closure.
- **Batching & Fault Isolation (Blocking):** Group related multi-state writes in a batch/transaction when the reactive system supports it. Verify a throwing subscriber cannot drop notifications to sibling subscribers.
- **Self-Subscription Loops (Blocking):** Inside reactive effects or computed getters, flag reads of state mutated by the same effect unless explicitly untracked (e.g. `.peek()` / `untrack()`).
- **Async Cancellation & Races (Blocking):** Long-running `fetch` calls, streams, and async loaders must support `AbortSignal` cleanup and guard against out-of-order settlement (monotone request/run ID or abort check before committing state).
- **Unhandled Rejections & Concurrency (Important):** Every `async` call or Promise chain needs error handling (`try/catch` or `.catch()`). Flag independent sequential `await` calls inside loops; recommend `Promise.all()` or `Promise.allSettled()`.

---

## 3. DOM, Web Components & Pointer Safety
- **XSS Prevention (Blocking):** Never assign unsanitized input to `innerHTML`, `outerHTML`, or `insertAdjacentHTML`. Use `textContent`, `document.createTextNode`, or safe DOM/template bindings.
- **Lifecycle & Leak-Free Cleanup (Blocking):** Every `addEventListener`, `ResizeObserver`, `IntersectionObserver`, `MutationObserver`, `setInterval`, or `requestAnimationFrame` loop created on mount must clean up on unmount. Prefer passing an `AbortController` `signal` to listeners.
- **Shadow DOM Dark-Mode CSS (Blocking):**
  - Never use `:root[data-theme="dark"]` inside Shadow DOM stylesheets (`:root` matches nothing inside a shadow root).
  - Never chain `:host-context(...):host(...)` or `:host-context(...)[attr]` (invalid CSS Scoping Level 1; ignored by browsers).
  - Drive light and dark themes through inherited CSS custom properties (`var(--surface-card)`, `var(--text-primary)`) so Chromium, Firefox, and Safari render identically.
- **Pointer Capture Trap (Blocking):** Never call `setPointerCapture()` on `pointerdown` before checking a drag threshold (`> 5px`) or excluding interactive descendants (`button`, `a`, `input`, `select`, `textarea`). Premature capture steals `click` events and blocks text selection.
- **Form-Associated Custom Elements (Important):** Custom form controls (`static formAssociated = true`) must call `setFormValue(null)` when cleared/unchecked, expose their owning `form`, and implement `formResetCallback()` and `formDisabledCallback()`.
- **Multi-Instance Overlays (Important):** Fixed viewport overlays (toasts, snackbars, modals) must coordinate across multiple mounted instances so duplicate stacks do not overlap.

---

## 4. Accessibility & Motion Craft
- **WCAG 2.2 AA Contrast & Focus (Blocking):** Maintain `>= 4.5:1` text contrast and `>= 3:1` UI control contrast in both light and dark modes, `>= 24x24px` hit targets, and visible `:focus-visible` outlines (never `outline: none` without a `:focus-visible` replacement).
- **Keyboard State Machines (Important):** Interactive composite widgets (dialogs, menus, tabs, trees, calendars, comboboxes) must support WAI-ARIA APG keyboard navigation (`Arrow*`, `Home`/`End`, `Enter`/`Space`, `Escape`) and restore focus when overlays close.
- **Motion Contracts (Blocking):** Never use `transition: all` (list explicit properties). Every `@keyframes` animation must respect `@media (prefers-reduced-motion: reduce)`.

---

## 5. Security, Runtime & Bundle Hygiene
- **Dangerous Sinks (Blocking):** Block `eval()`, `new Function()`, `javascript:`, `vbscript:`, `data:text/html`, `data:image/svg+xml` URLs, and inline `on*` event attributes on untrusted inputs.
- **Prototype Pollution & Graph Bounds (Blocking):** Any dynamic object path, JSON pointer, or deep merge helper must reject `__proto__`, `constructor`, and `prototype`, and bound recursion depth on untrusted payloads.
- **Edge & Zero-Bloat Runtime (Important):** Flag unnecessary third-party utility imports when native platform APIs (`structuredClone`, `Intl`, `URLPattern`, `fetch`, `AbortSignal.timeout`) suffice. For Edge runtimes, block Node-only built-ins (`node:fs`, `Buffer`, `readline`) and unsupported syntax.

---

## 6. Verification After Review
Before approving, run the project's verification suite (tests, coverage, typecheck, lint, bundle size check, and browser/a11y E2E where applicable) and report exact pass/fail results.
