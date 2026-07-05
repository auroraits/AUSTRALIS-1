# System Baseline — AUSTRALIS-1 (DIY Nanosat MVP)

**Revisión:** 2026-03-21
**Estado:** Baseline
**Trazabilidad:** ADR-20260320-orbit-attitude-solar-layout-baseline, ADR-20260320-thermal-design-radiator-cm5-coupling

Este documento resume el baseline canónico del sistema y separa lo **bloqueado** de lo que sigue **en evaluación**.

---

## 1) Fuente de verdad y precedencia

- Documento MVP consolidado: `00_MVP/MVP v2.2.md`
- Mapa/estado arquitectónico: `architecture.md`
- Política documental global: `AGENTS.md`
- Decisiones: `08_Decisions/` (ADRs)

Ante contradicción, prevalecen:
1. ADRs `Accepted` más recientes.
2. `00_MVP/MVP v2.2.md`.
3. Documentación por subsistema.

Regla: Un documento `Draft`, `Proposed` o `Preliminary` no sobreescribe una decisión bloqueada por ADR `Accepted`.

---

## 2) Objetivo de misión (MVP)

**AUSTRALIS-1 — Experimental Autonomic Flight AI-Assisted CubeSat**

Objetivo primario:
- Poner un payload de inteligencia artificial en órbita LEO, operarlo como asistente de vuelo autónomo bajo supervisión determinística y descargar datos de comportamiento válidos para entrenamiento futuro.

Objetivos secundarios:
- Validar cadena end-to-end IoT: nodo LoRa (Buenos Aires) → satélite (RX) → estación terrena (UHF) → backend.
- Store and forward por pasadas LEO.
- Science Pack (UV, ALS, magnetómetro, temperatura).
- `PHOTO_DEMO` opcional, no crítico, best-effort.

---

## 3) Baseline bloqueado (hard constraints)

### 3.1 Plataforma
- Form factor: **1.5U** (100×100×150 mm).

### 3.1.1 Órbita de diseño (Accepted — 2026-03-20)
- Tipo: **SSO (Sun-Synchronous Orbit)**, inclinación ~98° (rango 97.6°–98.8°).
- Altitud de diseño: **600 km** (rango aceptable 550–650 km).
- LTAN: **10:00h** preferido (simétrico con 14:00h).
- Eclipse nominal: **~34%**.
- Fuente: ADR-20260320-orbit-attitude-solar-layout-baseline; barrido 400 candidatos, simulador v9.2 auditado.

### 3.1.2 Actitud nominal (Accepted — 2026-03-20)
- **10×10 nadir:** cara cuadrada +Z apuntando a Tierra (nadir), eje +X en dirección de avance (ram).

### 3.1.3 Layout solar body-mounted (Accepted — 2026-03-20)
- Paneles: **+Y, −X, +X, −Z** (4 caras, ~484 cm² activa, packing 88%).
- Cara radiadora: **−Y** (LTAN 10h, antisolar), 150 cm².
- Recubrimiento radiador: **AZ-93** (preferido, α_solar≤0.20, ε_IR≥0.88) o Al anodizado blanco (fallback).
- Cara nadir +Z: libre para antenas UHF, sensores.
- Paneles desplegables: **no requeridos** para baseline.
- Celdas: 7 celdas **IBC/Maxeon baseline** (η~24%, TBD familia final).

### 3.1.4 Diseño térmico baseline (Accepted — 2026-03-20, cifras actualizadas 2026-03-21)
- Radiador −Y: α_solar ≤ 0.20, ε_IR ≥ 0.88 (AZ-93 o anodizado blanco).
- CM5 acoplado a pared −Y por pad térmico ~1 mm (G_conducción ≈ 1.5 W/K).
- Tcm5 promedio anual (sweet spot): ≤ 43°C (límite operativo 80°C) — margen 37°C.
- Tcm5 peor caso global anual: ≤ 59°C (margen 21°C).
- Tbat promedio anual (sweet spot): ≥ 17.5°C (límite operativo −10°C) — margen 28°C.
- Tbat peor caso global anual: ≥ 8.5°C (margen 18°C).
- Heater de batería: **no requerido** (margen ≥ 18°C en peor caso global).
- **TBD:** validar conductancia real y ΔT en banco con prototipo mecánico.
- Fuente: ADR-20260320-thermal-design-radiator-cm5-coupling.
- Validado con barridos de 24h, 6 meses y 12 meses (simulador v9.2/v9.3).

