# ADR-20260313-eps-separacion-bench-flightlike-flight

- **Fecha:** 2026-03-13
- **Estado:** Accepted

---

## Contexto

La documentación del EPS (Electrical Power System) tenía ambigüedades en la separación entre el banco de validación (1S, COTS) y las capas de flight-like y flight (2S + MPPT). En algunos documentos el banco se describía de forma que podía malinterpretarse como arquitectura de vuelo. La política COTS-to-Flight estaba definida conceptualmente pero no había una separación explícita de tres capas con nombres canónicos.

---

## Decisión

Se adopta una separación inequívoca de tres capas EPS con nombres canónicos:

| Capa | Nombre canónico | Descripción |
|---|---|---|
| Bench | `EPS_Bench1_1S` | Hardware COTS para validación funcional y desarrollo de firmware. Topología 1S. **No es hardware de vuelo.** |
| Flight-Like | `EPS_Flight_Like_2S_MPPT` | Arquitectura eléctrica en PCB custom (KiCad). Topología 2S + MPPT. No calificado de vuelo. Para integración y pruebas de sistema. |
| Flight | `EPS_Flight_2S_MPPT` | Hardware final de vuelo. 2S + MPPT. Política COTS-to-Flight completa. TBD. |

**Reglas:**
1. El banco 1S sirve para validar: carga solar, protección de batería, rails regulados, power-gating, telemetría, watchdog de OBC y firmware. No para dimensionamiento de vuelo.
2. La arquitectura flight-like y de vuelo es **2S + MPPT** (bloqueada por `ADR-20260218-battery-topology-2s-flight`).
3. Toda BOM, plan de pruebas y documento de costos debe indicar explícitamente la capa.
4. No se mezclan líneas de bench y flight-like en la misma entrada de BOM.
5. Las reglas de `03_Power/EPS_DESIGN_RULES.md` son guía técnica `Draft` y aplican principalmente al diseño de las capas flight-like y flight.

---

## Alternativas consideradas

1. **Dos capas (bench / flight)**: rechazada. La capa flight-like es necesaria para integración y pruebas antes de comprometer diseño de vuelo final.
2. **Una sola capa (bench = desarrollo)**: rechazada. No captura la separación de intención entre validación funcional y arquitectura integrable.
3. **Tres capas explícitas con nombres canónicos** (elegida).

---

## Tradeoffs / riesgos

- A favor: elimina ambigüedad documental; facilita trazabilidad de BOM; aclara qué evidencia aplica a qué capa.
- En contra: overhead de mantener tres capas en documentación y BOM.
- Riesgo residual: que la capa flight-like se trate como "suficientemente buena para vuelo". Mitigación: documentar explícitamente que flight-like requiere calificación adicional para convertirse en flight.

---

## Implicancias (archivos actualizados)

- `03_Power/EPS_Bench1_1S.md` — cabecera con advertencia de capa actualizada.
- `03_Power/EPS Sizing.md` — sección de separación de capas agregada.
- `01_Mission/mission_definition.md` — §10 separación de capas.
- `01_Mission/requirements_matrix.md` — MIS-REQ-13 agregado.
- `01_Mission/compliance_matrix.md` — CX-EPS-01 referenciando esta ADR.
- `06_Costs/BOM_master.csv` — columna `Stage` con valores Bench/Flight-Like/Flight/EGSE.
- `SYSTEM_BASELINE.md` — §3.7 actualizado.
- `architecture.md` — §8 actualizado.
- `AGENTS.md` — §9 política separación.
- `README.md` — tabla de separación EPS.
