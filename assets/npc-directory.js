/* Local, progressive directory search. No portraits, remote requests or hidden lore. */
(() => {
  const directory = document.querySelector('main.npc-directory');
  if (!directory) return;
  const form = directory.querySelector('[data-npc-tools]');
  const search = form.querySelector('input');
  const shelf = form.querySelector('select');
  const status = directory.querySelector('#npc-search-results');
  const empty = directory.querySelector('[data-npc-empty]');
  const sections = [...directory.querySelectorAll(':scope > section.section')];
  const normalize = text => text.normalize('NFKD').replace(/\p{M}/gu, '').toLocaleLowerCase().trim();
  const entries = [...directory.querySelectorAll('.npc-card')].map(card => ({
    card, section: card.closest('section').id,
    text: normalize(card.textContent)
  }));
  const render = () => {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    let count = 0;
    entries.forEach(({card, section, text}) => {
      const visible = (shelf.value === 'all' || shelf.value === section) && terms.every(term => text.includes(term));
      card.hidden = !visible;
      if (visible) count++;
    });
    sections.forEach(section => {
      section.querySelectorAll('.npc-ledger-group').forEach(group => {
        group.hidden = !group.querySelector('.npc-card:not([hidden])');
      });
      section.hidden = !section.querySelector('.npc-card:not([hidden])');
    });
    empty.hidden = count !== 0;
    status.textContent = terms.length || shelf.value !== 'all'
      ? `${count} matching ${count === 1 ? 'entry' : 'entries'} · ${entries.length} in the archive`
      : `${entries.length} entries across six shelves`;
  };
  const clear = () => { search.value = ''; shelf.value = 'all'; render(); };
  search.addEventListener('input', render);
  shelf.addEventListener('change', render);
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('reset', event => { event.preventDefault(); clear(); });
  directory.querySelector('[data-npc-clear]').addEventListener('click', () => { clear(); search.focus(); });
  // Chapter links always lead to an open shelf, even after a narrow search.
  directory.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', clear));
  form.hidden = false;
  render();
})();
