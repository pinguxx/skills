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

- `use plan to scope adding room reconnection`
- `/rust-review` or `use rust-review on git diff`
- `use google-rust-style to audit src/`
- `use rust-axum-ws to design the WebSocket broadcast loop`
- `use formal-verification on the token consumption path`

The `google-rust-style` skill includes a standalone Python scanner for common Google Rust Style Guide violations. Run it against any Rust crate or file:

```bash
python ~/.agents/skills/google-rust-style/scripts/audit_google_style.py src/
```

When running directly from a clone of this repository, use `skills/google-rust-style/scripts/audit_google_style.py`.

## Included skills

### Core workflow, security, and hygiene

| Skill | Purpose |
| :--- | :--- |
| `plan` | Concise, file-level implementation plans with invariants, edge cases, and exact verification gates before coding. |
| `implement-plan` | Step-by-step execution of an approved plan with tight test loops, zero scope creep, diff cleanup, and full verification gates. |
| `formal-verification` | Generates a project-local formal verification skill and bounded/state-space verifier for high-consequence invariants. |
| `security-audit` | Threat-focused review for XSS/DOM sinks, URL sanitization, prototype pollution, injection, path traversal, SSRF, auth/CORS/CSRF, and secret leaks. |
| `code-unslop` | Pre-commit diff cleanup pass that removes redundant comments, section banners, filler docstrings, and dead wrappers. |
| `unslop` | 30-rule editing pass to strip AI writing tells from READMEs, docs, release notes, and blog posts. |
| `release-hygiene` | Pre-release checklist covering repo-wide stale version sweeps, dead file pruning, docs sync, and verification gates. |

### Web, UI, and JavaScript

| Skill | Purpose |
| :--- | :--- |
| `javascript-review` | Code review for JS/TS, Web Components, reactivity, async flows, Shadow DOM dark mode, pointer safety, WCAG 2.2 AA, and security. |
| `a11y-audit` | Dedicated WCAG 2.2 AA and WAI-ARIA APG audit covering semantics, light/dark contrast, keyboard navigation, focus traps, ARIA, and `axe-core`. |
| `ui-stress-test` | Adversarial UI testing across viewports, light/dark contrast, extreme content, keyboard focus, and rapid interactions. |
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

## Workflow: building and shipping a Rust project

1. **Scope and plan (`plan`)**
   Define affected crates, state invariants, lock boundaries, and exact `cargo` verification gates before editing code.
2. **Build step by step (`implement-plan`)**
   Implement the plan in small increments, running targeted `cargo check` and `cargo test` commands after each step.
3. **Apply architecture and protocol rules (`rust-axum-ws`, `rust-wasm-sandbox`, `rust-durable-state`, `rust-mcp`)**
   - Use `rust-axum-ws` for Axum HTTP/WebSocket rooms, broadcast decoupling, generation cancellation, and health checks.
   - Use `rust-wasm-sandbox` when executing guest WebAssembly with fuel metering and memory envelopes.
   - Use `rust-durable-state` when persisting state transitions and single-use resume tokens in SQLite WAL.
   - Use `rust-mcp` when implementing JSON-RPC 2.0 MCP servers or clients over stdio or SSE.
4. **Verify critical invariants (`formal-verification`)**
   Use `formal-verification` when a protocol, token transition, lock ordering, or state machine has interleavings that unit tests rarely cover.
5. **Audit code, style, security, and performance (`rust-review`, `google-rust-style`, `security-audit`, `rust-perf-profile`)**
   - Run `rust-review` on the diff for production unwraps, lock guards across `.await`, `unsafe` invariants, and SQL/command boundaries.
   - Run `google-rust-style` and `audit_google_style.py` to enforce import discipline, flexible reference types, and standard traits.
   - Run `security-audit` for web endpoints, auth/CORS/CSRF, path traversal, and secret hygiene.
   - Run `rust-perf-profile` against `--release` binaries when measuring RSS memory, latency percentiles, or binary size budgets.
6. **Clean the diff and docs (`code-unslop`, `unslop`)**
   Run `code-unslop` on `git diff` and `unslop` on `README.md`, crate docs, and changelogs.
7. **Release (`release-hygiene`)**
   Sweep `Cargo.toml` and docs for stale versions, verify `cargo fmt --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace`, and `cargo build --release` before tagging.

## License

MIT
