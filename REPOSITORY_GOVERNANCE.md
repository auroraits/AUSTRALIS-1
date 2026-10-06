# Repository governance

Status: **Active**
Effective date: 2026-07-27
Last reviewed: 2026-10-05

## Authority

The sole current technical configuration authority for AUSTRALIS is
`https://github.com/auroraits/AUSTRALIS-1`, branch `main`. A revision becomes
part of the current project baseline only after it is reviewed and merged into
`main`. The exact baseline used by a review, test, website claim or release must
be identified by commit SHA; a tag may identify an immutable public snapshot.

No private workspace, unpublished mirror, local clone or historical export is
implicitly canonical. If another repository contains newer work, it is an input
until the change is reviewed and merged here. Divergent copies must be
reconciled explicitly; chronology alone does not confer authority.

## Historical repository disposition

`auroraits/DIY-Nanosat` is an archived private historical repository. Its remote
history, local checkouts, branches and uncommitted files are `Historical
Snapshot` inputs and have no current baseline authority.

- Keep the repository archived; do not resume authoritative development there.
- Do not merge, mirror, rebase or synchronize its history into this repository.
- Do not copy a complete legacy tree over the current baseline.
- Import useful legacy material only through a scoped pull request targeting
  `AUSTRALIS-1/main`.
- Each import must identify its legacy source path and commit when available,
  then be re-evaluated against current ADRs, requirements, provenance, license,
  security and repository validation checks.
- Conflicts are resolved in favor of the current AUSTRALIS configuration and
  its accepted decision hierarchy, not by legacy chronology.

## Branch and release meaning

- A feature or remediation branch is proposed configuration.
- `main` is the current technical configuration branch.
- `main` shall use server-side protection or a ruleset. Until that control is
  enabled, pull-request review and passing CI remain mandatory process controls;
  the enforcement gap does not transfer authority to another repository.
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
