# Documento Técnico — MVP v2.1 (Consolidado técnico)

## DIY Nanosat 1.5U — LoRa Uplink RX-Only + UHF Downlink + Science Pack + GNSS-A

**Estado:** consolidado vigente para ingeniería de sistema (sin cambios técnicos nuevos respecto a v1.4 + anexos).  
**Alcance:** integración coherente de `MVP v1`, `v1.1`, `v1.3`, `v1.4` y anexos de `Power Budget`, `EPS Sizing` e `ICD/Block Diagram`.

---

## 1) Objetivo del MVP y criterio de éxito

### 1.1 Objetivo principal
Validar una cadena orbital end-to-end real:

**Nodo IoT (Buenos Aires, LoRa) → Satélite (recepción) → Estación terrena (UHF) → Backend con trazabilidad completa.**

### 1.2 Criterio de éxito mínimo (obligatorio)
1. Recepción en órbita de **al menos 10 paquetes LoRa** originados en Buenos Aires.  
2. Descarga a tierra de esos paquetes por **downlink UHF ~435 MHz**.  
3. Registro por paquete de: timestamp, RSSI, SNR, CFO y estado de integridad/CRC.  
4. Evidencia reproducible con correlación a ventanas de pasada orbital.

### 1.3 Criterio de éxito extendido (MVP+)
- Operación estable durante 30 días o más.  
- Más de 70% de paquetes válidos por pasada (configuración robusta).  
- Telemetría histórica y trending operativo.

---

## 2) Criterios de consolidación y precedencia

- Se preserva toda información no contradictoria de versiones previas.  
- Ante conflicto, prevalecen decisiones de versiones más nuevas.  
- El baseline técnico final queda fijado por **MVP v1.4 + anexos técnicos v1.4**.

### 2.1 Decisiones bloqueadas
- **Form factor:** 1.5U (100 × 100 × 150 mm).  
- **CONOPS:** store & forward por ventanas orbitales.  
- **Comunicaciones:** LoRa en órbita como **RX-only** (sin TX ISM desde satélite en MVP).  
- **Downlink principal:** UHF 435 MHz con tasa robusta (baseline 1k2).  
- **Arquitectura de energía:** EPS con rails medidos, power-gating y lógica de energía por modos.
- **Topología de batería de vuelo:** 2S (dos celdas Li-ion en serie, 7.4 V nominal, target 6–10 Wh con celdas de ~1 000–1 500 mAh por posición).
- **Modulación downlink UHF:** FSK 1 200 bps.
- **Science Pack MVP:** UV, ALS/visible, magnetómetro 3 ejes, temperatura multipunto. **Geiger HV no incluido en MVP.**
- **UHF TX power RF:** 500 mW objetivo (derivado de link budget preliminar LEO 550 km).

---

## 3) Concepto de misión (CONOPS)

### 3.1 Modo de servicio
Servicio no continuo: operación por pasadas LEO sobre zona de interés, con almacenamiento a bordo y descarga diferida a estación terrena.

### 3.2 Modos operativos
1. **SAFE MODE (default post-reset)**  
   - Prioriza supervivencia, housekeeping y beacon mínimo.  
2. **SCIENCE MODE**  
   - Activa Science Pack con duty-cycles controlados.  
3. **DOWNLINK WINDOW MODE**  
   - Prioriza dump de datos con UHF TX/RX y control de energía.

### 3.3 Reglas operativas clave
- Boot determinista siempre a SAFE.  
- GNSS es best-effort y nunca bloquea operación.  
- En eclipse, baseline operativo conservador (SAFE por defecto).  
- Dump y actividades de alto consumo condicionadas a estado energético.

---

## 4) Órbita objetivo y operación

- **Tipo:** LEO circular.  
- **Altitud objetivo:** 500–600 km.  
- **Inclinación:** seleccionada para habilitar pasadas útiles sobre Buenos Aires (incluyendo opciones no SSO y SSO según acceso de lanzamiento).

### 4.1 Supuesto de ingeniería para presupuestos
Para dimensionamiento preliminar de energía se usa:
- Período orbital: 90 min.  
- Insolación/eclipse: 60/30 min.

Este perfil es de diseño preliminar y debe recalibrarse con órbita final y beta-angle.

---

## 5) Arquitectura del sistema por segmentos

## 5.1 Segmento usuario (nodos IoT)
- Banda de operación en tierra: 915–928 MHz (configuración regional equivalente).  
- Potencia típica de módulo LoRa (sin amplificación extra en MVP).  
- Antena simple eficiente (¼ onda o dipolo).  
- Tramas cortas (payload breve) y transmisión sólo durante ventanas estimadas de pasada.

## 5.2 Segmento espacial (satélite 1.5U)
Arquitectura modular por placas, con separación funcional y de ruido:

1. **EPS Board**  
   - Gestión solar, batería Li-ion, DC/DC, telemetría eléctrica por rail.

2. **OBC Board**  
   - MCU STM32L4 (bajo consumo), watchdog HW externo, RTC con respaldo, almacenamiento dual (NOR para crítico + microSD para bulk).

