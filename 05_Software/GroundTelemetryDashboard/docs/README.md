# GroundTelemetryDashboard

.NET 8 / Blazor dashboard for the versioned 433 MHz engineering bench.
It is not orbital ground-station flight software.

## Build and test

```bash
dotnet restore 05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln
dotnet test 05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln -c Release
```

The build restores pinned browser assets from `libman.json` into
`wwwroot/vendor`. Runtime pages use those local files and do not require a CDN.
The restored license/notice files are retained beside the assets.

Run locally:

```bash
dotnet run --project 05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web
```

The application is loopback-only. LAN access is intentionally rejected even if
an operator binds Kestrel to `0.0.0.0`; remote access needs a separately
reviewed authenticated gateway.

## Evidence

Evidence recording is on by default. Each run creates a unique directory below
the configured `Evidence:Root` containing:

- `manifest.json`;
- SHA-256-chained `evidence.jsonl`.

The log records raw serial lines before parsing, parsed samples, rejected lines
with reason codes, connection transitions and errors. Check the live chain at
`/api/evidence/status`. A valid chain is tamper-evident but is not a digital
signature or trusted timestamp.

## Supported input

Preferred V4:

```text
version,boot_id,seq,t_ms,quality_flags,ax,ay,az,gx,gy,gz,q0,q1,q2,q3
```

Diagnostic compatibility:

- legacy 8 columns without quaternion;
- legacy 12 columns with quaternion.

The parser enforces finite/ranged values and quaternion norm. V4 session-aware
statistics separate gaps, duplicates, out-of-order frames, wrap and reboot.

## Interpretation limits

- Raw MPU6050 values are not calibrated physical measurements.
- Madgwick IMU output is a terrestrial bench visualization and is not an
  orbital ADCS solution.
- A local TX `started` status does not prove RF delivery; use receiver-side
  sequence/PER evidence.
- No Gate closes merely because the dashboard builds or records a session.
