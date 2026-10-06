"""Keep the public player census and its HTML fallbacks in sync."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ArchiveCensusTest(unittest.TestCase):
    def test_player_count_is_consistent(self) -> None:
        snapshot = json.loads((ROOT / "data/archive-public.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["playerCount"], 1486)

        for path in ("index.html", "leaderboard/index.html"):
            with self.subTest(page=path):
                html = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("data-archive-player-count>1,486<", html)
                self.assertNotIn("data-archive-player-count>903<", html)


if __name__ == "__main__":
    unittest.main()
