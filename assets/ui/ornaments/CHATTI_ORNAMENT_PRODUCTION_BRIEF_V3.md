# Aevum Archive - Chatti Ornament Production Brief v3

Version: 2026-08-17
Measured basis: effective HTML/CSS and DOM inventory across all 46 routes at 100% browser zoom.
Purpose: exact production dimensions, safe zones, naming, placement and art direction for a large ornament library.

## 1. Why the current frame looked stretched

The supplied sealed and fallen PNGs are 2057 x 764 px (2.692:1). Live status cards range from about 2.04:1 to 2.59:1. Scaling a complete frame to every card deforms circles, gems, corners and line weight.

Never ship a flexible card frame as one raster image. Use four fixed corners plus repeatable straight horizontal/vertical edges, or a true nine-slice asset. Only straight, texture-light sections may tile. Gems, seals, circles and corners must never stretch.

The live v3 frame is responsive CSS, so it has no stretched raster pixels. New raster modules can replace its individual corners/edges later without changing layout.

## 2. Non-negotiable rules

- Never replace profile icons or portrait-rune symbols with portraits.
- Portrait art belongs only in portrait-slot, artwork-slot, duality-art, sigil-stage, relic-image or inline-artwork.
- Never show admin, GM, setup or spoiler instructions on player pages.
- No text, names, Roman numerals, labels or fake UI inside ornament files.
- Transparent PNG or lossless WebP only. A visible checkerboard is an automatic rejection.
- Preserve the center of every card and hero for HTML text.
- Export at 3x intended CSS size unless a master size is specified below.
- Export at natural opacity; CSS controls final opacity.
- One ornament per file; lowercase snake_case filenames.
- Produce many assets, but display at most one hero crest, one divider and one card-family accent per viewport.

## 3. Global page geometry

Page width above 640 px: min(1180 px, viewport - 32 px).
Page width at or below 640 px: viewport - 22 px.

| Viewport | Page | Side gutter |
|---:|---:|---:|
| 1440 | 1180 | 130 |
| 1280 | 1180 | 50 |
| 1024 | 992 | 16 |
| 980 | 948 | 16 |
| 768 | 736 | 16 |
| 640 | 618 | 11 |
| 390 | 368 | 11 |
| 360 | 338 | 11 |

Global spacing:
- Page top: 28 desktop, 12 mobile.
- Page bottom: 56.
- Effective header: 14 top, 16 bottom.
- Navigation gap: 10.
- Hero padding: 34 desktop, 22 mobile.
- Hero column gap: 28.
- Section top margin: 46.
- Section heading bottom margin: 18.
- Standard grid gap: 16.
- Standard card padding: 22.
- Record/download panel padding: 26.
- Character body padding: 18.
- Footer top margin: 56; footer top padding: 24.

Global radii:
- Hero: 32 desktop, 24 mobile.
- Hero inner keyline: 24.
- Standard card: 24.
- Archive card: 26.
- Status v3 outer frame: 27 desktop, 25 mobile.
- Status inner panel: 19.

## 4. Responsive card widths

Formula: card = (page width - gap x (columns - 1)) / columns.

| Layout | shell 1180 | shell 992 | shell 948 | shell 736 | shell 618 | shell 368 | shell 338 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2 columns | 582 | 488 | 466 | 360 | 301 | 368 | 338 |
| 3 columns | 382.67 | 480 at 2-col | 466 at 2-col | 360 at 2-col | 301 at 2-col | 368 | 338 |
| 4 columns | 283 | 488 at 2-col | 466 at 2-col | 360 at 2-col | 301 at 2-col | 368 | 338 |
| 5 columns | 223.2 | 488 at 2-col | 466 at 2-col | 360 at 2-col | 301 at 2-col | 368 | 338 |

Breakpoints:
- At 980 and below: standard grids and status grids become 2 columns; hero/record-hero become 1 column.
- At 640 and below: grids become 1 column.
- Leaderboard and old-name grids: 5 -> 2 -> 1.

## 5. DOM component inventory

| Component | Count | Geometry / safe zone |
|---|---:|---|
| hero | 27 | full shell, padding 34/22 |
| archive-card | 26 | min-height 360; compact 300; padding 26 |
| section | 94 | top margin 46 |
| section-head | 26 | bottom 18; gap 16 |
| card | 153 | padding 22; radius 24 |
| character-card | 23 | 5/2/1; profile icon untouched |
| portrait-slot | 20 | min-height 220/180; padding 18 |
| portrait-rune | 20 | fixed 112 x 112; never replace |
| status-card | 17 | 3/2/1; min-height 180 |
| achievement-lock | 24 | 4/2/1; min-height 150; padding 18 |
| trophy-card | 2 | standard card |
| constellation-card | 4 | background lines max 12% opacity |
| realm-card | 18 | corner motif max 76 CSS px |
| npc-card | 12 | 3/2/1; no portraits |
| record-hero | 18 | 0.9fr/1.1fr then 1fr; gap 24 |
| record-panel | 18 | padding 26 |
| download-panel | 2 | padding 26 |
| sealed-record-card | 12 | corner seal max 72 CSS px |
| relic-card | 5 | art only inside relic-image |
| gate-card | 6 | 3/2/1; min-height 178 |
| leaderboard-board | 1 | full shell; inner inset 15 |
| leaderboard-slot | 10 | 5/2/1; min-height 112; numerals stay HTML |

