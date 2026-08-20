(() => {
  function initRaceArchive() {
    const form = document.querySelector('#codex-filters');
    const grid = document.querySelector('#codex-race-grid');
    if (!form || !grid) return;
    const search = document.querySelector('#codex-search');
    const state = document.querySelector('#codex-state');
    const classification = document.querySelector('#codex-classification');
    const style = document.querySelector('#codex-style');
    const empty = document.querySelector('#codex-no-results');
    const records = [...grid.querySelectorAll('.codex-entry')];
    const sealedDivider = document.querySelector('#codex-sealed-divider');

    function applyFilters() {
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      records.forEach((record) => {
        const isUnlocked = record.dataset.state === 'unlocked';
        const stateMatch = state.value === 'all' || record.dataset.state === state.value;
        const classMatch = classification.value === 'all' || record.dataset.classification === classification.value;
        const styleMatch = style.value === 'all' || (record.dataset.styles || '').split(' ').includes(style.value);
        const queryMatch = !query || (isUnlocked && (record.dataset.search || '').includes(query));
        const show = stateMatch && classMatch && styleMatch && queryMatch;
        record.hidden = !show;
        if (show) visible += 1;
      });
      empty.hidden = visible !== 0;
      if (sealedDivider) sealedDivider.hidden = Boolean(query) || state.value === 'unlocked' || classification.value !== 'all' || style.value !== 'all';
    }

    form.addEventListener('input', applyFilters);
    form.addEventListener('change', applyFilters);
    form.addEventListener('reset', () => requestAnimationFrame(applyFilters));
  }

  function createLockedTrait(recordNumber) {
    const number = String(recordNumber).padStart(3, '0');
    const article = document.createElement('article');
    article.className = 'codex-entry codex-trait-record is-sealed';
    article.dataset.state = 'sealed';
    article.dataset.category = 'unknown';
    article.dataset.rarity = 'unknown';
    article.dataset.record = number;
    article.dataset.search = 'sealed trait record';
    article.innerHTML = '<span class="codex-entry-top"><span class="status-badge">Sealed</span><span class="codex-classification">Unknown</span></span><span class="codex-lock" aria-hidden="true"><i></i></span><p class="eyebrow">Sealed Trait Record</p><h3>Unknown Trait</h3><p>Discovery required.</p>';
    return article;
  }

  function initTraitArchive() {
    const form = document.querySelector('#trait-filters');
    const grid = document.querySelector('#codex-trait-grid');
    if (!form || !grid) return;
    const placeholderStart = Number(grid.dataset.placeholderStart || 13);
    const placeholderCount = Number(grid.dataset.placeholderCount || 0);
    const fragment = document.createDocumentFragment();
    for (let index = 0; index < placeholderCount; index += 1) fragment.append(createLockedTrait(placeholderStart + index));
    grid.append(fragment);

    const search = document.querySelector('#trait-search');
    const state = document.querySelector('#trait-state');
    const category = document.querySelector('#trait-category');
    const rarity = document.querySelector('#trait-rarity');
    const sort = document.querySelector('#trait-sort');
    const empty = document.querySelector('#trait-no-results');
    const count = document.querySelector('#trait-result-count');
    const records = [...grid.querySelectorAll('.codex-trait-record')];
    const comparators = {
      archive: (left, right) => Number(left.dataset.record) - Number(right.dataset.record),
      reverse: (left, right) => Number(right.dataset.record) - Number(left.dataset.record),
      name: (left, right) => (left.dataset.name || 'zzzz').localeCompare(right.dataset.name || 'zzzz') || Number(left.dataset.record) - Number(right.dataset.record),
      category: (left, right) => (left.dataset.category || 'unknown').localeCompare(right.dataset.category || 'unknown') || Number(left.dataset.record) - Number(right.dataset.record)
    };

    function applyFilters() {
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      records.forEach((record) => {
        const show = (state.value === 'all' || record.dataset.state === state.value)
          && (category.value === 'all' || record.dataset.category === category.value)
          && (rarity.value === 'all' || record.dataset.rarity === rarity.value)
          && (!query || (record.dataset.search || '').includes(query));
        record.hidden = !show;
        if (show) visible += 1;
      });
      records.sort(comparators[sort.value] || comparators.archive).forEach((record) => grid.append(record));
      empty.hidden = visible !== 0;
      count.textContent = visible === 0 ? 'No matching records' : 'Witnessed and sealed records';
    }

    form.addEventListener('input', applyFilters);
    form.addEventListener('change', applyFilters);
    form.addEventListener('reset', () => requestAnimationFrame(applyFilters));
    applyFilters();
  }

  initRaceArchive();
  initTraitArchive();
})();
