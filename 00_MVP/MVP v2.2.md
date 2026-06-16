# Documento Técnico — MVP v2.2 (Consolidado técnico + baseline de misión)

## AUSTRALIS-1 - Experimental Autonomic Flight AI-Assisted CubeSat

### AI Payload + LoRa Uplink RX-Only + UHF Downlink + Science Pack + GNSS-A

**Estado:** consolidado vigente para ingenieria de sistema (alineado con ADRs `Accepted` vigentes).
**Alcance:** integracion coherente de `MVP v1`, `v1.1`, `v1.3`, `v1.4` y anexos de `Power Budget`, `EPS Sizing` e `ICD/Block Diagram`.

---

## 1) Objetivo del MVP y criterio de exito

### 1.1 Objetivo principal
Poner un payload de inteligencia artificial (IA) en orbita LEO, operarlo como asistente de vuelo autonomo bajo supervision deterministica, y recolectar datos de desempeno del modelo para entrenar versiones futuras de IA para CubeSats.

Objetivos secundarios vigentes:
- Validar la cadena end-to-end IoT: nodo LoRa (Buenos Aires) -> satelite (RX) -> estacion terrena (UHF) -> backend.
- Demostrar store-and-forward por pasadas LEO.
- Operar el Science Pack MVP (UV, ALS, magnetometro, temperatura).
- Mantener `PHOTO_DEMO` como payload opcional, no critico y best-effort.

### 1.2 Criterio de exito minimo (obligatorio)
1. **[PRIMARIO]** El payload IA (CM5 + SmolLM2-360M-Instruct INT4) completa al menos **5 ciclos de inferencia** en orbita con propuestas validadas por el Runtime Safety Supervisor y logging completo descargado a tierra.
2. **[PRIMARIO]** Se recolectan y descargan al menos **100 registros `AI_BEHAVIOR_LOG`** con datos validos (`timestamp`, `model_version`, `prompt_version`, `decision_id`, `recommended_action`, `confidence`, `supervisor_result`, `MISSION_MODE`, `EPS_STATE`).
3. **[PRIMARIO]** Al menos **1 prompt versionado** es recibido por uplink, aplicado por el `PromptStore` y utilizado en una inferencia registrada.
4. **[SECUNDARIO]** Se reciben en orbita al menos **10 paquetes LoRa** originados en Buenos Aires y se descargan por UHF con `RSSI`, `SNR`, `CFO`, `timestamp` y `CRC`.
5. Evidencia reproducible con correlacion a ventanas de pasada orbital.

### 1.3 Criterio de exito extendido (MVP+)
- Operacion del payload IA estable durante **>=30 dias**.
- Recoleccion y descarga de **>=1 000 registros `AI_BEHAVIOR_LOG`**.
- Operacion y comparacion en orbita de **>=3 versiones de prompt**.
- Analisis post-vuelo suficiente para generar dataset util para fine-tuning.
- **>=70%** de paquetes LoRa validos por pasada en configuracion robusta.
- Telemetria historica y trending operativo.

---

## 2) Criterios de consolidación y precedencia

- Se preserva toda información no contradictoria de versiones previas.
- Ante conflicto, prevalecen decisiones formalizadas en ADR `Accepted`.
- El baseline técnico vigente queda fijado por **MVP v2.2 + ADRs Accepted en `08_Decisions/`**.

### 2.1 Decisiones bloqueadas
- **Form factor:** 1.5U (100 × 100 × 150 mm).
- **CONOPS:** store & forward por ventanas orbitales.
- **Comunicaciones:** LoRa en órbita como **RX-only** (sin TX ISM desde satélite en MVP).
- **Downlink principal:** UHF 435 MHz con tasa robusta (baseline 1k2).
- **Arquitectura de energía:** EPS con rails medidos, power-gating y lógica de energía por modos.
- **Topología de batería de vuelo:** 2S (dos celdas Li-ion en serie, 7.4 V nominal) con referencia actual **2S1P, 18650 de 3.0 Ah (~22 Wh nominal)**; `2S2P (~44 Wh)` queda como ruta de mitigación TBD tras Gate IA-2.
- **Modulación downlink UHF:** FSK 1 200 bps.
- **Science Pack MVP:** UV, ALS/visible, magnetómetro 3 ejes, temperatura multipunto. **Geiger HV no incluido en MVP.**
- **UHF TX power RF:** 500 mW objetivo (derivado de link budget preliminar LEO 550 km; válido también para 600 km de diseño actual).
- **Órbita de diseño:** SSO ~98°, 600 km, LTAN 10:00h, eclipse ~34% (ADR-20260320-orbit-attitude-solar-layout-baseline).
- **Actitud nominal:** 10×10 nadir (+Z Tierra, +X ram).
- **Layout solar:** body-mounted +Y/±X/−Z, 484 cm² activa; radiador −Y; sin desplegables.

