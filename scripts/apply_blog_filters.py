#!/usr/bin/env python3
"""Write era/topic filters and data-tags onto the writings listing."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tag_blog_posts import RULES, infer_tags, tag_label

ROOT = Path(__file__).resolve().parents[1]
LISTING = ROOT / "blog.html"
POSTS_PATH = ROOT / "blog" / "posts.json"

ERA_META = [
    {
        "key": "singularity-hacker",
        "label": "Futurism",
        "short": "Fut",
        "blurb": "Computing, the technological singularity, cypherpunk privacy, and later Bitcoin and DeFi — {count} posts from the original Singularity Hacker years.",
    },
    {
        "key": "medium",
        "label": "Project management",
        "short": "PM",
        "blurb": "Scrum, agile delivery, and technical writing — {count} essays from the program-agilist years.",
    },
    {
        "key": "0xjustice",
        "label": "Crypto",
        "short": "0x",
        "blurb": "DAO design, on-chain organization, tokenization, and the agent economy — {count} posts.",
    },
    {
        "key": "qacc",
        "label": "q/acc",
        "short": "q/acc",
        "blurb": "Founded the Quadratic Accelerator. Protocol notes, cohorts, and season impact reports — {count} posts from the live seasons.",
    },
    {
        "key": "clawbank",
        "label": "ClawBank",
        "short": "CB",
        "blurb": "Founded ClawBank. Agents with bank accounts, companies, and contracts — {count} product notes.",
    },
]

FILTER_LABELS = {
    "singularity-hacker": "Futurism",
    "medium": "Project management",
    "0xjustice": "Crypto",
    "qacc": "q/acc",
    "clawbank": "ClawBank",
}


def month_year(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%B %Y")


def build_eras(posts: list[dict]) -> list[dict]:
    eras = []
    for meta in ERA_META:
        dates = [p["date"] for p in posts if p.get("project") == meta["key"] and p.get("date")]
        if not dates:
            continue
        start, end = min(dates), max(dates)
        eras.append(
            {
                **meta,
                "start": start,
                "end": end,
                "count": len(dates),
                "range": f"{month_year(start)} – {month_year(end)}",
                "blurb": meta["blurb"].format(count=len(dates)),
            }
        )
    return eras


def header_html(tag_slugs: list[str], eras: list[dict]) -> str:
    era_btns = ['\t\t\t<button type="button" class="blog-filter is-active" data-filter="all">All</button>']
    for era in eras:
        era_btns.append(
            f'\t\t\t<button type="button" class="blog-filter" data-filter="{era["key"]}">{FILTER_LABELS[era["key"]]}</button>'
        )
    tag_btns = [
        '\t\t\t<button type="button" class="blog-tag-filter is-active" data-tag="all">All topics</button>'
    ]
    for slug in tag_slugs:
        tag_btns.append(
            f'\t\t\t<button type="button" class="blog-tag-filter" data-tag="{slug}">{tag_label(slug)}</button>'
        )

    return f"""\t\t<p class="blog-lede">Writing since 2011 — 15 years — across futurism, technical project management, token engineering, governance, and AI. Cited by ZDNet, Daring Fireball, OSNews, Forefront, TalentDAO, and other DAO newsletters and thought leaders, and translated into other languages.</p>
\t\t<div class="blog-filters" role="group" aria-label="Filter writings by era">
{chr(10).join(era_btns)}
\t\t</div>
\t\t<div class="blog-tag-filters" role="group" aria-label="Filter writings by topic">
{chr(10).join(tag_btns)}
\t\t</div>
\t\t<p class="blog-count" id="blog-count"></p>
\t\t<div class="blog-empty" id="blog-empty" hidden>No writings match this filter.</div>"""


def apply_card_tags(html: str, posts: list[dict]) -> str:
    by_slug = {p["slug"]: p for p in posts}

    def repl(match: re.Match[str]) -> str:
        attrs, rest = match.group(1), match.group(2)
        href = re.search(r'href="blog/([^"]+)\.html"', rest)
        if not href:
            return match.group(0)
        post = by_slug.get(href.group(1))
        if not post:
            return match.group(0)
        tags = post.get("tags") or infer_tags(post)
        attrs = re.sub(r'\sdata-tags="[^"]*"', "", attrs)
        tag_attr = f' data-tags="{" ".join(tags)}"' if tags else ' data-tags=""'
        return f'<article class="blog-card"{attrs}{tag_attr}>{rest}</article>'

    return re.sub(
        r'<article class="blog-card"([^>]*)>([\s\S]*?)</article>',
        repl,
        html,
    )


def main() -> int:
    posts = json.loads(POSTS_PATH.read_text(encoding="utf-8"))
    for post in posts:
        post["tags"] = infer_tags(post)
    POSTS_PATH.write_text(json.dumps(posts, indent=2) + "\n", encoding="utf-8")

    tag_counts = Counter()
    for post in posts:
        tag_counts.update(post["tags"])
    tag_slugs = [slug for slug, _label, _pats in RULES if tag_counts[slug]]

    html = LISTING.read_text(encoding="utf-8")
    html = apply_card_tags(html, posts)

    start = html.find('\t\t<p class="blog-lede">')
    end = html.find('\t\t<div class="blog-list"')
    if start < 0 or end < 0:
        raise SystemExit("Could not find listing header markers in blog.html")
    eras = build_eras(posts)
    html = html[:start] + header_html(tag_slugs, eras) + "\n" + html[end:]
    LISTING.write_text(html, encoding="utf-8")
    print("updated blog.html and posts.json")
    print("eras", [(e["key"], e["start"], e["end"], e["count"]) for e in eras])
    print("tags", dict(tag_counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
