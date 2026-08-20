(() => {
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
      // Search is intentionally limited to opened public records.
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
})();