### 3.2 Energía (EPS)
- Topología batería de vuelo: **2S Li-ion + MPPT**.
- Batería de referencia: **2S1P con celdas 18650 de 3.0 Ah (~22 Wh nominal)**.
- Ruta de mitigación abierta: **2S2P (~44 Wh)** si el power budget con payload IA y la corriente de descarga lo requieren tras medición real en Gate IA-1.
- Banco actual: `EPS_Bench1_1S` — 1S para validación funcional (no hardware de vuelo).
- Política: **COTS bench → custom flight PCB**.
- Objetivos de referencia:
  - escenario **sin payload IA activo**: solar neto **≥1.2 W** y pico de diseño preliminar **~3 W**,
  - escenario **con payload IA activo**: target solar **TBD** hasta cerrar consumo real CM5 + duty-cycle orbital,
  - **CONF-01 abierto**: peor caso plausible mayor; no declarar cerrado sin medición de hardware TX real y Gate IA-1.
- Generación simulada (η=24%, body-mounted 4 caras, 600 km SSO): **~4.5 Wh/órbita, ~72 Wh/24h** (barrido 24h). Barrido anual (8760h, v9.3): **~4.76 Wh/órbita, ~76 Wh/día**. Margen con IA payload 20% duty: **3.6× (confirmado anual)**. TBD hasta Gate IA-1.
- Validado con barridos de 24h, 6 meses y 12 meses (simulador v9.2/v9.3).

### 3.3 COMMS
- Uplink usuario: **LoRa RX-only en órbita**, banda terrestre 915–928 MHz.
- Nodo típico: clase de nodo (radio clase SX1262/SX1276, MCU clase ESP32-S3, +20–21 dBm, sin PA/LNA/TCXO externo). No se fija SKU de mercado.
- Downlink/TTC: **UHF 435 MHz**, baseline **FSK 1200 bps**.
- Potencia objetivo UHF TX RF: **500 mW** (preliminar; requiere medición hardware final).
- Modo publico: `PUBLIC_BEACON` UHF compatible con SatNOGS, documentado y decodificable por terceros, limitado a telemetria minima no sensible.
- Downlink/uplink controlado: payload (`PHOTO_DEMO`, performance IA, `AI_BEHAVIOR_LOG` detallado, `SCIENCE`, `LORA_LOG`) y comandos TTC operan por estacion/es propia/s o autorizada/s, no por SatNOGS.
- Estacion propia: diseno dual-use SatNOGS receive-only + AUSTRALIS privado/controlado, con antena/rotor UHF compartidos y transmisor aislado de SatNOGS.
- Corrección de papel a 10°: **FSPL ~153 dB**, potencia recibida **~−119 dBm**, margen teórico **+1 dB**.
- Política de datos: **resumen por pasada por defecto + detalle on-demand**.
- Hardware TTC UHF final: **TBD**. Hardware RF orbital (PCB) no existe todavía; ver riesgo R16 en `07_Risk/top_risks.md`.
- Máscara operativa downlink UHF (provisional): validación nominal ≥20°; <20° experimental. Ver `ADR-20260313-uhf-downlink-operational-mask.md`.

### 3.4 Modelo operativo canónico

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

- `SAFE` = modo por defecto post-reset.
- Eclipse = `SAFE` por defecto.
- Actividad científica = actividad dentro de `MISSION_MODE = NOMINAL` (no modo independiente).
- Si `EPS_STATE = CRIT` → degrada a `MISSION_MODE = SAFE` sin excepción.
- `EPS_STATE = LOW` → `SAFE` por defecto; `NOMINAL` solo para housekeeping esencial explícitamente permitido.
- `EPS_STATE = NOMINAL` → operación regular, actividad científica y LoRa RX permitidos.
- `EPS_STATE = HIGH` → margen amplio para downlink extendido y ventana IA ampliada si condiciones lo permiten.
- Payload IA solo permitido con `MISSION_MODE = NOMINAL`, fase de sol y `EPS_STATE >= NOMINAL`.
- Downlink arbitration:
  1. `HOUSEKEEPING`
  2. `COMMAND_ACK`
  3. `AI_BEHAVIOR_LOG`
  4. `LORA_LOG`
  5. `SCIENCE`
  6. `OPTIONAL_PAYLOAD`
