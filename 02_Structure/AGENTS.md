# AGENTS.md — 02_Structure (Estructura + térmico + ambientes)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
>
> **Referencia mecánica:** CubeSat Design Specification Rev 14.1 (Cal Poly). Volumen nominal 1.5U = 100×100×150 mm. Orbita target: 500–600 km LEO.

## Propósito
Documenta:
- diseño mecánico (volumen, interfaces, materiales),
- térmico (rango operativo, disipación),
- vibración/shock (requisitos y consideraciones).

## Cómo debe trabajar un agente aquí
- Mantener enfoque “engineering notebook”: supuestos + justificación.
- No inventar certificaciones; si aplica un estándar, citarlo y marcar **TBD** si falta detalle.

Si se introduce nueva masa/volumen/interfaz:
- actualizar `00_MVP/MVP v2.2.md`,
- revisar impacto en EPS y COMMS,
- actualizar riesgos en `07_Risk/`.

## Formato recomendado
- Tablas: masas, dimensiones, interfaces mecánicas
- Secciones: thermal budget (alto nivel), materiales, consideraciones de prototipado
