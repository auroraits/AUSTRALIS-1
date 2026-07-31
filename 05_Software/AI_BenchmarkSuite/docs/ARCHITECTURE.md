# Architecture

**Revision:** 2026-07-31
**Estado:** Active

## v0.2 Responsibility Split

The central dashboard and benchmark nodes are separate responsibilities.

```text
Central host
  - serves static console and scenario pack
  - builds export ZIP
  - does not need telemetry or inference

Browser console
  - persists the node registry locally
  - orchestrates the distributed queue
  - consumes remote SSE telemetry
  - creates client-side lifecycle events
  - scores normalized output
  - presents and exports evidence

Remote node agent
  - advertises capabilities and node metadata
  - collects telemetry from its own host
  - optionally proxies inference to its own runtime

Inference runtime
  - Ollama, llama.cpp, or OpenAI-compatible service
  - addressed from the node agent, not from the browser
```

The same dependency-light Python program can run in three roles:

| Role | Static/scenario/export | Telemetry | Inference |
|---|---:|---:|---:|
| default `telemetry+inference` | yes | yes | yes |
| `--telemetry-only` | yes | yes | no |
| `--dashboard-only` | yes | no | no |

Static/scenario/export support on node roles preserves v0.1 local development
compatibility. It is not an architectural requirement for the central
dashboard to be a benchmark node.

## Node Model

The central registry keeps configured and discovered state separate:

| Field | Meaning |
|---|---|
| `name` | unique operator-facing node name |
| `stage` | `pre-staging` or `staging` |
| `type` | PC, CM5, or other host class |
| `agent_endpoint` | remote unified-protocol base URL |
| `telemetry_capability` | agent advertises telemetry support |
| `telemetry_enabled` | dashboard should subscribe |
| `inference_capability` | agent advertises inference support |
| `inference_enabled` | dashboard should schedule runs |
| `inference_endpoint` | runtime URL resolved by the node agent |
| `runtime` / `model` | configured runtime identity |
| `enabled` | fleet-level operator enablement |
| `notes` / `tags` | local registry annotations |
| `last_health` | latest result, latency, agent version, role, and timestamp |

Names are case-insensitively unique. Internal IDs keep telemetry and historical
runs associated if a node is renamed.

## Unified Agent API

| Method | Path | Capability | Purpose |
|---|---|---|---|
| GET | `/api/health` | all roles | lightweight liveness and capabilities |
| GET | `/api/status` | all roles | metadata plus current telemetry when enabled |
| GET | `/api/metadata` | all roles | role, host, node, runtime, and capabilities |
| GET | `/api/scenarios/australis` | scenario pack | built-in deterministic scenarios |
| GET | `/api/telemetry/stream` | telemetry | remote-node SSE stream |
| POST | `/api/infer` | inference | node-local inference proxy |
| POST | `/api/export-bundle` | export bundle | sanitized ZIP export |

Capability metadata shape:

```json
{
  "role": "telemetry+inference",
  "capabilities": {
    "telemetry": {
      "available": true,
      "transport": "sse",
      "endpoint": "/api/telemetry/stream"
    },
    "inference": {
      "available": true,
      "endpoint": "/api/infer",
      "runtimes": ["ollama", "llama.cpp", "openai-compatible"]
    },
    "scenario_pack": {
      "available": true,
      "endpoint": "/api/scenarios/australis"
    },
    "export_bundle": {
      "available": true,
      "endpoint": "/api/export-bundle"
    }
  }
}
```

A capability-disabled endpoint returns HTTP 409 with
`error.code = capability_disabled`.

## Multi-Node Queue

The browser expands one queue item per:

```text
enabled inference node
  x selected episode
  x selected sweep value
  x repeat
```

A shared worker pool enforces global concurrency. Per-node progress is derived
from queued/running/terminal run state. The queue never calls `/api/infer` on a
node whose inference capability or operator inference enablement is false.

The browser owns cancellation. Abort controllers stop active requests and mark
unstarted work as aborted. Dashboard timeout adds a small transport allowance
to the timeout already passed to the node proxy.

## Run Event Model

Events are part of each run and are also exported as a session-level stream:

| Event | Source |
|---|---|
| `queued` | queue expansion |
| `inference_start` | worker acquisition |
| `request_sent` | before browser-to-agent fetch |
| `first_byte_or_first_token` | runtime metric, only when available |
| `response_received` | agent response body received |
| `generation_complete` | successful normalized response |
| `scoring_complete` | deterministic scorer completed |
| `timeout` | agent or dashboard timeout |
| `error` | transport, proxy, or inference failure |
| `abort` | operator cancellation |

Each event contains run ID, node ID/name, episode, UTC timestamp, elapsed run
time, duration since the previous event, and optional details.

## Telemetry Model

SSE samples remain tagged with the registry node ID and name. The console
maintains:

- bounded per-node history for rendering and run interval selection;
- bounded session history for export;
- separate runtime-performance points for latency, tokens/s, and energy;
- a metric registry that returns `null` for absent values.

The chart uses one horizontal track per selected metric and one color per node.
Percent, temperature, memory, and positive-only values use explicit domains.
Missing data is labeled unavailable and is never replaced with zero.

Run telemetry contains only samples whose timestamps fall between
`started_utc` and `completed_utc`.

## Inference Normalization

Normalized metrics:

- latency;
- prompt tokens;
- generated tokens;
- total tokens;
- generated tokens/s;
- optional first-token timing;
- errors;
- timeouts;
- raw response.

The proxy supports common response shapes from Ollama, llama.cpp completion,
and OpenAI-compatible chat completions.

## Scoring Model

The score retains the v0.1 weighting:

- JSON valid: +35;
- required contract fields: +20;
- expected tools: +20;
- valid supervisor expectation: +10;
- behavior log present: +10;
- no hard fails: +5;
- hard fails subtract 25 each;
- soft warnings subtract 5 each.

The v0.2 result also records structured details:

- missing required fields;
- expected tools found and missing;
- prohibited tools detected;
- hard-fail ID, rule, and explanation;
- soft-warning ID, rule, and explanation;
- pass/warn/fail rule explanations;
- configured latency and throughput warnings;
- telemetry coverage warnings.

Pass requires a successful proxy response, valid JSON, all required fields,
expected tools, and no hard fail.

## Central Hosting and Fallbacks

The preferred central host is:

```bash
python agent/australis_benchmark_agent.py --dashboard-only
```

The console can also be served by a generic static server from the suite root.
It first loads the relative scenario JSON and then tries the host API. ZIP
export first tries the central host and then registered agents. If none is
reachable, the browser emits a sanitized session JSON instead.

## Boundaries

This suite is EGSE/benchmark software. It does not modify flight software,
energize hardware, transmit RF, or publish artifacts. The development protocol
has no authentication; use a controlled lab network.
