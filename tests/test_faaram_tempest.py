"""The October 20 canon supersedes former current identity and power values."""

from html import unescape
from html.parser import HTMLParser
import hashlib
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RecordParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.abilities = []
        self.weapons = []
        self.ids = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-ability" in attrs:
            self.abilities.append(attrs["data-ability"])
        if "data-weapon" in attrs:
            self.weapons.append(attrs["data-weapon"])
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.anchors.append(attrs["href"][1:])


class FaaramTempestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detail = (ROOT / "characters/faaram.html").read_text(encoding="utf-8")
        cls.text = " ".join(unescape(re.sub(r"<[^>]+>", " ", cls.detail)).split())

    def test_current_identity_and_power_are_unambiguous(self):
        self.assertIn("Faaram Tempest — Ascended", self.detail)
        hero = re.search(r'<section class="tempest-hero".*?</section>', self.detail, re.S).group(0)
        for fact in ('<dt>Power Level</dt><dd>2500</dd>', '<dt>State</dt><dd>ASCENDED</dd>', '<dt>Status</dt><dd>ACTIVE</dd>'):
            self.assertIn(fact, hero)
        self.assertNotRegex(hero, r"908|2050|The Faceless</h1>")
        self.assertIn("Historical milestone", self.detail)
        self.assertIn("+450 PL since initial Ascension", self.text)
        self.assertIn("Whole. Sovereign. Faaram Tempest.", self.text)
        self.assertIn("Not a fragment. A whole being.", self.text)
        self.assertIn("Faaram Tempest is a complete, independent being.", self.text)
        self.assertIn("not a form waiting to end", self.text)
        self.assertNotRegex(self.detail, r"(?i)faceless|first piece|champion vessel|further integration")

    def test_connected_records_do_not_assign_the_old_identity(self):
        for filename in ("characters/bonds.html", "npcs/nox.html", "npcs/nyx.html", "npcs/rapax.html", "npcs/poison.html", "playthroughs/aizen-ended-road.html", "updates/index.html"):
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"(?i)faceless|first piece")

    def test_all_eighteen_kit_entries_and_three_unique_weapons(self):
        parsed = RecordParser()
        parsed.feed(self.detail)
        expected = {"Summoner's Authority", "Ritual Mastery", "Named Servant Ritual", "Command Seal: Kneel", "Silence Circle",
                    "Harvest Festival", "Wyrmheart Cataclysm", "Crown of the Ancient Wyrm", "Wyrmheart Dominion", "The Wyrm Does Not Kneel",
                    "Hellborn Instinct", "Soulbrand", "Ninefold Perception", "Foxfire Reversal", "Everthorn", "Battle Memory", "Thorn Instinct", "The Fourth Exchange"}
        self.assertEqual(set(parsed.abilities), expected)
        self.assertEqual(len(parsed.abilities), 18)
        self.assertEqual(parsed.weapons, ["Icewhisper", "Soul Devourer", "Demigod's Unholy Blade"])
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertTrue(set(parsed.anchors).issubset(set(parsed.ids)))

    def test_current_portrait_is_the_supplied_tempest_artwork(self):
        artwork = (ROOT / "assets/images/faaram-tempest.png").read_bytes()
        self.assertEqual(hashlib.sha256(artwork).hexdigest(),
                         "af1400393858726266ad3490915724424915e6299e440cf214b48f90ec7c2e2b")
        self.assertEqual(struct.unpack(">II", artwork[16:24]), (1024, 1536))
        hero = re.search(r'<section class="tempest-hero".*?</section>', self.detail, re.S).group(0)
        self.assertIn('src="/aevum-archive/assets/images/faaram-tempest.png"', hero)
        self.assertNotIn('src="/aevum-archive/assets/images/faaram.png"', hero)
        self.assertIn('width="1024" height="1536"', hero)
        self.assertIn("Ascended · Icewhisper", hero)

    def test_everthorn_history_and_counter_limits(self):
        for phrase in ("Five legendary elven warriors", "S'klrdor", "One fell", "four survivors", "Legendary Warrior Trait",
                       "Up to +15%", "+20%", "+25%", "+50%", "Three observations do not reveal every attack",
                       "deceptive variants", "Applies to the learned pattern, not universal resistance"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_legacy_mechanics_preserve_limits(self):
        for phrase in ("approximately 12 seconds", "+70%", "+45%", "+35%", "+50%", "Every third meaningful successful hit",
                       "maximum of 5 stacks", "approximately 10 seconds", "+40% Potency", "Once per encounter",
                       "Not absolute immortality", "conceptual destruction", "35% Health", "Fear Immunity",
                       "Not unconditional reflection", "Compatibility, strength and opposed power still matter"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_ascended_icewhisper_and_other_weapons(self):
        for phrase in ("ASCENDED UNIQUE / Godslayer Frost Polearm", "+260", "55%", "42%", "90%", "45%", "110%", "+300",
                       "One Demi-God", "One Demon Lord", "Two Thrones Broken", "White Silence", "Winter Remembers", "Shatter the Throne",
                       "Absolute Silence", "Godblood Crystallized", "Crownbreaker Winter", "−60% resistance during the encounter",
                       "+250% Damage", "1.5 seconds", "Does not automatically hard-freeze every Boss", "+210", "+195",
                       "No specific stored souls are recorded here", "once per Ascension"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_knowledge_and_preserved_history(self):
        for phrase in ("Programming", "Engineering remains part of Aevum's broader progression", "TemmieTown", "SEMPAI",
                       "knows the location of The Library", "Götterfamilie", "hierarchy remain unrevealed", "Gray Orb", "Nocturne",
                       "Runic Piercer", "Lost", "Overlord's Grace", "8th recorded bearer", "not a relic or a separate World Item",
                       "Reclaiming His Place · COMPLETE", "Hollow Star did not transfer cleanly", "Astera's destination remain unresolved"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)
        self.assertNotIn("God Family", self.text)
        for internal in ("DEFINITION_ONLY", "NOT IMPLEMENTED", "COMING SOON", "NO HANDLER", "PROVIDER MISSING", "INTERNAL ONLY"):
            self.assertNotIn(internal, self.detail)

    def test_connected_current_shelves_match(self):
        for filename in ("characters/index.html", "characters/all.html", "index.html", "updates/index.html"):
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("Faaram Tempest", text)
                self.assertIn("2500 PL", text)
        self.assertIn('data-status="active" data-name="Faaram Tempest"', (ROOT / "characters/all.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
