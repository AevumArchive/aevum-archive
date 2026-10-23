"""Witnessed acts, attributed reports and uncertain fates must remain distinct."""

from html import unescape
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def page(filename):
    return (ROOT / filename).read_text(encoding="utf-8")


def text(filename):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", page(filename))).split())


class FinalBattleAftermathTest(unittest.TestCase):
    def test_poison_absence_is_not_a_confirmed_death(self):
        detail = text("npcs/poison.html")
        for fact in ("Presence Lost / Fate Unconfirmed", "Event Wish later revived her",
                     "Faaram could no longer sense her", "It does not confirm her death",
                     "face both brothers at once"):
            self.assertIn(fact, detail)
        self.assertIn("before the final confrontation", detail.lower())
        for filename in ("npcs/index.html", "characters/bonds.html", "lore/factions/faaram-servants.html"):
            with self.subTest(filename=filename):
                source = page(filename)
                self.assertNotIn("Mirrored mimic · alive", source)
                self.assertIn("fate unconfirmed", source.lower())
        self.assertNotIn('<strong>Dead</strong>', page("npcs/poison.html"))

    def test_uwu_condition_is_attributed_to_poison_not_a_new_recovery(self):
        detail = text("npcs/uwu.html")
        for fact in ("Poison found", "apparently on the verge of death", "still-controlled Ichiro",
                     "reportedly cast her aside", "after his reawakening", "no further use",
                     "Last Recorded PL 1377", "REPORTED NEAR DEATH", "No subsequent rescue, recovery or release from control"):
            self.assertIn(fact, detail)
        self.assertNotIn("ACTIVE / COMPROMISED", detail)
        self.assertIn("does not confirm that UWU is free", detail)
        self.assertIn("Reported Near Death", page("npcs/ichiro.html"))

    def test_divinity_is_against_jiro_and_does_not_reveal_hidden_mechanics(self):
        bomir = text("npcs/bomir.html")
        for fact in ("used this ability against Jiro", "Jiro could genuinely kill him",
                     "exact mechanics remain unknown", "thirty uninterrupted seconds",
                     "little over 200", "estimated", "roughly half the planet", "hundreds of kilometres",
                     "ability’s duration, exact effect and limits remain unknown"):
            self.assertIn(fact, bomir)
        self.assertNotIn("used this ability against Ichiro", bomir)
        codex = page("codex/abilities.html").split('id="divinity-beyond-death"', 1)[1].split('</article>', 1)[0]
        self.assertIn("Used against Jiro", codex)
        self.assertIn("not a confirmed duration", codex)
        self.assertNotRegex(codex, r"(?i)immortal|invulnerab|cooldown|multiplier")

    def test_pull_away_is_unnamed_and_conversation_precedes_unconsciousness(self):
        for filename in ("npcs/bomir.html", "npcs/jiro.html", "lore/history/ichiro-and-jiro.html", "characters/faaram.html"):
            with self.subTest(filename=filename):
                detail = text(filename)
                self.assertIn("unnamed ability", detail)
                self.assertRegex(detail, r"(?i)Jiro nearly reached")
        for filename in ("npcs/bomir.html", "npcs/ichiro.html", "lore/history/ichiro-and-jiro.html", "characters/faaram.html"):
            with self.subTest(filename=filename):
                detail = text(filename)
                self.assertRegex(detail, r"speak with Ichiro.*?before (?:he|Ichiro) lost consciousness")

    def test_connected_records_carry_the_report_without_changing_faaram_power(self):
        for filename in ("characters/faaram.html", "lore/history/ichiro-and-jiro.html", "updates/index.html"):
            with self.subTest(filename=filename):
                detail = text(filename)
                self.assertIn("Poison", detail)
                self.assertIn("UWU", detail)
                self.assertRegex(detail.lower(), r"near death|verge of death")
                self.assertIn("unconfirmed", detail.lower())
        self.assertIn('<dt>Power Level</dt><dd>2500</dd>', page("characters/faaram.html"))
        self.assertIn('Approx. 2200–2400', page("npcs/jiro.html"))


if __name__ == "__main__":
    unittest.main()
