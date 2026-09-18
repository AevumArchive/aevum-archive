(() => {
  const controls = [...document.querySelectorAll("[data-timeo-control]")];
  const cards = [...document.querySelectorAll("[data-timeo-form]")];
  if (!controls.length || !cards.length) return;

  const showForm = (form) => {
    document.body.dataset.timeoForm = form;
    controls.forEach((control) => {
      control.setAttribute("aria-pressed", String(control.dataset.timeoControl === form));
    });
    cards.forEach((card) => {
      card.hidden = card.dataset.timeoForm !== form;
    });
  };

  controls.forEach((control) => {
    control.addEventListener("click", () => showForm(control.dataset.timeoControl));
  });

  showForm("rampage");
})();
