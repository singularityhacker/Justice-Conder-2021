#!/usr/bin/env python3
"""Generate small WebP thumbnails for blog cover images and point the pages at them.

The listing (blog.html) and every post page reference the original uploads in
blog/media, which are often multi-megabyte PNGs and animated GIFs. This step:

  * writes 21:9 card thumbnails at 480w and 960w for every card on blog.html
    (animated GIFs become a static first frame there),
  * writes a 1600w hero for each post page's cover (GIFs are left animated),
  * rewrites the <img> tags with src/srcset/sizes/width/height,
  * removes thumbnails that are no longer referenced.

Thumbnail names include a content hash so they can be cached as immutable.
Safe to re-run; it only regenerates missing files. Requires ImageMagick 7
(`magick`) on PATH. Runs automatically at the end of build-blog.py and
publish_local_posts.py; run directly after any manual edit to blog.html.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "blog"
MEDIA_DIR = BLOG_DIR / "media"
THUMB_DIR = MEDIA_DIR / "thumbs"
LISTING = ROOT / "blog.html"

CARD_WIDTHS = (480, 960)
CARD_RATIO = 21 / 9  # matches .blog-card-cover { aspect-ratio: 21 / 9 }
CARD_SIZES = "(max-width: 600px) 100vw, (max-width: 960px) 50vw, 380px"
HERO_WIDTH = 1600
EAGER_CARDS = 3  # first row loads immediately; the rest stay lazy
WEBP_QUALITY = "78"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}

CARD_IMG_RE = re.compile(
    r'(?P<open><div class="blog-card-cover">\s*)<img (?P<attrs>[^>]*?)\s*/?>',
    re.S,
)
HERO_IMG_RE = re.compile(r'<p class="blog-cover"><img (?P<attrs>[^>]*?)\s*/?></p>')
ATTR_RE = re.compile(r'([a-zA-Z-]+)="([^"]*)"')


def attrs_of(text: str) -> dict[str, str]:
    return dict(ATTR_RE.findall(text))


def card_height(width: int) -> int:
    return round(width / CARD_RATIO)


def file_hash(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:8]


def identify(path: Path) -> tuple[int, int] | None:
    try:
        out = subprocess.run(
            ["magick", "identify", "-format", "%w %h", f"{path}[0]"],
            check=True, capture_output=True, text=True,
        ).stdout.split()
        return int(out[0]), int(out[1])
    except (subprocess.CalledProcessError, ValueError, IndexError):
        return None


def make_card_thumb(src: Path, dest: Path, width: int) -> None:
    height = card_height(width)
    subprocess.run(
        [
            "magick", f"{src}[0]",
            "-auto-orient", "-strip", "-background", "none",
            "-resize", f"{width}x{height}^",
            "-gravity", "center", "-extent", f"{width}x{height}",
            "-quality", WEBP_QUALITY, "-define", "webp:method=6",
            str(dest),
        ],
        check=True, capture_output=True,
    )


def make_hero(src: Path, dest: Path, width: int) -> None:
    subprocess.run(
        [
            "magick", str(src),
            "-auto-orient", "-strip",
            "-resize", f"{width}x>",
            "-quality", "80", "-define", "webp:method=6",
            str(dest),
        ],
        check=True, capture_output=True,
    )


class Job:
    """One source image and the derivatives it needs."""

    def __init__(self, src: Path) -> None:
        self.src = src
        self.hash = file_hash(src)
        self.stem = f"{src.stem}-{self.hash}"
        self.dims = identify(src)
        self.card_files: dict[int, Path] = {}
        self.hero_file: Path | None = None
        self.hero_dims: tuple[int, int] | None = None

    def card_widths(self) -> list[int]:
        if not self.dims:
            return []
        src_w = self.dims[0]
        widths = [w for w in CARD_WIDTHS if w <= src_w]
        return widths or [min(src_w, CARD_WIDTHS[0])]

    def plan_cards(self) -> None:
        for w in self.card_widths():
            self.card_files[w] = THUMB_DIR / f"{self.stem}-{w}.webp"

    def plan_hero(self) -> None:
        if not self.dims:
            return
        w, h = self.dims
        if w > HERO_WIDTH:
            h = round(h * HERO_WIDTH / w)
            w = HERO_WIDTH
        self.hero_dims = (w, h)
        self.hero_file = THUMB_DIR / f"{self.stem}-hero.webp"

    def build(self) -> list[str]:
        made = []
        for w, dest in self.card_files.items():
            if not dest.exists():
                make_card_thumb(self.src, dest, w)
                made.append(dest.name)
        if self.hero_file and not self.hero_file.exists():
            make_hero(self.src, self.hero_file, HERO_WIDTH)
            made.append(self.hero_file.name)
        return made


def original_from_attrs(attrs: dict[str, str], page_dir: Path) -> Path | None:
    """Resolve the source image an <img> refers to, whether or not it has been rewritten already."""
    candidate = attrs.get("data-original") or attrs.get("src") or ""
    if not candidate or candidate.startswith(("http:", "https:", "data:")):
        return None
    path = (page_dir / candidate).resolve()
    if THUMB_DIR in path.parents:
        return None  # rewritten tag without data-original; nothing to do
    if path.suffix.lower() not in IMAGE_EXTS or not path.is_file():
        return None
    return path


def rel(path: Path, page_dir: Path) -> str:
    return path.relative_to(page_dir).as_posix()


def card_tag(job: Job, page_dir: Path, index: int) -> str:
    widths = sorted(job.card_files)
    largest = widths[-1]
    srcset = ", ".join(f"{rel(job.card_files[w], page_dir)} {w}w" for w in widths)
    loading = "eager" if index < EAGER_CARDS else "lazy"
    return (
        f'<img src="{rel(job.card_files[largest], page_dir)}"'
        f' srcset="{srcset}"'
        f' sizes="{CARD_SIZES}"'
        f' width="{largest}" height="{card_height(largest)}"'
        f' alt="" loading="{loading}" decoding="async"'
        f' data-original="{rel(job.src, page_dir)}">'
    )


def hero_tag(job: Job, page_dir: Path) -> str:
    assert job.hero_file and job.hero_dims
    w, h = job.hero_dims
    return (
        f'<p class="blog-cover"><img src="{rel(job.hero_file, page_dir)}"'
        f' width="{w}" height="{h}" alt="" decoding="async"'
        f' data-original="{rel(job.src, page_dir)}"></p>'
    )


def main() -> int:
    if not shutil.which("magick"):
        print("optimize_blog_covers: ImageMagick `magick` not found; skipping.", file=sys.stderr)
        return 1
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    jobs: dict[Path, Job] = {}

    def job_for(src: Path) -> Job:
        if src not in jobs:
            jobs[src] = Job(src)
        return jobs[src]

    # Listing cards
    listing_html = LISTING.read_text(encoding="utf-8")
    card_plan: list[tuple[re.Match, Job]] = []
    for match in CARD_IMG_RE.finditer(listing_html):
        src = original_from_attrs(attrs_of(match.group("attrs")), ROOT)
        if not src:
            continue
        job = job_for(src)
        job.plan_cards()
        card_plan.append((match, job))

    # Post-page heroes (GIFs stay animated, so they are not converted)
    hero_plan: dict[Path, list[tuple[re.Match, Job]]] = {}
    for page in sorted(BLOG_DIR.glob("*.html")):
        html = page.read_text(encoding="utf-8")
        for match in HERO_IMG_RE.finditer(html):
            src = original_from_attrs(attrs_of(match.group("attrs")), BLOG_DIR)
            if not src or src.suffix.lower() == ".gif":
                continue
            job = job_for(src)
            job.plan_hero()
            hero_plan.setdefault(page, []).append((match, job))

    print(f"optimize_blog_covers: {len(card_plan)} cards, "
          f"{sum(len(v) for v in hero_plan.values())} heroes, {len(jobs)} source images")

    failures: list[str] = []
    made: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(j.build): j for j in jobs.values()}
        for fut in concurrent.futures.as_completed(futs):
            job = futs[fut]
            try:
                made += fut.result()
            except subprocess.CalledProcessError as exc:
                failures.append(f"{job.src.name}: {exc.stderr.decode(errors='replace').strip()[:200]}")
    print(f"  generated {len(made)} new files")
    for line in failures:
        print(f"  FAIL {line}")

    # Rewrite the listing
    index = 0
    def card_repl(match: re.Match) -> str:
        nonlocal index
        job = next((j for m, j in card_plan if m.start() == match.start()), None)
        if not job or not job.card_files or not all(p.exists() for p in job.card_files.values()):
            return match.group(0)
        tag = card_tag(job, ROOT, index)
        index += 1
        return f"{match.group('open')}{tag}"
    new_listing = CARD_IMG_RE.sub(card_repl, listing_html)
    if new_listing != listing_html:
        LISTING.write_text(new_listing, encoding="utf-8")
    print(f"  rewrote {index} card images in blog.html")

    # Rewrite post pages
    rewritten = 0
    for page, plan in hero_plan.items():
        html = page.read_text(encoding="utf-8")
        def hero_repl(match: re.Match) -> str:
            job = next((j for m, j in plan if m.start() == match.start()), None)
            if not job or not job.hero_file or not job.hero_file.exists():
                return match.group(0)
            return hero_tag(job, BLOG_DIR)
        new_html = HERO_IMG_RE.sub(hero_repl, html)
        if new_html != html:
            page.write_text(new_html, encoding="utf-8")
            rewritten += 1
    print(f"  rewrote covers in {rewritten} post pages")

    # Drop thumbnails nothing references anymore
    keep = {p for j in jobs.values() for p in j.card_files.values()}
    keep |= {j.hero_file for j in jobs.values() if j.hero_file}
    removed = 0
    for stale in THUMB_DIR.glob("*.webp"):
        if stale not in keep:
            stale.unlink()
            removed += 1
    if removed:
        print(f"  removed {removed} stale thumbnails")

    total = sum(p.stat().st_size for p in THUMB_DIR.glob("*.webp"))
    print(f"  thumbs dir: {len(list(THUMB_DIR.glob('*.webp')))} files, {total / 1_000_000:.1f} MB")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
