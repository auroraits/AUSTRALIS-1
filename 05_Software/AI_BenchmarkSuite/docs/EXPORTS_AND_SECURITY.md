# Exports and Security

**Revision:** 2026-07-31
**Estado:** Active

## Export Bundle v0.2

The central exporter creates:

```text
manifest.json
results.jsonl
results.csv
events.jsonl
telemetry.jsonl
prompts/
raw_responses/
scoring.json
config.sanitized.json
report.md
```

`manifest.json` identifies:

- suite version;
- generated timestamp;
- session ID;
- distributed dashboard architecture;
- source documents;
- evidence-only status.

Each result can include:

- queue and terminal status;
- node, model, and runtime;
- prompt and satellite snapshot;
- normalized and raw response;
- parsed JSON and parse error;
- structured hard fails and soft warnings;
- expected/prohibited tool findings;
- rule explanations;
- run lifecycle events;
- telemetry samples and summary for the run interval.

`events.jsonl` is the session-level event stream. The same events remain nested
under their run in `results.jsonl`.

## Sanitization

Both browser fallback export and Python ZIP export redact object keys
containing:

- `secret`;
- `password`;
- `authorization`;
- `api_key` / `apikey`;
- `access_token`;
- `auth_token`;
- `agent_token`;
- `bearer_token`.

Token-count metric names such as `generated_tokens` are not credentials and are
preserved.

The Python exporter sanitizes manifest, results, telemetry, events, scoring,
responses, prompts, and config objects before writing them. Do not put secrets
inside free-form strings such as node names, model names, notes, prompts, or
raw model output; key-based redaction cannot safely infer arbitrary text.

## Central Export Selection

The browser tries exporters in this order:

1. the dashboard page origin;
2. unique registered node-agent endpoints;
3. sanitized session JSON fallback.

Use a `--dashboard-only` central host when ZIP export must not depend on a
benchmark node.

## Browser Registry

Node configuration is stored in browser local storage under a v0.2 key. It can
contain lab endpoints and operator notes. Do not put credentials in endpoint
URLs, notes, tags, or node names.

## Network Security

The dependency-light development agent:

- has no authentication;
- permits cross-origin HTTP requests;
- exposes host metadata and telemetry;
- can proxy inference when that capability is enabled;
- can package submitted benchmark artifacts.

Run it only on a controlled benchmark network. Use host firewall rules and
network segmentation. Do not expose port 8765 to the public Internet.

`--telemetry-only` prevents inference at the agent protocol boundary.
`--dashboard-only` prevents telemetry and inference at the protocol boundary.
A disabled capability returns HTTP 409.

These role gates are operational controls, not an authentication system.

## Public Repo Rules

Allowed:

- localhost endpoints used as examples;
- reserved `.example` hostnames;
- sanitized configs and documentation;
- model aliases without private filesystem paths.

Not allowed:

- real access tokens or credentials;
- mandatory private-LAN addresses;
- private filesystem paths;
- generated exports, model weights, binaries, or caches;
- claims of flight readiness or flight validation.

## Evidence Wording

Use:

- "benchmark evidence";
- "candidate";
- "pre-staging";
- "staging measurement";
- "CM5 hardware measurement";
- "unavailable" for missing sensors.

Avoid:

- "validated for flight";
- "flight-ready";
- "qualified";
- invented power or energy;
- inferred thermal margin without measurement.
