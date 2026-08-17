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
- Locked: violet wax and muted chain steel; chains visibly cross the card surface below live HTML text.
- Active: archive green, pale silver, minimal life rune.

### 6.1 Premium Sealed set - Moonveil Covenant

This is the preferred ornate Sealed family. It must feel magical and expensive without returning to a stretched full-card picture frame.

- ui_characters_state_sealed_moonveil_corner_384: fixed corner with smoked-silver crescent filigree, dark amethyst enamel and one 6-10 px rendered magenta crystal.
- ui_characters_state_sealed_moonveil_edge_h_1536x096: perfectly tileable horizontal silver thread with sparse violet enamel; render 24-32 px high.
- ui_characters_state_sealed_moonveil_edge_v_096x768: matching vertical thread; render 24-32 px wide.
- ui_characters_state_sealed_moonveil_knot_192: symmetrical covenant diamond for top and bottom center; render 16-20 px.
- ui_characters_state_sealed_moonveil_badge_halo_288x144: faint crescent halo behind the HTML SEALED badge; render 72 x 36 px.
- ui_characters_state_sealed_moonveil_veil_512x192: optional corner mist, maximum runtime opacity 0.10; never behind text.

Layer order: card panel 1, edge/corner art 2, live badge/title/body 3. Corner art may extend 8 px outside the card and at most 16 px inward. The middle 70% of the card stays visually quiet.

Moonveil prompt:
Create one isolated responsive Aevum Archive SEALED ornament named [FILENAME], exact size [SIZE], genuine transparent PNG. Refined smoked-silver lunar filigree, dark amethyst enamel, one restrained magenta crystal and tiny antique-gold micro accents. Premium occult archive covenant, elegant and sharp, with clean tile boundaries where requested. No complete card frame, no text, no portrait, no checkerboard, no opaque background, no large glow and no decoration in the central text-safe zone.

### 6.2 Premium Fallen set - Last Ember Memorial

This is the preferred ornate Fallen family. It should read as a dignified memorial, not horror decoration.

- ui_characters_state_fallen_last_ember_corner_384: blackened-iron memorial corner with oxblood enamel and one restrained ruby ember.
- ui_characters_state_fallen_last_ember_edge_h_1536x096: tileable dark iron thread with sparse ember cracks; render 24-32 px high.
- ui_characters_state_fallen_last_ember_edge_v_096x768: matching vertical thread; render 24-32 px wide.
- ui_characters_state_fallen_last_ember_knot_192: symmetrical dying-ember diamond for top and bottom center; render 16-20 px.
- ui_characters_state_fallen_last_ember_badge_halo_288x144: muted red memorial halo behind the HTML DEAD badge; render 72 x 36 px.
- ui_characters_state_fallen_last_ember_ash_thread_768x064: optional sparse ash line for the Fallen section heading; render up to 384 x 32 px.

Layer order and safe zones are identical to Moonveil. No skulls, bones, gore, roses, giant flames or bright red plastic bevels. The ember is a focal point, not a floodlight.

Last Ember prompt:
Create one isolated responsive Aevum Archive FALLEN memorial ornament named [FILENAME], exact size [SIZE], genuine transparent PNG. Crisp blackened iron, deep oxblood enamel, one restrained ruby ember and subtle antique-bronze engraving. Somber, dignified and expensive. No complete card frame, no gore, skulls, bones, roses, text, portrait, checkerboard, opaque background, blurry glow or decoration in the central text-safe zone.

### 6.3 Locked achievements - crossed chain overlay

Locked achievement cards are 283 px wide on the 1180 px desktop shell, 236 px at a 1024 px viewport, 466 px at 980 px, 360 px at 768 px, 618 px at 640 px, 368 px at 390 px and 338 px at 360 px. Minimum card height is 150 px and content padding is 18 px.

The chains must visibly lie over the card surface. Use seamless chain modules instead of stretching a complete chain image:

