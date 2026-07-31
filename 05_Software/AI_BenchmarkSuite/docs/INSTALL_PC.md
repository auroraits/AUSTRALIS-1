# PC Pre-Staging Install

**Revision:** 2026-07-31
**Estado:** Active

Use this path for desktop or laptop benchmarking before CM5 staging.

## Requirements

- Python 3.9+
- A local inference runtime:
  - Ollama, or
  - llama.cpp server, or
  - an OpenAI-compatible local server
- Optional: `psutil` for richer telemetry.

Optional dependency:

```bash
python -m pip install -r agent/requirements-optional.txt
```

The suite runs without `psutil`; telemetry will be reduced.

## Start With Ollama

From `05_Software/AI_BenchmarkSuite`:

```bash
python agent/australis_benchmark_agent.py \
  --node-name local-pc \
  --stage pre-staging \
  --node-type pc-linux \
  --runtime ollama \
  --model gemma4:e2b \
  --inference-endpoint http://127.0.0.1:11434
```

Windows PowerShell equivalent:

```powershell
python .\agent\australis_benchmark_agent.py --node-name local-pc --stage pre-staging --node-type pc-windows --runtime ollama --model gemma4:e2b --inference-endpoint http://127.0.0.1:11434
```

Open:

```text
http://127.0.0.1:8765/
```

## Start With llama.cpp

If `llama-server` exposes `/completion`:

```bash
python agent/australis_benchmark_agent.py \
  --runtime llama.cpp \
  --model gemma4:e2b-q8_0 \
  --inference-endpoint http://127.0.0.1:8082
```

The console renders a Gemma-style final-channel raw prompt for llama.cpp
completion mode.

## Minimum Local Smoke

1. Start the node agent.
2. Open the console.
3. Press `Health`.
4. Select minimum episodes.
5. Run E05/E09/E12 with `repeats=1`.
6. Export the bundle.

Do not compare Ollama and llama.cpp results without declaring runtime, model
identity, context, template, seed and endpoint mode.
