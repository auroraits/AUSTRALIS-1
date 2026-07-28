# Historical AI bench record — 2026-03-16

**Original session date:** 2026-03-16
**Audit disposition:** Historical / invalidated as validation evidence
**Disposition date:** 2026-07-27

This file preserves provenance of the March experiment. It does **not**
establish a functional baseline, validate Granite 350M, demonstrate safety or
support flight-readiness claims.

## Audit determination

The original interpretation is withdrawn for the following independent
reasons.

### 1. Model attribution mismatch

The training, benchmark and holdout programs reference
`ibm-granite/granite-3.1-2b-instruct`, not Granite 350M:

- `train_granite_lora_v2.py`
- `benchmark_granite_lora_vs_base_corrected.py`
- `test_granite_lora_holdout.py`

Therefore no latency, quality, memory, energy or compatibility result from this
session may be attributed to Granite 350M. The existing numbers are, at most,
historical Granite 3.1 2B observations on an incompletely captured host.

### 2. Training/holdout contamination

Static analysis of `cubesat_granite_v3_1800.jsonl` found:

- 1,715 rows, 1,204 unique prompts and 511 exact prompt repetitions;
- no row carrying the metadata required by the documented schema;
- holdout case H06 duplicated exactly 22 times in training;
- maximum prompt similarity between each holdout and training ranging from
  0.727 to 1.000 by the audit metric.

The historical statement that the holdout contained unseen cases is false.

### 3. Dataset policy defects

The legacy corpus includes:

- 220 prompts with `EPS_STATE=SAFE`, which is not one of the canonical
  four-level EPS states;
- 17 of 142 `EPS_STATE=CRIT` responses that do not set the AI payload to OFF;
- 100 responses that violate the mandatory
  `HOUSEKEEPING, COMMAND_ACK` queue prefix;
- 679 responses that place `AI_BEHAVIOR_LOG` below other best-effort queues.

The generator uses unseeded randomness and produces an arbitrary,
uncalibrated `confidence` value. The corpus is quarantined from future
training until regenerated from reviewed, versioned source scenarios.

### 4. Scorer and holdout defects

The historical scorer:

- accepted case identifiers by prefix;
- treated `mission_mode=UNCHANGED` as correct without evaluating output;
- accepted supersets of selected items;
- allowed a mismatch to pass as cosmetic.

Negative audit cases confirmed that an AI left ON in `EPS_STATE=CRIT`, an
incorrect extra image and a changed mission mode could still pass. The holdout
program only printed responses; it had no oracle or pass/fail assertions.

The agentic benchmark introduced later is separate. Its strict evaluator and
adversarial unit tests do not retroactively validate this session.

### 5. Statistical and reproducibility limits

The reported pass rates were 1/7 and 4/7. Their Wilson 95% intervals overlap
substantially (approximately 2.6–51.3% and 25.1–84.2%); the sample cannot
support a robust improvement or safety claim.

The run also lacks an immutable manifest binding model/tokenizer/adapter
digests, dependency versions, seeds, raw outputs, exact host state and source
commit. Reproduction is therefore not demonstrated.

## Historical raw observations

The following values are retained only so later readers can reconcile older
ADRs and reports. They are not acceptance results.

- reported base pass rate: 14.29% (1/7);
- reported fine-tuned pass rate: 57.14% (4/7);
- reported average score ratios: 0.3163 and 0.8313;
- reported average latencies on an RTX 4060 host: 5.975 s and 6.691 s.

These values must be labelled “historical Granite 3.1 2B experiment using an
invalidated protocol” wherever reproduced.

## Current disposition

- Granite 350M work is deferred.
- `gemma4:e2b` is the current bench candidate, subject to a new preregistered
  protocol and CM5 measurements.
- No AI model currently has status “validated baseline”.
- The OBC deterministic supervisor remains the sole authority over actions.
- Legacy scripts and data remain in Git for provenance, not reuse as evidence.

The evidence requirements for future runs are defined in `MODEL_ASSETS.md`,
`AI_AGENT_PROTOCOL.md` and the active mission V&V documentation.
