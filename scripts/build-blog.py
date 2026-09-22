#!/usr/bin/env python3
"""Ingest Justice Conder writings and generate static blog pages."""

from __future__ import annotations

import concurrent.futures
import email.utils
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import markdown as mdlib

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "blog"
SOURCE_DIR = BLOG_DIR / "source"
UA = "justiceconder-blog-import/1.0 (+https://justiceconder.com)"

PROJECTS = {
    "0xjustice": {
        "label": "Crypto",
        "home": "https://paragraph.com/@0xjustice",
    },
    "singularity-hacker": {
        "label": "Futurism",
        "home": "https://singularityhacker.com/",
    },
    "qacc": {
        "label": "q/acc",
        "home": "https://paragraph.com/@qacc",
    },
    "clawbank": {
        "label": "ClawBank",
        "home": "https://clawbank.co/blog.html",
    },
    "medium": {
        "label": "Project management",
        "home": "https://justiceconder.medium.com/",
    },
}

MD = mdlib.Markdown(extensions=["extra", "sane_lists", "nl2br"])


def fetch(url: str, retries: int = 3, timeout: int = 35) -> tuple[str | None, str | None]:
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                return data.decode(charset, errors="replace"), None
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
            time.sleep(0.6 * (attempt + 1))
    return None, last_err


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "post"


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    value = value.replace("Z", "+00:00")
    try:
        dt = email.utils.parsedate_to_datetime(value)
        if dt:
            return dt
    except (TypeError, ValueError):
        pass
    formats = (
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
        "%B %d %Y",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", value)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def iso_date(dt: datetime | None) -> str:
    if not dt:
        return ""
    if dt.tzinfo:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%d")


def display_date(dt: datetime | None) -> str:
    if not dt:
        return ""
    return dt.strftime("%B %-d, %Y")


def strip_tags(text: str) -> str:
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def excerpt_of(text: str, limit: int = 220) -> str:
    text = strip_tags(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def rewrite_urls(html_text: str, base: str) -> str:
    base = base.rstrip("/")

    def abs_url(match: re.Match) -> str:
        attr, quote, url = match.group(1), match.group(2), match.group(3)
        if url.startswith(("http://", "https://", "mailto:", "data:", "#")):
            return match.group(0)
        if url.startswith("//"):
            return f"{attr}={quote}https:{url}{quote}"
        if url.startswith("/"):
            host = re.match(r"https?://[^/]+", base)
            origin = host.group(0) if host else base
            return f"{attr}={quote}{origin}{url}{quote}"
        return f"{attr}={quote}{base}/{url}{quote}"

    html_text = re.sub(
        r"""(?i)(src|href)=(['"])([^'"]+)(['"])""",
        lambda m: abs_url(m)[:-1] + m.group(4) if False else abs_url(m),
        html_text,
    )
    return html_text


def sanitize_html(html_text: str) -> str:
    html_text = re.sub(r"(?is)<script[^>]*>.*?</script>", "", html_text)
    html_text = re.sub(r"(?is)<style[^>]*>.*?</style>", "", html_text)
    html_text = re.sub(r"(?i)\son\w+\s*=\s*(['\"]).*?\1", "", html_text)
    return html_text.strip()


def md_to_html(text: str) -> str:
    MD.reset()
    return MD.convert(text)


def extract_between(text: str, start_pat: str, end_pat: str) -> str | None:
    start = re.search(start_pat, text, re.I)
    if not start:
        return None
    rest = text[start.end() :]
    end = re.search(end_pat, rest, re.I)
    if not end:
        return rest
    return rest[: end.start()]


# ── collectors ──────────────────────────────────────────────────────────────


def collect_paragraph(handle: str, project: str) -> list[dict]:
    sitemap_url = f"https://paragraph.com/@{handle}/sitemap.xml"
    rss_url = f"https://paragraph.com/api/blogs/rss/%40{handle}"
    sitemap, sitemap_err = fetch(sitemap_url)
    rss, rss_err = fetch(rss_url)
    posts: dict[str, dict] = {}

    if sitemap:
        for loc in re.findall(r"<loc>(.*?)</loc>", sitemap):
            if re.search(rf"/@{handle}/[^/]+$", loc) and "/p/" not in loc:
                slug = loc.rstrip("/").split("/")[-1]
                posts[slug] = {
                    "slug": f"{project}-{slug}",
                    "source_slug": slug,
                    "project": project,
                    "canonical": loc,
                    "title": "",
                    "date": "",
                    "excerpt": "",
                    "body_html": "",
                    "source_kind": "paragraph",
                }
    else:
        print(f"WARN sitemap {handle}: {sitemap_err}", file=sys.stderr)

    rss_items = {}
    if rss:
        try:
            root = ET.fromstring(rss)
        except ET.ParseError:
            root = None
        if root is not None:
            for item in root.findall(".//item"):
                link = (item.findtext("link") or "").strip()
                slug = link.rstrip("/").split("/")[-1]
                title = (item.findtext("title") or "").strip()
                pub = (item.findtext("pubDate") or "").strip()
                desc = (item.findtext("description") or "").strip()
                content = ""
                for child in list(item):
                    tag = child.tag.split("}")[-1]
                    if tag in ("encoded", "content") and child.text:
                        content = child.text
                rss_items[slug] = {
                    "title": title,
                    "date": pub,
                    "excerpt": desc,
                    "content": content,
                    "link": link,
                }
                if slug not in posts and link:
                    posts[slug] = {
                        "slug": f"{project}-{slug}",
                        "source_slug": slug,
                        "project": project,
                        "canonical": link,
                        "title": title,
                        "date": pub,
                        "excerpt": desc,
                        "body_html": "",
                        "source_kind": "paragraph",
                    }
    else:
        print(f"WARN rss {handle}: {rss_err}", file=sys.stderr)

    for slug, meta in rss_items.items():
        if slug in posts:
            if meta["title"]:
                posts[slug]["title"] = meta["title"]
            if meta["date"]:
                posts[slug]["date"] = meta["date"]
            if meta["excerpt"]:
                posts[slug]["excerpt"] = meta["excerpt"]
            posts[slug]["_rss_html"] = meta["content"]

    return list(posts.values())


def collect_clawbank() -> list[dict]:
    manifest, err = fetch("https://clawbank.co/posts/manifest.json")
    if not manifest:
        print(f"WARN clawbank manifest: {err}", file=sys.stderr)
        return []
    data = json.loads(manifest)
    posts = []
    for item in data:
        slug = item["slug"]
        posts.append(
            {
                "slug": f"clawbank-{slug}",
                "source_slug": slug,
                "project": "clawbank",
                "canonical": f"https://clawbank.co/blog/{slug}/",
                "title": item.get("title") or slug,
                "date": item.get("date") or "",
                "excerpt": item.get("description") or "",
                "cover": item.get("cover_image") or "",
                "body_html": "",
                "source_kind": "clawbank",
            }
        )
    return posts


def collect_singularity() -> list[dict]:
    pages = ["https://singularityhacker.com/"]
    pages += [f"https://singularityhacker.com/page{n}/" for n in range(2, 8)]
    found: dict[str, dict] = {}
    for url in pages:
        html_text, err = fetch(url)
        if not html_text:
            if "page" in url:
                continue
            print(f"WARN singularity index: {err}", file=sys.stderr)
            continue
        if "Page not found" in html_text and "page" in url:
            break
        # post cards
        for card in re.finditer(
            r'<a class="post-card-content-link" href="([^"]+)"[\s\S]*?<h2 class="post-card-title">([\s\S]*?)</h2>[\s\S]*?<section class="post-card-excerpt">([\s\S]*?)</section>',
            html_text,
        ):
            href, title, excerpt = card.group(1), card.group(2), card.group(3)
            path = href.split("?")[0].rstrip("/")
            if not path.startswith("/") or path in ("", "/about", "/feed.xml"):
                continue
            if path.startswith("/page") or path.startswith("/tag/") or path.startswith("/author/"):
                continue
            slug = path.strip("/")
            if slug in found:
                continue
            found[slug] = {
                "slug": f"sh-{slug}",
                "source_slug": slug,
                "project": "singularity-hacker",
                "canonical": f"https://singularityhacker.com/{slug}",
                "title": strip_tags(title),
                "date": "",
                "excerpt": excerpt_of(excerpt),
                "body_html": "",
                "source_kind": "singularity",
            }
        # fallback: any root-level post hrefs
        for href in re.findall(r'href="(/[a-z0-9][a-z0-9\-]+)"', html_text):
            slug = href.strip("/")
            if slug.startswith("page") or slug in ("about", "feed.xml", "404.html"):
                continue
            if slug not in found:
                found[slug] = {
                    "slug": f"sh-{slug}",
                    "source_slug": slug,
                    "project": "singularity-hacker",
                    "canonical": f"https://singularityhacker.com/{slug}",
                    "title": "",
                    "date": "",
                    "excerpt": "",
                    "body_html": "",
                    "source_kind": "singularity",
                }
    return list(found.values())


# ── fetch bodies ────────────────────────────────────────────────────────────


def fill_paragraph(post: dict) -> dict:
    slug = post["source_slug"]
    handle = "0xjustice" if post["project"] == "0xjustice" else "qacc"
    md_url = f"https://paragraph.com/@{handle}/{slug}.md"
    text, err = fetch(md_url)
    source_text = ""
    title = post.get("title") or ""
    dt = parse_date(post.get("date"))
    body_md = ""

    if text and text.lstrip().startswith("#") and len(text) > 80:
        source_text = text
        lines = text.splitlines()
        if lines and lines[0].startswith("# "):
            title = title or lines[0][2:].strip()
            lines = lines[1:]
        # byline
        joined = "\n".join(lines).lstrip()
        by = re.match(r"By \[[^\]]+\]\([^)]+\) · (\d{4}-\d{2}-\d{2})\s*", joined)
        if by:
            dt = dt or parse_date(by.group(1))
            joined = joined[by.end() :]
        joined = re.sub(r"^---\s*", "", joined)
        body_md = joined.strip()
        post["body_html"] = sanitize_html(md_to_html(body_md))
        post["_source_ext"] = "md"
        post["_source_text"] = source_text
    elif post.get("_rss_html") and len(strip_tags(post["_rss_html"])) > 200:
        post["body_html"] = sanitize_html(rewrite_urls(post["_rss_html"], f"https://paragraph.com/@{handle}"))
        post["_source_ext"] = "html"
        post["_source_text"] = post["_rss_html"]
        post["_fetch_note"] = f"markdown missing ({err}); used RSS HTML"
    else:
        post["_error"] = err or "empty paragraph body"
        return post

    if title:
        post["title"] = title
    if dt:
        post["date"] = iso_date(dt)
        post["date_display"] = display_date(dt)
    if not post.get("excerpt"):
        post["excerpt"] = excerpt_of(post["body_html"])
    else:
        post["excerpt"] = excerpt_of(post["excerpt"])
    return post


def fill_clawbank(post: dict) -> dict:
    slug = post["source_slug"]
    md_url = f"https://clawbank.co/posts/{slug}.md"
    text, err = fetch(md_url)
    if not text:
        post["_error"] = err or "empty clawbank markdown"
        return post
    fm = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"')
            body = parts[2].lstrip("\n")
    title = fm.get("title") or post.get("title") or slug
    dt = parse_date(fm.get("date") or post.get("date"))
    excerpt = fm.get("description") or post.get("excerpt") or ""
    html_body = sanitize_html(md_to_html(body))
    html_body = rewrite_urls(html_body, "https://clawbank.co")
    cover = fm.get("cover_image") or post.get("cover") or ""
    if cover.startswith("/"):
        cover = "https://clawbank.co" + cover
    post.update(
        {
            "title": title,
            "date": iso_date(dt),
            "date_display": display_date(dt),
            "excerpt": excerpt_of(excerpt or html_body),
            "body_html": html_body,
            "cover_remote": cover,
            "_source_ext": "md",
            "_source_text": text,
        }
    )
    return post


def fill_singularity(post: dict) -> dict:
    url = post["canonical"]
    html_text, err = fetch(url)
    if not html_text:
        post["_error"] = err or "empty singularity page"
        return post
    title = post.get("title") or ""
    og = re.search(r'<meta property="og:title" content="([^"]+)"', html_text)
    if og:
        title = html.unescape(og.group(1))
    if not title:
        h = re.search(r'<h1 class="post-full-title">([\s\S]*?)</h1>', html_text)
        if h:
            title = strip_tags(h.group(1))
    published = None
    meta = re.search(r'<meta property="article:published_time" content="([^"]+)"', html_text)
    if meta:
        published = parse_date(meta.group(1))
    if not published:
        t = re.search(r'<time class="post-full-meta-date"[^>]*>([\s\S]*?)</time>', html_text)
        if t:
            published = parse_date(strip_tags(t.group(1)))
    body = extract_between(
        html_text,
        r'<section class="post-full-content">',
        r'</section>\s*<footer class="post-full-footer"',
    )
    if not body:
        body = extract_between(html_text, r'<section class="kg-card-markdown">', r"</section>")
    if not body:
        md_block = extract_between(html_text, r'<div class="kg-card-markdown">', r"</div>")
        body = md_block
    if not body:
        post["_error"] = "could not extract post body"
        post["_source_text"] = html_text[:2000]
        return post
    # drop share/read-next leftovers
    body = re.sub(r'(?is)<aside[\s\S]*?</aside>', "", body)
    body = re.sub(r'(?is)<footer class="post-full-footer">[\s\S]*', "", body)
    body = re.sub(r'(?is)<section class="author-card">[\s\S]*', "", body)
    body = sanitize_html(rewrite_urls(body, "https://singularityhacker.com"))
    og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html_text)
    if og_img:
        cover = og_img.group(1)
        if cover.startswith("/"):
            cover = "https://singularityhacker.com" + cover
        post["cover_remote"] = cover
    if len(strip_tags(body)) < 40:
        post["_error"] = "extracted body too short"
        return post
    post.update(
        {
            "title": title or post["source_slug"].replace("-", " ").title(),
            "date": iso_date(published),
            "date_display": display_date(published),
            "excerpt": post.get("excerpt") or excerpt_of(body),
            "body_html": body,
            "_source_ext": "html",
            "_source_text": html_text,
        }
    )
    if post.get("excerpt"):
        post["excerpt"] = excerpt_of(post["excerpt"])
    return post


def fill_post(post: dict) -> dict:
    kind = post["source_kind"]
    try:
        if kind == "paragraph":
            return fill_paragraph(post)
        if kind == "clawbank":
            return fill_clawbank(post)
        if kind == "singularity":
            return fill_singularity(post)
    except Exception as exc:  # noqa: BLE001
        post["_error"] = f"exception: {exc}"
    return post


# ── HTML generation ─────────────────────────────────────────────────────────

NAV_ITEMS = [
    ("index.html#about", "About"),
    ("index.html#resume", "Experience"),
    ("index.html#education", "Education"),
    ("index.html#portfolio", "Portfolio"),
    ("blog.html", "Writing"),
    ("index.html#testimonials", "Testimonials"),
]


def nav_html(active: str, prefix: str = "") -> str:
    def href(target: str) -> str:
        return prefix + target

    def items(extra_class: str = "") -> str:
        out = []
        for target, label in NAV_ITEMS:
            current = ' class="is-current"' if label == active else ""
            out.append(f'<li><a href="{href(target)}"{current}>{label}</a></li>')
        return "\n\t\t\t".join(out)

    return f"""\t<nav id="menu" class="navbar navbar-default desktop-only">
\t\t<div class="navbar-header">
\t\t\t<a rel="noopener" class="navbar-brand" href="{href("index.html")}">
\t\t\t\t<img id="logo_img" src="{prefix}images/logo.webp" alt="" height="40px" width="55px" loading="lazy">
\t\t\t\t<span class="brand-lockup">
\t\t\t\t\t<span class="brand-name">Justice Conder</span>
\t\t\t\t</span>
\t\t\t</a>
\t\t</div>
\t\t<ul class="nav-link title-text flex-container">
\t\t\t{items()}
\t\t</ul>
\t</nav>

\t<nav id="menu" class="navbar navbar-default mobile-only">
\t\t<div class="navbar-header">
\t\t\t<a rel="noopener" class="navbar-brand" href="{href("index.html")}">
\t\t\t\t<img id="logo_img" src="{prefix}images/logo.webp" alt="" height="40px" width="55px" loading="lazy">
\t\t\t\t<span class="brand-lockup">
\t\t\t\t\t<span class="brand-name">Justice Conder</span>
\t\t\t\t</span>
\t\t\t</a>
\t\t</div>
\t\t<div class="nav-opener">
\t\t\t<div class="unselectable hamburger">
\t\t\t\t<div></div>
\t\t\t\t<div></div>
\t\t\t\t<div></div>
\t\t\t</div>
\t\t\t<ul class="nav-link flex-container title-text">
\t\t\t{items()}
\t\t\t</ul>
\t\t</div>
\t</nav>"""


def page_shell(title: str, body: str, prefix: str = "", extra_head: str = "", extra_js: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
\t<meta charset="utf-8">
\t<meta http-equiv="X-UA-Compatible" content="IE=edge">
\t<meta name="description" content="{html.escape(title)}" />
\t<meta name="author" content="justiceconder.com" />
\t<meta name="viewport" content="width=device-width, initial-scale=1" />
\t<title>{html.escape(title)}</title>
\t<link rel="shortcut icon" href="{prefix}images/icon/favicon.ico" />
\t<link rel="stylesheet" href="https://unpkg.com/bulma@0.9.1/css/bulma.min.css" type="text/css" />
\t<link rel="stylesheet" href="{prefix}css/style.css" type="text/css" />
\t<link rel="stylesheet" href="{prefix}css/theme-icon.css" type="text/css" />
\t<link rel="stylesheet" href="{prefix}css/blog.css" type="text/css" />
\t<link rel="stylesheet" href="{prefix}css/dark-operator.css" type="text/css" />
\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500;600&family=Syne:wght@500;600;700;800&display=swap" />
\t<link rel="preload"
\t\thref="https://fonts.googleapis.com/css?family=Open+Sans:400,300,600,300italic,400italic,600italic,700,700italic,800,800italic&display=swap"
\t\tas="style" onload="this.rel='stylesheet'" />
\t<link rel="preload"
\t\thref="https://fonts.googleapis.com/css?family=Raleway:400,100,100italic,200italic,200,300,300italic,400italic,500,500italic,600,600italic,700italic,900italic,900,800,700,800italic&display=swap"
\t\tas="style" onload="this.rel='stylesheet'" />
{extra_head}
</head>

<body class="blog-page dark-operator">
\t<header class="header" id="home"></header>
{nav_html("Writing", prefix)}
\t<div class="container blog-wrap">
{body}
\t</div>
\t<footer class="footer site-footer">
\t\t<div class="site-footer-grid">
\t\t\t<div class="site-footer-identity">
\t\t\t\t<p class="site-footer-name">Justice Conder</p>
\t\t\t\t<p class="site-footer-blurb">Technically capable founder and strategist preparing for forward-deployed engineering and strategy roles at AI companies.</p>
\t\t\t\t<ul class="site-footer-social">
\t\t\t\t\t<li>
\t\t\t\t\t\t<a rel="noopener" href="https://github.com/singularityhacker" target="_blank" aria-label="GitHub">
\t\t\t\t\t\t\t<i class="fa fa-github"></i>
\t\t\t\t\t\t</a>
\t\t\t\t\t</li>
\t\t\t\t\t<li>
\t\t\t\t\t\t<a rel="noopener" href="https://twitter.com/singularityhack" target="_blank" aria-label="Twitter">
\t\t\t\t\t\t\t<i class="fa fa-twitter"></i>
\t\t\t\t\t\t</a>
\t\t\t\t\t</li>
\t\t\t\t\t<li>
\t\t\t\t\t\t<a rel="noopener" href="https://www.linkedin.com/in/justiceconder" target="_blank" aria-label="LinkedIn">
\t\t\t\t\t\t\t<i class="fa fa-linkedin"></i>
\t\t\t\t\t\t</a>
\t\t\t\t\t</li>
\t\t\t\t</ul>
\t\t\t</div>
\t\t\t<nav class="site-footer-nav" aria-label="Footer">
\t\t\t\t<p class="site-footer-heading">Navigation</p>
\t\t\t\t<ul>
\t\t\t\t\t<li><a href="{prefix}index.html#about">About</a></li>
\t\t\t\t\t<li><a href="{prefix}index.html#resume">Experience</a></li>
\t\t\t\t\t<li><a href="{prefix}index.html#portfolio">Portfolio</a></li>
\t\t\t\t\t<li><a href="{prefix}blog.html">Writing</a></li>
\t\t\t\t</ul>
\t\t\t</nav>
\t\t\t<div class="site-footer-contact">
\t\t\t\t<p class="site-footer-heading">Get in Touch</p>
\t\t\t\t<a class="site-footer-email" href="mailto:justiceconder@gmail.com">justiceconder@gmail.com</a>
\t\t\t</div>
\t\t</div>
\t\t<div class="site-footer-bar">
\t\t\t<p>© 2026 Justice Conder. All rights reserved.</p>
\t\t\t<p>Built with intention.</p>
\t\t</div>
\t</footer>
{extra_js}
</body>

</html>
"""


def write_listing(posts: list[dict]) -> None:
    cards = []
    for post in posts:
        project = post["project"]
        label = PROJECTS[project]["label"]
        date_iso = post.get("date") or ""
        date_disp = post.get("date_display") or date_iso
        tags = " ".join(post.get("tags") or [])
        cards.append(
            f"""\t\t\t<article class="blog-card" data-project="{html.escape(project)}" data-date="{html.escape(date_iso)}" data-tags="{html.escape(tags)}">
\t\t\t\t<div class="blog-card-meta">
\t\t\t\t\t<span class="blog-tag blog-tag--{html.escape(project)}">{html.escape(label)}</span>
\t\t\t\t\t<time datetime="{html.escape(date_iso)}">{html.escape(date_disp)}</time>
\t\t\t\t</div>
\t\t\t\t<h3><a href="blog/{html.escape(post['slug'])}.html">{html.escape(post['title'])}</a></h3>
\t\t\t\t<p>{html.escape(post.get('excerpt') or '')}</p>
\t\t\t</article>"""
        )
    filters = [
        ('all', 'All'),
        ('0xjustice', '0xjustice'),
        ('singularity-hacker', 'Singularity Hacker'),
        ('qacc', 'q/acc'),
        ('clawbank', 'ClawBank'),
    ]
    filter_btns = "\n".join(
        f'\t\t\t<button type="button" class="blog-filter{" is-active" if key=="all" else ""}" data-filter="{key}">{label}</button>'
        for key, label in filters
    )
    body = f"""\t\t<div class="subject-header">
\t\t\t<span>Writings</span>
\t\t\t<h2>Writing</h2>
\t\t\t<div class="bg-text unselectable"><strong>Writings</strong></div>
\t\t</div>
\t\t<p class="blog-lede">Collected posts from 0xjustice, Singularity Hacker, q/acc, and ClawBank — original wording, with dates and source links preserved.</p>
\t\t<p class="blog-cite">My writing has been cited by ZDNet, Daring Fireball, OSNews, Forefront, TalentDAO, and many other DAO newsletters and thought leaders across the ecosystem and translated into other languages.</p>
\t\t<div class="blog-filters" role="group" aria-label="Filter writings by project">
{filter_btns}
\t\t</div>
\t\t<p class="blog-count" id="blog-count"></p>
\t\t<div class="blog-empty" id="blog-empty" hidden>No writings match this filter.</div>
\t\t<div class="blog-list" id="blog-list">
{chr(10).join(cards)}
\t\t</div>"""
    extra_js = '\t<script src="js/blog.js"></script>'
    (ROOT / "blog.html").write_text(
        page_shell("Writing — Justice Conder", body, extra_js=extra_js),
        encoding="utf-8",
    )


def write_post_page(post: dict) -> None:
    project = post["project"]
    label = PROJECTS[project]["label"]
    date_iso = post.get("date") or ""
    date_disp = post.get("date_display") or date_iso
    canonical = post["canonical"]
    body = f"""\t\t<p class="blog-crumb"><a href="../blog.html">← All writings</a></p>
\t\t<article class="blog-article">
\t\t\t<div class="blog-card-meta">
\t\t\t\t<span class="blog-tag blog-tag--{html.escape(project)}">{html.escape(label)}</span>
\t\t\t\t<time datetime="{html.escape(date_iso)}">{html.escape(date_disp)}</time>
\t\t\t</div>
\t\t\t<h1>{html.escape(post['title'])}</h1>
\t\t\t<p class="blog-source">Originally published at <a href="{html.escape(canonical)}" target="_blank" rel="noopener">{html.escape(canonical)}</a></p>
\t\t\t<div class="blog-prose">
{post['body_html']}
\t\t\t</div>
\t\t</article>"""
    html_page = page_shell(
        f"{post['title']} — Justice Conder",
        body,
        prefix="../",
    )
    (BLOG_DIR / f"{post['slug']}.html").write_text(html_page, encoding="utf-8")


def save_source(post: dict) -> None:
    ext = post.get("_source_ext") or "txt"
    raw = post.get("_source_text")
    if not raw:
        return
    dest = SOURCE_DIR / post["project"]
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{post['source_slug']}.{ext}").write_text(raw, encoding="utf-8")


def sort_key(post: dict) -> tuple:
    date = post.get("date") or ""
    return (date == "", date)


def main() -> int:
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    print("Collecting post lists…")
    inventory = []
    inventory += collect_paragraph("0xjustice", "0xjustice")
    inventory += collect_paragraph("qacc", "qacc")
    inventory += collect_clawbank()
    inventory += collect_singularity()
    print(f"Discovered {len(inventory)} posts")
    for project in PROJECTS:
        n = sum(1 for p in inventory if p["project"] == project)
        print(f"  {project}: {n}")

    print("Fetching bodies…")
    filled = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futs = [pool.submit(fill_post, dict(p)) for p in inventory]
        for fut in concurrent.futures.as_completed(futs):
            post = fut.result()
            if post.get("_error") or not post.get("body_html"):
                errors.append(post)
                print(f"  FAIL {post.get('canonical')} — {post.get('_error')}")
            else:
                filled.append(post)
                print(f"  ok   {post['project']:18} {post.get('date','?'):10} {post['title'][:60]}")

    filled.sort(key=sort_key, reverse=True)

    # clean previously generated pages except source
    for old in BLOG_DIR.glob("*.html"):
        old.unlink()

    for post in filled:
        save_source(post)
        write_post_page(post)

    write_listing(filled)

    index = []
    for post in filled:
        index.append(
            {
                "slug": post["slug"],
                "title": post["title"],
                "date": post.get("date") or "",
                "date_display": post.get("date_display") or "",
                "project": post["project"],
                "project_label": PROJECTS[post["project"]]["label"],
                "canonical": post["canonical"],
                "excerpt": post.get("excerpt") or "",
                "path": f"blog/{post['slug']}.html",
            }
        )
    (BLOG_DIR / "posts.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    report = {
        "ok": {p: sum(1 for x in filled if x["project"] == p) for p in PROJECTS},
        "failed": [
            {"title": p.get("title"), "url": p.get("canonical"), "error": p.get("_error")}
            for p in errors
        ],
        "total_ok": len(filled),
        "total_failed": len(errors),
    }
    (BLOG_DIR / "ingest-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    # Keep a local copy of every image/video so pages do not depend on Paragraph etc.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import localize_blog_media
    localize_blog_media.main()
    import apply_blog_filters
    apply_blog_filters.main()
    return 0 if filled else 1


if __name__ == "__main__":
    raise SystemExit(main())
