/* Shelf links open their sections without JavaScript and switch views when enhanced. */
(() => {
  const directory = document.querySelector('main.npc-directory');
  if (!directory) return;
  const form = directory.querySelector('[data-npc-tools]');
  const search = form.querySelector('input');
  const reset = form.querySelector('button[type="reset"]');
  const status = directory.querySelector('#npc-search-results');
  const empty = directory.querySelector('[data-npc-empty]');
  const sections = [...directory.querySelectorAll(':scope > section.section')];
  const tabs = [...directory.querySelectorAll('.npc-ledger-nav a')];
  const shelfNames = new Map(tabs.map(tab => [tab.hash.slice(1), tab.querySelector('strong').textContent]));
  const shelfFromHash = () => tabs.find(tab => tab.hash === location.hash)?.hash ?? tabs[0].hash;
  let activeShelf = shelfFromHash();
  const normalize = text => text.normalize('NFKD').replace(/\p{M}/gu, '').toLocaleLowerCase().trim();
  const entries = [...directory.querySelectorAll('.npc-card')].map(card => {
    const section = card.closest('section').id;
    const affiliation = card.closest('[data-npc-affiliation]')?.dataset.npcAffiliation ?? '';
    return { card, section, text: normalize(`${card.textContent} ${shelfNames.get(section)} ${affiliation}`) };
  });
  const render = () => {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    const searching = terms.length > 0;
    const activeId = activeShelf.slice(1);
    let count = 0;
    entries.forEach(({card, section, text}) => {
      const visible = searching ? terms.every(term => text.includes(term)) : section === activeId;
      card.hidden = !visible;
      if (visible) count++;
    });
    sections.forEach(section => {
      section.querySelectorAll('.npc-ledger-group').forEach(group => {
        group.hidden = !group.querySelector('.npc-card:not([hidden])');
      });
      section.hidden = !section.querySelector('.npc-card:not([hidden])');
    });
    tabs.forEach(tab => {
      if (!searching && tab.hash === activeShelf) tab.setAttribute('aria-current', 'location');
      else tab.removeAttribute('aria-current');
    });
    reset.hidden = !search.value;
    empty.hidden = count !== 0;
    status.textContent = searching
      ? `${count} ${count === 1 ? 'result' : 'results'} across all shelves`
      : '';
  };
  const clearSearch = () => { search.value = ''; render(); };
  tabs.forEach(tab => {
    tab.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      if (location.hash !== tab.hash) history.pushState(null, '', tab.hash);
      activeShelf = tab.hash;
      clearSearch();
    });
  });
  window.addEventListener('hashchange', () => {
    activeShelf = shelfFromHash();
    clearSearch();
  });
  search.addEventListener('input', render);
  form.addEventListener('submit', event => event.preventDefault());
  const resetSearch = () => { clearSearch(); search.focus(); };
  form.addEventListener('reset', event => { event.preventDefault(); resetSearch(); });
  directory.querySelector('[data-npc-clear]').addEventListener('click', resetSearch);
  form.hidden = false;
  render();
})();
