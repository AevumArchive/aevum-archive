"""Every archive route gets the same optional, date-gated seasonal costume."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HeadAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.assets = []

    def handle_starttag(self, tag, attrs):
        if tag == 'head':
            self.in_head = True
        values = dict(attrs)
        target = values.get('src', values.get('href', ''))
        if 'assets/halloween.' in target:
            self.assets.append((tag, target, self.in_head, 'defer' in values))

    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False


class HalloweenTest(unittest.TestCase):
    def test_every_page_loads_the_same_theme_before_paint(self):
        pages = list(ROOT.rglob('*.html'))
        self.assertGreaterEqual(len(pages), 123)
        for page in pages:
            with self.subTest(page=page.relative_to(ROOT)):
                parsed = HeadAssets()
                parsed.feed(page.read_text(encoding='utf-8'))
                self.assertEqual(parsed.assets, [
                    ('link', '/aevum-archive/assets/halloween.css?v=20261030-allhallows1', True, False),
                    ('script', '/aevum-archive/assets/halloween.js?v=20261030-allhallows1', True, False)])

    def test_motion_and_print_have_explicit_opt_outs(self):
        css = (ROOT / 'assets/halloween.css').read_text(encoding='utf-8')
        for rule in ('prefers-reduced-motion: reduce', '@media print', '.halloween-quiet', 'pointer-events: none'):
            self.assertIn(rule, css)
        # No global palette replacement that could recolor special NPC/status cards.
        for variable in ('--green:', '--gold:', '--text:', '--pink:'):
            self.assertNotIn(variable, css)
