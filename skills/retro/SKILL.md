---
name: retro
description: Conduct a post-session retrospective to improve the coding agent's environment (navigation pointers, automated checks, review standards, steering files, tooling, and log access).
disable-model-invocation: true
---

# Session retrospective

Suggest concrete changes to the coding agent's environment so future sessions run faster and make fewer mistakes.

## 1. Read primary sources
- Inspect the session specified by the user (session logs, git diffs, test output, and tool calls). If no session is specified, inspect the current session.

## 2. Audit improvement candidates
Look for high-impact gaps across these seven categories:

- **Navigation:** The agent spent extra steps locating files or missed hidden cross-file dependencies. Add a short navigation pointer where the agent looks first.
- **Automated checks:** Read existing check scripts (`package.json`, `Cargo.toml`, `Makefile`, pre-commit hooks, and CI workflows) first so unwired or broken checks are fixed rather than reinvented. Treat a repository with no pre-commit hook or CI check running lint, typecheck, and tests as a standing finding.
- **Coding standards (mechanical vs. judgment calls):** Classify every missed mistake before writing a rule. Mechanical violations (banned APIs, fixed syntactic patterns, import shapes, file placement) require a deterministic check (a linter rule, pre-commit hook, or CI job), not prose. Reserve review standards (`CODING_STANDARDS.md` or project review skills) for judgment calls that no linter can replace.
- **Steering files (`AGENTS.md`, `CLAUDE.md`):** Keep always-loaded steering files short and focused on navigation pointers. Move coding rules to review-time standards or automated checks whenever repo or global steering files grow large.
- **Tool economy:** Flag token-heavy CLI or MCP calls, noisy outputs, or repeated exploration steps that can be replaced with narrower commands or scripts.
- **No-ops:** Flag instructions in steering files that do not change agent behavior so they can be pruned.
- **Information access:** Flag missing runtime signals (such as teeing dev server logs or read-only access to service logs) that blocked diagnosis.

## 3. Implementation vs. review context pressure
- Implementation carries the highest context pressure (exploration, code edits, debugging). Review has low context pressure because it operates on a diff. Place coding standards on the review side rather than inflating always-loaded implementation prompts.
- Keep `AGENTS.md` and `CLAUDE.md` as compact navigation indexes, place judgment-based rules in review standards or skills, and keep deep reference material in docs linked on demand.

## 4. Present and confirm
1. Present improvement candidates ordered by severity with exact target files.
2. Keep every proposed rule terse, concrete, and compliant with `unslop`.
3. Ask for explicit user approval before editing `AGENTS.md`, hooks, CI configs, or review skills.
