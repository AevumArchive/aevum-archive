(() => {
  const scene = document.querySelector(".kenka-cut");
  const button = document.querySelector(".kenka-cut-button");

  button.addEventListener("click", () => {
    scene.classList.remove("is-cut");
    // Commit the intact state before replaying the CSS animations.
    scene.getBoundingClientRect();
    scene.classList.add("is-cut");
    button.textContent = "Replay the Cut";
  });
  button.hidden = false;
})();
