/* Motion is decorative; the entire record remains available without JavaScript. */
(() => {
  const stages = [...document.querySelectorAll('[data-monarch-motion]')];
  if (!stages.length || !('IntersectionObserver' in window)) return;
  const visible = new Set();
  const sync = () => stages.forEach(stage => {
    stage.classList.toggle('is-moving', visible.has(stage) && !document.hidden);
  });
  const observer = new IntersectionObserver(entries => {
    entries.forEach(({target, isIntersecting}) => {
      if (isIntersecting) visible.add(target);
      else visible.delete(target);
    });
    sync();
  }, {threshold: 0.12});
  stages.forEach(stage => observer.observe(stage));
  document.addEventListener('visibilitychange', sync);
})();
