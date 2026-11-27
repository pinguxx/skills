---
name: design-craft
description: Structured UI design workflow that eliminates generic AI aesthetics. Enforces a project DESIGN.md brief, 4-part UI prompts, multi-variant exploration before committing, a shared refinement vocabulary (critique, bolder, quieter, distill, normalize, polish), and deterministic anti-slop checks.
---

# Design Craft

Use this skill when designing, redesigning, or refining web pages, landing pages, dashboards, or component layouts so the output looks intentional instead of generic AI output.

## 1. Establish Project Context (`DESIGN.md`)
Before generating UI for a project, read `DESIGN.md` if it exists. If it does not exist, create a short one (under 60 lines) with:
- **Aesthetic brief (5 to 8 lines):** visual tone, density (editorial, balanced, or dense ops), typography pairing, color palette (surface, primary, ink, accent), and radius/elevation style.
- **Reference anchors:** specific products, screenshots, or existing pages in the repo to match.
- **Intent:** what the user is trying to accomplish on the screen and what single action matters most.
- **Guardrails:**
  - `ALWAYS`: use design tokens/CSS custom properties, one primary CTA per view, real domain copy, `tabular-nums` on numbers, light and dark mode contrast `>= 4.5:1`.
  - `NEVER`: default purple/indigo hero gradients, gratuitous glassmorphism, eyebrow pill above every heading, one colored word inside every headline, nested cards inside cards, placeholder "Lorem ipsum" or "Acme" slop.

## 2. Never One-Shot: Propose 2 to 3 Macro Variants First
For new pages or major redesigns, do not commit to the first layout:
1. Propose **2 to 3 distinct macro directions** (for example: *Editorial*, *Dense Ops*, *Warm Minimal*) with concrete differences in layout hierarchy, typography scale, and density.
2. Let the user pick a direction (or combine elements) before polishing details.
3. Inspect the rendered output in a real browser at desktop (`1440px`) and mobile (`375px`) in both light and dark modes.

## 3. Shared Refinement Vocabulary
When iterating on an existing screen, map short steering directives to concrete edits:
- **`critique`**: Score visual hierarchy, typography, spacing rhythm, color restraint, contrast, and domain fit; list the top 3 concrete fixes.
- **`bolder`**: Increase typographic contrast (display vs body ratio), strengthen focal point, commit to one clear accent color, remove timid gray-on-gray boxes.
- **`quieter`**: Reduce border weight, drop decorative badges/icons/gradients, widen whitespace, and limit accent color to the primary CTA.
- **`distill`**: Cut redundant headings, duplicate cards, filler subtitles, and unnecessary controls until only essential elements remain.
- **`normalize`**: Replace hardcoded hex colors, ad-hoc spacing, and stray radii with the project's design tokens and `DESIGN.md` scale.
- **`polish`**: Tighten alignment, optical padding, hover/focus/active states, loading/empty states, and micro-copy.

## 4. Typography, Micro-Copy & Persistent Taste Memory
- **Typography:** Apply `text-wrap: balance` on display headings, `text-wrap: pretty` on body prose (`max-width: 65ch`), `font-variant-numeric: tabular-nums` on numbers/KPIs/tables, and concentric radii (`outer radius = inner radius + padding`).
- **Actionable UI micro-copy:** Use verb-first button labels ("Save workspace", not "Submit" or "OK"). Every error state and empty state must explain what happened and the next concrete action.
- **Remember keep/reject decisions:** When the user accepts or rejects a visual choice, append a one-line decision to `DESIGN.md` so later screens never drift back to rejected patterns.

## 5. Deterministic UI Anti-Slop Checklist
Before shipping any UI diff, check for and remove these patterns:
1. **Default AI palettes:** unrequested purple/cyan gradients or neon glow borders.
2. **Eyebrow + colored-word spam:** repeating uppercase tracked pills above every section heading or highlighting one word in every headline.
3. **Card-in-card nesting:** wrapping cards inside cards or putting heavy `1px solid` gray borders on every container instead of using whitespace and subtle surface contrast.
4. **Hardcoded colors:** inline hex/rgb colors that break dark mode instead of semantic tokens.
5. **Transition bloat:** `transition: all`, `scale(0)` pops, layout-property transitions (`width`/`height`/`top`/`left`), or slow (`> 300ms`) entrance animations.
6. **Fake copy:** generic buzzwords ("Supercharge your workflow", "Unlock next-gen AI") instead of concrete product language.
