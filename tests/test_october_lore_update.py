"""Checks for the witnessed Poison, OBAMA, Astera and Tenrei archive updates."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def page(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class OctoberLoreUpdateTest(unittest.TestCase):
    def test_poison_is_alive_across_public_records(self) -> None:
        detail = page("npcs/poison.html")
        ledger = page("npcs/index.html")
        bonds = page("characters/bonds.html")

        self.assertIn('<span>Current state</span><strong>Alive</strong>', detail)
        self.assertIn('<span class="pill">Alive</span>', ledger)
        self.assertIn('Mirrored mimic · alive', bonds)
        self.assertNotIn('Afterlife', detail)
        self.assertNotIn('fallen before Rift', bonds)

    def test_obama_power_level_is_2100(self) -> None:
        detail = page("characters/obama.html")
        self.assertIn('<dt>Power Level</dt><dd>2100</dd>', detail)
        self.assertNotIn('<dt>Power Level</dt><dd>1600</dd>', detail)

    def test_astera_divine_discovery_is_witnessed(self) -> None:
        trophies = page("achievements/index.html")
        astera = page("characters/astera-zenith.html")
        styles = page("assets/astera-lore.css")

        self.assertIn('id="a-name-unknown-until-now"', trophies)
        self.assertIn('Divine Achievement · Lore Discovery', trophies)
        self.assertIn('A Name Unknown to the World...', trophies)
        self.assertIn('<strong>Tenrei</strong>', trophies)
        self.assertIn('+250,000 Points', trophies)
        self.assertIn('7 records held', trophies)
        self.assertEqual(trophies.count('class="trophy-card'), 7)
        self.assertNotIn('Coin of the Astral Veil', trophies)
        self.assertNotIn('Astral Coin · Guts', trophies)
        self.assertIn('<h3>Astral Coin</h3>', trophies)
        self.assertIn('class="pill divine-achievement-pill"', astera)
        self.assertIn('class="divine-discovery-card"', astera)
        self.assertIn('.divine-trophy {', styles)

    def test_tenrei_is_first_witnessed_dev_npc(self) -> None:
        devs = page("deep-archive/dev-npcs.html")
        self.assertIn('01 of 15 witnessed', devs)
        self.assertIn('01 / 15 signatures witnessed', devs)
        self.assertIn('<h3>Tenrei</h3>', devs)
        self.assertIn('DEV NPC · Discovered by Astera Zenith', devs)
        self.assertEqual(devs.count('class="dev-slot'), 15)
        self.assertEqual(devs.count('DEV NPC · Unwitnessed'), 14)


if __name__ == "__main__":
    unittest.main()
