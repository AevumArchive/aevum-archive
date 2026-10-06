"""Focused regression checks for the character archive's public record state."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def page(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class CharacterRecordsTest(unittest.TestCase):
    def test_obama_is_active_across_public_entries(self) -> None:
        detail = page("characters/obama.html")
        hall = page("characters/all.html")
        shelf = page("characters/index.html")
        old_road = page("playthroughs/aizen-ended-road.html")

        self.assertIn("<dt>Status</dt><dd>ACTIVE</dd>", detail)
        self.assertIn('data-status="active" data-name="OBAMA"', hall)
        self.assertIn("Active <span>6</span>", hall)
        self.assertIn("Sealed <span>4</span>", hall)
        self.assertIn("Six active names", shelf)
        self.assertIn('status-card active golden-status" href="/aevum-archive/characters/obama.html"', old_road)

    def test_portraits_are_not_repeated_below_the_hero(self) -> None:
        for name in (
            "astera-zenith", "faaram", "guts", "jango", "jonathan",
            "lythariel", "obama", "william-carter", "zeke",
        ):
            with self.subTest(character=name):
                detail = page(f"characters/{name}.html")
                self.assertIn('class="record-hero"', detail)
                self.assertNotIn('class="card portrait-card', detail)
                self.assertIn('role="img" aria-label="Portrait of ', detail)

    def test_gray_orb_visual_does_not_claim_a_canonical_likeness(self) -> None:
        detail = page("characters/faaram.html")
        self.assertIn('class="orb-archive-diagram"', detail)
        self.assertIn("Archive visualization · likeness unknown", detail)
        self.assertIn('/world-items/#gray-orb', detail)

    def test_hero_art_uses_uncropped_source_ratio(self) -> None:
        styles = page("assets/archive-record-refresh.css")
        self.assertIn("aspect-ratio: var(--portrait-ratio, 2 / 3)", styles)
        self.assertIn("background-size: cover, contain", styles)
        for name in ("guts", "jonathan", "obama"):
            self.assertIn(f"body.route-characters-{name} {{ --portrait-ratio:", styles)

    def test_character_facts_are_readable_pairs(self) -> None:
        styles = page("assets/archive-record-refresh.css")
        self.assertIn(".record-panel .record-fact", styles)
        self.assertIn("font-size: 1rem;", styles)
        for name in (
            "astera-zenith", "faaram", "guts", "jango", "jonathan",
            "lythariel", "obama", "william-carter", "jawohl", "khealdur",
            "mortis", "raven", "tony", "zeke",
        ):
            with self.subTest(character=name):
                detail = page(f"characters/{name}.html")
                facts = re.search(r'<article class="record-panel">.*?<dl>(.*?)</dl>', detail)
                self.assertIsNotNone(facts)
                pairs = re.findall(
                    r'<div class="record-fact"><dt>.*?</dt><dd>.*?</dd></div>',
                    facts.group(1),
                )
                self.assertGreater(len(pairs), 0)
                self.assertEqual("".join(pairs), facts.group(1))
                self.assertIn("archive-record-refresh.css?v=20261006-4", detail)


if __name__ == "__main__":
    unittest.main()
