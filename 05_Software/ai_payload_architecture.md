# Arquitectura del Payload IA - AUSTRALIS-1

**Revision:** 2026-04-03
**Estado:** Active
**Trazabilidad:** `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`, `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`

---

> Este documento describe el payload IA experimental de autonomia asistida. El payload IA es el payload cientifico primario de mision. Su falla no impide la supervivencia del bus, pero si impacta el criterio de exito primario. El OBC deterministico conserva la autoridad final de vuelo en todo momento.

---

## 1) Proposito del payload IA

### 1.1 Objetivo cientifico

El payload IA materializa el objetivo primario de AUSTRALIS-1:

1. Ejecutar inferencias en orbita bajo supervision deterministica.
2. Evaluar asistencia de modelos de lenguaje pequenos en operacion satelital real.
3. Registrar comportamiento del modelo para analisis y ajuste fino en tierra.
4. Explorar priorizacion inteligente de downlink, telemetria e imagenes.

### 1.2 Posicion en el sistema

- Payload cientifico primario de la mision.
- No es subsistema mission-critical para la supervivencia del bus.
- La plataforma y el CONOPS deterministico deben seguir operando si el payload IA falla o se apaga.
- El payload IA opera siempre bajo `MISSION_MODE` / `EPS_STATE` canonicos y bajo supervision del OBC.

---

## 2) Arquitectura hardware

### 2.1 Familia de hardware seleccionada

| Rol | Familia | Descripcion |
|---|---|---|
| Familia base | Raspberry Pi CM5 (Compute Module 5) | Familia tecnologica adoptada como baseline |
| Bench candidate | CM5 8 GB | Target preferente para Gate IA-2 en banco |
| Flight-like candidate inicial | CM5 4 GB + eMMC | Primera integracion, no calificado |
| Hardware de vuelo calificado | TBD | Pendiente de validacion y calificacion |

> La decision de arquitectura bloquea la familia CM5, no un SKU comercial especifico.

### 2.2 Diagrama conceptual

```text
OBC STM32L4 (autoridad de vuelo)
  -> RuntimeSafetySupervisor
  -> AIInterface
  -> AIHealthMonitor
  -> DownlinkManager

rail AI power-gated
  -> CM5 real / familia CM5
  -> PromptStore
  -> BehaviorLogger
  -> inferencia Granite 350M fine-tuned
```

### 2.3 Separacion de capas

| Capa | Nombre | Proposito |
|---|---|---|
| Bench | CM5 8 GB sobre carrier board COTS externa | Exploracion y Gate IA-2 en banco |
| Flight-Like | CM5 4 GB + eMMC | Primera integracion, no calificado |
| Flight | TBD | Hardware de vuelo, no declarado |
| EGSE | PC tierra | Herramientas de test, simulacion y analisis |

### 2.4 Integracion bench Gate IA-2

La integracion de banco para Gate IA-2 se apoya en `EPS_Bench1_1S` extendido y mantiene la separacion canonica bench / flight-like / flight:

- `EPS_Bench1_1S` agrega un rail IA **bench-only**.
- El CM5 real corre sobre una carrier board COTS externa.
- La alimentacion principal del CM5 en banco entra por `J_AI_PWR` como `5V_AI_EXT`.
- `JP1` 2x12 queda reservado a control, sense y telemetria.
- La potencia principal del rail IA **no** pasa por `JP1`.
- El bench extendido valida secuenciamiento, FPM, logging, heartbeat, boot, kill/reset, consumo y termica basica.
- Esta integracion **no** valida el rail IA de `EPS_Flight_Like_2S_MPPT` ni cierra la arquitectura electrica de vuelo 2S + MPPT.

### 2.5 Senales de integracion bench

| Senal | Rol en banco |
|---|---|
| `EN_AI` | Habilita `SW_AI` en el bench |
| `PGOOD_AI` | Power-good del rail IA, real o sintetico por firmware bench |
| `FAULT_AI` | Fault de la rama IA, real o sintetico por firmware bench |
| `HB_AI` | Heartbeat fisico separado del CM5 |
| `AI_BOOT_OK` | Indicacion de boot operativo del CM5 |
| `AI_KILL_N` | Kill/reset de emergencia desde el FPM bench |
| `AI_UART_TX` / `AI_UART_RX` | Interfaz primaria de banco, con adaptacion de niveles si corresponde |
| `AI_THERM` | Telemetria termica basica del CM5 |
| `5V_AI_SENSE` | Sense del rail IA bench-only |

---

## 3) Modelo IA baseline

