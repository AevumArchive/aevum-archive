"""The Bridge remains a distinct, canon-bounded dimensional record."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BridgeDimensionTest(unittest.TestCase):
    def test_bridge_page_has_its_own_visual_and_opened_facts(self) -> None:
        page = (ROOT / "lore/dimensions/the-bridge.html").read_text(encoding="utf-8")
        css = (ROOT / "assets/bridge-dimension.css").read_text(encoding="utf-8")

        self.assertIn('bridge-dimension.css', page)
        self.assertIn('aria-label="Abstract Archive visualization', page)
        self.assertIn('Not a surveyed map', page)
        self.assertIn('Major gates and scattered access points', page)
        self.assertIn('under Lilith\'s rule', page)
        self.assertIn('Weak souls that remain there too long may be warped into demons', page)
        self.assertIn('The Bridge is a separate otherworldly dimension', page)
        self.assertIn('Lilith is not named as their cause', page)
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertIn('bridge-dimension-entry', (ROOT / 'lore/dimensions/index.html').read_text(encoding='utf-8'))


if __name__ == "__main__":
    unittest.main()
