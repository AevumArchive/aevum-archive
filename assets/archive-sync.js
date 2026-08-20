(() => {
  const endpoint = document.body.dataset.archiveEndpoint || '/aevum-archive/data/archive-public.json';
  const number = new Intl.NumberFormat('en-US');
  const normalize = (value) => String(value || '').trim().toLowerCase().replace(/[_ ]+/g, '-');

  const setStatus = (message) => {
    document.querySelectorAll('[data-archive-sync-status]').forEach((node) => {
      node.textContent = message;
    });
  };

  const applyCharacters = (characters) => {
    const byId = new Map(characters.map((character) => [normalize(character.id), character]));
    document.querySelectorAll('[data-archive-character-id]').forEach((record) => {
      const character = byId.get(normalize(record.dataset.archiveCharacterId));
      if (!character) return;
      record.querySelectorAll('[data-archive-field]').forEach((field) => {
        const key = field.dataset.archiveField;
        if (Object.prototype.hasOwnProperty.call(character, key)) {
          field.textContent = key === 'powerLevel' ? number.format(character[key]) : String(character[key]);
        }
      });
    });
  };

  const applyLeaderboard = (entries) => {
    document.querySelectorAll('[data-archive-leaderboard-list]').forEach((list) => {
      list.replaceChildren();
      if (!entries.length) {
        const empty = document.createElement('li');
        empty.className = 'archive-live-empty';
        empty.textContent = 'No signed server ranking has been published yet.';
        list.append(empty);
        return;
      }
      entries.slice(0, 10).forEach((entry) => {
        const item = document.createElement('li');
        const rank = document.createElement('span');
        const name = document.createElement('strong');
        const power = document.createElement('em');
        rank.textContent = String(entry.rank).padStart(2, '0');
        name.textContent = String(entry.name || 'Unnamed record');
        power.textContent = `${number.format(Math.max(0, Number(entry.powerLevel) || 0))} PL`;
        item.append(rank, name, power);
        list.append(item);
      });
    });
  };

  fetch(endpoint, { cache: 'no-store', credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw new Error(`Archive request failed: ${response.status}`);
      return response.json();
    })
    .then((archive) => {
      if (!archive || archive.schemaVersion !== 1 || !Array.isArray(archive.characters)
          || !Array.isArray(archive.leaderboard)) {
        throw new Error('Unsupported public archive schema');
      }
      const playerCount = Math.max(0, Number(archive.playerCount) || 0);
      document.querySelectorAll('[data-archive-player-count]').forEach((node) => {
        node.textContent = number.format(playerCount);
      });
      applyCharacters(archive.characters);
      applyLeaderboard(archive.leaderboard);
      const generated = archive.generatedAt ? new Date(archive.generatedAt) : null;
      setStatus(generated && !Number.isNaN(generated.getTime())
        ? `Public snapshot · ${generated.toLocaleString()}`
        : 'Awaiting signed publication');
    })
    .catch(() => setStatus('Public snapshot unavailable'));
})();