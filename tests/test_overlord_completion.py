"""Completion rewards survival; it never implies resurrection from Soul Death."""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def page(path):
    return (ROOT / path).read_text(encoding="utf-8")


def text(source):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", source)).split())


class Chapters(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.links.append(attrs["href"][1:])


class OverlordCompletionTest(unittest.TestCase):
    def test_one_identical_transcendent_record_on_profile_and_trophy_shelf(self):
        records = []
        for filename in ("characters/faaram.html", "achievements/index.html"):
            source = page(filename)
            record = re.search(r'<article class="transcendent-achievement".*?</article>', source, re.S).group(0)
            self.assertEqual(source.count('id="the-one-who-refused-the-end"'), 1)
            records.append(record)
            for fact in ("The One Who Refused the End", "TRANSCENDENT", "Highest achievement rarity", "Faaram Tempest",
                         "Second-Highest", "Multiple Years", "Soul Deaths escaped 26", "Final 8 sections 5",
                         "Complete the entire Overlord Questline", "not 26 resurrections after soul destruction",
                         "Overlord / Questline Completion / Survival"):
                with self.subTest(filename=filename, fact=fact):
                    self.assertIn(fact, text(record))
            self.assertNotIn("locked", record)
            self.assertNotIn("reward", record.lower())  # No invented points/item reward.
        self.assertEqual(records[0], records[1])

    def test_completion_does_not_change_identity_power_or_retire_faaram(self):
        source = page("characters/faaram.html")
        hero = re.search(r'<section class="tempest-hero".*?</section>', source, re.S).group(0)
        for label, value in (("Power Level", "2500"), ("Status", "ACTIVE"), ("State", "ASCENDED"), ("Race", "Elf")):
            self.assertIn(f"<dt>{label}</dt><dd>{value}</dd>", hero)
        self.assertIn("a soul he has never lost", hero)
        self.assertIn("a body he has never had to replace", hero)
        for phrase in ("Overlord Questline COMPLETED", "You did well.", "Now… you may rest.", "The road can wait.",
                       "For once, there is nothing left you need to survive.", "Reclaiming His Place · COMPLETE"):
            self.assertIn(phrase, text(source))

    def test_no_new_facts_are_invented_about_the_controller_or_recovery(self):
        story = text(page("lore/history/ichiro-and-jiro.html"))
        for fact in ("probably intercepted", "That interpretation remains a suspicion", "Kazz lent Faaram part of his power",
                     "no intention of killing Ichiro or Jiro", "World Item", "mysterious Orb", "left arm", "survive is unknown"):
            self.assertIn(fact, story)
        self.assertNotIn("Gray Orb", story)
        ichiro = page("npcs/ichiro.html")
        hero = re.search(r'<section class="jiro-hero".*?</section>', ichiro, re.S).group(0)
        self.assertNotRegex(hero.lower(), r"hidden betrayer|body is dead|remains sealed")

    def test_css_is_shared_scoped_and_has_non_flashing_reduced_motion(self):
        css = page("assets/overlord-completion.css")
        for filename in ("characters/faaram.html", "achievements/index.html"):
            self.assertIn("overlord-completion.css?v=20261023-finale1", page(filename))
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn(".transcendent-halo i, .transcendent-halo > span { animation: none; }", css)
        self.assertIn("42s linear infinite", css)
        self.assertNotIn("@import", css)

    def test_updated_records_have_unique_ids_and_working_chapters(self):
        for filename in ("characters/faaram.html", "achievements/index.html", "npcs/ichiro.html", "npcs/jiro.html"):
            with self.subTest(filename=filename):
                parsed = Chapters()
                parsed.feed(page(filename))
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                self.assertTrue(set(parsed.links).issubset(parsed.ids))

    def test_connected_summaries_do_not_keep_the_willing_betrayer_claim(self):
        for filename in ("npcs/index.html", "characters/bonds.html", "lore/factions/faaram-servants.html"):
            source = page(filename)
            self.assertNotIn("hidden betrayer", source)
            self.assertNotIn("Former servant · betrayer", source)
            self.assertIn("Unconscious" if filename != "characters/bonds.html" else "unconscious", source)
        for filename in ("index.html", "updates/index.html"):
            self.assertIn("The One Who Refused the End", page(filename))
            self.assertIn("They never chose to leave", page(filename))


if __name__ == "__main__":
    unittest.main()