- ui_achievements_locked_chain_tile_256x096: one seamless run of 2-3 muted steel links; repeat along both diagonal strips; render each tile about 96 x 36 px.
- ui_achievements_locked_chain_endcap_192: one ornate archive anchor that can be mirrored at strip ends; render 38-46 px.
- ui_achievements_locked_chain_crossing_clasp_192: central violet-metal clasp at the chain crossing; render 34-42 px.
- ui_achievements_locked_wax_seal_192: violet wax archive seal attached near the crossing; render 42-52 px.
- ui_achievements_locked_corner_384: restrained locked-card corner, render 38-48 px.
- ui_achievements_locked_chain_shadow_512x128: soft contact shadow below a chain strip, runtime opacity 0.16-0.24.

Placement:
- Chain A crosses from x=-24, y=38 to x=card width+24, y=112; rotate approximately +9 degrees.
- Chain B crosses from x=-24, y=112 to x=card width+24, y=38; rotate approximately -9 degrees.
- Each strip is 36-42 px high and extends 24 px beyond both card sides.
- Render chains above the card panel at layer 2 and live HTML text at layer 3. The chains are visibly on top of the card but cannot make the title unreadable.
- Put the clasp close to 50%/50%. Keep the wax seal 14-24 px away from the exact text center.
- At mobile widths reduce chain-strip height to 32-36 px and the clasp to 32-36 px. Never scale link circles non-uniformly.
- Normal opacity: 0.58-0.72. Hover opacity: maximum 0.82. Contact shadows remain below 0.24.

Locked-chain prompt:
Create one isolated Aevum Archive LOCKED ACHIEVEMENT chain module named [FILENAME], exact size [SIZE], genuine transparent PNG. Heavy but refined medieval archive chain in muted gunmetal steel with tiny violet enamel accents, crisp individual links, believable overlap and restrained wear. The module must tile seamlessly where requested and look like it lies physically over a dark violet card. No card background, no text, no padlock emoji, no checkerboard, no opaque rectangle, no giant glow, no rust-orange color and no blurry links.

## 6.4 OBAMA portrait border - New Order Mandate

This border is only for the explicit portrait slot on characters/obama.html. It must never replace or cover a profile icon.

Measured sources:
- OBAMA portrait: 1024 x 1536 px, exact 2:3 aspect.
- Current New Order frame: 1600 x 2100 px, aspect 0.7619; it is too wide for the live portrait container and should be replaced.
- Portrait-card padding: 28 px.
- Portrait wrapper maximum width: 820 px.
- Wrapper frame padding above 760 px: vertical clamp(22.4 px, 3.2vw, 48 px), horizontal clamp(24 px, 3.6vw, 54.4 px).
- At 760 px and below the effective wrapper padding is 16 px on every side.
- The portrait image also has max-height: 86vh. Actual outer height is min(1.5 x inner portrait width, 0.86 x viewport height) + twice the effective vertical padding.
- Because viewport height can cap the portrait, the new border must be true nine-slice/segmented artwork. A rigid one-piece bitmap is not acceptable even at the 1380 x 2000 master ratio.

Measured live outer wrapper sizes before the 86vh image-height cap:
| Viewport | Uncapped outer portrait-border slot | Approximate inner portrait width |
|---:|---:|---:|
| 1440 | 820 x 1166.6 | 716.3 |
| 1280 | 820 x 1173.7 | 727.8 |
| 1024 | 820 x 1184.9 | 746.3 |
| 980 | 820 x 1186.9 | 749.4 |
| 768 | 680 x 986.2 | 624.7 |
| 640 | 562 x 827 | 530 |
| 390 | 312 x 452 | 280 |
| 360 | 282 x 407 | 250 |

