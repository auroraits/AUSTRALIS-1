# Riesgos — Banco de telemetría 433 MHz

**Revisión:** 2026-07-27
**Estado:** Active — banco terrestre únicamente

| ID | ParentRiskID | Riesgo | Prob. | Impacto | Owner role | Mitigación | Trigger | Due gate |
|---|---|---|---|---|---|---|---|---|
| R-433-01 | RSK-CONF-01 | Interferencia/pérdida ASK | Alta | Media | Bench RF/Ground SW | PER/gaps/duplicates/out-of-order por boot/session | PER supera criterio | Bench-433 evidence review |
| R-433-02 | RSK-CONF-01; RSK-RF-02 | Fuente/ruido degrada canal sin que `send()` lo reporte | Alta | Media | Bench RF/EMC | desacople/layout y métrica RX end-to-end; retorno TX no indica pérdida RF | PER/gaps cambian por fuente/modo | Bench-433 evidence review |
| R-433-03 | RSK-CONF-01 | Pinout/cableado incorrecto | Media | Media | Embedded/Test | pin map y checklist | boot/I2C/radio falla | Bench-433 evidence review |
| R-433-04 | RSK-CONF-01 | Banco se extrapola a arquitectura orbital | Media | Alta | Systems/QA | bench-only explícito | claim orbital lo cita | Each review |
| R-433-05 | RSK-ADCS-01; RSK-CONF-01 | Madgwick terrestre se extrapola a ADCS orbital | Alta | Alta | ADCS/Embedded/QA | accel correction solo 0.5–1.5 g; documentar caída libre | se usa para pointing orbital | Bench-433 evidence review |
| R-433-06 | RSK-ADCS-01; RSK-CONF-01 | Sensor→body no es rotación válida | Media | Alta | ADCS/Embedded | matriz ortonormal det +1; identidad hasta medir montaje | det≠+1/ejes invertidos | Bench-433 evidence review |
| R-433-07 | RSK-CONF-01 | Tasa RF excede airtime | Alta | Media | Embedded/Bench RF | filtro 100 Hz no bloqueante, RF 2 Hz, medir busy/dropped | loop bloquea o no logra 2 Hz | Bench-433 evidence review |
| R-433-08 | RSK-DATA-03 | PER mezcla reset/wrap/reorder | Media | Media | Ground SW | frame V4 `boot_id` + quality flags; stats session-aware | reboot crea pérdida artificial | Bench-433 evidence review |

## Límites

- RH_ASK 2000 bit/s.
- Paquete histórico 41 bytes: 164 ms mínimos solo para bits, sin overhead.
- Configuración actual: **2 Hz RF** y filtro IMU **100 Hz** no bloqueante.
- No constituye enlace ni ADCS orbital.

## Referencias

- `../08_Decisions/ADR-20260727-telemetry-bench-433-v4.md`
- `../docs/TELEMETRY_433_README.md`
