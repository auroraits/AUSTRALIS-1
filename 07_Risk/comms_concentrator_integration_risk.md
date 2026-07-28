# COMMS — Riesgo de receptor LoRa concentrator

**Revisión:** 2026-07-27
**Estado:** Active — selección reabierta

Un concentrator multicanal/multi-SF puede aportar capacidad, pero no demuestra
por sí mismo mejor sensibilidad que un receptor simple y agrega potencia,
masa, software, térmica y EMI. SX1302/SX1303 y el front-end completo deberán
compararse contra alternativas con hardware medido.

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| COMMS-RX-01 | Concentrator excede allocations o no aporta ventaja RF | Alta | Alta | Trade study medido: sensibilidad/PDR, CFO/Doppler, blocking, consumo, masa y software | no supera receptor simple o excede budget |
| COMMS-RX-02 | Sleep COTS se confunde con OFF seguro | Media | Alta | rail power-gated, leakage/boot/backfeed medidos | corriente OFF supera allocation |
| COMMS-RX-03 | UHF/EPS/CM5 desensibilizan RX | Alta | Alta | mode matrix, aislamiento, filtros y blocker/EMC tests | noise floor/PDR varía por modo |
| COMMS-RX-04 | BOM/documentos mezclan SX1302/SX1303 | Media | Media | congelar módulo/front-end/reloj por ConfigurationID | evidencia usa hardware distinto |

La ADR histórica del concentrator está superseded. Selección y parámetros
permanecen TBD hasta Gate B.

## Referencias

- `../08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`
- `../01_Mission/verification_cross_reference_matrix.csv`
