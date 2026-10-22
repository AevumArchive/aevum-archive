/* Progressive enhancement only: every public record remains in the static page. */
(() => {
  const tools = document.querySelector('[data-ledger-tools]');
  const records = document.getElementById('npc-ledger-records');
  if (!tools || !records) return;
  const input = document.getElementById('npc-search');
  const shelf = document.getElementById('npc-shelf');
  const status = document.getElementById('npc-search-status');
  const empty = document.querySelector('[data-ledger-empty]');
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('en').trim();
  const sections = [...records.querySelectorAll(':scope > section[id]')];
  const groups = sections.map(section => ({
    section,
    groups: [...section.querySelectorAll('.npc-ledger-group')].map(group => ({
      group, entries: [...group.querySelectorAll('.npc-card')].map(card => ({ card, text: normalize(card.textContent) }))
    }))
  }));
  const filter = () => {
    const terms = normalize(input.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const { section, groups: chapterGroups } of groups) {
      const inShelf = shelf.value === 'all' || shelf.value === section.id;
      let sectionCount = 0;
      for (const { group, entries } of chapterGroups) {
        let count = 0;
        for (const { card, text } of entries) {
          const matches = inShelf && terms.every(term => text.includes(term));
          card.hidden = !matches;
          if (matches) count++;
        }
        group.hidden = count === 0;
        sectionCount += count;
      }
      section.hidden = sectionCount === 0;
      const link = document.querySelector(`.npc-ledger-nav a[href="#${section.id}"]`);
      if (link) link.hidden = section.hidden;
      visible += sectionCount;
    }
    empty.hidden = visible !== 0;
    status.textContent = `${visible} ${visible === 1 ? 'entry' : 'entries'} shown`;
  };
  input.addEventListener('input', filter);
  shelf.addEventListener('change', filter);
  tools.querySelector('.ledger-reset').addEventListener('click', () => {
    input.value = '';
    shelf.value = 'all';
    filter();
    input.focus();
  });
  tools.hidden = false;
  filter();
})();
