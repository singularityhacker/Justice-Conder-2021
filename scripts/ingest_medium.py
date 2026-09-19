#!/usr/bin/env python3
"""Ingest Justice Conder Medium articles that are not already on the blog."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path
from urllib.parse import unquote, urlparse

import markdown as mdlib

_BB = Path(__file__).resolve().parent / "build-blog.py"
_spec = importlib.util.spec_from_file_location("build_blog", _BB)
bb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(bb)

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
SOURCE = BLOG / "source" / "medium"
MEDIA = BLOG / "media"
EXTRACTS = [
    Path("/home/ubuntu/.cursor/projects/workspace/agent-tools/33171cfc-663b-4bce-9963-49605587f47f.txt"),
    Path("/home/ubuntu/.cursor/projects/workspace/agent-tools/114af955-fe81-410a-87ff-b0c049b74ada.txt"),
]
UA = "justiceconder-blog-import/1.0 (+https://justiceconder.com)"
MD = mdlib.Markdown(extensions=["extra", "sane_lists", "nl2br"])

SKIP_TITLES = {
    "hacking your situation",
    "the multiple persona theory of digital secrecy",
    "computer generated education",
    "is blockchain a fad",
    "front running defi regulation",
    "optimizing dao delivery",
    "rethinking the dao contributor funnel",
    "the unreasonable effectiveness of tiny ai models",
    "ai as industrial scale induction",
    "7 power laws of the technological singularity",
    "out to sea",
}

AUTHOR_PHOTO = "XCnpvvkArT3yf9QR_r0Uxg"
DATE_RE = re.compile(
    r"\b("
    r"January|February|March|April|May|June|July|August|September|October|November|December|"
    r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
    r")\s+\d{1,2},\s+\d{4}\b"
)
CHROME_LINE = re.compile(
    r"^(?:"
    r"Listen|Share|Follow|Sitemap|Open in app|Sign up|Sign in|Get app|Write|"
    r"Press enter or click to view image in full size|"
    r"\d+ min read|"
    r"·|--|"
    r"Help|Status|About|Careers|Press|Blog|Store|Privacy|Rules|Terms|Text to speech|"
    r"58 followers|92 following|Operator|"
    r"Join Medium for free to get updates from this writer\.|"
    r"Subscribe|"
    r"Remember me for faster sign in|"
    r"\[x\]"
    r")\s*$",
    re.I,
)
CUT_RE = re.compile(
    r"(?m)^(?:#{0,3}\s*)?(?:\[)?(?:"
    r"Written by|"
    r"Get Justice|"
    r"Sitemap\]|"
    r"Help\n\nStatus\n\nAbout"
    r")",
)


def norm_title(text: str) -> str:
    text = unescape(text).lower()
    text = re.sub(r"[*_`#]+", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return text.strip()


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/").split("/")[-1]
    path = re.sub(r"-[a-f0-9]{8,}$", "", path)
    return path or "medium-post"


def parse_rss_dates() -> dict[str, str]:
    req = urllib.request.Request(
        "https://justiceconder.medium.com/feed",
        headers={"User-Agent": UA},
    )
    data = urllib.request.urlopen(req, timeout=30).read()
    root = ET.fromstring(data)
    out = {}
    for item in root.findall(".//item"):
        link = (item.findtext("link") or "").split("?")[0]
        pub = item.findtext("pubDate") or ""
        dt = bb.parse_date(pub)
        if link and dt:
            out[link] = bb.iso_date(dt)
    return out


def parse_sitemap_dates() -> dict[str, str]:
    req = urllib.request.Request(
        "https://justiceconder.medium.com/sitemap/sitemap.xml",
        headers={"User-Agent": UA},
    )
    data = urllib.request.urlopen(req, timeout=30).read()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.fromstring(data)
    out = {}
    for url in root.findall("sm:url", ns):
        loc = url.findtext("sm:loc", namespaces=ns) or ""
        last = url.findtext("sm:lastmod", namespaces=ns) or ""
        if loc and last and "/about" not in loc and loc.rstrip("/") != "https://justiceconder.medium.com":
            out[loc.split("?")[0]] = last[:10]
    return out


def strip_chrome(body: str) -> str:
    body = re.sub(
        r"(?ms)^#{0,3}\s*Get Justice Gödel Conder.?s stories in your inbox\n.*?(?=^[^\n])",
        "",
        body,
    )
    body = re.sub(
        r"(?ms)^#{0,3}\s*Get Justice.?s stories in your inbox\n.*?(?=\n\n[A-Z#])",
        "\n",
        body,
    )
    cut = CUT_RE.search(body)
    if cut:
        body = body[: cut.start()]
    kept = []
    for line in body.splitlines():
        stripped = line.strip()
        if CHROME_LINE.match(stripped):
            continue
        if re.fullmatch(r"\d+", stripped):
            continue
        if re.match(r"^\[(?:Listen|Share|Follow)\]", stripped):
            continue
        if re.match(r"^[-*]\s+\[x\]\s*$", stripped) or stripped == "[x]":
            continue
        if re.match(r"^!\[Image \d+: Justice", stripped):
            continue
        if AUTHOR_PHOTO in stripped and "resize:fill:" in stripped:
            continue
        if re.match(r"^\[Justice Gödel Conder\]", stripped):
            continue
        if re.match(r"^\[\]\([^)]+\)\s*$", stripped):
            continue
        kept.append(line)
    body = "\n".join(kept)
    body = re.sub(r"^(?:!\[[^\]]*\]\([^)]+\)\s*)+", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return body


def clean_markdown(raw: str) -> tuple[str, str, str]:
    """Return title, date display snippet, body markdown."""
    h1 = re.search(r"^#\s+(.+)$", raw, re.M)
    if not h1:
        raise ValueError("no title")
    title = unescape(re.sub(r"[*_]+", "", h1.group(1))).strip()
    rest = raw[h1.end() :]
    date_hit = DATE_RE.search(rest[:1200])
    date_text = date_hit.group(0) if date_hit else ""
    if date_hit:
        rest = rest[date_hit.end() :]
    body = strip_chrome(rest)
    if len(re.sub(r"\s+", " ", body)) < 80:
        raise ValueError("body too short")
    return title, date_text, body


def pick_cover(images: list[str], body: str) -> str:
    candidates = []
    for url in images or []:
        if "resize:fill:" in url or AUTHOR_PHOTO in url:
            continue
        candidates.append(url)
    for url in re.findall(r"!\[[^\]]*\]\((https://miro\.medium\.com[^)]+)\)", body):
        if "resize:fill:" in url or AUTHOR_PHOTO in url:
            continue
        if url not in candidates:
            candidates.append(url)
    for url in candidates:
        if "resize:fit:" in url:
            return url
    return candidates[0] if candidates else ""


def asset_name(url: str, suffix: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    raw = Path(unquote(urlparse(url).path)).stem
    raw = re.sub(r"[^a-zA-Z0-9_-]+", "-", raw).strip("-")[:40] or "asset"
    return f"{digest}-{raw}{suffix}"


def download_cover(url: str) -> str:
    if not url:
        return ""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = resp.read()
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0]
    except Exception as exc:  # noqa: BLE001
        print(f"  cover fail {url} {exc}")
        return ""
    path = urlparse(url).path
    suffix = Path(unquote(path)).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        suffix = ".jpg" if "jpeg" in ctype else ".png"
    MEDIA.mkdir(parents=True, exist_ok=True)
    name = asset_name(url, suffix)
    (MEDIA / name).write_bytes(data)
    return f"blog/media/{name}"


def localize_body_images(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        url = match.group(1)
        if "miro.medium.com" not in url:
            return match.group(0)
        if "resize:fill:" in url or AUTHOR_PHOTO in url:
            return ""
        local = download_cover(url)
        if not local:
            return match.group(0)
        return f'src="{local.replace("blog/", "")}"'

    return re.sub(r'src="(https://miro\.medium\.com[^"]+)"', repl, html)


def card_html(post: dict) -> str:
    cover = ""
    if post.get("cover"):
        cover = (
            f'\n\t\t\t\t<div class="blog-card-cover">\n'
            f'\t\t\t\t\t<img src="{post["cover"]}" alt="" loading="lazy">\n'
            f"\t\t\t\t</div>"
        )
    tags = " ".join(post.get("tags") or [])
    return f"""\t\t\t<article class="blog-card" data-project="medium" data-date="{post["date"]}" data-tags="{tags}">{cover}
