#!/usr/bin/env python3
"""Publish the BanklessDAO Efficient DAO Design backfill and the X-article folder."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

import markdown as mdlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tag_blog_posts import infer_tags

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
SOURCE = BLOG / "source"
MEDIA = BLOG / "media"
BACKFILL = ROOT / "blog-backfill"
UA = "justiceconder-blog-import/1.0 (+https://justiceconder.com)"
MD = mdlib.Markdown(extensions=["extra", "sane_lists", "nl2br"])

ERA_LABELS = {
    "singularity-hacker": "Futurism",
    "medium": "Project management",
    "0xjustice": "Crypto",
    "qacc": "q/acc",
    "clawbank": "ClawBank",
}

DAO_MD_URL = "https://paragraph.com/@banklessdao-2/efficient-dao-design.md"
DAO_CANONICAL = "https://paragraph.com/@banklessdao-2/efficient-dao-design"
DAO_IMAGES = {
    "cover": "https://storage.googleapis.com/papyrus_images/76ff7a23139de93ea793437e426d3d17a92323ebc159d210b6a3077fbb84c8eb.png",
    "11ab28fd3734feeb14a8ec5024a726f7c0774d956d7c934728ea60eb9de681e5.jpg": "https://storage.googleapis.com/papyrus_images/11ab28fd3734feeb14a8ec5024a726f7c0774d956d7c934728ea60eb9de681e5.jpg",
    "350b4a2b401d9f8839826d41a6d2a5f72eb5949f4b4f1515525c4e0efdbd6c8f.jpg": "https://storage.googleapis.com/papyrus_images/350b4a2b401d9f8839826d41a6d2a5f72eb5949f4b4f1515525c4e0efdbd6c8f.jpg",
    "a98dcc76b7bb8809d7a462b6797c0943695d35ef9665d9a4c47f313f4dc6e4b6.jpg": "https://storage.googleapis.com/papyrus_images/a98dcc76b7bb8809d7a462b6797c0943695d35ef9665d9a4c47f313f4dc6e4b6.jpg",
}

BACKFILL_POSTS = [
    {
        "file": "skillshop.md",
        "cover_src": "skillshop.jpg",
        "slug": "0xjustice-introducing-skillshop",
        "title": "Introducing SkillShop: The Skill Marketplace for Agents",
        "date": "2026-02-23",
        "project": "0xjustice",
        "canonical": "https://x.com/singularityhack/article/2026003382939324814",
        "status_id": "2026003382939324814",
    },
    {
        "file": "machine-econ.md",
        "cover_src": "machine-econ.jpg",
        "slug": "0xjustice-the-new-machine-economy",
        "title": "The New Machine Economy",
        "date": "2026-03-04",
        "project": "0xjustice",
        "canonical": "https://x.com/singularityhack/article/2029279897957310715",
        "status_id": "2029279897957310715",
    },
    {
        "file": "agent-econ.md",
        "cover_src": "agent-econ.jpg",
        "slug": "0xjustice-agent-economics-skillshop-is-go",
        "title": "Agent Economics: SkillShop is GO",
        "date": "2026-03-06",
        "project": "0xjustice",
        "canonical": "https://x.com/singularityhack/article/2029993400569843976",
        "status_id": "2029993400569843976",
    },
    {
        "file": "clawbank-status-updates.md",
        "cover_src": "clawbank-status-update.jpg",
        "slug": "clawbank-status-update",
        "title": "ClawBank Status Update",
        "date": "2026-03-17",
        "project": "clawbank",
        "canonical": "https://x.com/clawbankco/article/2033997750145036498",
        "status_id": "2033997750145036498",
    },
    {
        "file": "building-tokenized systems.md",
        "cover_src": "building-tokenized-systems.jpg",
        "slug": "0xjustice-building-tokenized-systems-in-2026",
        "title": "Building Tokenized Systems in 2026",
        "date": "2026-03-18",
        "project": "0xjustice",
        "canonical": "https://x.com/singularityhack/article/2034304913254068462",
        "status_id": "2034304913254068462",
    },
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read()


def md_to_html(text: str) -> str:
    MD.reset()
    return MD.convert(text)


def display_date(iso: str) -> str:
    return datetime.fromisoformat(iso).strftime("%B %-d, %Y")


def excerpt_of(text: str, limit: int = 220) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(".,;:") + "…"


def local_media_name(hint: str, data: bytes, suffix: str) -> str:
    digest = hashlib.sha1(data).hexdigest()[:12]
    stem = re.sub(r"[^a-z0-9]+", "-", hint.lower()).strip("-")[:40]
    return f"{digest}-{stem}{suffix}"


def save_media(data: bytes, hint: str, suffix: str) -> str:
    MEDIA.mkdir(parents=True, exist_ok=True)
    name = local_media_name(hint, data, suffix)
    dest = MEDIA / name
    if not dest.exists():
        dest.write_bytes(data)
    return f"media/{name}"


def clean_x_article(raw: str, title: str, status_id: str) -> str:
    end = re.search(
        rf"\[[^\]]*{re.escape(status_id)}\]",
        raw,
    )
    # Prefer the byline timestamp near the end of the article, not the header.
    stamps = list(re.finditer(r"\[\d{1,2}:\d{2} [AP]M · [A-Z][a-z]{2} \d{1,2}, 2026\]", raw))
    cutoff = stamps[-1].start() if stamps else (end.start() if end else len(raw))

    # Body starts after the first /analytics) that precedes the title-or-prose.
    start = 0
    marker = raw.find(title)
    if marker != -1:
        after_title = raw[marker + len(title) :]
        analytics = list(re.finditer(r"/analytics\)", after_title))
        if analytics:
            start = marker + len(title) + analytics[0].end()
        else:
            start = marker + len(title)
    body = raw[start:cutoff]

    # Drop X chrome blocks.
    body = re.sub(r"\[\s*!\[.*?\]\([^)]+\)\s*\]\([^)]+\)", "", body, flags=re.S)
    body = re.sub(r"!\[.*?\]\([^)]*pbs\.twimg\.com/profile_images[^)]+\)", "", body)
    body = re.sub(r"^\[?\s*\d[\d.,]*[KM]?\s*\]?\s*$", "", body, flags=re.M)
    body = re.sub(r"^(Boost|See new posts|GIF|Relevant|Reply|Post your reply|Everyone can reply|Live on X)\s*$", "", body, flags=re.M)
    body = re.sub(r"^\[?\s*\d+\s*\]?\s*$", "", body, flags=re.M)
    body = re.sub(r"^\s*·\s*$", "", body, flags=re.M)

    # Promote empty ## followed by a short label into a heading.
    def heading(match: re.Match[str]) -> str:
        label = match.group(1).strip()
        if not label or label.startswith("[") or label.startswith("http"):
            return match.group(0)
        if len(label) < 80 and not label.endswith("."):
            return f"## {label}\n\n"
        return f"{label}\n\n"

    body = re.sub(r"^##\s*\n+([^\n]+)\n", heading, body, flags=re.M)
    body = re.sub(r"^##\s*$", "", body, flags=re.M)

    # Fix protocol-relative and cashtag links.
    body = body.replace("](//", "](https://")
    body = re.sub(r"\[\$ClawBank\]\([^)]+\)", "ClawBank", body)
    body = re.sub(r"\[(https://t\.co/[^)]+)\]\(\1\)", r"\1", body)

    # Collapse leftover empty link wrappers and extra blank lines.
    body = re.sub(r"\[\s*\]\([^)]+\)", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def page_shell(title: str, body: str, prefix: str = "", extra_js: str = "") -> str:
    switcher = f'\t<script src="{prefix}js/theme-switcher.js"></script>'
    extra_js = f"{extra_js}\n{switcher}" if extra_js else switcher
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="description" content="{html.escape(title)}" />
	<meta name="author" content="justiceconder.com" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<title>{html.escape(title)}</title>
	<link rel="shortcut icon" href="{prefix}images/icon/favicon.ico" />
	<link rel="stylesheet" href="https://unpkg.com/bulma@0.9.1/css/bulma.min.css" type="text/css" />
	<link rel="stylesheet" href="{prefix}css/style.css" type="text/css" />
	<link rel="stylesheet" href="{prefix}css/theme-icon.css" type="text/css" />
	<link rel="stylesheet" href="{prefix}css/blog.css" type="text/css" />
	<link rel="stylesheet" href="{prefix}css/themes.css" type="text/css" />
	<script>
	(function () {{
		try {{
			var q = new URLSearchParams(location.search).get("theme");
			var t = q || localStorage.getItem("jc-site-theme");
			if (t) document.documentElement.setAttribute("data-theme", t);
		}} catch (e) {{}}
	}})();
	</script>
	<link rel="preload"
		href="https://fonts.googleapis.com/css?family=Open+Sans:400,300,600,300italic,400italic,600italic,700,700italic,800,800italic&display=swap"
		as="style" onload="this.rel='stylesheet'" />
	<link rel="preload"
		href="https://fonts.googleapis.com/css?family=Raleway:400,100,100italic,200italic,200,300,300italic,400italic,500,500italic,600,600italic,700italic,900italic,900,800,700,800italic&display=swap"
		as="style" onload="this.rel='stylesheet'" />
</head>

<body class="blog-page">
	<header class="header" id="home"></header>
	<nav id="menu" class="navbar navbar-default desktop-only">
		<div class="navbar-header">
			<a rel="noopener" class="navbar-brand" href="{prefix}index.html">
				<img id="logo_img" src="{prefix}images/logo.webp" alt="" height="40px" width="55px" loading="lazy">
			</a>
		</div>
		<ul class="nav-link title-text flex-container">
			<li><a href="{prefix}index.html#about">About</a></li>
			<li><a href="{prefix}index.html#resume">Experience</a></li>
			<li><a href="{prefix}index.html#education">Education</a></li>
			<li><a href="{prefix}index.html#portfolio">Portfolio</a></li>
			<li><a href="{prefix}index.html#content">Content</a></li>
			<li><a href="{prefix}blog.html" class="is-current">Blog</a></li>
			<li><a href="{prefix}index.html#testimonials">Testimonials</a></li>
		</ul>
	</nav>

	<nav id="menu" class="navbar navbar-default mobile-only">
		<div class="navbar-header">
			<a rel="noopener" class="navbar-brand" href="{prefix}index.html">
				<img id="logo_img" src="{prefix}images/logo.webp" alt="" height="40px" width="55px" loading="lazy">
			</a>
		</div>
		<div class="nav-opener">
			<div class="unselectable hamburger">
				<div></div>
				<div></div>
				<div></div>
			</div>
			<ul class="nav-link flex-container title-text">
			<li><a href="{prefix}index.html#about">About</a></li>
			<li><a href="{prefix}index.html#resume">Experience</a></li>
			<li><a href="{prefix}index.html#education">Education</a></li>
			<li><a href="{prefix}index.html#portfolio">Portfolio</a></li>
			<li><a href="{prefix}index.html#content">Content</a></li>
			<li><a href="{prefix}blog.html" class="is-current">Blog</a></li>
			<li><a href="{prefix}index.html#testimonials">Testimonials</a></li>
			</ul>
		</div>
	</nav>
	<div class="container blog-wrap">
{body}
	</div>
	<div class="footer flex-container"></div>
{extra_js}
</body>

</html>
"""


