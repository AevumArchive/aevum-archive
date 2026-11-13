(() => {
  const mark = document.querySelector('.astral-shatter');
  if (!mark || !('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const observer = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    mark.classList.add('is-shattering');
    observer.disconnect();
  }, { threshold: 0.45 });

  observer.observe(mark);
})();