| Atributo | Valor |
|---|---|
| Modelo baseline funcional actual | IBM Granite 350M fine-tuned (LoRA/QLoRA) |
| Licencia | Apache 2.0 |
| Origen | IBM Research |
| Estado del baseline | Baseline funcional validado en banco (2026-03-16) |
| Fine-tuning | LoRA/QLoRA sobre dataset JSONL de operaciones satelitales (~1800 ejemplos) |
| Modelo historico / superseded | SmolLM2-360M-Instruct INT4 |
| Comparative bench descartado | Qwen2.5-0.5B-Instruct |
| Modelo final de vuelo | TBD |

Reglas:
- Cualquier cambio de modelo baseline requiere ADR `Accepted`.
- El modelo final de vuelo no se declara hasta cerrar Gate IA-2 y validaciones posteriores.

---

## 4) Arquitectura software del payload IA

### 4.1 Componentes logicos

| Componente | Corre en | Responsabilidad |
|---|---|---|
| `RuntimeSafetySupervisor` | OBC | Valida o rechaza recomendaciones IA. Autoridad final |
| `AIInterface` | OBC | Interfaz OBC <-> CM5 |
| `PromptStore` | CM5 | Almacena prompts versionados |
| `BehaviorLogger` | CM5 / OBC | Registra eventos de inferencia |
| `AIHealthMonitor` | OBC | Supervisa `EN_AI`, `PGOOD_AI`, `FAULT_AI`, `HB_AI`, `AI_BOOT_OK`, `AI_THERM`, `5V_AI_SENSE` y contadores |

### 4.2 Separacion entre software de vuelo y payload IA

```text
Software de vuelo deterministico (OBC):
  - DownlinkManager
  - FaultManager
  - CommandHandler
  - RuntimeSafetySupervisor
  - AIInterface
  - AIHealthMonitor

Payload IA (CM5 / Linux):
  - inferencia LLM
  - PromptStore
  - BehaviorLogger
```

El software de vuelo deterministico corre en el OBC y no depende de que el CM5 este activo. Los componentes que corren en el CM5 son parte del payload experimental.

---

## 5) Flujo OBC <-> IA

```text
1. OBC evalua condiciones operativas:
   - MISSION_MODE == NOMINAL
   - EPS_STATE in {NOMINAL, HIGH}
   - fase de sol activa
   - ventana experimental habilitada

2. OBC/FPM bench habilita SW_AI (EN_AI = HIGH) y espera PGOOD_AI

3. Se habilita la interfaz de banco hacia el CM5 y, si corresponde, se genera pulso de encendido

4. El CM5 boota, carga SO, modelo y prompt activo, y afirma AI_BOOT_OK

5. OBC/FPM bench exige HB_AI antes de aceptar la sesion como valida

6. AIInterface serializa estado/contexto y lo envia al CM5

7. El CM5 ejecuta inferencia y genera propuesta

8. El CM5 envia propuesta al OBC via AIInterface

9. RuntimeSafetySupervisor valida propuesta:
   - accepted -> OBC ejecuta
   - clipped  -> OBC ejecuta version reducida/segura
   - rejected -> OBC descarta

10. BehaviorLogger registra el evento completo

11. Al finalizar ventana experimental:
   - OBC pide shutdown logico
   - espera caida de HB_AI o timeout
   - corta SW_AI

12. Ante falla:
   - afirmar AI_KILL_N
   - esperar timeout corto
   - cortar SW_AI
```

---

## 6) Runtime Safety Supervisor

### 6.1 Reglas de mision validadas por el supervisor

| Regla | Descripcion |
|---|---|
| Energia | No activar cargas que excedan margen EPS disponible |
| Temperatura | No operar fuera de rango seguro |
| Prohibiciones RF | No comandar TX UHF durante periodos prohibidos |
| Mutua exclusion IA <-> TX | No operar IA y TX UHF simultaneamente |
| SAFE | No ejecutar acciones no criticas en `MISSION_MODE = SAFE` |
| EPS | No ejecutar inferencias con `EPS_STATE = CRIT` o `LOW` |
| Power-gating | No activar subsistemas power-gated sin condicion valida |
| Prioridad de downlink | No desplazar `HOUSEKEEPING` ni `COMMAND_ACK` |

### 6.2 Resultados posibles

| Resultado | Descripcion |
|---|---|
| `accepted` | Propuesta dentro de reglas; OBC ejecuta |
| `rejected` | Propuesta invalida; OBC descarta |
| `clipped` | Propuesta ejecutada en version limitada/segura |

---

## 7) Prompting en orbita

### 7.1 Concepto

El comportamiento del modelo IA puede modificarse en orbita mediante uplink de prompts versionados, sin reemplazar el modelo completo.

### 7.2 PromptStore

- Los prompts se almacenan de forma persistente y versionada en el CM5.
- Existe siempre un prompt seguro por defecto.
- El OBC puede cargar el prompt activo, revertir al prompt seguro y registrar que prompt estaba activo en cada inferencia.

