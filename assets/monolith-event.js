(() => {
  const event = document.querySelector('[data-monolith-event]');
  if (!event) return;
  const start = Date.parse(event.dataset.eventStart);
  const end = Date.parse(event.dataset.eventEnd);
  const timer = event.querySelector('[role="timer"]');
  const label = event.querySelector('[data-event-label]');
  const slots = [...timer.querySelectorAll('span')];

  const tick = () => {
    const now = Date.now();
    if (now >= end) {
      label.textContent = 'World Event · Ended';
      timer.textContent = 'Event ended';
      return false;
    }
    const upcoming = now < start;
    label.textContent = upcoming ? 'World Event · Upcoming' : 'World Event · Live';
    timer.setAttribute('aria-label', upcoming ? 'Time until the event starts' : 'Time remaining');
    const remaining = Math.ceil(((upcoming ? start : end) - now) / 1000);
    const values = [Math.floor(remaining / 86400), Math.floor(remaining / 3600) % 24,
      Math.floor(remaining / 60) % 60, remaining % 60];
    slots.forEach((slot, index) => {
      slot.textContent = String(values[index]).padStart(2, '0') + ['d', 'h', 'm', 's'][index];
    });
    return true;
  };

  if (tick()) {
    const interval = window.setInterval(() => {
      if (!tick()) window.clearInterval(interval);
    }, 1000);
  }
})();
