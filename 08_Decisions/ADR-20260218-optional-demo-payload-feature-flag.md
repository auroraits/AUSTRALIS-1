# ADR-20260218-optional-demo-payload-feature-flag

- **Fecha:** 2026-02-18
- **Estado:** Superseded
- **Supersedida por:** `ADR-20260313-photo-demo-opcional-no-critico.md` (2026-03-13)

> Esta ADR queda en estado `Superseded`. Las decisiones sobre PHOTO_DEMO están formalizadas en `ADR-20260313-photo-demo-opcional-no-critico.md`.

## Contexto
Se requiere evaluar un payload DEMO de fotografía de alto riesgo/bajo impacto sin comprometer la misión principal ni el framework permanente.

<!-- FEATURE:PHOTO_DEMO START -->

## Decisión [PHOTO_DEMO]
- Integrar [PHOTO_DEMO] como feature encapsulado y desactivable por power-gating.
- Mantener estado OFF por defecto al boot.
- En downlink, usar solo cola best-effort (`OPTIONAL_PAYLOAD`) con cuota por pasada.
- Flujo operativo: catálogo de thumbnails → selección por uplink → transferencia por chunks reanudables.

## Alternativas consideradas [PHOTO_DEMO]
1. Incluir [PHOTO_DEMO] como payload crítico (rechazada).
2. Excluir totalmente [PHOTO_DEMO] de MVP (viable, pero se pierde demostración).
3. Feature encapsulado con flag documental (elegida para evaluación).

## Tradeoffs / riesgos [PHOTO_DEMO]
- A favor: demostración incremental sin afectar cadena principal.
- En contra: complejidad adicional de manejo de archivos/chunks.
- Riesgo residual: fallas de captura/transferencia; mitigación por aislamiento y apagado.

## Implicancias (archivos actualizados) [PHOTO_DEMO]
- `00_MVP/MVP v2.2.md`
- `01_Mission/mission_definition.md`
- `02_Structure/Block Diagram.md`
- `03_Power/Power Budget.md`
- `03_Power/EPS Sizing.md`
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/link_budget_uhf_preliminary.md`
- `05_Software/software_framework_mvp22.md`
- `architecture.md`

<!-- FEATURE:PHOTO_DEMO END -->
