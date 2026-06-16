# ADR-20260313-photo-demo-opcional-no-critico

- **Fecha:** 2026-03-13
- **Estado:** Accepted
- **Supersede:** `ADR-20260218-optional-demo-payload-feature-flag.md` (que pasa a estado `Superseded` por esta ADR)

---

## Contexto

La ADR anterior (`ADR-20260218-optional-demo-payload-feature-flag.md`) dejó `PHOTO_DEMO` en estado `Proposed`. El estado ambiguo permitía interpretaciones sobre si el payload podía considerarse parte del criterio de éxito o si podía bloquear el baseline. Esta ADR congela formalmente su posición.

---

## Decisión

`PHOTO_DEMO` queda **congelado** con las siguientes características normativas:

1. **Opcional** — no es parte del criterio mínimo de éxito del MVP.
2. **No crítico** — su falla no degrada la cadena principal de misión.
3. **OFF por defecto al boot** — off-by-default por hardware y software.
4. **Best-effort** — opera exclusivamente bajo cola `OPTIONAL_PAYLOAD` del Downlink Manager.
5. **Fuera del criterio mínimo de éxito** — los criterios 1-4 de `00_MVP/MVP v2.2.md` §1.2 no incluyen PHOTO_DEMO.
6. **No desplaza housekeeping ni comandos** — prioridad siempre por debajo de `HOUSEKEEPING` y `COMMAND_ACK`.
7. **No bloquea baseline** — puede existir o no existir sin afectar el resto del sistema.
8. **Encapsulado por feature flag** — delimitado por `<!-- FEATURE:PHOTO_DEMO START/END -->` en documentación.

---

## Alternativas consideradas

1. **Incluir PHOTO_DEMO como payload crítico**: rechazada. Aumenta riesgo sin beneficio de misión crítica.
2. **Excluir PHOTO_DEMO totalmente del MVP**: viable, pero se pierde demostración incremental.
3. **Mantener como Proposed indefinidamente**: rechazada. La ambigüedad crea riesgo documental y de diseño.
4. **Feature encapsulado, congelado como Accepted opcional** (elegida).

---

## Tradeoffs / riesgos

- A favor: demostración incremental sin comprometer misión; complejidad aislada y desactivable.
- En contra: complejidad adicional de manejo de archivos/chunks.
- Riesgo residual: fallas de captura/transferencia. Mitigación: aislamiento por Fault/Power Manager y apagado forzado.

---

## Implicancias (archivos actualizados)

- `00_MVP/MVP v2.2.md` — §17.6 agregado con freeze formal.
- `01_Mission/mission_definition.md` — sección §12 actualizada con estado Accepted.
- `01_Mission/requirements_matrix.md` — requisitos MIS-REQ-PH-01 a PH-04 actualizados.
- `01_Mission/compliance_matrix.md` — ítems CX-PH-01 y CX-PH-02 referenciando esta ADR.
- `architecture.md` — tabla de ADRs actualizada.
- `AGENTS.md` — §10 política PHOTO_DEMO.
