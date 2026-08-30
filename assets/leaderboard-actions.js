(() => {
  const cards = [...document.querySelectorAll('.route-leaderboard .global-rank-card')];
  if (!cards.length || !('HTMLDialogElement' in window)) return;

  const dialog = document.createElement('dialog');
  dialog.className = 'leaderboard-challenge-dialog';
  dialog.setAttribute('aria-labelledby', 'challenge-writ-title');
  dialog.innerHTML = `
    <div class="challenge-writ">
      <p class="eyebrow">Public duel writ</p>
      <h2 id="challenge-writ-title">Challenge the ranked.</h2>
      <p class="challenge-writ-target" data-challenge-target></p>
      <div class="challenge-writ-facts">
        <div><span>Global standing</span><strong data-challenge-rank></strong></div>
        <div><span>Stable Power Level</span><strong data-challenge-power></strong></div>
      </div>
      <p class="challenge-writ-note">The Archive prepares the writ; copy it and deliver it through the channel your server uses for duels. Stable PL does not determine the outcome.</p>
      <div class="challenge-writ-actions">
        <button type="button" data-challenge-close>Close</button>
        <button type="button" class="copy-challenge-writ" data-challenge-copy>Copy challenge writ</button>
      </div>
    </div>`;
  document.body.append(dialog);

  const target = dialog.querySelector('[data-challenge-target]');
  const rank = dialog.querySelector('[data-challenge-rank]');
  const power = dialog.querySelector('[data-challenge-power]');
  const copy = dialog.querySelector('[data-challenge-copy]');
  let currentWrit = '';

  const copyText = async (value) => {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(value);
    const field = document.createElement('textarea');
    field.value = value;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.append(field);
    field.select();
    document.execCommand('copy');
    field.remove();
  };

  cards.forEach((card) => {
    const powerBlock = card.querySelector('.global-power');
    const name = card.querySelector('.global-rank-head h2')?.textContent.trim();
    const standing = card.querySelector('.global-rank-head .eyebrow')?.textContent.trim();
    const title = card.querySelector('.global-rank-title')?.textContent.trim();
    const levelNode = card.querySelector('.global-power strong');
    if (!powerBlock || !name) return;

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'leaderboard-challenge';
    button.textContent = 'Challenge';
    button.setAttribute('aria-label', `Challenge ${name}`);
    button.addEventListener('click', () => {
      const level = levelNode?.textContent.trim() || 'DATA UNAVAILABLE';
      target.textContent = `${name} · ${title}`;
      rank.textContent = standing.replace('Global ', '');
      power.textContent = level;
      currentWrit = `⚔ AEVUM GLOBAL CHALLENGE\nTarget: ${name} — ${standing}\nTitle: ${title}\nStable Power Level: ${level}\nRecord: ${location.origin}${location.pathname}#${card.id}`;
      copy.textContent = 'Copy challenge writ';
      dialog.showModal();
    });
    powerBlock.append(button);
  });

  dialog.querySelector('[data-challenge-close]').addEventListener('click', () => dialog.close());
  copy.addEventListener('click', async () => {
    try {
      await copyText(currentWrit);
      copy.textContent = 'Challenge writ copied';
    } catch {
      copy.textContent = 'Copy failed — try again';
    }
  });
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
})();
