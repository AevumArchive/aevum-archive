"""Astera's visual refresh must preserve her uncertain fate and witnessed discoveries."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DossierParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.fragments.append(attrs["href"][1:])


class AsteraDossierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "characters/astera-zenith.html").read_text(encoding="utf-8")
        cls.styles = (ROOT / "assets/astera-dossier.css").read_text(encoding="utf-8")

    def test_hero_keeps_last_confirmed_state_and_full_portrait(self):
        hero = re.search(r'<section class="astral-hero".*?</section>', self.page, re.S).group(0)
        for fact in ('<dt>Status</dt><dd>LOST / UNKNOWN</dd>', '<dt>Race</dt><dd>Elf</dd>',
                     '<dt>Path</dt><dd>Star Magic / Dark Astral</dd>', '<dt>Instructor</dt><dd>Mythic</dd>',
                     '<dt>Known Bond</dt><dd>Jango</dd>', '<dd>Hollow Star · COMPLETE</dd>',
                     '<dd>STABILIZED · Left Eye Fully Awakened</dd>',
                     'Her current whereabouts are unknown; no death is confirmed.'):
            self.assertIn(fact, hero)
        self.assertNotIn("Power Level", hero)
        self.assertEqual(self.page.count('src="/aevum-archive/assets/images/astera-zenith-cosmic-ruins.png"'), 1)
        self.assertNotIn('class="record-hero"', self.page)
        self.assertIn("align-self: start", self.styles)
        self.assertIn("width: 100%; height: auto", self.styles)

    def test_all_chapters_resolve_without_duplicate_ids(self):
        parsed = DossierParser()
        parsed.feed(self.page)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertTrue(set(parsed.fragments).issubset(set(parsed.ids)))
        self.assertEqual(len(re.findall(r'<a href="#', self.page.split('class="astral-chapters"')[1].split('</nav>')[0])), 7)

    def test_discoveries_artwork_and_unresolved_boundaries_survive(self):
        for phrase in ("major but incomplete portion", "Neither is confirmed to hold her entire soul.",
                       "The Mark's present state is unresolved.", "The Silent Gate", "The Hall of Second Sight",
                       "And still I remain.", "The Umbral Meridian", "Beyond the Mark", "it is not yet her home",
                       "A Name Unknown to the World... Until Now.", "+250,000 Points", "Tenrei",
                       "not a battle", "Duality", "zero-slot Signature Trait", "Historical / unrealized vision",
                       "Dominant current trajectory", "Magical Understanding and Cleansing Breath"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.page)
        self.assertIn('astera-umbral-meridian-quest-complete.png', self.page)
        self.assertIn('class="divine-discovery-card"', self.page)
        self.assertIn(".astera-dossier .divine-discovery-card", self.styles)
        self.assertIn("prefers-reduced-motion: reduce", self.styles)
        self.assertIn(":focus-visible", self.styles)


if __name__ == "__main__":
    unittest.main()
