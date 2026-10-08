"""Keep the homepage's latest records aligned with the update ledger."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class UpdateLedgerTest(unittest.TestCase):
    def test_homepage_cards_match_latest_ledger_entries(self) -> None:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        ledger = (ROOT / "updates/index.html").read_text(encoding="utf-8")
        home_section = home.split('id="latest-archive-updates"', 1)[1]
        home_titles = re.findall(r"<h3>([^<]+)</h3>", home_section)[:3]
        ledger_titles = re.findall(r'<article class="archive-update">.*?<h2>([^<]+)</h2>', ledger)
        self.assertEqual(home_titles, ledger_titles[:3])
        self.assertEqual(len(home_titles), 3)
        self.assertIn("Faaram nears his true potential", home_titles)
        self.assertIn("has yet to fully claim", home_section)
        self.assertNotIn("Ichiro likeness recorded", home_section)
        self.assertNotIn("The Sunflower had three heads", home_section)


if __name__ == "__main__":
    unittest.main()
