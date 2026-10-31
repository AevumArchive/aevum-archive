"""The welcoming homepage preserves archive routes/canon and avoids portrait previews."""
from html.parser import HTMLParser
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AtriumParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.links, self.ids, self.fragments = [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            self.images.append(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            target = attrs.get('href', '')
            self.links.append(target)
            if target.startswith('#'):
                self.fragments.append(target[1:])


class HomeAtriumTest(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / 'index.html').read_text(encoding='utf-8')
        self.parsed = AtriumParser()
        self.parsed.feed(self.page)

    def test_one_new_atmospheric_image_replaces_the_old_tile_gallery(self):
        self.assertEqual([image['src'] for image in self.parsed.images], [
            '/aevum-archive/assets/home-v2/home-archive-sigil.webp',
            '/aevum-archive/assets/images/archive-threshold.png'])
        self.assertEqual(self.parsed.images[1]['alt'], '')
        self.assertEqual(self.parsed.images[1]['fetchpriority'], 'high')
        self.assertEqual(self.parsed.images[1]['width'], '1672')
        self.assertEqual(self.parsed.images[1]['height'], '941')
        data = (ROOT / 'assets/images/archive-threshold.png').read_bytes()
        self.assertEqual(struct.unpack('>II', data[16:24]), (1672, 941))
        for old in ('home-hero-archive-realm', 'home-current-playthrough', 'home-card-', 'home-v2.css', 'landing-polish.css'):
            self.assertNotIn(old, self.page)

    def test_all_existing_destinations_and_newcomer_guide_are_accessible(self):
        for route in ('playthroughs/#current', 'characters/', 'characters/all.html', 'codex/', 'npcs/',
                      'achievements/', 'lore/', 'leaderboard/', 'world-events/', 'world-items/',
                      'sealed-records/', 'downloads/texture-pack.html', 'events/', 'updates/', 'codex/handbook.html'):
            self.assertIn('/aevum-archive/' + route, self.parsed.links)
        self.assertEqual(len(re.findall(r'class="atrium-wing"', self.page)), 6)
        self.assertEqual(len(self.parsed.ids), len(set(self.parsed.ids)))
        self.assertTrue(set(self.parsed.fragments).issubset(set(self.parsed.ids)))
        self.assertNotRegex(self.page, r'<[^>]+\shidden(?:[=\s>])')
        self.assertIn('New to Aevum?', self.page)

    def test_current_facts_and_ledger_records_survive(self):
        for fact in ('data-archive-player-count>4,981<', 'Avalon', 'Neris', 'First Roads.',
                     'Ichiro — Awake at 3300 PL', 'The One Who Refused the End', 'They never chose to leave',
                     '2500 PL', '26 Soul Deaths escaped', 'Jiro’s last recorded injuries remain unresolved',
                     'Poison’s fate is unconfirmed'):
            self.assertIn(fact, self.page)
        self.assertIn('archive-sync.js', self.page)
        self.assertIn('halloween.js?v=20261030-allhallows1', self.page)

    def test_decorations_are_scoped_nonblocking_and_motion_optional(self):
        styles = (ROOT / 'assets/home-atrium.css').read_text(encoding='utf-8')
        self.assertIn('body.route-home', styles)
        self.assertIn('prefers-reduced-motion: reduce', styles)
        self.assertIn('pointer-events: none', styles)
        self.assertIn(':focus-visible', styles)
        self.assertNotIn('url(', styles)  # The one artwork is a semantic, preloaded HTML image.
