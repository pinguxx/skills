#!/usr/bin/env python3
"""Compute WCAG 2.2 AA contrast ratios for hex CSS custom properties in a stylesheet.

Usage:
    python3 check_contrast.py path/to/tokens.css [--min-text 4.5] [--min-ui 3.0]
"""

import re
import sys
from pathlib import Path


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rel_luminance(hex_color: str) -> float:
    r, g, b = hex_to_rgb(hex_color)
    channels = []
    for c in (r, g, b):
        s = c / 255.0
        channels.append(s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(a: str, b: str) -> float:
    l1, l2 = sorted((rel_luminance(a), rel_luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def extract_blocks(css: str) -> dict[str, dict[str, str]]:
    clean = re.sub(r"/\*[\s\S]*?\*/", "", css)
    blocks: dict[str, dict[str, str]] = {}
    for m in re.finditer(r"([^{}@]+)\{([^{}]+)\}", clean):
        sel = " ".join(m.group(1).split())
        tokens = dict(re.findall(r"(--[a-zA-Z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\s*;", m.group(2)))
        if tokens:
            blocks.setdefault(sel, {}).update(tokens)
    return blocks


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 check_contrast.py <tokens.css>", file=sys.stderr)
        return 2
    css_path = Path(sys.argv[1])
    if not css_path.exists():
        print(f"File not found: {css_path}", file=sys.stderr)
        return 2

    blocks = extract_blocks(css_path.read_text(encoding="utf-8"))
    failures = 0

    for sel, tokens in blocks.items():
        surfaces = {k: v for k, v in tokens.items() if any(w in k for w in ("surface", "bg", "canvas", "card", "elevated", "muted")) and "text" not in k}
        texts = {k: v for k, v in tokens.items() if "text" in k}
        if not surfaces or not texts:
            continue
        print(f"\n=== {sel} ({len(texts)} text x {len(surfaces)} surface tokens) ===")
        for tk, tv in sorted(texts.items()):
            if "inverse" in tk or "tooltip" in tk:
                continue
            for sk, sv in sorted(surfaces.items()):
                if any(skip in sk for skip in ("border", "hover", "tooltip", "skeleton", "code", "tint")):
                    continue
                ratio = contrast_ratio(tv, sv)
                status = "AA-TEXT" if ratio >= 4.5 else ("UI-ONLY" if ratio >= 3.0 else "FAIL")
                if status != "AA-TEXT":
                    failures += 1
                    print(f"  [{status:7}] {ratio:5.2f}:1  {tk} ({tv}) on {sk} ({sv})")

    if failures:
        print(f"\nFound {failures} text-on-surface pairing(s) below 4.5:1.")
        return 1
    print("\nAll checked text-on-surface token pairings pass WCAG 2.2 AA (>= 4.5:1).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
