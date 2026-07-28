# COMMS — Riesgo CFO/Doppler LoRa

**Revisión:** 2026-07-27
**Estado:** Active

En 915 MHz se combinan Doppler orbital, error de reloj TX/RX, deriva térmica y
front-end. BW/receptor finales son TBD; no se supone que BW125 sea óptimo.

| ID | ParentRiskID | Riesgo | Prob. | Impacto | Owner role | Mitigación | Trigger | Due gate |
|---|---|---|---|---|---|---|---|---|
| COMMS-LORA-02 | RSK-COMMS-02 | CFO+Doppler impiden lock/PDR con nodo típico | Alta | Alta | COMMS/Node | Doppler ramp calibrado; error combinado TX+RX; cold/hot; comparar BW/receptores | PDR/IC bajo threshold preregistrado | Gate B |
| COMMS-LORA-03 | RSK-COMMS-02 | CFO estático de banco subestima dinámica orbital | Alta | Alta | COMMS/Node | perfil temporal de pasada con rate-of-change y adquisición inicial | static test pasa y ramp falla | Gate B |
| COMMS-LORA-04 | RSK-COMMS-02 | Canales BW250 se solapan con spacing histórico 200 kHz | Alta | Media | COMMS | frequency plan por BW, filtros/IF medidos y autorización | occupied bandwidths se solapan | Gate B |

## Gate de cierre

Gate B con hardware exacto, configuración/digests, raw IQ/logs y análisis de
incertidumbre.
