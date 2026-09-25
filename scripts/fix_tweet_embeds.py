#!/usr/bin/env python3
"""Rebuild flattened tweet embeds in blog/*.html as proper quote-tweet blocks.

Paragraph exports a tweet embed as a run of bare paragraphs:

    <p><a href="https://twitter.com/HANDLE"><img alt="User Avatar" src="…"></a></p>
    <p><a href="https://twitter.com/HANDLE">Display Name</a></p>
    <p><a href="https://twitter.com/HANDLE">@HANDLE</a></p>
    <p><a href="TWEET_URL"><img alt="Twitter Logo" src="…"></a></p>
    …tweet text, emoji as <img>, attached media…
    <p><a href="TWEET_URL"><img alt="Like Icon" src="…"> 27</a>[</p>
    <p>6:31 AM • Aug 14, 2023</p>
    <p>](TWEET_URL)</p>

A tweet quoting another tweet nests a second header + body inside the first
body, sharing the outer footer. This script turns each of those into

    <blockquote class="tweet-embed"> … </blockquote>

with author, handle, text, media, and date, and no avatar, logo, heart, or
like count. Emoji images are replaced by their alt text. Idempotent. Runs
from build-blog.py after localize_blog_media; safe to run directly.
"""

from __future__ import annotations

import html as htmlmod
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "blog"

HEADER_RE = re.compile(
    r'<p><a href="(?P<profile>https://(?:twitter|x)\.com/(?P<handle>[A-Za-z0-9_]+))"><img alt="User Avatar"[^>]*></a></p>\s*'
    r'<p><a href="(?P=profile)">(?P<name>[^<]*)</a></p>\s*'
    r'<p><a href="(?P=profile)">@(?P=handle)</a></p>\s*'
    r'<p><a href="(?P<url>https://(?:twitter|x)\.com/(?P=handle)/status/\d+)"><img alt="Twitter Logo"[^>]*></a></p>\s*',
    re.S,
)

FOOTER_TEMPLATE = (
    r'<p><a href="{url}"><img alt="Like Icon"[^>]*>\s*[\d,.]*\s*[KM]?</a>\[</p>\s*'
    r'<p>(?P<date>[^<]*)</p>\s*'
    r'<p>\]\({url}\)</p>\s*'
)

EMOJI_IMG_RE = re.compile(r'<img alt="(?P<alt>[^"]+)" src="[^"]*-1f[0-9a-f]{3,}(?:-[0-9a-f-]+)?\.(?:png|svg)"\s*/?>')
TRAILING_SPACE_RE = re.compile(r"[ \t]+(?=</p>)")

X_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18">'
    '<path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>'
    "</svg>"
)


def clean_body(body: str) -> str:
    body = EMOJI_IMG_RE.sub(lambda m: htmlmod.unescape(m.group("alt")), body)
    body = TRAILING_SPACE_RE.sub("", body)
    body = re.sub(r"\n{2,}", "\n", body).strip("\n")
    return body


def render(handle: str, name: str, url: str, body: str, date: str | None, quoted: bool = False) -> str:
    cls = "tweet-embed tweet-embed--quoted" if quoted else "tweet-embed"
    profile = f"https://x.com/{handle}"
    out = [
        f'<blockquote class="{cls}">',
        '<div class="tweet-embed-head">',
        f'<a class="tweet-embed-author" href="{profile}" target="_blank" rel="noopener">'
        f'<strong>{name}</strong> <span>@{handle}</span></a>',
        f'<a class="tweet-embed-x" href="{url}" target="_blank" rel="noopener" aria-label="View post on X">{X_ICON}</a>',
        "</div>",
        '<div class="tweet-embed-body">',
        body,
        "</div>",
    ]
    if date:
        out.append(
            f'<p class="tweet-embed-meta"><a href="{url}" target="_blank" rel="noopener">{date.strip()}</a></p>'
        )
    out.append("</blockquote>")
    return "\n".join(out) + "\n"


def convert_body(body: str) -> str:
    """Convert a nested (quoted) tweet header inside a body, if present."""
    inner = HEADER_RE.search(body)
    if not inner:
        return clean_body(body)
    before = clean_body(body[: inner.start()])
    inner_body = clean_body(body[inner.end():])
    quoted = render(inner.group("handle"), inner.group("name"), inner.group("url"), inner_body, None, quoted=True)
    return (before + "\n" if before else "") + quoted.rstrip("\n")


def convert(html: str) -> tuple[str, int, list[str]]:
    count = 0
    problems: list[str] = []
    pos = 0
    out: list[str] = []
    while True:
        head = HEADER_RE.search(html, pos)
        if not head:
            out.append(html[pos:])
            break
        url = head.group("url")
        footer_re = re.compile(FOOTER_TEMPLATE.format(url=re.escape(url)), re.S)
        foot = footer_re.search(html, head.end())
        if not foot:
            problems.append(f"no footer for {url}")
            out.append(html[pos:head.end()])
            pos = head.end()
            continue
        body = convert_body(html[head.end():foot.start()])
        out.append(html[pos:head.start()])
        out.append(render(head.group("handle"), head.group("name"), url, body, foot.group("date")))
        pos = foot.end()
        count += 1
    return "".join(out), count, problems


def main() -> int:
    total = 0
    pages = 0
    all_problems: list[str] = []
    for page in sorted(BLOG_DIR.glob("*.html")):
        html = page.read_text(encoding="utf-8")
        if 'alt="User Avatar"' not in html:
            continue
        new_html, count, problems = convert(html)
        all_problems += [f"{page.name}: {p}" for p in problems]
        if count:
            page.write_text(new_html, encoding="utf-8")
            total += count
            pages += 1
    print(f"fix_tweet_embeds: rebuilt {total} tweet embeds in {pages} pages")
    for p in all_problems:
        print(f"  WARN {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
