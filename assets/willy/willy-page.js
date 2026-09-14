(() => {
  'use strict';

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#?%&§∆ΩΞЖ░▒▓';

  function scrambleText(el) {
    const source = el.dataset.text || el.textContent || '';
    if (!source) return;

    const tick = () => {
      let output = '';
      for (const char of source) {
        if (/\s/.test(char)) output += char;
        else if (/[-/.:]/.test(char) && Math.random() > .25) output += char;
        else output += pool[Math.floor(Math.random() * pool.length)];
      }
      el.textContent = output;
    };

    tick();
    if (!reducedMotion) setInterval(tick, 95 + Math.floor(Math.random() * 55));
  }

  document.querySelectorAll('.willy-corrupt[data-text]').forEach(scrambleText);

  if (reducedMotion) return;

  const revealers = [...document.querySelectorAll('.willy-reveal[data-reveal]')];

  function scheduleReveal(el) {
    const wait = 5000 + Math.random() * 12000;
    setTimeout(() => {
      if (Math.random() < .38) {
        const current = el.textContent;
        el.textContent = el.dataset.reveal;
        el.classList.add('is-revealed');
        const duration = 420 + Math.random() * 680;
        setTimeout(() => {
          el.classList.remove('is-revealed');
          el.textContent = current;
        }, duration);
      }
      scheduleReveal(el);
    }, wait);
  }

  revealers.forEach(scheduleReveal);

  // Rarely corrupt the browser tab title for a moment.
  const originalTitle = document.title;
  const titlePool = ['WILLY', '██████', 'FAARAM I SEE YOU', 'OBAMA I SEE YOU TOO', 'DO NOT TURN AROUND', 'HE IS STILL HERE'];
  function titleEvent() {
    setTimeout(() => {
      if (Math.random() < .18) {
        document.title = titlePool[Math.floor(Math.random() * titlePool.length)];
        setTimeout(() => { document.title = originalTitle; }, 650 + Math.random() * 1200);
      }
      titleEvent();
    }, 9000 + Math.random() * 18000);
  }
  titleEvent();
})();
