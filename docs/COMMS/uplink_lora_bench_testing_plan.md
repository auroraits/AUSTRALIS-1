# COMMS — Uplink LoRa Bench Testing Plan (P1)

**Fecha de revisión:** 2026-02-20
**Objetivo:** cerrar factibilidad de uplink LoRa 915 con nodos típicos (RFM95W) y validar el modo B2 (slotted + predicción de pasadas).

## 1) Alcance
- Validar PHY y robustez (SF/BW/CR/preamble/payload).
- Medir tolerancia a **CFO** (offset de frecuencia) y a condiciones de "casi borde".
- Validar slotting con múltiples nodos (colisiones, tasa CRC OK).

> Esto NO reemplaza pruebas de campo con antenas reales, pero reduce incertidumbre y evita sorpresas de protocolo.

## 2) Hardware mínimo
- 2–10 nodos TX: ESP32 + RFM95W (ideal: al menos 3 para colisiones).
- RX:
  - opción A (mínima): otro SX1276 (single‑channel) para test PHY básico.
  - opción B (objetivo): **LoRa concentrator** (multi‑canal / multi‑SF) + logging de RSSI/SNR/CFO.
- Antenas: al menos 2 tipos:
  - "mala" (whip genérica),
  - "mejorada" (dipolo o 1/4 con plano de masa).
- Atenuadores/caja metálica o distancia controlada para no saturar RX.

## 3) Testcases

### T1 — ToA y configuración base
- Configurar baseline: SF12/BW125/CR4/5/preamble16/payload12B.
- Verificar ToA real vs esperado.

### T2 — Sensibilidad relativa (comparativa)
- Con atenuación creciente o distancia creciente (si es posible): comparar CRC OK vs nivel.
- Objetivo: establecer un umbral práctico y márgenes aproximados.

### T3 — CFO (offset de frecuencia)
- Simular CFO configurando el TX con offsets (ej. ±5, ±10, ±20, ±30 kHz) alrededor del canal.
- Medir tasa de demodulación/CRC OK.
- Repetir con BW125 y BW250.

### T4 — Multi‑node collisions: ALOHA vs slotted
- Mismo PHY.
- N nodos transmitiendo:
  - ALOHA con jitter (baseline negativo),
  - slotted determinístico (modo B).
- Métricas: rx_total, CRC OK, colisiones estimadas.

### T5 — Redundancia 2× y 2 canales
- Primary en f1 + retry en f2.
- Comparar vs 1 canal.

### T6 — Scheduler (modo B2) con “pasada simulada”
- Emular ventana de 6 min con slots.
- Validar que cada nodo respeta su slot, incluso con drift (introducir drift artificial en RTC si se puede).

## 4) Métricas a registrar
- Por paquete:
  - timestamp RX,
  - node_id, seq,
  - RSSI, SNR,
  - CFO/offset estimado (si el RX lo da),
  - CRC ok/fail.
- Agregados por ventana:
  - total, ok, fail,
  - per-node ok.

## 5) Criterio de salida (P1)
- Elegir un baseline operativo (SF/BW/canales/redundancia) con evidencia:
  - CFO tolerable,
  - tasa de CRC OK aceptable en slotted,
  - y plan de fallback (BW250 o diversidad de frecuencia).

## 6) Referencias
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `07_Risk/comms_lora_cfo_doppler_risk.md`
