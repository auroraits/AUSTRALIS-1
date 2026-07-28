# AUSTRALIS ground data architecture

**Revision:** 2026-07-27
**Status:** Partially implemented; not Gate-closure evidence by itself

## Implemented path

The .NET dashboard now uses:

```text
serial input
  -> append-only evidence record (raw line)
  -> strict parser and quality checks
  -> append-only validated/rejected record
  -> session-aware statistics
  -> bounded in-memory UI cache
```

Each application run creates:

- `manifest.json`: run ID, UTC start, host/OS/application version, optional
  source commit and chain definition;
- `evidence.jsonl`: raw lines, rejected lines/reasons, validated samples,
  connection changes and runtime errors.

Records are numbered and SHA-256 chained. `EvidenceVerifier` detects record
modification, deletion/reordering within the retained chain and broken
predecessor links. This is tamper-evident engineering evidence, not a digital
signature or trusted timestamp; operator identity and off-host immutable
archival remain open.

Evidence output is enabled by default and excluded from Git. The exact run
directory is reported at startup and by `/api/evidence/status`.

## Frame and quality model

The current V4 bench CSV is:

```text
version,boot_id,seq,t_ms,quality_flags,ax,ay,az,gx,gy,gz,q0,q1,q2,q3
```

Legacy 8/12-column input remains diagnostic-only. V4 provides the boot/session
identifier needed to avoid treating a reboot as packet loss.

The parser rejects:

- wrong field count or unsupported protocol version;
- invalid, NaN or infinite numbers;
- counters or flags outside declared ranges;
- sensor values outside signed 16-bit raw range;
- quaternion norm outside 0.9–1.1.

Rejected raw input and reason code are preserved. A syntactically valid sample
is not evidence of sensor calibration; calibration revision and uncertainty
must be added before physical measurements are used scientifically.

## PER/statistics

Statistics distinguish:

- unique forward packets;
- estimated sequence gaps;
- duplicates;
- out-of-order packets;
- boot/session changes;
- uint32 sequence wrap.

A V4 `boot_id` change starts a new session window and does not create artificial
loss. Legacy input uses a conservative joint time/sequence rollback heuristic
and therefore cannot provide the same confidence.

PER is calculated as `lost / (unique_received + lost)` within the current
window. Duplicates and out-of-order packets are reported separately instead of
being silently folded into loss.

## Security and operation

- The web application is loopback-only in code and launch settings.
- Remote/LAN requests receive HTTP 403 even if the socket is accidentally
  bound broadly.
- Remote operation requires a separately reviewed authenticated gateway; a
  `0.0.0.0` how-to is not an approved configuration.
- Connect requests only accept serial ports enumerated by the OS.
- A monotonically increasing connection generation forces the reader to close
  and reopen when port/baud changes, preventing UI/reader divergence.
- Browser libraries are pinned and restored locally at build; runtime does not
  depend on public CDNs.

## Still open

- replay UI and controlled export bundle;
- operator notes/signature and role authentication;
- off-host/WORM archive and trusted time source;
- calibration metadata and instrument traceability;
- RF measurements such as RSSI/SNR/CFO in the 433 bench frame;
- end-to-end test against actual hardware after firmware compilation;
- evidence-pack procedure, reviewer sign-off and VCRM linkage for each test.

Accordingly, the implementation removes the “RAM-only” blocker but does not
close Gate B or any flight requirement without an executed, reviewed test
procedure.
