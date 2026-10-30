/* A two-night costume for the Archive; no lore or saved character state changes. */
(() => {
  const root = document.documentElement;
  const calendar = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Berlin', year: 'numeric', month: '2-digit', day: '2-digit'
  });
  const inSeason = () => {
    const parts = Object.fromEntries(calendar.formatToParts(new Date()).map(p => [p.type, p.value]));
    const day = `${parts.year}-${parts.month}-${parts.day}`;
    return day >= '2026-10-30' && day < '2026-11-01';
  };
  const pumpkin = `<svg viewBox="0 0 120 120" fill="none" aria-hidden="true"><path d="M59 29c-3-12 4-19 14-20l-3 8c-6 0-8 5-7 12" stroke="#938165" stroke-width="4"/><path d="M60 31C25 13 5 51 17 83c8 24 28 24 43 18 17 6 37 6 45-18 12-32-8-70-45-52Z" fill="#3e211a" stroke="#d68841" stroke-width="1.5"/><path d="M60 32c-24-11-34 18-30 43s15 31 30 26c15 5 28-7 30-26s-8-54-30-43Z" stroke="#b46c35"/><path d="M60 33c-10 14-11 52 0 68 11-16 10-54 0-68Z" stroke="#91522c"/><g class="halloween-flame" fill="#ffd888"><path d="m31 53 19 12-20 4Zm58 0-19 12 20 4ZM57 70l3-10 4 10ZM31 80l14 3 4-7 9 8 10-8 5 7 17-3-12 13H43Z"/></g></svg>`;
  const web = `<svg viewBox="0 0 200 200" fill="none" aria-hidden="true"><g stroke="currentColor" stroke-width=".8"><path d="M0 0v195M0 0l52 190M0 0l100 172M0 0l143 140M0 0l173 99M0 0l192 50M0 0h200"/><path d="M0 35q6-6 9-1 3-8 9-3 0-8 7-6-2-8 6-7-4-7 3-9-6-4 1-9M0 75q14-13 20-3 4-17 18-7 0-17 15-12-4-17 12-15-10-13 7-18-12-10 3-20M0 120q22-20 32-4 7-27 29-12 0-27 24-19-8-27 19-24-15-23 12-29-20-16 4-32M0 175q31-29 47-6 9-39 41-18 0-39 35-28-11-39 28-35-22-33 18-41-29-23 6-47"/></g></svg>`;
  const bat = `<svg viewBox="0 0 100 45" aria-hidden="true"><path d="M50 21 44 13l1 13C31 12 16 4 1 2c7 8 6 17 4 24 8-5 15-2 17 6 10-5 17 0 21 7l7-5 7 5c4-7 11-12 21-7 2-8 9-11 17-6-2-7-3-16 4-24-15 2-30 10-44 24l1-13Z"/></svg>`;
  let banner;
  let atmosphere;
  let quiet = false;
  try { quiet = sessionStorage.getItem('aevum-halloween-quiet') === 'true'; } catch (_) { /* Storage is optional. */ }
  const mount = () => {
    if (!document.body || !inSeason() || banner) return;
    banner = document.createElement('aside');
    banner.className = 'halloween-banner';
    banner.setAttribute('aria-label', 'Halloween at the Archive');
    banner.innerHTML = `<div class="halloween-lantern">${pumpkin}</div><div class="halloween-copy"><p class="halloween-kicker">All Hallows’ Eve <span>30 — 31 OCT 2026</span></p><p class="halloween-title">The veil grows thin.</p><p class="halloween-whisper">Keep a light. The Archive is awake.</p></div><div class="halloween-moon" aria-hidden="true">${bat}</div><button class="halloween-toggle" type="button" aria-pressed="${quiet}">Still the shadows</button>`;
    const header = document.querySelector('.site-header');
    if (header) header.after(banner); else document.body.prepend(banner);
    atmosphere = document.createElement('div');
    atmosphere.className = 'halloween-atmosphere';
    atmosphere.setAttribute('aria-hidden', 'true');
    atmosphere.innerHTML = `<div class="halloween-web halloween-web-left">${web}</div><div class="halloween-web halloween-web-right">${web}</div><div class="halloween-fog"></div><div class="halloween-embers">${Array.from({length: 9}, (_, i) => `<i style="--n:${i}"></i>`).join('')}</div><div class="halloween-bat halloween-bat-one">${bat}</div><div class="halloween-bat halloween-bat-two">${bat}</div>`;
    document.body.append(atmosphere);
    root.classList.toggle('halloween-quiet', quiet);
    const toggle = banner.querySelector('button');
    toggle.addEventListener('click', () => {
      quiet = !quiet;
      root.classList.toggle('halloween-quiet', quiet);
      toggle.setAttribute('aria-pressed', String(quiet));
      toggle.textContent = quiet ? 'Wake the shadows' : 'Still the shadows';
      try { sessionStorage.setItem('aevum-halloween-quiet', String(quiet)); } catch (_) { /* Storage is optional. */ }
    });
    if (quiet) toggle.textContent = 'Wake the shadows';
  };
  const sync = () => {
    const active = inSeason();
    root.classList.toggle('halloween-night', active);
    if (active) mount();
    else {
      banner?.remove(); atmosphere?.remove();
      banner = atmosphere = undefined;
      root.classList.remove('halloween-quiet');
    }
  };
  // Set the class in the head before first paint, then mount when the document exists.
  sync();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', sync, {once: true});
  if (inSeason()) {
    const timer = setInterval(() => { sync(); if (!inSeason()) clearInterval(timer); }, 15000);
    document.addEventListener('visibilitychange', sync);
    window.addEventListener('pageshow', sync);
  }
})();
