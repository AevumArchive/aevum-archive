(() => {
  "use strict";

  const SITE_ROOT = "/aevum-archive";
  const SESSION_KEY = "aevum.deepArchive.v1";
  const ACCESS_WINDOW_MS = 4 * 60 * 60 * 1000;

  // Canonical assembled cipher. Keep only its hash in the static client.
  const RECORDS_BY_HASH = new Map([
    ["2b6630d837c6ccc9d1ecceb0441cd545559e87f7d7f4bdb266811f46b9d49182", `${SITE_ROOT}/deep-archive/vault.html`]
  ]);

  const normalizeCode = (value) => value.trim().toUpperCase().replace(/[\s_]+/g, "-").replace(/-+/g, "-");

  const digest = async (value) => {
    const bytes = new TextEncoder().encode(value);
    const result = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(result), (byte) => byte.toString(16).padStart(2, "0")).join("");
  };

  const grant = () => {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify({ scope: "deep-archive", expiresAt: Date.now() + ACCESS_WINDOW_MS }));
  };

  const hasAccess = () => {
    try {
      const record = JSON.parse(sessionStorage.getItem(SESSION_KEY) || "null");
      return Boolean(record && record.scope === "deep-archive" && Number(record.expiresAt) > Date.now());
    } catch (_error) {
      return false;
    }
  };

  const protectedRecord = document.body.dataset.restrictedRecord;
  if (protectedRecord) {
    if (!hasAccess()) {
      window.location.replace(`${SITE_ROOT}/deep-archive/?sealed=${encodeURIComponent(protectedRecord)}`);
      return;
    }
  }

  const form = document.querySelector("[data-deep-gate]");
  if (!form) return;

  const input = form.querySelector("input");
  const button = form.querySelector("button");
  const status = document.getElementById("gate-status");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const code = normalizeCode(input.value);
    if (!code) {
      status.textContent = "The terminal requires all three cipher fragments.";
      form.dataset.state = "error";
      input.focus();
      return;
    }

    button.disabled = true;
    status.textContent = "Reading the assembled cipher…";
    form.dataset.state = "reading";

    try {
      const hash = await digest(code);
      const route = RECORDS_BY_HASH.get(hash);
      if (!route) {
        status.textContent = "Cipher rejected. The fragments do not align.";
        form.dataset.state = "error";
        input.select();
        return;
      }
      grant();
      status.textContent = "Cipher accepted. Descending into the Archive…";
      form.dataset.state = "success";
      window.setTimeout(() => window.location.assign(route), 700);
    } catch (_error) {
      status.textContent = "The terminal could not verify this cipher.";
      form.dataset.state = "error";
    } finally {
      button.disabled = false;
    }
  });
})();