- Health mínimo por subsistema: `PGOOD_x`, `EN_x`, `FAULT_x`, `HB_x` + contadores.
- Uplink mínimo de control: `SET_MODE`, `POWER_SET`, `DL_SELECT`, `DL_SET_LIMITS`, `REQUEST_STATUS`, `ABORT`.

> Nota histórica: la denominación "SCIENCE MODE" como tercer modo operativo aparece en versiones anteriores del MVP. Queda supersedada por `MISSION_MODE = NOMINAL` con actividad científica como actividad interna. El cálculo del power budget mantiene columna `duty_sci` por compatibilidad de cálculo.

### 3.5 Payload científico MVP
- Science Pack sin Geiger/HV en MVP.
- `PHOTO_DEMO`: **Accepted** — opcional, no crítico, off-by-default, best-effort, fuera del criterio mínimo MVP. Ver `08_Decisions/ADR-20260313-photo-demo-opcional-no-critico.md`.
- **Payload IA**: **Accepted** — ver §3.6 y `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`.

### 3.6 Payload IA experimental (Accepted — actualizado 2026-03-16)

El payload IA (Inteligencia Artificial) queda bloqueado con las siguientes características normativas:

- **Rol:** payload científico primario de misión. Su fallo no impide la supervivencia del bus, pero sí impacta el criterio de éxito primario.
- **Autoridad de vuelo:** el OBC (On-Board Computer) determinístico es la autoridad final. La IA no ejecuta acciones directamente sobre subsistemas críticos.
- **Control:** la IA genera recomendaciones que el OBC valida a través de un **Runtime Safety Supervisor** determinístico.
- **Kill switch:** software y hardware. Mandatorio.
- **Hardware baseline:** familia **Raspberry Pi CM5 (Compute Module 5)**.
  - Bench candidate: CM5 8 GB.
  - Flight-like candidate inicial: CM5 4 GB + eMMC.
  - Hardware de vuelo calificado: **TBD**.
- **Modelo baseline funcional (2026-03-16):** **IBM Granite 350M fine-tuned (LoRA/QLoRA)**. Licencia Apache 2.0. Origen IBM Research.
  - Estado: baseline funcional validado en banco. No declarado modelo final de vuelo.
  - SmolLM2-360M-Instruct INT4: baseline histórico / superseded para esta función.
  - Referencia ADR: `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`.
  - Cambio de modelo baseline shall documentarse mediante nueva ADR `Accepted`.
- **Evidencia funcional de banco (2026-03-16):**
  - pass_rate_pct: BASE 14.29 % → FINE_TUNED 57.14 %
  - avg_score_ratio: BASE 0.3163 → FINE_TUNED 0.8313
  - Holdout funcional: comportamiento útil en SAFE fallback, RF fault isolation, regulatory refusal TX ISM, eclipse hold, triage de imagen.
  - Defectos residuales menores: `ai_payload_state` contextual, `policy override` total, `decision_id` normalización.
- **Operación por defecto:**
  - IA `OFF` en `MISSION_MODE = SAFE`.
  - IA `OFF` en eclipse.
  - IA `OFF` con `EPS_STATE = CRIT` o `LOW`.
  - IA `OFF` durante `MISSION_MODE = DOWNLINK_WINDOW` (salvo experimento documentado).
  - IA `ON` solo en ventanas experimentales en fase de sol, `MISSION_MODE = NOMINAL`, `EPS_STATE >= NOMINAL`.
- **Mutua exclusión IA ↔ TX UHF**: política por defecto.
- **Uplink de prompts:** el sistema soporta carga de system prompts / policy prompts versionados en órbita.
- **Behavior logging:** cada inferencia registra timestamp, model_version, prompt_version, decision_id, recommended_action, confidence, supervisor_result, MISSION_MODE, EPS_STATE.
- **Presupuesto energético:** `CONF-01` permanece abierto. Objetivo arquitectónico de pico transitorio: **6–7 W** (hipótesis de análisis, no medido). Operación continua **no asumida**. Consumo del CM5 con Granite fine-tuned **no medido** hasta Gate IA-2.
- **Fuentes:**
  - `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md` (modelo baseline)
  - `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` (arquitectura)
- **Documento técnico:** `05_Software/ai_payload_architecture.md`.
- **Evidencia técnica completa:** `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`.

### 3.7 Separación EPS

