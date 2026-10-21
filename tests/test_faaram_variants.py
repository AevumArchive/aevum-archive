"""Remove the obsolete future path; keep the witnessed alternate a separate record."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FaaramVariantsTest(unittest.TestCase):
    def test_cross_continuity_art_is_local_and_separately_classified(self) -> None:
        detail = (ROOT / "characters/faaram.html").read_text(encoding="utf-8")
        styles = (ROOT / "assets/archive-record-refresh.css").read_text(encoding="utf-8")

        self.assertIn('id="faaram-variants"', detail)
        self.assertNotIn('Possible future', detail)
        self.assertNotIn('future-variant', detail)
        self.assertNotIn('faaram-possible-future.png', detail)
        self.assertIn('not a future path for Faaram Tempest', detail)
        self.assertIn('Alternate multiverse · Witnessed', detail)
        self.assertIn('The Faaram who never died', detail)
        self.assertIn('a different multiverse that is already collapsing', detail)
        self.assertIn('not a transformation awaiting Faaram Tempest', detail)
        self.assertEqual(detail.count('<figure class="faaram-variant-card'), 1)
        self.assertIn('width: 100%; height: auto', styles)

        for asset in ("faaram-alternate-never-died.png",):
            with self.subTest(asset=asset):
                self.assertTrue((ROOT / "assets/images" / asset).is_file())
                self.assertIn(f'/aevum-archive/assets/images/{asset}', detail)

        # The separate sighting must not replace his present-day hero portrait.
        self.assertIn('class="tempest-portrait"><img src="/aevum-archive/assets/images/faaram-tempest.png"', detail)


if __name__ == "__main__":
    unittest.main()
