/* Keep the symbolic clock still when the user or the viewport asks it to. */
(() => {
  if (!('IntersectionObserver' in window)) return;

  const stages = [...document.querySelectorAll('[data-death-motion]')];
  if (stages.length === 0) return;

  const visible = new Set();
  const paused = new Set();
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const sync = () => {
    for (const stage of stages) {
      stage.toggleAttribute('data-death-running',
        visible.has(stage) && !paused.has(stage) && !document.hidden && !motion.matches);
    }
  };

  const observer = new IntersectionObserver(entries => {
    for (const { target, isIntersecting } of entries) {
      if (isIntersecting) visible.add(target);
      else visible.delete(target);
    }
    sync();
  });

  for (const stage of stages) {
    observer.observe(stage);
    const control = stage.querySelector('[data-death-pause]');
    if (!control) continue;
    control.hidden = false;
    control.addEventListener('click', () => {
      if (paused.has(stage)) paused.delete(stage);
      else paused.add(stage);
      control.textContent = paused.has(stage) ? 'Resume motion' : 'Pause motion';
      sync();
    });
  }

  document.addEventListener('visibilitychange', sync);
  motion.addEventListener('change', sync);
})();