3. **RF Board**  
   - LoRa RX 915 MHz.  
   - UHF TX/RX 435 MHz para telemetría/dump con framing y reanudación robusta.

4. **Science Board**  
   - UV sensor, ALS/visible sensor, magnetómetro 3 ejes, sensores de temperatura multipunto (I2C). Sin HV en MVP.

5. **GNSS-A**  
   - UART + antena patch, uso no crítico para continuidad de misión.

### 5.3 Segmento terreno
- Antena UHF direccional (Yagi/Cross-Yagi), LNA, receptor SDR/radio, decoder y backend.  
- Seguimiento manual asistido o rotor az/el.  
- Pipeline de ingestión y persistencia para auditoría de paquetes.

---

## 6) Interfaces e integración (ICD consolidado)

### 6.1 Buses internos
- **SPI (OBC↔RF):** control de radio y framing.  
- **I2C (OBC↔Science):** sensores y housekeeping científico.  
- **UART (OBC↔GNSS):** posicionamiento/tiempo.  
- **GPIO:** enables, resets y control de estados.

### 6.2 Reglas de integración obligatorias
- Todos los subsistemas deben poder apagarse por control de potencia.  
- Todos los rails críticos deben tener medición (V/I) para gobernanza.  
- Ningún subsistema puede impedir entrada o permanencia en SAFE.

### 6.3 Criterios físicos de layout
- Separación RF y fuentes de ruido.  
- Integración mecánica por stack 1.5U compatible con despliegue de antenas.

---

## 7) Arquitectura de comunicaciones y datos

### 7.1 Uplink IoT (nodo→satélite)
- LoRa PHY con configuración priorizando robustez sobre throughput en MVP.  
- Operación por ventanas de pasada para evitar saturación de canal.

### 7.2 Downlink satélite→tierra
- Enlace UHF robusto (baseline 435 MHz, ~1200 bps), con tramas cortas, CRC y numeración.  
- Reanudación de transferencia para tolerar cortes por geometría/pérdida de enlace.

### 7.3 Tipos de tramas mínimas
- **BEACON**  
- **SCIENCE_SUMMARY**  
- **LORA_LOG**  
- **ACK/NACK**

Todas las tramas se manejan con integridad y secuencia para idempotencia operativa.

---

## 8) Presupuesto de potencia y dimensionamiento EPS

Ver política COTS-to-Flight en `03_Power/EPS Sizing.md` y `03_Power/Power Budget.md`.

## 8.1 Filosofía de diseño energético
- SAFE dominante para supervivencia sostenida.  
- SCIENCE y DOWNLINK habilitados por estado de energía (SOC/VBAT/temperatura).  
- Valores numéricos preliminares sujetos a validación en banco.

### 8.2 Consumos promedio de referencia por modo
- **SAFE avg:** ~0.143 W (objetivo ≤0.20 W).  
- **SCIENCE avg:** ~0.379 W (objetivo ≤0.5 W).  
- **DOWNLINK window avg:** ~1.14 W durante ventana.

### 8.3 Energía por órbita (referencia)
- Caso típico recomendado (SAFE + ventana downlink): **~0.381 Wh/orbita**.  
- Caso SCI en sol + SAFE en eclipse: **~0.371 Wh/orbita**.
- Nota: el cálculo anterior de 0.915 Wh/orbita asumía SCI durante eclipse y contradecía la política operativa; se corrige a SCI solo en sol.

### 8.4 Targets EPS bloqueados
- Objetivo de potencia neta disponible en sol: **≥1.2 W**.  
- Batería nominal de diseño recomendada: **~6–10 Wh** (margen operativo y envejecimiento).  
- Capacidad útil asegurada objetivo: **≥3 Wh**.  
- EPS preparado para picos eléctricos de **~4 W** sin brownout (1.5 W TX + 2,5 W margen para cargas simultáneas).  
- MPPT recomendado para márgenes de misión en 1.5U.

### 8.4.1 Banco EPS Hardware Actual
Componentes comprados actualmente para prototipo/banco:
- 2× Panel Solar Monocristalino 1.2W 5.5V 98×98 mm.
- Cargador Solar CN3065 (entrada 4.4–6.0 V, carga hasta 500 mA).
- Diodos Schottky 1N5819 / SS34.
- Fusibles plásticos 1 A T.
- Sensores de corriente/voltaje INA219.

> Aclaración de arquitectura: el CN3065 se usa para prototipo y banco de pruebas; es un cargador solar lineal y **no implementa MPPT real**. La recomendación para EPS de vuelo se mantiene en control de carga basado en **MPPT**.

### 8.5 Reglas energéticas de firmware
- Eclipse en SAFE por defecto.  
- Downlink habilitado sólo con energía y geometría favorables.  
- Escritura intensiva en microSD preferentemente en sol.

---

## 9) Software de vuelo (lineamientos mínimos)

