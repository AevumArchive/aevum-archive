"""The shared character dossier must change presentation without rewriting a life."""
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / 'tests/fixtures/character_dossier_content.json').read_text(encoding='utf-8'))


def plain(source):
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', source)).split())


class Dossier(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images, self.fragments = [], [], [], []

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


class CharacterDossiersTest(unittest.TestCase):
    def test_every_existing_story_and_fact_survives(self):
        for name, baseline in BASELINE.items():
            with self.subTest(page=name):
                source = (ROOT / name).read_text(encoding='utf-8')
                main = re.search(r'<main\b[\s\S]*?</main>', source).group()
                facts = Counter(hashlib.sha256(plain(m[1]).encode()).hexdigest()
                                for m in re.findall(r'<(p|h[1-4]|li|dt|dd)\b[^>]*>([\s\S]*?)</\1>', main))
                self.assertFalse(Counter(baseline['facts']) - facts)
                parsed = Dossier()
                parsed.feed(source)
                self.assertTrue(set(baseline['links']).issubset(parsed.links))
                self.assertTrue(set(baseline['images']).issubset(parsed.images))
                self.assertTrue(set(baseline['ids']).issubset(parsed.ids))
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                self.assertTrue(set(parsed.fragments).issubset(parsed.ids))
                self.assertNotIn('\ufffd', source)

    def test_all_regular_profiles_join_the_dossier_and_unknown_power_is_not_invented(self):
        profiles = set(p.as_posix() for p in (ROOT / 'characters').glob('*.html'))
        expected = {str(ROOT / name).replace('\\', '/') for name in BASELINE}
        excluded = {
            (ROOT / 'characters' / name).as_posix()
            for name in (
                'all.html', 'index.html', 'bonds.html', 'faaram.html', 'faaram-tempest-origin.html', 'kazz.html',
                'miles.html', 'josef.html', 'johann.html', 'jackson.html',
                'thomas-meyer.html', 'jon-snow.html', 'solaire.html', 'tony-arasaka.html',
                'guts-retired.html',
            )
        }
        self.assertEqual(profiles, expected | excluded)
        for name in BASELINE:
            source = (ROOT / name).read_text(encoding='utf-8')
            self.assertIn('character-dossiers.css?v=20261102-dossiers1', source)
            self.assertIn('character-dossier-main', source)
            if name.endswith('astera-zenith.html'):
                self.assertNotIn('Recorded Power Level', source)
                continue
            hero = re.search(r'<section class="record-hero"[\s\S]*?</section>', source).group()
            known_power = '<dt>Power Level</dt>' in hero
            self.assertEqual('Recorded Power Level' in hero, known_power)

    def test_existing_art_is_used_once_and_missing_art_remains_a_sigil(self):
        for name, baseline in BASELINE.items():
            if 'hero_art' not in baseline:
                continue  # Astera retains her original portrait and discovery illustrations.
            with self.subTest(page=name):
                source = (ROOT / name).read_text(encoding='utf-8')
                hero = re.search(r'<section class="record-hero"[\s\S]*?</section>', source).group()
                if baseline['hero_art']:
                    self.assertEqual(source.count('src="' + baseline['hero_art'] + '"'), 1)
                    self.assertIn('class="dossier-portrait"', hero)
                    self.assertNotIn('dossier-symbol', hero)
                else:
                    self.assertIn('class="dossier-portrait dossier-seal"', hero)
                    self.assertNotIn('<img ', hero)
                self.assertNotIn('When the portrait is ready', source)

    def test_special_exhibits_keep_their_original_markup_and_scripts(self):
        obama = (ROOT / 'characters/obama.html').read_text(encoding='utf-8')
        astera = (ROOT / 'characters/astera-zenith.html').read_text(encoding='utf-8')
        for value in ('id="imposed-reality"', 'class="unique-trait-card"', 'class="trait-future"',
                      '<progress value="0" max="100">', 'willy-watcher.js'):
            self.assertIn(value, obama)
        for value in ('class="divine-discovery-card"', 'astera-quest-completion', 'soul-mark-ring',
                      'id="duality"', 'astera-dossier.css?v=20261113-peak'):
            self.assertIn(value, astera)
        faaram = (ROOT / 'characters/faaram.html').read_text(encoding='utf-8')
        self.assertIn('class="tempest-hero"', faaram)
        self.assertNotIn('character-dossiers.css', faaram)

    def test_colors_motion_and_uncropped_art_have_scoped_styles(self):
        css = (ROOT / 'assets/character-dossiers.css').read_text(encoding='utf-8')
        for value in ('body.character-dossier', 'prefers-reduced-motion: reduce', 'animation: none !important',
                      ':focus-visible', 'align-self: start', 'width: 100%; height: auto',
                      'dossier-orbit 85s linear infinite'):
            self.assertIn(value, css)
        for name in BASELINE:
            slug = Path(name).stem
            self.assertIn('body.character-dossier.route-characters-' + slug, css)
