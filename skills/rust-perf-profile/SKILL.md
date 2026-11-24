---
name: rust-perf-profile
description: Profiles and optimizes Rust RSS memory footprint, latency percentiles, hot-path allocations, lock contention, and release binary size.
---

# Rust performance and memory profiling

Measure first, optimize only with release-mode data, and enforce concrete latency, memory, and binary-size budgets. Never optimize debug builds (`target/debug`) or invent unmeasured numbers.

---

## 1. Set numeric budgets first
Define explicit targets before profiling or rewriting code:
- **Resident memory (RSS):** Idle baseline and peak under expected concurrency (in MB).
- **Operation latency:** Median (p50) and tail (p95/p99) targets for hot-path handlers, state commits, or frame renders (in microseconds or milliseconds).
- **Binary size budget:** Target stripped release executable or `.wasm` artifact size when deploying to containers, edge runtimes, or browsers.

---

## 2. Measure RSS memory on release builds
Always build with `--release` before recording memory numbers:

```bash
cargo build --release
```

- **Windows (PowerShell):**
  ```powershell
  $proc = Get-Process -Name "<binary_name>"
  [math]::Round($proc.WorkingSet64 / 1MB, 2)
  ```
- **Linux / macOS:**
  ```bash
  grep -E 'VmRSS|VmHWM' /proc/<pid>/status
  # or on macOS: ps -o rss= -p <pid>
  ```

Record both idle startup RSS and peak RSS after sustained load so memory leaks and unbounded caches show up immediately.

---

## 3. Measure latency and throughput
- Use `criterion` for repeatable micro-benchmarks (`cargo bench`), or wrap realistic end-to-end flows with warm-up iterations and `std::time::Instant` in release mode.
- Report minimum, median (p50), and tail (p95/p99) latencies rather than single-run timings.
- Isolate allocation vs I/O vs lock wait time when diagnosing tail spikes.

---

## 4. Common Rust hot-path and binary bottlenecks
- **Excessive cloning and heap churn:** Replace `.clone()` on strings, maps, and vectors in loops with `&str`, `&[T]`, `Cow<'_, str>`, `Bytes`, or preallocated buffers (`Vec::with_capacity`).
- **Lock contention:** Split coarse `Mutex<AppState>` locks by shard or convert read-heavy maps to `RwLock` with short read scopes. Remove I/O and serialization from inside lock guards.
- **JSON overhead in tight loops:** Serialize broadcast payloads once (`Arc<str>` or pre-serialized `Bytes`) before fanning out across N WebSocket clients instead of running `serde_json::to_string` inside the per-client loop.
- **Release profile tuning:** When deployment size or throughput requires it, check `[profile.release]` in `Cargo.toml` (`lto = "thin"` or `true`, `codegen-units = 1`, `strip = true`) and compare binary size before and after.

---

## Verification
1. Capture baseline RSS, latency, and binary size on `--release`.
2. Apply targeted fixes one bottleneck at a time.
3. Re-measure with the same command and report exact before/after numbers.
4. Run `cargo test --workspace` and `cargo clippy --workspace --all-targets -- -D warnings` to confirm zero behavioral regressions.
