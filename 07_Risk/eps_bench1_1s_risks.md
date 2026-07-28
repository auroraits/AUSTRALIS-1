# EPS Bench1 1S — Risk Matrix

**Revisión:** 2026-07-27
**Scope:** banco 1S y riesgo de extrapolación

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| EPS-B1-01 | CN3065 sin MPPT no representa vuelo | Alta | Alta | etiquetar Bench; medir solo objetivos locales | dato se usa en budget orbital |
| EPS-B1-02 | BMS mal conectado anula protección | Media | Alta | checklist P+/P− y fault test | no corta OVP/UVP/OCP |
| EPS-B1-03 | Módulos COTS dispersos falsean resultados | Alta | Media | registrar lote/configuración y medir cada unidad | rails fuera de tolerancia |
| EPS-B1-04 | Telemetría insuficiente oculta causa | Alta | Media | V/I/T raw, sample/accuracy/calibration | falla sin datos correlacionados |
| EPS-B1-05 | Banco se presenta como diseño de vuelo | Alta | Crítica | stage separation y revisión de claims | BOM/test bench cierra requisito flight |
| EPS-B1-06 | Panel/Vmp no mantiene cargador | Alta | Media | curva I-V real en rango ambiental | Vmp cae bajo rango funcional |
| EPS-B1-07 | KiCad 2S placeholder se fabrica | Alta | Crítica | bloqueo Gate D; reconstruir, ERC/BOM/DRC/release | orden de PCB/partes antes de review |
| EPS-B1-08 | Rail IA 5V externo se extrapola a EPS 2S | Alta | Alta | evidencia limitada a bench; flight rail independiente | claim de potencia/boot de vuelo |

**Riesgo residual:** alto. El banco habilita aprendizaje funcional, no reduce el
riesgo del diseño 2S flight-like actual.
