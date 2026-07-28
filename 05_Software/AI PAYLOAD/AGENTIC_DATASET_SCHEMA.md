# AUSTRALIS agentic dataset schema

**Revision:** 2026-07-27
**Status:** Proposed — required for the next curated corpus
**Model scope:** Model-neutral; first candidate `gemma4:e2b`

## Scientific rules

1. Split assignment is performed by scenario family before paraphrase or
   synthetic mutation. Related examples cannot cross splits.
2. Holdout content is blind to training, prompt tuning and model selection.
3. Every target decision is expert-reviewed and evaluated by a deterministic
   oracle/postcondition.
4. Synthetic data records generator, exact revision, seed and parent example.
5. Exact and near duplicates are grouped; a group belongs to one split only.
6. `confidence` is optional labelled calibration data. It is never generated
   from an arbitrary random range and never authorizes an action.
7. Safety-critical rules use exact assertions; semantic similarity cannot turn
   a violation into a pass.

## JSONL record

Each line is one object:

```json
{
  "schema_version": "AUSTRALIS_AGENTIC_DATASET_V1",
  "example_id": "EX-000001",
  "scenario_family_id": "EPS_CRIT_SURVIVAL-001",
  "duplicate_group_id": "DG-000001",
  "split": "train",
  "source": {
    "kind": "expert|simulation|synthetic_mutation",
    "source_ref": "REQ/ADR/Test/episode identifier",
    "generator": "human or exact program revision",
    "parent_example_id": null,
    "seed": null,
    "license": "project-authored or SPDX identifier"
  },
  "context_snapshot": {},
  "available_tools_revision": "sha256:...",
  "target_decision": {},
  "oracle": {
    "required_actions": [],
    "forbidden_actions": [],
    "postconditions": [],
    "hard_fail_conditions": []
  },
  "labels": {
    "bucket": "energy_survival",
    "difficulty": "nominal|edge|adversarial",
    "safety_critical": true
  },
  "review": {
    "status": "approved",
    "reviewer": "named project role",
    "reviewed_at": "RFC3339 timestamp",
    "notes": ""
  }
}
```

`target_decision` must conform exactly to `AgentDecisionEnvelope` in
`AI_AGENT_PROTOCOL.md`. Tool arguments and safety class are validated against
the same catalog revision referenced by `available_tools_revision`.

## Split policy

- `train`: may be inspected and transformed during training.
- `validation`: used for predefined training/selection checks, never training.
- `holdout`: sealed before candidate comparison and opened once per
  preregistered campaign.

Random row-level 80/10/10 splitting is prohibited. The split tool must group by
`scenario_family_id`, `duplicate_group_id` and a near-duplicate fingerprint.
Any exact duplicate or similarity above the approved threshold across splits
is a hard failure.

## Required validation

Before training:

- JSON/schema validation passes for every record;
- identifiers are unique and references resolve;
- every target passes the deterministic supervisor and oracle;
- no canonical EPS state outside `CRIT|LOW|NOMINAL|HIGH`;
- critical queue order begins
  `HOUSEKEEPING, COMMAND_ACK, AI_BEHAVIOR_LOG`;
- no unsafe action is present in any safety-critical example;
- split leakage checks pass;
- provenance and review state are complete.

Before claiming a result, archive the dataset hash, split manifest, validator
version/output and all rejected-record diagnostics.
