# Round 4 UI asset integration

Source: `C:/Users/Yonk/Desktop/aevum_archive_ui_assets_round_4_full.zip`

Integrated: 2026-08-17

Rebalanced after live visual review: 2026-08-17

## Direction

- 40 transparent PNG assets are imported and ready.
- 17 assets currently have deliberate live placements; the remaining 23 are staged for later route-specific slots.
- A page region receives at most one focal ornament. Generic cards, links and section boundaries do not repeat detailed raster art.
- Character profile icons remain the existing symbols. No portrait or portrait-like backplate replaces them.
- Sealed and Fallen state cards use segmented edges, knots and corners at their natural aspect ratios.
- Locked achievements use the established quiet edge-chain treatment. The large Round 4 chain sprites are reserved for a future dedicated lock panel because crossing them through every card reduced readability.
- Player-facing text contains no admin or Gamemaster guidance.

## Live placements

- Global: compact header brand medallion.
- Home: one restrained archive-door crest with protected spacing above the hero copy.
- 404: one lost-page sigil.
- Character status shelf: Active, Sealed, Fallen and Retired corners; Sealed/Fallen edge segments and state knots.
- Leaderboard: crown in the dedicated board slot and the gold board divider.

## Reserved groups

- Navigation endcaps and page-corner whispers.
- Roster, profile-card and profile-slot ornaments.
- Bond-oracle crests.
- Full chain tiles, endcaps, crossing clasp and wax seal.
- Additional home pins, halos, card corners and keylines.
- Generic footer, mobile and section dividers.

These files are intentionally kept out of unsuitable or repeated slots. They can be assigned when later asset rounds supply complete route families.

## Technical note

Several filenames describe intended production slots, while the delivered canvases use generator dimensions such as `1254 x 1254`, `2172 x 724` and `724 x 2172`. CSS therefore preserves source ratios with contain-style sizing. Flexible frame geometry remains CSS/segmented; no complete raster frame is stretched over a variable card.
