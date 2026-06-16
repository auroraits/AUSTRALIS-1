# EPS Bench1 1S — Cost Model (Bench)

**Review date:** 2026-04-03
**Moneda:** USD (**TBD** conversión local)
**Estado:** estimación documental de banco (sin cotización cerrada)

## Alcance
Modelo de costos para `EPS_Bench1_1S` orientado a validación funcional.
Incluye la extensión bench-only para Gate IA-2: FPM bench + rail IA bench-only + inyección externa de 5V para CM5 real.

## BOM económico (rangos)

| Grupo | Low (USD) | Expected (USD) | High (USD) | Nota |
|---|---:|---:|---:|---|
| COTS modules | TBD | TBD | TBD | CN3065, BMS 1S, Boost 5V, Buck 3V3 |
| Discretos y protección | TBD | TBD | TBD | 1N5817, fusible 1A, pasivos |
| Conectores/cableado | TBD | TBD | TBD | Borneras/JST/cables |
| Delta Gate IA-2 bench-only | TBD | TBD | TBD | `J_AI_PWR`, harness 5V, `F_AI`, `SW_AI` TBD, `JP1` 2x12 |
| Interfaz CM5 bench | TBD | TBD | TBD | Carrier board COTS, adaptación UART/niveles, `AI_THERM` |
| Metrología IA bench | TBD | TBD | TBD | Instrumentación adicional para `T20` / `T21`; `INA219` extra solo como bench option |
| Instrumentación bench | TBD | TBD | TBD | No incluida en costo unitario EPS final |

## Cost drivers
- Disponibilidad local de módulos COTS.
- Variabilidad por lote de convertidores DC/DC.
- Disponibilidad/costo del delta bench-only de Gate IA-2.
- Selección del switch principal `SW_AI` una vez medida la corriente real del CM5.
- Costo de transición de módulo a IC en PCB custom.

## Relación con evolución EPS
- `EPS_Bench1_1S`: costo de validación rápida (bench-only).
- Extensión Gate IA-2: costo adicional bench-only para integrar CM5 real en banco sin cambiar la arquitectura de vuelo.
- `EPS_Flight_Like`: incremento por PCB custom, fabricación y ensamble.
- `EPS_Flight`: incremento adicional por calificación y ensayos ambientales.

## Referencias
- `03_Power/EPS_Bench1_1S.md` (documento canónico, sección BOM).
- `docs/EPS/BOM_EPS_Bench1_1S.md` (histórico).
- `08_Decisions/ADR-20260218-eps-bench1s-cots-to-custom-flight-pcb.md`.
