"""The Violet Eclipse record preserves earlier discoveries and current canon."""

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

    def test_hero_shows_current_canon_and_keeps_unfiltered_portrait(self):
        hero = re.search(r'<section class="astral-hero".*?</section>', self.page, re.S).group(0)
        for fact in ('<span class="astral-status">Active / Alive</span>', '<dt>Race</dt><dd>Elf</dd>',
                     'Head of House Zenith', 'Dark Astral · Mastered', '<dt>Instructor</dt><dd>Mythic</dd>',
                     '>Zenith Estate</a>', '>Jango</a>', 'Duality · Unresolved', 'Diadem of the Silent Orbit'):
            self.assertIn(fact, hero)
        self.assertIn('<span>Power Level</span><strong aria-label="Unknown">???</strong>', hero)
        self.assertIn('<title>Astera Zenith, The Violet Eclipse - Aevum Archive</title>', self.page)
        self.assertNotIn('Lost / Unknown', hero)
        self.assertEqual(hero.count('src="/aevum-archive/assets/images/astera-dark-astral-complete.webp"'), 1)
        self.assertIn('wound beneath her awakened left eye', hero)
        self.assertNotRegex(self.page, r'luminous (?:violet )?injury')
        self.assertIn('>The Faceless</a> left the wound beneath it while trying to tear the Hollow Star from her.', self.page)
        self.assertNotIn('astral-portrait-aura', self.page)
        self.assertNotIn('class="record-hero"', self.page)
        self.assertIn('class="astral-sky"', self.page)
        self.assertIn("@keyframes astral-fragment", self.styles)

    def test_all_chapters_resolve_without_duplicate_ids(self):
        parsed = DossierParser()
        parsed.feed(self.page)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertTrue(set(parsed.fragments).issubset(set(parsed.ids)))
        chapters = self.page.split('class="astral-chapters"')[1].split('</nav>')[0]
        self.assertEqual(len(re.findall(r'<a href="#', chapters)), 15)
        self.assertIn('href="#diadem-of-the-silent-orbit"', chapters)
        self.assertIn('last-sighting', parsed.ids)
        self.assertIn('last-sighting-title', parsed.ids)
        self.assertNotIn('unresolved-records', parsed.ids)

    def test_return_and_house_folios_keep_testimony_qualified(self):
        timeline = self.page.split('<ol class="astral-timeline"', 1)[1].split('</ol>', 1)[0]
        self.assertEqual(re.findall(r'<h3(?: [^>]*)?>([^<]+)</h3>', timeline), [
            'The Unrecorded Return', 'The Claim of Zenith', 'The Zenith Restoration',
            'The Zenith Dispute', 'The Sealed Archives',
        ])
        house = (ROOT / "lore/noble-houses/house-zenith.html").read_text(encoding="utf-8")
        self.assertIn('<p>Astera stripped several opponents of their positions and banished them from the lands under her authority.</p>', timeline)
        self.assertIn('Unverified accounts</strong> Some exiles are said to have returned', timeline)
        testimony = re.search(r'<aside class="zenith-testimony".*?</aside>', house, re.S).group(0)
        self.assertIn('>Unverified Accounts</h3>', testimony)
        self.assertIn('are said to have returned and been killed', testimony)
        self.assertNotIn('stripped several opponents', testimony)
        self.assertIn('stripped several opponents of their positions and banished them', house)
        for record in (timeline, house):
            self.assertIn('reliability of these accounts remain unverified', record)
            self.assertIn('regardless of noble ancestry', record)
        self.assertIn('<dt>Heraldry</dt><dd>The Split Star</dd>', house)
        self.assertIn('<dt>Wider influence</dt><dd>Unconfirmed</dd>', house)

    def test_dev_note_appears_beside_archive_footer_credit(self):
        footer = self.page.split('<footer class="footer">', 1)[1].split('</footer>', 1)[0]
        self.assertRegex(footer, r'witnessed knowledge only\.</span>\s*<span class="astral-dev-note">DEV approved')

    def test_house_and_characters_share_the_council_panorama(self):
        house = (ROOT / "lore/noble-houses/house-zenith.html").read_text(encoding="utf-8")
        panorama = "/aevum-archive/assets/images/astera-zenith-council.webp"
        for record in (self.page, house):
            self.assertEqual(record.count('src="' + panorama + '"'), 1)
            self.assertRegex(record, r'<img src="' + re.escape(panorama) + r'"[^>]+width="1912" height="823" loading="lazy" decoding="async">')
        self.assertIn('characters/astera-zenith.html#zenith-council', house)

    def test_diadem_keeps_worn_and_shrine_effects_distinct(self):
        worn, shrine = re.findall(r'<article class="diadem-mode .*?</article>', self.page, re.S)
        for phrase in ('Power Level 2,500', 'Magical Power</dt><dd>+529',
                       'Elemental Power</dt><dd>+380', '+11%</strong> effect radius',
                       'current Power Level is unknown', 'both stats are also unknown'):
            self.assertIn(phrase, worn)
        for phrase in ('250 blocks', 'Bedrock than on Obsidian', 'Moonstone',
                       'Day</small> Spell range', 'Night</small> Magical Power',
                       'Echo Stone', 'lingers briefly after leaving the shrine'):
            self.assertIn(phrase, shrine)
        self.assertIn('Minimum Power Level</dt><dd>500', self.page)

    def test_discoveries_artwork_and_unresolved_boundaries_survive(self):
        for phrase in ("major but incomplete portion", "Neither is confirmed to hold her entire soul.",
                       "Nothing of the binding remains on Astera’s soul.", "The Silent Gate", "The Hall of Second Sight",
                       "And still I remain.", "The Umbral Meridian", "Beyond the Mark", "it is not yet her home",
                       "A Name Unknown to the World... Until Now.", "+250,000 Points", "Tenrei",
                       "not a battle", "Duality", "zero-slot Signature Trait", "Historical / unrealized vision",
                       "Mastered path", "Magical Understanding and Cleansing Breath"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.page)
        self.assertIn('astera-umbral-meridian-quest-complete.png', self.page)
        self.assertIn('class="divine-discovery-card"', self.page)
        self.assertIn(".astera-dossier .divine-discovery-card", self.styles)
        self.assertIn("prefers-reduced-motion: reduce", self.styles)
        self.assertIn(":focus-visible", self.styles)


if __name__ == "__main__":
    unittest.main()
