# Documento Técnico — MVP v1.3

## 1.5U DIY Nanosat: LoRa Uplink RX-Only + UHF Downlink 1k2 + Science Payload + GNSS-A

**Versión:** 1.3
**Prioridad:** robustez, recuperabilidad, telemetría rica
**Estrategia regulatoria MVP:** no transmitir ISM desde órbita (LoRa RX-only); downlink por UHF tipo amateur-sat (requiere coordinación/encuadre).

---

## 1) Requisitos (nivel sistema)

### R1 — Conectividad mínima

* Recibir paquetes LoRa 915–928 MHz desde 1–10 nodos en Buenos Aires (RX-only).
* Bajar a tierra esos paquetes + métricas RF por paquete mediante UHF 435 MHz a 1200 bps.

### R2 — Instrumentación científica mínima (Science Pack)

* Radiación ionizante: etapa HV de radiación CPS/CPM (con HV controlado).
* UV: UVA/UVB (I2C).
* Contexto: luz visible, magnetómetro 3 ejes, temperaturas multipunto (≥4).

### R3 — Tiempo y posición

* GNSS-A: receptor GNSS por UART + antena patch (best-effort).
* RTC con respaldo (batería/supercap).
* Operación tolerante a GNSS-fail (todo sigue funcionando con RTC).

---

## 2) Arquitectura por segmentos

### 2.1 Nodos terrestres (Buenos Aires)

* LoRa 915–928 (AU915 o equivalente).
* TX 20 dBm típico; antena ¼ onda o dipolo.
* Operación por ventanas de pasada (preprogramado por horario).

### 2.2 Segmento espacial (1.5U)

**Masa/volumen objetivo:** 1.5U (10×10×15 cm).

**Stack recomendado (4 PCBs):**

1. EPS Board
2. OBC Board (STM32 + RTC + storage + watchdog)
3. RF Board (LoRa RX + UHF TX/RX + front-end)
4. Science Board (etapa HV de radiación HV + UV + light + mag + temps)

### 2.3 Estación terrena DIY (Buenos Aires)

* Antena direccional UHF (yagi/cross-yagi), LNA en mástil, SDR/radio.
* Tracking manual asistido (MVP) o rotor az/el (ideal).
* Backend: demod + decod frames + DB + dashboard.

---

## 3) Selección de plataforma OBC (STM32 Arduino-compatible)

### 3.1 Familia recomendada (para v1.3)

* **STM32L4** (bajo consumo, suficiente potencia) **o** **STM32F4/F7** (más performance, más consumo).
  Para robustez-first en 1.5U, sugiero **STM32L4** salvo que necesites DSP/SDR (no es el caso).

### 3.2 Reglas de robustez (hard requirements)

* Watchdog **hardware** activado siempre.
* Brownout real (supervisor) + reset limpio.
* “Safe mode” por defecto tras reset.
* Logs idempotentes (no perder integridad si se reinicia durante escritura).

---

## 4) Telecomunicaciones

### 4.1 Uplink IoT (LoRa RX-only, 915–928)

**Modos cerrados (MVP):**

* R1: BW 125 kHz, SF12
* R2: BW 125 kHz, SF11
* E: BW 250 kHz, SF10–11 (solo para medición Doppler/CFO cuando R2 funcione)

**Métricas por paquete:**

* RSSI, SNR, CFO, CRC, timestamp sat, mode_id.

### 4.2 Downlink (UHF 435 MHz, 1200 bps, robusto)

* Modulación: AFSK/FSK robusta (1k2) + CRC por frame.
* Beacon periódico + dump con reanudación.

> Nota regulatoria: amateur-sat es “muy probado” pero no es “sin regulación”; requiere coordinación/encuadre.

---

## 5) GNSS-A + RTC (tolerante a GNSS-fail)

### 5.1 GNSS-A (best-effort)

* GNSS UART a OBC (sentencias NMEA o binario).
* Antena patch (montaje con plano de masa y clear view lo mejor posible en 1.5U).
* GNSS aporta:

  * timestamp absoluto preciso
  * (si disponible) posición/velocidad para correlación ciencia y enlace

### 5.2 RTC (obligatorio)

* RTC con cristal + respaldo.
* RTC es “source of truth” cuando GNSS no fija.

### 5.3 Política de sincronización tiempo

* Si GNSS Fix válido:

  * ajustar RTC (slew/step según criterio)
  * marcar `time_source = GNSS`
* Si GNSS no Fix:

  * usar RTC, marcar `time_source = RTC`
* Telemetría siempre incluye:

  * `time_source`, `rtc_drift_est` (estimado), `last_gnss_fix_age`

---

## 6) Science Payload Pack (Arduino-compatible)

### 6.1 etapa HV de radiación (radiación ionizante)

* Módulo HV + tubo etapa HV de radiación con salida TTL (pulsos).
* Contador por hardware (timer/counter) → CPS/CPM.
* HV controlado:

  * OFF por defecto
  * ON por ventanas programadas
  * medición de corriente HV para diagnóstico

### 6.2 UV

* VEML6075 (I2C): UVA/UVB + flags.

### 6.3 Luz visible

* Fotodiodo/ALS (I2C o analógico).

### 6.4 Magnetómetro 3 ejes

* I2C/SPI.

