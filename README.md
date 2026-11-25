# skills

Personal, repo-agnostic Agent Skills for software engineering, JavaScript and Rust code review, systems architecture, formal verification, UI craft, and writing.

## Install globally

Install all skills across supported coding agents (Claude Code, Cursor, Codex, Windsurf, Gemini CLI, Antigravity) with one command:

```bash
npx skills add pinguxx/skills --global
```

Install a single skill:

```bash
npx skills add pinguxx/skills --skill javascript-review --global
npx skills add pinguxx/skills --skill rust-review --global
```

## How to use

Reference any installed skill by name in your prompt or with a slash command when your agent supports it:

- `use spec to define a new CLI tool before coding`
- `use plan to scope adding room reconnection`
- `use debug to isolate the flaky auth test`
- `use simplify on src/parser.ts`
- `use web-perf to audit checkout LCP`
- `/rust-review` or `use rust-review on git diff`
- `use google-rust-style to audit src/`
- `use rust-axum-ws to design the WebSocket broadcast loop`
- `use formal-verification on the token consumption path`
- `/retro` or `use retro on this session`

The `google-rust-style` skill includes a standalone Python scanner for common Google Rust Style Guide violations. Run it against any Rust crate or file:

```bash
python ~/.agents/skills/google-rust-style/scripts/audit_google_style.py src/
```

When running directly from a clone of this repository, use `skills/google-rust-style/scripts/audit_google_style.py`.

## Included skills

### Core workflow, security, and hygiene

| Skill | Purpose |
| :--- | :--- |
| `spec` | Versioned specs, assumption checks, measurable success criteria, three-tier boundaries, capability maps, and delta specs before planning. |
| `plan` | Concise, file-level implementation plans with invariants, edge cases, and exact verification gates before coding. |
| `implement-plan` | Step-by-step execution of an approved plan with tight test loops, zero scope creep, diff cleanup, and full verification gates. |
| `debug` | Root-cause error triage with stop-the-line discipline, isolation, minimal repros, and failing-first regression tests. |
| `simplify` | Structural code simplification (nesting, control flow, naming, speculative abstractions) without changing behavior. |
| `formal-verification` | Generates a project-local formal verification skill and bounded/state-space verifier for high-consequence invariants. |
| `security-audit` | Threat-focused review for XSS/DOM sinks, URL sanitization, prototype pollution, injection, path traversal, SSRF, LLM output, supply chain, and secrets. |
| `code-unslop` | Pre-commit diff cleanup pass that removes redundant comments, section banners, filler docstrings, and dead wrappers. |
| `unslop` | 30-rule editing pass to strip AI writing tells from READMEs, docs, release notes, and blog posts. |
| `release-hygiene` | Pre-release checklist covering stale version sweeps, git doc-drift checks, dependency audits, dead file pruning, and verification gates. |
| `retro` | Post-session retrospective that turns friction into navigation pointers, deterministic lint/CI checks, leaner steering files, and review rules. |

### Web, UI, and JavaScript

| Skill | Purpose |
| :--- | :--- |
| `javascript-review` | Code review for JS/TS, Web Components, reactivity, async flows, Shadow DOM dark mode, pointer safety, anti-shortcut floor, and API hygiene. |
| `a11y-audit` | Dedicated WCAG 2.2 AA and WAI-ARIA APG audit covering semantics, light/dark contrast, keyboard navigation, focus traps, ARIA, and `axe-core`/`pa11y`. |
| `ui-stress-test` | Adversarial UI testing across viewports, light/dark contrast, UI states, extreme content, keyboard focus, and rapid interactions. |
| `design-craft` | Structured UI design workflow: `DESIGN.md` context, 4-part briefs, multi-variant exploration, refinement vocabulary (`critique`, `bolder`, `quieter`, `distill`, `normalize`, `polish`), and anti-slop checks. |
| `web-perf` | Measure-first web and backend performance profiling covering Core Web Vitals, `EXPLAIN ANALYZE`, connection pools, caches, and keep-or-revert budgets. |
| `mobile-craft` | Mobile-native CSS and touch standards (`touch-action`, sticky hover guards, iOS zoom prevention, `100dvh`, safe areas). |
| `motion-craft` | CSS transition and animation standards (explicit properties, tight durations, origin-aware overlays, reduced motion). |

