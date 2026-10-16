"""Jiro's return must not turn apparent memory recovery into restored peak power."""

from html import unescape
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def page(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class JiroReturnTest(unittest.TestCase):
    def test_memory_and_power_remain_distinct(self) -> None:
        detail = page("npcs/jiro.html")
        ledger = re.search(r'<dl class="jiro-power-ledger">(.*?)</dl>', detail, re.S).group(1)
        facts = dict(re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', ledger))
        self.assertEqual(facts["Current power"], "Unconfirmed / Recovering")
        self.assertEqual(facts["Historical power"], "Approx. 2200–2400")
        self.assertEqual(facts["Memory state"], "Appears Fully Restored")
        self.assertEqual(facts["Peak strength"], "Not Restored")
        self.assertIn("Whether every memory has truly returned cannot yet be proven", detail)
        self.assertIn("The echo is Jiro's own soul", detail)
        self.assertIn("no separate personality or will", detail)

    def test_return_keeps_bonds_history_and_approved_artwork(self) -> None:
        detail = page("npcs/jiro.html")
        self.assertIn("Jiro is <a", detail)
        self.assertIn("Ichiro's brother", detail)
        self.assertIn("Ultimate Empowered Resurrection", detail)
        self.assertIn("cost Faaram the ability itself", detail)
        self.assertIn("Jiro survived the Aizen event with severe injuries", detail)
        self.assertNotIn("as fallen again", detail)
        self.assertNotIn("Ichiro's defining association remains", detail)
        self.assertEqual(detail.count('src="/aevum-archive/assets/images/jiro-returned.png"'), 1)
        self.assertTrue((ROOT / "assets/images/jiro-returned.png").is_file())
        visible_text = " ".join(unescape(re.sub(r"<[^>]+>", " ", detail)).split())
        self.assertIn("In Jiro's eyes, every living thing is vermin.", visible_text)
        self.assertIn("Jiro remembers the height from which he once looked down upon the world. He simply has not climbed back to it yet.", unescape(detail))

    def test_connected_current_records_no_longer_call_jiro_fallen(self) -> None:
        npc_entry = re.search(r'<a[^>]+href="/aevum-archive/npcs/jiro.html".*?</a>', page("npcs/index.html"), re.S).group(0)
        bond_entry = re.search(r'<a[^>]+href="/aevum-archive/npcs/jiro.html".*?</a>', page("characters/bonds.html"), re.S).group(0)
        faction_entry = re.search(r'<div class="faction-member"><strong>Jiro</strong>.*?</div>', page("lore/factions/faaram-servants.html"), re.S).group(0)
        for entry in (npc_entry, bond_entry, faction_entry):
            self.assertRegex(entry.lower(), r"alive|surviv")
            self.assertIn("aizen", entry.lower())
            self.assertNotIn("fallen", entry.lower())

    def test_hero_summary_agrees_with_detailed_power_record(self) -> None:
        detail = page("npcs/jiro.html")
        hero = re.search(r'<dl class="jiro-identity-facts">(.*?)</dl>', detail, re.S).group(1)
        ledger = re.search(r'<dl class="jiro-power-ledger">(.*?)</dl>', detail, re.S).group(1)
        summary = dict(re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', hero))
        facts = dict(re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', ledger))
        self.assertEqual(summary["Power Level"], facts["Current power"])
        self.assertEqual(summary["Historical PL"], facts["Historical power"])
        self.assertEqual(summary["Memory"], facts["Memory state"])
        self.assertEqual(summary["Peak strength"], facts["Peak strength"])
        self.assertEqual(summary["Presence"], "Alive · Recovering")

    def test_aizen_survival_is_explained_in_connected_lore(self) -> None:
        for path in ("npcs/jiro.html", "npcs/index.html", "lore/factions/faaram-servants.html", "lore/history/ichiro-and-jiro.html", "updates/index.html", "index.html"):
            with self.subTest(path=path):
                self.assertIn("survived the aizen event with severe injuries", page(path).lower())


if __name__ == "__main__":
    unittest.main()
