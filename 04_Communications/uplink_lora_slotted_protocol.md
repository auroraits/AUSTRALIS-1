# Uplink LoRa (915 MHz) — Protocolo propuesto (Slotted, modo B)

**Fecha de revisión:** 2026-02-20
**Estado:** propuesta P1 (exploración de factibilidad con nodos típicos)

## 1) Objetivo
Permitir uplink desde **muchos nodos baratos** (RFM95W/SX1276, +20 dBm) maximizando:
- compatibilidad + costo bajo en nodo,
- probabilidad de recepción (uplink muy justo),
- capacidad (N nodos) evitando colisiones.

Se asume satélite **RX-only** en LoRa (sin downlink LoRa desde órbita).

## 2) Node class objetivo (clase de nodo — no SKU específico)

El nodo objetivo se define como **clase**, sin fijar SKU de mercado. Ver `08_Decisions/ADR-20260313-nodo-tipico-lora-clase.md`.

- Radio: clase **SX1262 / SX1276 o equivalente** (915 MHz).
- MCU: clase **ESP32-S3 o equivalente**.
- TX: +20 a +21 dBm (sin PA externo).
- Antena: simple, 0–2 dBi (sin antena direccional).
- Cristal: **±10 ppm** (comercial típico; sin TCXO).
- Restricción: solo se permiten mejoras de **antena** y **firmware**.

Ejemplos de clase (referencia, no normativa): RFM95W, módulos Heltec ESP32+SX1262, SX1276-based y equivalentes.

## 3) Idea central: modo B (slotted ALOHA determinístico)
En vez de ALOHA puro, cada nodo transmite en un **slot** determinístico calculado por firmware.

Beneficios:
- reduce colisiones sin requerir hardware extra,
- escala mejor (más nodos por pasada),
- facilita operación “sin coordinación en vivo”.

## 4) Dos variantes de operación (ambas firmware-only)

### B1) Always-on slotted (sin conocimiento de pasadas)
- El tiempo se divide en epochs fijas (ej. cada 60 s).
- Cada nodo transmite 1 vez por epoch en su slot.
- El satélite recibe lo que “engancha” durante la pasada.

Pros: nodos no necesitan efemérides/predicción de pasadas.
Contras: desperdicia energía/aire en tierra; capacidad efectiva menor.

### B2) Pass-aware slotted (recomendado — nodos calculan pasadas)
- Los nodos transmiten **solo** dentro de ventanas asociadas a pasadas (ej. 6 min alrededor de máxima elevación).
- Requiere que el nodo tenga **hora UTC razonable** (RTC disciplinado por GNSS 1 vez/día) y que pueda **calcular pasadas offline**.
- Implementación sugerida: TLE + propagador **SGP4** en el ESP32.

Pros: maximiza capacidad útil y energía; no depende de NTP.
Contras: requiere mantener TLE actualizado (out-of-band).

## 5) Parámetros PHY recomendados (baseline a validar)

### 5.0 Baseline de referencia para primeras operaciones (a validar)
Prioridad: **sensibilidad** (nodos típicos, enlace justo) y control de colisiones por slotting.

- PHY: **SF12 / BW TBD / CR 4/5 / CRC ON / explicit header**
- Preamble: **16** (robustez de sync)
- Payload objetivo: **12 B** (frame METEO)
- Redundancia: **2 TX por ventana** (primary + retry) en slots distintos.

> **BW definitivo: TBD.** BW125 maximiza sensibilidad pero es frágil ante la combinación de error de cristal (±10 ppm → ±9 kHz a 915 MHz) y Doppler orbital (±23 kHz típico en LEO). **BW250 es el candidato preferente para robustez** frente a CFO/Doppler. BW125 solo puede adoptarse como opción definitiva si la evidencia de banco/campo demuestra margen suficiente con hardware real de clase nodo, offset realista y tasa CRC OK aceptable. Ver §5.1, §5.2 y §13 Puntos abiertos.

Canalización sugerida (para mantener simple y con margen):
- **2 canales** de 125 kHz separados 200 kHz (ejemplo): `f1=915.2 MHz`, `f2=915.4 MHz`.
- Cada nodo manda primary en `f1` y retry en `f2` (reduce riesgo de interferencia puntual y ayuda con offsets).

Ventana uplink sugerida (si el nodo puede estimar pasadas):
- **6 min** alrededor del máximo de elevación (núcleo “alto” de la pasada).

Nota: todos estos parámetros deben quedar **tuneables** desde tierra (por comando TTC UHF) y/o por actualización de firmware de nodos.

### 5.1 Opción BW125 (máxima sensibilidad — requiere evidencia)
- LoRa: **SF12**, **BW 125 kHz**, **CR 4/5**, CRC ON

ToA (Time-on-Air) aproximado (payload 12 B): **~1.155 s**.

> **Advertencia CFO/Doppler:** BW125 queda en el límite de tolerancia frente a la combinación de offset de cristal (±10 ppm) y Doppler orbital (±23 kHz típico). Con hardware real de clase nodo (sin TCXO), el offset total puede acercarse al BW disponible para demodulación. **Solo adoptar BW125 como opción definitiva con evidencia experimental** que demuestre margen de PDR/CRC OK aceptable bajo condiciones realistas de pasada. Ver §13.

### 5.2 Opción BW250 (candidato preferente por robustez a CFO/Doppler)
- LoRa: **SF12**, **BW 250 kHz**, **CR 4/5**, CRC ON

ToA aproximado (payload 12 B): **~0.496 s**.

Nota: BW250 reduce sensibilidad ~3 dB vs BW125 (orden de magnitud), pero es significativamente más tolerante al offset combinado CFO+Doppler. **BW250 es el candidato preferente** mientras no haya evidencia experimental que respalde BW125. El BW definitivo queda **TBD** hasta Gate B.

