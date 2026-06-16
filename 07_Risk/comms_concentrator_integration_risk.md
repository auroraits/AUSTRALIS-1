# COMMS — Riesgo: integración de LoRa concentrator en vuelo (potencia/EMI/complexidad)

**Review date:** 2026-06-15

## Resumen
Se eligió explorar un RX orbital tipo **LoRa concentrator** para mejorar probabilidad de uplink con nodos típicos.
Esto incrementa complejidad, consumo y riesgo de integración (EMI con EPS/UHF, thermal, software).

La referencia cuantitativa de sizing incorporada al power budget es un COTS de clase SX1303 HAT:
- RX con GNSS ON: **99 mA @ 5 V ≈ 0.495 W**.
- Sleep COTS con GPS OFF: **41 mA @ 5 V ≈ 0.205 W**; no aceptarlo como sustituto de OFF real.
- TX LoRa COTS: del orden de **3.55 W**; permanece prohibido en el CONOPS MVP.

Estos valores son de especificación y no reemplazan medición de banco integrada.

## Risk matrix

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger condition |
|---|---|---|---|---|---|
| COMMS-RX-01 | El concentrator excede presupuesto de potencia/EMI o no integra bien en stack 1.5U | Media | Alta | Selección con mediciones de consumo; power-gating con OFF real; layout/filtrado; pruebas en FlatSat; modo degradado (single-channel) | Medición en banco muestra consumo/ruido fuera de margen; fallas en UHF o EPS durante RX |
| COMMS-RX-02 | El COTS concentrator queda en sleep en vez de OFF real y consume energía residual significativa | Media | Media | Rail switchable medido; requerir corriente OFF/fuga compatible con SAFE; validar secuencia de apagado | Corriente fuera de ventana comparable a sleep COTS (~0.205 W) o caída de margen energético |
| COMMS-RX-03 | Simultaneidad UHF TX + concentrator RX + microSD write causa brownout o ruido acoplado | Media | Alta | Política inicial de no simultaneidad; prueba FlatSat con peor caso; fallback single-channel | Reset, `PGOOD_RF` falso, pérdida de frames UHF o corrupción de logs |

## Referencias
- `08_Decisions/ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx.md`
- `03_Power/Power Budget.md`
