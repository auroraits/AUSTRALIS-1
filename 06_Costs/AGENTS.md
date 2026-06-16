# AGENTS.md — 06_Costs (Modelo de costos y BOM)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
>
> **BOM maestra:** `BOM_master.csv` con separación obligatoria Bench / Flight-Like / Flight / EGSE.
> No mezclar capas en la misma fila de BOM.

## Propósito
Centraliza:
- costo de construcción del satélite (BOM + estimaciones),
- costo de lanzamiento (rangos + supuestos),
- y sensibilidad (qué variables dominan el costo).

## Cómo debe trabajar un agente aquí
- No inventar precios: usar rangos y fuente/fecha si existe; si no, marcar **TBD**.
- Mantener moneda y fecha de referencia.

Cuando cambie un subsistema:
- actualizar BOM/costos relevantes,
- reflejar en `00_MVP/MVP v2.2.md`,
- si el cambio fue una decisión, el ADR debe referenciar impacto en costos.

## Entregables esperados
- `BOM_master.csv` con subsistemas, stages, candidatos, suppliers y costos.
- `bom_overview.md` como overview humano.
- Rangos (low/expected/high) con fuente/fecha.
- Cost drivers y notas de riesgo (importación, disponibilidad, EOL).

## Reglas locales adicionales
- Separar obligatoriamente: Bench / Flight-Like / Flight / EGSE.
- No inventar MPNs, precios ni fechas. TBD si falta dato.
- Alertar componentes EOL en la BOM y en `bom_overview.md`.