### Rust and systems

| Skill | Purpose |
| :--- | :--- |
| `rust-review` | Code review for Rust crates covering panic freedom (`unwrap`/`expect`/indexing), async locks across `.await`, ownership, `unsafe` comments, and SQL/command/SSRF boundaries. |
| `google-rust-style` | Google Rust Style Guide audit and refactoring standards across imports, borrows, traits, naming, and idioms, with an automated Python scanner. |
| `rust-axum-ws` | Architecture and review rules for Axum and Tokio HTTP/WebSocket backends covering state lock scoping, split writer channels, generation tokens, reconnects, and security headers. |
| `rust-wasm-sandbox` | In-process Wasmtime sandbox rules covering instruction fuel metering, linear memory limits, zero-access WASI, and host-guest pointer ABIs. |
| `rust-durable-state` | Event-sourced state machines with SQLite WAL configuration, transactional checkpoints, crash recovery, and atomic single-use resume tokens. |
| `rust-mcp` | Rust Model Context Protocol (MCP) server and client rules covering JSON-RPC 2.0 lifecycles, `stdout`/`stderr` stdio hygiene, schema validation, and transport bounds. |
| `rust-perf-profile` | Release-mode RSS memory measurement, `criterion` latency benchmarks, hot-path clone and lock audits, and `[profile.release]` tuning. |

## Workflow: creating and shipping a web project

Use the skills in order from first spec to release when building a new project from scratch or shipping a major feature. Invoke a skill by name in your prompt (for example, `use spec to define...`, `use plan to scope...`, or `/javascript-review`).

1. **Create the spec and plan (`spec`, `plan`)**
   When starting a new project from scratch, or tackling an ambiguous or multi-module request, run `spec` first to settle assumptions, tech stack, commands, project layout, measurable success criteria, and three-tier boundaries. After approving the spec, run `plan` to map the exact files to create or change, invariants, edge cases, and verification gates.
2. **Establish UI direction (`design-craft`)**
   For user-facing web UI, create or read `DESIGN.md` (`ALWAYS`/`NEVER` guardrails), explore 2 to 3 distinct layout variants before committing, and steer iterations with `critique`, `bolder`, `quieter`, `distill`, `normalize`, and `polish`.
3. **Build step by step (`implement-plan`, `debug`)**
   Execute the approved plan one step at a time with `implement-plan`. Run the narrowest test after each step and keep edits scoped to the plan. When a test fails or behavior breaks, run `debug` to isolate the root cause and write a failing-first regression test before fixing.
4. **Polish UI behavior (`mobile-craft`, `motion-craft`)**
   When building web UI, apply `mobile-craft` for touch targets, `100dvh`, safe areas, and sticky-hover guards, and `motion-craft` for explicit transitions and reduced-motion rules.
5. **Verify critical invariants (`formal-verification`)**
   If the project has stateful logic, concurrency, reactive graphs, parsers, or security boundaries where unit tests miss edge cases, run `formal-verification` to generate a fast, project-local verifier.
6. **Audit code, accessibility, security, performance, and UI (`javascript-review`, `a11y-audit`, `security-audit`, `web-perf`, `ui-stress-test`)**
   - Run `javascript-review` on the diff for modern JS/TS, async races, leaks, Shadow DOM traps, and anti-shortcut checks.
   - Run `a11y-audit` to verify WCAG 2.2 AA contrast, keyboard navigation, focus traps, and ARIA contracts.
   - Run `security-audit` to check DOM sinks, URL validation, prototype pollution, injection, SSRF, supply chain, and secrets.
   - Run `web-perf` when optimizing Core Web Vitals, bundle budgets, SQL query plans, or caches.
   - Run `ui-stress-test` across `320px` to `1440px`, light and dark modes, UI states, extreme content, and rapid interactions.
