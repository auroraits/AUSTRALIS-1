# Plan de Validación y Stage-Gates — AUSTRALIS-1 / DIY Nanosat MVP

**Revisión:** 2026-04-03
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md`, `01_Mission/compliance_matrix.md`, `01_Mission/requirements_matrix.md`

> Este documento define el **plan** de validación y los criterios de los stage-gates. No declara resultados de ensayo. Los resultados se documentan en la evidence pack de cada gate cuando se obtengan.

---

## 1) Objetivo

Definir una ruta de validación incremental desde banco hasta órbita que:
- cierre requisitos verificables (`01_Mission/requirements_matrix.md`),
- genere evidencia trazable para la compliance matrix,
- identifique dependencias y riesgos antes de cada fase,
- sea coherente con la separación bench / flight-like / flight,
- y priorice el cierre del objetivo primario de misión en el payload IA.

**Regla de criticidad:** `Gate IA-1` es el gate más crítico del plan. Sin su cierre no puede declararse cumplimiento del criterio mínimo primario de misión.

---

## 2) Fases de ensayo

| Fase | Nombre | Descripción |
|---|---|---|
| F0 | Bench | Validación funcional de componentes y subsistemas en laboratorio |
| F1 | Campo | Validación de enlace RF terrestre (LoRa + UHF) con hardware representativo |
| F2 | FlatSat | Integración completa del sistema en mesa (sin estructura/vuelo) |
| F3 | Ambiental / Fit-Check | Ensayos ambientales básicos + fit-check con dispenser (si aplica) |
| F4 | Operación inicial (Órbita) | Activación progresiva post-lanzamiento |

---

## 3) Stage-Gates

### Gate A — Configuración documental coherente

**Objetivo:** El baseline documental está sincronizado y los agentes tienen una fuente de verdad unificada.

**Criterios de entrada:**
- Repositorio accesible con estructura definida.

**Criterios de salida:**
- `AGENTS.md` raíz con política documental global completo y aceptado.
- `architecture.md` actualizado con precedencia, estados y regla de propagación.
- `SYSTEM_BASELINE.md` y `README.md` sincronizados.
- `00_MVP/MVP v2.2.md` con modelo operativo único (`MISSION_MODE`/`EPS_STATE`).
- `PHOTO_DEMO` congelado como opcional no crítico (ADR `Accepted`).
- Compliance matrix (`compliance_matrix.md`) inicial creada.
- ADRs de gobierno documental, nodo típico, EPS separación, misión primaria y EPS_STATE 4 niveles en estado `Accepted`.

**Estado actual (2026-03-14):** ✅ **Completado** — baseline documental resincronizado en esta pasada correctiva.

**Evidencias requeridas:** Este documento + ADRs listadas en `architecture.md`.

**Dependencias:** Ninguna.

**Owner tentativo:** Sistema / Documentación.

---

### Gate IA-1 — Payload IA bench baseline cerrado

**Objetivo:** El payload IA experimental ha sido validado en banco con el modelo baseline y puede considerarse candidato a integrarse en la plataforma.

**Criterios de entrada:**
- Gate A completado. ✅
- Hardware bench candidate (CM5 8 GB o equivalente) disponible.
- Interfaz OBC ↔ CM5 definida y conectada en banco.

**Criterios de salida (subdivididos en alcanzados / pendientes):**

Alcanzados (evidencia de banco sin hardware CM5):
- ✅ Benchmark funcional del modelo baseline completado (benchmark corrected + holdout 2026-03-16).
- ✅ Modelo baseline seleccionado con criterios explícitos y documentado en ADR `Accepted`.
- ✅ Dataset de entrenamiento representativo del dominio de operaciones satelitales (~1800 ejemplos).
- ✅ Fine-tuning QLoRA operativo y reproducible en hardware local.
- ✅ Mejora sustancial verificada (pass_rate 14 % → 57 %; avg_score_ratio 0.32 → 0.83).
- ✅ Holdout funcional en tareas misión-críticas: SAFE fallback, RF fault isolation, regulatory refusal, eclipse hold.

Pendientes (requieren hardware CM5 real — Gate IA-2):
- ❌ Boot reproducible del payload IA en CM5 real (CM5 8 GB + Linux + Granite fine-tuned).
- ❌ Inferencia reproducible en CM5 real con prompt por defecto.
- ❌ Cambio de prompt por uplink simulado — verificar que el modelo usa el nuevo prompt en CM5 real.
- ❌ Behavior logging persistente en CM5 real — verificar que los campos mínimos se registran.
- ❌ RuntimeSafetySupervisor integrado — al menos un caso de accept y uno de reject en CM5 real.
- ❌ Power cycling controlado — verificar boot limpio tras corte de alimentación en CM5.
- ❌ Medición de consumo en CM5 real: idle, activo, inferencia burst (mW reales).
- ❌ Evidencia de fallback a control determinístico — operación normal del OBC con CM5 apagado.
- ❌ Ningún cierre falso de térmica/consumo sin datos medidos.

**Estado actual:** ⚠️ Parcialmente completado.
- Parte funcional (benchmark de modelo, holdout, selección con criterios, evidencia de banco): **alcanzada** (2026-03-16).
- Parte de hardware (boot CM5 real, medición consumo, integración OBC↔CM5, supervisor integrado): **pendiente** — requiere hardware bench candidate.

**Evidencias requeridas (pendientes):** Reporte de banco con CM5 real, logs de inferencia en hardware, mediciones de consumo reales, resultados del supervisor integrado.

**Evidencias requeridas (disponibles):** `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`, `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`.

**Dependencias:** Hardware bench candidate (CM5 8 GB), interfaz OBC↔CM5 implementada.

**Owner tentativo:** FSW/EPS.

**Riesgos relacionados:** Top-risks 17–23 (payload IA).

---

### Gate IA-2 — Payload IA en hardware CM5 real sobre `EPS_Bench1_1S` extendido

**Objetivo:** Validar el payload IA con Granite fine-tuned en hardware CM5 real usando `EPS_Bench1_1S` extendido como plataforma bench-only. Este gate cierra boot, secuenciamiento, FPM, logging, consumo y térmica básica del CM5 real en banco. **No** valida el rail IA de vuelo 2S + MPPT.

**Criterios de entrada:**
- Gate A completado. ✅
- Evidencia funcional de banco (benchmark + holdout) completada. ✅
- `EPS_Bench1_1S` extendido documentado con FPM bench + rail IA bench-only + `J_AI_PWR`.
- Hardware bench candidate (CM5 8 GB) disponible.
- Interfaz OBC ↔ CM5 de banco definida (UART primaria; SPI / I2C siguen TBD para otras capas).
- Firmware del RuntimeSafetySupervisor disponible para prueba integrada.

**Criterios de salida:**
- `T11` — presencia de `5V_AI_EXT` con rail IA apagado y sin backfeed.
- `T12` — `EN_AI` / `SW_AI` ON y verificación de `PGOOD_AI`.
- `T13` — boot reproducible del CM5 real x5.
- `T14` — `HB_AI` válido.
- `T15` — pérdida de `HB_AI` -> kill + retry + lockout.
- `T16` — prompt versionado cargado y usado en inferencia.
- `T17` — `AI_BEHAVIOR_LOG` persistente con campos mínimos.
- `T18` — un caso `accepted` y un caso `rejected` del supervisor.
- `T19` — mutua exclusión IA ↔ TX UHF.
- `T20` — medición real de consumo: idle / activo / inferencia burst.
- `T21` — medición térmica básica del CM5 + fallback determinístico con CM5 apagado.
- Ningún cierre de presupuesto energético sin datos medidos.
- Ninguna extrapolación del rail IA bench-only al rail IA de vuelo.

**Estado actual:** ❌ Pendiente — existe definición documental del bench extendido, pero no hay evidencia de ejecución T11–T21 en el repo.

**Evidencias requeridas:** Reporte de banco sobre `EPS_Bench1_1S` extendido, medición de corriente (idle/active/inference), logs de inferencia en hardware, informe térmico básico, resultados del supervisor integrado y evidencia de T11–T21.

**Dependencias:** Hardware CM5 8 GB, interfaz OBC↔CM5 implementada, wiring bench extendido cerrado.

**Owner tentativo:** FSW/EPS.

**Bloquea:** Gate E (FlatSat integrado), Gate F (Readiness), criterio primario de éxito orbital.

---

### Gate B — Cierre uplink P1

**Objetivo:** Evidencia medida de que el uplink LoRa con nodos de clase típica es factible en condiciones representativas.

**Criterios de entrada:**
- Gate A completado.
- Banco LoRa disponible con hardware de clase nodo típica.
- Plan de pruebas `docs/COMMS/uplink_lora_bench_testing_plan.md` definido.

**Criterios de salida:**
- Medición real de sensibilidad RX del receptor orbital en banco.
- Tolerancia a CFO/Doppler medida con offset simulado (BW125 vs BW250 evidenciados; BW definitivo cerrado).
- Probabilidad de recepción en ventana de 6 min estimada con datos medidos.
- Parámetros TBD cerrados: elevación mínima operativa, BW definitivo, criterio de aceptación.
- Riesgos CX-RF-01 y `comms_lora_uplink_feasibility_risk.md` con evidencia.
- Validación de base temporal del modo B2: deriva real del RTC/cristal medida y dentro del guard time del slot (o decisión documentada de operar en B1).
- **Implementación funcional de persistencia de datos de tierra** según `05_Software/ground_data_architecture.md` §8.2.

**Estado actual:** ❌ Pendiente — requiere hardware y ensayos.

**Evidencias requeridas:** Reporte de banco con datos medidos, plots de BER/PDR vs elevación simulada, parámetros cerrados en ADR.

**Dependencias:** Hardware receptor LoRa orbital seleccionado (concentrator o módulo), nodo de clase típica disponible.

**Owner tentativo:** COMMS.

**Riesgos relacionados:** Top-risks 1, 2, 3, 4, 5.

---

### Gate C — TTC UHF dev base cerrado

**Objetivo:** Hardware TTC UHF seleccionado, evaluado en banco y candidato a flight-like.

**Criterios de entrada:**
- Gate B completado (o en paralelo).
- Candidato de TTC UHF definido (OpenLST-derived u otro).

**Criterios de salida:**
- Medición de potencia RF, sensibilidad RX y consumo eléctrico del TX (resuelve CONF-01).
- Medición de emisiones espurias / armónicos (verificar CX-RF-03).
- Supply chain del PA y SAW confirmada (sin EOL crítico).
- ADR de adopción TTC UHF en estado `Accepted`.
- Baseline operativo UHF (bitrate, modulación, potencia) confirmado o actualizado.
- `PUBLIC_BEACON` transmitido por hardware candidato, recibido por SDR/estación propia y decodificado con frame schema publico.
- Separación verificada entre `PUBLIC_BEACON`, `CONTROLLED_DOWNLINK` y `PRIVATE_UPLINK`; el beacon no incluye payload, comandos, prompts ni datos operativos sensibles.
- Paquete preliminar SatNOGS DB preparado: frecuencia, modo, baudrate, servicio, estado, referencia publica y decoder/protocolo del beacon.
- Estacion terrena fase 1/2 disponible para recepcion UHF direccional: rotor AZ/EL, antena 435-438 MHz, SDR, LNA/filtro, logs y pipeline de evidencia.
- T/R switch digital y secuenciador evaluados en banco/dummy load antes de cualquier uplink radiado.
- Validación de máscara operativa ≥20° con hardware real: link budget re-calculado con pérdidas medidas. Confirmación o revisión de `ADR-20260313-uhf-downlink-operational-mask.md`.

**Estado actual:** ❌ Pendiente — hardware TTC UHF final TBD.

**Evidencias requeridas:** Medición de espectro, link budget validado con hardware real, ADR de adopción, captura/decoder del `PUBLIC_BEACON`, evidencia de separación publico/controlado, evidencia de estacion terrena RX direccional y pruebas de T/R switch sin TX radiado.

**Dependencias:** Selección de PA UHF, SAW, placa PCB flight-like.

**Owner tentativo:** COMMS/EPS.

**Riesgos relacionados:** Top-risks 6, 11, 12, 31.

---

### Gate D — EPS flight-like cerrado

**Objetivo:** PCB EPS 2S + MPPT flight-like fabricado, ensayado y apto para integración FlatSat.

**Criterios de entrada:**
- Gate A completado.
- Diseño KiCad `EPS_PCB/EPS_Bench2S_FlightLike/` completado.
- BOM 2S confirmada con componentes disponibles.

**Criterios de salida:**
- Pruebas T1-T10 equivalentes al banco 1S pero en plataforma 2S.
- Medición real de consumo en todos los modos (`MISSION_MODE = SAFE / NOMINAL / DOWNLINK_WINDOW`).
- Validación de transiciones `EPS_STATE = CRIT / LOW / NOMINAL / HIGH`.
- Pico EPS medido con carga real (resuelve CONF-01 de `architecture.md`).
- Dossier de batería 2S completado (CX-EPS-02).
- Power-gating y health signals verificados.

**Estado actual:** ❌ Pendiente — PCB 2S en KiCad, sin fabricar.

**Evidencias requeridas:** Reporte de pruebas T1-T10 (2S), medición de corrientes, dossier batería.

**Dependencias:** BOM EPS flight-like cerrada, fabricación PCB, selección celda 2S.

**Owner tentativo:** EPS.

**Riesgos relacionados:** Top-risks 7, 8, 14.

---

### Gate E — FlatSat integrado

**Objetivo:** Sistema completo integrado en mesa con todos los subsistemas funcionales end-to-end.

**Criterios de entrada:**
- Gate IA-2 completado (incluye evidencia funcional de banco y hardware CM5 real validado).
- Gate B, C y D completados (o versiones preliminares funcionales documentadas).
- OBC con firmware de vuelo (beta).

**Criterios de salida:**
- Boot determinista en `MISSION_MODE = SAFE`.
- Arbitraje de colas verificado bajo saturación.
- Payload IA integrado en el loop OBC ↔ supervisor ↔ logging.
- LoRa RX activo en ventana de pasada simulada.
- UHF TX/RX operativo end-to-end con estación terrena.
- Modo SatNOGS receive-only aislado del modo AUSTRALIS privado/controlado; SatNOGS sin acceso al transmisor/PTT.
- Science Pack I2C funcional.
- GNSS best-effort funcional.
- Power-gating por `EN_x` verificado.
- `PHOTO_DEMO` off-by-default y aislado (si está incluido).
- Persistencia de logs en NOR + microSD verificada.

**Estado actual:** ❌ Pendiente — requiere Gates IA-2, B, C y D.

**Evidencias requeridas:** Reporte de integración FlatSat, screenshots/logs de cada función.

**Dependencias:** Gates IA-2, B, C, D.

**Owner tentativo:** Sistema / FSW.

**Riesgos relacionados:** Top-risks 9, 10, 13, 15, 17–23.

---

### Gate F — Readiness / Compliance Pack

**Objetivo:** El sistema está listo para integración con el integrador de lanzamiento; compliance pack documentado.

**Criterios de entrada:**
- Gates IA-2 y E completados.
- ICD del integrador disponible.

**Criterios de salida:**
- Compliance matrix con todos los ítems `Closed` o `Blocked by Integrator` con justificación documentada.
- Evidence pack completo: banco, campo, FlatSat, ambiental (si aplica).
- Coordinación IARU documentada (CX-RF-04).
- Camino regulatorio ENACOM documentado (CX-RF-05).
- Inhibiciones RF implementadas y verificadas (CX-RF-02).
- Dossier de batería completo (CX-EPS-02).
- Fit-check completado (CX-M-06).
- Masa, CG y propiedades mecánicas documentadas (CX-M-02, CX-M-03).
- Documentación de ICD, drawings y owners entregada al integrador (CX-M-07).

**Estado actual:** ❌ Pendiente — requiere todos los gates anteriores.

**Evidencias requeridas:** Evidence pack completo, compliance matrix cerrada, documentación entregada al integrador.

**Dependencias:** Gates A, IA-1, IA-2, B, C, D, E + ICD del integrador.

**Owner tentativo:** Sistema / Operaciones.

**Riesgos relacionados:** Top-risks 12, 13; todos los ítems `Blocked by Integrator` en compliance matrix.

---

## 4) Resumen de gates

| Gate | Nombre | Estado actual | Bloquea |
|---|---|---|---|
| A | Configuración documental coherente | ✅ Completado (2026-03-14) | Gate IA-1, IA-2, B, C, D |
| IA-1 | Payload IA bench baseline — parte funcional (benchmark + holdout + ADR) | ⚠️ Parcialmente completado (2026-03-16) | Gate IA-2 |
| IA-2 | Payload IA en hardware CM5 real sobre `EPS_Bench1_1S` extendido | ❌ Pendiente — bench extendido documentado; faltan T11–T21 | Gate E, Gate F y criterio primario de misión |
| B | Cierre uplink P1 | ❌ Pendiente | Gate E |
| C | TTC UHF dev base cerrado | ❌ Pendiente | Gate E |
| D | EPS flight-like cerrado | ❌ Pendiente | Gate E |
| E | FlatSat integrado | ❌ Pendiente | Gate F |
| F | Readiness / Compliance Pack | ❌ Pendiente | Lanzamiento |

---

## 5) Riesgos vs gates

| Riesgo (top_risks.md) | Gate de cierre | Evidencia requerida |
|---|---|---|
| 1 — Uplink LoRa factibilidad | B | Medición real PDR en banco |
| 2 — CFO/Doppler BW125 | B | Test de tolerancia a offset |
| 3 — Slots desalineados | B | Test de slotting con múltiples nodos |
| 4 — TLE desactualizado | B | Validación del mecanismo TLE update |
| 5 — Integración concentrator | B/C | Banco de integración RF |
| 6 — Downlink UHF margen | C | Medición real con hardware TX |
| 7 — Déficit energético / brownouts | D | Pruebas banco 2S bajo carga real |
| 8 — EMI interna EPS vs RF | D/E | Medición integrada |
| 9 — Reset / SW no idempotente | E | Test de robustez FlatSat |
| 10 — Regulatorio / frecuencias | F | Documentación IARU/ENACOM |
| 11 — Supply chain TTC UHF | C | BOM cerrada sin EOL |
| 12 — Compliance integrador | F | ICD + evidence pack |
| 13 — IARU sin coordinación | F | Documentación coordinación |
| 14 — Pico EPS real | D / IA-1 | Medición con TX real y carga IA |
| 15 — Persistencia datos tierra | B/E | Implementación ground_data_architecture |
| 17 — Sobreconsumo payload IA | IA-2 | Medición real idle/active/inference en CM5 real |
| 18 — Fallo Linux / boot CM5 | IA-2 | Test de boot reproducible en CM5 real y fallback |
| 19 — Corrupción PromptStore | IA-2 | Test de prompt swap y verificación de integridad en CM5 real |
| 20 — Recomendaciones erróneas del modelo | IA-1 (parcial) / IA-2 | IA-1: evidencia de banco (holdout, benchmark corrected — 2026-03-16). IA-2: test del supervisor integrado en hardware real. |
| 21 — Deriva térmica payload IA | IA-2 / E | Análisis térmico + medición en CM5 real |
| 22 — Acoplamiento EMI (digital noise) | IA-2 / E | Medición con analizador espectro integrado |
| 23 — Dependencia indebida CONOPS en IA | IA-2 | Verificar operación nominal del OBC con CM5 apagado |
| 24 — Extrapolación indebida bench 1S -> rail IA de vuelo | IA-2 / D | Evidencia bench acotada + separación documental conservada hasta `EPS_Flight_Like_2S_MPPT` |
| 25 — Backfeed entre `5V_AI_EXT` y rails del bench | IA-2 | Resultado de `T11` con rail IA apagado y sin retroalimentación |
| 26 — Potencia IA rutada por `JP1` | IA-2 | Inspección de wiring y evidencia de `J_AI_PWR` como entrada principal |
| 27 — `SW_AI` insuficiente para corriente de arranque del CM5 | IA-2 | Resultado de `T12`, `T13` y medición de corriente real |
| 28 — Caída excesiva si se usa `INA219` inline | IA-2 | Medición T20 + justificación de metrología externa si corresponde |
| 29 — Secuenciamiento incorrecto del CM5 | IA-2 | Evidencia de T12–T15 y secuencia documentada de encendido/apagado |
| 30 — Corrupción por apagado brusco del CM5 | IA-2 | Evidencia de apagado lógico, kill controlado y fallback determinístico |

---

## 6) Referencias

- `01_Mission/compliance_matrix.md`
- `01_Mission/requirements_matrix.md`
- `00_MVP/MVP v2.2.md`
- `07_Risk/top_risks.md`
- `architecture.md`
- `04_Communications/ground_station_dual_use_satnogs_australis.md`
- `05_Software/ai_payload_architecture.md`
- `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md`
- `08_Decisions/ADR-20260314-eps-state-4-levels.md`
- `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`
- `docs/COMMS/uplink_lora_bench_testing_plan.md`
- `03_Power/EPS_Bench1_1S.md` §9 (plan de pruebas T1-T21)
- `03_Power/EPS_PCB/EPS_Bench1S/eps_bench_mods.md`