## 6) Slotting: tamaño de slot y guard
Propuesta inicial (conservadora):
- `slot_len = ToA_max + guard`
- `guard = 250–500 ms` (para error de hora + drift + retardo de scheduling)

Ejemplos con payload 12 B:
- SF12/BW125: slot_len ≈ 1.155 s + 0.5 s ≈ **1.65 s**
- SF12/BW250: slot_len ≈ 0.496 s + 0.3 s ≈ **0.80 s**

Slots por ventana (ej. ventana = 4 min = 240 s):
- BW125: ~240/1.65 ≈ **145 slots**
- BW250: ~240/0.80 ≈ **300 slots**

## 7) Cálculo de slot por nodo (determinístico)

Inputs mínimos:
- `node_id` (16-bit)
- `epoch_id` (ej. minuto UTC o índice de ventana)
- `S = slots_por_epoch`

Propuesta:
- `slot_index = hash16(node_id XOR epoch_id) mod S`
- offset de inicio = `slot_index * slot_len`
- jitter dentro del slot: `±(guard/3)` para romper sincronías perfectas

## 8) Formato de payload recomendado (meteo)
Para minimizar ToA:

### 8.1 Frame METEO (12 bytes)
- `node_id` (uint16)
- `seq` (uint16)
- `temp_c_x100` (int16)
- `rh_x100` (uint16)
- `press_hpa_x10` (uint16)
- `batt_mV` (uint16)

### 8.2 Frame GNSS (opcional, raro)
Enviar GNSS solo cada X pasadas/día (no en cada uplink). Definir separado.

## 9) Receptor orbital “más robusto” (para mejorar uplink y ampliar capacidad)
Decisión de exploración (P1): usar **LoRa concentrator** (RX tipo gateway, multi‑canal/multi‑SF) para uplink.

Motivo:
- con nodos típicos el uplink es justo; un RX más robusto permite:
  - demodular múltiples SF (y a veces múltiples canales) en paralelo,
  - tolerar mejor coexistencia de muchos nodos,
  - registrar métricas por paquete (RSSI/SNR/CFO) con alta fidelidad.

Criterio adicional de diseño:
- priorizar **sensibilidad** sobre “cantidad máxima” (la capacidad se obtiene principalmente con slotting, no con BW enorme).

## 10) Clock / sincronización de slots — requisito de base temporal para B2

> **Restricción de sistema (ver `ADR-20260313-b2-uplink-timebase-requirement.md`):** El modo B2 NO puede depender implícitamente de un RTC interno sin validar.

### 10.1 Condiciones de aceptación para B2
Para que un nodo opere en B2 (pass-aware slotted), debe cumplir **al menos una** de las siguientes condiciones:

1. **Base temporal validada experimentalmente:** deriva medida del RTC/cristal dentro del guard time para el BW y slot_len elegidos, bajo condiciones de temperatura representativas.
2. **Cristal/RTC externo adecuado:** cristal de referencia de baja deriva (p. ej. 32.768 kHz con histéresis térmica conocida) que garantice la precisión requerida.
3. **Resincronización activa ≤24 h antes de la pasada:** el nodo disciplina su RTC con una fuente externa confiable (GNSS u otra) con periodicidad suficiente para el presupuesto de slot.
4. **Otra estrategia documentada y validada:** cualquier mecanismo que garantice el error temporal dentro del guard time, documentado con evidencia experimental.

### 10.2 Fallback obligatorio
Si ninguna de las condiciones anteriores se cumple → el nodo **shall operar en B1** (always-on slotted) hasta que la base temporal sea validada.

### 10.3 Supuesto de trabajo (pendiente de validación)
El supuesto de trabajo es: ESP32 + disciplina GNSS 1 vez/día. **Este supuesto debe validarse experimentalmente** para el guard time de slot elegido (ver §6), bajo condiciones de temperatura representativas del despliegue real. No se fijan cifras de deriva del RTC hasta tener medición con el hardware específico.

### 10.4 Riesgo documentado
El riesgo principal es: cristal de ESP32 con deriva térmica real mayor al guard time → slots desalineados en la práctica → colisiones → pérdida de paquetes. Ver `07_Risk/comms_uplink_slotting_time_sync_risk.md` y top-risk #3.

## 11) Firmware de nodo: cálculo de pasadas (offline)
- Los nodos (ESP32) calculan pasadas offline usando **TLE+SGP4**.
- Se disciplina el RTC con GNSS 1 vez/día.
- Documento guía: `05_Software/node_uplink_scheduler_pass_prediction.md`.

## 12) Downlink: filosofía “resumen primero; detalle on‑demand”
Para no saturar el downlink UHF:
- por defecto se baja un **resumen** (agregado) de recepción LoRa:
  - conteos por `node_id`, últimos `seq`, %CRC OK, estadísticas de RSSI/SNR/CFO,
  - y un “top‑N” de eventos/anomalías.
- el detalle (payloads crudos) se baja **solo** bajo comando (uplink TTC UHF):
  - seleccionar `node_id`/rango de tiempo/últimos K paquetes,
  - y permitir descarga en 1 o múltiples pasadas por chunks.

## 13) Puntos abiertos / TBD
- Definir canalización (cantidad de frecuencias) y spacing dentro de 915–928.
- Definir elevación mínima operacional del uplink para nodos típicos (probablemente ≥25–35°).
- Medir sensibilidad real del concentrator + front‑end RF y tolerancia a CFO/Doppler.
- Definir estrategia anti‑CFO/Doppler si BW=125 (ej. diversidad de frecuencia en nodo).

## 11) Referencias cruzadas
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `01_Mission/mission_definition.md`
- `07_Risk/comms_lora_uplink_feasibility_risk.md`
