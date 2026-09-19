#!/usr/bin/env python3
"""Infer topic tags from real post title, excerpt, and opening prose."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
POSTS_PATH = BLOG / "posts.json"

# Distinctive tags only. Matched against title, excerpt, and the opening of the
# body so long product posts do not inherit every incidental mention.
RULES: list[tuple[str, str, list[str]]] = [
    ("ai", "AI", [
        r"\bai\b", r"a\.i\.", r"artificial intelligence", r"\bllms?\b",
        r"language model", r"machine learning", r"\bdeepfake", r"superintelligence",
        r"turing (scale|test)", r"industrial-scale induction",
        r"human emulation", r"reverse engineering human emotion",
        r"computer generated education",
    ]),
    ("agents", "Agents", [
        r"ai agents?", r"agentic", r"software agents?", r"\bmanfred\b",
        r"agent-first", r"agent economy", r"agent company", r"agent-operated",
        r"personal software agents",
    ]),
    ("singularity", "singularity", [r"\bsingularit"]),
    ("crypto", "crypto", [
        r"\bcrypto(?:currency)?\b", r"\bbitcoin\b", r"\bblockchain\b",
        r"\bweb3\b", r"\bon-?chain\b", r"\bonchain\b",
    ]),
    ("defi", "DeFi", [
        r"\bdefi\b", r"decentralized finance", r"\buniswap\b",
        r"liquidity pool", r"\blp management\b", r"trade to earn",
    ]),
    ("daos", "DAOs", [r"\bdaos?\b", r"\bdacs?\b", r"decentralized autonomous"]),
    ("tokenization", "tokenization", [
        r"tokeniz", r"token unlock", r"token deals?", r"token agreement",
        r"quadratic accelerat", r"\bq/acc\b", r"quadratic funding",
    ]),
    ("ethereum", "Ethereum", [r"\bethereum\b", r"\bpolygon\b"]),
    ("privacy", "privacy", [
        r"\bprivacy\b", r"\bcypherpunk\b", r"client-side crypto",
        r"\bencryption\b", r"digital secrecy", r"\bwhistleblower\b",
        r"net neutrality", r"random number generator",
    ]),
    ("hardware", "hardware", [
        r"\biphone\b", r"\bairpods\b", r"\bplaybook\b", r"windows 8",
        r"wearable", r"\bradioshack\b", r"handheld linux",
    ]),
    ("cyberspace", "cyberspace", [
        r"\bcyberspace\b", r"augmented reality", r"virtual reality",
        r"internet of things", r"\bneuromancer\b",
    ]),
    ("software", "software", [
        r"learn to code", r"full stack", r"source code", r"\bapis?\b",
        r"development sandbox", r"\bprogramming\b", r"rewrite its own",
    ]),
    ("agile", "agile", [
        r"\bagile\b", r"\bscrum\b", r"value stream", r"\bkanban\b",
        r"sprint planning", r"low-?code", r"delivery metrics",
    ]),
]


def strip_html(text: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text)


def focus_text(post: dict) -> str:
    parts = [post.get("title") or "", post.get("excerpt") or ""]
    page = ROOT / post["path"]
    if page.exists():
        html = page.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'<div class="blog-prose">([\s\S]*?)</div>\s*</article>', html)
        if match:
            parts.append(strip_html(match.group(1))[:1200])
    return " ".join(parts).lower()


def infer_tags(post: dict) -> list[str]:
    text = focus_text(post)
    return [slug for slug, _label, pats in RULES if any(re.search(p, text, re.I) for p in pats)]


def tag_label(slug: str) -> str:
    for item_slug, label, _pats in RULES:
        if item_slug == slug:
            return label
    return slug


def main() -> int:
    posts = json.loads(POSTS_PATH.read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    for post in posts:
        tags = infer_tags(post)
        post["tags"] = tags
        counts.update(tags)
    POSTS_PATH.write_text(json.dumps(posts, indent=2) + "\n", encoding="utf-8")
    print("tagged", len(posts), "posts")
    for slug, n in counts.most_common():
        print(f"  {slug:16} {n}")
    print("untagged", sum(1 for p in posts if not p["tags"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
