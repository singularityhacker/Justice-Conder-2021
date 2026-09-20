#!/usr/bin/env python3
"""Download remote blog media into blog/media and rewrite pages to local paths."""

from __future__ import annotations

import concurrent.futures
import hashlib
import html as htmlmod
import json
import mimetypes
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "blog"
MEDIA_DIR = BLOG_DIR / "media"
SOURCE_DIR = BLOG_DIR / "source"
UA = "justiceconder-blog-import/1.0 (+https://justiceconder.com)"

SKIP_HOST_FRAGMENTS = (
    "unpkg.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "googletagmanager.com",
)

CHROME_URL_PARTS = (
    "/assets/images/gif-logo.gif",
    "/assets/images/favicon",
)

ATTR_URL_RE = re.compile(
    r"""(?P<attr>src|poster)=(?P<q>['"])(?P<url>[^'"]+)(?P=q)""",
    re.I,
)
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\((https?://[^)\s]+)\)")


def fetch_bytes(url: str, retries: int = 3, timeout: int = 45) -> tuple[bytes | None, str | None, str | None]:
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": UA, "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
                return data, ctype, None
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
            time.sleep(0.5 * (attempt + 1))
    return None, None, last_err


def fetch_text(url: str) -> str | None:
    data, _, err = fetch_bytes(url)
    if not data:
        return None
    return data.decode("utf-8", errors="replace")


def ext_for(url: str, ctype: str | None) -> str:
    path = urlparse(url).path
    suffix = Path(unquote(path)).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif", ".mp4", ".webm", ".mov"}:
        return suffix
    guessed = mimetypes.guess_extension(ctype or "") or ""
    if guessed == ".jpe":
        guessed = ".jpg"
    return guessed or ".bin"


def local_name(url: str, ctype: str | None) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    raw = Path(unquote(urlparse(url).path)).stem
    raw = re.sub(r"[^a-zA-Z0-9_-]+", "-", raw).strip("-")[:40] or "asset"
    return f"{digest}-{raw}{ext_for(url, ctype)}"


def normalize_url(url: str) -> str | None:
    url = url.strip()
    if url.startswith("{{DOMAIN}}"):
        url = "https://paragraph.com" + url[len("{{DOMAIN}}") :]
    if url.startswith("//"):
        url = "https:" + url
    if url.startswith("/"):
        return None
    if not url.startswith(("http://", "https://")):
        return None
    host = urlparse(url).netloc.lower()
    if any(part in host for part in SKIP_HOST_FRAGMENTS):
        return None
    if url.startswith("data:"):
        return None
    return url


def is_media_url(url: str) -> bool:
    path = urlparse(url).path.lower()
    if re.search(r"\.(jpg|jpeg|png|gif|webp|svg|avif|mp4|webm|mov)(\?|$)", path):
        return True
    if any(x in url for x in (
        "papyrus_images",
        "img.paragraph.com",
        "/assets/blog/",
        "/assets/images/",
        "/assets/uploads/",
        "/assets/videos/",
        "pbs.twimg.com",
        "media.tumblr.com",
        "/editor/",
    )):
        return True
    return False


def is_chrome(url: str) -> bool:
    return any(part in url for part in CHROME_URL_PARTS)


def clean_singularity_html(html: str) -> str:
    html = html.replace("{{DOMAIN}}", "https://paragraph.com")
    html = re.sub(r"(?is)<!-- Email subscribe form[\s\S]*$", "", html)
    html = re.sub(r'(?is)<footer class="post-full-footer">[\s\S]*$', "", html)
    html = re.sub(r'(?is)<section class="author-card">[\s\S]*$', "", html)
    html = re.sub(r'(?is)<div class="post-full-footer-right">[\s\S]*$', "", html)
    html = re.sub(r'(?is)<aside[\s\S]*?</aside>', "", html)
    html = re.sub(r"(?is)<script[\s\S]*?</script>", "", html)
    return html


def collect_urls_from_html(html: str) -> list[str]:
    urls = []
    for match in ATTR_URL_RE.finditer(html):
        url = normalize_url(match.group("url"))
        if url and is_media_url(url):
            urls.append(url)
    for match in MD_IMG_RE.finditer(html):
        url = normalize_url(match.group(1))
        if url and is_media_url(url):
            urls.append(url)
    return urls


def clawbank_covers() -> dict[str, str]:
    covers = {}
    folder = SOURCE_DIR / "clawbank"
    if not folder.exists():
        return covers
    for md in folder.glob("*.md"):
        text = md.read_text(errors="replace")
        m = re.search(r"^cover_image:\s*(.+)$", text, re.M)
        if not m:
            continue
        path = m.group(1).strip().strip('"')
        if path.startswith("/"):
            url = "https://clawbank.co" + path
        else:
            url = normalize_url(path)
            if not url:
                continue
        covers[f"clawbank-{md.stem}"] = url
    return covers


def singularity_covers() -> dict[str, str]:
    covers = {}
    folder = SOURCE_DIR / "singularity-hacker"
    if not folder.exists():
        return covers
    for page in folder.glob("*.html"):
        text = page.read_text(errors="replace")
        og = re.search(r'<meta property="og:image" content="([^"]+)"', text)
        hero = re.search(r'<img[^>]+class="[^"]*post-full-image[^"]*"[^>]+src="([^"]+)"', text)
        src = (og.group(1) if og else "") or (hero.group(1) if hero else "")
        if not src:
            continue
        if src.startswith("/"):
            src = "https://singularityhacker.com" + src
        url = normalize_url(src)
        if url:
            covers[f"sh-{page.stem}"] = url
    return covers


# Site chrome only — not the designed title-card heroes (those live in coverPhotoUrl).
PLACEHOLDER_COVER = re.compile(r"(?:logo\.png|play\.png|branding/)", re.I)
PARAGRAPH_CHROME = (
    "63e5f16669b3b00cd647",  # profile avatar
    "paragraph.com/branding",
)


def is_placeholder_cover(url: str) -> bool:
    if not url:
        return True
    if PLACEHOLDER_COVER.search(url):
        return True
    return any(part in url for part in PARAGRAPH_CHROME)


def paragraph_cover_url(page_html: str) -> str | None:
    """Use Paragraph's designed hero (coverPhotoUrl), not the first body image."""
    og = re.search(r'<meta property="og:image" content="([^"]+)"', page_html)
    if og:
        raw = htmlmod.unescape(og.group(1))
        cover = (parse_qs(urlparse(raw).query).get("coverPhotoUrl") or [None])[0]
        if cover:
            return cover
    for src in re.findall(r'<img[^>]+src="([^"]+)"', page_html):
        url = normalize_url(htmlmod.unescape(src))
        if not url or is_placeholder_cover(url):
            continue
        stored = re.search(r"(https://storage\.googleapis\.com/papyrus_images/[^\"?]+)", url)
        if stored:
            return stored.group(1)
        if "papyrus_images" in url or "img.paragraph.com" in url:
            return url
    return None


def paragraph_covers(posts: list[dict]) -> dict[str, str]:
    covers = {}

    def one(post: dict) -> tuple[str, str | None]:
        html = fetch_text(post["canonical"])
        if not html:
            return post["slug"], None
        return post["slug"], paragraph_cover_url(html)

    targets = [p for p in posts if p["project"] in {"0xjustice", "qacc"}]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for slug, url in pool.map(one, targets):
            if url:
                covers[slug] = url
    return covers


def rewrite_html(html: str, mapping: dict[str, str], prefix: str) -> str:
    def repl(match: re.Match) -> str:
        url = normalize_url(match.group("url")) or match.group("url")
        local = mapping.get(url)
        if not local:
            return match.group(0)
        return f'{match.group("attr")}={match.group("q")}{prefix}{local}{match.group("q")}'

    html = ATTR_URL_RE.sub(repl, html)
    html = html.replace("{{DOMAIN}}", "https://paragraph.com")
    return html


def inject_cover(html: str, local_rel: str) -> str:
    if 'class="blog-cover"' in html:
        return re.sub(
            r'(<p class="blog-cover"><img src=")[^"]+(" alt="">)',
            rf"\1{local_rel}\2",
            html,
            count=1,
        )
    block = (
        f'\t\t\t<p class="blog-cover"><img src="{local_rel}" alt=""></p>\n'
    )
    return html.replace(
        '<div class="blog-prose">',
        block + '\t\t\t<div class="blog-prose">',
        1,
    )


def update_listing(posts: list[dict], covers: dict[str, str]) -> None:
    listing = (ROOT / "blog.html").read_text(encoding="utf-8")
    for post in posts:
        slug = post["slug"]
        cover = covers.get(slug)
        if not cover:
            continue
        marker = f'href="blog/{slug}.html"'
        idx = listing.find(marker)
        if idx < 0:
            continue
        card_start = listing.rfind('<article class="blog-card"', 0, idx)
        if card_start < 0:
            continue
        insert_at = listing.find(">", card_start) + 1
        snippet = (
            f'\n\t\t\t\t<div class="blog-card-cover">'
            f'\n\t\t\t\t\t<img src="blog/{cover}" alt="" loading="lazy">'
            f'\n\t\t\t\t</div>'
        )
        card_end = listing.find("</article>", card_start)
        card = listing[card_start:card_end]
        if re.search(r'<div class="blog-card-cover">', card):
            card = re.sub(
                r'(<div class="blog-card-cover">\s*<img src=")[^"]+(")',
                rf'\1blog/{cover}\2',
                card,
                count=1,
            )
            listing = listing[:card_start] + card + listing[card_end:]
            continue
        listing = listing[:insert_at] + snippet + listing[insert_at:]
    (ROOT / "blog.html").write_text(listing, encoding="utf-8")


def main() -> int:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    posts = json.loads((BLOG_DIR / "posts.json").read_text())

    print("Cleaning leftover theme chrome…")
    for page in BLOG_DIR.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        cleaned = clean_singularity_html(text)
        if cleaned != text:
            page.write_text(cleaned, encoding="utf-8")

    print("Collecting cover URLs…")
    covers_remote = {}
    covers_remote.update(clawbank_covers())
    covers_remote.update(singularity_covers())
    covers_remote.update(paragraph_covers(posts))
    print(f"  covers found: {len(covers_remote)}")

    wanted: dict[str, None] = {}
    for page in BLOG_DIR.glob("*.html"):
        html = page.read_text(encoding="utf-8")
        for url in collect_urls_from_html(html):
            if not is_chrome(url):
                wanted[url] = None
    for url in covers_remote.values():
        if url and not is_chrome(url):
            wanted[url] = None

    print(f"Downloading {len(wanted)} unique assets…")
    mapping: dict[str, str] = {}
    failed: list[dict] = []

    def one(url: str) -> tuple[str, str | None, str | None]:
        data, ctype, err = fetch_bytes(url)
        if not data:
            return url, None, err or "empty"
        name = local_name(url, ctype)
        (MEDIA_DIR / name).write_bytes(data)
        return url, f"media/{name}", None

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(one, url) for url in wanted]
        for fut in concurrent.futures.as_completed(futs):
            url, local, err = fut.result()
            if local:
                mapping[url] = local
                print(f"  ok   {local}  ← {url[:90]}")
            else:
                failed.append({"url": url, "error": err})
                print(f"  FAIL {url} — {err}")

    print("Rewriting pages…")
    local_covers = {}
    for page in BLOG_DIR.glob("*.html"):
        html = page.read_text(encoding="utf-8")
        html = rewrite_html(html, mapping, prefix="")
        slug = page.stem
        remote_cover = covers_remote.get(slug)
        local_cover = mapping.get(remote_cover) if remote_cover else None
        if local_cover:
            html = inject_cover(html, local_cover)
            local_covers[slug] = local_cover
        page.write_text(html, encoding="utf-8")

    for post in posts:
        if post["slug"] in local_covers:
            post["cover"] = f"blog/{local_covers[post['slug']]}"
    (BLOG_DIR / "posts.json").write_text(json.dumps(posts, indent=2) + "\n", encoding="utf-8")
    update_listing(posts, local_covers)

    report = {
        "downloaded": len(mapping),
        "failed": failed,
        "covers": len(local_covers),
        "bytes": sum(p.stat().st_size for p in MEDIA_DIR.iterdir() if p.is_file()),
    }
    (BLOG_DIR / "media-manifest.json").write_text(
        json.dumps({"map": mapping, "covers": local_covers, "failed": failed}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({k: report[k] for k in report if k != "failed"}, indent=2))
    if failed:
        print("failed", len(failed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
