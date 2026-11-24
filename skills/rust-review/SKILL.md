---
name: rust-review
description: Reviews Rust crates, async Tokio services, error handling, concurrency, ownership, unsafe blocks, and security boundaries. Invoke when reviewing Rust files, diffs, or PRs.
---

# Rust code review

Audit changes across the 5 areas below. Categorize every finding as **Blocking**, **Important**, or **Nit** with exact `file:line` references and concrete fixes. Report defects, hazards, and missing verification gates without filler.

---

## 1. Panic freedom and error handling
- **Production unwrap and expect (Blocking):** Forbid `.unwrap()`, `.expect()`, and `panic!()` in non-test production code. Return `Result<T, E>` or `Option<T>` instead.
- **Unchecked indexing and slicing (Blocking):** Flag direct indexing (`slice[i]`, `&s[a..b]`) on dynamic indices or untrusted lengths. Use `.get(...)` or `.split_at_checked(...)`.
- **Integer overflow and division by zero (Important):** Guard untrusted or accumulating integer arithmetic with `checked_*` or `saturating_*` operations, and validate divisors before division or modulo.
- **Structured errors (Important):** Use `thiserror` for typed domain and library errors with preserved source context. Return opaque external error messages to callers so internal SQL errors, paths, and tokens never leak.

---

## 2. Async and concurrency safety
- **Lock guards held across await (Blocking):** Never hold `std::sync::MutexGuard` or `std::sync::RwLock*Guard` across an `.await` point. Even with `tokio::sync::Mutex`, clone or extract the minimal data needed and drop guards before awaiting network I/O or broadcasts.
- **Background task cancellation (Blocking):** Spawned Tokio tasks (timers, heartbeats, workers, bot loops) must use cancellation tokens, shutdown channels, or monotonic generation counters so stale tasks exit when state resets or clients disconnect.
- **Cross-task bounds (Important):** Types crossing task or trait boundaries should satisfy `'static + Send + Sync` via owned values or explicit shared handles.
- **Poisoned mutexes (Blocking):** Never call `.into_inner()` on a `PoisonError` to salvage mutable state after a panic. Propagate the failure cleanly.

---

## 3. Ownership, borrowing, and performance
- **Flexible parameter types (Important):** Accept `&str`, `&[T]`, `&T`, and `Option<&T>` instead of `&String`, `&Vec<T>`, `&Box<T>`, or `&Option<T>`.
- **Clones in hot paths (Important):** Flag `.clone()` used as a borrow-checker workaround in request handlers, broadcast loops, or serializers. Use borrowed views, `Cow<'_, str>`, or cheap `Arc` handle clones only where shared ownership is required.
- **Resource bounds (Blocking):** Cap untrusted request bodies, WebSocket frame sizes, channel capacities (prefer bounded `mpsc::channel` where backpressure matters), and recursion depths.
- **Preallocation (Nit):** Use `Vec::with_capacity` and `String::with_capacity` when output size is known ahead of loops.

---

## 4. Unsafe code and security boundaries
- **Safety comments (Blocking):** Every `unsafe` block and `unsafe fn` requires an adjacent `// SAFETY:` comment stating the exact invariant upheld by the caller or surrounding code. Flag unannotated or broad `unsafe` blocks.
- **Parameterized SQL (Blocking):** Reject string formatting or concatenation (`format!`) in SQL statements or dynamic identifiers. Require compile-time checked or parameterized queries (`sqlx`, `tokio-postgres`, `rusqlite` params) and strict allowlists for dynamic sort columns.
- **Command injection and SSRF (Blocking):** Never interpolate untrusted strings into `Command::new("sh")` or shell flags; pass discrete arguments to the target binary. Validate outbound user URLs for scheme allowlists and block loopback, private, and cloud metadata IP ranges.
- **Path traversal and secret leaks (Blocking):** Canonicalize user-supplied paths and confirm they stay inside the intended root directory before file I/O. Never log API keys, JWTs, cookies, salts, or passwords via `tracing`, `println!`, or `Debug` derives.

---

## 5. Verification
Before approving, run the workspace toolchain and report exact pass/fail results:
- `cargo fmt --check`
- `cargo check --workspace --all-targets`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `cargo test --workspace`
- `cargo llvm-cov --workspace` when coverage tracking is configured.
