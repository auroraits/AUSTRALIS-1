# Documento Técnico — MVP v1

## Nanosat IoT Experimental (LoRa Uplink + Downlink Satélite-a-Tierra probado)

**Versión:** 1.0 (MVP)
**Alcance:** prueba de conectividad + aprendizaje operativo orbital.
**Restricción clave:** **NO** se realiza downlink satélite→nodos IoT en esta etapa para minimizar riesgo regulatorio.

---

## 0) Objetivos y criterio de éxito

### Objetivo principal

Validar una cadena completa de comunicaciones y operación:

**Nodo (Buenos Aires) → Satélite (LoRa uplink) → Estación terrena (downlink sat) → Backend (decode + logging).**

### “Éxito MVP” (mínimo)

1. Recepción en el satélite de al menos **N ≥ 10** paquetes uplink LoRa provenientes de nodos en BA.
2. Descarga a la estación terrena de esos paquetes + **métricas RF por paquete**.
3. Evidencia reproducible: logs firmados con timestamp, RSSI/SNR/CFO, y correlación con ventana de pasada.

### “Éxito MVP+”

* Operación estable ≥ 30 días.
* > 70% de paquetes recibidos por pasada (con configuración robusta).
* Tablero de telemetría/operación con trending.

---

## 1) Concepto de misión

### Modo de servicio (por diseño)

**Store & Forward**: el satélite escucha uplinks durante cada pasada y almacena; luego baja a tu estación terrena cuando tiene enlace.

> No hay servicio continuo con un único satélite en LEO; el “servicio” es por ventanas de pasada.

---

## 2) Órbita recomendada y justificación

### Parámetros objetivo (MVP)

* **Órbita:** LEO circular
* **Altitud:** **500–600 km**
* **Inclinación:** **50–60°** (prioridad: cobertura BA + flexibilidad/costo)
  **o** **SSO ~97°** (prioridad: estándar nanosat + operaciones + acceso)

**Justificación técnica:**

* 500–600 km reduce drag vs VLEO y facilita vida útil.
* Footprint y duración de pasada adecuados para múltiples intentos diarios.
* El Doppler en LEO no se elimina “con órbita”; se gestiona con diseño RF/PHY y medición (se instrumenta CFO/Doppler).

### Nota sobre proveedor de inserción

TLON Space publicita inserción orbital dedicada para nanosats (“pick your orbit…”), alineada con el perfil del MVP (LEO). ([Tlon][1])

---

## 3) Arquitectura del sistema (segmentos)

### 3.1 Segmento Usuario (Nodos LoRa en Buenos Aires)

**Cantidad inicial:** 1–10 nodos

**Requisitos mínimos del nodo:**

* Banda: **915–928 MHz** (plan AU915 o configuración equivalente)
* TX: potencia típica del módulo (sin amplificadores en MVP)
* Antena: ¼ onda real / dipolo con ROE razonable
* Payload: 12–40 bytes
* Periodicidad: 30–120 s **solo durante ventana estimada de pasada** (para no inundar el canal)

**Regulación terrestre Argentina:** 915–928 MHz se encuadra en bandas “compartidas/sin autorización individual”, bajo Resolución 581/2018 y parámetros ENACOM (p.ej. 4653/2019). ([Enacom][2])

---

### 3.2 Segmento Espacial (Satélite)

**Plataforma sugerida:** 3U–6U CubeSat (recomendación: 3U si el bus lo permite; 6U si necesitás márgenes de potencia y antenas)

#### Payload IoT (Uplink LoRa – Receive Only)

* Receptor LoRa (915) con:

  * logging de **RSSI, SNR, CFO**, timestamp (GNSS si existe), CRC ok/fail
  * modos configurables SF/BW/CR (tabla en §6)
  * buffer local para ≥ 10.000 mensajes

**Importante:** el payload LoRa es **solo receptor** en MVP para minimizar riesgos regulatorios (no transmitís ISM desde órbita).

#### Telecom de downlink (Satélite → Estación terrena)

Acá hay que ser preciso con tu pedido: **en espacio no existe “banda sin regulación”**; lo que sí existe es **banda y equipamiento altamente probado** con un marco de acceso relativamente alcanzable: el **Servicio de Aficionados por Satélite (Amateur-Satellite Service)**, típicamente en **UHF 435–438 MHz** (y a veces VHF 145.8–146).
Esto está masivamente probado en CubeSats, con coordinación IARU. ([AMSAT-UK][3])

**Opción recomendada para MVP (probada en CubeSat):**

* **Downlink UHF 435–438 MHz**, modulación robusta (FSK/GMSK/BPSK), 1k2–9k6 bps inicialmente.
* Coordinación de frecuencias por **IARU** (proceso estándar) para evitar conflictos y operar ordenadamente en asignaciones de aficionados por satélite. ([AMSAT-UK][3])

**Marco argentino (amateur):** ENACOM gestiona licencias y reglamentos de radioaficionados; existe normativa y listados vigentes. ([Enacom][4])

> Nota realista: operar en bandas de aficionados no significa “sin permiso”; significa que el camino de coordinación/uso suele ser más accesible que una asignación comercial, pero requiere cumplir reglas del servicio (no uso comercial, identificaciones, etc.).

#### OBC/EPS/ADCS (mínimo viable)

* **OBC** con watchdog + almacenamiento (MMC/flash) + RTC.
* **EPS** con MPPT, batería Li-ion, medición de corrientes/voltajes por rail.
* **ADCS** mínimo: magnetómetro + magnetorquers (coarse), suficiente para estabilizar y mejorar patrón de antena.
* **Thermal** pasivo + sensores.

---

### 3.3 Segmento Terreno (Estación terrena en Buenos Aires)

**Arquitectura recomendada (mínimo viable):**

