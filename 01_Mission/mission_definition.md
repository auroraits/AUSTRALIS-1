# Mission Definition — AUSTRALIS-1

**Revisión:** 2026-04-03
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md`, ADRs Accepted en `08_Decisions/`

## 1) Objetivo de misión

**AUSTRALIS-1 — Experimental Autonomic Flight AI-Assisted CubeSat**

Objetivo primario:
- Poner un payload de inteligencia artificial en órbita LEO, operarlo como asistente de vuelo autónomo bajo supervisión determinística y recolectar datos válidos para entrenar futuras versiones de IA para CubeSats.

Objetivos secundarios:
1. Validar una cadena orbital end-to-end real: nodo IoT (Buenos Aires, LoRa 915 MHz) → satélite (recepción en órbita) → estación terrena (downlink UHF 435 MHz) → backend con trazabilidad completa.
2. Validar store and forward por pasadas LEO.
3. Operar el Science Pack (UV, ALS/visible, magnetómetro 3 ejes, temperatura multipunto).
4. Mantener `PHOTO_DEMO` como feature opcional, no crítico y best-effort.

## 2) Criterio de éxito mínimo
1. El payload IA (CM5 + IBM Granite 350M fine-tuned, o el modelo baseline vigente según la ADR más reciente) completa **al menos 5 ciclos de inferencia** en órbita con propuestas validadas por el `RuntimeSafetySupervisor` y logging completo descargado a tierra.
2. Se recolectan y descargan **al menos 100 registros `AI_BEHAVIOR_LOG`** con datos válidos (`timestamp`, `model_version`, `prompt_version`, `decision_id`, `recommended_action`, `confidence`, `supervisor_result`, `MISSION_MODE`, `EPS_STATE`).
3. Al menos **1 prompt versionado** es recibido por uplink, aplicado por `PromptStore` y usado en inferencia con resultado registrado.
4. Como objetivo secundario, se reciben en órbita **al menos 10 paquetes LoRa** originados en Buenos Aires y se descargan a tierra por UHF con métricas (`RSSI`, `SNR`, `CFO`, `timestamp`, `CRC`).
5. Existe evidencia reproducible con correlación a ventanas de pasada orbital.

## 3) Criterio de éxito extendido (MVP+)
- Operación estable del payload IA durante **>=30 días**.
- **>=1 000 registros `AI_BEHAVIOR_LOG`** descargados.
- Al menos **3 versiones de prompt** operadas y comparadas en órbita.
- Dataset post-vuelo útil para análisis y fine-tuning.
- **>=70%** de paquetes LoRa válidos por pasada (configuración robusta).
- Telemetría histórica y trending operativo.

## 4) Parámetros orbitales de diseño
- Tipo: LEO circular.
- Altitud: 500-600 km.
- Inclinación: TBD (seleccionada según acceso de lanzamiento, habilitando pasadas sobre Buenos Aires — latitud -34.6).
- Período: ~95 min (600 km) a ~94 min (500 km).
- Duración de misión objetivo: >=30 días operativos.
- Para presupuesto EPS preliminar: supuesto de diseño 90 min con 60 min sol / 30 min eclipse (ver `03_Power/Power Budget.md`). `03_Power/EPS_DESIGN_RULES.md` es guía técnica draft, no normativa.

## 5) Segmento usuario
- Nodos IoT en tierra como objetivo secundario de misión.
- Uplink LoRa 915 MHz.
- Tramas cortas por ventanas de pasada.
- Clase objetivo de nodo: SX1262/SX1276, MCU clase ESP32-S3, +20–21 dBm, antena 0–2 dBi, sin PA externo.

## 6) Segmento espacial
- Plataforma 1.5U.
- EPS:
  - topología de vuelo 2S (bloqueada por ADR),
  - referencia actual 2S1P con 18650 de 3.0 Ah (~22 Wh nominal),
  - banco actual `EPS_Bench1_1S` extendido para Gate IA-2 con FPM bench + rail IA bench-only + inyección externa de 5V para CM5 real,
  - orientación de arquitectura: battery-bus backbone (VBAT) con rails derivados y control de power-gating.
- OBC STM32L4 con Downlink Manager + Fault/Power Manager + Runtime Safety Supervisor.
- **Payload IA experimental / primario** (familia CM5): payload científico primario de misión. El OBC conserva la autoridad final; el payload IA no es mission-critical para la supervivencia del bus.
- RF Board: LoRa RX 915 + UHF 435 para downlink/TTC.
- Science Board: UV, ALS/visible, magnetómetro 3 ejes, temperatura multipunto (sin etapa HV en MVP).
- GNSS-A para sincronización/telemetría best-effort.

## 7) Segmento terreno
- Estación Buenos Aires con Yagi UHF.
- LNA + SDR/radio.
- Dashboard .NET 8 para visualización y trazabilidad de telemetría.
- Backend para persistencia y correlación de `AI_BEHAVIOR_LOG`, `LORA_LOG` y housekeeping.

## 8) CONOPS resumen
- Estrategia store and forward.
- Operación por pasadas LEO.
- Modelo operativo canónico:
  - `MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW`
  - `EPS_STATE = CRIT | LOW | NOMINAL | HIGH`
- Reglas de seguridad operacional:
  - `SAFE` es el modo por defecto post-reset.
  - En eclipse se opera en `SAFE` por defecto.
  - Si `EPS_STATE = CRIT`, el sistema degrada a `MISSION_MODE = SAFE` sin excepción.
  - Si `EPS_STATE = LOW`, el sistema permanece en `SAFE` por defecto; `NOMINAL` solo para housekeeping esencial explícitamente permitido.
  - La actividad científica se ejecuta como actividad dentro de `MISSION_MODE = NOMINAL`; **no es un modo operativo independiente**.
  - El payload IA solo puede operar en fase de sol, `MISSION_MODE = NOMINAL` y `EPS_STATE >= NOMINAL`.
  - `AI_BEHAVIOR_LOG` es la cola best-effort de mayor prioridad científica en downlink.
- `SOLAR_ONLY` se mantiene como contingencia propuesta en evaluación (no requisito bloqueado de aceptación MVP).

> Nota histórica: la denominación "SCIENCE MODE" como tercer modo operativo apareció en versiones anteriores. Queda **supersedada** por el modelo canónico `MISSION_MODE = NOMINAL` con actividad científica como actividad interna.

## 9) Requisitos verificables mínimos

### La matriz canónica de requisitos vive en:
- `01_Mission/requirements_matrix.md`

### Los IDs `MIS-REQ-xx` se mantienen por compatibilidad con versiones previas, pero la fuente de verdad para verificación/estado es la matriz.

## 10) Lineamientos EPS (separación de capas)

### 10.0 Separación inequívoca bench / flight-like / flight

| Capa | Nombre | Propósito |
|---|---|---|
| Bench | `EPS_Bench1_1S` | Validación funcional COTS, 1S, extendida para Gate IA-2 con FPM bench + rail IA bench-only + CM5 real por inyección externa. **No hardware de vuelo.** |
| Flight-Like | `EPS_Flight_Like_2S_MPPT` | PCB custom KiCad, 2S + MPPT. No calificado de vuelo. |
| Flight | `EPS_Flight_2S_MPPT` | Hardware de vuelo definitivo. TBD. |

Referencia: `08_Decisions/ADR-20260313-eps-separacion-bench-flightlike-flight.md`

Lineamientos adicionales para misión:
- `EPS_Bench1_1S` extendido existe para cerrar Gate IA-2 en banco, no para redefinir la arquitectura EPS de vuelo.
- El CM5 real en banco usa carrier board COTS externa y `5V_AI_EXT` por `J_AI_PWR`.
- `JP1` queda como interfaz de control/sense/telemetría; la potencia principal del rail IA no pasa por `JP1`.
- La arquitectura de vuelo se mantiene en `EPS_Flight_Like_2S_MPPT` / `EPS_Flight_2S_MPPT` con topología 2S + MPPT.

## 11_EPS) Lineamientos EPS incorporados desde `EPS_DESIGN_RULES.md` (draft, no normativo)

### 11.1 Bloqueado por baseline/ADR
- Topología de batería de vuelo: **2S**.
- SAFE por defecto ante reset y ante degradación energética.
- Ningún cambio en estas decisiones se considera válido sin ADR `Accepted`.

### 11.2 En evaluación (no normativo aún)
- Arquitectura power: battery-bus backbone con dual-bus como opción (no adoptada en baseline).
- Rails críticos propuestos: `3V3_OBC` always-on + `RX_KEEPALIVE` dedicado.
- Política de robustez TX/PA propuesta: rail separado, `TX default OFF`, OCP + soft-start + reintentos controlados.
- Estrategia solar-only survival y política de heater de batería como opciones sujetas a cierre de power budget y validación térmica.
- Cierre del target solar con payload IA activo y eventual necesidad de `2S2P`.

### 11.3 Implicancia para misión
- Estos lineamientos orientan diseño y V&V del segmento espacial.
- Hasta no tener ADR nueva, prevalece la precedencia: ADR `Accepted` -> `00_MVP/MVP v2.2.md` -> `SYSTEM_BASELINE.md`.

<!-- FEATURE:PHOTO_DEMO START -->

## 12) [PHOTO_DEMO] Requisitos opcionales encapsulados (Accepted — opcional no crítico)

| ID | Requisito | Criterio de verificación | Subsistema |
|---|---|---|---|
| MIS-REQ-PH-01 | El payload [PHOTO_DEMO] shall iniciar OFF por defecto al boot. | Boot test + lectura de `EN_x` | FSW/EPS |
| MIS-REQ-PH-02 | El payload [PHOTO_DEMO] shall usar cuota best-effort por pasada sin desplazar housekeeping/comandos. | Test de arbitraje con colas saturadas | FSW/COMMS |
| MIS-REQ-PH-03 | El payload [PHOTO_DEMO] shall transferir imagen por chunks reanudables tras selección uplink. | Test de pérdida de paquetes + reanudación | FSW/COMMS |

<!-- FEATURE:PHOTO_DEMO END -->

<!-- FEATURE:AI_PAYLOAD START -->

## 13) [AI_PAYLOAD] Payload IA experimental (Accepted — 2026-03-14)

### 13.1 Objetivo científico del payload IA

El payload IA constituye el **objetivo científico primario de la misión**:

1. Operar inferencias en órbita bajo supervisión determinística.
2. Evaluar asistencia de modelos de lenguaje pequeños en operación satelital.
3. Registrar comportamiento del modelo IA para análisis y ajuste fino en tierra.
4. Explorar priorización inteligente de downlink, telemetría e imágenes.

### 13.2 Posición en la misión

- El payload IA es un **payload científico primario de misión**, pero **no** un subsistema mission-critical para la supervivencia del bus.
- Si el payload IA falla o se apaga, la plataforma y el CONOPS determinístico deben seguir operando.
- Esa falla impacta directamente el criterio de éxito primario del MVP.

### 13.3 Arquitectura de control

- El **OBC (On-Board Computer) determinístico** es la autoridad final de vuelo en todo momento.
- El payload IA genera **recomendaciones / propuestas**; el OBC las valida a través de un **Runtime Safety Supervisor** determinístico.
- Ninguna recomendación IA se ejecuta sin pasar por el supervisor.
- Debe existir **kill switch** software y hardware del payload IA.

### 13.4 Hardware baseline

| Rol | Descripción |
|---|---|
| Familia | Raspberry Pi CM5 (Compute Module 5) |
| Bench candidate | CM5 8 GB |
| Flight-like candidate inicial | CM5 4 GB + eMMC |
| Hardware de vuelo calificado | TBD |

### 13.5 Modelo baseline experimental

- **IBM Granite 350M fine-tuned (LoRA/QLoRA)** — baseline funcional validado en banco (2026-03-16). Licencia Apache 2.0. Origen IBM Research.
- Estado: baseline funcional de banco. No declarado modelo final de vuelo. No declarado flight-ready.
- SmolLM2-360M-Instruct INT4: baseline histórico / superseded para esta función.
- Referencia ADR: `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`.
- Cambio de modelo baseline shall documentarse mediante nueva ADR `Accepted`.
- Evidencia funcional de banco: pass_rate 14.29 % → 57.14 %; avg_score_ratio 0.3163 → 0.8313 (benchmark corrected BASE vs FINE_TUNED).
- Defectos residuales menores: `ai_payload_state` contextual, `policy override` total, `decision_id` normalización (no invalidan el baseline funcional).
- Bench candidate comparativo descartado: `Qwen2.5-0.5B-Instruct` (origen geopolítico); `Llama 3.2` (restricciones de licencia).

### 13.6 CONOPS del payload IA

- IA `OFF` en `MISSION_MODE = SAFE` (mandatorio).
- IA `OFF` en eclipse (mandatorio).
- IA `OFF` con `EPS_STATE = CRIT` o `LOW` (mandatorio).
- IA `OFF` durante `MISSION_MODE = DOWNLINK_WINDOW` (salvo experimento explícito documentado).
- IA `ON` solo en `MISSION_MODE = NOMINAL`, fase de sol y `EPS_STATE >= NOMINAL`.
- `EPS_STATE = HIGH` puede habilitar ventanas IA ampliadas si las condiciones térmicas y de energía lo permiten.
- Política por defecto: **mutua exclusión operacional IA ↔ TX UHF**.
- El payload IA nunca bloquea housekeeping ni comandos.

### 13.7 Prompting en órbita y logging

- El sistema soporta uplink de **system prompts / policy prompts versionados**.
- El **Behavior Logger** registra cada evento de inferencia con: timestamp, model_version, prompt_version, decision_id, recommended_action, confidence, supervisor_result, MISSION_MODE, EPS_STATE.
- Los logs forman el dataset científico primario de la misión.
- `AI_BEHAVIOR_LOG` es la cola best-effort de mayor prioridad dentro del Downlink Manager.

### 13.8 Requisitos IA

Ver `01_Mission/requirements_matrix.md` — sección 5 (requisitos IA-REQ-01 a IA-REQ-10) y requisitos primarios MIS-REQ-16 a MIS-REQ-18.

### 13.9 Referencia

`08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md` — baseline funcional de banco (modelo)
`08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` — arquitectura payload IA
`08_Decisions/ADR-20260314-mission-redef-ai-primary.md`
`05_Software/ai_payload_architecture.md`
`05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`

<!-- FEATURE:AI_PAYLOAD END -->

## 14) Referencias
- `00_MVP/MVP v2.2.md`
- `SYSTEM_BASELINE.md`
- `architecture.md`
- `AGENTS.md`
- `01_Mission/requirements_matrix.md`
- `01_Mission/compliance_matrix.md`
- `01_Mission/validation_plan_and_stage_gates.md`
- `03_Power/EPS_DESIGN_RULES.md` (draft, no normativo)
- `05_Software/ai_payload_architecture.md`
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md`
- `08_Decisions/ADR-20260314-eps-state-4-levels.md`
- `08_Decisions/ADR-20260313-gobierno-documental.md`
- `08_Decisions/ADR-20260313-photo-demo-opcional-no-critico.md`
- `08_Decisions/ADR-20260313-eps-separacion-bench-flightlike-flight.md`
- `08_Decisions/ADR-20260218-battery-topology-2s-flight.md`
- `08_Decisions/ADR-20260218-downlink-arbitration-and-subsystem-power-framework.md`
- `08_Decisions/ADR-20260218-uhf-link-budget-preliminary.md`
