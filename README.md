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

The character roster is maintained in `characters/all.html`; avoid duplicating a static name list here. Codex records live under `codex/`, including separate Traits, Abilities and Bindings shelves. Restricted entity records use the client-side Deep Archive presentation; this is an immersive gate, not a security boundary for private future lore.

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

To update the pack without editing the website:

1. Open the repository's `Releases` page on GitHub.
2. Choose `Draft a new release`.
3. Create any new unique tag and choose any release title.
4. Attach the texture pack as a ZIP. Its filename can be anything.
5. Publish it as a normal release, not as a draft or prerelease.

The Downloads page queries the latest published release and automatically links its newest ZIP asset. If a release contains multiple ZIP files, the most recently updated ZIP is selected. No HTML change or repository commit is required for later pack updates.

Do not store sealed truths, hidden quest outcomes or private future plans in this public repository.
