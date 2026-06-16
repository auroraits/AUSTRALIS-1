# COMMS — Riesgo: CFO/Doppler en LoRa 915 MHz (uplink)

**Review date:** 2026-02-20

## Resumen
En 915 MHz, el uplink desde LEO enfrenta offsets de frecuencia significativos:
- Doppler por velocidad orbital (orden de decenas de kHz),
- error de cristal del nodo (±10 ppm → ±9 kHz),
- deriva térmica y tolerancias del front‑end.

Con BW=125 kHz se maximiza sensibilidad pero se reduce tolerancia a offsets y errores de reloj.

## Risk matrix

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger condition |
|---|---|---|---|---|---|
| COMMS-LORA-02 | CFO+Doppler impiden demodulación estable en BW=125 kHz con nodos típicos (±10 ppm) | Media | Alta | (1) Medir tolerancia real con hardware (nodo + RX orbital); (2) fallback a BW=250 kHz si es necesario; (3) diversidad por firmware: retransmisión multi‑frecuencia; (4) operación solo a elevación alta | Pruebas muestran caída marcada de CRC OK o ausencia de lock con offsets simulados |

## Referencias
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
