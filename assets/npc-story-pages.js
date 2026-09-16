document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".route-npcs-uwu");
  if (!page) return;

  const controls = [...document.querySelectorAll("[data-uwu-control]")];
  const states = [...document.querySelectorAll(".uwu-state-card[data-state]")];
  controls.forEach((control) => {
    control.addEventListener("click", () => {
      const state = control.dataset.uwuControl;
      page.dataset.uwuState = state;
      states.forEach((item) => {
        item.hidden = item.dataset.state !== state;
      });
      controls.forEach((item) => {
        item.setAttribute("aria-pressed", String(item.dataset.uwuControl === state));
      });
    });
  });
});
