# ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx

- **Fecha:** 2026-02-20
- **Estado:** Accepted (preliminar — sujeto a validación en banco/campo)

## Contexto
El objetivo de misión del MVP requiere recibir en órbita paquetes LoRa 915 MHz originados en Buenos Aires usando nodos típicos (RFM95W/SX1276, +20 dBm) y bajar a tierra evidencia reproducible.

Problemas identificados:
- Uplink con nodos típicos es **justo**: sólo es realista en elevaciones altas.
- ALOHA puro escala mal por colisiones.
- En 915 MHz existen offsets significativos por Doppler + error de cristal (±10 ppm), que pueden degradar la demodulación.
- El downlink UHF 1k2 es cuello de botella: no es viable bajar todos los payloads por defecto.

## Decisión
Adoptar como baseline de operación del MVP (P1):

1) **Uplink LoRa (915 MHz) RX-only en satélite** desde nodos típicos.
2) Acceso múltiple: **Modo B2 slotted (pass-aware)**.
   - Los nodos (ESP32) calculan pasadas offline con **TLE+SGP4**.
   - Hora: RTC disciplinado por **GNSS 1 vez/día** (sin asumir NTP).
3) Receptor orbital: **LoRa concentrator** (multi‑canal/multi‑SF) priorizando **sensibilidad**.
4) Baseline success-first (primeras operaciones):
   - PHY: **SF12 / BW 125 kHz / CR 4/5 / CRC ON / preamble 16**.
   - Ventana uplink: **6 min** alrededor del pico de elevación.
   - Canalización inicial: **2 canales** (BW125) con retry en canal alterno.
   - Redundancia: **2 TX por ventana** (primary + retry) en slots distintos.
5) Downlink: filosofía **resumen primero; detalle on‑demand**.
   - Por defecto se baja resumen por pasada.
   - El detalle (payloads crudos) se descarga bajo comando TTC UHF y en múltiples pasadas si hace falta.

## Alternativas consideradas
- ALOHA puro (más simple, pero colisiones dominan y reduce probabilidad de éxito).
- "Gateway dedicado" en tierra (mejora margen pero no cumple el objetivo de nodos típicos).
- BW 250 kHz como baseline (más tolerante a CFO/Doppler pero menos sensibilidad).
- Uplink por TTC UHF en vez de LoRa (cambio de arquitectura/objetivo de misión).

## Tradeoffs / riesgos
- Requiere manejo de TLE (actualización out-of-band) y tolerancia a TLE viejo.
- Complejidad/consumo del concentrator RX vs SX1276 simple.
- Riesgo CFO/Doppler en BW125: mitigación por redundancia + canal alterno y posible diversidad de frecuencia.

## Implicancias
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `04_Communications/uplink_data_products_and_downlink_policy.md`
- `05_Software/node_uplink_scheduler_pass_prediction.md`
- `05_Software/node_tle_update_mechanism.md`
- `07_Risk/comms_*.md`
- `01_Mission/mission_definition.md` (operación summary-first + evidencia)

## Evidencia / próximos pasos
- Ejecutar `docs/COMMS/uplink_lora_bench_testing_plan.md`.
- Revisar si BW125 sostiene CFO/Doppler; si no, activar fallback a BW250 o diversidad de frecuencia.