| Capa | Nombre | Propósito |
|---|---|---|
| Bench | `EPS_Bench1_1S` | Validación funcional COTS, 1S. **No hardware de vuelo.** |
| Flight-Like | `EPS_Flight_Like_2S_MPPT` | PCB custom KiCad, 2S + MPPT. No calificado. |
| Flight | `EPS_Flight_2S_MPPT` | Hardware de vuelo, 2S + MPPT, política COTS-to-Flight. TBD. |

---

## 4) Baseline P1 uplink LoRa (Accepted preliminar)

Objetivo: maximizar probabilidad de uplink con nodos de clase típica bajo restricciones de mejoras firmware+antena.

- Acceso múltiple: **modo B2 slotted (pass-aware)**.
- Nodos:
  - predicción offline de pasadas con **TLE (Two-Line Element) + SGP4 (Simplified General Perturbations 4)**,
  - RTC disciplinado por GNSS (sin depender de NTP).
- Receptor orbital objetivo: **LoRa concentrator** priorizando sensibilidad.
- Baseline success-first inicial:
  - PHY: **SF12 / BW125 / CR4/5 / CRC ON / preamble 16**
  - ventana uplink: **6 min** alrededor del pico de elevación
  - canalización inicial: **2 canales** BW125
  - redundancia: **2 TX por ventana** en slots distintos.

Parámetros TBD (no cerrados):
- elevación mínima operativa
- canalización exacta dentro de 915–928 MHz
- **BW definitivo TBD** — BW250 candidato preferente (robustez CFO/Doppler); BW125 requiere evidencia
- criterio numérico final de aceptación
- base temporal del modo B2: validación experimental pendiente (ver `ADR-20260313-b2-uplink-timebase-requirement.md`)

Fuentes: `08_Decisions/ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx.md`, `04_Communications/uplink_lora_slotted_protocol.md`.

---

## 5) Estado TTC UHF y OpenLST

- Baseline operativo vigente: **UHF 435 MHz FSK 1200 bps**.
- Arquitectura UHF vigente: un TRX TTC debe permitir `PUBLIC_BEACON` SatNOGS-friendly, `CONTROLLED_DOWNLINK` para payload/operacion y `PRIVATE_UPLINK` para comandos.
- Ground segment vigente: estacion dual-use propia con SatNOGS receive-only y AUSTRALIS privado/controlado; ver `04_Communications/ground_station_dual_use_satnogs_australis.md`.
- OpenLST: candidato técnico / base de desarrollo. Análisis técnico activo en `04_Communications/RF_ANALISYS_OPENLST.md`.
- **No adoptar OpenLST "tal cual"**: componente RFFM6403 (FEM) es EOL.
- Hardware final TTC UHF: **TBD** (requiere ADR de adopción).
- Documentar eventual adopción mediante ADR nueva antes de considerarlo baseline.
- Decision SatNOGS/publico-privado: `ADR-20260704-satnogs-public-beacon-private-payload-uplink.md`.

---

## 6) Últimas actualizaciones de subsistema incorporadas

### Desde 2026-03-16 (sesión de entrenamiento y benchmark IA)

- Payload IA — modelo baseline:
  - `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md` — nuevo baseline funcional de banco: IBM Granite 350M fine-tuned. Actualiza §C de `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`. SmolLM2 pasa a baseline histórico/superseded.
  - `05_Software/ai_payload_architecture.md` — modelo baseline actualizado, pipeline de entrenamiento y evidencia técnica incorporados.
  - `00_MVP/MVP v2.2.md` §20 — addendum modelo baseline Granite 350M fine-tuned con evidencia de banco.
  - `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md` — evidencia técnica completa de benchmark y holdout.
  - `01_Mission/requirements_matrix.md` — IA-REQ-10 actualizado; IA-REQ-11 añadido (regla de modificación de modelo por ADR).
  - `01_Mission/compliance_matrix.md` — estado de CX-AI-XX actualizado con evidencia parcial de benchmark.
  - `01_Mission/validation_plan_and_stage_gates.md` — Gate IA-1 refinado con evidencia funcional de banco; Gate IA-2 definido.
  - `07_Risk/top_risks.md` — riesgo 20 (recomendaciones erróneas del modelo) parcialmente mitigado por evidencia de banco.

### Desde 2026-03-14

- Mission / baseline:
  - `ADR-20260314-mission-redef-ai-primary.md` — redefine AUSTRALIS-1 con payload IA como objetivo primario.
  - `ADR-20260314-eps-state-4-levels.md` — amplía `EPS_STATE` a cuatro niveles.
