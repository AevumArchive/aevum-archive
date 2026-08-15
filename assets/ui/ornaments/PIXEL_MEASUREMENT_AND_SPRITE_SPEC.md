# Aevum Archive — Pixel Measurement & Sprite Production Spec

Version: 2026-08-15  
Measured source: commit `c427318` plus the current CSS state  
Coverage: all 46 HTML files

## 1. Non-negotiable art rules

- Do not generate character portraits, profile pictures or replacements for `.portrait-rune` icons.
- Character icons remain HTML/CSS symbols. Decorative assets may frame cards, but must not occupy portrait or icon slots.
- Export one ornament per transparent PNG. No text, labels, Roman numerals or UI screenshots inside artwork.
- Export artwork at full opacity. Runtime CSS controls opacity.
- Do not make one large full-page frame. Use independent corners, edge tiles, seals and dividers.
- Never place decorative detail inside the text safe zone defined for a slot.
- Corners and borders must be designed for 9-slice/segmented composition so cards can grow vertically.

## 2. Measurement basis

These are CSS pixels at browser zoom 100%. The current shell is fluid, so a single full-card bitmap cannot fit every viewport without distortion.

The app browser could not start because the local Windows sandbox helper failed. Therefore the values below come from the effective CSS rules, the full 46-file DOM inventory and the supplied desktop screenshots. CSS-defined dimensions and formulas are exact; content-driven heights are marked as minimum or variable.

### Page shell

| Viewport | `.page` width | Left/right gutter | Page top padding |
|---:|---:|---:|---:|
| 1440 | 1180 | 130 | 28 |
| 1280 | 1180 | 50 | 28 |
| 1024 | 992 | 16 | 28 |
| 980 | 948 | 16 | 28 |
| 768 | 736 | 16 | 28 |
| 640 | 618 | 11 | 12 |
| 390 | 368 | 11 | 12 |
| 360 | 338 | 11 | 12 |

Formula: above 640 px, `min(1180px, viewport - 32px)`; at and below 640 px, `viewport - 22px`.

### Global spacing and radii

| Token | Desktop | Mobile ≤640 |
|---|---:|---:|
| Header top/bottom padding | 18 / 28 | unchanged |
| Hero padding | 34 | 22 |
| Hero outer radius | 32 | 24 |
| Hero inner line inset/radius | 14 / 24 | 14 / 24 |
| Hero column gap | 28 | stacked, 28 vertical |
| Normal section top margin | 46 | 46 |
| Section heading bottom margin | 18 | 18 |
| Standard grid gap | 16 | 16 |
| Standard card padding/radius | 22 / 24 | 22 / 24 |
| Record/download panel padding/radius | 26 / 24 | 26 / 24 |
| Footer margin/padding top | 56 / 24 | 56 / 24 |

## 3. Exact component boxes

### Heroes

At the 1180 px desktop shell, a normal hero has a 1110 px content box after border and padding. After the 28 px gap, the tracks are approximately 606 px and 476 px.

| Component | Desktop 1180 shell | Tablet ≤980 | Mobile 390 |
|---|---:|---:|---:|
| Normal hero | 1180 × variable | 948 × variable, stacked | 368 × variable, stacked |
| Compact hero aside | 476 × min 300 | 878 × min 300 | 322 × min 300 |
| Full hero aside | 476 × min 360 | 878 × min 360 | 322 × min 360 |
| Record hero tracks | 520 + 24 gap + 636 | one column, 948 | one column, 368 |
| Leaderboard desktop tracks | about 747 + 28 gap + 335 | one column | one column |

Do not generate a full hero overlay. Recommended hero art is a 64–96 px rendered corner or an 80–104 px seal placed in an intentionally empty corner.

### Standard grid widths

| Grid | Desktop shell 1180 | Tablet shell 948 | Tablet shell 736 | Mobile shell 368 |
|---|---:|---:|---:|---:|
| 2 columns | 582 | 466 | 360 | 368, one column |
| 3 columns | 382.7 | 466, two columns | 360, two columns | 368, one column |
| 4 columns | 283 | 466, two columns | 360, two columns | 368, one column |
| 5 character columns | 223.2 | 466, two columns | 360, two columns | 368, one column |

### Card families

