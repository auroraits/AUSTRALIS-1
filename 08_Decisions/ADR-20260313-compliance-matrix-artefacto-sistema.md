# ADR-20260313-compliance-matrix-artefacto-sistema

- **Fecha:** 2026-03-13
- **Estado:** Accepted

---

## Contexto

El proyecto carecía de una matriz de compliance viva que trazara los requisitos del sistema con el estado de cumplimiento, evidencia y dependencias del integrador de lanzamiento. Sin esta matriz, hay riesgo de llegar al PDR/CDR del integrador con requisitos no trazados o evidencia faltante.

---

## Decisión

Se adopta la compliance matrix como **artefacto vivo obligatorio** del sistema:

- **Ruta:** `01_Mission/compliance_matrix.md`
- **Formato:** tabla Markdown con columnas mínimas: `ID`, `Requirement`, `Source`, `Owner`, `Verification`, `Evidence`, `Status`, `Notes`.
- **Estados permitidos:** `Open`, `Partial`, `Closed`, `Blocked by Integrator`.
- **Mantenimiento:** debe actualizarse al cierre de cada stage-gate y cuando se obtiene nueva evidencia.
- **Ítems mínimos:** cubiertos en la versión inicial (2026-03-13), incluyendo mecánica, RF/regulatorio, EPS, software y PHOTO_DEMO.

---

## Alternativas consideradas

1. **No tener compliance matrix**: rechazada. Riesgo de incumplimiento con integrador.
2. **Spreadsheet externo**: rechazada. El repositorio es la fuente de verdad.
3. **Solo requirements_matrix**: rechazada. La requirements_matrix define los requisitos; la compliance matrix traza el estado de cumplimiento con evidencia.
4. **Compliance matrix en el repo** (elegida).

---

## Tradeoffs / riesgos

- A favor: trazabilidad completa; clarifica qué está abierto vs cerrado; facilita PDR/CDR.
- En contra: overhead de mantenimiento.
- Riesgo residual: que no se actualice oportunamente. Mitigación: regla de DoD incluye actualizar compliance matrix.

---

## Implicancias (archivos actualizados)

- `01_Mission/compliance_matrix.md` — creado.
- `01_Mission/requirements_matrix.md` — MIS-REQ-15 agregado.
- `01_Mission/validation_plan_and_stage_gates.md` — referencia a compliance matrix en criterios de salida de gates.
- `architecture.md` — tabla de ADRs actualizada; regla de propagación incluye compliance matrix.
- `AGENTS.md` — §16 DoD incluye compliance matrix.
- `SYSTEM_BASELINE.md` — §8 referencias operativas incluye compliance matrix.
