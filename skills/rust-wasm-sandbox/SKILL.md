---
name: rust-wasm-sandbox
description: Designs and audits in-process WebAssembly sandboxes in Rust using Wasmtime, covering instruction fuel metering, linear memory limits, zero-access WASI, and host-guest memory ABIs.
---

# Rust WebAssembly sandboxes

Design and audit in-process Wasmtime sandboxes that execute untrusted guest modules with deterministic CPU, memory, and capability limits. Categorize findings as **Blocking**, **Important**, or **Nit**.

---

## 1. Instruction fuel metering
- **Enable fuel consumption on the shared engine (Blocking):** Set `config.consume_fuel(true)` when constructing `wasmtime::Engine`. Reuse the compiled `Engine` and compiled `Module`s across runs where possible while isolating each execution in a fresh `Store`.
- **Per-run fuel budgets (Blocking):** Set an explicit `store.set_fuel(limit)` (and epoch interruption for async yields if host calls can run long) before invoking any guest export.
- **Deterministic exhaustion traps (Important):** Handle `Trap::OutOfFuel` explicitly so infinite loops abort in bounded time without panicking or tearing down the host process.

---

## 2. Linear memory envelopes and bounds checking
- **Cap memory and table growth (Blocking):** Wire a `StoreLimits` implementation (`StoreLimitsBuilder`) into `store.limiter(...)` with explicit caps on linear memory bytes, tables, and instances so malicious `memory.grow` loops trap cleanly.
- **Validate guest pointers and lengths (Blocking):** Never trust an `(ptr, len)` pair returned by a guest export. Before reading or writing linear memory, verify `ptr >= 0`, `len >= 0`, `checked_add` does not overflow, and `ptr + len <= memory.data_size(&store)`.
- **Bounded payload sizes (Important):** Enforce a maximum host-side serialization size before allocating guest buffers so oversized requests cannot exhaust guest memory before execution starts.

---

## 3. Zero-access WASI isolation
- **Deny ambient capabilities by default (Blocking):** Initialize guest WASI contexts with no preopened directories, no network sockets, and no inherited environment variables unless an explicit capability allowlist grants them.
- **Constrain host functions (Important):** Every imported host function exposed via `Linker` must validate arguments, charge appropriate fuel or quotas, and reject ambient filesystem or subprocess access.

---

## 4. Host-guest linear memory ABI
Use a minimal, auditable 3-export ABI when exchanging structured payloads (such as JSON or MessagePack) between host and guest:
1. `allocate(size: i32) -> i32`: guest reserves `size` bytes and returns the base offset in linear memory.
2. `deallocate(ptr: i32, size: i32)`: guest frees an allocated input or output slice.
3. `execute(ptr: i32, len: i32) -> i64`: guest reads input bytes, runs logic, writes output bytes, and returns a packed `u64` containing `(out_ptr << 32) | out_len`.

Always unpack `(out_ptr, out_len)` carefully on the host (`((packed >> 32) & 0xFFFF_FFFF) as usize` and `(packed & 0xFFFF_FFFF) as usize`), validate bounds against linear memory, copy the bytes out, and call `deallocate` (ignoring trap if the module already aborted).

---

## Verification
Write automated integration tests using compiled `.wat` fixtures to verify:
1. An infinite-loop guest traps with `OutOfFuel` within the configured wall-clock budget.
2. A guest allocating or requesting out-of-bounds memory is rejected without host panics.
3. A roundtrip compute/echo module passes input, unpacks output, frees guest memory, and reports remaining fuel accurately.
4. Run `cargo clippy --workspace --all-targets -- -D warnings` and `cargo test --workspace`.
