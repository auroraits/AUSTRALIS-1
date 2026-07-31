# CM5 Staging Node Install

**Revision:** 2026-07-31
**Estado:** Active

Use this path for staging measurements on Raspberry Pi CM5/Linux with
llama.cpp. The central dashboard runs elsewhere unless a local development
case is intentionally configured.

## Guardrails

- Do not run heavy inference by default.
- Check health and live telemetry before queueing inference.
- Monitor temperature, throttling, RAM, and swap.
- Do not infer watts unless a real power source reports them.
- Stop tests if thermal or power-path behavior is unsafe.

## Recommended Runtime

The current CM5 operational baseline is llama.cpp:

- reproducible benchmark API mode: `/completion`;
- template: raw Gemma prompt with final-channel prefill;
- export the model identity/hash, llama.cpp version, context, KV cache,
  threads, and endpoint mode.

## Start the Remote Node Agent

From the suite directory on the CM5:

```bash
python3 agent/australis_benchmark_agent.py \
  --host 0.0.0.0 \
  --port 8765 \
  --node-name staging-node-a \
  --stage staging \
  --node-type cm5 \
  --runtime llama.cpp \
  --model gemma4:e2b-q8_0 \
  --inference-endpoint http://127.0.0.1:8082 \
  --runtime-process-hint llama-server
```

In the central dashboard, register:

```text
Agent endpoint: http://<cm5-host>:8765
Inference endpoint: http://127.0.0.1:8082
Runtime: llama.cpp
```

The inference URL is interpreted by the CM5 agent, so localhost refers to the
CM5 rather than the central dashboard PC.

## Telemetry-Only CM5

To characterize the host without allowing inference through the benchmark
agent:

```bash
python3 agent/australis_benchmark_agent.py \
  --host 0.0.0.0 \
  --node-name staging-telemetry-a \
  --stage staging \
  --node-type cm5 \
  --telemetry-only
```

Health metadata advertises `role = telemetry-only`. The dashboard must keep
inference capability and enablement false for this registry entry.

## CM5 Telemetry

The agent attempts:

- `vcgencmd measure_temp`;
- `vcgencmd get_throttled`;
- `vcgencmd pmic_read_adc`;
- process RSS via optional `psutil`;
- CPU, RAM, swap, and disk via optional `psutil`.

If a source is absent, its field remains unavailable. PMIC text is retained as
reported, but the agent does not derive power from voltage-only readings.

## Minimum CM5 Regression

1. Start llama.cpp with the declared benchmark profile.
2. Start the remote node agent.
3. Register it in the central dashboard and run its health check.
4. Confirm CM5 telemetry is associated with that node name.
5. Run E05, E09, and E12 with `repeats=1`.
6. Inspect lifecycle markers and interval telemetry per run.
7. Export the central session bundle.
8. Review temperature, throttling, warnings, and pass/fail before increasing
   repeats or concurrency.