---

## 3) Concepto de misión (CONOPS)

### 3.1 Modo de servicio
Servicio no continuo: operación por pasadas LEO sobre zona de interés, con almacenamiento a bordo y descarga diferida a estación terrena.

### 3.2 Modelo operativo canónico (actualizado 2026-03-14)

El sistema implementa un modelo de modos operativos único:

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

1. **MISSION_MODE = SAFE** (modo por defecto post-reset y en eclipse)
   - Prioriza supervivencia, housekeeping y beacon mínimo.
   - Downlink: solo `HOUSEKEEPING` y `COMMAND_ACK`.

2. **MISSION_MODE = NOMINAL** (operación regular)
   - Actividades científicas ejecutadas como actividad dentro de este modo.
   - LoRa RX activo en ventanas de pasada.
   - Payload IA permitido solo en fase de sol y `EPS_STATE >= NOMINAL`.
   - Downlink: colas con prioridad estricta + best-effort con cuotas.

3. **MISSION_MODE = DOWNLINK_WINDOW** (ventana de descarga)
   - Prioriza dump de datos con UHF TX/RX y control de energía.
   - Mantiene prioridad estricta HOUSEKEEPING/COMMAND_ACK.
   - IA OFF por defecto.

**Reglas de degradación energética:**
- `EPS_STATE = CRIT` → degrada automáticamente a `MISSION_MODE = SAFE` sin excepción.
- `EPS_STATE = LOW` → `SAFE` por defecto; `NOMINAL` solo para housekeeping esencial explícitamente permitido.
- `EPS_STATE = NOMINAL` → operación regular.
- `EPS_STATE = HIGH` → margen amplio para downlink extendido y ventana IA ampliada si condiciones lo permiten.

> Nota histórica: versiones anteriores (MVP v1 a v2.1) denominaban el segundo modo operativo "SCIENCE MODE". Esa nomenclatura queda **supersedada** por `MISSION_MODE = NOMINAL`. La actividad científica no es un modo independiente sino una actividad condicional dentro de NOMINAL. El presupuesto de potencia en `03_Power/Power Budget.md` mantiene la columna `duty_sci` por compatibilidad de cálculo histórico.

### 3.3 Reglas operativas clave
- Boot determinista siempre a SAFE.
- GNSS es best-effort y nunca bloquea operación.
- En eclipse, baseline operativo conservador (SAFE por defecto).
- Dump y actividades de alto consumo condicionadas a estado energético.

---

## 4) Órbita objetivo y operación

### Órbita de diseño (actualizado 2026-03-20, ADR-20260320-orbit-attitude-solar-layout-baseline)
- **Tipo:** SSO (Sun-Synchronous Orbit)
- **Inclinación:** ~98° (rango aceptable 97.6°–98.8°)
- **Altitud de diseño:** **600 km** (rango aceptable 550–650 km)
- **LTAN:** **10:00h** preferido (simétrico con 14:00h)
- **Eclipse nominal:** ~34%
- Fuente: barrido 400 candidatos, simulador AUSTRALIS v9.2 auditado

### Layout de caras y actitud nominal (ADR-20260320-orbit-attitude-solar-layout-baseline)
- Actitud: **10×10 nadir** (+Z Tierra, +X ram)
- Paneles solares body-mounted: **+Y, ±X, −Z** (484 cm² activa, packing 88%)
- Cara radiadora: **−Y** (LTAN 10h, antisolar), 150 cm²
- Recubrimiento radiador: AZ-93 (preferido) o Al anodizado blanco (fallback)
- Cara nadir +Z: libre para antenas UHF, sensores
- Paneles desplegables: **no requeridos** para baseline
- Celdas: 7 celdas IBC/Maxeon baseline (TBD familia final)

