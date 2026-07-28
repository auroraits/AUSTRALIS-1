# AUSTRALIS ground data architecture

**Revision:** 2026-07-27
**Status:** Partially implemented; not Gate-closure evidence by itself

## Implemented path

```text
serial input
  -> append-only raw evidence
  -> structural frame parser
  -> independent link and scientific-quality dispositions
  -> append-only classified evidence
  -> session-aware statistics using a host monotonic clock
  -> bounded UI series containing forward samples only
```

Each application run creates:

- `manifest.json`: run ID, host/runtime, claimed source commit and chain rules;
- `configuration.json`: recoverable non-secret Serial/Evidence configuration;
- `evidence.jsonl`: raw/rejected/classified frames, acquisition-session IDs,
  connection transitions and runtime errors;
- `bundle_seal.json`: record count, final record hash, manifest hash and
  complete evidence-file hash, emitted only on orderly close.

During acquisition the verifier can only report `ACTIVE_PREFIX_VALID`. That
state cannot prove that the tail was not truncated. A completed bundle must
contain `run_started`, `run_closed`, the manifest anchor and a matching local
seal. It can then detect modification, deletion/reordering and truncation
relative to that seal.

This is local tamper evidence, not a signature or trusted timestamp. A 40/64
hex `source_commit_claim` is recorded but is not proof that the executable was
built from that object. External signing/anchoring, operator identity and
off-host immutable archival remain open.

## Frame and quality model

The preferred V4 bench CSV is:

```text
version,boot_id,seq,t_ms,sensor_type,quality_flags,ax,ay,az,gx,gy,gz,q0,q1,q2,q3,dt_ms
```

The RX normalizes V1–V3 into the same 17-column envelope and retains
`sensor_type`/`dt_ms` when those fields exist. Raw legacy 8/12-column lines
remain accepted for diagnostics. All V1–V3 samples are `DIAGNOSTIC_ONLY`
because they lack V4 session/quality semantics.

For V4 the structural parser requires:

- exact supported field/version layout;
- parseable counters and finite sensor fields in their transport ranges.

It deliberately retains a structurally valid frame when `IMU_VALID` is clear
or another scientific-quality check fails. This preserves its sequence number
for RF-link statistics. Scientific admission separately requires MPU6050
`sensor_type`, no unknown quality bits, `IMU_VALID`, nonzero bounded `dt_ms`
and:
- quaternion norm within 0.9–1.1.

`BENCH_SENSOR_VALID_UNCALIBRATED` means only that the frame passed those
checks. It is not evidence of calibration, physical units or uncertainty.

## PER and series admission

Link statistics distinguish unique forward packets, gaps, duplicates,
out-of-order frames, reboot/session changes and uint32 wrap.
A V4 `boot_id` change starts a new window and does not create false loss.
Legacy packets use a conservative joint time/sequence rollback heuristic.

Link PER is `lost / (unique_received + lost)`. An unset estimate is reported
as `N/A`, never as an invented 0% PER. Scientific yield is independently
`admitted / (admitted + quality_or_time_rejected)`. A frame received with
invalid sensor quality therefore lowers scientific yield but does not become
RF loss. Device-time regressions also reject scientific admission without
rewinding the link sequence tracker. Window eviction uses `Stopwatch`
monotonic ticks, so UTC/NTP corrections cannot alter duration. Duplicates,
out-of-order, quality-invalid and time-regressed frames remain in evidence but
are excluded from the chart/scientific series.

## Security and connection truth

- The application rejects non-loopback requests even if Kestrel is bound
  broadly.
- Connect/disconnect require a 256-bit same-origin control token in a custom
  header; cross-origin form POSTs cannot operate the bench.
- Serial state is explicit: `REQUESTED` → `OPENING` → `OPEN` or `FAULT`.
  The UI reports connected only after `SerialPort.Open` succeeds.
- A connection generation forces close/reopen when port or baud changes.
- Browser dependencies are local and versioned; runtime does not need a CDN.

## Still open

- replay UI and signed/controlled export;
- repository-resolved build provenance and dependency/SBOM binding;
- operator signature/role authentication and external hash/signature anchor;
- off-host/WORM archive and trusted UTC;
- calibration metadata, instrument traceability and RF RSSI/SNR/CFO;
- hardware end-to-end execution after firmware compilation;
- evidence-pack procedure, reviewer sign-off and VCRM linkage.

The implementation removes the RAM-only blocker. It does not close Gate B or
any flight requirement without an executed and independently reviewed test.
