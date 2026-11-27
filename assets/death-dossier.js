/* Run the symbolic clock only while it is visible and motion is allowed. */
(() => {
  if (!('IntersectionObserver' in window)) return;

  const stages = [...document.querySelectorAll('[data-death-motion]')];
  if (stages.length === 0) return;

  const visible = new Set();
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const sync = () => {
    for (const stage of stages) {
      stage.toggleAttribute('data-death-running',
        visible.has(stage) && !document.hidden && !motion.matches);
    }
  };

  const observer = new IntersectionObserver(entries => {
    for (const { target, isIntersecting } of entries) {
      if (isIntersecting) visible.add(target);
      else visible.delete(target);
    }
    sync();
  });

  for (const stage of stages) observer.observe(stage);

  document.addEventListener('visibilitychange', sync);
  motion.addEventListener('change', sync);
})();