* Antena UHF direccional (yagi/cross-yagi) + LNA + SDR/receptor
* Seguimiento:

  * MVP: seguimiento manual asistido (software de tracking + rotor opcional)
  * Ideal: rotor az/el
* Decodificación:

  * demod + FEC + framing
* Backend:

  * ingesta de paquetes, base de datos, dashboard, export

---

## 4) Protocolo y flujo de datos

### 4.1 Uplink LoRa (nodo → satélite)

* Usar LoRa PHY (no necesariamente LoRaWAN completo en MVP).
* Paquete con:

  * NodeID (4–8 bytes)
  * seq
  * payload corto
  * CRC
* Sin downlink al nodo (esta etapa).

### 4.2 Downlink satélite → ground (UHF)

* Enlace “telemetría + store&forward”
* Tramas con:

  * header + sat timestamp
  * housekeeping
  * bloque de mensajes LoRa recibidos (con métricas RF)
  * CRC/FEC
* Planificar “dump windows” en pasadas con mejor elevación.

---

## 5) Telemetría y medición (obligatorio del MVP)

### 5.1 Métricas RF por paquete LoRa recibido

* RSSI
* SNR
* CFO (offset de frecuencia) y/o estimación Doppler
* SF/BW/CR
* Timestamp (ideal GNSS)
* Estado CRC

### 5.2 Telemetría satélite (housekeeping)

* Voltajes/corrientes por rail
* Estado batería (SOC estimado)
* Temperaturas críticas
* Estado ADCS (modo, tasas)
* Contadores:

  * pkts LoRa rx ok/fail
  * bytes almacenados
  * bytes downlink exitosos
  * resets/watchdog

### 5.3 Telemetría estación terrena

* SNR downlink por trama
* tasa de frames OK/fail
* espectro/ruido de fondo en UHF durante pasadas
* logs de tracking

---

## 6) Configuración RF LoRa (MVP: robustez > throughput)

### Recomendación de perfiles (para probar y medir)

Definir 3 “modes” conmutables por comando desde tierra (no desde nodos):

* **Modo R (Robusto):** SF alto, BW medio, payload mínimo
  Objetivo: primer contacto, tolerancia a enlace débil.
* **Modo B (Balance):** SF medio, BW medio, payload medio
  Objetivo: compromiso éxito/tiempo-en-aire.
* **Modo E (Experimental):** variaciones para caracterizar Doppler/interferencia
  Objetivo: dataset para fase 2.

> La selección exacta (SF/BW/CR) se fija con un mini link budget y pruebas terrestres/estratosféricas. En el MVP v1 no “bloqueo” valores sin tu presupuesto de potencia/antena y target de tasa.

---

## 7) Plan de pruebas por fases (para reducir riesgo antes de órbita)

### Fase 0 — Banco (laboratorio)

* Nodo → receptor LoRa en movimiento simulado (offsets de frecuencia)
* Downlink UHF en banco: loopback, BER básico

### Fase 1 — Campo

* Ensayos a larga distancia en BA / alrededores
* Perfil de interferencia en 915 y UHF

### Fase 2 — “Pseudo-orbital” (opcional pero muy valiosa)

* Globo estratosférico / avión / dron alto (si es viable)
* Objetivo: validar geometría + tracking + pipeline operativo

### Fase 3 — Operación orbital (MVP)

* Primera semana: sólo housekeeping y downlink estable
* Semana 2: habilitar escucha LoRa y colecta
* Semana 3+: iteración de perfiles R/B/E

---

## 8) Riesgos y mitigaciones

### R1 — Regulatorio (espacial)

* **Riesgo:** uso ISM desde órbita (TX) complica; mitigado porque MVP LoRa es RX-only.
* **Riesgo:** downlink en UHF amateur requiere coordinación IARU y cumplimiento de reglas del servicio. ([AMSAT-UK][3])

**Mitigación:** operar el downlink en asignaciones amateur con coordinación IARU + encuadre ENACOM (licencia/club/estación). ([Enacom][4])

### R2 — Enlace (uplink LoRa)

* **Riesgo:** SNR insuficiente en uplink.
  **Mitigación:** modo robusto + antenas correctas + baja tasa + limitar nodos.

### R3 — Operación (ground segment)

* **Riesgo:** estación terrena insuficiente (tracking, LNA, RFI).
  **Mitigación:** comenzar con downlink simple y robusto; priorizar elevaciones altas.

### R4 — Complejidad del satélite

* **Riesgo:** 1 satélite = 1 oportunidad.
  **Mitigación:** minimizar “novedad” en downlink, maximizar logging.

---

## 9) Entregables del MVP v1 (lo que deberías producir como “pack”)

1. **ICD** (interface control doc) Nodo↔Sat (payload) y Sat↔Ground
2. Diseño de tramas (uplink LoRa, downlink UHF)
3. Plan de operación (CONOPS) por semana
4. Esquema de telemetría + dashboard
5. Checklist de coordinación/licencias (IARU + ENACOM)
6. Plan de pruebas (Fase 0→3) con criterios de aceptación

---

## 10) Decisiones cerradas en este MVP v1

* **No** downlink a nodos en 915 (evitamos TX ISM desde órbita en MVP).
* Downlink sat→tierra usando banda **amateur-sat** (UHF 435–438) por ser el estándar de CubeSats y con coordinación IARU ampliamente establecida. ([CubeSatShop.com][5])
* Uplink IoT LoRa en 915–928 desde nodos en BA, bajo el marco de uso compartido terrestre. ([Argentina][6])

---

## Anexo A — Nota sobre TLON (encaje de inserción)

TLON Space declara “Dedicated Orbital Insertion” para nanosats, lo que calza con un MVP que necesita elegir órbita LEO práctica. ([Tlon][1])

---