| Slot | Width behavior | Height | Padding | Text safe zone |
|---|---|---:|---:|---|
| `.card` | grid width above | variable | 22 | 28 px from all edges; reserve 52 px top-right only if a marker is used |
| `.status-card` | 382.7 / 466 / 360 / 368 | min 180 | 22 | x 22…width-22; y 18…height-18; state seal max 36 px at top-right |
| `.npc-card` | 382.7 / 466 / 360 / 368 | min 245 | 22 | x 22…width-22; no full overlay |
| `.realm-card` | 382.7 / 466 / 360 / 368 | min 210 | 22 | x 22…width-22; bottom ornament max 32 px high |
| `.achievement-lock` desktop | 274.5 | min 150 | 18 | x 20…width-20; y 18…height-18 |
| `.achievement-lock` tablet 980 | 455 | min 150 | 18 | same 20 px edge clearance |
| `.achievement-lock` tablet 768 | 349 | min 150 | 18 | same 20 px edge clearance |
| `.achievement-lock` mobile 390 | 364 | min 150 | 18 | same 20 px edge clearance |
| `.trophy-card` | 582 / 466 / 360 / 368 | variable | 24 | left 116 px reserved for 84 px seal on desktop |
| `.constellation-card` | 582 desktop | min 310 | 24 | use background motes only; no enclosing bitmap |
| `.campaign-block` | 1180 / fluid | variable | 22 | use a 72 px corner or 48 px seal only |
| `.download-panel` | 582 desktop | min 250 for feature | 26 | x 26…width-26 |
| `.relic-card` | 382.7 desktop | variable | 22 | artwork slot is separate; ornament max 40 px at card edge |
| `.leaderboard rank slot` | 212 desktop | min 112 | internal centering | Roman numeral remains HTML; corners max 24 px |

### Achievement grid calculation

The grid has 8 px left/right padding and 22 px gaps. At 1180 px: `(1180 - 16 - 66) / 4 = 274.5 px`. At 948 px: `(948 - 16 - 22) / 2 = 455 px`. At mobile the padding becomes 2 px each.

### Character icon slots — do not generate for these

| Slot | Desktop | Mobile |
|---|---:|---:|
| Character index card width | 223.2 | 368 |
| `.portrait-slot` minimum height | 220 | 180 |
| `.portrait-rune` icon | 112 × 112 | 112 × 112 |

These are intentionally symbolic profile icons. No sprite in this production batch may replace or cover them.

## 4. Supplied ZIP audit

All three supplied PNGs use a 2057 × 764 RGBA canvas.

| File | Alpha bounds | Center-zone occupancy | Decision |
|---|---|---:|---|
| `ui_characters_card_frame_sealed_horizontal.png` | x 10–2047, y 0–763 | 6.3% | Composition is usable, but aspect ratio 2.69 does not match 2.13 desktop status cards. Slice into corners/edges or regenerate segmented. |
| `ui_characters_card_frame_dead_fallen_horizontal.png` | full canvas | 8.6% | Same aspect mismatch. Slice/regenerate; do not stretch. |
| `ui_achievements_overlay_locked_cross_chains_horizontal.png` | full canvas | 58.4%, mean alpha 130/255 | Reject as a foreground overlay. It will cover the title and copy. Regenerate as edge chains plus a separate lock seal. |

Target desktop status card including a 7 px decorative bleed is approximately 397 × 194 CSS px. A direct 3× fixed master would be about 1191 × 582, but segmented assets are preferred because tablet cards become 466 px wide.

## 5. Required master presets

| Preset | Master canvas | Intended rendered size | Transparent safe margin |
|---|---:|---:|---:|
| Compact seal | 512 × 512 | 80–104 × 80–104 | 48 master px |
| Tiny marker | 256 × 256 | 24–40 × 24–40 | 32 master px |
| Hero corner | 512 × 512 | 64–96 × 64–96 | 48 master px |
| Micro divider | 1080 × 108 | 300–360 × 30–36 | 36 master px top/bottom |
| Major divider | 1800 × 180 | max 600 × 60, once per landing page | 54 master px top/bottom |
| Horizontal edge tile | 768 × 72 | 256 × 24 | design must tile or stretch only through center 50% |
| Vertical edge tile | 72 × 576 | 24 × 192 | design must tile or stretch only through center 50% |
| Frame corner | 256 × 256 | 32–40 × 32–40 | 24 master px |
| Standalone lock/state seal | 320 × 320 | 36–44 × 36–44 | 32 master px |

Do not generate another 2057 × 764 one-piece frame unless it targets one fixed, non-responsive slot.

## 6. Segmented state-frame sets

Each state set should contain independent pieces. The center remains fully transparent.

### Sealed character set

- `ui_characters_state_sealed_corner_tl.png` — 256 × 256
- `ui_characters_state_sealed_corner_tr.png` — 256 × 256
- `ui_characters_state_sealed_corner_bl.png` — 256 × 256
- `ui_characters_state_sealed_corner_br.png` — 256 × 256
- `ui_characters_state_sealed_edge_horizontal.png` — 768 × 72
- `ui_characters_state_sealed_edge_vertical.png` — 72 × 576
- `ui_characters_state_sealed_lock_seal.png` — 320 × 320

