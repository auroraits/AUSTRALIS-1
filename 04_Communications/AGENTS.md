# AGENTS.md — 04_Communications (RF, LoRa, antenas, ground)

> **Hereda:** todas las reglas del `AGENTS.md` raíz (`/AGENTS.md`). Este archivo solo agrega reglas locales del subsistema.
>
> **Nodo típico LoRa:** definir como clase, no como SKU. Ver `ADR-20260313-nodo-tipico-lora-clase.md`.
>
> **OpenLST:** análisis técnico activo, no baseline final. No adoptar "tal cual". RFFM6403 es EOL. Requiere ADR de adopción para convertirse en baseline.
>
> **TTC UHF:** hardware final TBD. Baseline operativo vigente: UHF 435 MHz FSK 1200 bps.

## Propósito
Define el sistema de comunicaciones:
- bandas, radio(s), antenas, link budget, framing/protocolo, y ground station.

Documentos clave:
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/link_budget_uhf_preliminary.md`
- `04_Communications/ground_station_dual_use_satnogs_australis.md`

## Cómo debe trabajar un agente aquí
- Mantener un link budget trazable (tabla) con supuestos explícitos.
- Separar: requisitos regulatorios/legales vs decisiones técnicas.

Si se cambia banda, potencia TX, ganancia de antena, modulación o data rate:
- actualizar riesgos (regulatorio + interferencias) en `07_Risk/`,
- actualizar costos en `06_Costs/`,
- ADR obligatorio en `08_Decisions/`,
- actualizar `00_MVP/MVP v2.2.md`.

## Entregables esperados
- Tabla de link budget (uplink/downlink) con supuestos de clase de nodo explícitos.
- Lista de radios/antenas candidatos con pros/cons y estado de supply chain.
- Plan de pruebas en tierra (range tests).
- Para TTC UHF: verificar disponibilidad de componentes (sin EOL crítico).

## Reglas locales adicionales
- No fijar SKU de nodo como requisito normativo. Usar clase de nodo.
- No promover OpenLST a baseline final sin ADR nueva `Accepted`.
- No depender de RFFM6403 en ningún diseño. Alternativa de PA discreto requerida.
- Parámetros TBD de uplink LoRa (elevación mínima, canalización, BW): dejar como TBD hasta evidencia de banco/campo.