def write_post_page(post: dict) -> None:
    project = post["project"]
    label = ERA_LABELS[project]
    cover = post.get("cover_local")
    cover_html = f'\t\t\t<p class="blog-cover"><img src="{cover}" alt=""></p>\n' if cover else ""
    body = f"""\t\t<p class="blog-crumb"><a href="../blog.html">← All writings</a></p>
\t\t<article class="blog-article">
\t\t\t<div class="blog-card-meta">
\t\t\t\t<span class="blog-tag blog-tag--{html.escape(project)}">{html.escape(label)}</span>
\t\t\t\t<time datetime="{html.escape(post['date'])}">{html.escape(post['date_display'])}</time>
\t\t\t</div>
\t\t\t<h1>{html.escape(post['title'])}</h1>
\t\t\t<p class="blog-source">Originally published at <a href="{html.escape(post['canonical'])}" target="_blank" rel="noopener">{html.escape(post['canonical'])}</a></p>
{cover_html}\t\t\t<div class="blog-prose">
{post['body_html']}
\t\t\t</div>
\t\t</article>"""
    (BLOG / f"{post['slug']}.html").write_text(
        page_shell(f"{post['title']} — Justice Conder", body, prefix="../"),
        encoding="utf-8",
    )


def card_html(post: dict) -> str:
    cover = post.get("cover")
    cover_block = ""
    if cover:
        src = cover if cover.startswith("blog/") else f"blog/{cover}"
        cover_block = (
            f'\n\t\t\t\t<div class="blog-card-cover">'
            f'\n\t\t\t\t\t<img src="{html.escape(src)}" alt="" loading="lazy">'
            f"\n\t\t\t\t</div>"
        )
    tags = " ".join(post.get("tags") or [])
    return f"""<article class="blog-card" data-project="{html.escape(post['project'])}" data-date="{html.escape(post['date'])}" data-tags="{html.escape(tags)}">{cover_block}
				<div class="blog-card-meta">
					<span class="blog-tag blog-tag--{html.escape(post['project'])}">{html.escape(post['project_label'])}</span>
					<time datetime="{html.escape(post['date'])}">{html.escape(post['date_display'])}</time>
				</div>
				<h3><a href="blog/{html.escape(post['slug'])}.html">{html.escape(post['title'])}</a></h3>
				<p>{html.escape(post.get('excerpt') or '')}</p>
			</article>"""


