# GroundTelemetryDashboard

.NET 8 / Blazor dashboard for the versioned 433 MHz engineering bench. It is
not orbital ground-station or flight software.

## Build and test

```bash
dotnet restore 05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln
dotnet test 05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln -c Release
```

Browser assets are pinned/restored locally from `libman.json`; runtime does not
depend on a public CDN.

```bash
dotnet run --project 05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web
```

The application is loopback-only. Remote access requires a separately reviewed
authenticated gateway.

## Evidence

Each enabled run writes:

- `manifest.json`;
- `configuration.json`;
- SHA-256-chained `evidence.jsonl`;
- `bundle_seal.json` after orderly close.

Set a full 40/64-hex `AUSTRALIS_SOURCE_COMMIT` or
`Evidence:SourceCommit`; otherwise the bundle is explicitly
`DIAGNOSTIC_ONLY_UNIDENTIFIED_SOURCE`. Even a populated value is a local claim,
not independently verified binary provenance.

`/api/evidence/status` distinguishes an active valid prefix from a completed
locally sealed bundle. Only the latter detects truncation relative to its seal.
Neither is a digital signature, trusted timestamp or external anchor.

## Supported input

Preferred V4:

```text
version,boot_id,seq,t_ms,sensor_type,quality_flags,ax,ay,az,gx,gy,gz,q0,q1,q2,q3,dt_ms
```

Diagnostic compatibility:

- legacy raw 8 columns without quaternion;
- legacy raw 12 columns with quaternion;
- receiver-normalized V1–V3 in the 17-column envelope.

The V4 structural parser retains finite, counter-bearing frames even when
sensor quality is invalid. Scientific admission separately requires known
sensor/quality bits, `IMU_VALID`, bounded `dt_ms` and a normalized quaternion.
Session-aware link statistics separate gaps, duplicates, out-of-order frames,
wrap and reboot. Link PER never treats a received quality-invalid frame as RF
loss, while scientific yield reports its rejection. Before any frame arrives,
both estimates display `N/A`. Non-forward, time-regressed and quality-invalid
frames remain in evidence but do not enter the scientific UI series.

## Control security

Connect/disconnect requests require an ephemeral 256-bit same-origin header
token. Connection state remains `REQUESTED`/`OPENING` until the port actually
opens, then becomes `OPEN`; failures become `FAULT`.

## Interpretation limits

- MPU6050 values are not calibrated physical measurements.
- `BENCH_SENSOR_VALID_UNCALIBRATED` is not a calibration claim.
- Madgwick IMU output is terrestrial visualization, not orbital ADCS.
- Local TX `started` does not prove RF delivery; use RX sequence/PER evidence.
- A successful build or recorded session closes no gate by itself.
