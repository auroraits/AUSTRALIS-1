# PC Install and Central Operations

**Revision:** 2026-07-31
**Estado:** Active

Use a PC either as the central dashboard host, a benchmark node, or both as an
explicit development configuration.

## Requirements

- Python 3.9+;
- optional `psutil` for richer node telemetry;
- an inference runtime only on machines registered for inference.

Optional dependency:

```bash
python -m pip install -r agent/requirements-optional.txt
```

## Central Dashboard PC

From `05_Software/AI_BenchmarkSuite`:

```powershell
python .\agent\australis_benchmark_agent.py --dashboard-only
```

Open `http://127.0.0.1:8765/`.

This process does not collect dashboard-PC telemetry or accept inference. It
serves the static console, deterministic scenarios, and sanitized ZIP export.

To access the dashboard from another trusted lab machine:

```powershell
python .\agent\australis_benchmark_agent.py --dashboard-only --host 0.0.0.0
```

The agent has no authentication. Do not expose it outside the controlled
benchmark network.

## PC Telemetry and Inference Node

Run this on the PC that owns Ollama:

```powershell
python .\agent\australis_benchmark_agent.py `
  --host 0.0.0.0 `
  --node-name prestage-node-a `
  --stage pre-staging `
  --node-type pc-windows `
  --runtime ollama `
  --model gemma4:e2b `
  --inference-endpoint http://127.0.0.1:11434
```

Linux equivalent:

```bash
python agent/australis_benchmark_agent.py \
  --host 0.0.0.0 \
  --node-name prestage-node-a \
  --stage pre-staging \
  --node-type pc-linux \
  --runtime ollama \
  --model gemma4:e2b \
  --inference-endpoint http://127.0.0.1:11434
```

Register `http://<node-host>:8765` in the central dashboard. Keep the
inference endpoint as the URL visible from that agent process.

## PC Telemetry-Only Node

```powershell
python .\agent\australis_benchmark_agent.py `
  --host 0.0.0.0 `
  --node-name telemetry-node-a `
  --node-type pc-windows `
  --telemetry-only
```

Register with:

- telemetry capability enabled;
- inference capability disabled;
- runtime `none`;
- no model or inference endpoint.

The node appears in telemetry and health, but the run queue skips it.

## Generic Static Host

For UI development only, from the suite root:

```bash
python -m http.server 8000
```

Open `http://127.0.0.1:8000/console/`. Relative scenario loading works. The
browser falls back to session JSON if no dashboard/agent ZIP exporter is
reachable.

## Local All-in-One Development

The default agent can still serve the console and act as one registered node:

```powershell
python .\agent\australis_benchmark_agent.py `
  --node-name local-development `
  --node-type pc-windows `
  --runtime ollama `
  --model gemma4:e2b `
  --inference-endpoint http://127.0.0.1:11434
```

Open the console, create a node explicitly, and set its agent endpoint to
`http://127.0.0.1:8765`. The browser machine and node happen to be the same in
this mode; the console does not infer that relationship.

## Minimum Distributed Smoke

1. Start the central dashboard-only host.
2. Start one remote telemetry and inference agent.
3. Optionally start one telemetry-only agent.
4. Register both with unique names.
5. Health-check each node and confirm discovered roles.
6. Select E05, E09, and E12.
7. Run with `repeats=1` and declared global concurrency.
8. Open each run detail and inspect events, warnings, and interval telemetry.
9. Export the ZIP and inspect `events.jsonl`, detailed scoring, and redaction.

Do not compare runtime results without declaring model identity, template,
context, seed, endpoint mode, and node hardware.