Violet archive metal, restrained chains, closed seal. Rendered corner 36 px; seal 36 px. No detail beyond 44 rendered px from the edge.

### Dead/fallen character set

- `ui_characters_state_fallen_corner_tl.png`
- `ui_characters_state_fallen_corner_tr.png`
- `ui_characters_state_fallen_corner_bl.png`
- `ui_characters_state_fallen_corner_br.png`
- `ui_characters_state_fallen_edge_horizontal.png`
- `ui_characters_state_fallen_edge_vertical.png`
- `ui_characters_state_fallen_extinguished_flame.png`

Crimson-black iron, one extinguished ember, no gore and no portrait imagery.

### Retired character set

- `ui_characters_state_retired_corner_tl.png`
- `ui_characters_state_retired_corner_tr.png`
- `ui_characters_state_retired_corner_bl.png`
- `ui_characters_state_retired_corner_br.png`
- `ui_characters_state_retired_edge_horizontal.png`
- `ui_characters_state_retired_edge_vertical.png`
- `ui_characters_state_retired_scroll_seal.png`

Muted antique gold and dark parchment, quiet rather than dead.

### Locked achievement set

- `ui_achievements_locked_chain_corner_tl.png`
- `ui_achievements_locked_chain_corner_tr.png`
- `ui_achievements_locked_chain_corner_bl.png`
- `ui_achievements_locked_chain_corner_br.png`
- `ui_achievements_locked_chain_edge_horizontal.png`
- `ui_achievements_locked_chain_edge_vertical.png`
- `ui_achievements_locked_lock_seal_center.png`

The lock seal renders at 40–44 px in the top-right reserved area. Chains stay within 24 rendered px of the border. Nothing crosses the center.

## 7. Additional useful sprites

### Global shell

- `ui_global_navigation_archive_crest_compact.png` — 256 × 256, render 48 × 48.
- `ui_global_section_divider_violet_micro.png` — 1080 × 108, render 360 × 36.
- `ui_global_section_divider_gold_micro.png` — 1080 × 108, render 360 × 36.
- `ui_global_section_divider_crimson_micro.png` — 1080 × 108, render 360 × 36.
- `ui_global_footer_archive_chain_micro.png` — 1080 × 108, render 300 × 30.
- `ui_global_empty_state_archive_lock.png` — 512 × 512, render 88 × 88.
- `ui_global_card_corner_violet.png` — 256 × 256, render 28 × 28.
- `ui_global_card_corner_gold.png` — 256 × 256, render 28 × 28.

### Achievements and leaderboard

- `ui_achievements_hero_trophy_seal_gold.png` — 512 × 512, render 96 × 96; replaces stacked ring plus HTML glyph.
- `ui_achievements_trophy_shelf_divider_gold.png` — 1080 × 108, render 360 × 36.
- `ui_leaderboard_hero_crown_ledger_seal.png` — 512 × 512, render 92 × 92; one symbol, not ring plus crown.
- `ui_leaderboard_header_crown_divider_gold.png` — 1080 × 108, render 360 × 36.
- `ui_leaderboard_rank_slot_corner_gold.png` — 256 × 256, render 22 × 22.
- `ui_leaderboard_sync_marker_gold.png` — 256 × 256, render 32 × 32.

### Lore, NPCs and events

- `ui_lore_atlas_hero_seal.png` — 512 × 512, render 96 × 96.
- `ui_lore_category_kingdom_crown.png` — 256 × 256, render 32 × 32.
- `ui_lore_category_settlement_lantern.png` — 256 × 256, render 32 × 32.
- `ui_lore_category_house_banner.png` — 256 × 256, render 32 × 32.
- `ui_lore_category_warfront_blades.png` — 256 × 256, render 32 × 32.
- `ui_lore_category_rumor_moon.png` — 256 × 256, render 32 × 32.
- `ui_npcs_ledger_hero_medallion.png` — 512 × 512, render 92 × 92; replaces the diamond glyph rather than layering under it.
- `ui_npcs_record_footer_violet.png` — 1080 × 108, render 300 × 30.
- `ui_events_chronicle_hero_flame_seal.png` — 512 × 512, render 92 × 92; one combined seal, no second floating flame.
- `ui_world_events_anchor_ring.png` — 512 × 512, render 104 × 104.
- `ui_events_fallen_corner_crimson.png` — 256 × 256, render 32 × 32.

