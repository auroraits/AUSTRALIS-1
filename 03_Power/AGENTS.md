# AGENTS.md — 03_Power (EPS)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
>
> **Separación de capas EPS (obligatoria):**
> - `EPS_Bench1_1S` = Bench. Validación funcional COTS, 1S. No hardware de vuelo.
> - `EPS_Flight_Like_2S_MPPT` = Flight-Like. PCB custom KiCad, 2S + MPPT. No calificado.
> - `EPS_Flight_2S_MPPT` = Flight. Hardware de vuelo definitivo. TBD.
>
> **Modelo operativo:** no referenciar "SCIENCE MODE" como modo canónico. Usar `MISSION_MODE = NOMINAL` con actividad científica como actividad interna.

## Propósito
EPS end-to-end:
- generación (paneles), almacenamiento (batería), distribución (rails), protecciones, telemetría y presupuestos de energía.

Documentos clave:
- `03_Power/Power Budget.md`
- `03_Power/EPS Sizing.md`
- `03_Power/EPS_Bench1_1S.md` (banco 1S, canónico)
- `docs/EPS/EPS_Bench1_1S.md` (histórico / trazabilidad)

## Cómo debe trabajar un agente aquí
- Toda decisión debe mapearse a:
  - presupuesto de potencia (W) y energía (Wh/orbita),
  - márgenes,
  - riesgos térmicos/seguridad.
- No “optimizar” números sin dejar supuestos explícitos.

Si se cambia química/capacidad/topología de batería, rails o perfiles de consumo:
- actualizar `06_Costs/`,
- actualizar `07_Risk/`,
- crear/actualizar ADR en `08_Decisions/`,
- reflejarlo en `00_MVP/MVP v2.2.md`.

## Entregables esperados
- Tabla de cargas (nominal / SAFE / DOWNLINK_WINDOW peak) — por capa EPS.
- Presupuesto por órbita.
- Requisitos de protección (OVP/OCP/UVLO) y brownout/reset behavior.
- Indicar explícitamente la capa (Bench/Flight-Like/Flight) en cada tabla/resultado.

## Reglas locales adicionales
- No usar `EPS_DESIGN_RULES.md` como fuente normativa. Es guía técnica draft.
- Conflicto de pico EPS (~3 W vs ~5 W): documentar como abierto (CONF-01) hasta medición real con hardware TX.
- No mezclar datos de bench 1S y flight-like 2S en el mismo análisis normativo.