def rewrite_listing(posts: list[dict]) -> None:
    listing = ROOT / "blog.html"
    html_text = listing.read_text(encoding="utf-8")
    cards = "\n".join(card_html(p) for p in posts)
    start = html_text.find('<div class="blog-list" id="blog-list">')
    end = html_text.find('\t<div class="footer', start)
    if start < 0 or end < 0:
        raise SystemExit("Could not find blog-list / footer markers in blog.html")
    html_text = (
        html_text[:start]
        + '<div class="blog-list" id="blog-list">\n'
        + cards
        + "\n\t\t</div>\n\t</div>\n"
        + html_text[end:]
    )
    listing.write_text(html_text, encoding="utf-8")


def localize_md_images(md: str, extra: dict[str, str] | None = None) -> str:
    mapping = extra or {}

    def repl(match: re.Match[str]) -> str:
        alt, url = match.group(1), match.group(2)
        if url in mapping:
            return f"![{alt}]({mapping[url]})"
        if not url.startswith("http"):
            return match.group(0)
        if "paragraph.com/editor/twitter" in url or "branding" in url:
            return ""
        try:
            data = fetch(url)
        except Exception as exc:  # noqa: BLE001
            print(f"  image fail {url} {exc}")
            return match.group(0)
        suffix = Path(url.split("?")[0]).suffix or ".jpg"
        if suffix not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            suffix = ".jpg"
        local = "../" + save_media(data, Path(url).stem, suffix)
        mapping[url] = local
        return f"![{alt}]({local})"

    return re.sub(r"!\[([^\]]*)\]\((https?://[^)\s]+)\)", repl, md)


