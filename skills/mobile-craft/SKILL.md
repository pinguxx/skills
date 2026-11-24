---
name: mobile-craft
description: Mobile-native CSS and touch interaction standards for web apps and components. Prevents sticky hover states, tap highlight flashes, iOS input auto-zoom, 100vh clipping, and background scroll bleed.
---

# Mobile-Native Craft

Use this skill when building or auditing mobile views, responsive pages, bottom sheets, drawers, or touch interactions.

## Checklist
1. **Eliminate tap delay and grey flash.** Set `touch-action: manipulation` and `-webkit-tap-highlight-color: transparent` on buttons, toggles, chips, tabs, and segmented controls.
2. **Prevent sticky touch hover.** Wrap decorative `:hover` styles in `@media (hover: hover) and (pointer: fine)` so tapped elements do not stay stuck in a hover state on phones and tablets.
3. **Prevent iOS Safari input auto-zoom.** Inside `@media (pointer: coarse)`, ensure `input`, `select`, and `textarea` use `font-size: max(16px, 1em)` so focusing a field never zooms the viewport.
4. **Use dynamic viewport height and safe areas.** Pair `100vh` fallbacks with `100dvh` and `env(safe-area-inset-bottom, 0px)` on full-height sheets, drawers, and sticky bottom bars so mobile browser toolbars and home indicators never clip controls.
5. **Contain overlay scroll.** Set `overscroll-behavior: contain` on dialogs, drawers, and scrollable menus so scrolling inside an overlay never triggers pull-to-refresh or scrolls the page behind it.
6. **Keep hit targets reachable.** Maintain `>= 44x44px` comfortable touch targets on primary mobile actions (`>= 24x24px` minimum per WCAG 2.2 AA).
