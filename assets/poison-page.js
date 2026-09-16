(() => {
  const controls = [...document.querySelectorAll("[data-poison-control]")];
  const cards = [...document.querySelectorAll(".poison-form-card[data-form]")];

  if (!controls.length || !cards.length) return;

  const showForm = (form) => {
    document.body.dataset.poisonForm = form;
    controls.forEach((control) => control.setAttribute("aria-pressed", String(control.dataset.poisonControl === form)));
    cards.forEach((card) => { card.hidden = card.dataset.form !== form; });
  };

  controls.forEach((control) => control.addEventListener("click", () => showForm(control.dataset.poisonControl)));
  showForm("female");
})();