def publish_dao() -> dict:
    print("Fetching Efficient DAO Design…")
    raw = fetch(DAO_MD_URL).decode("utf-8")
    if "Decentralization is not only compatible" not in raw:
        raise SystemExit("DAO markdown did not contain the full article")

    lines = raw.splitlines()
    body = "\n".join(lines[5:]) if lines[0].startswith("# ") else raw
    body = re.sub(r"^---\s*", "", body)
    body = re.sub(
        r"\n---\n\*Originally published on \[BanklessDAO\].*$",
        "",
        body,
        flags=re.S,
    )
    body = body.strip()

    cover_bytes = fetch(DAO_IMAGES["cover"])
    cover_rel = save_media(cover_bytes, "efficient-dao-design-cover", ".png")

    image_map = {}
    for name, url in DAO_IMAGES.items():
        if name == "cover":
            continue
        data = fetch(url)
        local = "../" + save_media(data, name, Path(name).suffix)
        image_map[url] = local
        image_map[f"https://img.paragraph.com/cdn-cgi/image/format=auto,width=3840,quality=85/{url}"] = local

    body = localize_md_images(body, image_map)
    html_body = md_to_html(body)

    dest = SOURCE / "0xjustice" / "efficient-dao-design.md"
    dest.write_text(
        "# Efficient DAO Design\n\n"
        "By [BanklessDAO](https://paragraph.com/@banklessdao-2) · 2022-08-24\n\n"
        "---\n\n"
        f"{body}\n\n"
        "---\n\n"
        f"*Originally published on [BanklessDAO]({DAO_CANONICAL})*\n",
        encoding="utf-8",
    )

    post = {
        "slug": "0xjustice-efficient-dao-design",
        "title": "Efficient DAO Design",
        "date": "2022-08-24",
        "date_display": "August 24, 2022",
        "project": "0xjustice",
        "project_label": "Crypto",
        "canonical": DAO_CANONICAL,
        "excerpt": excerpt_of(html_body),
        "path": "blog/0xjustice-efficient-dao-design.html",
        "cover": f"blog/{cover_rel}",
        "cover_local": cover_rel,
        "body_html": html_body,
    }
    post["tags"] = infer_tags(post)
    write_post_page(post)
    print("  wrote Efficient DAO Design")
    return post


