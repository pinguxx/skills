---
name: a11y-audit
description: Audit and fix web applications and UI components for WCAG 2.2 AA and WAI-ARIA APG compliance. Covers semantic HTML, light/dark contrast, keyboard navigation, focus management, ARIA contracts, form associations, and automated axe-core verification.
---

# Accessibility Audit (WCAG 2.2 AA & WAI-ARIA APG)

Audit the target page, component, or diff across all 6 areas below. Categorize findings as **Blocking** (WCAG 2.2 AA failure or keyboard trap), **Important** (broken APG pattern or degraded screen-reader UX), or **Nit** with exact `file:line` references and concrete fixes.

## 1. Semantics & Landmarks
- Use native HTML elements (`<button>`, `<a>`, `<input>`, `<select>`, `<label>`, `<dialog>`) instead of clickable `<div>` or `<span>`.
- Ensure pages have `<html lang="...">`, a descriptive `<title>`, one `<main>`, a skip-to-content link visible on keyboard focus, proper heading hierarchy (`h1` to `h6` without skipped levels), and distinct `<nav>` labels (`aria-label`) when multiple nav landmarks exist.
- Mark up data tables with `<th>` headers and `scope` attributes.
- Every icon-only button, close control, and image needs an accessible name (`aria-label`, visually hidden text, or `alt`). Decorative icons and images must use `aria-hidden="true"` or `alt=""`.
- Ensure link text makes sense out of context (no "Click here" or "Read more") and distinguishes links from surrounding prose by more than color alone.

## 2. Color Contrast & Visual Accessibility
- Verify WCAG 2.2 AA contrast in both light and dark modes (`>= 4.5:1` for normal text, `>= 3:1` for large text `>= 18.67px` (`14pt`) bold / `>= 24px` (`18pt`) regular and UI controls/borders/focus indicators). Never round a failing contrast ratio up.
- **Separate solid-fill tokens from foreground-text tokens:** A brand fill color calibrated for white text on a solid button (e.g. `#2563eb` or `#dc2626`) drops to `2.0:1–3.4:1` when reused as text or icon color on a dark surface. Ghost buttons, links, active tabs, validation errors, chips, spinners, and status icons MUST use dedicated foreground text tokens (e.g. `--color-primary-text`, `--color-danger-text`) verified in both light and dark modes, including hover/active states.
- Never convey state (error, success, required, selected) by color alone; pair with text, icons, or attributes (`aria-invalid`, `aria-current`, `aria-selected`).
- Keep interactive target sizes `>= 24x24px` size or spacing for WCAG 2.2 AA (SC 2.5.8); target `>= 44x44px` on touch (SC 2.5.5 AAA).
- Verify layout and focus visibility under Windows High Contrast (`forced-colors: active`), support `prefers-reduced-motion: reduce` for all animations, avoid fixed heights that clip text at `200%` zoom, forbid content flashing `> 3` times per second (SC 2.3.1), and never autoplay audio or video without controls (SC 1.4.2).

## 3. Keyboard Navigation & Focus Management
- Every interactive control must be reachable and operable with `Tab`, `Shift+Tab`, `Enter`, and `Space` with zero keyboard traps, and focus order must match visual and DOM order (SC 2.4.3). Never use `tabindex > 0` (use `0` or `-1` only).
- Every focusable element must show a visible `:focus-visible` indicator. Never set `outline: none` without a visible `:focus-visible` replacement. Note `>= 3:1` focus indicator contrast against the unfocused state (SC 2.4.13 AAA) as **Important** or **Nit**, not an AA blocker.
- Modals, dialogs, and drawers must move focus inside on open, trap focus while open, close on `Escape`, and restore focus to the trigger element on close.
- Composite widgets must follow WAI-ARIA APG keyboard patterns (roving `tabindex` or `aria-activedescendant`, `Arrow*`, `Home`, `End`, `Escape`): tabs, menus, menubars, toolbars, radio groups, comboboxes, listboxes, trees, and calendars.

## 4. Forms & Live Regions
- Every form control must have a programmatic label (`<label for>`, wrapping `<label>`, or `aria-label` / `aria-labelledby`). `placeholder` disappears on input and does not satisfy SC 3.3.2.
- Set `autocomplete` attributes on known user fields (`name`, `email`, `current-password`, SC 1.3.5 AA).
- Associate hint and validation messages with `aria-describedby`, mark invalid inputs with `aria-invalid="true"`, and make form submission error summaries focusable (or move focus to the summary or first invalid field).
- Announce asynchronous status changes (toasts, form errors, loading completion, search result counts) with `role="status"` (`aria-live="polite"`) or `role="alert"` (`aria-live="assertive"`).

## 5. Shadow DOM & Custom Elements
- Verify ARIA references (`aria-labelledby`, `aria-describedby`, `aria-controls`) do not break across Shadow DOM boundaries.
- Verify custom focusable hosts use `delegatesFocus: true` or explicit `tabindex` management and expose clean `:focus-visible` rings.
- Verify dark-mode tokens inherit cleanly into Shadow DOM without dead `:root[data-theme="dark"]` or invalid `:host-context(...):host(...)` rules.

## 6. Automated & Manual Verification
- Run the bundled contrast matrix scanner against any CSS token sheet to verify every text-on-surface pairing mathematically in light and dark modes (`python3 scripts/check_contrast.py path/to/tokens.css`).
- Map every **Blocking** violation to a WCAG 2.2 Success Criterion; preferences without an SC or APG contract belong in **Nit**.
- Run automated accessibility checks (`@axe-core/playwright`, `jest-axe`, `@axe-core/cli`, or `pa11y`) in both light and dark themes when available. Confirm each tool exited validly and produced non-empty parseable output; never report a crashed tool or empty output as zero violations.
- Automated checks and code reading cannot prove screen-reader announcements. Tag AT-dependent items `manual` with the browser and screen reader pair to test (for example Chrome + NVDA or Safari + VoiceOver) unless that test was executed.
- Tab through the full interactive flow manually (or via Playwright keyboard tests) and confirm zero violations and zero focus loss.