\t\t\t\t<div class="blog-card-meta">
\t\t\t\t\t<span class="blog-tag blog-tag--medium">Medium</span>
\t\t\t\t\t<time datetime="{post["date"]}">{post["date_display"]}</time>
\t\t\t\t</div>
\t\t\t\t<h3><a href="blog/{post["slug"]}.html">{bb.html.escape(post["title"])}</a></h3>
\t\t\t\t<p>{bb.html.escape(post["excerpt"])}</p>
\t\t\t</article>"""


def insert_cards(listing: str, cards: list[tuple[str, str]]) -> str:
    """cards: (date, html) newest first merge into existing list."""
    start = listing.find('<div class="blog-list" id="blog-list">')
    if start < 0:
        raise SystemExit("blog-list markers missing")
    last = listing.rfind("</article>")
    list_end = listing.find("</div>", last)
    existing = listing[start:list_end]
    old_cards = re.findall(r'(<article class="blog-card"[\s\S]*?</article>)', existing)
    dated = []
    for html in old_cards:
        m = re.search(r'data-date="([^"]+)"', html)
        dated.append((m.group(1) if m else "", html))
    dated.extend(cards)
    dated.sort(key=lambda x: x[0], reverse=True)
    inner = "\n".join(html for _d, html in dated)
    rebuilt = f'<div class="blog-list" id="blog-list">\n{inner}\n\t\t'
    return listing[:start] + rebuilt + listing[list_end:]


def drop_previous_medium(posts_index: list[dict], listing: str) -> tuple[list[dict], str]:
    for old in BLOG.glob("medium-*.html"):
        old.unlink()
    if SOURCE.exists():
        for old in SOURCE.glob("*.md"):
            old.unlink()
    posts_index = [p for p in posts_index if p.get("project") != "medium"]
    listing = re.sub(
        r'\s*<article class="blog-card" data-project="medium"[\s\S]*?</article>',
        "",
        listing,
    )
    return posts_index, listing


def main() -> int:
    posts_index = json.loads((BLOG / "posts.json").read_text())
    listing = (ROOT / "blog.html").read_text(encoding="utf-8")
    posts_index, listing = drop_previous_medium(posts_index, listing)
    existing_titles = {norm_title(p["title"]) for p in posts_index}
    existing_titles |= SKIP_TITLES
    rss_dates = parse_rss_dates()
    sm_dates = parse_sitemap_dates()

    extracted = []
    for path in EXTRACTS:
        data = json.loads(path.read_text())
        extracted.extend(data.get("results") or [])

    added = []
    skipped_dupes = []
    failed = []
    date_notes = []

    SOURCE.mkdir(parents=True, exist_ok=True)

    for item in extracted:
        url = (item.get("url") or "").split("?")[0]
        raw = item.get("raw_content") or ""
        try:
            title, date_text, body_md = clean_markdown(raw)
        except Exception as exc:
            failed.append({"url": url, "error": str(exc)})
            continue
        key = norm_title(title)
        if key in existing_titles:
            skipped_dupes.append({"url": url, "title": title, "reason": "already on blog from another source"})
            continue
        dt = bb.parse_date(date_text)
        date_source = "byline" if dt else ""
        if not dt:
            dt = bb.parse_date(rss_dates.get(url, ""))
            date_source = "rss" if dt else date_source
        if not dt:
            dt = bb.parse_date(sm_dates.get(url, ""))
            date_source = "sitemap_lastmod" if dt else date_source
        if not dt:
            failed.append({"url": url, "title": title, "error": "no date"})
            continue
        stem = slug_from_url(url)
        slug = f"medium-{stem}"
        MD.reset()
        body_html = bb.sanitize_html(MD.convert(body_md))
        body_html = localize_body_images(body_html)
        body_html = re.sub(r"(?is)<p>\s*<a[^>]*>Listen</a>\s*</p>\s*", "", body_html)
        body_html = re.sub(r"(?is)<h2>[\s\S]*Written by[\s\S]*$", "", body_html)
        body_html = re.sub(r"(?is)<ul>\s*<li>\s*\[x\]\s*</li>\s*</ul>\s*", "", body_html)
        cover_remote = pick_cover(item.get("images") or [], body_md)
        cover = download_cover(cover_remote)
        post = {
            "slug": slug,
            "title": title,
            "date": bb.iso_date(dt),
            "date_display": bb.display_date(dt),
            "project": "medium",
            "project_label": "Medium",
            "canonical": url,
            "excerpt": bb.excerpt_of(body_md),
            "path": f"blog/{slug}.html",
            "cover": cover,
            "source_slug": stem,
            "body_html": body_html,
        }
        SOURCE.joinpath(f"{stem}.md").write_text(
            f"# {title}\n\n{url}\n\n{bb.iso_date(dt)}\n\n{body_md}\n",
            encoding="utf-8",
        )
        bb.write_post_page(post)
        if cover:
            page = BLOG / f"{slug}.html"
            html = page.read_text(encoding="utf-8")
            local = cover.replace("blog/", "")
            if 'class="blog-cover"' not in html:
                html = html.replace(
                    '<div class="blog-prose">',
                    f'<p class="blog-cover"><img src="{local}" alt=""></p>\n\t\t\t<div class="blog-prose">',
                    1,
                )
                page.write_text(html, encoding="utf-8")
        added.append(post)
        existing_titles.add(key)
        date_notes.append({"title": title, "date": post["date"], "source": date_source})
        print(f"  ok   {post['date']}  {title}  [{date_source}]")

    posts_index.extend(
        {k: p[k] for k in ("slug", "title", "date", "date_display", "project", "project_label", "canonical", "excerpt", "path", "cover") if k in p}
        for p in added
    )
    posts_index.sort(key=lambda p: (p.get("date") or ""), reverse=True)
    (BLOG / "posts.json").write_text(json.dumps(posts_index, indent=2) + "\n", encoding="utf-8")

    new_cards = [(p["date"], card_html(p)) for p in added]
    listing = insert_cards(listing, new_cards)
    (ROOT / "blog.html").write_text(listing, encoding="utf-8")

    report = {
        "added": [{"title": p["title"], "date": p["date"], "url": p["canonical"]} for p in added],
        "skipped_duplicates": skipped_dupes,
        "failed": failed,
        "date_sources": date_notes,
        "sitemap_articles": len(sm_dates),
        "not_on_public_listing": [
            {
                "title": "Out to Sea",
                "reason": "in skip list from earlier notes; not present on the public Medium sitemap or RSS",
            }
        ],
    }
    (BLOG / "medium-ingest-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "added": len(added),
        "skipped_duplicates": len(skipped_dupes),
        "failed": len(failed),
        "sitemap_articles": len(sm_dates),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
