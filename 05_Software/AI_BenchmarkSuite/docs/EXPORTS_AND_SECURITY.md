# Exports And Security

**Revision:** 2026-07-31
**Estado:** Active

## Export Bundle

The export ZIP contains:

```text
manifest.json
results.jsonl
results.csv
telemetry.jsonl
prompts/
raw_responses/
scoring.json
config.sanitized.json
report.md
```

`manifest.json` should identify:

- suite version;
- generated timestamp;
- session id;
- source documents;
- model/runtime/node metadata when available.

## Sanitization

The agent redacts config keys containing:

- `token`
- `secret`
- `password`
- `authorization`
- `api_key`
- `apikey`

Do not place secrets in node names, model names, prompt text or raw responses.

## Public Repo Rules

Allowed:

- localhost endpoints;
- placeholder hostnames;
- example configs;
- sanitized exports;
- model aliases without private paths.

Not allowed:

- tokens;
- private LAN addresses as mandatory defaults;
- credentials;
- undisclosed model weights;
- claims of flight readiness.

## Evidence Wording

Use:

- "benchmark evidence";
- "candidate";
- "pre-staging";
- "staging flight-like";
- "CM5 hardware measurement";
- "unavailable" for missing sensors.

Avoid:

- "validated for flight";
- "flight-ready";
- "qualified";
- invented watts;
- inferred thermal margins without measurement.
