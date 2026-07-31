# CM5 Staging Install

**Revision:** 2026-07-31
**Estado:** Active

Use this path for flight-like staging on Raspberry Pi CM5/Linux with llama.cpp.

## Guardrails

- Do not run heavy inference by default.
- First run `health/status`.
- Monitor temperature, throttling, RAM and swap.
- Do not infer watts unless a real power sensor is connected and reported.
- Stop tests if thermal or power path behavior is unsafe.

## Recommended Runtime

The current CM5 operational baseline is llama.cpp:

- API mode for reproducible benchmark: `/completion`.
- Template: raw Gemma prompt with final-channel prefill.
- Record model path/hash, llama.cpp version, context, KV cache, threads and
  endpoint mode in the export.

## Start Agent

From the suite directory on the CM5:

```bash
python3 agent/australis_benchmark_agent.py \
  --host 0.0.0.0 \
  --port 8765 \
  --node-name cm5-bench-1 \
  --stage staging \
  --node-type cm5 \
  --runtime llama.cpp \
  --model gemma4:e2b-q8_0 \
  --inference-endpoint http://127.0.0.1:8082 \
  --runtime-process-hint llama-server
```

Then open the console from a PC:

```text
http://<cm5-host>:8765/
```

Or add the CM5 as a remote node from another console:

```text
Agent endpoint: http://<cm5-host>:8765
Inference endpoint: http://127.0.0.1:8082
Runtime: llama.cpp
```

The inference endpoint is interpreted by the agent running on that node, so
`127.0.0.1` points to the CM5 when the agent is on the CM5.

## CM5 Telemetry

The agent attempts:

- `vcgencmd measure_temp`
- `vcgencmd get_throttled`
- `vcgencmd pmic_read_adc`
- process RSS via optional `psutil`
- RAM/swap/disk via optional `psutil`

If any source is absent, the field remains unavailable. The agent does not
invent power.

## Minimum CM5 Regression

1. Start llama.cpp with the benchmark profile.
2. Start the node agent.
3. Confirm `Health`.
4. Run E05/E09/E12 with `repeats=1`.
5. Export bundle.
6. Inspect temperature, throttling and pass/fail before increasing repeats.
