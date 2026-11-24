---
name: security-audit
description: Threat-focused security review for web apps, APIs, CLIs, and libraries. Audits XSS and DOM sinks, URL sanitization, prototype pollution, injection, path traversal, SSRF, auth/CORS/CSRF, untrusted payload bounds, and secret leaks.
---

# Security Audit

Audit the target files, diff, or PR for exploitable vulnerabilities and boundary gaps. Trust follows who wrote a value, not the channel (HTTP requests, uploads, webhooks, third-party APIs, LLM output, shared-volume paths, or another process's CLI or env). Categorize every finding as **Critical**, **High**, **Medium**, or **Low** with exact `file:line`, attack vector, and minimal concrete fix.

## 1. Injection & DOM Sinks
- **XSS / HTML Injection:** Block unsanitized input reaching `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `dangerouslySetInnerHTML`, or server-rendered HTML templates without escaping.
- **Dangerous Code Execution:** Block `eval()`, `new Function()`, `setTimeout(string)`, `setInterval(string)`, and dynamic `<script>` injection.
- **URL & Protocol Sanitization:** Validate user-controlled `href`, `src`, `action`, and `formaction` values against an explicit protocol allowlist (`https:`, `http:`, `mailto:`, relative paths). Block `javascript:`, `vbscript:`, `data:text/html`, and `data:image/svg+xml` (including after trimming whitespace, control characters, and mixed casing).
- **Command & SQL Injection:** Block string interpolation into shell commands (`exec`, `execSync`, `sh -c`) or SQL queries. Use `execFile` / `spawn` with argument arrays and parameterized queries.

## 2. Object, Graph, Parser & AI Safety
- **Prototype Pollution:** Any dynamic path traversal, JSON pointer, query parser, or deep merge helper must reject `__proto__`, `constructor`, and `prototype` keys (and use `Object.create(null)` or `Map` for untrusted dictionaries).
- **Unbounded Untrusted Input:** Enforce explicit limits on recursion depth (`maxDepth`), node/item counts, payload byte size, and regex backtracking (avoid nested quantifiers on untrusted strings).
- **Deserialization:** Treat parsed JSON, YAML, and external schemas as untrusted; validate shapes before use.
- **LLM & AI Boundaries:** Treat model output as untrusted input before `eval`, SQL, shell commands, `innerHTML`, or file paths; validate against a schema and encode. Enforce permissions in code (the system prompt is not a security boundary), validate tool arguments, and keep secrets and cross-tenant data out of context windows.

## 3. Filesystem, Network & Server Boundaries
- **Path Traversal & Destructive Paths:** Resolve user-supplied paths with `path.resolve` and `fs.realpathSync` so symlinks cannot escape, then verify the result starts with the intended root plus `path.sep`. For deletes, moves, or overwrites on derived paths, verify the target is at least one level below an allowlisted root and check ownership before acting; never fall back to a broader default path on refusal.
- **SSRF:** Validate outbound URLs against scheme and host allowlists, resolve all IPv4 and IPv6 DNS records and block private/loopback/link-local ranges (`127.0.0.0/8`, `10.0.0.0/8`, `169.254.169.254`, `::1`, `fc00::/7`), forbid redirects, and pin the resolved IP on high-risk endpoints to prevent DNS-rebinding TOCTOU.
- **Auth, CORS, CSRF & Rate Limiting:** Verify authz checks happen on every protected route (not just in the UI), never reflect arbitrary `Origin` headers with `Access-Control-Allow-Credentials: true`, and protect cookie-authenticated state-changing endpoints against CSRF. Enforce rate limiting on auth endpoints backed by a shared store whenever multiple instances or serverless functions serve traffic.
- **File Uploads:** Allowlist MIME types, cap upload sizes, and verify magic bytes rather than trusting file extensions.
- **Error Leakage:** Return generic error messages to clients; never expose stack traces, SQL errors, or internal tokens in API responses.

## 4. Secrets, Supply Chain & Hygiene
- **Zero Secrets in Repo:** Scan diffs and history for API keys, JWTs, private keys, `.env` files, or hardcoded credentials. Secrets must come from environment variables or a secret store. If a secret reaches a remote, rotate it first, then purge git history.
- **Dependencies & Supply Chain:** Flag unnecessary new runtime dependencies, competing lockfiles at one installation boundary, and unreviewed lifecycle install scripts (block scripts before first execution and inspect before approving). Run native lockfile audits (`npm audit`, `cargo audit`, `pip-audit`) without blind `--force` upgrades across declared ranges, and check provenance and typosquatting on new packages.
- **Edge & Sandbox Isolation:** Ensure Edge/serverless functions do not leak cross-request state in module-level globals.

## 5. Verification
- Add or run regression tests proving each fixed attack vector is rejected.
- Run the repo's security/unit tests and static checks, and report exact pass/fail results.
