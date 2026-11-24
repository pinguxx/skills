---
name: rust-axum-ws
description: Architecture and review standards for Rust Axum and Tokio HTTP/WebSocket backends, covering shared state, lock-free broadcasts, task cancellation, reconnects, health checks, and security headers.
---

# Rust Axum and WebSocket services

Build and audit stateful Axum + Tokio HTTP and WebSocket servers without deadlocks, zombie background tasks, or wide-open HTTP defaults. Categorize findings as **Blocking**, **Important**, or **Nit**.

---

## 1. Shared state and lock discipline
- **Explicit lock scoping (Blocking):** Store shared room or application registries in `Arc<RwLock<...>>` (or sharded concurrent maps). Extract or clone only the fields needed for a message, then drop the guard before any `.await`, WebSocket send, or broadcast loop.
- **No blocking calls on Tokio workers (Blocking):** Move synchronous filesystem reads, image processing, or heavy CPU loops onto `tokio::task::spawn_blocking`.
- **Single transition helpers (Important):** Route shared outcomes (such as human and automated player win checks or room cleanup) through one state-transition function so score updates, payouts, and event broadcasts never drift.

---

## 2. WebSocket lifecycle and background tasks
- **Split reader and writer tasks (Blocking):** Split each WebSocket with `futures_util::StreamExt::split`. Drive outgoing messages through a per-connection `mpsc` channel into a dedicated writer task so slow clients cannot stall shared broadcasts or hold state locks.
- **Monotonic generation counters for timers and loops (Blocking):** Track a `generation: u64` counter (or `CancellationToken`) on rooms and sessions. Increment it on pause, restart, or end-of-round. Every background timer, auto-caller, or bot loop must capture the starting generation and exit without mutating state if the live generation changed.
- **Empty and bot-only room cleanup (Important):** On client disconnect or leave, re-elect hosts strictly among connected human players. Remove rooms that contain zero remaining human participants so background tasks and memory are reclaimed.
- **Channel backpressure (Important):** Size per-client channels explicitly or disconnect lagging sockets rather than buffering unbounded queues on slow mobile connections.

---

## 3. Reconnection and input validation
- **Reconnect with stable session IDs (Important):** Issue an opaque player/session ID at join time so browser refreshes and transient mobile drops restore active state cleanly without duplicating participants.
- **Payload size and rate limits (Blocking):** Enforce maximum WebSocket message lengths and HTTP body limits (`DefaultBodyLimit`). Validate every client enum, string length, and integer range on the server before mutating room state.
- **Pause and resume toggle idempotency (Important):** Ensure toggle handlers check the current flag under lock and start at most one background loop per generation so pausing and resuming cannot spawn duplicate timers.

---

## 4. HTTP security, static assets, and health endpoints
- **Hardened response headers (Blocking):** Attach `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` (or `SAMEORIGIN`), and `Referrer-Policy: strict-origin-when-cross-origin` via `tower_http::set_header::SetResponseHeaderLayer`.
- **CORS boundaries (Blocking):** Avoid wildcard `AllowOrigin::any()` paired with credentials in production APIs. Configure allowed origins from environment variables with safe local defaults.
- **Zero-dependency health routes (Important):** Expose lightweight `GET /health` (plus aliases like `/healthz` or `/api/health` when platforms expect them) returning `200 OK` JSON without acquiring contested write locks or blocking on non-critical third-party calls.
- **Static asset serving (Nit):** Serve compiled frontend bundles via `tower_http::services::ServeDir` and configure explicit cache headers so stale HTML does not pin outdated WebSocket message shapes.

---

## Verification
1. Exercise HTTP routes (including `/health` and security headers) in-memory using `tower::ServiceExt::oneshot`.
2. Exercise live WebSocket joins, broadcasts, pauses, reconnects, and disconnects using `tokio-tungstenite` against an ephemeral `127.0.0.1:0` listener.
3. Run `cargo clippy --workspace --all-targets -- -D warnings` and `cargo test --workspace`.
