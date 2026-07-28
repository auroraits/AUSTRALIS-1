# COMMS — Riesgo de factibilidad LoRa Tierra→espacio

**Revisión:** 2026-07-27
**Estado:** Active — técnica y regulación abiertas

El satélite RX-only no autoriza una emisión intencional Tierra→espacio en
915 MHz. Aun con autorización, el enlace con nodo típico puede no alcanzar
margen/PDR suficientes.

| ID | ParentRiskID | Riesgo | Prob. | Impacto | Owner role | Mitigación | Trigger | Due gate |
|---|---|---|---|---|---|---|---|---|
| COMMS-LORA-01 | RSK-COMMS-01 | Link/PDR no cierra con clase típica | Alta | Alta | COMMS | link budget completo, patrón integrado y PDR calibrado con N/IC | worst-case bajo threshold | Gate B |
| COMMS-LORA-REG-01 | RSK-REG-01 | ENACOM no autoriza 915 MHz Tierra→espacio | Alta | Crítica | Regulatory/COMMS | consulta escrita; migrar servicio/banda, autorización experimental o redefinir objetivo | no existe respuesta favorable antes de radiar | SRR/Gate B |
| COMMS-LORA-05 | RSK-SEC-03 | CRC/16-bit node ID se interpreta como prueba de origen | Alta | Alta | Security/Node/Science | identidad/version/MIC/anti-replay y provenance | spoof/replay aceptado | Gate B/TRR |

## Referencias

- `../08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`
- `../01_Mission/mission_definition.md`
