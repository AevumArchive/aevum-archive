"""Ichiro's awakening and power share do not invent calculated stats or inherited traits."""

import hashlib
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


def page(filename):
    return (ROOT / filename).read_text(encoding="utf-8")


class IchiroAwakeningTest(unittest.TestCase):
    def test_supplied_artwork_is_unchanged_and_has_accurate_dimensions(self):
        artwork = (ROOT / "assets/images/ichiro-awakened.png").read_bytes()
        self.assertEqual(hashlib.sha256(artwork).hexdigest(),
                         "8687ed0f0ac5529d8fd149b41aae84e992bb774618b47ffb42106342108eadcc")
        self.assertEqual(struct.unpack(">II", artwork[16:24]), (1087, 1447))
        for filename in ("npcs/ichiro.html", "npcs/jiro.html"):
            source = page(filename)
            self.assertIn('src="/aevum-archive/assets/images/ichiro-awakened.png"', source)
            self.assertIn('width="1087" height="1447"', source)
            self.assertNotIn('src="/aevum-archive/assets/images/ichiro.png"', source)
        self.assertIn(".ichiro-dossier .jiro-hero-art { align-self: start; }", page("assets/ichiro-dossier.css"))

    def test_awake_identity_and_training_are_visible_in_the_hero(self):
        hero = re.search(r'<section class="jiro-hero".*?</section>', page("npcs/ichiro.html"), re.S).group(0)
        for fact in ("<dt>Status</dt><dd>Free · Awake</dd>", "<dt>Power Level</dt><dd>3300</dd>",
                     "15% of Jiro’s power", "awakened further strength", "Current likeness"):
            self.assertIn(fact, hero)
        self.assertNotRegex(hero.lower(), r"unconscious|before his liberation|dead|betrayer")

    def test_all_current_ichiro_summaries_have_moved_beyond_unconscious_recovery(self):
        for filename in ("npcs/index.html", "characters/bonds.html", "characters/faaram.html", "npcs/jiro.html",
                         "lore/index.html", "lore/history/ichiro-and-jiro.html", "lore/factions/faaram-servants.html",
                         "lore/cosmology/souls.html", "lore/dimensions/shadow-realm.html", "npcs/uwu.html", "npcs/keanu.html"):
            with self.subTest(filename=filename):
                source = page(filename)
                self.assertIn("3300 PL", source)
                for obsolete in ("Ichiro remains unconscious", "Free · Unconscious", "Free · unconscious",
                                 "For now, all he can do is wait for Ichiro to wake", "He is now free, unconscious and recovering"):
                    self.assertNotIn(obsolete, source)

    def test_donor_share_does_not_calculate_a_jiro_power_level_or_new_trait(self):
        jiro = page("npcs/jiro.html")
        hero = re.search(r'<dl class="jiro-identity-facts">.*?</dl>', jiro, re.S).group(0)
        self.assertIn("<dt>Power Level</dt><dd>3000</dd>", hero)
        self.assertIn("Approx. 2200–2400", hero)
        self.assertNotRegex(jiro, r"22000|22,000|18700|18,700")
        source = page("npcs/ichiro.html")
        self.assertNotIn("inherited Reinforced Soul", source)
        self.assertNotIn("15% PL", source)

    def test_severance_and_closed_seal_are_preserved_as_history(self):
        source = page("npcs/ichiro.html")
        self.assertIn("The violent severance had left him unconscious", source)
        self.assertIn("That unconscious recovery now belongs to the earlier aftermath", source)
        self.assertIn("The soul record remains sealed", source)
        self.assertNotIn("Lift the Soul Seal", source)
        self.assertNotRegex(source, r'<(?:button|summary|details)\b')
        seal = re.search(r'<article class="ichiro-portrait ichiro-seal-card".*?</article>', source, re.S).group(0)
        self.assertNotRegex(seal, r'\s(?:onclick|tabindex|hidden|aria-controls|href)=|role="button"')


if __name__ == "__main__":
    unittest.main()