Required production asset:
- ui_characters_obama_portrait_border_new_order_1380x2000: genuine transparent PNG, designed as a nine-slice portrait border.
- Master canvas: 1380 x 2000 px, aspect 0.69.
- Exact transparent portrait opening: x=88 to 1292 and y=97 to 1903. Opening size 1204 x 1806, exact 2:3.
- Keep at least 24 px transparent bleed around the outer canvas.
- Nine-slice guide zones: fixed left/right corners inside x=0-160 and x=1220-1380; fixed top/bottom corners inside y=0-190 and y=1810-2000.
- Only straight, low-detail edge sections between those guides may stretch.
- Render over the wrapper at 100% width/height. Do not bake the portrait into this file.
- Keep the portrait opening at least 96% transparent. Inner shadow belongs in CSS, not in the PNG.
- Important gold circles, the Mandate crown and the Red Orb must sit in fixed corner/center modules, never in stretch zones.
- Recommended rendered decorative thickness: 28-42 px desktop and 18-26 px mobile.
- Layer order: wrapper background 1, portrait image 2, new border 3, optional tiny crest 4.

Art direction:
A sovereign New Order archive frame in antique imperial gold, dark obsidian iron and restrained oxblood enamel. Use disciplined geometric authority rather than soft floral fantasy. Include one small Mandate crown at top center and one subtle Red Orb clasp at bottom center. Corners may suggest rebuilt architecture and binding law. Premium, solemn and controlled; not a giant glowing throne.

OBAMA border prompt:
Create one isolated Aevum Archive portrait border named ui_characters_obama_portrait_border_new_order_1380x2000 at exactly 1380 x 2000 pixels as a genuine transparent PNG. The transparent inner opening must be exactly x=88..1292 and y=97..1903, size 1204 x 1806 in a perfect 2:3 ratio. Design a responsive nine-slice sovereign New Order border using antique imperial gold, obsidian iron, restrained oxblood enamel, one small Mandate crown at top center and one subtle Red Orb clasp at bottom center. Keep all jewels, circles, crown details and corner architecture outside stretch zones x=160..1220 and y=190..1810. Straight edge sections must be texture-light and stretch-safe. No portrait, face, profile icon, text, letters, opaque background, checkerboard, giant glow, floral vines, oversized wings, throne, watermark or decoration crossing the portrait opening.

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
- ui_characters_state_sealed_moonveil_corner_384
- ui_characters_state_sealed_moonveil_edge_h_1536x096
- ui_characters_state_sealed_moonveil_edge_v_096x768
- ui_characters_state_sealed_moonveil_knot_192
- ui_characters_state_sealed_moonveil_badge_halo_288x144
- ui_characters_state_sealed_moonveil_veil_512x192
- ui_characters_state_fallen_last_ember_corner_384
- ui_characters_state_fallen_last_ember_edge_h_1536x096
- ui_characters_state_fallen_last_ember_edge_v_096x768
- ui_characters_state_fallen_last_ember_knot_192
- ui_characters_state_fallen_last_ember_badge_halo_288x144
- ui_characters_state_fallen_last_ember_ash_thread_768x064
- ui_characters_bonds_constellation_node_096
- ui_characters_bonds_constellation_thread_768x064
- ui_characters_bonds_oracle_crest_256
- ui_characters_record_hero_corner_256
- ui_characters_record_panel_bookmark_096
- ui_characters_portrait_slot_frame_768x768
- ui_characters_reward_frame_reserved_768
- ui_characters_obama_portrait_border_new_order_1380x2000

Achievements and leaderboard:
- ui_achievements_hero_trophy_256
- ui_achievements_trophy_card_corner_192
- ui_achievements_locked_corner_384
- ui_achievements_locked_chain_h_1536x096
- ui_achievements_locked_wax_seal_192
- ui_achievements_locked_chain_tile_256x096
- ui_achievements_locked_chain_endcap_192
- ui_achievements_locked_chain_crossing_clasp_192
- ui_achievements_locked_chain_shadow_512x128
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
