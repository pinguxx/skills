---
name: motion-craft
description: Author, audit, and refine CSS transitions, animations, and micro-interactions in web apps and components. Enforces explicit transition properties, crisp easing budgets, origin-aware overlays, and reduced-motion support.
---

# Motion Craft

UI motion should confirm state changes without slowing the user down. Apply these rules when authoring or reviewing CSS animations and transitions.

## Rules
1. **Never use `transition: all`.** List the exact properties being transitioned (`transform`, `opacity`, `background-color`, `border-color`, `box-shadow`). Animating layout properties (`width`, `height`, `top`, `left`) causes reflow jank.
2. **Keep durations tight.**
   - Micro-feedback (`:active` press, focus ring, hover tint): `100ms` to `150ms`.
   - Entrances, popovers, dropdowns, tooltips: `120ms` to `220ms` with `ease-out` or `cubic-bezier(0.16, 1, 0.3, 1)`. Never use `ease-in` for entrances.
   - Exits: faster than entrances (`100ms` to `160ms`).
3. **Origin-aware overlays.** Popovers, dropdowns, tooltips, and context menus should scale from the edge nearest their trigger (`transform-origin: bottom center` when placed above, `top center` when placed below). Centered modals scale from `center`.
4. **Respect reduced motion.** Every `@keyframes` animation and non-trivial transition must include a `@media (prefers-reduced-motion: reduce)` rule that removes spatial movement and collapses duration.
5. **Do not block interaction.** Animations must never prevent a user from clicking or typing before the transition finishes.
