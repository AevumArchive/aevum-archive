"""Ichiro is free; the earlier Soul Seal remains a closed historical card."""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DossierParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.anchors = []
        self.images = []
        self.styles = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.anchors.append(attrs["href"][1:])
        if tag == "img":
            self.images.append(attrs)
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.styles.append(attrs["href"].split("?")[0])


class IchiroDossierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detail = (ROOT / "npcs/ichiro.html").read_text(encoding="utf-8")
        cls.text = " ".join(unescape(re.sub(r"<[^>]+>", " ", cls.detail)).split())

    def test_hero_records_liberation_without_inventing_a_power_level(self):
        hero = re.search(r'<dl class="jiro-identity-facts">(.*?)</dl>', self.detail, re.S).group(1)
        facts = dict(re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', hero))
        self.assertEqual(facts["Status"], "Free · Unconscious")
        self.assertIn("Soul Manipulation", facts["Core power"])
        self.assertEqual(facts["Control"], "World Item connection severed")
        self.assertEqual(facts["Recovery"], "Soul-separation damage")
        self.assertIn("Faaram's Servant", facts["Former role"])
        self.assertNotIn("Power Level", facts)

    def test_cellar_memory_and_world_item_control_are_explicit(self):
        for fact in ("destroyed their home planet", "original universe", "perfect souls",
                     "drinking tea", "servant cellar", "possibly more than one person",
                     "warn Faaram", "Ichiro lost consciousness", "World Item controlled his soul and body",
                     "Kazz lent Faaram part of his power", "not intend to kill either brother"):
            with self.subTest(fact=fact):
                self.assertIn(fact, self.text)
        self.assertIn("suspected explanation", self.text)
        self.assertIn("cannot simply be treated as his freely chosen intent", self.text)

    def test_seal_history_does_not_override_current_survival_or_free_uwu(self):
        for fact in ("slow loss of his own conscious existence", "nearly impossible to reach",
                     "destroy the body almost immediately", "The Soul Seal stays closed",
                     "historical record", "present survival remain unrecorded",
                     "one of Ichiro's finger bones", "does not establish that she is free as well"):
            with self.subTest(fact=fact):
                self.assertIn(fact, self.text)
        self.assertNotIn("No likeness is opened", self.text)

    def test_shared_style_and_artwork_have_working_chapters(self):
        parser = DossierParser()
        parser.feed(self.detail)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertTrue(set(parser.anchors).issubset(set(parser.ids)))
        self.assertGreaterEqual(len(set(parser.anchors)), 6)
        for sheet in ("jiro-dossier.css", "ichiro-dossier.css"):
            self.assertIn("/aevum-archive/assets/" + sheet, parser.styles)
        portrait = [img for img in parser.images if img["src"].endswith("/ichiro.png")]
        self.assertEqual(len(portrait), 1)
        self.assertEqual(portrait[0]["width"], "1024")
        self.assertEqual(portrait[0]["height"], "1536")
        for image in parser.images:
            self.assertIn("alt", image)
            self.assertTrue((ROOT / image["src"].removeprefix("/aevum-archive/")).is_file())
        styles = (ROOT / "assets/ichiro-dossier.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion: reduce", styles)
        self.assertIn(".ichiro-threadwork i { animation: none; }", styles)

    def test_seal_is_a_permanently_closed_card_inside_an_open_profile(self):
        self.assertRegex(self.detail, r'<main\b[^>]*>\s*<section class="jiro-hero"')
        self.assertNotRegex(self.detail, r'<(?:details|summary|button)\b')
        for removed in ("Lift the Soul Seal", "Veil the record", "ichiro-soul-gate", "ichiro-unsealed-record"):
            self.assertNotIn(removed, self.detail)
        seal = re.search(r'<section[^>]+id="soul-seal".*?</section>', self.detail, re.S).group(0)
        card = re.search(r'<article class="ichiro-portrait ichiro-seal-card".*?</article>', seal, re.S).group(0)
        self.assertIn('class="sealed-portrait-frame"', card)
        self.assertIn("☍", card)
        self.assertIn("The soul record remains sealed.", card)
        self.assertNotRegex(card, r'\s(?:onclick|tabindex|hidden|aria-controls|href)=|role="button"')
        self.assertLess(self.detail.index('class="jiro-hero"'), self.detail.index('id="soul-seal"'))
        base = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
        frame = (ROOT / "assets/frame-overrides.css").read_text(encoding="utf-8")
        styles = (ROOT / "assets/ichiro-dossier.css").read_text(encoding="utf-8")
        self.assertIn("animation: soulPulse 4.6s ease-in-out infinite", base)
        self.assertIn('url("ui/frames/ichiro-soul-wide.png")', frame)
        self.assertIn(".ichiro-seal-card .sealed-portrait-frame::after { animation: none; }", styles)
        self.assertNotIn("ichiro-soul-gate", styles)


if __name__ == "__main__":
    unittest.main()
