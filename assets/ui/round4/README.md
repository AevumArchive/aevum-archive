# Round 4 UI asset integration

Source: C:/Users/Yonk/Desktop/aevum_archive_ui_assets_round_4_full.zip
Integrated: 2026-08-17

## Summary

- 40 transparent PNG assets imported.
- 34 assets are referenced by the live Round 4 CSS or leaderboard markup.
- 6 generic or redundant variants are retained for later placement.
- No portraits or profile icons were replaced.
- No player-facing text or admin/GM guidance was added.
- Raster assets preserve their source aspect ratios. Detailed jewels, circles and corner geometry are not stretched.

## Live groups

- Global: brand medallion, navigation endcaps, section dividers, footer rule and empty-state seal.
- Home: archive-door crest, portal halo, gate corners, shelf pins and soft-gate keyline.
- 404: lost-page sigil and return thread.
- Characters: roster crest, profile-card corners, profile-slot backplate, Active/Sealed/Fallen/Retired status corners, state edges and state knots.
- Bonds: oracle crest.
- Achievements: two crossed chain strips, keyhole clasp and wax seal above locked-card surfaces while HTML text remains above them.
- Leaderboard: crown, divider and compact empty-state seal.

## Reserved for later

- ui_corner_compass_violet_gothic.png
- ui_divider_moonhalo_amethyst.png
- ui_emblem_last_ember_ruby_core.png
- ui_global_page_corner_whisper_160.png
- ui_locked_chain_endcap_violet.png
- ui_oracle_crest_amethyst_moon.png

These are intentionally not forced into unsuitable slots. They can be assigned when the later asset rounds complete the remaining route families.

## Technical note

Several filenames describe intended production slots, but the delivered canvases use generator sizes such as 1254 x 1254, 2172 x 724 and 724 x 2172. CSS therefore renders each file proportionally with contain-style sizing. Flexible frame geometry remains CSS/segmented; no full raster frame is stretched over a variable card.
