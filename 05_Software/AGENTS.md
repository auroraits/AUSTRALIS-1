# AGENTS.md — 05_Software (Flight SW + Ground SW)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
>
> **Modelo operativo canónico:** `MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW`. No usar "SCIENCE MODE". La actividad científica es actividad dentro de NOMINAL.
>
> **Arquitectura de datos de tierra:** ver `ground_data_architecture.md`. El estado en memoria NO es la única fuente de verdad.

## Estructura vigente del subsistema
- `05_Software/embedded/`: firmware embebido de pruebas RF 433 MHz (ESP32-S3 TX + UNO RX logger).
- `05_Software/GroundTelemetryDashboard/`: dashboard de estación terrena en .NET 8 (Blazor Server + SignalR + serial COM).

## Propósito
Documenta software:
- flight software (modes, telemetry, telecommand, watchdogs),
- ground software (tools, parsing, storage, dashboards).

## Cómo debe trabajar un agente aquí
- Documentar en términos de estados/modos (state machine).
- Definir interfaces con EPS y COMMS: paquetes, tasas, comandos críticos.

Si se agregan o cambian modos operativos (`MISSION_MODE`) o cambia telemetría/tasas:
- actualizar link budget y tasas en `04_Communications/`,
- actualizar presupuesto de energía en `03_Power/`,
- reflejar en `00_MVP/MVP v2.2.md`,
- considerar ADR si es cambio de arquitectura.

## Entregables esperados
- Lista de modos (`MISSION_MODE`/`EPS_STATE`) y transiciones.
- Telemetría mínima (MVP) vs extendida.
- Plan de logging y post-mortem.
- Arquitectura de datos de tierra con separación cache UI / persistencia.

## Reglas locales adicionales
- No tocar código fuente funcional; solo documentación asociada.
- `PHOTO_DEMO` es off-by-default y best-effort. No puede bloquear housekeeping/comandos.
- Ground SW: implementar arquitectura de datos según `ground_data_architecture.md` antes de Gate B.
