# Global Top 10 portrait slots

The leaderboard points to these final artwork files:

- `thren-valis.webp`
- `lysander-crowe.webp`
- `rhazek-vaul.webp`
- `serin-dhal.webp`
- `vael-orrix.webp`
- `asha-verin.webp`
- `garruk-thorne.webp`
- `ilyra-sen.webp`
- `elira-mourne.webp`
- `mordren-vhal.webp`

## Replacing a portrait without editing HTML

1. Export the artwork as WebP.
2. Rename it to the exact filename above.
3. Put it in `assets/portraits/leaderboard/`, replacing the old file if one exists.
4. Commit and publish the replacement. The slot updates automatically after deployment and cache refresh.

Recommended artwork:

- Portrait ratio: 2:3
- Recommended source size: 1200 x 1800 pixels
- Keep faces and important details inside the central 80% safe area
- Use a dark or transparent-compatible background
- Do not bake text, rank numbers, UI frames or profile icons into the image
- For `vael-orrix.webp`, preserve the head or primary eye, upper arms, chest eye and circular halo geometry; avoid a tight center crop
- For `mordren-vhal.webp`, keep both horns and the upper-body silhouette visible

The page uses an actual `<img>` portrait slot with `object-fit: cover`. Replacing a file with the same filename requires no HTML or CSS change.