7. **Simplify and clean the diff and docs (`simplify`, `code-unslop`, `unslop`)**
   Run `simplify` on complex working code to reduce nesting and speculative abstractions without changing behavior. Run `code-unslop` on `git diff` to remove redundant comments, section banners, and dead wrappers. Run `unslop` on `README.md`, docs, and release notes to strip AI writing tells.
8. **Release (`release-hygiene`)**
   Before tagging, run `release-hygiene` to sweep the repo for stale version numbers, check doc drift, prune dead files, audit lockfile dependencies, sync changelogs, and verify every test, typecheck, build, and size gate passes.
9. **Run a retrospective (`retro`)**
   After shipping a milestone or finishing a rough session, run `retro` (user-invoked via `/retro` or `use retro`) to add missing navigation pointers, wire deterministic lint or CI checks for mechanical mistakes, and prune bloated `AGENTS.md` rules.

## Workflow: building and shipping a Rust project

1. **Create the spec and plan (`spec`, `plan`)**
   When starting a new Rust project from scratch, or tackling an ambiguous or multi-crate request, run `spec` first to lock down assumptions, crate layout, measurable targets, and boundaries. After approving the spec, run `plan` to define affected crates, state invariants, lock boundaries, and exact `cargo` verification gates before editing code.
2. **Build step by step (`implement-plan`, `debug`)**
   Implement the plan in small increments, running targeted `cargo check` and `cargo test` commands after each step. When a test fails or behavior diverges, run `debug` to reproduce, bisect or localize, and add a regression test before fixing.
3. **Apply architecture and protocol rules (`rust-axum-ws`, `rust-wasm-sandbox`, `rust-durable-state`, `rust-mcp`)**
   - Use `rust-axum-ws` for Axum HTTP/WebSocket rooms, broadcast decoupling, generation cancellation, and health checks.
   - Use `rust-wasm-sandbox` when executing guest WebAssembly with fuel metering and memory envelopes.
   - Use `rust-durable-state` when persisting state transitions and single-use resume tokens in SQLite WAL.
   - Use `rust-mcp` when implementing JSON-RPC 2.0 MCP servers or clients over stdio or SSE.
4. **Verify critical invariants (`formal-verification`)**
   Use `formal-verification` when a protocol, token transition, lock ordering, or state machine has interleavings that unit tests rarely cover.
5. **Audit code, style, security, and performance (`rust-review`, `google-rust-style`, `security-audit`, `rust-perf-profile`)**
   - Run `rust-review` on the diff for production unwraps, lock guards across `.await`, `unsafe` invariants, anti-shortcut checks, and SQL/command boundaries.
   - Run `google-rust-style` and `audit_google_style.py` to enforce import discipline, flexible reference types, and standard traits.
   - Run `security-audit` for web endpoints, auth/CORS/CSRF, path traversal, supply chain, and secret hygiene.
   - Run `rust-perf-profile` against `--release` binaries when measuring RSS memory, latency percentiles, or binary size budgets.
6. **Simplify and clean the diff and docs (`simplify`, `code-unslop`, `unslop`)**
   Run `simplify` to reduce structural complexity without changing behavior, `code-unslop` on `git diff`, and `unslop` on `README.md`, crate docs, and changelogs.
7. **Release (`release-hygiene`)**
   Sweep `Cargo.toml` and docs for stale versions, check doc drift, run `cargo audit`, verify `cargo fmt --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace`, and `cargo build --release` before tagging.
8. **Run a retrospective (`retro`)**
   After shipping a milestone or finishing a rough session, run `retro` to capture missing navigation pointers, wire deterministic checks for mechanical mistakes, and prune bloated `AGENTS.md` rules.

## License

MIT
