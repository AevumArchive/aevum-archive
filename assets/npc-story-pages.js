document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".route-npcs-uwu");
  if (!page) return;

  const controls = [...document.querySelectorAll("[data-uwu-control]")];
  controls.forEach((control) => {
    control.addEventListener("click", () => {
      const state = control.dataset.uwuControl;
      page.dataset.uwuState = state;
      controls.forEach((item) => {
        item.setAttribute("aria-pressed", String(item.dataset.uwuControl === state));
      });
    });
  });
});
