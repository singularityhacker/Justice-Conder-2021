#!/usr/bin/env python3
"""Point every HTML page at the cubes icon, consultant CSS, and era labels."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

THEME_SCRIPT = re.compile(
    r"\s*<script>\s*\(function \(\) \{[\s\S]*?jc-site-theme[\s\S]*?</script>\s*",
    re.I,
)
GOOGLE_FONTS = re.compile(
    r"\s*<link rel=\"preload\"\s+href=\"https://fonts\.googleapis\.com/css\?family=[^\"]+\"[\s\S]*?/>\s*",
    re.I,
)
SWITCHER = re.compile(r"\s*<script src=\"(?:\.\./)?js/theme-switcher\.js\"></script>\s*")
THEMES_CSS = re.compile(r"\s*<link rel=\"stylesheet\" href=\"(?:\.\./)?css/themes\.css\"[^>]*>\s*")


def chrome_head(prefix: str) -> str:
    return (
        f'\t<link rel="icon" href="{prefix}images/icon/cubes-icon.gif" type="image/gif" />\n'
        f'\t<link rel="shortcut icon" href="{prefix}images/icon/cubes-icon.gif" />'
    )


def apply(text: str, prefix: str) -> str:
    text = THEME_SCRIPT.sub("\n", text)
    text = GOOGLE_FONTS.sub("\n", text)
    text = SWITCHER.sub("\n", text)
    text = THEMES_CSS.sub("\n", text)
    text = text.replace(
        f'<link rel="shortcut icon" href="{prefix}images/icon/favicon.ico" />',
        chrome_head(prefix),
    )
    text = text.replace(
        f'src="{prefix}images/logo.webp" alt="" height="40px" width="55px" loading="lazy"',
        f'src="{prefix}images/icon/cubes-icon.gif" alt="Justice Conder" height="40" width="40"',
    )
    text = text.replace(
        f'src="{prefix}images/logo.webp"',
        f'src="{prefix}images/icon/cubes-icon.gif"',
    )
    if f'css/consultant.css' not in text and f"{prefix}css/blog.css" in text:
        text = text.replace(
            f'<link rel="stylesheet" href="{prefix}css/blog.css" type="text/css" />',
            f'<link rel="stylesheet" href="{prefix}css/blog.css" type="text/css" />\n'
            f'\t<link rel="stylesheet" href="{prefix}css/consultant.css" type="text/css" />',
        )
    text = text.replace('blog-tag--singularity-hacker">Singularity Hacker<', 'blog-tag--singularity-hacker">Futurism<')
    text = text.replace('blog-tag--medium">Medium<', 'blog-tag--medium">Project management<')
    text = text.replace('blog-tag--0xjustice">0xjustice<', 'blog-tag--0xjustice">Crypto<')
    return text


def main() -> int:
    files = [ROOT / "blog.html"]
    files += list((ROOT / "blog").glob("*.html"))
    extra = ROOT / "resume-print.html"
    if extra.exists():
        files.append(extra)
    n = 0
    for path in files:
        prefix = "" if path.parent == ROOT else "../"
        old = path.read_text(encoding="utf-8")
        new = apply(old, prefix)
        if new != old:
            path.write_text(new, encoding="utf-8")
            n += 1
    print(f"updated chrome on {n} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
