# COMMS — Riesgo de factibilidad LoRa Tierra→espacio

**Revisión:** 2026-07-27
**Estado:** Active — técnica y regulación abiertas

El satélite RX-only no autoriza una emisión intencional Tierra→espacio en
915 MHz. Aun con autorización, el enlace con nodo típico puede no alcanzar
margen/PDR suficientes.

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| COMMS-LORA-01 | Link/PDR no cierra con clase típica | Alta | Alta | link budget completo, patrón integrado y PDR calibrado con N/IC | worst-case bajo threshold |
| COMMS-LORA-REG-01 | ENACOM no autoriza 915 MHz Tierra→espacio | Alta | Crítica | consulta escrita; migrar servicio/banda, autorización experimental o redefinir objetivo | no existe respuesta favorable antes de radiar |
| COMMS-LORA-05 | CRC/16-bit node ID se interpreta como prueba de origen | Alta | Alta | identidad/version/MIC/anti-replay y provenance | spoof/replay aceptado |

## Referencias

- `../08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`
- `../01_Mission/mission_definition.md`
