#!/usr/bin/env python3
"""
Google Rust Style Guide automated auditor.

Scans Rust source files for common Google Rust Style Guide violations:
  - Glob imports (use foo::*)
  - Rigid borrowed parameters (&String, &Vec, &Box, &Option)
  - Check-then-unwrap patterns (.is_some() / .is_ok() followed by .unwrap())
  - Unsafe code without // SAFETY: explanation comment
  - std::panic::catch_unwind usage in production code
  - Multi-module paths inside a single use statement (use foo::{a, b::c})
  - Implementation of len() without is_empty()
  - String concatenation with chained '+'
"""

import re
import sys
from pathlib import Path


class StyleViolation:
    def __init__(self, file_path: str, line_no: int, rule: str, severity: str, message: str, snippet: str):
        self.file_path = file_path
        self.line_no = line_no
        self.rule = rule
        self.severity = severity  # Blocking, Important, Nit
        self.message = message
        self.snippet = snippet.strip()

    def __str__(self) -> str:
        return (
            f"[{self.severity}] {self.file_path}:{self.line_no} ({self.rule})\n"
            f"  {self.message}\n"
            f"  Code: {self.snippet}\n"
        )


def audit_file(file_path: Path) -> list:
    violations = []
    is_test_file = "tests" in file_path.parts or file_path.name.endswith("_test.rs")
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as exc:
        return [StyleViolation(str(file_path), 1, "FileRead", "Blocking", f"Could not read file: {exc}", "")]

    content = "".join(lines)

    # Check 1: pub fn len(&self) without pub fn is_empty(&self)
    has_len = bool(re.search(r"pub\s+fn\s+len\s*\(&self", content))
    has_is_empty = bool(re.search(r"pub\s+fn\s+is_empty\s*\(&self", content))
    if has_len and not has_is_empty:
        violations.append(
            StyleViolation(
                str(file_path),
                1,
                "API-Sets-Together",
                "Important",
                "Type implements pub fn len(&self) without pub fn is_empty(&self).",
                "pub fn len(&self)",
            )
        )

    in_test_mod = False
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if "#[cfg(test)]" in stripped:
            in_test_mod = True

        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        # Check 2: Glob imports
        if re.search(r"^\s*(pub\s+)?use\s+.*::\*\s*;", line):
            is_facade_reexport = stripped.startswith("pub use ") and file_path.name in {"lib.rs", "mod.rs"}
            if (
                not is_test_file
                and not in_test_mod
                and not is_facade_reexport
                and "super::*" not in line
                and "prelude::*" not in line
            ):
                violations.append(
                    StyleViolation(
                        str(file_path),
                        i,
                        "No-Glob-Imports",
                        "Important",
                        "Glob import detected. Name imported items explicitly.",
                        line,
                    )
                )

        # Check 3: Rigid container references in function signatures
        if re.search(r"fn\s+[a-zA-Z0-9_]+\s*\([^)]*&\s*String\b", line):
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "Flexible-References",
                    "Important",
                    "Parameter accepts '&String'. Prefer '&str'.",
                    line,
                )
            )

        if re.search(r"fn\s+[a-zA-Z0-9_]+\s*\([^)]*&\s*Vec\s*<", line):
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "Flexible-References",
                    "Important",
                    "Parameter accepts '&Vec<T>'. Prefer '&[T]'.",
                    line,
                )
            )

        if re.search(r"fn\s+[a-zA-Z0-9_]+\s*\([^)]*&\s*Box\s*<", line):
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "Flexible-References",
                    "Important",
                    "Parameter accepts '&Box<T>'. Borrow '&T' directly.",
                    line,
                )
            )

        if re.search(r"fn\s+[a-zA-Z0-9_]+\s*\([^)]*&\s*Option\s*<", line):
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "Flexible-References",
                    "Important",
                    "Parameter accepts '&Option<T>'. Prefer 'Option<&T>'.",
                    line,
                )
            )

        # Check 4: Unsafe code without adjacent // SAFETY: comment
        if re.search(r"\bunsafe\s*\{", line) or re.search(r"\bunsafe\s+fn\b", line):
            prev_lines = "".join(lines[max(0, i - 5):i - 1])
            if "SAFETY:" not in prev_lines:
                violations.append(
                    StyleViolation(
                        str(file_path),
                        i,
                        "Unsafe-Safety-Comment",
                        "Blocking",
                        "Unsafe block or function missing preceding '// SAFETY:' comment.",
                        line,
                    )
                )

        # Check 5: Multi-module use statements (e.g. use foo::{bar, baz::qux};)
        if re.search(r"^\s*(pub\s+)?use\s+[^{;]+::\{[^}]*::", line):
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "Single-Module-Use",
                    "Nit",
                    "A use statement should import from one module. Split nested '::' paths.",
                    line,
                )
            )

        # Check 6: catch_unwind prohibition
        if "catch_unwind" in line and not is_test_file and not in_test_mod:
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "No-Catch-Unwind",
                    "Important",
                    "Avoid panic::catch_unwind outside FFI boundaries.",
                    line,
                )
            )

        # Check 7: Check-then-unwrap on the same line
        if re.search(r"\.(is_some|is_ok)\(\).*\.unwrap\(\)", line) and not is_test_file and not in_test_mod:
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "Pattern-Matching-Over-Unwrap",
                    "Important",
                    "Replace check-then-unwrap with 'if let' or 'match'.",
                    line,
                )
            )

        # Check 8: Multiple string concatenations with '+'
        if re.search(r'"\s*\+\s*&?[a-zA-Z0-9_.]+\s*\+\s*"', line):
            violations.append(
                StyleViolation(
                    str(file_path),
                    i,
                    "Format-Over-Plus",
                    "Nit",
                    "Prefer format!(...) or write! over chained '+' string concatenation.",
                    line,
                )
            )

    return violations


def scan_target(target: str) -> list:
    root = Path(target)
    if root.is_file():
        return audit_file(root) if root.suffix == ".rs" else []

    all_violations = []
    skip_dirs = {"target", ".git", "node_modules", ".venv", "venv", "dist", "build"}
    for path in root.rglob("*.rs"):
        rel_parts = path.relative_to(root).parts[:-1]
        if any(part in skip_dirs or part.startswith(".") for part in rel_parts):
            continue
        all_violations.extend(audit_file(path))
    return all_violations


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Scanning Rust code for Google Rust Style Guide violations: {target}")
    violations = scan_target(target)

    if not violations:
        print("\n[PASS] 0 Google Rust Style Guide violations found.")
        sys.exit(0)

    blockers = [v for v in violations if v.severity == "Blocking"]
    importants = [v for v in violations if v.severity == "Important"]
    nits = [v for v in violations if v.severity == "Nit"]

    print(
        f"\nFound {len(violations)} violations "
        f"({len(blockers)} Blocking, {len(importants)} Important, {len(nits)} Nits):\n"
    )
    for v in violations:
        print(v)

    sys.exit(1 if blockers else 0)


if __name__ == "__main__":
    main()