- Arranque seguro y determinista con watchdog HW activo.  
- Tolerancia explícita a reset y brownout.  
- Scheduler por ventanas orbitales y estado de energía.  
- Persistencia de logs críticos en NOR y bulk en microSD.  
- Telemetría de housekeeping, RF y energía como insumo primario de operación.

---

## 10) Plan de verificación y validación (V&V)

### 10.1 Fase 0 — banco
- Medición real de corrientes/potencias por subsistema.  
- Pruebas de brownout/reset.  
- Pruebas de storage y robustez de logs.

### 10.2 Fase 1 — campo
- Validación de enlaces terrestres y cadena de decodificación.  
- Simulación de ventanas de pasada y operación por modos.

### 10.3 Fase 2 — pseudo-orbital (recomendado)
- Ensayos de geometría desfavorable y ventanas cortas.  
- Validación de recuperación de transferencia y continuidad de telemetría.

### 10.4 Fase 3 — órbita
- Arranque conservador (beacon/housekeeping).  
- Activación progresiva de LoRa RX, science y dump según salud energética.

---

## 11) Riesgos consolidados y mitigaciones

| Riesgo | Impacto | Mitigación consolidada |
|---|---|---|
| Regulatorio/frecuencias | Alto | Mantener LoRa RX-only en órbita, gestionar coordinación/licencias del downlink UHF y operación de estación |
| Déficit energético | Alto | SAFE dominante, targets EPS con margen, gobernanza por estados energéticos, validación en banco |
| EMI/ruido interno | Medio-Alto | Separación de rails, layout con aislamiento RF y apagado de cargas conflictivas en downlink |
| Fallos por reset/brownout | Alto | Watchdog HW, boot a SAFE, logs idempotentes, pruebas agresivas de robustez |
| Complejidad de integración | Medio | ICD explícito, arquitectura modular por boards, V&V por fases |
| Science Pack simplificado (sin HV de radiación) | Bajo | Reducción de carga científica aceptada en MVP; sensor de radiación puede incorporarse en versión futura |

---

## 12) Pendientes técnicos (TBD explícitos)

1. Potencia eléctrica real del UHF TX según módulo/PA final medido.  
2. Consumo real de Science Board sin HV (sensores I2C y duty-cycles operativos).  
3. Potencia solar real por cara y condiciones térmicas (BOL/EOL).  
4. Dimensionamiento final de batería tras ensayos de banco y perfil orbital definitivo.

---

## 13) Estado final v2.1

- Documento consolidado y coherente para continuar ingeniería de detalle.  
- Sin cambios de decisión técnica respecto al baseline v1.4 + anexos.  
- Sustituye consolidado por transcripción, manteniendo contenido técnico heredado en formato de documento MVP.



## 14) Addendum software de banco (RF 433)

- El banco de telemetría 433 MHz en `05_Software/embedded` extiende la trama con quaternion (`q0..q3`) calculado por Madgwick IMU (sin magnetómetro).
- La orientación en yaw presenta deriva esperada; el banco se mantiene como entorno de laboratorio para validar pipeline de telemetría y visualización.
- El dashboard de estación terrena consume el quaternion directo para visualización 3D y conserva compatibilidad con formato CSV legacy de 8 campos.
- Se añadió calibración de bias de giroscopio en TX y zeroing visual en dashboard para alinear orientación percibida durante pruebas de banco con GY-521 (MPU6050).
- Referencias: `docs/TELEMETRY_433_README.md`, `05_Software/GroundTelemetryDashboard/docs/README.md`, `08_Decisions/ADR-20260212-quaternion-telemetry-dashboard-theme.md`.
- El banco 433 MHz valida exclusivamente el pipeline de software (firmware → CSV → dashboard); no es representativo del enlace RF orbital. El próximo banco de RF representativo usará el módulo transceptor seleccionado para vuelo (TBD).

---

## 15) Addendum EPS Bench1 1S (COTS→Flight-Like)

**Fecha de revisión:** 2026-02-18.

- Se formaliza el banco `EPS_Bench1_1S` como plataforma de validación funcional (no vuelo) para: carga solar, protección de batería, generación de `+5V` y `+3V3`, separación de buses y preparación de telemetría.
- Política permanente: módulos COTS económicos/disponibles para banco, con mapeo obligatorio a IC equivalente y topología de PCB custom en la fase de migración.
- Regla de protección BMS en banco 1S: cargador y cargas conectados al lado protegido `P+/P−`; `B+/B−` quedan reservados para conexión directa de celda.
- Se explicitan limitaciones del banco (sin MPPT real, sin redundancia, sin telemetría integrada aún, no diseño espacial).
- Roadmap EPS actualizado: `EPS_Bench1_1S` → `EPS_Flight_Like` → `EPS_Flight`.

Referencias cruzadas:
- `docs/EPS/EPS_Bench1_1S.md`.
- `docs/EPS/BOM_EPS_Bench1_1S.md`.
- `08_Decisions/ADR-20260218-eps-bench1s-cots-to-custom-flight-pcb.md`.
- `06_Costs/eps_bench1_1s_cost_model.md`.
- `07_Risk/eps_bench1_1s_risks.md`.
