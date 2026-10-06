"""Astera's completed questline stays consistent across public records."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def page(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class AsteraQuestCompletionTest(unittest.TestCase):
    def test_character_record_and_artwork(self) -> None:
        astera = page("characters/astera-zenith.html")
        artwork = ROOT / "assets/images/astera-umbral-meridian-quest-complete.png"

        self.assertTrue(artwork.is_file())
        self.assertIn('id="umbral-meridian-complete"', astera)
        self.assertIn('src="/aevum-archive/assets/images/astera-umbral-meridian-quest-complete.png"', astera)
        self.assertIn('<dt>Main Quests</dt><dd>The Umbral Meridian · Beyond the Mark — COMPLETE</dd>', astera)
        self.assertIn('<dd>Hollow Star · COMPLETE</dd>', astera)
        self.assertIn('<dd>STABILIZED · Left Eye Fully Awakened</dd>', astera)
        self.assertIn('Faaram\'s Soul Mark</span><strong>Active</strong>', astera)
        self.assertIn('Astera did not learn who caused the severance', astera)
        self.assertIn('it is not yet her home', astera)
        self.assertNotIn('PARTIAL INTEGRATION', astera)
        self.assertNotIn('AWAKENED / UNSTABLE', astera)

    def test_related_records_do_not_present_old_state_as_current(self) -> None:
        faaram = page("characters/faaram.html")
        playthrough = page("playthroughs/fantasy-medieval.html")

        self.assertIn('She has since completed its integration', faaram)
        self.assertIn('The Umbral Meridian · Beyond the Mark', playthrough)
        self.assertIn('Second Sight is stabilized', playthrough)
        self.assertNotIn('visibility-state partial">Partial</span><h3>The Umbral Meridian', playthrough)


if __name__ == "__main__":
    unittest.main()
