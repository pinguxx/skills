---
name: security-audit
description: Threat-focused security review for web apps, APIs, CLIs, and libraries. Audits XSS and DOM sinks, URL sanitization, prototype pollution, injection, path traversal, SSRF, auth/CORS/CSRF, untrusted payload bounds, and secret leaks.
---

# Security Audit

Audit the target files, diff, or PR for exploitable vulnerabilities and boundary gaps. Categorize every finding as **Critical**, **High**, **Medium**, or **Low** with exact `file:line`, attack vector, and minimal concrete fix.

## 1. Injection & DOM Sinks
- **XSS / HTML Injection:** Block unsanitized input reaching `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `dangerouslySetInnerHTML`, or server-rendered HTML templates without escaping.
- **Dangerous Code Execution:** Block `eval()`, `new Function()`, `setTimeout(string)`, `setInterval(string)`, and dynamic `<script>` injection.
- **URL & Protocol Sanitization:** Validate user-controlled `href`, `src`, `action`, and `formaction` values against an explicit protocol allowlist (`https:`, `http:`, `mailto:`, relative paths). Block `javascript:`, `vbscript:`, `data:text/html`, and `data:image/svg+xml` (including after trimming whitespace, control characters, and mixed casing).
- **Command & SQL Injection:** Block string interpolation into shell commands (`exec`, `execSync`, `sh -c`) or SQL queries. Use `execFile` / `spawn` with argument arrays and parameterized queries.

## 2. Object, Graph & Parser Safety
- **Prototype Pollution:** Any dynamic path traversal, JSON pointer, query parser, or deep merge helper must reject `__proto__`, `constructor`, and `prototype` keys (and use `Object.create(null)` or `Map` for untrusted dictionaries).
- **Unbounded Untrusted Input:** Enforce explicit limits on recursion depth (`maxDepth`), node/item counts, payload byte size, and regex backtracking (avoid nested quantifiers on untrusted strings).
- **Deserialization:** Treat parsed JSON, YAML, and external schemas as untrusted; validate shapes before use.

## 3. Filesystem, Network & Server Boundaries
- **Path Traversal:** Resolve user-supplied paths with `path.resolve` and verify the result starts with the intended root directory plus `path.sep` (and check symlinks with `fs.realpathSync` when serving files).
- **SSRF:** Validate outbound URLs against scheme allowlists and block private/loopback/link-local IP ranges (`127.0.0.0/8`, `10.0.0.0/8`, `169.254.169.254`, `::1`) when fetching user-supplied URLs.
- **Auth, CORS & CSRF:** Verify authz checks happen on every protected route (not just in the UI), never reflect arbitrary `Origin` headers with `Access-Control-Allow-Credentials: true`, and protect cookie-authenticated state-changing endpoints against CSRF.
- **Error Leakage:** Return generic error messages to clients; never expose stack traces, SQL errors, or internal tokens in API responses.

## 4. Secrets, Supply Chain & Hygiene
- **Zero Secrets in Repo:** Scan diffs and history for API keys, JWTs, private keys, `.env` files, or hardcoded credentials. Secrets must come from environment variables or a secret store.
- **Dependencies:** Flag unnecessary new runtime dependencies, unpinned or suspicious install scripts, and known vulnerable versions.
- **Edge & Sandbox Isolation:** Ensure Edge/serverless functions do not leak cross-request state in module-level globals.

## 5. Verification
- Add or run regression tests proving each fixed attack vector is rejected.
- Run the repo's security/unit tests and static checks, and report exact pass/fail results.
