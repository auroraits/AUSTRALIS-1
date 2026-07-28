# Repository governance

Status: **Active**
Effective date: 2026-07-27

## Authority

This public repository is the technical configuration source for material that
it publishes. A revision becomes a public project baseline only after it is
merged into the protected public baseline branch and identified by an approved
commit or tag.

No private workspace, unpublished mirror, local clone or historical export is
implicitly canonical. If another repository contains newer work, it is an input
until the change is reviewed and merged here. Divergent copies must be
reconciled explicitly; chronology alone does not confer authority.

## Branch and release meaning

- A feature or remediation branch is proposed configuration.
- The protected baseline branch is current public configuration.
- A tag is an immutable public snapshot, not evidence of verification.
- Test evidence is authoritative only when its EvidenceID, configuration,
  procedure, raw artifact digest and producing commit are recorded in the VCRM.

## Precedence

For technical configuration:

1. newest applicable Accepted ADR;
2. `00_MVP/MVP v2.2.md`;
3. `SYSTEM_BASELINE.md`;
4. mission requirements and VCRM;
5. subsystem documents.

An older Accepted ADR that has been explicitly superseded is historical. A
Draft, Proposed, Preliminary, Bench or Historical document cannot override an
Accepted decision or close a requirement.

## Change control

Every baseline change must:

1. identify affected requirements, risks, interfaces and evidence;
2. update supersession metadata atomically;
3. pass repository consistency checks;
4. receive the review authority required by the current stage gate;
5. avoid promoting an estimate, simulation or bench result beyond its evidence.

Release governance is defined in `PUBLIC_RELEASE_PROCESS.md`.
