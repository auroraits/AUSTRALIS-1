# COMMS — Riesgo CFO/Doppler LoRa

**Revisión:** 2026-07-27
**Estado:** Active

En 915 MHz se combinan Doppler orbital, error de reloj TX/RX, deriva térmica y
front-end. BW/receptor finales son TBD; no se supone que BW125 sea óptimo.

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| COMMS-LORA-02 | CFO+Doppler impiden lock/PDR con nodo típico | Alta | Alta | Doppler ramp calibrado; error combinado TX+RX; cold/hot; comparar BW/receptores | PDR/IC bajo threshold preregistrado |
| COMMS-LORA-03 | CFO estático de banco subestima dinámica orbital | Alta | Alta | perfil temporal de pasada con rate-of-change y adquisición inicial | static test pasa y ramp falla |
| COMMS-LORA-04 | Canales BW250 se solapan con spacing histórico 200 kHz | Alta | Media | frequency plan por BW, filtros/IF medidos y autorización | occupied bandwidths se solapan |

## Gate de cierre

Gate B con hardware exacto, configuración/digests, raw IQ/logs y análisis de
incertidumbre.
