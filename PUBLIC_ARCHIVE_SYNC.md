# Public archive synchronization

The website reads `data/archive-public.json`. That file is intentionally public and contains only schema-versioned DTO fields.

`AevumCore` creates the local export with `/aevum archive publish` (alias: `/aevum admin archive export`). Remote publishing is opt-in. The configured HTTPS receiver must verify `X-Aevum-Signature` with HMAC-SHA256, reject stale `X-Aevum-Timestamp` values, validate `X-Aevum-Schema-Version`, then atomically replace this JSON file and deploy the site.

Never place the signing secret in this repository or browser JavaScript. The plugin reads it only from the configured environment variable. Character records are opt-in through `archive-sync.public-character-ids`; an empty list exports no characters.