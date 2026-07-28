# EPS Bench1 1S — Risk Matrix

**Revisión:** 2026-07-27
**Estado:** Active — bench-only; riesgos abiertos
**Scope:** banco 1S y riesgo de extrapolación

| ID | ParentRiskID | Riesgo | Prob. | Impacto | Owner role | Mitigación | Trigger | Due gate |
|---|---|---|---|---|---|---|---|---|
| EPS-B1-01 | RSK-CONF-01; RSK-EPS-01 | CN3065 sin MPPT no representa vuelo | Alta | Alta | EPS/QA | etiquetar Bench; medir solo objetivos locales | dato se usa en budget orbital | Gate D |
| EPS-B1-02 | RSK-EPS-01 | BMS mal conectado anula protección | Media | Alta | EPS/Safety | checklist P+/P− y fault test | no corta OVP/UVP/OCP | Gate D |
| EPS-B1-03 | RSK-SUP-01; RSK-CONF-01 | Módulos COTS dispersos falsean resultados | Alta | Media | EPS/Configuration | registrar lote/configuración y medir cada unidad | rails fuera de tolerancia | Gate D |
| EPS-B1-04 | RSK-CONF-01 | Telemetría insuficiente oculta causa | Alta | Media | EPS/Test | V/I/T raw, sample/accuracy/calibration | falla sin datos correlacionados | Gate D |
| EPS-B1-05 | RSK-CONF-01 | Banco se presenta como diseño de vuelo | Alta | Crítica | Systems/QA | stage separation y revisión de claims | BOM/test bench cierra requisito flight | Gate A/each review |
| EPS-B1-06 | RSK-EPS-01 | Panel/Vmp no mantiene cargador | Alta | Media | EPS/Test | curva I-V real en rango ambiental | Vmp cae bajo rango funcional | Gate D |
| EPS-B1-07 | RSK-EPS-01 | KiCad 2S placeholder se fabrica | Alta | Crítica | EPS/QA | bloqueo Gate D; reconstruir, ERC/BOM/DRC/release | orden de PCB/partes antes de review | Gate D |
| EPS-B1-08 | RSK-CONF-01; RSK-AI-02 | Rail IA 5V externo se extrapola a EPS 2S | Alta | Alta | EPS/AI/QA | evidencia limitada a bench; flight rail independiente | claim de potencia/boot de vuelo | IA-2/Gate D |

**Riesgo residual:** alto. El banco habilita aprendizaje funcional, no reduce el
riesgo del diseño 2S flight-like actual.