### Diseño térmico baseline (ADR-20260320, actualizado con barrido anual 8760h)
- Radiador −Y (antisolar): α_solar ≤ 0.20, ε_IR ≥ 0.88 (AZ-93 o Al anodizado blanco)
- CM5 acoplado a pared interior −Y por pad térmico ~1 mm (G estimado ≈ 1.5 W/K)
- Tcm5 promedio anual (LTAN 9.5h, 650 km): 43.1°C (límite 80°C) — margen 37°C
- Tbat promedio anual (LTAN 9.5h, 650 km): 17.5°C (límite −10°C) — margen 28°C
- Peor caso global anual: Tcm5 59.2°C (margen 21°C), Tbat 8.5°C (margen 18°C)
- Heater de batería: **no requerido** (margen ≥ 18°C en peor caso)
- **TBD:** validar ΔT CM5-radiador en banco; verificar G real ≥ 0.60 W/K

### 4.1 Supuesto de ingeniería para presupuestos
Para dimensionamiento preliminar de energía se usa:
- Período orbital: ~96 min (600 km SSO).
- Eclipse nominal: ~34% (~33 min por órbita de ~96 min).

Este perfil es de diseño y debe recalibrarse con beta-angle estacional (ver RSK-ORB-01).

---

## 5) Arquitectura del sistema por segmentos

### 5.1 Segmento usuario (nodos IoT)
- Banda de operación en tierra: 915–928 MHz (configuración regional equivalente).
- Potencia típica de módulo LoRa (sin amplificación extra en MVP).
- Antena simple eficiente (¼ onda o dipolo).
- Tramas cortas (payload breve) y transmisión sólo durante ventanas estimadas de pasada.

### 5.2 Segmento espacial (satélite 1.5U)
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
- LoRa PHY con configuración priorizando **robustez y sensibilidad** sobre throughput.
- Operación por ventanas de pasada para concentrar margen geométrico (elevación alta).
- Acceso múltiple: **modo B2 slotted (pass-aware)** para reducir colisiones con nodos típicos.
- Los nodos calculan pasadas offline con TLE+SGP4 y usan RTC disciplinado por GNSS (sin asumir NTP).
- Receptor orbital objetivo: **LoRa concentrator** (multi‑canal/multi‑SF) para aumentar probabilidad de demodulación y logging de métricas.

Referencias:
- `04_Communications/uplink_lora_slotted_protocol.md`
- `05_Software/node_uplink_scheduler_pass_prediction.md`
- `08_Decisions/ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx.md`

### 7.2 Downlink satélite→tierra
- Enlace UHF robusto (baseline 435 MHz, ~1200 bps), con tramas cortas, CRC y numeración.
- Reanudación de transferencia para tolerar cortes por geometría/pérdida de enlace.

### 7.3 Tipos de tramas minimas
- **BEACON**
- **HOUSEKEEPING**
- **COMMAND_ACK**
- **AI_BEHAVIOR_LOG**
- **LORA_LOG**
- **SCIENCE_SUMMARY**
- **ACK/NACK**

Todas las tramas se manejan con integridad y secuencia para idempotencia operativa.
## 8) Presupuesto de potencia y dimensionamiento EPS

Ver política COTS-to-Flight en `03_Power/EPS Sizing.md` y `03_Power/Power Budget.md`.

### 8.1 Filosofía de diseño energético
- SAFE dominante para supervivencia sostenida.
- SCIENCE y DOWNLINK habilitados por estado de energía (SOC/VBAT/temperatura).
- Valores numéricos preliminares sujetos a validación en banco.

### 8.2 Consumos promedio de referencia por modo
- **SAFE avg:** ~0.143 W (objetivo ≤0.20 W).
- **SCIENCE avg:** ~0.379 W (objetivo ≤0.5 W).
- **DOWNLINK window avg:** ~1.14 W durante ventana.

### 8.3 Energía por órbita (referencia)
- Caso típico recomendado (SAFE + ventana downlink): **~0.381 Wh/orbita**.
- Caso SCI en sol + SAFE en eclipse: **~0.451 Wh/orbita**.
- Corrección 2026-03-14: el valor previo de **0.371 Wh/orbita** provenía de un `P_SCI` desincronizado (**0.299 W** vs **0.379 W**).

