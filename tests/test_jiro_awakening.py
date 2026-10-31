"""Jiro's confirmed awakening updates his current state without erasing its cost."""
from pathlib import Path
import hashlib
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


def page(filename):
    return (ROOT / filename).read_text(encoding='utf-8')


class JiroAwakeningTest(unittest.TestCase):
    def test_supplied_artwork_is_unchanged_and_appears_only_as_current_profile_art(self):
        artwork = (ROOT / 'assets/images/jiro-awakened.png').read_bytes()
        self.assertEqual(hashlib.sha256(artwork).hexdigest(),
                         '9041fa32b9fb44819fa6befb03864a247e2c21389db9ede07c5928038c22ab3e')
        self.assertEqual(struct.unpack('>II', artwork[16:24]), (1024, 1536))
        for filename in ('npcs/jiro.html', 'npcs/ichiro.html'):
            source = page(filename)
            self.assertIn('src="/aevum-archive/assets/images/jiro-awakened.png"', source)
            self.assertIn('width="1024" height="1536"', source)
            self.assertNotIn('src="/aevum-archive/assets/images/jiro-returned.png"', source)
        self.assertNotIn('jiro-awakened.png', page('npcs/index.html'))

    def test_hero_summarizes_training_power_goal_and_permanent_injury(self):
        hero = re.search(r'<section class="jiro-hero".*?</section>', page('npcs/jiro.html'), re.S).group(0)
        for fact in ('Free · Awakened', '<dt>Power Level</dt><dd>3000</dd>',
                     'Awakening with Ichiro', 'Permanent left-arm injury', 'Left hand needs special protection',
                     'href="#family-sword"', 'Current likeness'):
            self.assertIn(fact, hero)
        for obsolete in ('Free · Critical', 'Unconfirmed / Critical', 'may not survive', 'Whether he will ever wake'):
            self.assertNotIn(obsolete, hero)

    def test_family_sword_has_no_invented_identity_location_or_powers(self):
        source = page('npcs/jiro.html')
        sword = re.search(r'<section[^>]*id="family-sword".*?</section>', source, re.S).group(0)
        self.assertIn("family's inherited sword", sword)
        self.assertIn('passed down through generations', sword)
        self.assertIn('The sword is still to be found.', sword)
        self.assertNotRegex(sword, r'World Item|Legendary|Mythic|Divine|Excalibur|Soulbrand')
        self.assertNotRegex(source, r'arm (?:regenerated|regrew)|prosthetic|regeneration ability')

    def test_historical_aftermath_and_unknown_orb_mechanics_are_preserved(self):
        source = page('npcs/jiro.html')
        for history in ('Approx. 2200–2400', 'condition was critical', 'survival was uncertain',
                        'lost his left arm', 'massive hole in his chest', 'probably intercepted',
                        'Its precise amplification during that battle remains unknown',
                        'not a confirmed ability duration', 'Both earlier portraits predate'):
            self.assertIn(history, source)
        self.assertIn('her fate remains unconfirmed', source)
        self.assertIn('href="/aevum-archive/assets/images/jiro-returned.png"', source)
        self.assertIn('src="/aevum-archive/assets/images/jiro.png"', source)

    def test_connected_current_summaries_have_new_power_without_invented_other_outcomes(self):
        for filename in ('npcs/index.html', 'npcs/ichiro.html', 'npcs/bomir.html', 'characters/faaram.html',
                         'characters/bonds.html', 'lore/index.html', 'lore/history/ichiro-and-jiro.html',
                         'lore/factions/faaram-servants.html', 'lore/cosmology/souls.html', 'updates/index.html', 'index.html'):
            with self.subTest(filename=filename):
                source = page(filename)
                self.assertIn('3000 PL', source)
                self.assertNotIn('Free · Critical', source)
                self.assertNotIn('Jiro’s last recorded injuries remain unresolved', source)
        self.assertIn('<dt>Power Level</dt><dd>3300</dd>', page('npcs/ichiro.html'))
        self.assertIn('<dt>Power Level</dt><dd>2500</dd>', page('characters/faaram.html'))
        self.assertIn('Presence Lost / Fate Unconfirmed', page('npcs/poison.html'))
        self.assertIn('REPORTED NEAR DEATH', page('npcs/uwu.html'))
