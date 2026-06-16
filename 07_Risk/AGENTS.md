# AGENTS.md — 07_Risk (Riesgos, FMEA liviano)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
>
> **Compliance matrix:** los riesgos de compliance con integrador se trazan en `01_Mission/compliance_matrix.md`.
> **Top-risks:** ver `top_risks.md` (actualizado a top-15 en 2026-03-13).

## Propósito
Gestiona riesgos técnicos, programáticos y regulatorios:
- matriz probabilidad/impacto,
- mitigaciones,
- y riesgo residual.

## Cómo debe trabajar un agente aquí
- Mantener riesgos accionables: cada riesgo debe tener mitigación concreta.

Cuando cambie arquitectura o un supuesto clave:
- revisar riesgos afectados y actualizarlos,
- linkear al ADR que causó el cambio,
- reflejar top-risks en `00_MVP/MVP v2.2.md`.

## Entregables esperados
- Risk matrix (tabla).
- Top-N riesgos con mitigación, owner y gate de cierre (ver `01_Mission/validation_plan_and_stage_gates.md`).
- Trigger conditions (cómo detectamos que el riesgo se materializa).

## Reglas locales adicionales
- Linkear cada riesgo al gate de cierre correspondiente.
- Riesgos de compliance con integrador: dejar como "Blocked by Integrator" hasta recibir ICD.
- No declarar riesgos cerrados sin evidencia de ensayo.
