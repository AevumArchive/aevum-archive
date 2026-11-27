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
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.shelves.append(attrs['href'][1:])


class NpcDirectoryTest(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / 'npcs/index.html').read_text(encoding='utf-8')
        self.parsed = DirectoryParser()
        self.parsed.feed(self.page)

    def test_all_entries_remain_public_without_script_and_have_no_portrait_elements(self):
        self.assertEqual(len(self.parsed.cards), 54)
        for tag, attrs in self.parsed.cards:
            self.assertNotIn('hidden', attrs)
            self.assertNotIn('style', attrs)
            if tag == 'a':
                self.assertTrue((ROOT / attrs['href'].removeprefix('/aevum-archive/')).is_file())
        self.assertEqual(self.parsed.images, ['/aevum-archive/assets/archive-mark.svg'])
        self.assertNotIn('assets/images/', self.page)
        self.assertNotIn('Enski', self.page)
        self.assertNotIn('Tenrei', self.page)

    def test_distinguished_cards_keep_two_artwork_exceptions(self):
        for special in ('npc-feature-lilith', 'npc-feature-veyr', 'npc-feature-izumi',
                        'npc-feature-bomir', 'npc-feature-peter', 'npc-feature-kaede', 'npc-feature-death'):
            self.assertEqual(sum(special in attrs['class'].split() for _, attrs in self.parsed.cards), 1)
        old_styles = (ROOT / 'assets/npc-index.css').read_text(encoding='utf-8')
        self.assertEqual(set(re.findall(r'assets/images/([^"\)]+)', old_styles)), {'lilith.png', 'veyr.png'})
        for color in ('rgba(109, 222, 145, .18)', 'rgba(231, 189, 89, .2)', 'rgba(132, 25, 38, .22)'):
            self.assertIn(color, old_styles)
        new_styles = (ROOT / 'assets/npc-directory.css').read_text(encoding='utf-8')
        self.assertNotIn('url(', new_styles)

    def test_shelves_and_count_are_consistent(self):
        expected = ['all-npcs', 'current-npcs', 'sovereigns', 'divine-alliance', 'servants',
                    'tengoku-clan', 'known-figures', 'contained-records', 'silver-monarch']
        self.assertEqual(self.parsed.shelves, expected)
        for shelf in expected:
            self.assertIn(shelf, self.parsed.ids)
            self.assertIn(f'href="#{shelf}"', self.page)
        self.assertEqual(len(self.parsed.ids), len(set(self.parsed.ids)))
        self.assertIn('<strong>Known Figures</strong><small>12 records</small>', self.page)
        self.assertIn('<strong>All NPCs</strong><small>8 shelves</small>', self.page)
        self.assertRegex(self.page, r'<strong>51</strong>\s*<span>NPCs discovered</span>')
        major_shelf = self.page.split('id="sovereigns"', 1)[1].split('</section>', 1)[0]
        kaede = 'href="/aevum-archive/npcs/kaede.html"'
        self.assertNotIn(kaede, major_shelf)
        self.assertIn('<strong>Major Presences</strong><small>3 records</small>', self.page)
        self.assertIn('<span class="npc-count">03 major records</span>', major_shelf)
        death = 'href="/aevum-archive/npcs/death.html"'
        self.assertIn(death, major_shelf)
        self.assertEqual(self.page.count(death), 1)
        self.assertIn('<strong>Restricted</strong><small>6 records</small>', self.page)
        restricted = self.page.split('id="contained-records"', 1)[1].split('</section>', 1)[0]
        self.assertIn(kaede, restricted)
        self.assertEqual(self.page.count(kaede), 1)
        faceless = 'href="/aevum-archive/npcs/the-faceless.html"'
        self.assertIn(faceless, restricted)
        self.assertEqual(self.page.count(faceless), 1)
        self.assertIn("An entity that possessed the earlier Faaram", restricted)
        self.assertNotIn('broken loyalty', self.page)

    def test_tengoku_has_all_six_profiles_once_in_its_own_shelf(self):
        clan_section = self.page.split('id="tengoku-clan"', 1)[1].split('</section>', 1)[0]
        clan = DirectoryParser()
        clan.feed(clan_section)
        self.assertEqual(len(clan.cards), 6)
        self.assertFalse(clan.images)
        for name, slug in [('zenith', 'zenith-kurogane'), ('kiyoko', 'kiyoko-kurogane'),
                           ('asakura', 'asakura-kurogane'), ('kenka', 'kenka'), ('kenji', 'kenji'), ('daiki', 'daiki')]:
            href = f'/aevum-archive/npcs/{slug}.html'
            self.assertEqual(sum(attrs.get('href') == href for _, attrs in self.parsed.cards), 1)
            self.assertTrue(any(attrs.get('href') == href and f'tengoku-card--{name}' in attrs['class'].split()
                                for _, attrs in clan.cards))

    def test_death_has_a_symbolic_dossier_and_historical_links(self):
        dossier = (ROOT / 'npcs/death.html').read_text(encoding='utf-8')
        parsed = DirectoryParser()
        parsed.feed(dossier)
        self.assertEqual(parsed.images, ['/aevum-archive/assets/archive-mark.svg'])
        self.assertEqual(len(set(parsed.ids)), len(parsed.ids))
        self.assertTrue(set(parsed.shelves).issubset(parsed.ids))
        self.assertIn('<dt>Power Level</dt><dd>Unknown</dd>', dossier)
        self.assertIn('<svg class="death-clock"', dossier)
        for role, path in [('Former Student', 'characters/obama.html'),
                           ('Historical Connection', 'npcs/peter.html')]:
            self.assertRegex(dossier, rf'href="/aevum-archive/{re.escape(path)}">\s*<small>{role}</small>')
            related = (ROOT / path).read_text(encoding='utf-8')
            self.assertIn('href="/aevum-archive/npcs/death.html#threads-of-fate"', related)
        bonds = (ROOT / 'characters/bonds.html').read_text(encoding='utf-8')
        self.assertIn('class="tree-node death-bond" href="/aevum-archive/npcs/death.html"', bonds)

    def test_servants_are_grouped_under_their_existing_affiliations(self):
        shelf = self.page.split('id="servants"', 1)[1].split('</section>', 1)[0]
        groups = re.findall(r'data-npc-affiliation="([^"]+)">(.*?)(?=class="npc-ledger-group|$)', shelf, re.S)
        expected = [
            ('Faaram', ['uwu', 'jiro', 'ichiro', 'keanu', 'timeo', 'arisu']),
            ('Faaram', ['nox', 'nyx', 'rapax', 'poison', 'yori', 'kimiko']),
            ('OBAMA', ['peter', 'hans', 'fritz']),
        ]
        self.assertEqual([(affiliation, re.findall(r'/npcs/([^"]+)\.html"', group))
                          for affiliation, group in groups], expected)

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
