# Node orbit-data update mechanism

**Revision:** 2026-07-27
**Status:** Proposed / implementation and radiated use blocked
**Requirements:** `COMMS-UL-02`, `COMMS-UL-03`
**Verification:** `PROC-RF-002`, test `LORA-06`
**Risk:** `RSK-COMMS-03`, `OPS-TLE-01..03`

## Scope and safety state

This specification defines how a ground sensor node may receive and activate
orbit data for offline pass prediction. It does not authorize transmission,
adopt B2, or make 915 MHz Earth-to-space operation legal. Until the regulatory
gate, time-error campaign and implementation tests close, the operational
output is always `TX_INHIBITED`.

Loss of valid orbit data never enables B1. B1 is a separate mode that requires
its own explicit authorization, bounded airtime/energy configuration and test
evidence. Conducted, shielded or simulation-only work remains permitted under
the applicable laboratory procedure.

## Controlled update object

The node accepts a signed envelope, not two unauthenticated text lines. The
canonical payload shall contain at least:

```text
schema_version
mission_id
generation                         monotonic unsigned integer
object.norad_catalog_id
object.international_designator
tle.line1
tle.line2
tle.epoch_utc
source.id
source.retrieved_at_utc
validity.not_before_utc
validity.not_after_utc
policy_id
key_epoch
signature_algorithm
signing_key_id
payload_sha256
signature
```

The exact canonical encoding and signature suite remain a security-design
selection. Ed25519 is a candidate, not a decision. HTTPS/BLE/serial transport
alone is not provenance; every transport carries the same signed envelope.
Secrets are never embedded in a public node image.

## Admission pipeline

A candidate becomes active only if every step succeeds:

1. Enforce size, encoding and schema limits before parsing.
2. Validate both TLE line numbers, lengths and line checksums.
3. Parse the catalog number from both lines and require the configured
   `norad_catalog_id`; reject a different object even with a valid checksum.
4. Recompute the canonical-payload SHA-256 digest and verify the signature
   against an allowed key and `key_epoch`.
5. Require `generation > active_generation`; reject replay and rollback.
6. Require consistent UTC fields and an accepted local time-quality state.
7. Parse the epoch and all SGP4 inputs without truncation or silent defaults.
8. Evaluate validity against the measured orbit/time error budget described
   below.
9. Write to the inactive A/B slot, read it back, revalidate it, then switch one
   atomic active-slot marker. A power loss before the marker preserves the
   previous valid slot.
10. Emit an append-only local activation record with the envelope digest,
    object ID, generation, source/key IDs, active slot and result.

An authenticated recovery package may intentionally supersede a bad update,
but it still requires a strictly higher generation. There is no network
command that silently lowers the anti-rollback counter.

## Validity is error-based, not age-based

Fixed rules such as “warn after 7 days” or “use B1 after 30 days” are removed.
The allowable age shall be derived experimentally for the selected orbit and
propagator:

1. Archive successive authoritative element sets and independently determined
   reference pass times.
2. Replay predictions at multiple element ages, sites, elevations and relevant
   drag/space-weather conditions.
3. Measure timing, elevation and range errors with sample size and confidence
   intervals defined by `LORA-06`.
4. Combine orbit-prediction error with measured RTC holdover, GNSS fix,
   scheduler latency and RF-slot uncertainty. Correlated terms use a
   conservative sum unless independence is demonstrated.
5. Approve an expiry policy only where the total worst-case allocation remains
   inside the pass/slot guard with the required margin.

Before that campaign exists, any age threshold is diagnostic only and cannot
enable radiated operation.

## State machine

```text
EMPTY / INVALID / EXPIRED / ROLLBACK / WRONG_OBJECT / BAD_SIGNATURE
                         -> TX_INHIBITED

CANDIDATE_VALID --atomic activation--> ACTIVE_WITHIN_ERROR_BUDGET
                         -> scheduler may evaluate other interlocks
```

`ACTIVE_WITHIN_ERROR_BUDGET` is necessary but not sufficient for transmission.
Loss of time validity, authorization, site validity or any other scheduler
interlock returns `TX_INHIBITED`.

## Required local telemetry

- active generation, object ID, TLE epoch and envelope digest;
- source/key ID and key epoch, never private key material;
- active/previous slot and last update result;
- time source, age and uncertainty;
- predicted orbit/time error allocation and remaining guard margin;
- reject reason (`BAD_SIGNATURE`, `ROLLBACK`, `WRONG_OBJECT`, `EXPIRED`,
  `BAD_CHECKSUM`, `SCHEMA`, `TIME_INVALID`, or `STORAGE_VERIFY`);
- firmware/configuration identity and boot/session ID.

## Verification cases

`LORA-06` shall include valid update, corrupt line, wrong object, stale object,
signature/key failure, replay, lower generation, expired validity, power loss
at each write stage, corrupt active slot, clock invalidity and recovery from the
previous slot. Acceptance requires fail-silent behavior and a reproducible
audit record for every negative case.

## References

- `05_Software/node_uplink_scheduler_pass_prediction.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/regulatory_gate_rf.md`
- `docs/COMMS/uplink_lora_bench_testing_plan.md`
- `08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`
