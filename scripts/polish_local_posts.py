#!/usr/bin/env python3
"""Clean leftover X chrome in locally published posts and rebuild the listing."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
LISTING = ROOT / "blog.html"
POSTS = BLOG / "posts.json"

SLUGS = [
    "0xjustice-efficient-dao-design",
    "0xjustice-introducing-skillshop",
    "0xjustice-the-new-machine-economy",
    "0xjustice-agent-economics-skillshop-is-go",
    "clawbank-status-update",
    "0xjustice-building-tokenized-systems-in-2026",
]


def abs_x(url: str) -> str:
    if url.startswith("/"):
        return "https://x.com" + url
    return url


def polish(html_text: str) -> str:
    html_text = re.sub(r'<p>\]\([^)]+\)</p>\s*', "", html_text)
    html_text = re.sub(r"<p>(!|\||Show more|Article|Views)</p>\s*", "", html_text)
    html_text = html_text.replace('href="/singularityhack', 'href="https://x.com/singularityhack')
    html_text = html_text.replace('href="/clawbankco', 'href="https://x.com/clawbankco')
    html_text = html_text.replace('href="/openclaw', 'href="https://x.com/openclaw')
    html_text = html_text.replace('href="/mntruell', 'href="https://x.com/mntruell')
    html_text = html_text.replace("<h2>Why this matters for</h2>\n<p>ClawBank</p>", "<h2>Why this matters for ClawBank</h2>")
    html_text = html_text.replace("<h2>The</h2>\n<p>ClawBank</p>\n<p>Token</p>", "<h2>The ClawBank Token</h2>")
    html_text = html_text.replace("<p>Made for...</p>", "<h3>Made for</h3>")
    html_text = html_text.replace("<p>bash</p>\n", "")
    html_text = html_text.replace("<p>1. Tokens as Money</p>", "<h3>1. Tokens as Money</h3>")
    html_text = html_text.replace("<p>2. Builder Coins</p>", "<h3>2. Builder Coins</h3>")
    html_text = html_text.replace("<p>3. Tokens for Nothing</p>", "<h3>3. Tokens for Nothing</h3>")
    html_text = html_text.replace("<p>4. Tokenized Intelligent Systems</p>", "<h3>4. Tokenized Intelligent Systems</h3>")
    html_text = html_text.replace("<p>Build It Yourself</p>", "<h3>Build It Yourself</h3>")
    html_text = html_text.replace("<p>Pay an Agent (Outsource)</p>", "<h3>Pay an Agent (Outsource)</h3>")
    html_text = html_text.replace("<p>Buy (Skills)</p>", "<h3>Buy (Skills)</h3>")
    html_text = html_text.replace("<p>Job Hunter Template</p>", "<h3>Job Hunter Template</h3>")
    html_text = html_text.replace("<p>The Architect Agent</p>", "<h3>The Architect Agent</h3>")
    html_text = html_text.replace("<p>8004 Reputation</p>", "<h3>8004 Reputation</h3>")
    html_text = html_text.replace("<p>Marketplace Dashboard</p>", "<h3>Marketplace Dashboard</h3>")
    html_text = html_text.replace("<p>Automatic Code Quality Scans</p>", "<h3>Automatic Code Quality Scans</h3>")

    # Collapse X display-name / handle / date leftovers into a cite line when
    # they sit immediately before a real paragraph.
    html_text = re.sub(
        r"<p>0xJustice\.eth[^<]*</p>\s*<p>@singularityhack</p>\s*<p><a href=\"([^\"]+)\">([^<]+)</a></p>\s*",
        r'<p class="blog-embed-cite"><a href="\1">@singularityhack · \2</a></p>\n',
        html_text,
    )
    html_text = re.sub(
        r"<p>ClawBank Agent \(Manfred\)</p>\s*<p>@clawbankco</p>\s*<p><a href=\"([^\"]+)\">([^<]+)</a></p>\s*(?:<p>Automated by <a href=\"[^\"]+\">@singularityhack</a></p>\s*)?",
        r'<p class="blog-embed-cite"><a href="\1">@clawbankco · \2</a></p>\n',
        html_text,
    )
    html_text = re.sub(
        r"<p>OpenClaw🦞</p>\s*<p>@openclaw</p>\s*<p><a href=\"([^\"]+)\">([^<]+)</a></p>\s*",
        r'<p class="blog-embed-cite"><a href="\1">@openclaw · \2</a></p>\n',
        html_text,
    )
    html_text = re.sub(
        r"<p>Michael Truell</p>\s*<p>@mntruell</p>\s*<p><a href=\"([^\"]+)\">([^<]+)</a></p>\s*",
        r'<p class="blog-embed-cite"><a href="\1">@mntruell · \2</a></p>\n',
        html_text,
    )
    html_text = re.sub(
        r"<p><a href=\"https://twitter.com/hongkim__\"><img alt=\"User Avatar\"[^>]+/></a></p>\s*<p><a href=\"https://twitter.com/hongkim__\">Hong Kim</a></p>\s*<p><a href=\"https://twitter.com/hongkim__\">@hongkim__</a></p>\s*<p><a href=\"([^\"]+)\"></a></p>\s*<p>([^<]+)</p>\s*<p><a href=\"[^\"]+\">\s*161</a>\[</p>\s*<p>7:11 PM • Jul 8, 2022</p>\s*<p>\]\([^)]+\)</p>",
        r'<blockquote><p>\2</p><p><a href="\1">@hongkim__ · Jul 8, 2022</a></p></blockquote>',
        html_text,
    )
    html_text = re.sub(
        r"<p><a href=\"https://twitter.com/DrNickA\"><img alt=\"User Avatar\"[^>]+/></a></p>\s*<p><a href=\"https://twitter.com/DrNickA\">Nick Almond</a></p>\s*<p><a href=\"https://twitter.com/DrNickA\">@DrNickA</a></p>\s*<p><a href=\"([^\"]+)\"></a></p>\s*<p>([^<]+)</p>\s*<p><a href=\"[^\"]+\">\s*41</a>\[</p>\s*<p>1:56 AM • Aug 4, 2022</p>\s*<p>\]\([^)]+\)</p>",
        r'<blockquote><p>\2</p><p><a href="\1">@DrNickA · Aug 4, 2022</a></p></blockquote>',
        html_text,
    )
    html_text = re.sub(
        r"<p><a href=\"https://twitter.com/chaserchapman\"><img alt=\"User Avatar\"[^>]+/></a></p>\s*<p><a href=\"https://twitter.com/chaserchapman\">Chase Chapman</a></p>\s*<p><a href=\"https://twitter.com/chaserchapman\">@chaserchapman</a></p>\s*<p><a href=\"([^\"]+)\"></a></p>\s*<p>([\s\S]*?)</p>\s*<p><a href=\"[^\"]+\">\s*180</a>\[</p>\s*<p>2:16 PM • Aug 8, 2022</p>\s*<p>\]\([^)]+\)</p>",
        r'<blockquote><p>\2</p><p><a href="\1">@chaserchapman · Aug 8, 2022</a></p></blockquote>',
        html_text,
    )
    html_text = re.sub(r"\n{3,}", "\n\n", html_text)
    return html_text


def card_html(post: dict) -> str:
    cover = post.get("cover") or ""
    cover_block = ""
    if cover:
        src = cover if cover.startswith("blog/") else f"blog/{cover}"
        cover_block = (
            f'\n\t\t\t\t<div class="blog-card-cover">'
            f'\n\t\t\t\t\t<img src="{html.escape(src)}" alt="" loading="lazy">'
            f"\n\t\t\t\t</div>"
        )
    tags = " ".join(post.get("tags") or [])
    return (
        f'<article class="blog-card" data-project="{html.escape(post["project"])}" '
        f'data-date="{html.escape(post["date"])}" data-tags="{html.escape(tags)}">{cover_block}\n'
        f'\t\t\t\t<div class="blog-card-meta">\n'
        f'\t\t\t\t\t<span class="blog-tag blog-tag--{html.escape(post["project"])}">{html.escape(post["project_label"])}</span>\n'
        f'\t\t\t\t\t<time datetime="{html.escape(post["date"])}">{html.escape(post["date_display"])}</time>\n'
        f"\t\t\t\t</div>\n"
        f'\t\t\t\t<h3><a href="blog/{html.escape(post["slug"])}.html">{html.escape(post["title"])}</a></h3>\n'
        f"\t\t\t\t<p>{html.escape(post.get('excerpt') or '')}</p>\n"
        f"\t\t\t</article>"
    )


def rebuild_listing() -> None:
    posts = json.loads(POSTS.read_text(encoding="utf-8"))
    text = LISTING.read_text(encoding="utf-8")
    start = text.find('<div class="blog-list" id="blog-list">')
    end = text.find("\t\t</div>\n\t</div>\n\t<div class=\"footer")
    if start < 0 or end < 0:
        raise SystemExit(f"listing markers missing start={start} end={end}")
    cards = "\n".join(card_html(p) for p in posts)
    text = text[:start] + f'<div class="blog-list" id="blog-list">\n{cards}\n' + text[end:]
    LISTING.write_text(text, encoding="utf-8")
    print(f"listing rebuilt with {len(posts)} cards")


def main() -> int:
    for slug in SLUGS:
        path = BLOG / f"{slug}.html"
        old = path.read_text(encoding="utf-8")
        new = polish(old)
        path.write_text(new, encoding="utf-8")
        print(f"polished {slug} ({len(old)} -> {len(new)})")
    rebuild_listing()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
