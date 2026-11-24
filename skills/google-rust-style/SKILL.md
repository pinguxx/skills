---
name: google-rust-style
description: Audits and refactors Rust code against the Google Rust Style Guide, covering imports, ownership, signatures, traits, concurrency, naming, and idioms. Includes an automated Python scanner.
---

# Google Rust Style Guide audit

Audit, compare, and refactor Rust crates against the official Google Rust Style Guide. Prioritize readability and safe large-scale refactoring over short keystrokes. Classify every deviation as **Blocking**, **Important**, or **Nit** with exact `file:line` references and drop-in fixes.

---

## 1. Automated static scan
Run the bundled scanner on a target directory or `.rs` file to surface mechanical violations before manual inspection:

```bash
python skills/google-rust-style/scripts/audit_google_style.py <target-dir-or-file>
```

If the skill is installed globally, point Python to the installed `scripts/audit_google_style.py` path in your agent skills directory.

---

## 2. Core rules by domain

### Code organization and imports (Important)
- Keep non-leaf modules (`mod.rs` or hub files) limited to `mod` declarations and `pub use` re-exports. Place implementation logic in leaf modules named after their primary abstraction.
- Forbid glob imports (`use foo::*;`). Explicit imports keep refactoring safe. Exceptions: `use super::*;` inside test modules, `use Enum::*;` inside a method body on that enum, and `pub use sub::*;` in a non-leaf facade.
- Limit each `use` statement to one module (`use foo::bar;` and `use foo::baz::Qux;` separately, without nested `::` inside `{...}`).
- Qualify imported free functions with their module name (`fs::read(path)`, `mem::replace(&mut a, b)`), and import types unqualified (`HashMap`, not `collections::HashMap`) unless disambiguating common names such as `io::Result`.

### Formatting and unsafe code (Blocking)
- Enforce default `rustfmt` (`cargo fmt --check`). Reserve `#[rustfmt::skip]` strictly for intentional tables or generated blocks.
- Keep `unsafe` encapsulated behind safe APIs, and require an adjacent `// SAFETY:` comment explaining every precondition.

### Ownership and signatures (Important)
- Prefer unique ownership (`T`, `Box<T>`) and borrows (`&T`, `&mut T`) over `Rc` or `Arc` unless multi-threaded or cyclic ownership requires shared handles.
- Accept borrowed views in parameters: `&str` instead of `&String`, `&[T]` instead of `&Vec<T>`, `&T` instead of `&Box<T>`, and `Option<&T>` instead of `&Option<T>`.
- Replace ambiguous `bool` parameters with clear two-variant enums, or document inline call-site booleans when changing the signature is out of scope.
- Match failure semantics: `Option<T>` for self-evident absence, `Result<T, E>` for recoverable failures, and `panic!` only for broken internal invariants.

### Types, traits, and metaprogramming (Important)
- Use newtypes (`struct UserId(u64);`) instead of bare aliases for distinct semantic domains. Use named struct fields instead of multi-field positional tuples.
- Prefer standard traits (`FromStr`, `Default`, `Display`, `Debug`, `Hash`, `PartialEq`, `Ord`) and `#[derive(...)]` over custom conversion names like `from_string`.
- Mark options structs with `Default`, pure helper functions and critical handles with `#[must_use]`, and evolving public enums with `#[non_exhaustive]`.
- Implement paired APIs together (if `len(&self)` exists, implement `is_empty(&self)`).
- Prefer generics (`impl Trait` or `T: Trait`) over `dyn Trait` when static dispatch fits. Reserve macros (`macro_rules!`, then `proc_macro`) for patterns regular functions and traits cannot express cleanly.

### Naming, documentation, and idioms (Nit)
- Follow conversion prefixes: `as_*` for cheap borrows (`&self -> &T`), `to_*` for conversions (`&self -> T`), and `into_*` for consuming conversions (`self -> T`). Name constructors `new`, `new_with_*`, and fallible ones `try_new`.
- Document public items with `///` (covering `# Panics`, `# Errors`, and `# Safety` where relevant) and crate or module overviews with `//!`.
- Prefer `if let` or `match` over check-then-unwrap (`if x.is_some() { x.unwrap() }`), `format!` or `write!` over chained `+` concatenation, and informative messages on assertions in tests.
- Avoid `std::panic::catch_unwind` outside FFI boundaries.

---

## 3. Audit workflow
1. Run `audit_google_style.py` on the target crate.
2. Review imports, module hierarchy, and public function signatures across changed `.rs` files.
3. Audit types, traits, `unsafe` comments, and error paths.
4. Apply refactors cleanly without altering public behavior unless requested.

---

## Verification
After refactoring, run:
- `python skills/google-rust-style/scripts/audit_google_style.py <target-dir>`
- `cargo fmt --check`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `cargo test --workspace`
