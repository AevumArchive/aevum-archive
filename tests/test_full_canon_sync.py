"""Regression checks for the October 2026 public canon synchronization."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def page(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class FullCanonSyncTest(unittest.TestCase):
    def test_beru_is_public_and_portrait_is_local(self) -> None:
        detail = page("characters/beru.html")
        self.assertIn("Sunborn Goliath", detail)
        self.assertIn("Divine Greatshield", detail)
        self.assertIn('data-name="Beru"', page("characters/all.html"))
        self.assertIn('id="sunborn-goliath"', page("codex/races.html"))
        self.assertIn('images/beru.png', page("assets/archive-record-refresh.css"))
        self.assertTrue((ROOT / "assets/images/beru.png").is_file())

    def test_enski_is_restricted_only(self) -> None:
        self.assertIn('data-restricted-record="enski"', page("deep-archive/entities/enski.html"))
        self.assertIn('deep-archive/entities/enski.html', page("deep-archive/vault.html"))
        self.assertNotIn("Enski", page("npcs/index.html"))

    def test_character_states_and_world_gateway(self) -> None:
        self.assertIn('Reclaiming His Place · COMPLETE', page("characters/faaram.html"))
        self.assertIn('major but incomplete portion', page("characters/astera-zenith.html"))
        self.assertIn("Faaram's Soul Mark", page("codex/bindings.html"))
        self.assertIn('Gateway status</dt><dd>OPEN', page("world-events/index.html"))
        self.assertIn('Opening sequence</dt><dd>COMPLETE', page("world-events/index.html"))
        self.assertIn('permanent +70%', page("characters/obama.html"))
        self.assertIn('Event Wish later revived her', page("npcs/poison.html"))
        self.assertIn('Treacherous Cleaver ×2', page("npcs/timeo.html"))

    def test_codex_classification_boundaries(self) -> None:
        traits = page("codex/traits.html")
        abilities = page("codex/abilities.html")
        for trait in ('id="imposed-reality"', 'id="overlords-grace"', 'id="duality"'):
            self.assertIn(trait, traits)
        for ability in ('id="second-sight"', 'id="meridian-vision"', 'id="adaptive-copy"', 'id="beast-taming"'):
            self.assertIn(ability, abilities)
        self.assertNotIn('id="faarams-soul-mark"', traits)
        self.assertIn('id="faarams-soul-mark"', page("codex/bindings.html"))
        self.assertIn('Character-bound artifact · not a World Item', page("world-items/index.html"))


if __name__ == "__main__":
    unittest.main()
