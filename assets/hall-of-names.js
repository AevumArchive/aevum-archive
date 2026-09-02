(() => {
  const grid = document.querySelector('#hall-card-grid');
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll('.hall-card'));
  const filters = Array.from(document.querySelectorAll('.hall-filter'));
  const views = Array.from(document.querySelectorAll('.hall-view'));
  const search = document.querySelector('#hall-search');
  const sort = document.querySelector('#hall-sort');
  const pagination = document.querySelector('#hall-pagination');
  const summary = document.querySelector('#hall-results-summary');
  const empty = document.querySelector('#hall-empty');
  const pageSize = 10;
  const statusOrder = { active: 0, sealed: 1, fallen: 2, retired: 3 };

  let activeFilter = 'all';
  let activePage = 1;

  const normalizedName = (card) => (card.dataset.name || '').toLocaleLowerCase('en');

  const filteredCards = () => {
    const query = (search?.value || '').trim().toLocaleLowerCase('en');
    return cards.filter((card) => {
      const statusMatches = activeFilter === 'all' || card.dataset.status === activeFilter;
      const textMatches = !query || `${card.dataset.name} ${card.textContent}`.toLocaleLowerCase('en').includes(query);
      return statusMatches && textMatches;
    });
  };

  const sortedCards = (records) => records.sort((a, b) => {
    if (sort?.value === 'name-desc') return normalizedName(b).localeCompare(normalizedName(a));
    if (sort?.value === 'status') {
      const statusDifference = statusOrder[a.dataset.status] - statusOrder[b.dataset.status];
      return statusDifference || normalizedName(a).localeCompare(normalizedName(b));
    }
    return normalizedName(a).localeCompare(normalizedName(b));
  });

  const pageButton = (label, page, options = {}) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.disabled = Boolean(options.disabled);
    if (options.current) button.setAttribute('aria-current', 'page');
    if (options.label) button.setAttribute('aria-label', options.label);
    button.addEventListener('click', () => {
      activePage = page;
      render();
      grid.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
    return button;
  };

  const renderPagination = (pageCount) => {
    pagination.replaceChildren();
    if (pageCount <= 1) return;

    pagination.append(pageButton('‹', Math.max(1, activePage - 1), {
      disabled: activePage === 1,
      label: 'Previous character page'
    }));

    for (let page = 1; page <= pageCount; page += 1) {
      pagination.append(pageButton(String(page), page, {
        current: page === activePage,
        label: `Character page ${page}`
      }));
    }

    pagination.append(pageButton('›', Math.min(pageCount, activePage + 1), {
      disabled: activePage === pageCount,
      label: 'Next character page'
    }));
  };

  const render = () => {
    const matches = sortedCards(filteredCards());
    const pageCount = Math.max(1, Math.ceil(matches.length / pageSize));
    activePage = Math.min(activePage, pageCount);
    const first = (activePage - 1) * pageSize;
    const visible = new Set(matches.slice(first, first + pageSize));

    sortedCards(cards).forEach((card) => grid.append(card));
    cards.forEach((card) => { card.hidden = !visible.has(card); });

    empty.hidden = matches.length !== 0;
    grid.hidden = matches.length === 0;
    summary.textContent = matches.length
      ? `Showing ${Math.min(pageSize, matches.length - first)} of ${matches.length} matching record${matches.length === 1 ? '' : 's'}`
      : 'No matching records';
    renderPagination(pageCount);
  };

  filters.forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.filter || 'all';
      activePage = 1;
      filters.forEach((item) => {
        const selected = item === button;
        item.classList.toggle('is-active', selected);
        item.setAttribute('aria-pressed', String(selected));
      });
      render();
    });
  });

  views.forEach((button) => {
    button.addEventListener('click', () => {
      const listView = button.dataset.view === 'list';
      grid.classList.toggle('is-list', listView);
      views.forEach((item) => {
        const selected = item === button;
        item.classList.toggle('is-active', selected);
        item.setAttribute('aria-pressed', String(selected));
      });
    });
  });

  search?.addEventListener('input', () => {
    activePage = 1;
    render();
  });

  sort?.addEventListener('change', () => {
    activePage = 1;
    render();
  });

  render();
})();
