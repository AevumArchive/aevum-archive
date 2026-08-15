# Aevum Archive Ornament Generation Brief

This file is the production brief for the next ornament batch. The website already contains reusable rails, dividers, seals and markers. New images should fill the named slots below instead of replacing portraits, profile icons or readable UI.

## Visual contract

- Dark fantasy archive: carved obsidian, restrained violet/pink magic and selective antique gold.
- One isolated ornament per transparent PNG. No scene backgrounds, text, letters, numbers, portraits or UI screenshots.
- Export at full visual strength. Do not bake in ghost-like transparency; CSS controls final opacity.
- Keep the center or text-facing edge quiet. Fine silhouettes are welcome, but never cover headings or controls.
- Use symmetry for dividers and seals. Use directional light only for explicitly left/right corner pairs.
- Gold marks prestige, ranks, relics and achievements. Violet marks archive/lore/characters. Crimson is reserved for world events and danger.
- Character profile icons stay icons. Portrait artwork belongs only in existing portrait slots.

## File contract

Naming: `ui_[scope]_[area]_[object]_[variant].png`

Canvas presets:

- Hero ornament: 1400 x 420 px
- Long divider: 1400 x 160 px
- Micro divider: 720 x 140 px
- Vertical edge rail: 180 x 1400 px
- Corner: 512 x 512 px
- Seal/marker: 512 x 512 px
- Timeline spine: 240 x 1400 px

All files must be transparent PNGs, sRGB, tightly cropped without clipping glow. Keep at least 32 px transparent safety margin; 64 px for glowing assets.

## Generation queue

### Global shell

1. `ui_global_navigation_archive_crest_compact.png` — compact archive crest for navigation; violet core, thin gold rim.
2. `ui_global_footer_archive_chain_divider.png` — quiet horizontal chain-and-rune divider.
3. `ui_global_section_corner_left_violet.png` — inward-facing violet section corner.
4. `ui_global_section_corner_right_violet.png` — mirrored companion, generated as its own correctly lit asset.
5. `ui_global_empty_state_archive_lock.png` — compact lock/sigil for empty states.
6. `ui_global_status_active_marker.png` — living/active status, violet-pink pulse.
7. `ui_global_status_sealed_marker.png` — closed seal with chain notch.
8. `ui_global_status_fallen_marker.png` — compact extinguished flame, not a large death portrait.
9. `ui_global_status_retired_marker.png` — quiet archived scroll marker.

### Route identities

10. `ui_404_broken_archive_sigil.png` — fractured but elegant archive seal.
11. `ui_achievements_trophy_shelf_gold.png` — horizontal gold shelf with restrained laurels.
12. `ui_characters_roster_header_divider.png` — violet roster divider with small central gem.
13. `ui_characters_bonds_knot_divider.png` — linked magical knot for Bonds.
14. `ui_characters_record_footer_violet.png` — slim record-ending flourish; never a portrait frame.
15. `ui_downloads_bundle_scroll_frame.png` — compact scroll corners framing download bundle metadata.
16. `ui_events_chronicle_edge_crimson.png` — slim crimson chronicle rail.
17. `ui_leaderboard_crown_header_gold.png` — wide, low crown-and-ledger flourish with a clear empty center.
18. `ui_leaderboard_rank_slot_corner_gold.png` — tiny gold rank-slot corner, usable on all ten empty seats.
19. `ui_lore_atlas_header_compass.png` — violet compass/astrolabe header.
20. `ui_lore_kingdom_crown_divider.png` — low heraldic crown divider.
21. `ui_lore_location_compass_seal.png` — compact location seal.
22. `ui_lore_noble_house_banner_divider.png` — folded banner divider with empty central field.
23. `ui_lore_settlement_marker.png` — lantern/town marker seal.
24. `ui_npcs_ledger_header_seal.png` — witness-ledger seal distinct from character roster.
25. `ui_npcs_record_footer_violet.png` — slim NPC record-ending flourish.
26. `ui_playthroughs_timeline_spine_violet.png` — vertical timeline spine with spaced rune nodes.
27. `ui_playthroughs_ended_thread_marker.png` — cut-thread seal for ended roads.
28. `ui_relics_vault_header_orb.png` — gold/violet vault-orb focal ornament.
29. `ui_relics_item_separator_gold.png` — narrow relic-card separator.
30. `ui_sealed_records_lock_chain_corner.png` — compact lock and chain corner.
31. `ui_world_events_anchor_ring.png` — crimson-violet event anchor ring.

### Optional homepage additions

The homepage layout is intentionally unchanged. Only generate these when new homepage controls are ready:

32. `ui_home_portal_corner_left.png`
33. `ui_home_portal_corner_right.png`

They should frame the portal area from outside, leaving the archive title, subtitle and future two-button space completely clear.

## Placement rules

- One focal ornament per hero, one divider per major transition, and no more than two edge accents in a viewport.
- Never layer two detailed ornaments on the same axis.
- Use rank-slot corners only on the empty leaderboard seats; Roman numerals remain HTML text.
- Use state markers at 28–44 CSS px. Locked, sealed, fallen and retired states must stay compact.
- Mobile layouts drop edge rails first, then corners; seals and micro dividers remain.
- Every decorative image gets empty alt text and `aria-hidden="true"` when placed in HTML.
