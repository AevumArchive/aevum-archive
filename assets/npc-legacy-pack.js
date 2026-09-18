(() => {
  const page = document.querySelector('[data-izumi-form]');
  if (!page) return;

  const controls = [...page.querySelectorAll('[data-izumi-control]')];
  const forms = [...page.querySelectorAll('[data-izumi-form-card]')];

  const showForm = (form) => {
    page.dataset.izumiForm = form;
    controls.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.izumiControl === form)));
    forms.forEach((card) => { card.hidden = card.dataset.izumiFormCard !== form; });
  };

  controls.forEach((button) => button.addEventListener('click', () => showForm(button.dataset.izumiControl)));
  showForm(page.dataset.izumiForm || 'masked');
})();