def publish_backfill() -> list[dict]:
    posts = []
    for spec in BACKFILL_POSTS:
        raw = (BACKFILL / spec["file"]).read_text(encoding="utf-8")
        body = clean_x_article(raw, spec["title"], spec["status_id"])
        if len(body) < 400:
            raise SystemExit(f"cleaned body too short for {spec['file']}: {len(body)}")
        cover_src = BACKFILL / spec["cover_src"]
        cover_rel = save_media(cover_src.read_bytes(), spec["slug"], cover_src.suffix)
        body = localize_md_images(body)
        html_body = md_to_html(body)
        source_dir = SOURCE / spec["project"]
        source_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / f"{spec['slug'].split('-', 1)[1]}.md").write_text(
            f"# {spec['title']}\n\n"
            f"By 0xJustice · {spec['date']}\n\n---\n\n{body}\n",
            encoding="utf-8",
        )
        post = {
            "slug": spec["slug"],
            "title": spec["title"],
            "date": spec["date"],
            "date_display": display_date(spec["date"]),
            "project": spec["project"],
            "project_label": ERA_LABELS[spec["project"]],
            "canonical": spec["canonical"],
            "excerpt": excerpt_of(html_body),
            "path": f"blog/{spec['slug']}.html",
            "cover": f"blog/{cover_rel}",
            "cover_local": cover_rel,
            "body_html": html_body,
        }
        post["tags"] = infer_tags(post)
        write_post_page(post)
        print(f"  wrote {spec['title']} ({spec['date']}, {len(body)} chars)")
        posts.append(post)
    return posts


VYPRPAD_CANONICAL = "https://vyprpad.xyz/blog"
VYPRPAD_IMAGES = [
    ("cover", "https://vyprpad.xyz/images/vypr-banner.png", "Vypr Pad Banner"),
    ("approvals", "https://vyprpad.xyz/images/approvals.png", "Token Approvals"),
    ("air-gapped", "https://vyprpad.xyz/images/air-gapped.jpg", "Air-gapped Security"),
    ("sequence", "https://vyprpad.xyz/images/SEQUENCE.png", "Sequence Diagram"),
    ("ens", "https://vyprpad.xyz/images/the-ens.jpg", "ENS Domain"),
    ("x402", "https://vyprpad.xyz/images/x402.png", "x402 Protocol"),
    ("weird-shit", "https://vyprpad.xyz/images/weird-shit.gif", "Weird Shit"),
]


