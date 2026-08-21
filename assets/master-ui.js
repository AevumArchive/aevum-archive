(() => {
  const body = document.body;
  if (!body) return;

  const normalizedPath = (value) => {
    const url = new URL(value, window.location.href);
    return url.pathname.replace(/index\.html$/, "").replace(/\/$/, "") || "/";
  };

  const currentPath = normalizedPath(window.location.href);
  const sectionAliases = new Map([
    ["/aevum-archive/world-events", "/aevum-archive/events"],
    ["/aevum-archive/sealed-records", "/aevum-archive/achievements"],
    ["/aevum-archive/top-characters", "/aevum-archive/leaderboard"],
  ]);
  const activePath = sectionAliases.get(currentPath) || currentPath;

  document.querySelectorAll(".nav a").forEach((link) => {
    const linkPath = normalizedPath(link.href);
    const isSection = linkPath !== "/aevum-archive" && activePath.startsWith(`${linkPath}/`);
    if (linkPath === activePath || isSection) link.classList.add("master-nav-current");
  });

  if (!body.classList.contains("route-events")) return;

  const hero = document.querySelector(".hero");
  if (!hero || hero.querySelector("[data-master-asset=\"051\"]")) return;

  hero.classList.add("master-event-banner-host");
  const banner = document.createElement("img");
  banner.className = "master-event-banner";
  banner.src = "/aevum-archive/assets/ui/master-pack/Round_06/051_Events_Header_Banner.png";
  banner.alt = "";
  banner.setAttribute("aria-hidden", "true");
  banner.decoding = "async";
  banner.dataset.masterAsset = "051";
  hero.append(banner);
})();