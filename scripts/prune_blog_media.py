#!/usr/bin/env python3
"""Delete files in blog/media that no served page references.

localize_blog_media downloads every asset URL it sees, including Paragraph's
auto-generated og:image share cards and images from earlier revisions of a
post. Anything not referenced by blog.html, index.html, resume.html, a post
page, or site JS is dead weight in the deploy. Thumbnails in blog/media/thumbs
are managed by optimize_blog_covers and are left alone here.

Runs from build-blog.py and publish_local_posts.py; safe to run directly.
Pass --dry-run to list without deleting.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "blog"
MEDIA_DIR = BLOG_DIR / "media"


def referencing_text() -> str:
    pages = list(BLOG_DIR.glob("*.html"))
    pages += [ROOT / "blog.html", ROOT / "index.html", ROOT / "resume.html"]
    pages += list((ROOT / "js").glob("*.js"))
    pages += list((ROOT / "css").glob("*.css"))
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in pages if p.exists())


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry_run = "--dry-run" in argv
    if not MEDIA_DIR.exists():
        return 0
    corpus = referencing_text()
    orphans = [
        f for f in sorted(MEDIA_DIR.iterdir())
        if f.is_file() and f.name != ".DS_Store" and f.name not in corpus
    ]
    total = sum(f.stat().st_size for f in orphans)
    verb = "would remove" if dry_run else "removed"
    for f in orphans:
        if not dry_run:
            f.unlink()
    print(f"prune_blog_media: {verb} {len(orphans)} orphaned files ({total / 1e6:.1f} MB)")
    if dry_run:
        for f in orphans:
            print(f"  {f.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