### 8.4 Targets EPS bloqueados
- Objetivo de potencia neta disponible en sol para el escenario **sin IA activa**: **≥1.2 W**.
- Con payload IA activo, el target solar queda **TBD** hasta medir consumo real del CM5 y cerrar duty-cycle orbital.
- Batería nominal de diseño recomendada: **~22 Wh nominal** con referencia **2S1P, 18650 de 3.0 Ah**.
- Ruta de mitigación abierta: **2S2P (~44 Wh)** si el power budget con IA lo requiere.
- Capacidad útil asegurada objetivo: **≥3 Wh**.
- EPS preparado para picos eléctricos de **~3 W** sin IA activa; cierre con IA pendiente por `CONF-01`.
- MPPT recomendado para márgenes de misión en 1.5U.

### Validación por simulador v9.2/v9.3 (2026-03-21, actualizado con barrido anual)
- **Barrido 24h (v9.2):** ~72 Wh/día, ~4.5 Wh/órbita, margen 3.4×. Base de decisiones iniciales.
- **Barrido 6 meses (v9.2, 4320h):** captura variación estacional de β. Confirma sweet spot y energía.
- **Barrido anual (v9.3, 8760h, 6 radiadores por candidato):** ~76 Wh/día, ~4.76 Wh/órbita, margen **3.6×**. Fuente definitiva.
- Consumo total con AI payload (20% duty): ~1.34 Wh/órbita.
- Convergencia: los tres barridos (24h, 6m, 12m) coinciden en margen 3.4–3.6× y en la selección de órbita, actitud, paneles y radiador.
- **TBD:** validar con η real de celda y consumo real CM5 en Gate IA-2.

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
- Activacion progresiva de LoRa RX, science, payload IA y dump segun salud energetica y resultados de banco.

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

## 13) Estado final v2.2

- Documento consolidado y coherente para continuar ingenieria de detalle.
- Baseline actualizado al corte 2026-03-14 con ADRs `Accepted` integradas hasta `ADR-20260314-mission-redef-ai-primary.md` y `ADR-20260314-eps-state-4-levels.md`.
- El payload IA queda incorporado como objetivo cientifico primario de mision; la cadena IoT store-and-forward permanece como objetivo secundario.
- Sustituye consolidado por transcripcion, manteniendo contenido tecnico heredado en formato de documento MVP.
## 14) Addendum software de banco (RF 433)

- El banco de telemetría 433 MHz en `05_Software/embedded` extiende la trama con quaternion (`q0..q3`) calculado por Madgwick IMU (sin magnetómetro).
- La orientación en yaw presenta deriva esperada; el banco se mantiene como entorno de laboratorio para validar pipeline de telemetría y visualización.
- El dashboard de estación terrena consume el quaternion directo para visualización 3D y conserva compatibilidad con formato CSV legacy de 8 campos.
- Se añadió calibración de bias de giroscopio en TX y zeroing visual en dashboard para alinear orientación percibida durante pruebas de banco con GY-521 (MPU6050).
- Referencias: `docs/TELEMETRY_433_README.md`, `05_Software/GroundTelemetryDashboard/docs/README.md`, `08_Decisions/ADR-20260212-quaternion-telemetry-dashboard-theme.md`.
- El banco 433 MHz valida exclusivamente el pipeline de software (firmware → CSV → dashboard); no es representativo del enlace RF orbital. El próximo banco de RF representativo usará el módulo transceptor seleccionado para vuelo (TBD).

---

## 15) Addendum EPS Bench1 1S (COTS→Flight-Like)

**Fecha de revision:** 2026-04-03.

- Se formaliza `EPS_Bench1_1S` como plataforma de validación funcional (no vuelo) para: carga solar, protección de batería, generación de `+5V` y `+3V3`, separación de buses, preparación de telemetría y cierre de Gate IA-2 en banco.
- `EPS_Bench1_1S` agrega un FPM bench y una rama IA **bench-only**: `J_AI_PWR` -> `5V_AI_EXT` -> `F_AI` -> `SW_AI` -> `5V_AI_SW`, con carrier board COTS externa para el CM5 real.
- La inyección externa de 5V existe para validar secuenciamiento, FPM, logging, heartbeat, boot, kill/reset, consumo y térmica básica del CM5 real en banco.
- `JP1` se redefine como header de control/sense/telemetría (2x12); la potencia principal del rail IA **no** pasa por `JP1`.
- Política permanente: módulos COTS económicos/disponibles para banco, con mapeo obligatorio a IC equivalente y topología de PCB custom en la fase de migración.
- Regla de protección BMS en banco 1S: cargador y cargas conectados al lado protegido `P+/P−`; `B+/B−` quedan reservados para conexión directa de celda.
- Se explicitan limitaciones del banco (sin MPPT real, sin redundancia, no diseño espacial y sin validar el rail IA de vuelo 2S+MPPT).
- Se reafirma la separación canónica: `EPS_Bench1_1S` -> `EPS_Flight_Like_2S_MPPT` -> `EPS_Flight_2S_MPPT`.