Other fixed slots:
- relic-image: 210 desktop, 180 mobile, compact 170.
- duality-art: min-height 330.
- sigil-stage: min-height 330.
- sealed-portrait-frame: min-height 360, padding 34.
- footer: margin 56, padding 24.

## 6. Exact state-frame production spec

Live status widths by target viewport: 382.67, 480, 466, 360, 301, 368 and 338 px.
Minimum height: 180 px; content may increase height.

Segmented master assets:
- Corner: 384 x 384 transparent; render 42-56 square.
- Horizontal edge: 1536 x 96; render 32 high; middle 80% seamless.
- Vertical edge: 96 x 768; render 32 wide; middle 80% seamless.
- Center medallion: 192 x 192; render 14-20.
- Badge halo: 288 x 144; render 72 x 36 behind the HTML badge.
- Transparent bleed: 24 around corner masters.
- Maximum intrusion into text-safe zone: 18.
- At 360 viewport, status text-safe width is 294.
- At desktop, status text-safe width is 334.67.
- Keep top-left ornate mass out of x=18-148 and y=16-58 relative to the card because the HTML state badge lives there.

Current live v3 geometry:
- Outer frame extension: 8 top/bottom and 5 left/right.
- Mobile extension: 7 top/bottom and 4 left/right.
- Inner panel inset: 7 vertical, 5 horizontal.
- Center diamonds: 11 x 11 with 1 px keyline.
- Corner markers: centered 13 from each edge.
- Layer order: text 3, frame 2, panel 1.

State palettes:
- Sealed: amethyst, smoked silver, restrained magenta, tiny antique gold.
- Fallen: blackened iron, oxblood, ruby ember, restrained bronze; memorial, not gore.
- Retired: aged brass, smoke-gray parchment, quiet amber.
- Locked: violet wax, muted chain steel; chains never cross text.
- Active: archive green, pale silver, minimal life rune.

## 7. Full ornament production queue

Global:
- ui_global_header_brand_medallion_048
- ui_global_nav_endcap_left_032
- ui_global_nav_endcap_right_032
- ui_global_section_divider_center_640x072
- ui_global_section_knot_064
- ui_global_footer_rule_1180x048
- ui_global_mobile_divider_338x048
- ui_global_page_corner_whisper_160
- ui_global_empty_state_seal_128

Home and 404:
- ui_home_archive_door_crest_720x180
- ui_home_gate_card_corner_192
- ui_home_primary_portal_halo_480x160
- ui_home_shelf_link_pin_064
- ui_home_soft_gate_keyline_582x178
- ui_404_lost_page_sigil_256
- ui_404_return_thread_480x064

Characters and bonds:
- ui_characters_roster_crest_720x160
- ui_characters_profile_card_corner_192
- ui_characters_profile_slot_backplate_336
- ui_characters_state_sealed_corner_384
- ui_characters_state_sealed_edge_h_1536x096
- ui_characters_state_sealed_edge_v_096x768
- ui_characters_state_sealed_medallion_192
- ui_characters_state_fallen_corner_384
- ui_characters_state_fallen_edge_h_1536x096
- ui_characters_state_fallen_edge_v_096x768
- ui_characters_state_fallen_medallion_192
- ui_characters_state_retired_corner_384
- ui_characters_state_active_corner_384
- ui_characters_bonds_constellation_node_096
- ui_characters_bonds_constellation_thread_768x064
- ui_characters_bonds_oracle_crest_256
- ui_characters_record_hero_corner_256
- ui_characters_record_panel_bookmark_096
- ui_characters_portrait_slot_frame_768x768
- ui_characters_reward_frame_reserved_768

Achievements and leaderboard:
- ui_achievements_hero_trophy_256
- ui_achievements_trophy_card_corner_192
- ui_achievements_locked_corner_384
- ui_achievements_locked_chain_h_1536x096
- ui_achievements_locked_wax_seal_192
- ui_achievements_earned_medal_backplate_256
- ui_leaderboard_hero_crown_256
- ui_leaderboard_gold_divider_768x096
- ui_leaderboard_board_corner_384
- ui_leaderboard_slot_first_384x192
- ui_leaderboard_slot_standard_384x192
- ui_leaderboard_sync_seal_192
- ui_leaderboard_empty_champion_mark_096
- ui_leaderboard_rank_flourish_128

