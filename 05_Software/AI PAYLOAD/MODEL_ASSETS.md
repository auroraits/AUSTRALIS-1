# AI model assets and evidence policy

**Revision:** 2026-07-27
**Status:** Active policy

The public repository does not vendor model weights, tokenizer artifacts,
adapters or generated checkpoints. A model name alone is not reproducible
evidence: every benchmark must bind the exact bytes, runtime and configuration
used.

## Current model roles

- `gemma4:e2b`: primary **bench candidate** for the next comparison and CM5
  characterization. It is not a validated baseline, flight model or
  flight-ready component.
- Granite 350M: deferred for a later work package. No current AUSTRALIS result
  validates this model.
- `ibm-granite/granite-3.1-2b-instruct`: model actually referenced by the
  historical March training, benchmark and holdout scripts. Those artifacts
  may be studied as legacy 2B experiments, but are inadmissible as evidence for
  Granite 350M or for a flight candidate.
- Other models: comparison controls only unless an Accepted ADR assigns a role.

The governing decision is
`08_Decisions/ADR-20260727-ai-payload-gemma4-e2b-candidate.md`.

## Historical Granite disposition

The following scripts hard-code Granite 3.1 2B:

- `train_granite_lora_v2.py`
- `benchmark_granite_lora_vs_base_corrected.py`
- `test_granite_lora_holdout.py`

They are retained for provenance. Their scorer, dataset split and holdout do
not meet the current scientific protocol, and they must not be cited as
validation. The associated evidence file records the audit disposition.

## Public tree policy

Keep in Git:

- source code, schemas and test suites;
- project-authored datasets whose provenance and license permit publication;
- immutable manifests, raw-result checksums and analysis scripts;
- negative tests and acceptance criteria.

Do not keep in Git:

- model or tokenizer directories;
- adapters and checkpoints;
- `*.safetensors`, `*.gguf`, `*.bin`, `*.pt` or `*.pth`;
- private credentials, operator keys or unreviewed third-party datasets.

## Required evidence manifest

Every run proposed as evidence must record at least:

- public model identifier, exact digest/hash and upstream revision;
- tokenizer/template digest and adapter digest, if any;
- quantization, context length, decoding parameters, seed and repeat index;
- runtime name/version, dependency lock, OS/kernel and source commit;
- suite/protocol/dataset/holdout hashes;
- host identifier and hardware configuration;
- raw prompt, raw response, parsed response and deterministic evaluation;
- wall time, memory, input/output token counts;
- input power, energy per inference and relevant temperatures when measured;
- start/end timestamps and any throttling, undervoltage or runtime warning.

Generated evidence belongs in an immutable run directory referenced by a
manifest checksum. Aggregate tables without the raw artifacts are diagnostic,
not closure evidence.

## Promotion gates

`gemma4:e2b` can only advance beyond bench candidate after:

1. a preregistered benchmark with a blind, contamination-checked holdout;
2. zero hard safety failures at the approved sample size and confidence bound;
3. reproducible CM5 latency, memory, power and thermal measurements;
4. deterministic OBC supervisor integration and fault-injection tests;
5. exact license, provenance and supply-chain review of the model artifact;
6. an Accepted ADR that cites the immutable evidence.

Until then, documentation must use “candidate” or “experiment”, never
“validated baseline”.
