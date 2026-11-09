"""New archive leaves keep public records, ownership and sealed boundaries intact."""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / 'tests/fixtures/archive_wings_content.json').read_text(encoding='utf-8'))


def plain(source):
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', source)).split())


class WingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.fragments, self.links, self.images = [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            target = attrs.get('href', '')
            self.links.append(target)
            if target.startswith('#'):
                self.fragments.append(target[1:])
        if tag == 'img':
            self.images.append(attrs['src'])


class ArchiveWingsTest(unittest.TestCase):
    def test_existing_record_contents_and_destinations_are_preserved(self):
        for name, baseline in BASELINE.items():
            with self.subTest(page=name):
                source = (ROOT / name / 'index.html').read_text(encoding='utf-8')
                if name == 'achievements':
                    records = re.findall(r'<article\b[^>]*>[\s\S]*?</article>', source)
                    self.assertEqual(len(records), 52)  # 25 earned, 3 explanatory notes, 24 locked.
                    hashes = {hashlib.sha256(plain(record).encode()).hexdigest() for record in records}
                    self.assertTrue(set(baseline['records']).issubset(hashes))
                else:
                    # Decorative diagrams may change; record text and individual destinations may not.
                    records = re.findall(r'<a class="event-(?:feature[ "][^>]*|ledger-row[^>]*)>[\s\S]*?</a>', source)
                    self.assertEqual(len(records), 9)
                    facts = [plain(match[1]) for record in records
                             for match in re.findall(r'<(h3|p|small|strong|em)\b[^>]*>([\s\S]*?)</\1>', record)]
                    self.assertEqual(facts, baseline['facts'])
                parsed = WingParser()
                parsed.feed(source)
                self.assertTrue(set(baseline['links']).issubset(parsed.links))

    def test_navigation_is_open_and_all_chapters_resolve(self):
        for name in ('events', 'achievements'):
            with self.subTest(page=name):
                source = (ROOT / name / 'index.html').read_text(encoding='utf-8')
                parsed = WingParser()
                parsed.feed(source)
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                self.assertTrue(set(parsed.fragments).issubset(parsed.ids))
                self.assertNotRegex(source, r'<section[^>]*\shidden(?:[=\s>])')
                self.assertIn('archive-wings.css?v=20261102-folio1', source)
                for old in ('frame-overrides.css', 'ornament-v3.css', 'round4-assets.css', 'events-page.css'):
                    self.assertNotIn(old, source)
                self.assertIn('aria-hidden="true"', source)
        events = (ROOT / 'events/index.html').read_text(encoding='utf-8')
        self.assertEqual(len(re.findall('class="event-backlog-era"', events)), 3)

    def test_only_existing_chain_art_and_branding_are_preview_images(self):
        for name in ('events', 'achievements'):
            source = (ROOT / name / 'index.html').read_text(encoding='utf-8')
            parsed = WingParser()
            parsed.feed(source)
            allowed = {'/aevum-archive/assets/archive-mark.svg'}
            if name == 'achievements':
                allowed.add('/aevum-archive/assets/ui/achievements/locked-achievement-chain-overlay.png')
                self.assertEqual(source.count('class="locked-achievement-chain-overlay"'), 24)
            self.assertTrue(set(parsed.images).issubset(allowed))
        for filename in ('archive-wings.css', 'event-chronicle.css', 'achievement-gallery.css'):
            css = (ROOT / 'assets' / filename).read_text(encoding='utf-8')
            self.assertNotRegex(css, r'url\([^)]*\.(?:png|webp|jpg)')

    def test_rarity_order_and_top_achievement_are_preserved(self):
        source = (ROOT / 'achievements/index.html').read_text(encoding='utf-8')
        ladder = re.findall(r'<span class="rarity-tier" data-tier="([^"]+)">([^<]+)</span>', source)
        self.assertEqual([item[1] for item in ladder], [
            'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Mythic', 'Ancient', 'Divine', 'Transcendent'])
        self.assertEqual(source.count('data-rarity="transcendent"'), 1)
        self.assertIn('id="the-one-who-refused-the-end"', source)
        self.assertIn('id="a-name-unknown-until-now"', source)
        self.assertIn('overlord-completion.css?v=20261023-finale1', source)
        self.assertIn('astera-lore.css?v=20261006-2', source)
        self.assertIn('achievement-lock-overlay.css?v=20260829-crosschain1', source)

    def test_animation_and_accessibility_stay_index_scoped(self):
        common = (ROOT / 'assets/archive-wings.css').read_text(encoding='utf-8')
        earned = (ROOT / 'assets/achievement-gallery.css').read_text(encoding='utf-8')
        for rule in ('body.grimoire-wing', ':focus-visible', 'prefers-reduced-motion: reduce',
                     'animation: none !important', 'pointer-events: none'):
            self.assertIn(rule, common)
        self.assertIn('animation: wing-orbit 150s linear infinite', common)
        self.assertIn('.route-achievements .transcendent-achievement', earned)
        self.assertIn('.route-achievements .overlord-trophy .trophy-seal::before', earned)
        self.assertNotIn('route-characters-faaram', earned)
