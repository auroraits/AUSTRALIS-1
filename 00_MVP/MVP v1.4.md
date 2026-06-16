# Documento Técnico — MVP v1.4 (CONSOLIDADO)

## Nanosatélite DIY Experimental 1.5U
**LoRa Uplink RX‑Only + UHF Downlink 1k2 + Science Pack + GNSS‑A**

**Versión:** 1.4 (baseline única y vigente)

---

## Regla de consolidación aplicada
Esta versión **1.4** consolida **MVP v1 → v1.1 → v1.3** bajo la siguiente jerarquía obligatoria:

- **v1.3 > v1.2 > v1.1 > v1**
- Toda decisión explícita en una versión superior **prevalece**.
- Ningún requisito, restricción u objetivo definido en versiones previas se pierde:
  - Si no entra en conflicto, **se incorpora**.
  - Si entra en conflicto, **se documenta y se resuelve** a favor de la versión superior.

El presente documento es el **único documento válido** para avanzar con el MVP.

---

## 0) Objetivo del MVP (conservado y reforzado)

### Objetivo principal (v1)
Demostrar una cadena **end‑to‑end real orbital**:

**Nodo terrestre (Buenos Aires, LoRa) → Satélite (RX) → Estación terrena (UHF) → Backend**

### Criterio de éxito mínimo (NO negociable)

1. Recepción en órbita de **≥10 paquetes LoRa** originados en Buenos Aires.
2. Descarga a tierra de esos paquetes vía **UHF 435 MHz ~1200 bps**.
3. Cada paquete debe incluir:
   - Timestamp
   - RSSI
   - SNR
   - CFO
   - CRC / integridad
4. Evidencia reproducible: logs persistentes + correlación con pasadas orbitales.

### Criterio de éxito extendido (MVP+ heredado)

- Operación estable ≥30 días
- >70 % de paquetes válidos por pasada
- Dashboard de telemetría histórica

---

## 1) Concepto de misión (CONOPS)

### Modo de servicio

**Store & Forward por ventanas orbitales**

- No existe servicio continuo (LEO + 1 satélite).
- Operación estricta por **ventanas de elevación**.

### Modos de operación (v1.3)

1. **SAFE MODE**
   - Beacon mínimo
   - Housekeeping
   - Consumo ultra bajo

2. **SCIENCE MODE**
   - Muestreo Science Pack
   - Logging persistente

3. **DOWNLINK WINDOW MODE**
   - Dump priorizado de datos
   - ARQ simple

Arranque **siempre en SAFE MODE** tras reset.

---

## 2) Decisiones de arquitectura BLOQUEADAS

### Form factor (decisión final)

- ❌ 1U (descartado por márgenes)
- ✅ **1.5U (10×10×15 cm)** — decisión heredada de v1.3

Justificación:
- Márgenes de potencia
- Separación EMI
- Inclusión Science Pack + GNSS
- Recuperabilidad

### Estrategia regulatoria (v1 + v1.3)

- **LoRa 915–928 MHz: RX‑ONLY en órbita**
- **No ISM TX desde espacio** en MVP
- Downlink por **UHF 435 MHz tipo amateur‑sat** (requiere coordinación/licencia)

---

## 3) Órbita objetivo

- Tipo: **LEO circular**
- Altitud: **500–600 km**
- Inclinación: compatible con múltiples pasadas sobre Buenos Aires

Órbita seleccionada para:
- Maximizar link budget uplink
- Vida orbital razonable
- Complejidad operativa baja

---

## 4) Segmento terrestre (heredado y ampliado)

### Nodos IoT (Buenos Aires)

- LoRa 915–928 MHz (AU915 o equivalente)
- TX típico: 20 dBm
- Antena: ¼ onda o dipolo
- Transmisión **solo dentro de ventana de pasada**
- Periodo: 30–120 s

### Estación terrena

- Antena UHF direccional (Yagi / Cross‑Yagi)
- LNA en mástil
- SDR o radio dedicado
- Decoder + backend + almacenamiento

---

## 5) Segmento espacial — arquitectura 1.5U

### Stack de subsistemas (bloqueado)

1. **EPS Board**
   - Paneles solares
   - Batería Li‑Ion
   - Reguladores DC/DC
   - Medición de rails

2. **OBC Board**
   - MCU: **STM32L4** (bajo consumo)
   - Watchdog HW externo
   - RTC con respaldo
   - Storage:
     - SPI NOR (logs críticos)
     - microSD industrial (bulk, tolerante a corrupción)

3. **RF Board**
   - LoRa RX 915 MHz
   - UHF TX/RX 435 MHz
   - Framing + ARQ simple
   - Filtros + aislamiento EMI

4. **Science Board (Science Pack)**
   - etapa HV de radiación (HV controlado)
   - Sensor UV (UVA/UVB)
   - Luz visible
   - Magnetómetro 3 ejes
   - ≥4 sensores de temperatura

5. **GNSS‑A**
   - Receptor GNSS UART
   - Antena patch
   - Best‑effort, no crítico

---

## 6) Antenas (decisiones heredadas)

- **UHF 435 MHz:**
  - Monopolo ¼ onda (~17 cm)
  - Desplegable (tipo cinta)

- **LoRa RX 915 MHz:**
  - Monopolo o dipolo simple

---

## 7) Presupuestos de diseño (obligatorios)

### Link Budget

- Downlink UHF 1k2 validado como viable
- Uplink LoRa viable con:
  - Elevación >20–30°
  - SF11–SF12
  - BW 125 kHz

### Power Budget

- SAFE MODE dominante
- Science + Downlink solo en ventanas
- Reset tolerante y frecuente asumido

---

## 8) Software de vuelo — principios obligatorios

- Boot determinista → SAFE MODE
- Logs idempotentes
- Tolerancia a reset/brownout
- Scheduler por ventanas
- GNSS opcional, nunca bloqueante

### Tramas mínimas

- BEACON
- SCIENCE_SUMMARY
- LORA_LOG
- ACK/NACK

Todas con CRC y numeración.

---

## 9) Plan de pruebas (V&V)

1. Banco:
   - Loopback UHF
   - Cortes de energía
   - Stress de storage

2. Campo:
   - Enlaces horizontales
   - Simulación de pasadas

3. Orbital:
   - Semana 1: solo beacon
   - Semana 2+: ciencia + LoRa RX

---

## 10) Estado del documento

- ✅ Todas las decisiones de v1, v1.1 y v1.3 preservadas
- ✅ Conflictos resueltos según jerarquía indicada
- ✅ Science Pack incluido
- ✅ 1.5U bloqueado

**Este documento habilita directamente:**
- Diseño eléctrico
- Block diagram final
- Firmware base
- Plan de estación terrena

---

**FIN — MVP v1.4**