Lore:
- ui_lore_archive_crest_720x160
- ui_lore_kingdom_crown_corner_192
- ui_lore_settlement_belltower_corner_192
- ui_lore_house_heraldry_corner_192
- ui_lore_warfront_spear_corner_192
- ui_lore_location_compass_corner_192
- ui_lore_sealed_crown_wax_192
- ui_lore_avalon_gate_divider_640x072
- ui_lore_neris_village_divider_640x072
- ui_lore_house_zenith_star_divider_640x072
- ui_lore_crownbridge_thread_768x064
- ui_lore_sunken_bell_wave_768x064
- ui_lore_record_page_bookmark_096
- ui_lore_unknown_record_veil_512x256

NPCs:
- ui_npcs_ledger_crest_720x160
- ui_npcs_current_card_corner_192
- ui_npcs_older_card_corner_192
- ui_npcs_sealed_portrait_corner_384
- ui_npcs_bond_marker_096
- ui_npcs_instructor_marker_096
- ui_npcs_enemy_marker_096
- ui_npcs_world_figure_marker_096
- ui_npcs_record_hero_corner_256
- ui_npcs_record_panel_bookmark_096
- ui_npcs_ichiro_memorial_seal_192
- ui_npcs_empty_portrait_backplate_512

Playthroughs, events and sealed records:
- ui_playthroughs_archive_crest_720x160
- ui_playthroughs_road_thread_1024x064
- ui_playthroughs_campaign_corner_256
- ui_playthroughs_sealed_road_wax_192
- ui_playthroughs_old_name_marker_096
- ui_events_chronicle_crest_720x160
- ui_events_chronicle_card_corner_192
- ui_world_event_anchor_crest_256
- ui_world_event_timer_bracket_512x192
- ui_world_event_active_corner_256
- ui_world_event_fault_thread_768x064
- ui_sealed_records_vault_crest_720x160
- ui_sealed_records_card_corner_256
- ui_sealed_records_wax_medallion_192
- ui_sealed_records_empty_shelf_512x192

Relics and downloads:
- ui_relics_vault_crest_720x160
- ui_relics_card_corner_192
- ui_relics_chain_corner_192
- ui_relics_legendary_corner_256
- ui_relics_image_vignette_768x256
- ui_relics_unknown_item_veil_512x256
- ui_downloads_archive_crest_720x160
- ui_downloads_entering_divider_640x072
- ui_downloads_package_corner_256
- ui_downloads_feature_marker_096
- ui_downloads_install_seal_192
- ui_downloads_checksum_thread_768x064

## 8. Route coverage

All 46 HTML routes are covered: root/404, achievements, 15 character pages plus roster/status/bonds, downloads, events, leaderboard, lore root and all kingdom/location/house/settlement pages, NPC root and all NPC records, playthrough root and Aizen Ended Road, sealed records, top characters, world events and world items.

Every placement must be checked at 1440, 1024, 768, 390 and 360 px. Desktop-only fit is rejected.

## 9. Copy-paste generation prompt

Create one isolated Aevum Archive website ornament named [FILENAME]. It belongs to [ROUTE/COMPONENT]. Export exactly [MASTER WIDTH] x [MASTER HEIGHT] pixels as a genuine transparent PNG. It renders at [CSS WIDTH] x [CSS HEIGHT]. Preserve [SAFE ZONE]. Use restrained archival gothic filigree, dark violet-to-pink identity, state accent [ACCENT], engraved edges and premium material separation. No text, letters, numerals, portrait, profile icon, UI screenshot, opaque background, checkerboard, fog over the safe zone or decoration touching the canvas edge. Straight edge tile regions must be seamless. Circles, gems, seals and corners must remain outside every stretch/tile region.

Negative prompt:
cheap mobile-game frame, oversized baroque decoration, plastic bevel, blurry glow, baked checkerboard, opaque rectangle, fake text, portrait, face, profile icon, skull gore, busy center, asymmetric crop, perspective mockup, stretched jewel, JPEG artifacts, watermark

## 10. Export validation

Reject if any answer is no:
1. Real alpha channel?
2. Outermost 12-24 px transparent?
3. Center safe zone at least 92% transparent?
4. Important circles/gems outside stretch/tile areas?
5. Sharp at CSS render size?
6. Works over #08070d and rgba(24,20,36,.78)?
7. Does not cover icons or portrait slots?
8. Legible at 360 viewport?
9. Exact lowercase filename?
10. One ornament, not a mockup/sheet?

## 11. Production order

Phase A: five state corner sets, sealed/fallen edges, global dividers, hero crest family, leaderboard gold family.
Phase B: lore category corners, NPC markers, playthrough road, world-event anchor/timer, relic/download families.
Phase C: bookmarks, knots, empty-state seals and hover accents. Character reward frames remain reserved until reward rules exist.
