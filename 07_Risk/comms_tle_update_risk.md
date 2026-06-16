# COMMS/OPS — Riesgo: TLE desactualizado degrada predicción de pasadas (modo B2)

**Review date:** 2026-02-20

## Resumen
El modo B2 (pass-aware) depende de predicción de pasadas con TLE+SGP4. Si el TLE está desactualizado, la ventana calculada puede correrse y reducir la probabilidad de uplink.

## Risk matrix

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger condition |
|---|---|---|---|---|---|
| OPS-TLE-01 | TLE viejo desplaza la ventana uplink y baja la tasa de recepción | Media | Alta | Ventanas más anchas al inicio; elevación mínima conservadora; disciplina de actualización TLE out-of-band; fallback a B1 always-on slotted | Resúmenes por pasada muestran caída sistemática de rx_total vs esperado |

## Referencias
- `05_Software/node_uplink_scheduler_pass_prediction.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