### 7.3 Comandos conceptuales relacionados

| Comando | Descripcion |
|---|---|
| `AI_PROMPT_UPLOAD(version, content)` | Sube prompt versionado |
| `AI_PROMPT_ACTIVATE(version)` | Activa prompt almacenado |
| `AI_PROMPT_RESET_SAFE` | Revierte al prompt seguro |
| `AI_PROMPT_STATUS` | Consulta prompt activo |
| `AI_POWER_SET(ON/OFF)` | Enciende / apaga rail AI |

---

## 8) Logging cientifico del comportamiento IA

### 8.1 Behavior Logger

Cada evento de inferencia del payload IA registra:

| Campo | Descripcion |
|---|---|
| `timestamp` | Marca temporal del evento |
| `model_version` | Version del modelo activo |
| `prompt_version` | Version del prompt activo |
| `decision_id` | Identificador unico de la decision |
| `recommended_action` | Accion propuesta por el modelo |
| `confidence` | Confianza reportada por el modelo |
| `supervisor_result` | `accepted` / `rejected` / `clipped` |
| `MISSION_MODE` | Modo de mision activo |
| `EPS_STATE` | Estado energetico activo |
| `state_snapshot_hash` | Hash del contexto enviado al modelo |

### 8.2 Downlink de logs

- Cola: `AI_BEHAVIOR_LOG`
- Prioridad: mayor prioridad best-effort del Downlink Manager
- Politica: best-effort, sin desplazar `HOUSEKEEPING` ni `COMMAND_ACK`
- Capacidad: TBD

### 8.3 Uso cientifico

Los logs forman el dataset cientifico primario de la mision para:
- analisis post-vuelo
- fine-tuning posterior
- evaluacion del supervisor deterministico

---

## 9) Estados operativos del payload IA

| Estado | Condicion | Descripcion |
|---|---|---|
| `AI_OFF` | Por defecto, SAFE, eclipse, `EPS_STATE` bajo o ventana no habilitada | Rail IA apagado |
| `AI_BOOTING` | `SW_AI` habilitado, esperando `PGOOD_AI` / `AI_BOOT_OK` | Cargando SO, modelo y prompt |
| `AI_IDLE` | Payload listo, sin inferencia activa | Espera solicitud del OBC |
| `AI_INFERENCE` | Ejecutando inferencia | Procesa contexto y genera propuesta |
| `AI_FAULT` | `FAULT_AI` activo, `HB_AI` perdido o timeout de boot | OBC/FPM bench aisla, reintenta y puede entrar en lockout |

### 9.1 Politica por `EPS_STATE`

| EPS_STATE | Politica IA |
|---|---|
| `CRIT` | IA prohibida |
| `LOW` | IA prohibida |
| `NOMINAL` | IA permitida solo en `MISSION_MODE = NOMINAL` y fase de sol |
| `HIGH` | IA permitida con ventana ampliada si termica y energia lo permiten |

---

## 10) Riesgos y limites declarados

| Riesgo / limite | Mitigacion o nota |
|---|---|
| Sobreconsumo del payload IA | No declarar consumo cerrado sin medicion real |
| Fallo Linux / boot CM5 | Watchdog, `HB_AI`, kill switch y fallback deterministico |
| Corrupcion del PromptStore | Prompt seguro por defecto y control de integridad |
| Recomendaciones erroneas | RuntimeSafetySupervisor obligatorio |
| Deriva termica | No declarar cierre termico sin ensayo |
| EMI / ruido digital | Mantener mutua exclusion IA <-> TX UHF y evaluar en banco |
| Dependencia indebida del CONOPS en IA | El sistema debe operar en modo deterministico sin CM5 |
| Validacion de rail de vuelo | El bench extendido **no** valida el rail 2S + MPPT de vuelo |

Reglas explicitas:
- No se declara hardware de vuelo calificado para el payload IA.
- No se cierra consumo energetico sin medicion.
- No se cierra termica sin ensayo.
- No se cierra masa sin diseno mecanico.
- `CONF-01` permanece abierto.

---

## 11) Evidencia funcional de banco y pipeline

### 11.1 Resumen de la sesion 2026-03-16

- Hardware de entrenamiento: RTX 4060
- Metodo: QLoRA / LoRA
- Dataset: ~1800 ejemplos de operaciones satelitales en JSONL
- Baseline funcional alcanzado: Granite 350M fine-tuned

### 11.2 Benchmark corrected

| Metrica | BASE | FINE_TUNED |
|---|---|---|
| `pass_rate_pct` | 14.29 | 57.14 |
| `avg_score_ratio` | 0.3163 | 0.8313 |
| `avg_latency_s` | 5.975 | 6.691 |
| `avg_gen_tok_s` | 35.74 | 19.92 |

