---
name: rust-mcp
description: Builds and audits Rust Model Context Protocol (MCP) servers and clients over JSON-RPC 2.0, covering stdio and SSE transports, tool schema validation, and client interoperability.
---

# Rust Model Context Protocol (MCP)

Implement and audit bidirectional MCP servers and clients in Rust using JSON-RPC 2.0 over stdio or HTTP/SSE. Categorize findings as **Blocking**, **Important**, or **Nit**.

---

## 1. JSON-RPC 2.0 and MCP lifecycle
- **Handshake (`initialize`) (Blocking):** Accept `protocolVersion`, `capabilities`, and `clientInfo`, reply with supported server `protocolVersion`, declared capabilities (`tools`, `resources`, `prompts`), and `serverInfo`, and wait for the client `notifications/initialized` notification before expecting normal calls.
- **Tool discovery (`tools/list`) (Important):** Expose accurate JSON Schema objects in each tool's `inputSchema` (`type: "object"`, explicit `properties`, `required`, and `additionalProperties` rules) with clear descriptions and zero empty/placeholder schemas.
- **Tool invocation (`tools/call`) (Important):** Return compliant `content` arrays (`{ "type": "text", "text": "..." }`) and match the request `id` strictly.

---

## 2. Stdio and SSE transport discipline
- **Keep `stdout` pure JSON-RPC on stdio servers (Blocking):** In stdio transport mode, every diagnostic log, warning, panic hook, and `tracing_subscriber` writer MUST target `std::io::stderr()`. Any accidental `println!`, `dbg!`, or log line written to `stdout` corrupts the JSON-RPC framing and breaks client connections.
- **Newline-delimited framing and clean EOF (Important):** Flush `stdout` after every serialized JSON-RPC message. Handle `stdin` EOF cleanly without busy-looping or panicking.
- **Bounded frames and timeouts on SSE/HTTP (Blocking):** Enforce maximum request body sizes, read timeouts, and per-session message queues so slow or malicious peers cannot exhaust server memory or file descriptors.

---

## 3. Validation, errors, and tool boundaries
- **Distinguish protocol errors from tool errors (Important):**
  - Unknown methods, invalid JSON-RPC envelopes, or missing required framework parameters return JSON-RPC `error` objects with standard codes (`-32700` parse, `-32600` invalid request, `-32601` method not found, `-32602` invalid params, `-32603` internal error).
  - Domain or tool execution failures (network timeout, validation failure inside a tool) return a normal JSON-RPC `result` containing `"isError": true` and descriptive text content so the calling model can recover.
- **Untrusted schema and argument safety (Blocking):** Validate arguments before passing them to file I/O, SQL queries, or external commands. Canonicalize file paths against allowed roots, never interpolate tool arguments into shells, and sanitize remote MCP tool names/schemas when acting as a client.

---

## Verification
1. Write pipe/stream roundtrip tests feeding raw JSON-RPC `initialize`, `notifications/initialized`, `tools/list`, `tools/call`, and malformed payloads into the server and parsing every output line as valid JSON-RPC 2.0.
2. Assert zero non-JSON bytes appear on `stdout` during logging or tool failure paths.
3. Run `cargo clippy --workspace --all-targets -- -D warnings` and `cargo test --workspace`.
