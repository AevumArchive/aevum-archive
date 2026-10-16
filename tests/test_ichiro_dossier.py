"""Ichiro's new presentation must keep the sealed record and its lore intact."""

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

    def test_hero_keeps_death_seal_and_trace_distinct(self):
        hero = re.search(r'<dl class="jiro-identity-facts">(.*?)</dl>', self.detail, re.S).group(1)
        facts = dict(re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', hero))
        self.assertEqual(facts["Status"], "Dead / Remains Sealed")
        self.assertIn("Soul Manipulation", facts["Core power"])
        self.assertIn("Shadow Realm · Cursed", facts["Remains"])
        self.assertIn("Influence Through UWU", facts["Current trace"])
        self.assertIn("Faaram's Servant", facts["Former role"])
        self.assertNotIn("Power Level", facts)

    def test_conspiracy_and_family_history_survive(self):
        for fact in ("destroyed their home planet", "original universe", "perfect souls",
                     "Ichiro remembered everything", "taken his brother from him",
                     "turned Timeo against Faaram", "restored Jiro's memories",
                     "stood apart from the final clash", "killed by the Death Note"):
            with self.subTest(fact=fact):
                self.assertIn(fact, self.text)
        self.assertIn("Jiro's Reinforced Soul resisted Ichiro's direct control", self.text)

    def test_seal_and_likeness_do_not_imply_resurrection_or_open_access(self):
        for fact in ("slow loss of his own conscious existence", "Reaching them is considered nearly impossible",
                     "destroy the body almost immediately", "the Soul Seal stays closed",
                     "Multiversal Convergence", "Whether the fusion lifted an older veil remains unknown",
                     "one of Ichiro's finger bones", "autonomy cannot yet be separated from his control"):
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


if __name__ == "__main__":
    unittest.main()
