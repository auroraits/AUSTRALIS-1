# Artifact provenance and reproducibility register

Status: **Active control / records incomplete**
Effective date: 2026-07-27

This register defines the minimum provenance required before an artifact may be
distributed, cited as evidence or used to close a requirement.

## Required fields

Every model, dataset, adapter, firmware image, binary, simulation result, CAD/PCB
release and test output requires:

- stable ArtifactID and type;
- upstream name and source;
- exact revision, immutable digest and retrieval/build date;
- applicable license and redistribution decision;
- producing repository commit and toolchain/environment lock;
- input artifact IDs and configuration;
- procedure/run ID, raw-output location and raw-output digest;
- owner role, review state and VCRM EvidenceID.

A mutable model tag, filename, screenshot, summary table or generated prose is
not sufficient identity or evidence.

## Current AI records

| Artifact | Current identity | State | Required disposition |
|---|---|---|---|
| `gemma4:e2b` | Mutable candidate tag only | Open; no validation claim | Capture upstream identity, manifest digest, tokenizer/runtime versions, license and CM5 run manifest before Gate IA |
| Granite 3.1 2B scripts/results | Scripts name `ibm-granite/granite-3.1-2b-instruct` | Historical bench material | Preserve as 2B evidence only; never relabel as 350M |
| Granite 350M claim | No matching executed pipeline in the archived evidence | Invalid as verification evidence | Deferred; a future independent pipeline requires a new ArtifactID |
| Historical training JSONL | File present; dataset provenance/metadata/split quality incomplete | Not accepted as independent benchmark evidence | Record generator revision/seed, source/license, deduplication, rule validation and immutable split digests |
| Historical holdout | Contaminated by exact/near training overlap | Invalid as blind holdout | Replace with preregistered, isolated and hashed evaluation set |

## Release rule

The release reviewer must export a machine-readable manifest containing the
fields above. Until that manifest exists, the relevant VCRM entry remains
`Open`, regardless of whether a file or summary report exists.

Third-party distribution constraints are controlled by
`THIRD_PARTY_NOTICES.md`, `LICENSE.md` and `LICENSE_SCOPE.md`.
