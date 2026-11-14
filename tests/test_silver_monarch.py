"""Keep the alternate sovereign separate from player Faaram and preserve ability limits."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SilverMonarchTest(unittest.TestCase):
    def test_twelve_arts_preserve_their_limits_and_history_is_not_an_ability(self):
        page = (ROOT / 'npcs/faaram-silver-monarch.html').read_text(encoding='utf-8')
        self.assertEqual(set(re.findall(r'data-ability="([^"]+)"', page)), {
            'Unbroken Continuity', 'Sovereign of the Bound', 'Soul Dominion',
            'Thousand-Year Echo', 'Severance', 'Black Star', 'Soul Imprint',
            'Servant Art — Sovereign Form', 'Borrowed Throne', 'Soulforge',
            'Unbroken Soul', 'Bound Resonance',
        })
        for constraint in ('Who Never Died.', 'Estimated Power Level', '10,000+',
                           'Universe 2', 'Never complete immunity',
                           'does not read thoughts', 'does not copy techniques',
                           'Restoration is not instantaneous', 'several successful applications',
                           'Faaram’s own stats, resources and Magical Power'):
            self.assertIn(constraint, page)

    def test_only_restricted_directory_shelf_contains_him(self):
        index = (ROOT / 'npcs/index.html').read_text(encoding='utf-8')
        href = '/aevum-archive/npcs/faaram-silver-monarch.html'
        self.assertEqual(index.count(href), 1)
        restricted = index.split('id="contained-records"')[1].split('</section>')[0]
        self.assertIn(href, restricted)
        self.assertIn('npcs/bobby.html', restricted)
        for player_list in ('characters/all.html', 'characters/index.html'):
            self.assertNotIn(href, (ROOT / player_list).read_text(encoding='utf-8'))
        current = (ROOT / 'characters/faaram.html').read_text(encoding='utf-8')
        self.assertIn(href, current)
        self.assertIn('resides in Universe 2', current)

    def test_motion_does_not_gate_content_and_can_pause(self):
        script = (ROOT / 'assets/silver-monarch.js').read_text(encoding='utf-8')
        style = (ROOT / 'assets/silver-monarch.css').read_text(encoding='utf-8')
        self.assertIn('IntersectionObserver', script)
        self.assertIn('!document.hidden', script)
        self.assertIn('prefers-reduced-motion:reduce', style)
        self.assertIn('animation-play-state:paused', style)
        self.assertNotIn('scrollIntoView', script)
        self.assertNotIn('innerHTML', script)
