---
name: rust-durable-state
description: Designs and audits durable event-sourced state machines in Rust with SQLite WAL persistence, transactional checkpoints, and atomic single-use resume tokens.
---

# Rust durable state and SQLite WAL

Design and audit crash-resilient workflows and event-sourced state machines backed by embedded SQLite. Categorize findings as **Blocking**, **Important**, or **Nit**.

---

## 1. SQLite WAL configuration
Configure every SQLite connection or pool initialization hook with write-ahead logging and strict integrity settings:

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
PRAGMA foreign_keys = ON;
```

- **Serialized or bounded writers (Blocking):** Keep write transactions brief so concurrent readers never stall and writers do not hit `SQLITE_BUSY` past `busy_timeout`.
- **No shared connection across threads without pooling (Blocking):** Manage concurrent access through a proper async pool (`sqlx::SqlitePool`) or dedicated writer channel rather than ad-hoc locking over a raw connection.

---

## 2. Transactional checkpointing and hydration
- **Persist before and after transitions (Blocking):** Write an intent/pre-step record (or transition event) and commit post-step state updates inside explicit SQLite transactions (`BEGIN` ... `COMMIT`). If the process crashes mid-step, recovery can distinguish completed steps from interrupted ones.
- **Deterministic state hydration (Important):** Reconstructing an active run after restart must read the latest committed checkpoint (or deterministically replay the ordered event log) without skipping idempotency guards.
- **Monotonic sequence ordering (Important):** Assign an auto-incrementing sequence number per run (`UNIQUE (run_id, seq)`) so replayed events always apply in total order.

---

## 3. Atomic single-use resume tokens
- **Cryptographic unpredictability (Blocking):** Generate suspension/approval tokens using a CSPRNG (for example UUIDv4 or 128+ bits of OS entropy). Never derive tokens from timestamps, sequential IDs, or predictable hashes.
- **Single-use atomic consumption (Blocking):** Validate and invalidate a resume token inside one database transaction:

```sql
DELETE FROM suspended_tokens
WHERE run_id = ?1 AND token = ?2 AND expires_at > ?3
RETURNING step_id;
```

Or check `rows_affected() == 1` on the `DELETE` before advancing the workflow. Separate `SELECT` followed by `DELETE` creates a race window allowing double-resumption replay attacks.

---

## 4. Query safety and migrations
- **Parameterized SQL only (Blocking):** Bind all values with placeholders (`?1`, `?2`). Never format runtime values or unvalidated identifiers into SQL strings.
- **Versioned idempotent migrations (Important):** Keep DDL under `migrations/` and index every foreign key, status filter, and expiration lookup column (`run_id`, `token`, `created_at`).
- **Store compact checkpoints (Nit):** Persist minimal serialized diffs or JSON state needed for replay rather than duplicating full context blobs on every transition.

---

## Verification
Write integration tests exercising a temporary or in-memory SQLite WAL database to prove:
1. A run halted midway rehydrates cleanly from SQLite and finishes without re-executing committed steps.
2. Submitting the same `resume_token` concurrently from two tasks succeeds once and rejects the second attempt cleanly.
3. Concurrent readers and writers operate under WAL mode with zero `SQLITE_BUSY` failures.
4. Run `cargo clippy --workspace --all-targets -- -D warnings` and `cargo test --workspace`.
