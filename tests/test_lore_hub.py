"""The Lore Atlas is a public, portrait-free index, not a source of new canon."""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HubParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images, self.scripts = [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "img":
            self.images.append(attrs.get("src", ""))
        if tag == "script":
            self.scripts.append(attrs.get("src", ""))


class LoreHubTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / "lore/index.html").read_text(encoding="utf-8")
        cls.text = " ".join(unescape(re.sub(r"<[^>]+>", " ", cls.source)).split())
        cls.parsed = HubParser()
        cls.parsed.feed(cls.source)

    def test_preserved_archive_routes_and_unique_chapters(self):
        destinations = ("lore/maps/", "lore/history/", "lore/locations/", "lore/factions/", "lore/cosmology/",
                        "lore/dimensions/", "codex/", "lore/cosmology/the-old-world.html", "lore/cosmology/the-umbral-meridian.html",
                        "lore/kingdoms/avalon.html", "lore/settlements/neris.html", "lore/noble-houses/house-zenith.html",
                        "lore/locations/crownbridge-front.html", "characters/", "playthroughs/alterra-origin.html",
                        "lore/factions/vault-8-authority.html", "lore/locations/temmie-town.html",
                        "events/multiversal-convergence.html", "lore/dimensions/shadow-realm.html",
                        "events/the-silent-fault.html", "events/night-of-thousand-gates.html", "sealed-records/", "updates/")
        for destination in destinations:
            self.assertIn("/aevum-archive/" + destination, self.parsed.links)
        self.assertEqual(len(self.parsed.ids), len(set(self.parsed.ids)))
        for href in self.parsed.links:
            if href.startswith("#"):
                self.assertIn(href[1:], self.parsed.ids)
        for chapter in ("current-road", "archive-wings", "deep-archive", "latest-revelations"):
            self.assertIn(chapter, self.parsed.ids)
        self.assertEqual(len(re.findall(r'<a class="atlas-wing(?:\s|\")', self.source)), 6)

    def test_latest_revelations_keep_completion_and_survival_distinct(self):
        for fact in ("Overlord Questline / COMPLETED", "The One Who Refused the End", "TRANSCENDENT",
                     "Highest achievement rarity", "26 Soul Deaths escaped", "5 in the final 8 sections",
                     "They never chose to leave.", "outside control", "Ichiro Free · Unconscious",
                     "Jiro Free · Critical", "Poison Fate Unconfirmed", "UWU Reported Near Death"):
            self.assertIn(fact, self.text)
        self.assertIn("characters/faaram.html#overlord-completion", self.source)
        self.assertIn("lore/history/ichiro-and-jiro.html", self.source)
        self.assertNotIn("26 resurrections", self.source)

    def test_uncertainty_and_sealed_knowledge_remain_explicit(self):
        for fact in ("her possible death is unconfirmed", "reported finding UWU apparently near death",
                     "Its exact effect remains unknown", "Partly sealed dimension", "Unopened shelf",
                     "Lost / Unknown · After the soul incident", "What has not been revealed remains unwritten"):
            self.assertIn(fact, self.text)
        self.assertNotIn("Enski", self.source)
        self.assertNotIn("Tenrei", self.source)
        self.assertNotRegex(self.source, r'(?i)poison (?:is dead|has died)|jiro is dead|astera is dead')
        self.assertNotIn("deep-archive/vault", self.source)

    def test_historical_dates_and_portrait_free_selection_are_preserved(self):
        for date in ("2017-05-04", "2019-02-23", "2021-06-21"):
            self.assertIn(f'datetime="{date}"', self.source)
        self.assertEqual(len(self.parsed.images), 1)  # Shared header crest only.
        self.assertNotIn("assets/images/", self.source)
        self.assertNotRegex(self.source, r'<[^>]+\shidden(?:[=\s>])')
        self.assertEqual(self.parsed.scripts, ["/aevum-archive/assets/master-ui.js?v=20260821-2"])

    def test_hub_styles_are_scoped_local_and_accessible(self):
        css = (ROOT / "assets/lore-atlas.css").read_text(encoding="utf-8")
        self.assertIn("lore-atlas.css?v=20261023-living-atlas1", self.source)
        self.assertIn("body.route-lore", css)
        self.assertIn(".lore-hub a:focus-visible", css)
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn("animation: none !important; transition: none !important", css)
        self.assertIn("100s linear infinite", css)
        self.assertNotIn("url(", css)
        self.assertNotIn("@import", css)


if __name__ == "__main__":
    unittest.main()
