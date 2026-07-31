# Simulator Bridge Plan

**Revision:** 2026-07-31
**Estado:** Draft

Alfredo indicated that this suite will later be unified with an orbital
simulator. The MVP keeps the boundary explicit through a `TelemetrySource`
interface in `console/app.js`.

## Current Sources

| Source | State | Notes |
|---|---|---|
| `manual` | implemented | UI fields/sliders edit one snapshot. |
| `preset` | implemented | scenario pack emits deterministic snapshots. |
| `replay` | stub-ready | JSONL replay parser exists client-side. |
| `simulator-stream` | stub | throws until phase 2 stream schema is approved. |

## Future Stream Schema

The simulator should emit messages compatible with `ai_agent_context.v1` or a
clear superset:

```json
{
  "schema_version": "simulator_telemetry.v1",
  "timestamp_utc": "2026-07-31T00:00:00Z",
  "source": "orbital-simulator",
  "snapshot": {
    "schema_version": "ai_agent_context.v1"
  }
}
```

Candidate future fields:

- illumination by face/panel;
- eclipse/sun and battery state;
- temperatures by face;
- radiative cooling capacity;
- Earth magnetic field vector;
- attitude/orientation;
- orbital pass geometry;
- deterministic RF window state.

## Adapter Contract

The bridge adapter should expose:

```js
{
  id: "simulator-stream",
  connect(url, onSnapshot, onStatus) {},
  disconnect() {},
  latest() {}
}
```

The benchmark runner should treat simulator snapshots exactly like preset or
manual snapshots once normalized.

## Non-Goals For MVP

- No orbital propagation implementation.
- No thermal/radiation physics model.
- No direct coupling to GroundTelemetryDashboard.
- No automatic promotion of simulator output to validation evidence.

Simulator output will be evidence input only after the simulator itself has
versioned inputs, assumptions, tolerances and review.
