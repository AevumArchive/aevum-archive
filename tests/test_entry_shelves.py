"""Current-company and campaign selection must never reveal character portraits."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ShelfParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.fragments = []
        self.characters = []
        self.images = []
        self.main = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main":
            self.main = True
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.fragments.append(attrs["href"][1:])
        if "data-current-character" in attrs:
            self.characters.append((attrs["data-current-character"], attrs["href"]))
        if self.main and (tag == "img" or attrs.get("role") == "img"):
            self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == "main":
            self.main = False


class EntryShelvesTest(unittest.TestCase):
    def test_both_selection_pages_are_portrait_free(self):
        for filename in ("characters/index.html", "playthroughs/index.html"):
            with self.subTest(filename=filename):
                page = (ROOT / filename).read_text(encoding="utf-8")
                parsed = ShelfParser()
                parsed.feed(page)
                self.assertEqual(parsed.images, [])
                self.assertNotIn('assets/images/', page)
                self.assertNotIn('class="character-card', page)
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                self.assertTrue(set(parsed.fragments).issubset(set(parsed.ids)))
                self.assertIn('archive-shelves.css?v=20261022-1', page)
        styles = (ROOT / "assets/archive-shelves.css").read_text(encoding="utf-8")
        self.assertNotIn("url(", styles)
        self.assertIn("prefers-reduced-motion: reduce", styles)
        self.assertIn(":focus-visible", styles)

    def test_current_company_is_exactly_four_names(self):
        page = (ROOT / "characters/index.html").read_text(encoding="utf-8")
        parsed = ShelfParser()
        parsed.feed(page)
        self.assertEqual([key for key, _ in parsed.characters], ["faaram", "lythariel", "william-carter", "jango"])
        for key, link in parsed.characters:
            self.assertEqual(link, f"/aevum-archive/characters/{key}.html")
        self.assertIn("Four current names", page)
        self.assertIn("Wyrm Sovereign", page)
        self.assertIn("2500 PL", page)
        self.assertIn("Astera's whereabouts remain unknown; Beru's record is sealed.", page)
        for outsider in ("guts", "astera-zenith", "beru", "obama"):
            self.assertNotIn(f'href="/aevum-archive/characters/{outsider}.html"', page)

    def test_chronology_preserves_eras_dates_and_closed_states(self):
        page = (ROOT / "playthroughs/index.html").read_text(encoding="utf-8")
        for route in ("fantasy-medieval", "alterra-origin", "vault-8", "temmie-town", "aizen-ended-road"):
            self.assertIn(f'href="/aevum-archive/playthroughs/{route}.html"', page)
        for date in ("2017-05-04", "2019-02-23", "2021-06-21"):
            self.assertIn(f'datetime="{date}"', page)
        self.assertEqual(len(re.findall(r'class="era-index"', page)), 5)
        self.assertIn("Later / Previous World Era", page)
        self.assertIn("Further detail remains unopened here.", page)
        self.assertIn("Partial record", page)
        self.assertIn("Sealed", page)
        self.assertIn("Four current names", page)
        self.assertNotIn("Five active player records", page)


if __name__ == "__main__":
    unittest.main()
