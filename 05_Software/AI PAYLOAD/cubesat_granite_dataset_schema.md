# Legacy Granite dataset schema

**Status:** Historical / superseded
**Disposition:** Not admissible for training or validation
**Superseded by:** `AGENTIC_DATASET_SCHEMA.md`

This file name is retained because historical scripts and reports reference it.
The associated `cubesat_granite_v3_1800.jsonl` corpus does not implement the
metadata that the old schema recommended, contains duplicate and policy-invalid
examples, and contaminates its holdout. It must not be silently repaired in
place because that would destroy provenance.

The legacy format consisted of a `messages` array with system, user and
assistant content. It did not bind examples to:

- a stable scenario family and independent source;
- a train/validation/holdout assignment made before generation;
- an expert-reviewed oracle and expected postcondition;
- a model-neutral protocol/schema version;
- provenance, license, generator revision and seed;
- duplicate/near-duplicate group;
- reviewer identity and approval state.

Forensic findings and the original reported results are recorded in
`ai_payload_bench_evidence_2026-03-16.md`. New data must use
`AGENTIC_DATASET_SCHEMA.md`; Granite 350M work remains deferred.
