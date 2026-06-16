# AGENTS.md — 00_MVP (Documento maestro)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
>
> **Baseline vigente:** `MVP v2.2.md` es la fuente de verdad del sistema. Versiones anteriores (v1…v2.1) son historial, no canónicas ante conflicto.
>
> **Modelo operativo canónico:** `MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW` y `EPS_STATE = CRIT | LOW | NOMINAL | HIGH`. No usar "SCIENCE MODE" como modo canónico.

## Propósito
Esta carpeta contiene el **documento maestro** del proyecto (baseline de sistema).

- **Baseline vigente (fuente de verdad):** `00_MVP/MVP v2.2.md`
- `MVP v1`…`v2.1` se conservan como **historial** (no canónico ante conflicto).

## Cómo debe trabajar un agente aquí
- Prioridad: mantener `00_MVP/MVP v2.2.md` coherente con el resto del repositorio.
- Cuando cambie cualquier subsistema, el agente debe:
  1) reflejar el cambio en `00_MVP/MVP v2.2.md` (sección correspondiente),
  2) agregar/actualizar referencias cruzadas a los archivos del subsistema,
  3) crear/actualizar un ADR si cambió una decisión relevante,
  4) marcar **TBD** si falta dato (no inventar).

## Estructura esperada dentro de MVP v2.2
- Resumen ejecutivo (1–2 pantallas)
- Alcance del MVP (in/out)
- Requisitos de misión (alto nivel) + criterios de éxito
- Arquitectura por subsistema (links)
- Presupuestos (potencia/energía, link budget, masa/volumen) con supuestos
- Riesgos top-10 y mitigaciones
- Índice de ADRs vigentes (Accepted) y Superseded

## Definición de “Hecho” (DoD)
- Índice actualizado
- Referencias cruzadas intactas
- Sin contradicciones con ADRs **Accepted**
