(() => {
  const main = document.querySelector("main.page");
  if (!main || document.querySelector(".codex-section-nav")) return;

  const sections = [
    ["Overview", "/aevum-archive/codex/"],
    ["Races", "/aevum-archive/codex/races.html"],
    ["Classes", "/aevum-archive/codex/classes.html"],
    ["Paths", "/aevum-archive/codex/paths.html"],
    ["Traits", "/aevum-archive/codex/traits.html"],
    ["Abilities", "/aevum-archive/codex/abilities.html"],
    ["Power", "/aevum-archive/codex/power.html"],
    ["Handbook", "/aevum-archive/codex/handbook.html"]
  ];

  const normalize = (value) => value.replace(/index\.html$/, "").replace(/\/$/, "");
  const current = normalize(window.location.pathname);
  const nav = document.createElement("nav");
  nav.className = "codex-section-nav";
  nav.setAttribute("aria-label", "Codex sections");

  const mark = document.createElement("span");
  mark.className = "codex-section-nav-mark";
  mark.setAttribute("aria-hidden", "true");
  mark.textContent = "⌘";
  nav.append(mark);

  const links = document.createElement("div");
  links.className = "codex-section-nav-links";
  sections.forEach(([label, href]) => {
    const link = document.createElement("a");
    link.href = href;
    link.textContent = label;
    if (normalize(new URL(href, window.location.origin).pathname) === current) {
      link.setAttribute("aria-current", "page");
    }
    links.append(link);
  });
  nav.append(links);
  main.prepend(nav);
})();
