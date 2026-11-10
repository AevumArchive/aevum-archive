(() => {
  if (!("IntersectionObserver" in window)) return;

  const scene = document.querySelector(".kenka-cut");
  const landscape = scene.querySelector(".kenka-cut-upper");
  const visibleFraction = 0.4;
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.intersectionRatio < visibleFraction) return;

    scene.classList.add("is-cut");
    observer.disconnect();
  }, { threshold: visibleFraction });

  if (landscape.complete && landscape.naturalWidth) {
    observer.observe(scene);
  } else {
    landscape.addEventListener("load", () => observer.observe(scene), { once: true });
  }
})();
