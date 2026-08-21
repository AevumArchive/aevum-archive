(() => {
  const root = "/aevum-archive/assets/ui/master-pack";
  const body = document.body;

  if (!body) return;

  const makeArt = (round, file, className = "") => {
    const image = document.createElement("img");
    image.className = `master-ui-art ${className}`.trim();
    image.src = `${root}/Round_${round}/${file}`;
    image.alt = "";
    image.setAttribute("aria-hidden", "true");
    image.decoding = "async";
    image.loading = "lazy";
    image.dataset.masterAsset = file.slice(0, 3);
    return image;
  };

  const place = (target, round, file, className, where = "append") => {
    const element = typeof target === "string" ? document.querySelector(target) : target;
    if (!element || element.querySelector(`:scope > [data-master-asset="${file.slice(0, 3)}"]`)) return null;
    element.classList.add("master-ui-host");
    const image = makeArt(round, file, className);
    if (where === "prepend") element.prepend(image);
    else element.append(image);
    return image;
  };

  const sectionNamed = (name) => [...document.querySelectorAll("section")].find((section) => {
    const heading = section.querySelector(":scope > .section-head h2, :scope > h2");
    return heading?.textContent.trim().toLowerCase() === name.toLowerCase();
  });

  const markSection = (section, round, file) => {
    const head = section?.querySelector(":scope > .section-head");
    if (head) place(head, round, file, "master-section-emblem");
  };

  const markCards = (section, round, file, className = "master-card-status-art") => {
    section?.querySelectorAll(":scope .status-grid > *, :scope .grid > *").forEach((card) => {
      place(card, round, file, className);
    });
  };

  const normalizedPath = (value) => {
    const url = new URL(value, window.location.href);
    return url.pathname.replace(/index\.html$/, "").replace(/\/$/, "") || "/";
  };

  if (body.classList.contains("route-home")) return;

  const currentPath = normalizedPath(window.location.href);
  document.querySelectorAll(".nav a").forEach((link) => {
    if (normalizedPath(link.href) === currentPath) link.classList.add("master-nav-current");
  });

  place(".footer", "10", "098_Global_Final_Section_Divider.png", "master-final-divider", "prepend");

  if (body.classList.contains("theme-characters")) {
    place(".hero", "02", "016_Characters_Section_Header_Banner.png", "master-hero-art");

    if (body.classList.contains("route-characters-all")) {
      const boards = [...document.querySelectorAll(".status-board")];
      markCards(boards[1], "02", "013_Characters_Sealed_Moonveil_Overlay.png", "master-card-strip master-sealed-strip");
      markCards(boards[2], "02", "018_Characters_Fallen_Status_Badge.png", "master-card-strip master-fallen-strip");
      markCards(boards[3], "02", "019_Characters_Retired_Status_Badge.png", "master-card-strip master-retired-strip");
    }

    if (body.classList.contains("route-characters-bonds")) {
      place(".bond-oracle-card", "03", "025_Bonds_Linked_Souls_Emblem.png", "master-aside-emblem");
      markSection(document.querySelector("#current-bonds"), "03", "029_Bonds_Trusted_Alliance_Emblem.png");
      markSection(document.querySelector("#faaram-web"), "03", "027_Bonds_Broken_Pact_Emblem.png");
      place("#faaram-web .faaram-tree", "02", "020_Characters_Bonds_Moon_Divider.png", "master-card-divider");
    }
  }

  if (body.classList.contains("theme-npcs")) {
    place(".hero", "03", "023_NPC_Section_Divider.png", "master-hero-art master-hero-art-npc");
    place(".hero .archive-card", "03", "026_NPC_Archive_Record_Seal.png", "master-aside-emblem");

    if (body.classList.contains("route-npcs")) {
      markSection(document.querySelector("#current-npcs"), "03", "022_NPC_Faction_Alliance_Badge.png");
      markSection(document.querySelector("#servants"), "03", "030_NPC_Arcane_Affiliation_Emblem.png");
      markSection(document.querySelector("#known-figures"), "03", "026_NPC_Archive_Record_Seal.png");
      place("#servants .ichiro-card", "03", "027_Bonds_Broken_Pact_Emblem.png", "master-card-badge master-hostile-badge");
      place("#servants .gold-card", "03", "029_Bonds_Trusted_Alliance_Emblem.png", "master-card-badge");
    }
  }

  if (body.classList.contains("theme-lore")) {
    place(".hero", "04", "037_Lore_Section_Title_Plate.png", "master-hero-art");
    place(".hero .archive-card", "04", "033_Lore_Atlas_Navigation_Compass.png", "master-aside-emblem");

    if (body.classList.contains("route-lore")) {
      const sections = [...document.querySelectorAll(".lore-map")];
      const assets = [
        ["04", "040_Lore_Legendary_Record_Emblem.png"],
        ["04", "034_Lore_Chronicle_Record_Scroll.png"],
        ["04", "032_Lore_Kingdom_Heraldry_Banner.png"],
        ["04", "035_Lore_Magical_Anomaly_Crystal.png"],
        ["04", "038_Lore_Rumor_Important_Marker.png"],
        ["04", "039_Lore_Sealed_Archive_Grimoire.png"],
      ];
      sections.forEach((section, index) => {
        if (assets[index]) markSection(section, assets[index][0], assets[index][1]);
      });
    }
  }

  if (body.classList.contains("theme-playthroughs")) {
    place(".hero", "05", "041_Playthroughs_Header_Ornament.png", "master-hero-art");
    place(".hero .archive-card", "05", "047_Playthroughs_Current_Era_Seal.png", "master-aside-emblem");
    place(".playthrough-primary", "05", "046_Playthroughs_Milestone_Emblem.png", "master-card-badge");
    markSection(document.querySelector("#history"), "05", "048_Playthroughs_Completed_Era_Seal.png");
    place("#history", "05", "050_Playthroughs_Timeline_Divider.png", "master-section-divider", "prepend");
  }

  if (body.classList.contains("theme-events")) {
    place(".hero", "06", "051_Events_Header_Banner.png", "master-hero-art");

    if (body.classList.contains("route-world-events")) {
      place(".anchor-card", "06", "053_Events_Countdown_Hourglass.png", "master-aside-emblem");
      place("#world-anchor .event-card", "06", "054_Events_World_Anchor_Emblem.png", "master-card-badge master-event-anchor");
      place("#world-anchor", "06", "059_Events_Phase_Timeline.png", "master-section-divider", "prepend");
    } else {
      place(".hero .archive-card", "06", "056_Events_Chronicle_Scroll.png", "master-aside-emblem");
      markSection(document.querySelector("#older-incidents"), "06", "058_Events_Event_Route_Connector.png");
    }
  }

  if (body.classList.contains("theme-achievements")) {
    place(".hero", "07", "061_Achievements_Header_Ornament.png", "master-hero-art");
    place(".hero .archive-card", "07", "065_Achievements_Prestige_Crest.png", "master-aside-emblem");
    place(".overlord-trophy", "07", "067_Achievements_Mythic_Frame.png", "master-trophy-halo");
    place(".blue-trophy", "07", "064_Achievements_Ranked_Emblem.png", "master-card-badge");
    markSection(document.querySelector("#locked"), "07", "063_Achievements_Locked_Overlay.png");
  }

  if (body.classList.contains("theme-leaderboard")) {
    place(".leaderboard-hero", "08", "071_Leaderboard_Header_Ornament.png", "master-hero-art");
    place(".leaderboard-hero .archive-card", "08", "073_Leaderboard_Champion_Trophy_Emblem.png", "master-aside-emblem");
    markSection(document.querySelector(".power-ledger"), "08", "074_Leaderboard_Global_Rank_Compass.png");
    place(".global-rank-card.rank-1 .global-rank-head", "08", "072_Leaderboard_Rank_01_Crown_Crest.png", "master-rank-crest");
    document.querySelectorAll(".global-rank-card.rank-2 .global-rank-head, .global-rank-card.rank-3 .global-rank-head").forEach((head) => {
      place(head, "08", "079_Leaderboard_Rank_Banner.png", "master-rank-banner");
    });
  }

  if (body.classList.contains("theme-relics")) {
    place(".relic-hero .archive-card", "09", "090_Relics_Unknown_Origin_Astrolabe.png", "master-aside-emblem");
    place(".nocturne-card .relic-copy", "09", "082_Relics_World_Item_Spectral_Blade.png", "master-relic-mark");
    place(".lost-relic-card .relic-copy", "09", "088_Relics_Lost_Item_Emblem.png", "master-relic-mark master-lost-mark");
    place(".relic-sealed-strip", "09", "086_Relics_Vault_Display.png", "master-card-badge master-vault-mark");
  }

  if (body.classList.contains("theme-downloads")) {
    place(".hero .archive-card", "10", "091_Downloads_Archive_Emblem.png", "master-aside-emblem");
    place(".feature-panel", "10", "093_Downloads_Download_Action_Emblem.png", "master-download-mark");
    place(".ritual-panel", "10", "092_Downloads_Texture_Pack_Record.png", "master-download-mark master-record-mark");
  }

  if (body.classList.contains("theme-codex")) {
    const search = document.querySelector('input[type="search"]');
    if (search?.parentElement) place(search.parentElement, "10", "094_Global_Search_Field_Frame.png", "master-search-frame");
  }

  if (body.classList.contains("route-sealed-records")) {
    place(".hero .archive-card", "04", "039_Lore_Sealed_Archive_Grimoire.png", "master-aside-emblem");
  }
})();