def publish_vyprpad() -> dict:
    print("Fetching Vypr Pad…")
    images: dict[str, str] = {}
    for key, url, _alt in VYPRPAD_IMAGES:
        data = fetch(url)
        if not data:
            raise SystemExit(f"failed to fetch {url}")
        suffix = Path(url.split("?")[0]).suffix.lower()
        images[key] = save_media(data, f"vypr-pad-{key}", suffix)
        print(f"  image {key} {len(data)} bytes -> {images[key]}")

    source = f"""# Introducing Vypr Pad

By 0xJustice · 2026-01-10

---

![Vypr Pad Banner](../{images["cover"]})

## Introduction

Requiring users to connect their wallets as soon as they open your app, then approving you to pull money from their wallets, has a chilling effect on crypto. The absolute best people I know in crypto have been burned by this. Stuff that should be fun, exciting, and experimental basically can't exist in this environment. When we should be cultivating a space where people create all kinds of weird and interesting things, we've made it so that only well-established big brands feel safe to use.

![Token Approvals](../{images["approvals"]})

## In-Browser Wallets

One way people have gotten around this is by building in-browser wallets that get created on the fly when you create an account. This may, in spirit, undermine decentralization, but it's a practical approach that addresses these issues and allows people to experiment without constant worry.

## The Headless Approach

Another approach I'd like to introduce is what I'm calling a "headless" approach: connectionless dapps that work without wallet connections or approvals. The idea is simple: create your apps so people can just send ETH to your contract and get back the thing they want. Send that thing back, get ETH back. No approvals, no signatures, no wallet connections.

One group doing cool stuff with this paradigm is [OnThis](https://www.onthis.xyz/), which enables bridging and swapping with simple transactions. I understand there are fundamental limitations with this approach, given how Ethereum currently works, so you're somewhat restricted. But I'm not convinced we've pushed it hard enough. I've been told this is how the original ICOs functioned, but I couldn't find much detail on the topic. So I decided to build something.

![Air-gapped Security](../{images["air-gapped"]})

## Introducing Vypr Pad

Vypr Pad is a headless token launchpad. You can launch and trade tokens entirely from within your wallet. No wallet connect, no signatures, no token approvals. Send ETH to vypr.eth to launch a new token. You collect trading fees. Find your token and trading address through the website or a block explorer. People mint and burn your tokens by sending ETH or tokens directly to your contract address.

![Sequence Diagram](../{images["sequence"]})

## Domain as UX

Take a moment to consider what this means for UX. You can point your ENS name to the contract address, effectively compressing your app interface to a single domain name. That's the interface. A few characters. People interact with it just by knowing those characters. That's interesting. All the information is on-chain. Anyone can build a different frontend, or skip the launchpad entirely and just build a frontend for their particular token.

![ENS Domain](../{images["ens"]})

## Agent-First Design

This should be much easier to script against. It's easier to ask your autonomous commerce agent to send money to your treasury when it reaches a certain threshold. No approvals, no liquidity pools. It's pristine. You can even have agents out in the wild: they find some valuable piece of data, want to sell it via x402, so before they do, they launch a token and begin selling the data. Then they use all the proceeds from that sale to buy into their own curve.

![x402 Protocol](../{images["x402"]})

You effectively have public, transparent, digitally native, agentic companies that anyone can buy into. You could guarantee these agents buy into the curve by using Trusted Execution Environments or some other magic. The whole thing is just cool.

## Limitations and Next Steps

People much smarter than me, with far more experience in Ethereum, will see the limitations of this approach. You shouldn't initiate new launches from a multi-sig. Things can get weird if you try to make a pool that assumes token approvals. Edge cases exist: gas can get out of control, transactions can revert, and agent interactions can be tricky.

But my hope is that where there's a will, there's a way. This might inspire others to build headless applications and develop interesting workarounds that enable people to trade, stake, vote, post, etc., within this reduced trust model. It would also be cool if it were easier to communicate information back to users within the transaction, so they could easily see what's happening. I'm definitely open to new ideas and to riffing on this if anyone's interested.

There are other primitives I plan to build on top of this that make it even more interesting. Time didn't permit building a graduate-to-DEX feature, but the foundation has been laid, and my goal of launching a POC and something I can start building on for my other projects has been achieved.

![Weird Shit](../{images["weird-shit"]})

## Try It Out

**Base Sepolia (testnet):** sepolia.vypr.eth

**Base Mainnet:** vypr.eth

Find your token on the homepage at [vyprpad.xyz](https://vyprpad.xyz/) or on a block explorer.

All of your created tokens will show here: [https://vyprpad.xyz/creators.html?wallet=<your wallet address>](https://vyprpad.xyz/creators)

Add your new token to your wallet, then point an ENS to your trading address for easy reference.

For full technical documentation: [https://vyprpad.xyz/docs](https://vyprpad.xyz/docs)

---

*Originally published on [Vypr Pad]({VYPRPAD_CANONICAL})*

**Disclaimer:** Vypr Pad is provided "as is" without warranty of any kind. Use of this platform and any tokens created or traded through it is at your own risk. The developers and operators of Vypr Pad are not responsible for any losses, damages, or liabilities that may arise from using this service. Always conduct your own research and exercise caution when interacting with smart contracts and cryptocurrency.
"""
    dest = SOURCE / "0xjustice" / "introducing-vypr-pad.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(source, encoding="utf-8")

    # Body for the site page: source minus title/byline and the cover image
    # already shown above the article.
    body_md = source.split("---\n", 1)[1].strip()
    body_md = re.sub(r"^!\[[^\]]*\]\([^)]+\)\s*", "", body_md.lstrip())
    html_body = md_to_html(body_md)
    if "headless token launchpad" not in html_body:
        raise SystemExit("Vypr Pad body did not contain the fetched article")

    post = {
        "slug": "0xjustice-introducing-vypr-pad",
        "title": "Introducing Vypr Pad",
        "date": "2026-01-10",
        "date_display": display_date("2026-01-10"),
        "project": "0xjustice",
        "project_label": "Crypto",
        "canonical": VYPRPAD_CANONICAL,
        "excerpt": excerpt_of(html_body),
        "path": "blog/0xjustice-introducing-vypr-pad.html",
        "cover": f"blog/{images['cover']}",
        "cover_local": images["cover"],
        "body_html": html_body,
    }
    write_post_page(post)
    post["tags"] = infer_tags(post)
    print(f"  wrote Introducing Vypr Pad ({post['date']}, tags={post['tags']})")
    return post


def merge_index(new_posts: list[dict]) -> list[dict]:
    index = json.loads((BLOG / "posts.json").read_text(encoding="utf-8"))
    by_slug = {p["slug"]: p for p in index}
    for post in new_posts:
        record = {k: post[k] for k in (
            "slug", "title", "date", "date_display", "project", "project_label",
            "canonical", "excerpt", "path", "cover", "tags",
        )}
        by_slug[post["slug"]] = record
    for post in by_slug.values():
        post["project_label"] = ERA_LABELS.get(post["project"], post.get("project_label"))
    merged = sorted(by_slug.values(), key=lambda p: (p.get("date") or "", p["slug"]), reverse=True)
    (BLOG / "posts.json").write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return merged


def main() -> int:
    MEDIA.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])
    posts: list[dict] = []
    if not only or "dao" in only:
        posts.append(publish_dao())
    if not only or "backfill" in only:
        posts += publish_backfill()
    if not only or "vyprpad" in only:
        posts.append(publish_vyprpad())
    merged = merge_index(posts)
    rewrite_listing(merged)
    import apply_blog_filters
    apply_blog_filters.main()
    print(f"published {len(posts)} local posts; catalog is {len(merged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
