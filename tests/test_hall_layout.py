"""The Hall's environment can change, but its canonical records and state borders cannot."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HallParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "hall-card" in attrs.get("class", "").split():
            self.cards.append(attrs)


class HallLayoutTest(unittest.TestCase):
    def test_all_fifteen_records_and_status_layers_remain(self):
        page = (ROOT / "characters/all.html").read_text(encoding="utf-8")
        parsed = HallParser()
        parsed.feed(page)
        self.assertEqual(len(parsed.cards), 15)
        self.assertEqual(Counter(card["data-status"] for card in parsed.cards),
                         {"active": 5, "sealed": 4, "fallen": 3, "lost": 2, "retired": 1})
        for card in parsed.cards:
            self.assertIn("status-card", card["class"])
            self.assertTrue((ROOT / card["href"].removeprefix('/aevum-archive/')).is_file())
        self.assertEqual(page.count('class="hall-card-overlay"'), 15)
        self.assertNotIn('assets/images/', page)

    def test_environment_art_is_removed_and_heading_uses_the_full_width(self):
        page = (ROOT / "characters/all.html").read_text(encoding="utf-8")
        styles = (ROOT / "assets/character-status-frames.css").read_text(encoding="utf-8")
        for asset in ("characters-bg-hall-main.png", "characters-bg-side-left.png", "characters-bg-side-right.png"):
            self.assertNotIn(asset, styles)
        self.assertNotIn('class="hall-tapestry', page)
        self.assertNotIn('class="hall-divider"', page)
        self.assertIn('id="hall-title">Hall of Names</h1>', page)
        self.assertIn('character-status-frames.css?v=20261023-hall-layout', page)
        heading = re.search(r'body\.route-characters-all \.hall-heading-row\s*\{([^}]+)\}', styles).group(1)
        self.assertIn('grid-template-columns: minmax(0, 1fr)', heading)
        self.assertNotIn('1fr 220px', styles)

    def test_original_frame_and_motif_files_remain_in_use(self):
        styles = (ROOT / "assets/character-status-frames.css").read_text(encoding="utf-8")
        motifs = {"active": "aether", "sealed": "chains", "fallen": "broken-chains", "lost": "fracture", "retired": "drapery"}
        for state, motif in motifs.items():
            for filename in (f"hall-card-{state}-frame-1200x1800.png", f"hall-card-{state}-motif-{motif}-1200x1800.png"):
                with self.subTest(filename=filename):
                    self.assertIn(filename, styles)
                    self.assertTrue((ROOT / 'assets/hall-of-names/v4' / filename).is_file())
        self.assertIn('background-size: 100% 100%', styles)
        self.assertIn('inset: -5px', styles)
        self.assertIn('prefers-reduced-motion: reduce', styles)


if __name__ == "__main__":
    unittest.main()
