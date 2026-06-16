# Documento Técnico — MVP v1.1 (1U / DIY / Arduino-compatible)

## 1) Objetivo (no cambia)

**Demostrar conexión end-to-end** y capturar métricas para iterar:

* **Nodo BA (LoRa 915) → Satélite (RX only) → Estación terrena (UHF downlink) → Backend**

**Criterio de éxito mínimo:**

* ≥10 paquetes LoRa recibidos en satélite y bajados a tierra con **RSSI/SNR/CFO/timestamp**.

---

## 2) Restricciones 1U (las que mandan el diseño)

En 1U vas a estar limitado por:

* **Potencia promedio** (típico 1–2 W promedio realista sin magia).
* **Antenas** (necesitás desplegable sí o sí para UHF eficiente).
* **Tiempo de radio** (downlink corto por pasada y tasa baja).
* **Robustez** (Arduino “de maker” funciona en banco, pero en órbita necesitás watchdog, brownout, memoria con ECC si se puede, y tolerancia a resets).

**Decisión clave MVP:** simplicidad extrema y telemetría exhaustiva.

---

## 3) Órbita y operación (ajustada al uplink LoRa)

**Órbita objetivo:** LEO 500–600 km (misma recomendación)

**Operación para maximizar uplink LoRa:**

* Definir un **umbral de elevación** para “ventana útil” (ej. solo transmitir cuando la pasada esté por encima de 20–30°).
  Esto te da 2 ventajas: baja el FSPL y suele mejorar geometría/antena.
* Los nodos transmiten **cada 30–120 s** solo dentro de ventana útil.
* El satélite escucha “siempre que puede” (o por schedule para ahorrar).

---

## 4) Arquitectura 1U (bloques y componentes sugeridos)

### 4.1 OBC (Arduino-compatible, pero serio)

Recomendación práctica: **MCU ARM** con core Arduino, no AVR.

* **SAMD51** (Arduino-compatible) o **STM32** (Arduino core)
* **Watchdog independiente** (ideal externo) + supervisor de tensión (brownout real)
* Almacenamiento: **microSD industrial** o **SPI NOR flash** + journaling simple
* RTC + (ideal) **GNSS** si el presupuesto lo permite (para timestamp real)

### 4.2 Payload LoRa (RX only)

* Chip tipo **SX1276/78** (LoRa clásico) o equivalente.
* Antena RX 915:

  * En 1U, una opción viable: **monopolo desplegable corto / dipolo simple** (aunque sea RX).
  * Si no desplegás, igual podés recibir, pero perdés margen y estabilidad.

**Métricas obligatorias por paquete:**

* RSSI, SNR, **CFO** (offset de frecuencia, proxy Doppler), CRC, timestamp.

### 4.3 Downlink UHF (satélite → estación)

* En 1U DIY, lo más pragmático:

  * **UHF 435 MHz** (enfoque satélite de aficionados), baja tasa (1k2 a 9k6).
  * Transceptor basado en chip tipo **Si4463** / **CC1120** / módulo UHF similar.
* Antena UHF:

  * **Cinta métrica** (tape-measure monopole) desplegable es lo más usado por CubeSats por simplicidad.
  * Un monopolo ¼ de onda en 435 MHz es ~17 cm: entra desplegado.

> Nota: aunque sea “banda típica”, **no es “sin regulación”**; lo “probado” acá significa *ecosistema y práctica*. En MVP te conviene tratar el downlink como “radioaficionado por satélite” (cumpliendo reglas) o, si más adelante querés comercial, cambiar el esquema.

### 4.4 EPS (potencia) minimalista

* Paneles: en 1U, probablemente 2–4 caras útiles + (si se puede) deployables (pero complica).
* Batería: Li-ion con BMS adecuado.
* MPPT (ideal) o al menos cargador eficiente.
* Medición: V/I batería, V/I panel, V/I rails.

### 4.5 ADCS mínimo (opcional pero recomendable)

* Magnetómetro + magnetorquers.
* Aunque sea “coarse”, te mejora:

  * estabilidad de enlace UHF
  * consistencia de patrón de antena
  * interpretación de datos RF

---

## 5) Estación terrena 100% DIY (pero efectiva)

Para que el MVP funcione, **la estación vale tanto como el satélite**.

**Recomendado:**

* Antena UHF direccional: **cross-yagi** (10–14 dBi típico) o yagi simple con polarización ajustable.
* **LNA** cerca de antena + buen coaxial.
* Receptor: **SDR** (RTL-SDR como mínimo, ideal uno con mejor rango dinámico) + demod software.
* Tracking:

  * MVP: manual con predicción de pasadas.
  * Ideal: rotor az/el (DIY con motores + control).

---

## 6) Link budget preliminar (con supuestos explícitos)

### 6.1 Downlink UHF 435 MHz (sat → ground) — **muy viable**

**Supuestos:**

* TX satélite: 1 W (30 dBm) *o incluso 100 mW (20 dBm)*
* G_tx sat: 0 dBi (monopolo)
* G_rx ground: 12 dBi (yagi/cross-yagi)
* Pérdidas: 3 dB (cables, mismatch, pointing imperfecto)
* Distancia slant:

  * buena elevación: ~600 km
  * baja elevación: ~2000 km

**FSPL (aprox):**

* 435 MHz @ 600 km: **140.8 dB**
* 435 MHz @ 2000 km: **151.2 dB**