### 6.5 Temperaturas multipunto

* ≥4 sensores: batería, EPS, RF, Science.

---

## 7) Buses y asignación (topología)

**I2C-A (science bus):** UV + magnetómetro + ALS + temps digitales
**SPI-A (RF):** LoRa transceiver
**UART-A:** GNSS
**UART-B:** UHF modem / control (o SPI si el módulo lo requiere)
**SDIO/SPI-B:** storage (microSD industrial o SPI NOR)

**Hardware counter input:** etapa HV de radiación pulse line

**Regla:** RF y HV lejos de DC/DC; masas y retornos controlados; filtros LC para HV.

---

## 8) Modelo de datos y tramas (compacto, 1k2)

### 8.1 Tipos de tramas UHF

1. **BEACON** (cada 10–20 s)
2. **STATUS_EXT** (bajo demanda)
3. **SCI_SUMMARY** (periódico, cada 10 s en SCIENCE MODE)
4. **LORA_LOG** (dump de registros LoRa recibidos)
5. **EOT** (fin de transmisión)
6. **ACK/NACK** (control de reanudación)

### 8.2 BEACON (objetivo: “siempre llega”)

Campos mínimos:

* sat_time (RTC)
* time_source (GNSS/RTC)
* battery_v, battery_i, temp_batt
* mode (SAFE/SCI/DL)
* logs_pending (lora_count, sci_count)
* last_reset_reason

### 8.3 SCI_SUMMARY (cada 10 s)

Campos:

* sat_time
* geiger_cps (u16) + optional cpm (u16 cada 60 s)
* uva, uvb (u16,u16)
* light (u16)
* mag_xyz (i16×3) (o cada 30 s)
* temps[4] (i16×4, deci-°C)
* flags (hv_on, gnss_fix, eclipse_est, etc.)

### 8.4 LORA_LOG (por registro)

Registro fijo (32–40 bytes):

* sat_time (u32)
* node_id (u32)
* seq (u16)
* rssi_x10 (i16)
* snr_x10 (i16)
* cfo_hz (i16)
* mode_id (u8)
* flags (u8)
* payload_len (u8)
* payload (0..24)

### 8.5 Reanudación robusta (idempotencia)

* Cada frame tiene `frame_index`.
* Ground envía `ACK(last_ok_index)`.
* Satélite reanuda desde `last_ok_index + 1`.

---

## 9) CONOPS (operación por modos)

### 9.1 SAFE MODE (default tras reset)

* UHF beacon ON
* Housekeeping básico
* HV OFF
* LoRa RX OFF
* GNSS ON best-effort (puede duty-cycle si consumo)

### 9.2 SCIENCE MODE (programado)

* HV ON por ventanas (ej. 10 min ON / 20 min OFF)
* SCI_SUMMARY cada 10 s
* LoRa RX ON solo en ventanas de pasadas previstas (para ahorrar y reducir interferencias)

### 9.3 DOWNLINK WINDOW

* Beacon más frecuente (ej. cada 10 s)
* DUMP: primero STATUS_EXT + SCI_SUMMARY backlog + luego LORA_LOG
* Política: solo hacer dump en pasadas de elevación alta.

---

## 10) Plan de pruebas (Fases 0–3) + criterios de aceptación

### Fase 0 — Banco

**A0.1:** Downlink UHF 1k2 loopback con BER aceptable
**A0.2:** Contador etapa HV de radiación no pierde pulsos a CPS esperado
**A0.3:** Logging idempotente: cortar energía en escritura sin corromper

**Aceptación:** 24 h de ejecución continua con resets inducidos y recuperación.

### Fase 1 — Campo

**A1.1:** Estación terrena recibe beacon a distancia (pruebas horizontales)
**A1.2:** Medición RFI: 915 y UHF con SDR

**Aceptación:** beacon decodificado ≥95% en ventana de test.

### Fase 2 — Pseudo-orbital (recomendado)

Globo/avión (si viable):

* Validar tracking, pipeline, y datasets de science.

**Aceptación:** dump de logs completo en movimiento + correlación de tiempos.

### Fase 3 — Órbita

**Semana 1:** solo beacon + housekeeping estable
**Semana 2:** science windows + dumps
**Semana 3:** habilitar LoRa RX y colecta

**Aceptación MVP:** ≥10 paquetes LoRa recibidos y bajados con métricas + science summary consistente 7 días.

---

## 11) Lista corta de decisiones de implementación (para pasar a diseño eléctrico)

* OBC: STM32L4 Arduino-core (baseline)
* Storage: SPI NOR para logs críticos + microSD opcional para bulk
* GNSS: módulo UART + patch (best-effort)
* UHF: 1k2 robusto + framing corto + ARQ simple
* HV etapa HV de radiación: enable + medición corriente + schedule

---

## 12) Riesgos y mitigaciones (actualizado)

* **GNSS no fija:** sistema opera con RTC; logs marcados con `time_source`.
* **HV EMI afecta RF:** HV duty-cycle + filtros + separación física.
* **Downlink débil:** 1k2 + frames cortos + yagi + LNA.
* **Resets por SEU:** safe-mode default + comandos idempotentes + reanudación.

---

## Referencias de soporte (mínimas)

* Dimensiones 1.5U:
* Coordinación amateur-sat/IARU (principio):

---

