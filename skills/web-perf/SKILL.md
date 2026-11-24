---
name: web-perf
description: Measure-first performance profiling and optimization for web frontends, APIs, databases, and caches. Enforces Core Web Vitals targets, query plans, variance-aware benchmarking, and keep-or-revert discipline.
---

# Web and backend performance optimization

Measure before changing code, target one bottleneck at a time, and keep only verified gains.

## 1. Measure first and set budgets
- Default Core Web Vitals targets: `LCP <= 2.5s`, `INP <= 200ms`, `CLS <= 0.1`.
- Define concrete bundle size (gzipped KB) and API `p95` latency budgets before editing.
- Capture a reproducible baseline (Lighthouse, DevTools Performance trace, bundle analyzer, `EXPLAIN ANALYZE`, or `web-vitals` field metrics) under controlled, repeatable conditions.

## 2. Frontend bottlenecks
- **Images and LCP:** Declare explicit `width` and `height` on images and `<source>` elements to prevent CLS. Serve AVIF/WebP with `srcset` and `sizes`. Add `fetchpriority="high"` without `loading="lazy"` on the LCP image, and use `loading="lazy"` with `decoding="async"` below the fold.
- **Main thread and INP:** Break up long tasks (`> 50ms`) with `scheduler.yield()` or chunked loops. Defer non-critical work (analytics, logging) out of interaction handlers, and move heavy computation to Web Workers.
- **Rendering, CSS, and fonts:** Batch DOM reads before DOM writes to prevent forced synchronous layouts. Apply `content-visibility: auto` with `contain-intrinsic-size` on large off-screen sections. Preserve bfcache eligibility (no `unload` listeners, no `Cache-Control: no-store` on standard HTML). Serve WOFF2 fonts with `font-display: swap` and fallback metric overrides (`size-adjust`).
- **Bundles:** Split routes and heavy optional features with dynamic `import()`.

## 3. Backend, database, and caching bottlenecks
- **Queries:** Eliminate N+1 loops with joins or batched loads. Paginate every list endpoint with explicit limits and a deterministic sort order.
- **Indexes:** Capture `EXPLAIN ANALYZE` before and after any change. Run `ANALYZE` when estimated vs actual rows differ by an order of magnitude. Order composite indexes by equality columns first, then range or sort columns. Account for write overhead and revert indexes that do not improve the query plan.
- **Connection pools:** Maintain one pool per process with `instances * max < database max_connections`. Front serverless or autoscaling workloads with a pooling proxy (such as PgBouncer or RDS Proxy) instead of raising pool limits blindly.
- **Caching:** Cache only measured expensive reads with high read/write ratios. Include every varying input in the key (tenant, viewer, locale, permissions). Specify an invalidation strategy and acceptable staleness window. Prevent cache stampedes with in-flight promise coalescing or `stale-while-revalidate`. Cache negative lookups with a shorter TTL, never cache origin errors, and set eviction and memory bounds.

## 4. Verify with keep-or-revert discipline
- Change one variable at a time and re-measure using the exact same command and cache temperature (cold vs warm).
- Repeat measurements and confirm the delta exceeds run-to-run variance, not just a single mean.
- **Neutral is a revert:** Revert any change that yields no measurable gain, regresses another metric, or fails a test.
- Log every attempt (kept and reverted: baseline to result, verdict, and reason) so failed experiments are not retried.
