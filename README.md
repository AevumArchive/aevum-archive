# Aevum Archive

Public archive website for witnessed Aevum records, portraits, lore and traveler downloads.

This repository is intentionally only for public-facing archive pages:

- public character records
- public lore pages
- traveler downloads
- event chronicles fit for public reading

## First pages

- Home: `index.html`
- Characters: `characters/index.html`
- All character records: `characters/all.html`
- Playthroughs: `playthroughs/index.html`
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

The public download buttons permanently use:

```text
https://github.com/AevumArchive/aevum-archive/releases/latest/download/Playthrough-Addon.zip
```

To update the pack without editing the website:

1. Open the repository's `Releases` page on GitHub.
2. Choose `Draft a new release`.
3. Create a new unique tag, for example `texture-pack-2026-09-28`.
4. Attach the new ZIP with the exact filename `Playthrough-Addon.zip`.
5. Publish it as a normal release, not as a draft or prerelease.

The Downloads page will then automatically serve the ZIP from the newest published release. No HTML change or repository commit is required for later pack updates.

Do not store sealed truths, hidden quest outcomes or private future plans in this public repository.