**Potencia recibida (aprox):**

* Caso bueno (600 km, 1 W):
  P_rx ≈ 30 + 0 + 12 − 140.8 − 3 = **−101.8 dBm**
* Caso malo (2000 km, 100 mW):
  P_rx ≈ 20 + 0 + 12 − 151.2 − 3 = **−122.2 dBm**

Eso es compatible con enlaces de baja tasa bien diseñados (1k2/9k6) con buenas cadenas RF.
**Conclusión:** downlink UHF es el camino correcto para el MVP.

---

### 6.2 Uplink LoRa 915 MHz (nodo → sat, RX only) — **viable si restringís geometría**

**Supuestos realistas MVP:**

* TX nodo: 20 dBm (módulos LoRa 915 típicos)
* G_tx nodo: 0 dBi (antena simple)
* G_rx sat: +2 a +3 dBi si la antena es decente (o 0 dBi si muy básica)
* Pérdidas: 3 dB
* Distancias:

  * buena elevación: ~600–1200 km
  * baja elevación: ~2000 km

**FSPL:**

* 915 MHz @ 600 km: **147.2 dB**
* 915 MHz @ 1200 km: **153.3 dB**
* 915 MHz @ 2000 km: **157.7 dB**

**P_rx ejemplo con G_rx sat=3 dBi:**

* 600 km: 20 + 0 + 3 − 147.2 − 3 = **−127.2 dBm**
* 1200 km: 20 + 0 + 3 − 153.3 − 3 = **−133.3 dBm**
* 2000 km: 20 + 0 + 3 − 157.7 − 3 = **−137.7 dBm**

LoRa en modos robustos puede detectar cerca de ~−137 dBm (depende BW/SF/implementación).
**Conclusión:** para que el uplink sea “confiable”, tu regla operativa debe ser:

* **Transmitir solo en pasadas con elevación razonable** (no apurar baja elevación).
* Empezar con **modos muy robustos**.

---

## 7) Tabla de modos LoRa recomendados (MVP)

La idea: arrancar con robustez, medir CFO/Doppler real y luego optimizar.

| Modo                     |      BW |    SF | Uso                                   | Pros                    | Contras            |
| ------------------------ | ------: | ----: | ------------------------------------- | ----------------------- | ------------------ |
| R1 (Ultra robusto)       | 125 kHz |    12 | primer contacto, elevación media/alta | máximo alcance          | time-on-air alto   |
| R2 (Robusto)             | 125 kHz |    11 | operación normal MVP                  | buen margen             | time-on-air alto   |
| B1 (Balance)             | 125 kHz |    10 | si R2 va sobrado                      | más throughput          | menos margen       |
| E (Experimental Doppler) | 250 kHz | 10–11 | medir tolerancia CFO                  | más tolerancia a offset | menor sensibilidad |

**Regla MVP:** arrancás con **R1/R2**, guardás CFO/SNR por paquete, y después pasás a B1/E cuando tengas datos.

---

## 8) Tramas y almacenamiento (simple pero auditables)

### 8.1 Uplink LoRa (nodo → sat)

Payload sugerido (ejemplo):

* NodeID (4B)
* Seq (2B)
* Timestamp nodo (4B opcional)
* Data (hasta 20–30B)
* CRC (LoRa lo aporta, pero podés agregar app-CRC)

### 8.2 Registro en satélite (por paquete)

* sat_time (GNSS/RTC)
* NodeID, seq
* RSSI, SNR, CFO
* config mode (SF/BW)
* CRC ok/fail

### 8.3 Downlink UHF (sat → ground)

* Housekeeping + lote de mensajes LoRa + checksums
* Enviar “resumen” primero (cuántos paquetes, rango tiempos), luego “dump” completo.

---

## 9) Plan de desarrollo DIY (Arduino-first → PCB)

### Etapa A — prototipo (100% dev kits)

* MCU Arduino-compatible + LoRa RX module + UHF module + sensores EPS
* Simular “pasada”:

  * variar frecuencia (CFO)
  * mover antenas
  * probar pipeline end-to-end con ground station

### Etapa B — prototipo integrado (stack de PCBs)

* 2–3 placas apiladas:

  1. EPS
  2. OBC + storage
  3. RF (LoRa RX + UHF TX) + filtros/duplex si aplica

### Etapa C — flight candidate 1U

* componentes seleccionados por temperatura y vibración
* conectores mínimos
* harness corto
* plan de “reset seguro” (watchdog + fallback firmware)

---

## 10) Riesgos específicos de “Arduino en el espacio” (y cómo mitigarlos)

* **Radiación / SEU / latch-up**: vas a tener resets.
  → Mitigación: watchdog, firmware idempotente, logs, “safe mode” UHF.
* **microSD corrupta**:
  → Mitigación: journaling simple, doble archivo, o SPI NOR.
* **RFI interna**:
  → Mitigación: buen layout RF, planos de masa, filtrado en EPS.
* **Antena deploy** falla:
  → Mitigación: mecanismo ultra simple, test de despliegue repetido, redundancia si cabe.

---

# Decisiones cerradas (v1.1)

* Satélite **1U**.
* Payload LoRa **solo RX** (915).
* Downlink a tierra por **UHF** (probado para CubeSats), estación DIY direccional.
* Estrategia uplink: **ventanas de elevación** + modos LoRa robustos + medición CFO/SNR.

---