### 11.3 Holdout funcional

Comportamiento util y no trivial en:
- SAFE fallback
- eclipse hold / AI OFF logic
- RF fault isolation
- regulatory refusal TX ISM
- textual image triage
- policy prompt override

### 11.4 Artefactos tecnicos relevantes

- `05_Software/AI PAYLOAD/train_granite_lora_v2.py`
- `05_Software/AI PAYLOAD/benchmark_granite_lora_vs_base_corrected.py`
- `05_Software/AI PAYLOAD/test_granite_lora_holdout.py`
- `05_Software/AI PAYLOAD/cubesat_granite_dataset_schema.md`
- `05_Software/AI PAYLOAD/cubesat_granite_v3_1800.jsonl`
- `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`

---

## 12) Estado de validacion y Gate IA-2

### 12.1 Estado actual

| Nivel de validacion | Estado |
|---|---|
| Baseline funcional de banco (modelo Granite fine-tuned) | Alcanzado |
| Benchmark corrected completado | Alcanzado |
| Holdout funcional completado | Alcanzado |
| Boot reproducible CM5 real | Pendiente - Gate IA-2 |
| Inferencia en CM5 real con Granite fine-tuned | Pendiente - Gate IA-2 |
| Medicion de consumo en CM5 real | Pendiente - Gate IA-2 |
| Validacion termica basica CM5 real | Pendiente - Gate IA-2 |
| Integracion OBC <-> CM5 fisica | Pendiente - Gate IA-2 |
| RuntimeSafetySupervisor integrado con Granite | Pendiente - Gate IA-2 |
| Modelo de vuelo final declarado | No declarado |

> El payload IA no esta declarado flight-ready. El baseline funcional de banco es solo el primer hito. No se declara vuelo calificado sin cerrar Gate IA-2 y las fases posteriores.

### 12.2 Gate IA-2

**Gate IA-2 - Payload IA en hardware CM5 real con presupuesto energetico y termico medidos**

Criterios de entrada:
- Gate A completado
- benchmark + holdout funcional completados
- hardware CM5 real disponible
- `EPS_Bench1_1S` extendido documentado como plataforma bench-only de integracion
- interfaz OBC <-> CM5 de banco definida

Criterios de salida:
- `T11`: presencia de `5V_AI_EXT` con rail IA apagado y sin backfeed
- `T12`: `EN_AI` / `SW_AI` ON con `PGOOD_AI` valido
- `T13`: boot reproducible del CM5 real x5
- `T14`: `HB_AI` valido
- `T15`: perdida de `HB_AI` con kill + retry + lockout
- `T16`: prompt versionado cargado y usado en inferencia
- `T17`: `AI_BEHAVIOR_LOG` persistente con campos minimos
- `T18`: un caso `accepted` y un caso `rejected` del supervisor
- `T19`: mutua exclusion IA <-> TX UHF
- `T20`: medicion real de consumo: idle, activo e inferencia burst
- `T21`: medicion termica basica del CM5 y fallback deterministico con CM5 apagado
- ningun cierre del rail IA de vuelo 2S + MPPT por evidencia obtenida en este bench

Estado actual:
- Pendiente. Este repositorio documenta la plataforma y el plan, pero no contiene todavia evidencia de ejecucion de T11-T21.

Evidencias requeridas:
- reporte de banco sobre `EPS_Bench1_1S` extendido
- mediciones de corriente idle / active / inference
- logs de inferencia en hardware
- informe termico basico
- evidencia del supervisor integrado

### 12.3 Proximos pasos

1. Resolver defectos residuales del fine-tuning (`ai_payload_state`, `policy override`, `decision_id`).
2. Cerrar wiring de `EPS_Bench1_1S` extendido: `J_AI_PWR`, `JP1` 2x12, `SW_AI`, harness y health signals.
3. Definir la interfaz OBC <-> CM5 de banco (UART primaria; SPI / I2C siguen TBD para otras capas).
4. Medir consumo del CM5 con Granite en inferencia sobre el bench extendido.
5. Medir termica basica del CM5 en operacion sobre el bench extendido.

---

## 13) Referencias

- `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md`
- `08_Decisions/ADR-20260314-eps-state-4-levels.md`
- `00_MVP/MVP v2.2.md`
- `SYSTEM_BASELINE.md`
- `architecture.md`
- `01_Mission/requirements_matrix.md`
- `01_Mission/compliance_matrix.md`
- `01_Mission/validation_plan_and_stage_gates.md`
- `03_Power/EPS_Bench1_1S.md`
- `05_Software/software_framework_mvp22.md`
- `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`
