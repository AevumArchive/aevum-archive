"""Keep Faaram's possible future and witnessed alternate distinct from canon present."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FaaramVariantsTest(unittest.TestCase):
    def test_cross_continuity_art_is_local_and_separately_classified(self) -> None:
        detail = (ROOT / "characters/faaram.html").read_text(encoding="utf-8")
        styles = (ROOT / "assets/archive-record-refresh.css").read_text(encoding="utf-8")

        self.assertIn('id="faaram-variants"', detail)
        self.assertIn('Possible future · Unconfirmed', detail)
        self.assertIn('A possible future for Faaram, not a confirmed outcome.', detail)
        self.assertIn('Alternate multiverse · Witnessed', detail)
        self.assertIn('The Faaram who never died', detail)
        self.assertIn('a different multiverse that is already collapsing', detail)
        self.assertIn('width: 100%; height: auto', styles)

        for asset in ("faaram-possible-future.png", "faaram-alternate-never-died.png"):
            with self.subTest(asset=asset):
                self.assertTrue((ROOT / "assets/images" / asset).is_file())
                self.assertIn(f'/aevum-archive/assets/images/{asset}', detail)

        # The variants must not replace his present-day hero portrait.
        self.assertIn('body.route-characters-faaram .record-hero > .character-card { --record-art: url("/aevum-archive/assets/images/faaram.png"); }', styles)


if __name__ == "__main__":
    unittest.main()
