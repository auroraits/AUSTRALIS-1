# COMMS — Riesgo de slotting y timebase

**Revisión:** 2026-07-27
**Estado:** Active

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| COMMS-SLOT-01 | Deriva invade slot/guard | Alta | Alta | base temporal medida, cold/hot drift y fail-silent al perder validity; NTP no es supuesto | worst-case invade guard |
| COMMS-SLOT-02 | Schedule no llega o es inválido | Media | Media | schedule autenticado/expirable; fail-silent. B1 exige autorización separada | nodo transmite con schedule inválido |
| COMMS-SLOT-03 | Hash genera colisiones persistentes/near-far | Alta | Alta | ToA correcto, Monte Carlo, percentiles, retries y load cap | PDR bajo threshold |
| COMMS-SLOT-04 | Capacidad usa preámbulo/ToA incorrectos | Alta | Alta | cálculo LoRa independiente y test con analizador/airtime | airtime medido excede slot |

Gate B debe fijar cantidad de nodos, canales no solapados, PHY, jitter, retry,
PDR e intervalo de confianza.
