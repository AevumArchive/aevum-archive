"""Index refresh must preserve public lore, navigation and classification boundaries."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GalleryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.fragments = []
        self.cards = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.fragments.append(attrs["href"][1:])
        if "npc-card" in attrs.get("class", "").split():
            self.cards += 1


class ArchiveGalleriesTest(unittest.TestCase):
    def test_navigation_has_unique_targets(self):
        for filename in ("npcs/index.html", "world-items/index.html"):
            with self.subTest(filename=filename):
                page = (ROOT / filename).read_text(encoding="utf-8")
                parser = GalleryParser()
                parser.feed(page)
                self.assertEqual(len(parser.ids), len(set(parser.ids)))
                self.assertTrue(set(parser.fragments).issubset(set(parser.ids)))
                if filename == "world-items/index.html":
                    self.assertIn("archive-galleries.css?v=20261022-1", page)
                    self.assertIn("gallery-page", page)
                else:
                    self.assertNotIn("archive-galleries.css", page)

    def test_every_npc_record_survives_without_javascript(self):
        page = (ROOT / "npcs/index.html").read_text(encoding="utf-8")
        parser = GalleryParser()
        parser.feed(page)
        self.assertEqual(parser.cards, 37)  # 34 named entries, 3 unopened presences.
        for name in ("Thalanil", "Rhys", "Varkhiel Dreadmar", "Raoul", "Arnold", "Mira", "Lilith", "Veyr",
                     "Izumi", "Bomir", "UWU", "Jiro", "Ichiro", "Keanu", "Timeo", "Arisu", "Nox", "Nyx", "Rapax",
                     "Poison", "Yori", "Kimiko", "Peter", "Hans", "Fritz", "J.A.R.V.I.S.", "John", "Deadshot",
                     "Uwubama", "Library Entity", "Chax", "Malrik", "Bobby", "???"):
            with self.subTest(name=name):
                self.assertIn(name, page)
        self.assertNotRegex(page, r'<[^>]+\shidden(?:[=\s>])')
        self.assertNotIn("Enski", page)
        self.assertNotIn("Tenrei", page)
        self.assertIn('<span class="pill">Fate Unconfirmed</span>', page)
        self.assertIn('<span class="pill">Reported Near Death</span>', page)

    def test_npc_index_keeps_the_original_special_divine_design(self):
        page = (ROOT / "npcs/index.html").read_text(encoding="utf-8")
        for marker in ('npc-index.css', 'npc-effects.css', 'npc-divine-ledger',
                       'npc-divine-card npc-feature-izumi', 'npc-divine-card npc-feature-bomir'):
            self.assertIn(marker, page)
        for removed in ('gallery-page', 'npc-portrait-thumb', 'npc-exhibit', 'npc-ledger.js'):
            self.assertNotIn(removed, page)
        styles = (ROOT / "assets/npc-index.css").read_text(encoding="utf-8")
        self.assertIn('rgba(109, 222, 145, .18)', styles)
        self.assertIn('rgba(231, 189, 89, .2)', styles)

    def test_relic_classifications_and_scaling_survive(self):
        page = (ROOT / "world-items/index.html").read_text(encoding="utf-8")
        for name in ("Red Orb", "Gray Orb", "Nocturne", "Treacherous Cleaver ×2", "Astera's Staff", "The Hollow Star.",
                     "Azure World Item Shard", "Divine Greatshield", "Runic Piercer"):
            self.assertIn(name, page)
        self.assertIn("Two distinct World Items", page)
        self.assertIn("Character-bound artifact · not a World Item", page)
        self.assertIn("not catalogued as a separate World Item", page)
        self.assertIn("not classified as a World Item", page)
        self.assertIn("No confirmed likeness", page)
        self.assertEqual(len(re.findall(r'<th scope="row">', page)), 14)
        for formula in ("+45% × 1.40 = +63%", "+35% × 1.40 = +49%", "It is not immunity."):
            self.assertIn(formula, page)
        self.assertIn('images/nocturne.jpg', page)
        self.assertIn('images/runic-piercer.jpg', page)

    def test_styles_are_index_scoped_and_respect_reduced_motion(self):
        styles = (ROOT / "assets/archive-galleries.css").read_text(encoding="utf-8")
        self.assertIn("body.gallery-page", styles)
        self.assertIn(".gallery-main [hidden] { display: none !important; }", styles)
        self.assertIn("prefers-reduced-motion: reduce", styles)
        self.assertIn("animation: none !important", styles)
        self.assertIn(":focus-visible", styles)


if __name__ == "__main__":
    unittest.main()
