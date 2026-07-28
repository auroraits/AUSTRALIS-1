# COMMS — Riesgo de slotting y timebase

**Revisión:** 2026-07-27
**Estado:** Active

| ID | ParentRiskID | Riesgo | Prob. | Impacto | Owner role | Mitigación | Trigger | Due gate |
|---|---|---|---|---|---|---|---|---|
| COMMS-SLOT-01 | RSK-COMMS-02 | Deriva invade slot/guard | Alta | Alta | Node FW/COMMS | base temporal medida, cold/hot drift y fail-silent al perder validity; NTP no es supuesto | worst-case invade guard | Gate B |
| COMMS-SLOT-02 | RSK-COMMS-03; RSK-SEC-02 | Schedule no llega o es inválido | Media | Media | Node FW/Security | schedule autenticado/expirable; fail-silent. B1 exige autorización separada | nodo transmite con schedule inválido | Gate B |
| COMMS-SLOT-03 | RSK-COMMS-02 | Hash genera colisiones persistentes/near-far | Alta | Alta | COMMS/Node | ToA correcto, Monte Carlo, percentiles, retries y load cap | PDR bajo threshold | Gate B |
| COMMS-SLOT-04 | RSK-COMMS-02 | Capacidad usa preámbulo/ToA incorrectos | Alta | Alta | COMMS/Node | cálculo LoRa independiente y test con analizador/airtime | airtime medido excede slot | Gate B |

Gate B debe fijar cantidad de nodos, canales no solapados, PHY, jitter, retry,
PDR e intervalo de confianza.