- EPS:
  - `03_Power/Power Budget.md` — corrección del caso SCI+SAFE: **0.371 → 0.451 Wh/orbita**.
  - `03_Power/EPS Sizing.md` — batería de referencia actualizada a **~22 Wh nominal** y target solar con IA marcado **TBD**.
- COMMS:
  - `04_Communications/link_budget_uhf_preliminary.md` — corrección FSPL 10° a **~153 dB** y margen a **+1 dB**.
  - `04_Communications/link_budget_lora_uplink_preliminary.md` — Caso A renombrado a **nodo mínimo / legacy**.
- Software:
  - `05_Software/software_framework_mvp22.md` — `AI_BEHAVIOR_LOG` pasa a prioridad best-effort superior.
  - `05_Software/ai_payload_architecture.md` — payload IA alineado a misión primaria.
- Compliance y validación:
  - `01_Mission/requirements_matrix.md` — nuevos requisitos primarios MIS-REQ-16 a MIS-REQ-18.
  - `01_Mission/validation_plan_and_stage_gates.md` — `Gate IA-1` pasa a gate crítico principal.
- Gobierno:
  - `AGENTS.md` raíz y `README.md` sincronizados con identidad AUSTRALIS-1.

---

## 7) En evaluación (sin bloquear baseline)

- `03_Power/EPS_DESIGN_RULES.md`: guía técnica EPS en `Draft`; requiere ADR para congelar cualquier cambio de arquitectura.
- Estrategia TTC UHF basada en OpenLST-derived board: candidata, sin decisión final.
- Parámetros finos de uplink LoRa (BW125 vs BW250, elevación mínima, quotas definitivas).
- Costos ROM: gran parte de los valores sigue en `TBD`.
- Power budget final del payload IA, target solar con IA y posible necesidad de `2S2P`.
- Pico EPS real con hardware TX definitivo (CONF-01 en `architecture.md`).

---

## 8) Referencias operativas clave

- Mission: `01_Mission/mission_definition.md`, `01_Mission/requirements_matrix.md`, `01_Mission/compliance_matrix.md`
- Power: `03_Power/Power Budget.md`, `03_Power/EPS Sizing.md`, `03_Power/EPS_Bench1_1S.md`
- COMMS: `04_Communications/rf_subsystem_overview.md`, `04_Communications/link_budget_uhf_preliminary.md`, `04_Communications/link_budget_lora_uplink_preliminary.md`, `04_Communications/ground_station_dual_use_satnogs_australis.md`
- Software: `05_Software/software_framework_mvp22.md`, `05_Software/ground_data_architecture.md`, `05_Software/ai_payload_architecture.md`
- Costos: `06_Costs/BOM_master.csv`, `06_Costs/bom_overview.md`
- Riesgos: `07_Risk/top_risks.md`
- Validación: `01_Mission/validation_plan_and_stage_gates.md`

---

## 9) Pendientes de cierre

1. Selección de módulo UHF final y eficiencia PA medida.
2. Cierre de factibilidad uplink LoRa con evidencia de banco/campo.
3. Parámetros finos uplink LoRa: elevación mínima, canalización exacta, BW definitivo, criterio de aceptación.
4. Actualización cuantitativa del modelo de costos.
5. Relevamiento y calculo estructural de estacion terrena dual-use: torre, anclajes, linea de transmision, T/R switch e interlocks.
6. Coordinación IARU y camino regulatorio ENACOM.
7. ICD completo con integrador (inhibición RF, fit-check, masa, propiedades mecánicas).
8. Resolución CONF-01: pico EPS real con hardware TX final y consumo real del CM5 con Granite fine-tuned.
9. Cierre del target solar con payload IA activo.
10. Confirmar si la batería de referencia `2S1P` alcanza o si debe escalarse a `2S2P` tras Gate IA-1 / Gate IA-2.
11. **Gate IA-2 — Payload IA en hardware CM5 real:** boot reproducible, inferencia Granite en CM5, medición de consumo, validación térmica básica, integración OBC↔CM5 real, RuntimeSafetySupervisor integrado.
12. Análisis térmico, de masa y EMC del payload IA (TBD, sin ensayo en hardware real).
13. Sourcing / BOM del payload IA (bench candidate CM5 8 GB y flight-like candidate CM5 4 GB + eMMC): TBD.
14. Resolución de defectos residuales del fine-tuning Granite: `ai_payload_state` contextual, `policy override` total, normalización de `decision_id`.
15. Expansión del dataset JSONL para próxima iteración de fine-tuning.
