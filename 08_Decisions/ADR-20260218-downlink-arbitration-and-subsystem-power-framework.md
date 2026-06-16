# ADR-20260218-downlink-arbitration-and-subsystem-power-framework

- **Fecha:** 2026-02-18
- **Estado:** Accepted

## Contexto
El MVP requería reglas permanentes para arbitrar downlink entre subsistemas, controlar power-gating selectivo y aislar fallas sin comprometer SAFE ni telemetría crítica.

## Decisión
Adoptar framework permanente en OBC/EPS:
1. **Downlink Manager** con colas `HOUSEKEEPING`, `COMMAND_ACK`, `LORA_LOG`, `SCIENCE`, `OPTIONAL_PAYLOAD`.
2. **Prioridad estricta** para housekeeping/comandos en todos los modos.
3. **Fault/Power Manager** con health mínimo (`PGOOD_x`, `EN_x`, `FAULT_x`, `HB_x`) + contadores de resets/faults.
4. **Aislamiento automático**: apagado inmediato, reintentos acotados y lockout hasta uplink/timeout.
5. **Uplink mínimo**: `SET_MODE`, `POWER_SET`, `DL_SELECT`, `DL_SET_LIMITS`, `REQUEST_STATUS`, `ABORT`.

## Alternativas consideradas
1. Scheduler por prioridad fija sin colas por tipo.
2. Fault handling manual desde tierra sin aislamiento automático.
3. Framework completo (elegida).

## Tradeoffs / riesgos
- A favor: robustez operativa, degradación controlada y trazabilidad de salud.
- En contra: mayor complejidad de software de vuelo y validación de estado.

## Implicancias (archivos actualizados)
- `00_MVP/MVP v2.2.md`
- `01_Mission/mission_definition.md`
- `02_Structure/Block Diagram.md`
- `03_Power/Power Budget.md`
- `03_Power/EPS Sizing.md`
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/link_budget_uhf_preliminary.md`
- `05_Software/software_framework_mvp22.md`
- `architecture.md`
