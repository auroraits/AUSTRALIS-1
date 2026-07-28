# COMMS — Riesgo de receptor LoRa concentrator

**Revisión:** 2026-07-27
**Estado:** Active — selección reabierta

Un concentrator multicanal/multi-SF puede aportar capacidad, pero no demuestra
por sí mismo mejor sensibilidad que un receptor simple y agrega potencia,
masa, software, térmica y EMI. SX1302/SX1303 y el front-end completo deberán
compararse contra alternativas con hardware medido.

| ID | ParentRiskID | Riesgo | Prob. | Impacto | Owner role | Mitigación | Trigger | Due gate |
|---|---|---|---|---|---|---|---|---|
| COMMS-RX-01 | RSK-COMMS-01 | Concentrator excede allocations o no aporta ventaja RF | Alta | Alta | COMMS | Trade study medido: sensibilidad/PDR, CFO/Doppler, blocking, consumo, masa y software | no supera receptor simple o excede budget | Gate B |
| COMMS-RX-02 | RSK-COMMS-01; RSK-EPS-01 | Sleep COTS se confunde con OFF seguro | Media | Alta | COMMS/EPS | rail power-gated, leakage/boot/backfeed medidos | corriente OFF supera allocation | Gate B |
| COMMS-RX-03 | RSK-RF-02 | UHF/EPS/CM5 desensibilizan RX | Alta | Alta | COMMS/EMC | mode matrix, aislamiento, filtros y blocker/EMC tests | noise floor/PDR varía por modo | Gate B/QAR |
| COMMS-RX-04 | RSK-CONF-01 | BOM/documentos mezclan SX1302/SX1303 | Media | Media | Configuration/COMMS | congelar módulo/front-end/reloj por ConfigurationID | evidencia usa hardware distinto | Gate B |

La ADR histórica del concentrator está superseded. Selección y parámetros
permanecen TBD hasta Gate B.

## Referencias

- `../08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`
- `../01_Mission/verification_cross_reference_matrix.csv`
