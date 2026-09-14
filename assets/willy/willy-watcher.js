(() => {
  'use strict';

  const body = document.body;
  if (!body) return;

  const allowed = body.classList.contains('route-characters-faaram') ||
                  body.classList.contains('route-characters-obama');
  if (!allowed) return;

  const ROOT = '/aevum-archive';
  const ASSET = `${ROOT}/assets/willy/willy-watcher-fade.png`;
  const EYES = `${ROOT}/assets/willy/willy-eyes.png`;
  const TARGET = `${ROOT}/npcs/willy.html`;

  const FOUND_KEY = 'aevum_willy_found';
  const TAB_KEY = `aevum_willy_first_visit_v2_${location.pathname}`;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Guaranteed once per character page and tab. No random success roll.
  if (sessionStorage.getItem(TAB_KEY) === '1') return;
  const APPEAR_AFTER = [30, 60];

  const placements = [
    { top: '17%', right: '-1.5%', width: '17vw', opacity: 0.14, flip: false },
    { top: '48%', left: '-2.8%', width: '15vw', opacity: 0.12, flip: true },
    { bottom: '3%', right: '5%', width: '14vw', opacity: 0.11, flip: false },
    { top: '31%', right: '0.5%', width: '13vw', opacity: 0.12, flip: false }
  ];

  const random = (min, max) => min + Math.random() * (max - min);
  const pick = arr => arr[Math.floor(Math.random() * arr.length)];

  function seconds([min, max]) {
    return random(min, max) * 1000;
  }

  function createWatcher() {
    const link = document.createElement('a');
    link.className = 'willy-watcher';
    link.href = TARGET;
    link.tabIndex = -1;
    link.setAttribute('aria-hidden', 'true');
    link.setAttribute('draggable', 'false');

    const face = document.createElement('img');
    face.src = ASSET;
    face.alt = '';
    face.decoding = 'async';
    face.draggable = false;

    const eyes = document.createElement('img');
    eyes.src = EYES;
    eyes.alt = '';
    eyes.decoding = 'async';
    eyes.draggable = false;
    eyes.className = 'willy-watcher__eyes';

    link.append(face, eyes);

    link.addEventListener('click', () => {
      localStorage.setItem(FOUND_KEY, '1');
      sessionStorage.setItem(TAB_KEY, '1');
    }, { once: true });

    return link;
  }

  function applyPlacement(el) {
    const p = pick(placements);
    ['top','left','right','bottom'].forEach(key => el.style.removeProperty(`--willy-${key}`));
    if (p.top) el.style.setProperty('--willy-top', p.top);
    if (p.left) el.style.setProperty('--willy-left', p.left);
    if (p.right) el.style.setProperty('--willy-right', p.right);
    if (p.bottom) el.style.setProperty('--willy-bottom', p.bottom);
    el.style.setProperty('--willy-width', p.width);
    el.style.setProperty('--willy-opacity', String(p.opacity));
    el.style.setProperty('--willy-fade', `${random(4, 7).toFixed(1)}s`);
    el.style.transform = p.flip ? 'scaleX(-1)' : 'none';
  }

  function show() {
    sessionStorage.setItem(TAB_KEY, '1');

    const watcher = createWatcher();
    applyPlacement(watcher);
    body.appendChild(watcher);

    // Force a paint before fading in.
    requestAnimationFrame(() => requestAnimationFrame(() => watcher.classList.add('is-visible')));

    // Extremely rare direct-gaze moment. Never becomes a jumpscare.
    if (!reducedMotion && Math.random() < 0.02) {
      setTimeout(() => {
        if (!watcher.isConnected) return;
        watcher.classList.add('is-looking');
        setTimeout(() => watcher.classList.remove('is-looking'), random(420, 850));
      }, random(8000, 17000));
    }

    const visibleFor = random(30000, 45000);
    setTimeout(() => {
      watcher.classList.add('is-leaving');
      watcher.classList.remove('is-visible');
      setTimeout(() => watcher.remove(), reducedMotion ? 1600 : 15000);
    }, visibleFor);
  }

  // Do not start the clock until the page is actually visible.
  const start = () => setTimeout(show, seconds(APPEAR_AFTER));
  if (document.visibilityState === 'visible') start();
  else document.addEventListener('visibilitychange', function onVisible() {
    if (document.visibilityState !== 'visible') return;
    document.removeEventListener('visibilitychange', onVisible);
    start();
  });
})();
