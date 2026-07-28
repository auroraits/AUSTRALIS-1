# Riesgos — Banco de telemetría 433 MHz

**Revisión:** 2026-07-27
**Estado:** Active — banco terrestre únicamente

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| R-433-01 | Interferencia/pérdida ASK | Alta | Media | PER/gaps/duplicates/out-of-order por boot/session | PER supera criterio |
| R-433-02 | Fuente/ruido degrada canal sin que `send()` lo reporte | Alta | Media | desacople/layout y métrica RX end-to-end; retorno TX no indica pérdida RF | PER/gaps cambian por fuente/modo |
| R-433-03 | Pinout/cableado incorrecto | Media | Media | pin map y checklist | boot/I2C/radio falla |
| R-433-04 | Banco se extrapola a arquitectura orbital | Media | Alta | bench-only explícito | claim orbital lo cita |
| R-433-05 | Madgwick terrestre se extrapola a ADCS orbital | Alta | Alta | accel correction solo 0.5–1.5 g; documentar caída libre | se usa para pointing orbital |
| R-433-06 | Sensor→body no es rotación válida | Media | Alta | matriz ortonormal det +1; identidad hasta medir montaje | det≠+1/ejes invertidos |
| R-433-07 | Tasa RF excede airtime | Alta | Media | filtro 100 Hz no bloqueante, RF 2 Hz, medir busy/dropped | loop bloquea o no logra 2 Hz |
| R-433-08 | PER mezcla reset/wrap/reorder | Media | Media | frame V4 `boot_id` + quality flags; stats session-aware | reboot crea pérdida artificial |

## Límites

- RH_ASK 2000 bit/s.
- Paquete histórico 41 bytes: 164 ms mínimos solo para bits, sin overhead.
- Configuración actual: **2 Hz RF** y filtro IMU **100 Hz** no bloqueante.
- No constituye enlace ni ADCS orbital.

## Referencias

- `../08_Decisions/ADR-20260727-telemetry-bench-433-v4.md`
- `../docs/TELEMETRY_433_README.md`
