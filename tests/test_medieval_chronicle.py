"""The current campaign is a readable, portrait-free chronicle of existing public lore."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ChronicleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.fragments, self.images, self.links, self.records = [], [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'img':
            self.images.append(attrs['src'])
        if tag == 'a':
            target = attrs.get('href', '')
            self.links.append(target)
            if target.startswith('#'):
                self.fragments.append(target[1:])
            if any(c in attrs.get('class', '').split() for c in ('campaign-person', 'campaign-contact', 'campaign-location', 'campaign-thread')):
                self.records.append(attrs)


class MedievalChronicleTest(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / 'playthroughs/fantasy-medieval.html').read_text(encoding='utf-8')
        self.parsed = ChronicleParser()
        self.parsed.feed(self.page)

    def test_chapters_and_existing_destinations_survive(self):
        self.assertEqual(len(self.parsed.ids), len(set(self.parsed.ids)))
        self.assertTrue(set(self.parsed.fragments).issubset(set(self.parsed.ids)))
        for chapter in ('status', 'characters', 'npcs', 'geography', 'threads'):
            self.assertIn('campaign-' + chapter, self.parsed.ids)
            self.assertIn('campaign-' + chapter, self.parsed.fragments)
        for route in ('characters/', 'lore/locations/crownbridge-front.html', 'lore/history/timeline.html',
                      'characters/astera-zenith.html', 'characters/jango.html', 'characters/lythariel.html',
                      'characters/william-carter.html', 'npcs/raoul.html', 'npcs/arnold.html', 'npcs/mira.html',
                      'lore/kingdoms/avalon.html', 'lore/settlements/neris.html', 'lore/noble-houses/house-zenith.html',
                      'world-events/', 'events/the-silent-fault.html', 'characters/faaram.html',
                      'lore/cosmology/the-umbral-meridian.html', 'updates/'):
            self.assertIn('/aevum-archive/' + route, self.parsed.links)

    def test_records_remain_open_without_portrait_previews(self):
        self.assertEqual(len(self.parsed.records), 19)  # 4 characters, 3 NPCs, 4 places, 8 threads.
        self.assertEqual(self.parsed.images, ['/aevum-archive/assets/archive-mark.svg'])
        self.assertNotIn('assets/images/', self.page)
        self.assertNotRegex(self.page, r'<[^>]+\shidden(?:[=\s>])')
        self.assertIn('class="chronicle-crest"', self.page)
        self.assertIn('aria-hidden="true"', self.page)
        self.assertNotIn('/characters/obama.html', self.page)
        self.assertNotIn('/characters/guts.html', self.page)

    def test_campaign_states_and_uncertain_outcomes_are_unchanged(self):
        for fact in ('ACTIVE', 'Post-Convergence', 'Avalon–Rath War',
                     'Rath initiated the conflict at Ardent Gate; Avalon answered in defense.',
                     'Lost / Unknown after Faaram’s soul extraction', 'whose present fate remains unknown',
                     'World Anchor — Part I is accessible', 'refusing every offensive use of her craft',
                     'Second Sight stabilized', 'Faaram’s Mark on her soul has been destroyed.',
                     'The soul incident and Astera’s fate remain unresolved.', 'Maps remain the visual authority'):
            self.assertIn(fact, self.page)
        self.assertIn('visibility-state partial">Partial</span><h3>Silent Fault', self.page)
        self.assertIn('visibility-state">Complete</span><h3>The Umbral Meridian · Beyond the Mark', self.page)

    def test_design_is_scoped_and_accessible(self):
        css = (ROOT / 'assets/medieval-chronicle.css').read_text(encoding='utf-8')
        for rule in ('body.route-playthrough-fantasy-medieval', ':focus-visible', 'prefers-reduced-motion: reduce', 'pointer-events: none'):
            self.assertIn(rule, css)
        self.assertEqual(re.findall(r'url\("([^"]+)"\)', css), ['/aevum-archive/assets/fonts/cinzel/Cinzel-Variable.ttf'])
        self.assertIn('medieval-chronicle.css?v=20261031-chronicle1', self.page)
        for old in ('frame-overrides.css', 'ornament-v3.css', 'round4-assets.css'):
            self.assertNotIn(old, self.page)