### Referencias cruzadas:
- `03_Power/EPS_Bench1_1S.md`.
- `03_Power/EPS_PCB/EPS_Bench1S/eps_bench_mods.md`.
- `docs/EPS/EPS_Bench1_1S.md` (historial/soporte).
- `docs/EPS/BOM_EPS_Bench1_1S.md` (historial BOM).
- `08_Decisions/ADR-20260218-eps-bench1s-cots-to-custom-flight-pcb.md`.
- `06_Costs/eps_bench1_1s_cost_model.md`.
- `07_Risk/eps_bench1_1s_risks.md`.


---

## 16) Framework permanente de arbitraje, potencia y salud

### 16.1 Downlink Manager (OBC)
Arquitectura permanente de colas por tipo de tráfico:
- `HOUSEKEEPING`
- `COMMAND_ACK`
- `AI_BEHAVIOR_LOG`
- `LORA_LOG`
- `SCIENCE`
- `OPTIONAL_PAYLOAD`

Política por modo:
- **SAFE:** solo `HOUSEKEEPING` + `COMMAND_ACK`; resto en retención.
- **NOMINAL:** `HOUSEKEEPING`/`COMMAND_ACK` con prioridad estricta; `AI_BEHAVIOR_LOG`, `LORA_LOG` y `SCIENCE` best-effort con cuotas.
- **DOWNLINK_WINDOW:** mantiene prioridad estricta de `HOUSEKEEPING`/`COMMAND_ACK` y amplía cuota para colas best-effort.

Reglas permanentes:
- Prioridad absoluta: `HOUSEKEEPING` y `COMMAND_ACK`.
- `AI_BEHAVIOR_LOG` es la cola best-effort de mayor prioridad científica.
- Tráfico no-crítico (`AI_BEHAVIOR_LOG`, `LORA_LOG`, `SCIENCE`, y colas opcionales) bajo cuota por pasada.
- `SCIENCE` y payloads opcionales nunca bloquean housekeeping o comandos.

### 16.2 Fault/Power Manager (OBC + EPS)
- Power-gating selectivo por subsistema (`EN_x`).
- Health monitoring continuo por señal mínima:
  - `PGOOD_x`
  - `FAULT_x`
  - `HB_x` (heartbeat)
  - contadores de resets/faults y último motivo
- Lógica de aislamiento:
  1) detección de anomalía,
  2) apagado inmediato del subsistema afectado,
  3) reintentos acotados,
  4) lockout hasta uplink explícito o timeout de recuperación.

### 16.3 Uplink mínimo de comandos (control manual)
Conjunto mínimo obligatorio:
- `SET_MODE`
- `POWER_SET`
- `DL_SELECT`
- `DL_SET_LIMITS`
- `REQUEST_STATUS`
- `ABORT`

### 16.4 Reglas de seguridad
- SAFE primero ante falla sistémica o energía degradada.
- Subsistemas no críticos off-by-default al boot hasta habilitación explícita.
- Downlink y operaciones de payload condicionadas a salud + energía.

<!-- FEATURE:PHOTO_DEMO START -->

## 17) [PHOTO_DEMO] Payload DEMO encapsulado (opcional en MVP 2.2)

### 17.0 [PHOTO_DEMO] Mapeo en Downlink Manager
Cuando este feature está habilitado, `OPTIONAL_PAYLOAD` se instancia como cola `PHOTO`.

### 17.1 [PHOTO_DEMO] Objetivo
Agregar una capacidad DEMO de captura fotográfica de alto riesgo / bajo impacto, encapsulada y desactivable sin afectar el resto del bus.

### 17.2 [PHOTO_DEMO] Política operativa
- Off-by-default al boot.
- Solo best-effort bajo Downlink Manager.
- Cuota configurable por pasada (`DL_SET_LIMITS`) y sin prioridad sobre housekeeping/comandos.

