#!/usr/bin/env python3
"""Restore classic chrome: yellow favicon, logo.webp, themes, look-switcher."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CUBES_FAVICONS = re.compile(
    r'\s*<link rel="icon" href="(?:\.\./)?images/icon/cubes-icon\.gif"[^>]*>\s*'
    r'<link rel="shortcut icon" href="(?:\.\./)?images/icon/cubes-icon\.gif"[^>]*>\s*',
    re.I,
)
CUBES_SHORTCUT = re.compile(
    r'<link rel="shortcut icon" href="((?:\.\./)?)images/icon/cubes-icon\.gif"[^>]*>',
    re.I,
)
CONSULTANT = re.compile(
    r'\s*<link rel="stylesheet" href="(?:\.\./)?css/consultant\.css"[^>]*>\s*',
    re.I,
)
CUBES_LOGO = re.compile(
    r'src="((?:\.\./)?)images/icon/cubes-icon\.gif"(?:\s+alt="Justice Conder")?(?:\s+height="40")?(?:\s+width="40")?'
)

THEME_SCRIPT = """\t<script>
\t(function () {
\t\ttry {
\t\t\tvar q = new URLSearchParams(location.search).get("theme");
\t\t\tvar t = q || localStorage.getItem("jc-site-theme");
\t\t\tif (t) document.documentElement.setAttribute("data-theme", t);
\t\t} catch (e) {}
\t})();
\t</script>
"""

FONTS = """\t<link rel="preload"
\t\thref="https://fonts.googleapis.com/css?family=Open+Sans:400,300,600,300italic,400italic,600italic,700,700italic,800,800italic&display=swap"
\t\tas="style" onload="this.rel='stylesheet'" />
\t<link rel="preload"
\t\thref="https://fonts.googleapis.com/css?family=Raleway:400,100,100italic,200italic,200,300,300italic,400italic,500,500italic,600,600italic,700italic,900italic,900,800,700,800italic&display=swap"
\t\tas="style" onload="this.rel='stylesheet'" />
"""


def apply(text: str, prefix: str) -> str:
    text = CUBES_FAVICONS.sub(
        f'\n\t<link rel="shortcut icon" href="{prefix}images/icon/favicon.ico" />\n',
        text,
    )
    text = CUBES_SHORTCUT.sub(
        f'<link rel="shortcut icon" href="{prefix}images/icon/favicon.ico" />',
        text,
    )
    text = CONSULTANT.sub("\n", text)
    text = CUBES_LOGO.sub(
        r'src="\1images/logo.webp" alt="" height="40px" width="55px" loading="lazy"',
        text,
    )

    if "bulma.min.css" not in text and f"{prefix}css/style.css" in text:
        text = text.replace(
            f'<link rel="stylesheet" href="{prefix}css/style.css" type="text/css" />',
            '<link rel="stylesheet" href="https://unpkg.com/bulma@0.9.1/css/bulma.min.css" type="text/css" />\n'
            f'\t<link rel="stylesheet" href="{prefix}css/style.css" type="text/css" />',
        )

    if "fonts.googleapis.com" not in text and "</head>" in text:
        text = text.replace("</head>", f"{FONTS}</head>")

    return text


def main() -> int:
    files = [ROOT / "blog.html"]
    files += list((ROOT / "blog").glob("*.html"))
    n = 0
    for path in files:
        prefix = "" if path.parent == ROOT else "../"
        old = path.read_text(encoding="utf-8")
        new = apply(old, prefix)
        if new != old:
            path.write_text(new, encoding="utf-8")
            n += 1
    print(f"restored chrome on {n} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
