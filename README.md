# Aevum Archive

Public archive website for the Aevum Minecraft roleplay server.

This repository is intentionally separate from `AevumCore`:

- `AevumCore` = plugin code
- `aevum-archive` = public website, character art, texture-pack links and player-safe lore

## First pages

- Home: `index.html`
- Characters: `characters/index.html`
- Downloads: `downloads/texture-pack.html`
- Lore: `lore/index.html`
- Events: `events/index.html`

Prepared character records:

- Astera Zenith
- Lythariel
- William Carter
- Jango
- Guts

## GitHub Pages setup

In the GitHub repository:

1. Open `Settings`
2. Open `Pages`
3. Source: `Deploy from a branch`
4. Branch: `main`
5. Folder: `/root`
6. Save

The public site should become available at:

```text
https://aevumarchive.github.io/aevum-archive/
```

## Adding character art

Put images into:

```text
assets/images/
```

Then update the matching character page to use the image instead of the current archive sigil placeholder.

## Adding texture packs

Recommended clean flow:

1. Upload ZIPs to GitHub Releases for stable downloads.
2. Link the newest ZIP from `downloads/texture-pack.html`.
3. Send players the page link in Minecraft chat.

Do not store GM-only secrets or hidden quest outcomes in this public repository.
