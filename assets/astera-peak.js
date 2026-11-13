(() => {
  const mark = document.querySelector('.astral-shatter');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!mark || motion.matches) return;

  const replay = mark.querySelector('.astral-replay');
  const play = () => {
    if (motion.matches) return;
    mark.classList.remove('is-shattering');
    // Flush the removed animation so another click can restart it.
    mark.getBoundingClientRect();
    mark.classList.add('is-shattering');
  };

  replay.hidden = false;
  replay.addEventListener('click', play);
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.intersectionRatio < 0.45) return;
    observer.disconnect();
    play();
  }, { threshold: 0.45 });
  observer.observe(mark);
})();
