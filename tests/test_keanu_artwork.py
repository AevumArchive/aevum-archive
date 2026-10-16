"""The approved Keanu artwork replaces the old file without keeping a second version."""

import hashlib
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


class KeanuArtworkTest(unittest.TestCase):
    def test_artwork_is_the_exact_supplied_replacement(self):
        artwork = (ROOT / "assets/images/keanu.png").read_bytes()
        self.assertEqual(hashlib.sha256(artwork).hexdigest(),
                         "a1849125e407f17882ff0a90e9075c371b33bf819de18610a3f77153359b4f96")
        self.assertEqual(struct.unpack(">II", artwork[16:24]), (1024, 1536))
        self.assertEqual(list((ROOT / "assets/images").glob("keanu*")), [ROOT / "assets/images/keanu.png"])

    def test_portrait_metadata_and_cache_version_match(self):
        detail = (ROOT / "npcs/keanu.html").read_text(encoding="utf-8")
        portraits = re.findall(r'<img\b[^>]*src="[^"]*/keanu\.png[^>]+>', detail)
        self.assertEqual(len(portraits), 2)
        for portrait in portraits:
            self.assertIn("keanu.png?v=20261017", portrait)
            self.assertIn('width="1024" height="1536"', portrait)
            self.assertIn("spectral faces", portrait)
        self.assertNotIn('width="1086" height="1448"', detail)
        css = (ROOT / "assets/npc-archive-refresh.css").read_text(encoding="utf-8")
        self.assertIn("keanu.png?v=20261017", css)
        self.assertIn("Gone / Lost Beyond Recovery", detail)
        self.assertIn("Raw PL 1080", detail)


if __name__ == "__main__":
    unittest.main()
