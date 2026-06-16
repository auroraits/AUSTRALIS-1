# AGENTS.md — 01_Mission (Misión, requisitos, compliance y validación)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
> **Documentos clave locales:** `mission_definition.md`, `requirements_matrix.md`, `compliance_matrix.md`, `validation_plan_and_stage_gates.md`.

## Propósito
Define la misión y los requisitos que “manejan” todo el diseño:
- statement de misión, órbita, payload, requisitos, criterios de éxito.

**Documento principal del subsistema:** `01_Mission/mission_definition.md`

## Cómo debe trabajar un agente aquí
- Especificar requisitos con lenguaje verificable: “shall / must”.
- Separar: objetivos (nice-to-have) vs requisitos (must-have).
- Mantener trazabilidad hacia subsistemas (COMMS/EPS/estructura/software).

Si se cambian requisitos o el criterio de éxito:
- actualizar `00_MVP/MVP v2.2.md`,
- crear/actualizar un ADR si el cambio redefine arquitectura o alcance.

## Plantilla sugerida por documento
- Contexto y objetivos
- CONOPS
- Requisitos (funcionales / no funcionales)
- Supuestos
- Interfaces externas (lanzador, ground segment)
- Criterios de éxito y medición

## Chequeos de consistencia
- Requisitos de COMMS ↔ `04_Communications/`
- Potencia/energía ↔ `03_Power/`
- Masa/volumen ↔ `02_Structure/`
- Compliance y validación ↔ `compliance_matrix.md`, `validation_plan_and_stage_gates.md`

## Reglas locales adicionales
- La compliance matrix (`compliance_matrix.md`) debe actualizarse al cierre de cada stage-gate.
- Los requisitos `shall` deben tener fuente normativa (ADR `Accepted` o `00_MVP/MVP v2.2.md`); no usar `EPS_DESIGN_RULES.md` (draft) como fuente normativa.
- No declarar como cerrado nada que dependa del ICD del integrador hasta recibirlo.
