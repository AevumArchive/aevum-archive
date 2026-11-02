"""A visual renewal cannot drop public records, artwork, navigation or sealed boundaries."""
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / 'tests/fixtures/archive_renewal_content.json').read_text(encoding='utf-8'))


def plain(source):
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', source)).split())


class Parsed(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.fragments, self.links, self.images = [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
            if attrs['href'].startswith('#'):
                self.fragments.append(attrs['href'][1:])
        if tag == 'img':
            self.images.append(attrs['src'])


class ArchiveRenewalTest(unittest.TestCase):
    def test_every_existing_public_text_block_survives(self):
        for name, baseline in BASELINE.items():
            with self.subTest(page=name):
                source = (ROOT / name).read_text(encoding='utf-8')
                main = re.search(r'<main\b[\s\S]*?</main>', source).group()
                facts = Counter(hashlib.sha256(plain(m[1]).encode()).hexdigest()
                                for m in re.findall(r'<(p|h[1-4]|li|dt|dd)\b[^>]*>([\s\S]*?)</\1>', main))
                self.assertFalse(Counter(baseline['facts']) - facts, 'Existing narrative or system text disappeared')

    def test_old_destinations_artwork_ids_and_new_chapters_remain_valid(self):
        for name, baseline in BASELINE.items():
            with self.subTest(page=name):
                source = (ROOT / name).read_text(encoding='utf-8')
                parsed = Parsed()
                parsed.feed(source)
                self.assertTrue(set(baseline['links']).issubset(parsed.links))
                self.assertTrue(set(baseline['images']).issubset(parsed.images))
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                self.assertTrue(set(parsed.fragments).issubset(parsed.ids))
                self.assertNotIn('\ufffd', source)
                self.assertIn('archive-wings.css?v=20261102-folio1', source)

    def test_codex_navigation_exists_before_javascript_and_includes_every_shelf(self):
        codex = [name for name, info in BASELINE.items() if info['kind'] == 'codex']
        self.assertEqual(len(codex), 10)
        for name in codex:
            with self.subTest(page=name):
                source = (ROOT / name).read_text(encoding='utf-8')
                nav = re.search(r'<nav class="codex-section-nav"[\s\S]*?</nav>', source).group()
                self.assertEqual(nav.count('aria-current="page"'), 1)
                self.assertEqual(nav.count('<a '), 10)
                self.assertIn('/codex/bindings.html', nav)
                self.assertIn('/codex/chapter-bosses.html', nav)
                self.assertIn('codex-grimoire.css?v=20261102-renewal1', source)
        for name in ('races', 'traits'):
            self.assertIn('assets/codex.js', (ROOT / 'codex' / (name + '.html')).read_text(encoding='utf-8'))

    def test_world_countdown_does_not_decide_canon_or_gateway_state(self):
        source = (ROOT / 'world-events/index.html').read_text(encoding='utf-8')
        self.assertIn("new Date('2026-10-31T06:41:24Z')", source)
        self.assertIn('Marked hour reached', source)
        self.assertIn('role="timer" aria-live="off"', source)
        self.assertNotIn('Loading...', source)
        for fact in ('<dt>Status</dt><dd>ACTIVE</dd>', '<dt>Gateway status</dt><dd>OPEN</dd>',
                     '<dt>Opening sequence</dt><dd>COMPLETE</dd>',
                     '<dt>Timer target</dt><dd>2026-10-31 08:41:24 realm time</dd>'):
            self.assertIn(fact, source)
        self.assertNotIn('<dt>Status</dt><dd>COMPLETED</dd>', source)

    def test_mythic_and_ancient_get_distinct_motion_with_accessible_fallbacks(self):
        css = (ROOT / 'assets/achievement-gallery.css').read_text(encoding='utf-8')
        self.assertIn('.rarity-tier[data-tier="mythic"]::after', css)
        self.assertIn('.rarity-tier[data-tier="ancient"]::after', css)
        self.assertIn('mythic-tier-glow 8s', css)
        self.assertIn('wing-orbit 60s', css)
        common = (ROOT / 'assets/archive-wings.css').read_text(encoding='utf-8')
        self.assertIn('prefers-reduced-motion: reduce', common)
        self.assertIn('animation: none !important', common)
        for filename in ('archive-folio', 'world-anchor', 'codex-grimoire'):
            css = (ROOT / 'assets' / (filename + '.css')).read_text(encoding='utf-8')
            self.assertNotRegex(css, r'url\([^)]*\.(?:png|webp|jpg)')
