#!/usr/bin/env python3
"""Deterministic scanner for mechanical unslop rules (3, 4, 5, 9, 15, 18, 21, 28).

Usage:
    python3 check_unslop.py <file1.md> [file2.md ...]

Exits 0 if no mechanical violations are found, 1 otherwise.
Skips fenced code blocks and inline code spans so technical identifiers do not false-positive.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BANNED_WORDS = (
    "additionally",
    "crucial",
    "delve",
    "enhance",
    "foster",
    "landscape",
    "pivotal",
    "showcase",
    "testament",
    "underscore",
    "vibrant",
)

METAPHOR_NOUNS = (
    "substrate",
    "wedge",
    "vector",
    "nexus",
    "primitive",
    "harness",
    "surface",
    "scaffolding",
    "paradigm",
    "ratchet",
    "north star",
    "flywheel",
)

RULES: list[tuple[int, re.Pattern[str], str]] = [
    (3, re.compile(r"\b(" + "|".join(BANNED_WORDS) + r")\b", re.I), "AI vocabulary"),
    (4, re.compile(r"\b(serves as|stands as|boasts)\b", re.I), "use 'is' or 'has'"),
    (5, re.compile(r"\bnot just\b[^.\n]{1,80}\bbut\b", re.I), "avoid 'not just X, but Y'"),
    (9, re.compile(r"[\u2014\u2013]|\s-\s"), "no em/en dash or spaced hyphen"),
    (15, re.compile(r"[\u201c\u201d\u2018\u2019]"), "use straight quotes"),
    (18, re.compile(r"\b(in order to|it is important to note)\b", re.I), "cut filler"),
    (21, re.compile(r"\b(" + "|".join(METAPHOR_NOUNS) + r")\b", re.I), "abstract metaphor noun"),
    (28, re.compile(r"\b(utilize|utilizes|utilized|utilizing|leverage|leverages|leveraged|leveraging)\b", re.I), "use plain word ('use')"),
]

INLINE_CODE_RE = re.compile(r"`[^`]*`")
URL_RE = re.compile(r"https?://\S+")


def strip_inline_code(line: str) -> str:
    return URL_RE.sub("", INLINE_CODE_RE.sub("", line))


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    in_fence = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prose = strip_inline_code(raw)
        # Skip markdown table separator rows and list bullets like "- item"
        if re.match(r"^\s*\|?[\s:|-]+\|?\s*$", prose):
            continue
        for rule_id, pattern, label in RULES:
            for m in pattern.finditer(prose):
                if rule_id == 9 and m.group(0) == " - " and re.match(r"^[>\s]*$", prose[: m.start()]):
                    continue
                findings.append(
                    f"{path}:{lineno}: [rule {rule_id}] {label}: {m.group(0)!r}"
                )
    return findings


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python3 check_unslop.py <file1> [file2 ...]", file=sys.stderr)
        return 2

    all_findings: list[str] = []
    for arg in argv:
        p = Path(arg)
        if not p.is_file():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 2
        all_findings.extend(scan_file(p))

    if all_findings:
        for line in all_findings:
            print(line)
        print(f"\nFound {len(all_findings)} mechanical unslop violation(s).")
        return 1

    print(f"OK: 0 mechanical unslop violations across {len(argv)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
