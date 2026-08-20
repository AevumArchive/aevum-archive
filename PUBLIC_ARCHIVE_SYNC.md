# Public archive synchronization

The website reads `data/archive-public.json`. That file is intentionally public and contains only schema-versioned DTO fields.

`AevumCore` creates the local export with `/aevum archive publish` (alias: `/aevum admin archive export`). Remote publishing is opt-in. The configured HTTPS receiver must verify `X-Aevum-Signature` with HMAC-SHA256, reject stale `X-Aevum-Timestamp` values, validate `X-Aevum-Schema-Version`, then atomically replace this JSON file and deploy the site.

Never place the signing secret in this repository or browser JavaScript. The plugin reads it only from the configured environment variable. Character records are opt-in through `archive-sync.public-character-ids`; an empty list exports no characters.
## Adjusting a public Power Level

Preferred server workflow:

```text
/aevum character set thren-valis power-level 800000
/aevum archive publish
```

The character ID must also be present in `archive-sync.public-character-ids`. The signed snapshot updates matching power labels, comparison bars and recorded gaps on the website after the receiver deploys `data/archive-public.json`.

For an emergency static-only edit, change the displayed value and its comparison values in `leaderboard/index.html`. Server publication is preferred because it keeps the public JSON, live ledger and visible profile in agreement.