---
name: a11y-audit
description: Audit and fix web applications and UI components for WCAG 2.2 AA and WAI-ARIA APG compliance. Covers semantic HTML, light/dark contrast, keyboard navigation, focus management, ARIA contracts, form associations, and automated axe-core verification.
---

# Accessibility Audit (WCAG 2.2 AA & WAI-ARIA APG)

Audit the target page, component, or diff across all 6 areas below. Categorize findings as **Blocking** (WCAG 2.2 AA failure or keyboard trap), **Important** (broken APG pattern or degraded screen-reader UX), or **Nit** with exact `file:line` references and concrete fixes.

## 1. Semantics & Landmarks
- Use native HTML elements (`<button>`, `<a>`, `<input>`, `<select>`, `<label>`, `<dialog>`) instead of clickable `<div>` or `<span>`.
- Ensure pages have one `<main>`, proper heading hierarchy (`h1` to `h6` without skipped levels), and distinct `<nav>` labels (`aria-label`) when multiple nav landmarks exist.
- Every icon-only button, close control, and image needs an accessible name (`aria-label`, visually hidden text, or `alt`). Decorative icons and images must use `aria-hidden="true"` or `alt=""`.

## 2. Color Contrast & Visual Accessibility
- Verify WCAG 2.2 AA contrast in both light and dark modes (`>= 4.5:1` for normal text, `>= 3:1` for large text `>= 18px` bold / `>= 24px` regular and UI controls/borders/focus indicators).
- Never convey state (error, success, required, selected) by color alone; pair with text, icons, or attributes (`aria-invalid`, `aria-current`, `aria-selected`).
- Keep interactive target sizes `>= 24x24px` (prefer `>= 44x44px` on touch).
- Support `prefers-reduced-motion: reduce` for all animations and avoid fixed heights that clip text at `200%` zoom.

## 3. Keyboard Navigation & Focus Management
- Every interactive control must be reachable and operable with `Tab`, `Shift+Tab`, `Enter`, and `Space` with zero keyboard traps.
- Every focusable element must show a visible `:focus-visible` indicator. Never set `outline: none` without a visible `:focus-visible` replacement.
- Modals, dialogs, and drawers must move focus inside on open, trap focus while open, close on `Escape`, and restore focus to the trigger element on close.
- Composite widgets must follow WAI-ARIA APG keyboard patterns (roving `tabindex` or `aria-activedescendant`, `Arrow*`, `Home`, `End`, `Escape`): tabs, menus, menubars, toolbars, radio groups, comboboxes, listboxes, trees, and calendars.

## 4. Forms & Live Regions
- Every form control must have a programmatic label (`<label for>`, wrapping `<label>`, or `aria-label` / `aria-labelledby`). Placeholder text is not a label.
- Associate hint and validation messages with `aria-describedby`, and mark invalid inputs with `aria-invalid="true"`.
- Announce asynchronous status changes (toasts, form errors, loading completion, search result counts) with `role="status"` (`aria-live="polite"`) or `role="alert"` (`aria-live="assertive"`).

## 5. Shadow DOM & Custom Elements
- Verify ARIA references (`aria-labelledby`, `aria-describedby`, `aria-controls`) do not break across Shadow DOM boundaries.
- Verify custom focusable hosts use `delegatesFocus: true` or explicit `tabindex` management and expose clean `:focus-visible` rings.
- Verify dark-mode tokens inherit cleanly into Shadow DOM without dead `:root[data-theme="dark"]` or invalid `:host-context(...):host(...)` rules.

## 6. Automated & Manual Verification
- Run automated accessibility checks (`@axe-core/playwright`, `jest-axe`, or `pa11y`) in both light and dark themes when available.
- Tab through the full interactive flow manually (or via Playwright keyboard tests) and confirm zero violations and zero focus loss.