### 17.3 [PHOTO_DEMO] Flujo de transferencia
1. Publicación de catálogo con 3–4 thumbnails comprimidos.
2. Espera de selección por uplink (`DL_SELECT`).
3. Transferencia de imagen elegida por chunks reanudables en múltiples pasadas con NACK/bitmap o lista de faltantes.

### 17.4 [PHOTO_DEMO] Interlocks y aislamiento
- Control por `POWER_SET` dedicado al subsistema de cámara.
- Aislamiento por Fault/Power Manager ante `FAULT_x`, pérdida de `HB_x` o sobreconsumo estimado.
- Lockout tras reintentos fallidos hasta comando manual o timeout.

### 17.5 [PHOTO_DEMO] Riesgo aceptado
Este payload puede fallar y debe poder desactivarse completamente sin afectar telemetría, comandos ni cadena principal de misión.

### 17.6 [PHOTO_DEMO] Estado y freeze (2026-03-13)

`PHOTO_DEMO` queda **congelado** como:
- **Opcional** y **no crítico**.
- **OFF por defecto** al boot (off-by-default hardware y software).
- **Best-effort** exclusivamente bajo cola `OPTIONAL_PAYLOAD` del Downlink Manager.
- **Fuera del criterio mínimo de éxito del MVP**.
- Su falla **no degrada** la cadena principal (housekeeping, comandos, LORA_LOG).
- No desplaza housekeeping ni comandos.
- No bloquea baseline.

Referencia ADR: `08_Decisions/ADR-20260313-photo-demo-opcional-no-critico.md`

<!-- FEATURE:PHOTO_DEMO END -->

---

## 18) Addendum de sincronizacion documental (2026-03-05)

### 18.1 Objetivo del addendum
Sincronizar el baseline `MVP v2.2` con los ultimos avances documentales de subsistemas, sin introducir cambios de arquitectura que no esten respaldados por ADR `Accepted`.

### 18.2 Estado de decisiones al corte
- Al corte de la primera version de este addendum (2026-03-05), no existian ADR nuevas en estado `Accepted` posteriores a 2026-02-20.
- Las ADRs incorporadas con fecha 2026-03-13 se documentan en `§18.6`.
- Las ADRs posteriores del 2026-03-14 se integran en `§19` y en la revision 2026-03-14 del baseline.
### 18.3 Actualizaciones de subsistemas incorporadas como contexto
1. EPS:
   - `03_Power/EPS_Bench1_1S.md` (rev 2026-02-27) amplia netlist, power-gating, telemetria y plan de pruebas T1-T10.
   - La ruta de migracion a 2S se mantiene en `03_Power/EPS_PCB/EPS_Bench2S_FlightLike/`.
2. COMMS:
   - `04_Communications/RF_ANALISYS_OPENLST.md` (2026-03-03) incorpora evaluacion de OpenLST como candidato TTC UHF.
   - Esta evaluacion no reemplaza la decision vigente de UHF 435 FSK 1k2 ni cierra aun seleccion de modulo.
3. Software/OPS:
   - Se mantiene el marco P1 slotted, scheduler de pasadas y mecanismo de actualizacion TLE como parte del plan de validacion.
4. Riesgos y costos:
   - Se conserva el estado ROM y matrices de riesgo activas; persisten `TBD` de costos y cierre experimental de uplink.

### 18.4 Regla de coherencia para documentos de trabajo
Documentos en estado `Draft`, `Propuesta` o `Preliminar` aportan direccion tecnica, pero no sobreescriben decisiones ya bloqueadas por ADR `Accepted` hasta que exista ADR nueva.

### 18.5 Pendientes de cierre del MVP
1. Selección final de transceptor/módulo UHF y medición real de eficiencia PA.
2. Cierre de factibilidad uplink LoRa con nodos típicos bajo CFO/Doppler.
3. Completar cuantificación del modelo de costos ROM.
4. `PHOTO_DEMO` resuelto: **Accepted** como opcional no crítico (ver ADR-20260313).

### 18.6 Sincronización documental (2026-03-13)

