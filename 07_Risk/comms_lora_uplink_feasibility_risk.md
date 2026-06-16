# COMMS — Riesgo de factibilidad uplink LoRa 915 (tierra→satélite)

**Review date:** 2026-02-20

## Resumen
El objetivo de misión del MVP incluye recepción de paquetes LoRa 915 MHz originados en Buenos Aires.
Si se interpreta “nodo” como un dispositivo LoRa típico (baja ganancia, potencia estándar, sin tracking), el uplink puede quedar sin margen suficiente, especialmente a elevaciones bajas.

## Risk matrix

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger condition |
|---|---|---|---|---|---|
| COMMS-LORA-01 | Uplink LoRa 915 no cierra con “nodos típicos” (EIRP bajo) en geometría real | Alta | Alta | (1) Cerrar link budget uplink LoRa con sensibilidad real y pérdidas; (2) redefinir “nodo” como gateway dedicado con antena direccional / operación por ventana; (3) definir elevación mínima operacional; (4) alternativa: mover uplink a TTC UHF | Link budget uplink muestra margen < 0 dB en condiciones objetivo; pruebas de campo no detectan paquetes a distancias representativas |

## Referencias
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `01_Mission/mission_definition.md`
