# skills

Personal, repo-agnostic Agent Skills for software engineering, code review, verification, UI craft, and writing.

## Install globally

Install all skills across supported coding agents (Claude Code, Cursor, Codex, Windsurf, Gemini CLI, Antigravity) with one command:

```bash
npx skills add pinguxx/skills --global
```

Install a single skill:

```bash
npx skills add pinguxx/skills --skill javascript-review --global
```

## Included skills

| Skill | Purpose |
| :--- | :--- |
| `plan` | Concise, file-level implementation plans with invariants, edge cases, and exact verification gates before coding. |
| `implement-plan` | Step-by-step execution of an approved plan with tight test loops, zero scope creep, diff cleanup, and full verification gates. |
| `javascript-review` | Code review for JS/TS, Web Components, reactivity, async flows, Shadow DOM dark mode, pointer safety, WCAG 2.2 AA, and security. |
| `a11y-audit` | Dedicated WCAG 2.2 AA and WAI-ARIA APG audit covering semantics, light/dark contrast, keyboard navigation, focus traps, ARIA, and `axe-core`. |
| `security-audit` | Threat-focused review for XSS/DOM sinks, URL sanitization, prototype pollution, injection, path traversal, SSRF, auth/CORS/CSRF, and secret leaks. |
| `code-unslop` | Pre-commit diff cleanup pass that removes redundant comments, section banners, filler docstrings, and dead wrappers. |
| `unslop` | 30-rule editing pass to strip AI writing tells from READMEs, docs, release notes, and blog posts. |
| `formal-verification` | Generates a project-local formal verification skill and bounded/state-space verifier for high-consequence invariants. |
| `ui-stress-test` | Adversarial UI testing across viewports, light/dark contrast, extreme content, keyboard focus, and rapid interactions. |
| `mobile-craft` | Mobile-native CSS and touch standards (`touch-action`, sticky hover guards, iOS zoom prevention, `100dvh`, safe areas). |
| `motion-craft` | CSS transition and animation standards (explicit properties, tight durations, origin-aware overlays, reduced motion). |
| `release-hygiene` | Pre-release checklist covering repo-wide stale version sweeps, dead file pruning, docs sync, and verification gates. |

## Workflow: creating and shipping a project

Use the skills in order from first spec to release. Invoke a skill by name in your prompt (for example, `use plan to scope...` or `/javascript-review`).

1. **Scope and plan (`plan`)**
   Start every new project or major feature with `plan`. Define the goal, exact files to create or change, invariants, edge cases, and the verification commands before writing code.
2. **Build step by step (`implement-plan`)**
   Execute the approved plan one step at a time with `implement-plan`. Run the narrowest test after each step and keep edits scoped to the plan.
3. **Polish UI behavior (`mobile-craft`, `motion-craft`)**
   When building web UI, apply `mobile-craft` for touch targets, `100dvh`, safe areas, and sticky-hover guards, and `motion-craft` for explicit transitions and reduced-motion rules.
4. **Verify critical invariants (`formal-verification`)**
   If the project has stateful logic, concurrency, reactive graphs, parsers, or security boundaries where unit tests miss edge cases, run `formal-verification` to generate a fast, project-local verifier.
5. **Audit code, accessibility, security, and UI (`javascript-review`, `a11y-audit`, `security-audit`, `ui-stress-test`)**
   - Run `javascript-review` on the diff for modern JS/TS, async races, leaks, and Shadow DOM traps.
   - Run `a11y-audit` to verify WCAG 2.2 AA contrast, keyboard navigation, focus traps, and ARIA contracts.
   - Run `security-audit` to check DOM sinks, URL validation, prototype pollution, injection, auth/CORS, and secrets.
   - Run `ui-stress-test` across `320px` to `1440px`, light and dark modes, extreme content, and rapid interactions.
6. **Clean the diff and docs (`code-unslop`, `unslop`)**
   Run `code-unslop` on `git diff` to remove redundant comments, section banners, and dead wrappers. Run `unslop` on `README.md`, docs, and release notes to strip AI writing tells.
7. **Release (`release-hygiene`)**
   Before tagging, run `release-hygiene` to sweep the repo for stale version numbers, prune dead files, sync docs and changelogs, and verify every test, typecheck, build, and size gate passes.

## License

MIT
