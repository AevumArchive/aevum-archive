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
    def test_all_records_and_status_layers_remain(self):
        page = (ROOT / "characters/all.html").read_text(encoding="utf-8")
        parsed = HallParser()
        parsed.feed(page)
        self.assertEqual(len(parsed.cards), 26)
        self.assertEqual(Counter(card["data-status"] for card in parsed.cards),
                         {"active": 4, "sealed": 5, "fallen": 8, "lost": 5, "retired": 4})
        statuses = {card["data-name"]: card["data-status"] for card in parsed.cards}
        for name in ("Thomas Meyer", "Tony Arasaka"):
            self.assertEqual(statuses[name], "retired")
        self.assertEqual(statuses["Jango"], "sealed")
        self.assertEqual(statuses["Jon Snow"], "lost")
        self.assertEqual(statuses["Solaire"], "fallen")
        self.assertEqual(statuses["Guts"], "fallen")
        self.assertEqual(statuses["Guts (Royal Bodyguard)"], "retired")
        for card in parsed.cards:
            self.assertIn("status-card", card["class"])
            self.assertTrue((ROOT / card["href"].removeprefix('/aevum-archive/')).is_file())
        self.assertEqual(page.count('class="hall-card-overlay"'), 26)
        self.assertNotIn('assets/images/', page)

    def test_environment_art_is_removed_and_heading_uses_the_full_width(self):
        page = (ROOT / "characters/all.html").read_text(encoding="utf-8")
        styles = (ROOT / "assets/character-status-frames.css").read_text(encoding="utf-8")
        for asset in ("characters-bg-hall-main.png", "characters-bg-side-left.png", "characters-bg-side-right.png"):
            self.assertNotIn(asset, styles)
        self.assertNotIn('class="hall-tapestry', page)
        self.assertNotIn('class="hall-divider"', page)
        self.assertIn('id="hall-title">Hall of Names</h1>', page)
        self.assertRegex(page, r'character-status-frames\.css\?v=')
        heading = re.search(r'body\.route-characters-all \.hall-heading-row\s*\{([^}]+)\}', styles).group(1)
        self.assertIn('grid-template-columns: minmax(0, 1fr)', heading)
        self.assertNotIn('1fr 220px', styles)

    def test_each_status_uses_a_self_contained_vector_ornament(self):
        styles = (ROOT / "assets/character-status-frames.css").read_text(encoding="utf-8")
        self.assertNotIn('hall-of-names/v4/', styles)
        for state in ("active", "sealed", "fallen", "lost", "retired"):
            with self.subTest(state=state):
                relative_path = f"hall-of-names/engraved/{state}.svg"
                self.assertRegex(styles, rf'url\("{re.escape(relative_path)}(?:\?[^"]+)?"\)')
                engraving = (ROOT / "assets" / relative_path).read_text(encoding="utf-8")
                self.assertIn('viewBox="0 0 240 360"', engraving)
                self.assertNotIn('<image', engraving)


if __name__ == "__main__":
    unittest.main()