Cambios incorporados en esta revisión:
- Modelo operativo unificado `MISSION_MODE / EPS_STATE` (sección 3.2); "SCIENCE MODE" como nomenclatura canónica supersedada.
- `PHOTO_DEMO` congelado como `Accepted` opcional no crítico (sección 17.6).
- Referencias cruzadas a nuevos artefactos: `01_Mission/compliance_matrix.md`, `01_Mission/validation_plan_and_stage_gates.md`, `06_Costs/BOM_master.csv`, `05_Software/ground_data_architecture.md`.
- 5 nuevas ADRs en `08_Decisions/` alineadas con esta revisión.
- Separación explícita EPS: `EPS_Bench1_1S` / `EPS_Flight_Like_2S_MPPT` / `EPS_Flight_2S_MPPT`.

---

## 19) Payload IA como objetivo primario de misión (2026-03-14)

### 19.1 Decisión

El payload IA (Inteligencia Artificial) queda incorporado al baseline como **payload científico primario de misión** por:
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md`

La misión pasa a denominarse:
**AUSTRALIS-1 — Experimental Autonomic Flight AI-Assisted CubeSat**

### 19.2 Rol y autoridad

- El payload IA es el **objetivo científico primario** del MVP, pero **no** es mission-critical para la supervivencia del bus.
- El **OBC (On-Board Computer) determinístico** conserva la autoridad final de vuelo.
- La IA genera únicamente **recomendaciones/propuestas**; el OBC las valida o rechaza a través de un **Runtime Safety Supervisor** determinístico.
- Debe existir **kill switch** software y hardware del payload IA.
- Si el payload IA falla o se apaga, el satélite debe seguir operando en modo determinístico, aunque el criterio primario de éxito quede afectado.

### 19.3 Hardware baseline

| Rol | Descripción |
|---|---|
| Familia | Raspberry Pi CM5 (Compute Module 5) |
| Bench candidate | CM5 8 GB |
| Flight-like candidate inicial | CM5 4 GB + eMMC |
| Hardware de vuelo calificado | TBD — no declarado |

No se fija SKU (Stock Keeping Unit) de marketplace como requisito normativo.

### 19.4 Modelo baseline experimental

- **SmolLM2-360M-Instruct**, cuantizado a **INT4**.
- Baseline experimental — no declarado modelo final de vuelo hasta Gate IA-2.
- `Qwen2.5-0.5B-Instruct`: comparative bench candidate, no baseline de misión.

### 19.5 Filosofía operativa

- Payload IA **power-gated** en rail dedicado.
- IA `OFF` en `MISSION_MODE = SAFE`.
- IA `OFF` en eclipse.
- IA `OFF` con `EPS_STATE = CRIT` o `LOW`.
- IA `OFF` en `MISSION_MODE = DOWNLINK_WINDOW` por defecto.
- IA `ON` solo en ventanas experimentales en fase de sol, `MISSION_MODE = NOMINAL` y `EPS_STATE >= NOMINAL`.
- `EPS_STATE = HIGH` puede habilitar ventanas IA ampliadas si las condiciones lo permiten.
- Política por defecto: **mutua exclusión operacional IA ↔ TX UHF**.

### 19.6 Prompting en órbita

- El sistema soporta uplink de **system prompts / policy prompts versionados**.
- El OBC puede cargar el prompt activo, revertir al prompt seguro y registrar qué prompt estaba activo en cada decisión.

### 19.7 Logging científico

El **Behavior Logger** del payload IA registra por evento: `timestamp`, `model_version`, `prompt_version`, `decision_id`, `recommended_action`, `confidence`, `supervisor_result` (`accepted`/`rejected`/`clipped`), `MISSION_MODE`, `EPS_STATE`, `state_snapshot_hash`.

Estos datos forman el dataset científico primario de la misión.

### 19.8 Downlink Manager — cola AI_BEHAVIOR_LOG

El Downlink Manager incorpora la cola `AI_BEHAVIOR_LOG` para el payload IA con el siguiente orden:

| Cola | Prioridad |
|---|---|
| `HOUSEKEEPING` | Estricta (máxima) |
| `COMMAND_ACK` | Estricta |
| `AI_BEHAVIOR_LOG` | Best-effort (mayor prioridad científica) |
| `LORA_LOG` | Best-effort |
| `SCIENCE` | Best-effort |
| `OPTIONAL_PAYLOAD` | Best-effort (mínima) |

### 19.9 Presupuesto energético (sin cerrar)

- Esta decisión **no cierra el power budget del payload IA**.
- Objetivo arquitectónico de pico transitorio: **6–7 W** (hipótesis de análisis, sin medir).
- Operación continua **no asumida**.
- `CONF-01` permanece **abierto**.
- Duración operativa por órbita: **TBD**.
- El target solar con IA activa permanece **TBD** hasta Gate IA-2.

### 19.10 Objetivos científicos del payload IA

1. Ejecutar inferencias en órbita con supervisión determinística.
2. Registrar comportamiento del modelo para análisis y ajuste fino en tierra.
3. Validar prompting versionado en órbita.
4. Explorar priorización inteligente de downlink, telemetría e imágenes.

### 19.11 Documento técnico de referencia

`05_Software/ai_payload_architecture.md` — arquitectura detallada del payload IA (propósito, hardware, software, flujo OBC↔IA, supervisor, prompting, logging, estados, riesgos).

---

## 20) Actualización modelo baseline experimental del payload IA (2026-03-16)

### 20.1 Decisión

Durante la sesión 2026-03-16 se reabrió la selección del modelo baseline experimental del payload IA y se adoptó un nuevo baseline por razones técnicas, de licenciamiento y narrativa. La decisión está formalizada en:

`08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`

Esta ADR actualiza **exclusivamente** el §C (modelo baseline) de `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`. El resto de esa ADR (arquitectura, CM5, supervisor, operación, kill switch, logging) permanece vigente sin cambio.

### 20.2 Nuevo baseline funcional experimental

- **Modelo:** IBM Granite 350M fine-tuned mediante LoRA/QLoRA
- **Licencia:** Apache 2.0
- **Origen:** IBM Research
- **Estado:** baseline funcional validado en banco
- **SmolLM2-360M-Instruct INT4:** baseline histórico / superseded para esta función

### 20.3 Criterios de cambio de modelo

| Criterio | Detalle |
|---|---|
| Geopolítico | Descarte de modelos de origen chino (Qwen) |
| Licencia | Descarte de Llama (restricciones de uso ambiguas para payload satelital) |
| Técnico | Granite 350M Apache 2.0 con fine-tuning QLoRA operativo y evidencia de banco |
| Narrativa | Ecosistema occidental, limpio ante patrocinadores y launch providers |

### 20.4 Evidencia funcional de banco (resumen)

| Métrica | BASE | FINE_TUNED |
|---|---|---|
| `pass_rate_pct` (%) | 14.29 | **57.14** |
| `avg_score_ratio` | 0.3163 | **0.8313** |
| `avg_latency_s` (s) | 5.975 | 6.691 |
| `avg_gen_tok_s` (tok/s) | 35.74 | 19.92 |

El holdout funcional verificó comportamiento útil y no trivial en: SAFE fallback, RF fault isolation, regulatory refusal TX ISM, eclipse hold, textual image triage y policy prompt override.

### 20.5 Estado de validación

| Nivel | Estado |
|---|---|
| Baseline funcional de banco | ✅ Alcanzado |
| Validación en CM5 real | ❌ Pendiente — Gate IA-2 |
| Validación energética y térmica | ❌ Pendiente — Gate IA-2 |
| Modelo de vuelo final | ❌ No declarado |
| Flight-ready | ❌ No declarado |

`CONF-01` permanece **abierto**. El consumo real del CM5 con Granite fine-tuned no ha sido medido.

### 20.6 Pendientes abiertos tras la sesión 2026-03-16

1. Sourcing del CM5 bench candidate (CM5 8 GB) para Gate IA-2.
2. Medición de consumo y latencia del modelo Granite en CM5 real.
3. Validación térmica del CM5 en operación.
4. Integración física OBC ↔ CM5 con interfaz real.
5. Resolución de defectos residuales: `ai_payload_state` contextual, `policy override` total, normalización de `decision_id`.
6. Benchmark adicional con dataset expandido en próxima iteración de fine-tuning.

### 20.7 Criterio de éxito actualizado (sin cambio de fondo)

Los criterios de éxito de §1.2 no cambian: la misión sigue requiriendo ≥5 ciclos de inferencia en órbita, ≥100 registros `AI_BEHAVIOR_LOG` y ≥1 prompt versionado aplicado. El modelo que ejecutará esas inferencias es ahora Granite 350M fine-tuned (sujeto a validación en hardware real).

### 20.8 Referencias

- `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` (vigente excepto §C)
- `05_Software/ai_payload_architecture.md`
- `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`
