"""Historical campaign folios preserve public facts, destinations and open access."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / 'tests/fixtures/recovered_era_content.json').read_text(encoding='utf-8'))


class EraParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.fragments, self.images, self.links = [], [], [], []

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


class EraChroniclesTest(unittest.TestCase):
    def test_all_detail_pages_share_the_reference_folio(self):
        details = set(p.name for p in (ROOT / 'playthroughs').glob('*.html')) - {'index.html'}
        self.assertEqual(details, set(BASELINE) | {'fantasy-medieval.html'})
        for name in BASELINE:
            with self.subTest(page=name):
                source = (ROOT / 'playthroughs' / name).read_text(encoding='utf-8')
                for component in ('playthrough-chronicle', 'medieval-chronicle', 'chronicle-breadcrumb',
                                  'chronicle-hero', 'chronicle-cover', 'chronicle-nav', 'chronicle-return'):
                    self.assertIn(component, source)
                self.assertIn('medieval-chronicle.css?v=20261102-eras1', source)
                for obsolete in ('frame-overrides.css', 'ornament-v3.css', 'round4-assets.css'):
                    self.assertNotIn(obsolete, source)

    def test_public_history_and_record_links_survive(self):
        for name, snapshot in BASELINE.items():
            with self.subTest(page=name):
                source = (ROOT / 'playthroughs' / name).read_text(encoding='utf-8')
                facts = [re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', ' ', m[1])).strip()
                         for m in re.findall(r'<(p|li|dt|dd|h2|h3)\b[^>]*>([\s\S]*?)</\1>', source)]
                # Every pre-existing story heading, paragraph, list item and definition stays in order.
                position = 0
                for fact in snapshot['facts']:
                    self.assertIn(fact, facts[position:])
                    position = facts.index(fact, position) + 1
                parsed = EraParser()
                parsed.feed(source)
                self.assertTrue(set(snapshot['links']).issubset(parsed.links))

    def test_chapters_resolve_and_no_portrait_previews_are_added(self):
        for name in BASELINE:
            with self.subTest(page=name):
                source = (ROOT / 'playthroughs' / name).read_text(encoding='utf-8')
                parsed = EraParser()
                parsed.feed(source)
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                self.assertTrue(set(parsed.fragments).issubset(parsed.ids))
                self.assertIn('era-status', parsed.fragments)
                self.assertEqual(parsed.images, ['/aevum-archive/assets/archive-mark.svg'])
                self.assertNotIn('assets/images/', source)
                self.assertNotRegex(source, r'<[^>]+\shidden(?:[=\s>])')
                self.assertIn('class="chronicle-crest"', source)

    def test_unknown_outcomes_stay_unknown(self):
        vault = (ROOT / 'playthroughs/vault-8.html').read_text(encoding='utf-8')
        temmie = (ROOT / 'playthroughs/temmie-town.html').read_text(encoding='utf-8')
        aizen = (ROOT / 'playthroughs/aizen-ended-road.html').read_text(encoding='utf-8')
        alterra = (ROOT / 'playthroughs/alterra-origin.html').read_text(encoding='utf-8')
        for fact in ('without producing one final canonical ending', 'possible, but no longer guaranteed',
                     'Finding it remains extraordinarily unlikely'):
            self.assertIn(fact, vault)
        self.assertIn('not literally indestructible', temmie)
        self.assertIn('theoretically possible rather than promised', temmie)
        self.assertIn('Pre-Fusion Continuity, not the current multiverse', aizen)
        self.assertIn('not an unquestionable historical timestamp', alterra)
        self.assertIn('does not identify the force within the Vault', alterra)

    def test_shared_styles_remain_scoped_and_motion_accessible(self):
        shared = (ROOT / 'assets/medieval-chronicle.css').read_text(encoding='utf-8')
        historical = (ROOT / 'assets/era-chronicles.css').read_text(encoding='utf-8')
        self.assertIn(':is(body.route-playthrough-fantasy-medieval, body.playthrough-chronicle)', shared)
        self.assertIn('prefers-reduced-motion: reduce', shared)
        self.assertIn(':focus-visible', shared)
        self.assertIn('pointer-events: none', shared)
        self.assertNotIn('url(', historical)
        for name in ('vault', 'temmie', 'aizen'):
            self.assertIn('era-' + name, historical)
