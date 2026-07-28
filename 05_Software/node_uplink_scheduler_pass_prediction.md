# Node uplink scheduler and offline pass prediction

**Revision:** 2026-07-27
**Status:** Proposed / implementation and radiated use blocked
**Requirements:** `COMMS-UL-02`, `COMMS-UL-03`, `COMMS-UL-06`
**Verification:** `PROC-RF-002`, test `LORA-06`
**Risk:** `RSK-COMMS-03`, `OPS-TLE-01..03`

## Purpose and non-authorization

This document defines a fail-silent candidate scheduler for an ESP32-class
ground node. It does not adopt B2 or authorize 915 MHz Earth-to-space
transmission. The default and every uncertain state is `TX_INHIBITED`.
Laboratory evaluation shall be conducted, shielded or simulated until the RF
regulatory gate explicitly permits radiated operation.

## Inputs

The scheduler consumes only versioned, validated inputs:

- active orbit-data envelope and object identity from
  `node_tle_update_mechanism.md`;
- site latitude, longitude, altitude, datum, provenance and uncertainty;
- UTC estimate, source, last synchronization, holdover model and uncertainty;
- SGP4 implementation/version and configuration identity;
- approved elevation mask and pass/slot uncertainty budget;
- signed operating policy with mission/network ID, node ID, PHY/channel plan,
  maximum airtime/energy and validity interval;
- explicit regulatory authorization state and authorized time/frequency limits.

Missing, expired, unauthenticated or internally inconsistent inputs inhibit TX.
“GNSS once per day” is not an accepted design rule. The required resynchronizing
interval is derived from measured holdover over voltage and temperature.

## Prediction and window construction

1. Propagate the approved object with a tested SGP4 implementation.
2. Transform to the declared site frame and find elevation-mask crossings with
   a coarse search followed by bounded refinement.
3. Compute peak time/elevation, range and Doppler for diagnostic use.
4. Construct the geometric interval where elevation is at or above the
   approved mask. A fixed six-minute interval around peak is not permitted.
5. Intersect the geometric interval with the signed authorized interval.
6. Shrink both ends by the conservative total timing uncertainty:

```text
U_total =
  U_orbit_prediction
  + U_clock_holdover_and_sync
  + U_site
  + U_propagator_and_numeric
  + U_scheduler_latency
  + U_RF_start_and_slot
```

Root-sum-square may replace the conservative sum only for terms demonstrated
independent with supporting data. If the remaining interval cannot contain a
complete frame, guard and required retry policy, the result is
`NO_ELIGIBLE_WINDOW`.

## Transmission interlocks

Every frame attempt requires all of the following at the instant of use:

- `regulatory_authorization == VALID`;
- authenticated operating policy within its validity interval;
- active orbit data within its measured error budget;
- matching mission, object, site, node, PHY and channel identifiers;
- time quality within the approved uncertainty;
- current time inside the clipped eligible interval;
- elevation and guard allocations still valid;
- airtime, energy, retry and per-node limits not exhausted;
- no local inhibit, fault, brownout or operator stop.

The interlocks are reevaluated immediately before RF keying. A previously
computed window is not authority to transmit after an input changes.

## Failure behavior

The scheduler is a state machine, not an optimistic timer:

```text
TX_INHIBITED
  -> INPUTS_VALID
  -> WINDOW_PREDICTED
  -> ELIGIBLE_NOW
  -> FRAME_ALLOWED
  -> TX_INHIBITED after the bounded attempt
```

Any validation failure or uncertainty-budget exceedance returns directly to
`TX_INHIBITED`. A loss of TLE, UTC/GNSS, storage, signature, object identity or
authorization never falls back automatically to B1. B1 may exist only as a
separately reviewed mode with its own explicit authorization and limits.

## Slotting and capacity

If slotting is later selected, frame time-on-air shall come from the exact
adopted PHY, payload, preamble, header, coding and low-data-rate optimization.
Slot assignment, jitter and retry rules shall be validated against collision,
near-far, adjacent/cochannel and clock/orbit errors. The scheduler shall not
infer capacity from the superseded February estimates.

## Audit record

For each prediction and attempt, persist:

- boot/session and decision ID;
- orbit envelope digest/generation/object ID;
- firmware, SGP4 and operating-policy identities;
- site and time-source identities with uncertainties;
- geometric, authorized and final clipped intervals;
- each uncertainty term, total guard and remaining margin;
- predicted elevation/range/Doppler;
- interlock vector, decision and reject reason;
- actual monotonic/UTC timestamps, requested/actual RF duration and outcome.

This log supports diagnosis; it does not by itself prove physical origin or
regulatory compliance.

## Verification

`LORA-06` shall inject:

- valid nominal and edge-of-mask passes;
- wrong object, stale/expired/signed-invalid/rollback orbit data;
- clock offset, drift, GNSS loss and temperature-dependent holdover;
- site-coordinate error and scheduler latency;
- authorization absent/expired or mismatched channel/policy;
- window shorter than one complete frame;
- reboot and power loss across every state;
- B1 configuration present but not explicitly authorized.

Acceptance requires no RF request outside the clipped interval, fail-silent
behavior for every invalid input and agreement with an independent reference
propagator/time calculation within an approved tolerance. Hardware-in-loop
radiated tests remain blocked until the regulatory gate closes.

## References

- `05_Software/node_tle_update_mechanism.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/regulatory_gate_rf.md`
- `docs/COMMS/uplink_lora_bench_testing_plan.md`
- `08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`
