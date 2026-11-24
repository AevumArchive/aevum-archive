(() => {
  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const mark = document.querySelector('.astral-shatter');
  if (mark) {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.intersectionRatio < 0.45) return;
      observer.disconnect();
      mark.classList.add('is-shattering');
    }, { threshold: 0.45 });
    observer.observe(mark);
  }

  const orbit = document.querySelector('.diadem-visual');
  if (orbit) {
    const observer = new IntersectionObserver(([entry]) => {
      orbit.classList.toggle('is-in-view', entry.isIntersecting);
    });
    observer.observe(orbit);
  }
})();
