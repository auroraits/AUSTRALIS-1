# ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision

- **Fecha:** 2026-03-14
- **Estado:** Accepted

---

## Contexto

El proyecto AUSTRALIS-1 / DIY Nanosat adopta como objetivo primario la validación de un payload IA asistente de vuelo en órbita (ver `ADR-20260314-mission-redef-ai-primary.md`). En sesión de diseño del 2026-03-14 se evaluaron distintas arquitecturas para incorporar capacidades de inteligencia artificial (IA) a bordo con seguridad operacional y autoridad determinística del OBC.

Los objetivos científicos asociados al payload IA son:

1. Estudiar toma de decisiones autónoma en CubeSat.
2. Evaluar asistencia de modelos de lenguaje en operación satelital.
3. Registrar comportamiento del modelo IA para análisis y ajuste fino en tierra.
4. Explorar priorización inteligente de downlink, telemetría e imágenes.

Las alternativas evaluadas abarcaron:
- IA como subsistema de vuelo mission-critical (rechazada: riesgo inaceptable).
- IA como payload experimental con supervisor determinístico (elegida).
- Sin payload IA (opción conservadora, preservada como fallback implícito).

La decisión de arquitectura también requirió seleccionar familia de hardware de cómputo y modelo de lenguaje baseline para el payload.

---

## Decisión

### A. Rol del payload IA

El subsistema IA (Inteligencia Artificial) se incorpora como **payload científico primario de la misión** y como **payload experimental de autonomía asistida**, no como subsistema mission-critical del bus.

Su falla o apagado no debe afectar la supervivencia del sistema ni la autoridad determinística del OBC, pero sí impacta directamente el criterio de éxito primario de misión.

El OBC (On-Board Computer) determinístico conserva la **autoridad final de vuelo** en todo momento.

La IA solo genera **recomendaciones / propuestas**. El OBC las valida o rechaza a través de un **Runtime Safety Supervisor** determinístico antes de cualquier ejecución.

Debe existir **kill switch** por software y por hardware del payload IA. Ante degradación energética o de salud del sistema, el satélite regresa a operación completamente determinística sin depender del payload IA.

### B. Hardware baseline del payload IA

Se adopta la **familia Raspberry Pi Compute Module 5 (CM5)** como baseline de hardware del payload IA. Esta decisión es sobre la familia tecnológica, no sobre un SKU (Stock Keeping Unit) comercial específico.

| Rol | Descripción |
|---|---|
| Bench candidate | CM5 8 GB — target preferente para exploración y comparación de modelos en laboratorio. |
| Flight-like candidate inicial | CM5 4 GB + eMMC (Embedded Multi-Media Card) — candidato sobrio para la primera iteración del payload IA. |
| Hardware de vuelo calificado | **No declarado aún. TBD.** |

La compra y sourcing local sigue siendo TBD y pertenece a la BOM (Bill of Materials) / costos, no a requisitos normativos. No se fija SKU de marketplace como requisito.

### C. Modelo IA baseline

Se adopta como baseline experimental inicial del payload IA:
- Modelo: **SmolLM2-360M-Instruct**
- Cuantización: **INT4**

Este modelo se trata como **baseline experimental**. No se declara como modelo final de vuelo hasta completar validación de banco (Gate IA-1).

`Qwen2.5-0.5B-Instruct` queda documentado como **stretch / comparative bench candidate** — no es el baseline de misión.

### D. Filosofía operativa del payload IA

El payload IA es **power-gated** en un rail dedicado. Es una carga **no crítica para la supervivencia del bus** pero **crítica para el objetivo científico primario**.

Política de operación por defecto:

| Condición | Estado payload IA |
|---|---|
| `MISSION_MODE = SAFE` | OFF (mandatorio) |
| Eclipse | OFF (mandatorio) |
| `EPS_STATE = CRIT` o `LOW` | OFF (mandatorio) |
| `MISSION_MODE = DOWNLINK_WINDOW` | OFF por defecto (salvo experimento explícito documentado) |
| Fase de sol + `MISSION_MODE = NOMINAL` + `EPS_STATE >= NOMINAL` | ON (permitido) |

Política por defecto: **mutua exclusión operacional IA ↔ TX UHF** (no operar simultáneamente sin evaluación explícita).

### E. Prompting en órbita

El sistema debe soportar uplink de **system prompts / policy prompts versionados** para modificar el comportamiento de la IA sin reemplazar el modelo. Los prompts se almacenan de forma persistente y versionada. El OBC debe poder:
- cargar el prompt activo,
- revertir al prompt seguro por defecto,
- registrar qué prompt estaba activo en cada decisión logueada.

### F. Logging científico del comportamiento IA

Debe existir un **Behavior Logger** del payload IA. Cada evento mínimo del payload IA debe registrar:

| Campo | Descripción |
|---|---|
| `timestamp` | Marca temporal del evento |
| `model_version` | Versión del modelo activo |
| `prompt_version` | Versión del prompt activo |
| `decision_id` | Identificador único de la decisión |
| `recommended_action` | Acción propuesta por la IA |
| `confidence` | Confianza reportada por el modelo |
| `supervisor_result` | `accepted` / `rejected` / `clipped` |
| `MISSION_MODE` | Modo de misión activo |
| `EPS_STATE` | Estado energético activo |
| state_snapshot_hash | Hash del contexto resumido |

