"""NPC discovery preserves distinguished cards and keeps portraits inside dossiers."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DirectoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards, self.images, self.shelves, self.ids = [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if 'npc-card' in attrs.get('class', '').split():
            self.cards.append((tag, attrs))
        if tag == 'img':
            self.images.append(attrs['src'])
        if tag == 'option':
            self.shelves.append(attrs.get('value'))


class NpcDirectoryTest(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / 'npcs/index.html').read_text(encoding='utf-8')
        self.parsed = DirectoryParser()
        self.parsed.feed(self.page)

    def test_all_entries_remain_public_without_script_and_have_no_portrait_elements(self):
        self.assertEqual(len(self.parsed.cards), 46)
        for tag, attrs in self.parsed.cards:
            self.assertNotIn('hidden', attrs)
            self.assertNotIn('style', attrs)
            if tag == 'a':
                self.assertTrue((ROOT / attrs['href'].removeprefix('/aevum-archive/')).is_file())
        self.assertEqual(self.parsed.images, ['/aevum-archive/assets/archive-mark.svg'])
        self.assertNotIn('assets/images/', self.page)
        self.assertNotIn('Enski', self.page)
        self.assertNotIn('Tenrei', self.page)

    def test_exactly_five_distinguished_cards_and_two_artwork_exceptions(self):
        for special in ('npc-feature-lilith', 'npc-feature-veyr', 'npc-feature-izumi',
                        'npc-feature-bomir', 'npc-feature-peter'):
            self.assertEqual(sum(special in attrs['class'].split() for _, attrs in self.parsed.cards), 1)
        old_styles = (ROOT / 'assets/npc-index.css').read_text(encoding='utf-8')
        self.assertEqual(set(re.findall(r'assets/images/([^"\)]+)', old_styles)), {'lilith.png', 'veyr.png'})
        for color in ('rgba(109, 222, 145, .18)', 'rgba(231, 189, 89, .2)', 'rgba(132, 25, 38, .22)'):
            self.assertIn(color, old_styles)
        new_styles = (ROOT / 'assets/npc-directory.css').read_text(encoding='utf-8')
        self.assertNotIn('url(', new_styles)

    def test_shelves_and_count_are_consistent(self):
        expected = ['all', 'current-npcs', 'sovereigns', 'divine-alliance', 'servants', 'known-figures', 'contained-records']
        self.assertEqual(self.parsed.shelves, expected)
        for shelf in expected[1:]:
            self.assertIn(shelf, self.parsed.ids)
            self.assertIn(f'href="#{shelf}"', self.page)
        self.assertEqual(len(self.parsed.ids), len(set(self.parsed.ids)))
        self.assertIn('14 recovered records', self.page)
        self.assertIn('46 entries across six shelves', self.page)
        self.assertNotIn('broken loyalty', self.page)

    def test_search_is_local_accessible_and_enhancement_only(self):
        self.assertIn('role="search"', self.page)
        self.assertIn('aria-live="polite"', self.page)
        self.assertIn('data-npc-tools role="search" aria-label="Search NPC records" hidden', self.page)
        script = (ROOT / 'assets/npc-directory.js').read_text(encoding='utf-8')
        self.assertIn("text.normalize('NFKD')", script)
        self.assertNotIn('fetch(', script)
        self.assertNotIn('createElement', script)
        self.assertNotIn('innerHTML', script)
        styles = (ROOT / 'assets/npc-directory.css').read_text(encoding='utf-8')
        self.assertIn('.npc-directory [hidden] { display: none !important; }', styles)
        self.assertIn('prefers-reduced-motion: reduce', styles)
        self.assertIn(':focus-visible', styles)