### Playthroughs, relics, downloads and sealed records

- `ui_playthroughs_timeline_spine_violet.png` — 72 × 576, render 24 × 192, tile vertically.
- `ui_playthroughs_timeline_node_active.png` — 256 × 256, render 30 × 30.
- `ui_playthroughs_timeline_node_ended.png` — 256 × 256, render 30 × 30.
- `ui_playthroughs_ended_thread_seal.png` — 512 × 512, render 88 × 88.
- `ui_relics_vault_hero_orb.png` — 512 × 512, render 104 × 104.
- `ui_relics_item_corner_gold.png` — 256 × 256, render 30 × 30.
- `ui_relics_item_marker_lost.png` — 256 × 256, render 32 × 32.
- `ui_downloads_bundle_scroll_corner.png` — 256 × 256, render 36 × 36.
- `ui_downloads_archive_wax_seal.png` — 512 × 512, render 88 × 88.
- `ui_sealed_records_lock_chain_corner.png` — 256 × 256, render 36 × 36.
- `ui_404_broken_archive_sigil.png` — 512 × 512, render 104 × 104.

## 8. Route coverage — all HTML files

### Global only

- `/index.html` — homepage layout stays intact; optional external portal corners only.
- `/top-characters/index.html` — redirect page; no dedicated sprite.

### Achievements and leaderboard

- `/achievements/index.html` — trophy seal, shelf divider, locked segmented set.
- `/leaderboard/index.html` — crown-ledger seal, gold divider, rank-slot corners, sync marker.

### Character pages

- `/characters/index.html` — roster divider only; never decorate portrait/icon slots.
- `/characters/all.html` — sealed, fallen and retired segmented state sets.
- `/characters/bonds.html` — small knot divider; no character imagery.
- `/characters/astera-zenith.html`
- `/characters/faaram.html`
- `/characters/guts.html`
- `/characters/jango.html`
- `/characters/jawohl.html`
- `/characters/khealdur.html`
- `/characters/lythariel.html`
- `/characters/mortis.html`
- `/characters/obama.html`
- `/characters/raven.html`
- `/characters/tony.html`
- `/characters/william-carter.html`

Character detail pages receive only a micro footer/divider outside portrait and profile-icon slots.

### Lore pages

- `/lore/index.html`
- `/lore/kingdoms/index.html`
- `/lore/kingdoms/avalon.html`
- `/lore/kingdoms/unnamed-crown.html`
- `/lore/locations/index.html`
- `/lore/locations/crownbridge-front.html`
- `/lore/locations/sunken-bell-tower.html`
- `/lore/noble-houses/index.html`
- `/lore/noble-houses/heraldry.html`
- `/lore/noble-houses/house-zenith.html`
- `/lore/settlements/index.html`
- `/lore/settlements/neris.html`

Use one atlas seal per hero and 32 px category markers. Do not repeat large dividers between every card row.

### NPC pages

- `/npcs/index.html`
- `/npcs/ichiro.html`
- `/npcs/jiro.html`
- `/npcs/keanu.html`
- `/npcs/nox.html`
- `/npcs/nyx.html`
- `/npcs/rapax.html`

Use one ledger medallion on the index and micro record footers on detail pages. Existing portrait slots remain unchanged.

### Remaining routes

- `/events/index.html` — chronicle seal and crimson micro divider.
- `/world-events/index.html` — anchor ring and event corner.
- `/playthroughs/index.html` — timeline spine and nodes.
- `/playthroughs/aizen-ended-road.html` — ended-thread seal.
- `/world-items/index.html` — vault orb, item corners and lost marker.
- `/downloads/texture-pack.html` — scroll corners and wax seal.
- `/sealed-records/index.html` — lock-chain corners and empty-state lock.
- `/404.html` — broken archive sigil.

## 9. Copy/paste generation prompt

Create the requested Aevum Archive UI sprite as one isolated transparent PNG. Dark fantasy archive aesthetic: blackened metal, restrained violet-to-pink magic and selective antique gold. No text, letters, numerals, portraits, faces, screenshots or full background. Use the exact filename and canvas dimensions from this specification. Keep all important pixels inside the stated transparent safety margin. The center/text safe zone must remain fully transparent. Export at full strength without baked-in ghost transparency; CSS will control opacity. Corners and edges must connect cleanly with the other pieces in the same segmented set. Do not add extra objects.

## 10. Implementation note

Use seals as replacements for existing glyphs, never as a second layer beneath the glyph. Use segmented frames or CSS 9-slice for fluid cards. Large side rails and repeated full-width dividers should not return; the screenshots show that they read as detached or clipped at the current page gutters.