Estos datos forman parte del dataset científico de la misión.

La cola `AI_BEHAVIOR_LOG` pasa a tener la **mayor prioridad best-effort** del Downlink Manager, por encima de `LORA_LOG` y `SCIENCE`, sin desplazar `HOUSEKEEPING` ni `COMMAND_ACK`.

### G. Seguridad y degradación

El Runtime Safety Supervisor valida que la recomendación IA no viole reglas determinísticas de misión: energía, temperatura, prioridades de downlink, power-gating, prohibiciones de emisión, reglas de SAFE.

Señales de salud mínimas del payload IA: `EN_AI`, `PGOOD_AI`, `FAULT_AI`, `HB_AI`, `reset_count_AI`, `fault_count_AI`.

Si el payload IA falla o se degrada: aislarlo, apagarlo si corresponde, y continuar misión base sin dependencia del payload IA.

### H. Energía y presupuesto (sin cerrar)

Esta ADR **no cierra el power budget del payload IA**. Se establece:
- Objetivo arquitectónico de pico transitorio: **6–7 W** totales para soportar el payload IA (hipótesis de análisis, no valor medido).
- Esto **no implica operación continua** del payload IA.
- `CONF-01` (conflicto de pico EPS real) permanece abierto.
- El payload IA se modela como carga experimental por duty-cycle corto en fase de sol hasta validar consumos reales.
- Duración operativa por órbita: **TBD** — hipótesis/escenario de análisis hasta validación de banco.

---

## Alternativas consideradas

| Alternativa | Evaluación |
|---|---|
| IA como subsistema de vuelo mission-critical | Rechazada. Riesgo inaceptable de pérdida de misión por fallo de modelo o Linux. |
| IA completamente autónoma, ejecuta acciones directamente | Rechazada. Sin supervisor determinístico, viola principio de seguridad operacional. |
| Hardware Intel NUC / Jetson Nano class | Rechazada. Consumo excesivo para la envolvente energética disponible. |
| Hardware microcontrolador + modelos sub-100 M parámetros | Viable como stretch conservador, pero insuficiente para los objetivos científicos. |
| CM5 family con SmolLM2-360M-Instruct INT4 (elegida) | Mejor equilibrio entre valor científico, energía, duty-cycle, integración y seguridad de misión. |
| Qwen2.5-0.5B-Instruct como baseline | No elegida como baseline. Mayor tamaño sin ventaja decisiva a este ciclo. Documentada como comparative bench candidate. |
| Sin payload IA | Conservadora y válida; preservada implícitamente como fallback si el payload falla. |

---

## Tradeoffs / riesgos

| Factor | Consideración |
|---|---|
| A favor | Valor científico diferencial; arquitectura segura con supervisor determinístico; fallback garantizado; modelo cuantizado viable en CM5. |
| En contra | Complejidad adicional (Linux, boot, watchdog, thermal); carga de trabajo de integración no trivial. |
| Riesgo principal | Sobreconsumo no previsto, fallo de boot de Linux, corrupción de prompt store, recomendaciones erróneas. |
| Mitigación | Supervisor determinístico, kill switch, power-gating, operación best-effort, logging, fallback. |

Nota: el consumo real del payload IA (idle, activo, inferencia) es desconocido hasta validación de banco. No declarar presupuesto energético como cerrado sin medición.

---

## Implicancias (archivos a actualizar)

- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` — este documento (creado).
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md` — reordenamiento de objetivos de misión.
- `00_MVP/MVP v2.2.md` — incorporar payload IA como objetivo primario, OBC como autoridad, modelo baseline, prompting y logging.
- `SYSTEM_BASELINE.md` — resumen ejecutivo del payload IA, impacto arquitectónico, CONF-01 visible.
- `architecture.md` — ADR al snapshot, regla de propagación para payload IA, capa IA en mapa.
- `README.md` — línea breve sobre payload IA primario.
- `01_Mission/mission_definition.md` — payload IA en definición de misión, objetivo científico primario, supervisor determinístico.
- `01_Mission/requirements_matrix.md` — requisitos IA-REQ-01 a IA-REQ-10 y criterios primarios MIS-REQ-16 a MIS-REQ-18.
- `01_Mission/compliance_matrix.md` — placeholders Open/Partial para ítems del payload IA.
- `01_Mission/validation_plan_and_stage_gates.md` — Gate IA-1 (bench baseline payload IA) como gate crítico.
- `03_Power/Power Budget.md` — escenario AI payload experimental; objetivo 6–7 W pico; CONF-01 reforzado.
- `04_Communications/uplink_data_products_and_downlink_policy.md` — uplink de prompts, downlink de AI behavior logs, prioridad de colas actualizada.
- `05_Software/software_framework_mvp22.md` — componentes lógicos del payload IA: RuntimeSafetySupervisor, AIInterface, PromptStore, BehaviorLogger, AIHealthMonitor.
- `05_Software/ai_payload_architecture.md` — documento detallado del payload IA.
- `06_Costs/cost_overview.md` — líneas AI payload bench y flight-like.
- `06_Costs/bom_overview.md` — subsistema AI Payload en tabla de subsistemas.
- `07_Risk/top_risks.md` — riesgos 17–23 del payload IA.