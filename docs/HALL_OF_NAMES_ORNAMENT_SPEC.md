# Hall of Names ornament production spec

This document is the technical contract for the next Hall of Names status ornaments. The existing character-card HTML must not be rebuilt around the artwork. Every delivered image is a decorative transparent layer placed over the stable card component.

## Final card geometry

- Card aspect ratio: **2:3** at every grid breakpoint.
- Production canvas for every ornament: **1200 x 1800 px**.
- Format: transparent **RGBA PNG**.
- The production canvas is exactly four times the largest normal CSS card target of 300 x 450 px.
- Do not crop a layer to its visible pixels. Every frame and motif file must keep the complete 1200 x 1800 transparent canvas so both layers align automatically.
- Do not include portraits, character names, status words, generated labels, lore text, checkerboards or opaque card backgrounds.

Measured rendered card sizes after the 2026-09-16 layout pass:

| Viewport | Columns | Rendered card |
| --- | ---: | ---: |
| 2536 px | 4 | 260.00 x 390.00 px |
| 2378 px | 4 | 260.00 x 390.00 px |
| 1440 px | 4 | 260.00 x 390.00 px |
| 1200 px | 4 | 260.00 x 390.00 px |
| 1024 px | 4 | 228.75 x 343.13 px |
| 768 px | 3 | 225.66 x 338.48 px |
| 390 px | 1 | 300.00 x 450.00 px |

The browser scales the 1200 x 1800 master uniformly to these sizes. No status asset may require a different card ratio.

## Protected zones on the 1200 x 1800 canvas

- Outer frame zone: `x 0-1199`, `y 0-1799`.
- Recommended straight-edge thickness: **56-76 px**.
- Maximum corner ornament reach: **96 px** from either outer edge.
- Minimum clear inner opening: `x 84-1116`, `y 110-1690`.
- Media focal-safe zone: `x 180-1020`, `y 200-1120`.
- Text-safe zone: `x 120-1080`, `y 1250-1700`.
- The text-safe zone must remain readable. Do not run chains, drapery, seals, cracks, weapons, sigils or other high-contrast shapes through it.
- Motifs may touch the outer 84 px of the text-safe zone at low opacity, but must not cross its center.
- Keep the lower status-badge area `x 390-810`, `y 1630-1750` clear.

## Required filenames and automatic placement

All files go in `assets/hall-of-names/v4/`.

| Status | Frame layer (`::before`) | Motif layer (`::after`) |
| --- | --- | --- |
| Active | `hall-card-active-frame-1200x1800.png` | `hall-card-active-motif-aether-1200x1800.png` |
| Sealed | `hall-card-sealed-frame-1200x1800.png` | `hall-card-sealed-motif-chains-1200x1800.png` |
| Fallen | `hall-card-fallen-frame-1200x1800.png` | `hall-card-fallen-motif-broken-chains-1200x1800.png` |
| Retired | `hall-card-retired-frame-1200x1800.png` | `hall-card-retired-motif-drapery-1200x1800.png` |
| Lost / Unknown | `hall-card-lost-frame-1200x1800.png` | `hall-card-lost-motif-fracture-1200x1800.png` |

The filename is the routing contract. Do not rename `lost` to `unknown`, `dead` or `missing`; the site status key is `lost`. Fallen uses the existing `fallen`/`dead` compatibility selectors internally, but the supplied asset name is always `fallen`.

## Layer responsibilities

### Frame layer

- Border, corners and small status-specific crest only.
- Must read clearly at 220 px rendered width.
- Keep the center and text-safe zone transparent.
- Avoid giant emblems, faces or scenery.

### Motif layer

- Secondary status storytelling only: restrained aether for Active, locks/chains for Sealed, broken chains for Fallen, drapery for Retired, dimensional fracture for Lost.
- Must use the same 1200 x 1800 canvas and align without offsets.
- Prefer edge-bound decoration. Never place a large motif across the character name, description or status badge.
- No baked glow outside the canvas. Soft internal glow is allowed.

## Status direction

- **Active:** restrained green-gold archive metal; open and alive, not overdecorated.
- **Sealed:** violet-black metal with arcane locks and controlled chains; bound, not visually buried.
- **Fallen:** dark iron and muted crimson with broken chains or a fractured seal; solemn rather than noisy.
- **Retired:** aged gold and dark cloth drapery; honored and at rest, not imprisoned.
- **Lost / Unknown:** cold cyan and dim violet dimensional fracture; unresolved and displaced, not confirmed dead.

## Delivery checklist

- Ten PNG files total: two for each of five statuses.
- Every PNG is exactly 1200 x 1800 px.
- Every PNG has genuine transparency.
- Frame and motif layers align when stacked at `(0, 0)`.
- No content in the protected text and badge zones.
- No character art, names, labels, watermarks or invented lore.
- Include a contact sheet for review, but the contact sheet is not integrated into the site.

When the correctly named files are supplied, integration only requires mapping each status selector to its two files in `assets/character-status-frames.css`; no HTML or JavaScript changes are needed.
