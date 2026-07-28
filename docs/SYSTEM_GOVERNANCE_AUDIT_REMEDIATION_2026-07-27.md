# System/governance audit remediation record — 2026-07-27

**Estado:** Active remediation record; not verification evidence

This record distinguishes documentation/configuration corrections from
engineering verification. `Controlled Open` means the false closure was
removed and a requirement, risk, procedure and gate now control the missing
work; it does not mean the hardware or analysis has passed.

## Baseline and decision control

| Audit topic | Disposition | Controlling evidence |
|---|---|---|
| Granite evidence attributed to 350M | Corrected; current claim invalidated | Gemma ADR; provenance register; historical AI record |
| Current AI candidate | Corrected to `gemma4:e2b`; not validated | ADR-20260727 AI candidate; IA-REQ-10 |
| Dual model statements in MVP | Resolved | atomic rewrite of MVP v2.2 |
| Scientific success based only on counts | Resolved as a criterion defect; experiment itself Open | mission scientific ADR; Mission Definition §§3–4 |
| Orbit 600/650 km and LTAN conflict | Controlled Open | orbit analysis ADR; RSK-ORB-01 |
| SSO/CSV/radiator conclusions | Invalidated for closure | orbit/thermal ADRs; SIM historical disposition |
| Energy margin and heater claims | Invalidated for closure | thermal/power ADR; Power Budget; VCRM |
| Historical documents appearing current | Resolved at configuration level | MVP banners; ADR supersession; docs historical disposition |
| Hybrid/missing ADR states and contradictory addenda | Resolved at configuration level | every ADR has one formal `Accepted` or `Superseded` state and every supersession target exists |
| Corrupt `filecite`, missing historical revision and stale synchronization claims | Disposed as historical, not silently repaired into evidence | historical MVP banners; active baseline/architecture rewrite |
| Gate A previously closed | Reopened | validation plan; RSK-CONF-01 |

## Requirements, verification and readiness

| Audit topic | Disposition | Controlling evidence |
|---|---|---|
| Requirement acceptance criteria missing | Resolved structurally | 74 atomic/acceptance-bearing requirement rows |
| Requirement-to-test traceability missing | Resolved structurally | 74-row one-to-one VCRM; 21 procedure families |
| Compliance state `Pending`/`Partial` ambiguity | Resolved | normalized state model and superseding ADR |
| Gate dependencies allowed preliminary substitutes | Resolved | strict dependency sequence |
| No SRR/PDR/CDR/TRR/QAR/FRR ladder | Resolved | validation and review plan |
| Environment optional / integrator blockers allowed at readiness | Resolved | mandatory program; blockers prevent FRR |
| Named owners, dates and evidence absent | Controlled Open | owner roles now assigned; SYS-REQ-06 and RSK-PROG-01 require names/authority/date at review |
| Launch safety requirements incomplete | Controlled Open | exact CDS minima in compliance/requirements/BOM; implementation still Open |
| RF inhibits frozen without an ICD | Corrected | CDS minima are design constraints; stricter quantity/location/interface remains `Blocked by Integrator` |
| Ground weather station promoted only from a draft | Corrected | MIS-REQ-22 now derives from the active MVP and a hazard analysis must define the actual sensors/thresholds |
| “Disable AI at any moment” physically impossible | Corrected | IA-REQ-08 separates autonomous local disable from authenticated disable at the next contact opportunity |
| `EPS_STATE` labels lacked a verifiable state machine | Controlled Open | the accepted ADR is limited to taxonomy; EPS-REQ-01 requires thresholds, hysteresis, invalid-input and boundary tests |
| Battery requirement covered discharge only | Controlled Open | THR-REQ-03 covers charge, discharge, storage, survival and tested interlocks for the selected cell |
| AI event record could not reproduce an inference | Controlled Open | Mission Definition §8 and IA-REQ-07 require versioned raw input/output, manifests, decoding, supervisor, energy/thermal and post-state correlation |
| CM5/model promoted before COTS-to-flight evidence | Corrected / Controlled Open | Gemma remains an unvalidated candidate; IA-REQ-09 and RAD-REQ-01 require exact hardware, radiation and fault-containment evidence |
| Scientific and engineering evidence provenance incomplete | Controlled Open | ArtifactID/ConfigurationID/EvidenceID/digest policy |

The 57 requirement IDs that existed before remediation were retained. Seventeen
assurance requirements were added, producing 74 current IDs and 74 unique VCRM
rows. No requirement is `Verified`.

## Risks, costs and configuration

| Audit topic | Disposition | Controlling evidence |
|---|---|---|
| Risk register lacked actionable ownership/triggers/gates | Resolved structurally | 37-risk register with initial P/I, owner role, trigger, due gate and closure evidence |
| Risks closed using invalid analyses | Reopened | all current risks are Open |
| Missing radiation/ADCS/BMS/environment/security risks | Resolved structurally | dedicated risk entries and VCRM links |
| BOM lacked mass/power/traceability and used `ROM` as cost | Resolved structurally | 26-column, 74-row BOM; all unknown values explicit TBD |
| BOM omitted ADCS, pack, launch safety and radiation | Controlled Open | placeholder rows added; decomposition/selection remains Open |
| BMS IC alternatives treated as equivalent/complete | Corrected | complete BMS architecture TBD; no isolated IC receives BMS credit |
| Cost overview omitted life-cycle drivers | Resolved structurally | 20-row LCC WBS with NRE/recurring classification |
| Numeric viability/cost baseline | Open | no prices or totals are invented |

## Publication, legal and repository authority

| Audit topic | Disposition | Controlling evidence |
|---|---|---|
| Public/private source-of-truth ambiguity | Resolved as policy | repository governance |
| Old publication audit appeared current | Resolved | Historical Snapshot disposition |
| Public mirror release preceded final blocker disposition | Controlled Open | every release now requires a dated sign-off and claim/provenance scan; prior audits remain historical |
| Model/dataset/CAD provenance incomplete | Controlled Open | artifact provenance register and release blocker |
| Copyright holder wording ambiguous | Corrected to explicit TBD | interim license notice; legal risk remains Open |
| Per-file license/SPDX and full texts absent | Controlled Open | license scope + mandatory pre-release action |
| Commercial contact absent | Explicitly controlled | no permission can be granted until an authorized contact/entity is designated |
| Contributor rights ambiguous | Controlled | external merges closed pending chain-of-title/CLA review |
| PHOTO_DEMO legal memo overstates heuristic thresholds | Corrected | Preliminary label; specialist/authority review required |

This repository does not claim that the interim legal controls establish
ownership or constitute legal advice.

## Verification performed

- requirement/VCRM one-to-one and duplicate check;
- VCRM ProcedureID/RiskID existence check;
- compliance and ADR state validation;
- supersession target existence check;
- BOM/LCC/CSV structural parse;
- Markdown local-link resolution;
- `git diff --check`;
- power-budget self-test;
- simulation validation;
- ground dashboard unit tests.

Physical tests, calibrated RF measurements, CAD/fit-check, ERC/DRC release,
environmental qualification, radiation analysis, regulatory authorization,
legal sign-off and flight evidence remain outside this documentation
remediation and stay `Open`.
