#!/usr/bin/env python3
"""Hero extraction must use Paragraph's cover photo, not a body image."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "localize_blog_media",
    Path(__file__).resolve().parent / "localize-blog-media.py",
)
localize_blog_media = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(localize_blog_media)
is_placeholder_cover = localize_blog_media.is_placeholder_cover
paragraph_hero_url = localize_blog_media.paragraph_hero_url


HERO = "https://storage.googleapis.com/papyrus_images/e4db67ae4359b94ea088be6c487f748e7281cdbd15350c9678676715e3cbf952.jpg"
BODY = "https://storage.googleapis.com/papyrus_images/823630b4ab076659622e1107f5efab380c78c55af7f24dbace6af3da8b263c75.jpg"
AVATAR = "https://storage.googleapis.com/papyrus_images/63e5f16669b3b00cd6473cc3db11d29092d68f0659ac0a95c557ceb3e35de908.jpg"
OG = (
    "https://paragraph.com/api/og?title=All+Worlds+End+in+an+AI+Singularity"
    f"&amp;blogName=0xJustice.eth&amp;coverPhotoUrl={HERO.replace(':', '%3A').replace('/', '%2F')}"
    f"&amp;blogImageUrl={AVATAR.replace(':', '%3A').replace('/', '%2F')}"
    "&amp;publishedDate=1767735041075"
)


SAMPLE = f"""
<html>
<head>
<meta property="og:image" content="{OG}">
<script type="application/ld+json">
{{"@graph":[{{"@type":"Article","headline":"All Worlds End in an AI Singularity","image":{{"@type":"ImageObject","url":"{HERO}","width":1200,"height":630}}}}]}}
</script>
</head>
<body>
<img src="https://paragraph.com/branding/v2/black.png">
<img src="https://img.paragraph.com/cdn-cgi/image/format=auto/{HERO}">
<img src="https://img.paragraph.com/cdn-cgi/image/format=auto/{BODY}">
<img src="{AVATAR}">
</body>
</html>
"""


class ParagraphHeroTests(unittest.TestCase):
    def test_cover_photo_beats_body_image(self):
        self.assertEqual(paragraph_hero_url(SAMPLE), HERO)

    def test_jsonld_fallback_when_og_missing(self):
        html = SAMPLE.replace(OG, "https://paragraph.com/api/og?title=Only")
        html = html.replace("coverPhotoUrl=", "notACover=")
        self.assertEqual(paragraph_hero_url(html), HERO)

    def test_generated_og_card_is_placeholder(self):
        self.assertTrue(is_placeholder_cover("https://paragraph.com/api/og?title=X"))
        self.assertFalse(is_placeholder_cover(HERO))
        self.assertTrue(is_placeholder_cover(AVATAR))


if __name__ == "__main__":
    unittest.main()
