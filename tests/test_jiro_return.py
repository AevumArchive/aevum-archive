"""The new liberation canon supersedes apparent memory recovery and safe survival."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def page(path):
    return (ROOT / path).read_text(encoding="utf-8")


class JiroReturnTest(unittest.TestCase):
    def facts(self, class_name):
        block = re.search(r'<dl class="' + class_name + r'">(.*?)</dl>', page("npcs/jiro.html"), re.S).group(1)
        return dict(re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', block))

    def test_orb_amplification_is_not_a_new_current_power_measurement(self):
        facts = self.facts("jiro-power-ledger")
        self.assertEqual(facts["Current power"], "Unconfirmed / Critical")
        self.assertEqual(facts["Historical power"], "Approx. 2200–2400")
        self.assertEqual(facts["Memory state"], "Gaps during control")
        self.assertEqual(facts["Control"], "Orb removed")
        self.assertEqual(facts["Survival"], "Uncertain")
        detail = page("npcs/jiro.html")
        self.assertIn("Jiro injured Bomir", detail)
        self.assertIn("The echo is Jiro's own soul", detail)
        self.assertIn("no separate personality or will", detail)

    def test_history_artwork_and_injury_boundaries_survive(self):
        detail = page("npcs/jiro.html")
        self.assertIn("Ichiro's brother", detail)
        self.assertIn("Ultimate Empowered Resurrection", detail)
        self.assertIn("cost Faaram the ability itself", detail)
        self.assertIn("Jiro survived the Aizen event with severe injuries", detail)
        self.assertEqual(detail.count('src="/aevum-archive/assets/images/jiro-returned.png"'), 1)
        self.assertIn("Before the final injuries", detail)
        self.assertIn("Both portraits predate the loss of his left arm", detail)
        for phrase in ("left arm", "massive hole in his chest", "condition is critical", "whether he will survive"):
            self.assertIn(phrase, detail)
        self.assertNotIn("His loyalty was conscious and chosen.", detail)
        self.assertNotIn("every living thing is <em>vermin", detail)

    def test_connected_current_records_agree_that_jiro_is_critical_not_dead(self):
        npc_entry = re.search(r'<a[^>]+href="/aevum-archive/npcs/jiro.html".*?</a>', page("npcs/index.html"), re.S).group(0)
        bond_entry = re.search(r'<a[^>]+href="/aevum-archive/npcs/jiro.html".*?</a>', page("characters/bonds.html"), re.S).group(0)
        faction_entry = re.search(r'<div class="faction-member"><strong>Jiro</strong>.*?</div>', page("lore/factions/faaram-servants.html"), re.S).group(0)
        for entry in (npc_entry, bond_entry, faction_entry):
            self.assertIn("critical", entry.lower())
            self.assertIn("free", entry.lower())
            self.assertNotIn("fallen", entry.lower())

    def test_hero_summary_agrees_with_detailed_power_record(self):
        hero = self.facts("jiro-identity-facts")
        ledger = self.facts("jiro-power-ledger")
        for short, full in (("Power Level", "Current power"), ("Historical PL", "Historical power"), ("Memory", "Memory state"), ("Control", "Control")):
            self.assertEqual(hero[short], ledger[full])
        self.assertEqual(hero["Presence"], "Free · Critical")
        self.assertEqual(hero["Injuries"], "Left arm lost · Massive chest wound")

    def test_the_warning_and_implantation_keep_uncertainty_distinct(self):
        detail = page("npcs/jiro.html")
        for fact in ("warn Faaram", "never reached", "probably intercepted", "no memory", "without his conscious knowledge", "interception is suspected", "influence over his will are confirmed"):
            self.assertIn(fact, detail)
        self.assertIn("He did not choose to abandon Faaram", detail)


if __name__ == "__main__":
    unittest.main()
