# COMMS — Riesgo: slotting requiere hora/sync (nodos típicos)

**Review date:** 2026-02-20

## Resumen
El modo B (slotted) mejora la escalabilidad del uplink con nodos típicos, pero depende de que:
- el nodo tenga una noción razonable de hora UTC (o al menos epoch boundaries), y
- si se usa B2 (pass-aware), el nodo reciba ventanas de pasada por un canal externo (internet/manual).

## Risk matrix

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger condition |
|---|---|---|---|---|---|
| COMMS-SLOT-01 | Error de hora/deriva en nodos causa desalineación de slots y colisiones | Media | Alta | Guard time conservador; jitter; re-sync periódico (NTP si existe); usar epochs cortos; opción B1 always-on si no hay schedule | Colisiones altas en pruebas / baja tasa de paquetes válidos vs esperado |
| COMMS-SLOT-02 | Falta de canal para distribuir ventanas de pasada (B2) reduce efectividad del esquema | Media | Media | Usar B1 (always-on) o distribuir schedule por internet/archivo; mantener fallback de transmisión periódica | Los nodos no transmiten durante pasadas o transmiten fuera de ventana |

## Referencias
- `04_Communications/uplink_lora_slotted_protocol.md`
