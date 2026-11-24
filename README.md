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
| `javascript-review` | Code review for JS/TS, Web Components, reactivity, async flows, Shadow DOM dark mode, pointer safety, WCAG 2.2 AA, and security. |
| `code-unslop` | Pre-commit diff cleanup pass that removes redundant comments, section banners, filler docstrings, and dead wrappers. |
| `unslop` | 30-rule editing pass to strip AI writing tells from READMEs, docs, release notes, and blog posts. |
| `formal-verification` | Generates a project-local formal verification skill and bounded/state-space verifier for high-consequence invariants. |
| `ui-stress-test` | Adversarial UI testing across viewports, light/dark contrast, extreme content, keyboard focus, and rapid interactions. |
| `mobile-craft` | Mobile-native CSS and touch standards (`touch-action`, sticky hover guards, iOS zoom prevention, `100dvh`, safe areas). |
| `motion-craft` | CSS transition and animation standards (explicit properties, tight durations, origin-aware overlays, reduced motion). |
| `release-hygiene` | Pre-release checklist covering repo-wide stale version sweeps, dead file pruning, docs sync, and verification gates. |

## License

MIT
