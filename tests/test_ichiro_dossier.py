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
        self.gate_attrs = None
        self.in_gate = False
        self.gated_ids = set()
        self.ungated_images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details" and attrs.get("id") == "soul-seal":
            self.gate_attrs = attrs
            self.in_gate = True
        if "id" in attrs:
            self.ids.append(attrs["id"])
            if self.in_gate:
                self.gated_ids.add(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.anchors.append(attrs["href"][1:])
        if tag == "img":
            self.images.append(attrs)
            if not self.in_gate:
                self.ungated_images.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.styles.append(attrs["href"].split("?")[0])

    def handle_endtag(self, tag):
        if tag == "details":
            self.in_gate = False


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

    def test_seal_must_be_lifted_before_any_dossier_information(self):
        parser = DossierParser()
        parser.feed(self.detail)
        self.assertIsNotNone(parser.gate_attrs)
        self.assertNotIn("open", parser.gate_attrs)
        for chapter in ("ichiro-title", "ichiro-unsealed-record", "current-state",
                        "soul-manipulation", "conspiracy", "sealed-remains", "uwu-trace", "bonds"):
            self.assertIn(chapter, parser.gated_ids)
        self.assertEqual(parser.ungated_images, ["/aevum-archive/assets/home-v2/home-archive-sigil.webp"])
        summary = re.search(r"<summary\b.*?</summary>", self.detail, re.S).group(0)
        self.assertIn("Lift the Soul Seal", summary)
        self.assertIn('aria-controls="ichiro-unsealed-record"', summary)
        for spoiler in ("Death Note", "Keanu", "UWU", "Timeo"):
            self.assertNotIn(spoiler, summary)
        base = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
        frame = (ROOT / "assets/frame-overrides.css").read_text(encoding="utf-8")
        self.assertIn("animation: soulPulse 4.6s ease-in-out infinite", base)
        self.assertIn('url("ui/frames/ichiro-soul-wide.png")', frame)
        self.assertNotIn("ichiro-seal-emblem", self.detail)


if __name__ == "__main__":
    unittest.main()
