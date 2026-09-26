(() => {
  const library = document.querySelector('[data-library]');
  if (!library || library.dataset.ready) return;
  library.dataset.ready = 'true';

  const search = library.querySelector('[data-library-search]');
  const buttons = [...library.querySelectorAll('button[data-topic]')];
  const cards = [...library.querySelectorAll('[data-library-card]')];
  const counter = library.querySelector('[data-library-count]');
  const empty = library.querySelector('[data-library-empty]');
  const normalize = (value) => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[đĐ]/g, 'd').toLowerCase();
  const entries = cards.map((card) => ({ card, text: normalize(card.textContent) }));
  let topic = 'all';

  function render() {
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    entries.forEach(({ card, text }) => {
      const matches = (topic === 'all' || card.dataset.topic === topic) && terms.every((term) => text.includes(term));
      card.hidden = !matches;
      if (matches) count += 1;
    });
    buttons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.topic === topic)));
    counter.textContent = `${count} bài viết${count !== cards.length ? ` / ${cards.length}` : ''}`;
    empty.hidden = count !== 0;
  }

  function readHash() {
    const hash = window.location.hash.slice(1);
    topic = buttons.some((button) => button.dataset.topic === hash) ? hash : 'all';
    render();
  }

  buttons.forEach((button) => button.addEventListener('click', () => {
    topic = button.dataset.topic;
    const url = new URL(window.location.href);
    url.hash = topic === 'all' ? '' : topic;
    window.history.replaceState(null, '', url);
    render();
  }));
  search.addEventListener('input', render);
  window.addEventListener('hashchange', readHash);
  library.querySelector('[data-library-reset]').addEventListener('click', () => {
    search.value = '';
    buttons[0].click();
    search.focus();
  });
  library.querySelector('[data-library-controls]').hidden = false;
  readHash();
})();
