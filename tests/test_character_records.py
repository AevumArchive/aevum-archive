"""Focused regression checks for the character archive's public record state."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def page(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class CharacterRecordsTest(unittest.TestCase):
    def test_obama_is_active_across_public_entries(self) -> None:
        detail = page("characters/obama.html")
        hall = page("characters/all.html")
        shelf = page("characters/index.html")
        old_road = page("playthroughs/aizen-ended-road.html")

        self.assertIn("<dt>Status</dt><dd>ACTIVE</dd>", detail)
        self.assertIn('data-status="active" data-name="OBAMA"', hall)
        self.assertIn("Active <span>5</span>", hall)
        self.assertIn("Sealed <span>3</span>", hall)
        self.assertIn("Five active names", shelf)
        self.assertIn('status-card active golden-status" href="/aevum-archive/characters/obama.html"', old_road)

    def test_guts_is_fallen_not_on_the_active_shelf(self) -> None:
        detail = page("characters/guts.html")
        hall = page("characters/all.html")
        shelf = page("characters/index.html")
        playthrough = page("playthroughs/fantasy-medieval.html")

        self.assertIn("<dt>Status</dt><dd>FALLEN</dd>", detail)
        self.assertIn('data-status="fallen" data-name="Guts"', hall)
        self.assertIn("Fallen <span>3</span>", hall)
        self.assertIn("Five active names", shelf)
        self.assertNotIn('href="/aevum-archive/characters/guts.html"', shelf)
        self.assertNotIn('href="/aevum-archive/characters/guts.html"', playthrough)

    def test_astera_is_lost_and_faaram_is_active(self) -> None:
        astera = page("characters/astera-zenith.html")
        faaram = page("characters/faaram.html")
        hall = page("characters/all.html")
        shelf = page("characters/index.html")
        old_road = page("playthroughs/aizen-ended-road.html")

        self.assertIn('<dt>Status</dt><dd>LOST / UNKNOWN</dd>', astera)
        self.assertIn('Her current whereabouts are unknown; no death is confirmed.', astera)
        self.assertIn('<dt>Status</dt><dd>ACTIVE</dd>', faaram)
        self.assertIn('data-status="lost" data-name="Astera Zenith"', hall)
        self.assertIn('data-status="active" data-name="Faaram"', hall)
        self.assertIn('Active <span>5</span>', hall)
        self.assertIn('Sealed <span>3</span>', hall)
        self.assertIn('Lost / Unknown <span>2</span>', hall)
        self.assertIn('Faaram, Lythariel, William, Jango and OBAMA', shelf)
        self.assertIn('status-card active" href="/aevum-archive/characters/faaram.html"', old_road)

    def test_portraits_are_not_repeated_below_the_hero(self) -> None:
        for name in (
            "astera-zenith", "beru", "faaram", "guts", "jango", "jonathan",
            "lythariel", "obama", "william-carter", "zeke",
        ):
            with self.subTest(character=name):
                detail = page(f"characters/{name}.html")
                self.assertIn('class="record-hero"', detail)
                self.assertNotIn('class="card portrait-card', detail)
                self.assertIn('role="img" aria-label="Portrait of ', detail)

    def test_gray_orb_visual_does_not_claim_a_canonical_likeness(self) -> None:
        detail = page("characters/faaram.html")
        self.assertIn('class="orb-archive-diagram"', detail)
        self.assertIn("Archive visualization · likeness unknown", detail)
        self.assertIn('/world-items/#gray-orb', detail)

    def test_overlords_grace_keeps_its_signature_layout_and_motion(self) -> None:
        detail = page("characters/faaram.html")
        styles = page("assets/archive-record-refresh.css")
        self.assertIn('class="section grace-section"', detail)
        self.assertIn('class="grace-emblem" aria-hidden="true"', detail)
        self.assertIn("8th recorded bearer", detail)
        self.assertIn("page-detail.route-characters-faaram main.page > .grace-section > .overlord-grace-card", styles)
        self.assertIn("animation: graceOrbit 36s linear infinite", styles)
        self.assertIn("@media (prefers-reduced-motion: reduce)", styles)

    def test_hero_art_uses_uncropped_source_ratio(self) -> None:
        styles = page("assets/archive-record-refresh.css")
        self.assertIn("aspect-ratio: var(--portrait-ratio, 2 / 3)", styles)
        self.assertIn("background-size: cover, contain", styles)
        self.assertIn('images/astera-zenith-cosmic-ruins.png', styles)
        self.assertNotIn('images/astera-zenith.png', styles)
        self.assertTrue((ROOT / "assets/images/astera-zenith-cosmic-ruins.png").is_file())
        for name in ("guts", "jonathan", "obama"):
            self.assertIn(f"body.route-characters-{name} {{ --portrait-ratio:", styles)

    def test_jonathan_landscape_portrait_keeps_full_art_without_letterbox(self) -> None:
        detail = page("characters/jonathan.html")
        styles = page("assets/archive-record-refresh.css")
        self.assertIn('archive-record-refresh.css?v=20261008-jonathan2', detail)
        self.assertIn("route-characters-jonathan .record-hero {\n    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)", styles)
        self.assertIn("background-size: cover, contain, cover", styles)


if __name__ == "__main__":
    unittest.main()
