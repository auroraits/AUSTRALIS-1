# ADR-20260316-ai-payload-granite350m-baseline-funcional-banco

- **Fecha:** 2026-03-16
- **Estado:** Accepted

---

## Contexto

El proyecto AUSTRALIS-1 / DIY Nanosat tiene como objetivo primario la demostración de un payload IA experimental en órbita LEO bajo supervisión determinística del OBC (ver `ADR-20260314-mission-redef-ai-primary.md`).

La decisión de arquitectura general del payload IA está establecida en `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` (Estado: `Accepted`): familia CM5, RuntimeSafetySupervisor, power-gating, kill switch, off-by-default. Esa arquitectura permanece vigente e inalterada.

Sin embargo, la **selección del modelo baseline experimental** (§C de esa ADR) requería actualización por las siguientes razones:

1. **Razones geopolíticas y de narrativa**: El modelo SmolLM2-360M-Instruct (HuggingFace/Mistral origin) y los modelos de origen chino (Qwen) generan fricción narrativa con patrocinadores, agencias de lanzamiento o partners institucionales que prefieren ecosistemas de origen occidental y licencias más transparentes.

2. **Razones de licenciamiento**: Llama (Meta) tiene restricciones de uso que crean ambigüedad jurídica para un payload satelital operado potencialmente por terceros o bajo contexto académico/comercial mixto.

3. **Evidencia técnica de banco**: Durante la sesión 2026-03-16 se realizó benchmark local, entrenamiento LoRA/QLoRA sobre hardware local (RTX 4060) y holdout funcional de múltiples familias de modelos. La familia IBM Granite 350M mostró el mejor equilibrio técnico dentro de los criterios de selección.

4. **Baseline funcional validado**: El modelo IBM Granite 350M fine-tuned mediante LoRA/QLoRA alcanzó resultados de benchmark que permiten declarar baseline funcional de banco, como se documenta en el bloque de evidencia técnica de esta ADR y en `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`.

---

## Problema a resolver

Definir el modelo baseline del payload IA experimental con criterios de selección explícitos y verificables, reemplazando el modelo SmolLM2-360M-Instruct INT4 como baseline activo por una alternativa técnicamente equivalente, de origen más limpio, con licenciamiento adecuado y con evidencia funcional de banco documentada.

---

## Alternativas consideradas

| Modelo | Familia / Origen | Evaluación | Motivo de descarte |
|---|---|---|---|
| SmolLM2-360M-Instruct INT4 | HuggingFace / Mistral | Benchmark completado; baseline anterior | Narrativa ambigua (origen y governance mixto); reemplazado por mejor alternativa. |
| Qwen2.5-0.5B-Instruct | Alibaba / China | Rendimiento aceptable en benchmark inicial | Descartado por origen geopolítico (China); ambigüedad regulatoria; fricción con patrocinadores. |
| Gemma 2B | Google / DeepMind | Demasiado grande para CM5 bench en inferencia local | Tamaño excesivo para el hardware objetivo; consumo potencialmente fuera de presupuesto. |
| Llama 3.2 1B / 3B | Meta | Rendimiento robusto; ecosistema activo | Descartado por restricciones de licencia Llama (uso comercial / space / mixto ambiguo). |
| IBM Granite 350M fine-tuned | IBM Research / Apache 2.0 | Benchmark + holdout + entrenamiento QLoRA completados | **Elegida** — ver decisión. |

---

## Decisión

### A. Modelo baseline funcional de banco

El modelo baseline experimental del payload IA pasa a ser:

- **Modelo:** IBM Granite (familia 350M parámetros)
- **Fine-tuning:** entrenado localmente mediante LoRA/QLoRA sobre dataset de operaciones satelitales en formato conversacional JSONL
- **Licencia:** Apache 2.0 (compatible con uso académico, experimental y potencialmente comercial sin ambigüedades)
- **Origen:** IBM Research — ecosistema occidental, sin fricción geopolítica
- **Estado:** baseline funcional validado en banco / baseline de desarrollo / candidato de vuelo pendiente de gates
- **No declarado:** modelo final de vuelo; modelo flight-ready; consumo cerrado; térmica cerrada

### B. Relación con ADR previas

Esta ADR **no borra ni anula** `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`. Esa ADR sigue en estado `Accepted` para todos sus aspectos excepto la selección de modelo baseline (§C):

| Aspecto de ADR-20260314 | Estado |
|---|---|
| Rol payload IA (experimental, no mission-critical) | **Vigente sin cambio** |
| Hardware baseline familia CM5 | **Vigente sin cambio** |
| Bench candidate CM5 8 GB | **Vigente sin cambio** |
| Flight-like candidate CM5 4 GB + eMMC | **Vigente sin cambio** |
| Filosofía operativa (OFF/ON policy) | **Vigente sin cambio** |
| Kill switch SW + HW | **Vigente sin cambio** |
| Runtime Safety Supervisor | **Vigente sin cambio** |
| Power-gating, rail dedicado | **Vigente sin cambio** |
| Behavior logging schema | **Vigente sin cambio** |
| Downlink queue AI_BEHAVIOR_LOG | **Vigente sin cambio** |
| CONF-01 energético abierto | **Vigente sin cambio** |
| **§C — Modelo baseline experimental** | **Actualizado por esta ADR** |

SmolLM2-360M-Instruct INT4 queda registrado como **baseline histórico / superseded** para la función de modelo IA del payload. No es borrado, no es irrelevante; es la referencia del primer ciclo de trabajo.

Qwen2.5-0.5B-Instruct queda registrado como **comparative bench candidate** descartado.

### C. Justificación de la decisión de modelo

1. **Licencia Apache 2.0**: sin restricciones de uso que generen ambigüedad para contexto satelital, académico o potencialmente comercial.
2. **Origen IBM Research**: narrativa clara ante patrocinadores y posibles launch providers institucionales.
3. **Tamaño compatible con CM5 bench**: ~350M parámetros es compatible con inferencia en el hardware objetivo.
4. **Entrenamiento QLoRA operativo**: pipeline reproducible y exitoso en hardware local (RTX 4060).
5. **Evidencia funcional de banco**: mejora sustancial en benchmark corrected frente al base (ver §Evidencia).
6. **Dominio de operaciones satelitales**: fine-tuning con dataset específico JSONL de ~1800 ejemplos construido durante esta sesión.
7. **Holdout funcional en tareas misión-críticas**: comportamiento útil y no trivial verificado.

### D. Estado de validación a documentar

| Nivel | Estado |
|---|---|
| Baseline funcional de banco | **Alcanzado** |
| Candidato de vuelo / flight candidate | **Seleccionado; pendiente de gates** |
| Validación térmica con CM5 real | **NO completada** |
| Validación energética cerrada | **NO completada** |
| Integración física flight-like completa | **NO completada** |
| Campaña ambiental | **NO completada** |
| Validación orbital | **NO completada** |
| Modelo de vuelo final | **NO declarado** |

---

## Evidencia técnica de banco

### Entorno de entrenamiento

- Hardware: RTX 4060 (GPU local)
- Método: QLoRA/LoRA
- Dataset: ~1800 ejemplos de operaciones satelitales en formato conversacional JSONL
- Reproducibilidad: pipeline estable y reproducible

### Resultados benchmark corrected — BASE vs FINE_TUNED

| Métrica | BASE | FINE_TUNED |
|---|---|---|
| `pass_rate_pct` | 14.29 | 57.14 |
| `avg_score_ratio` | 0.3163 | 0.8313 |
| `avg_latency_s` | 5.975 | 6.691 |
| `avg_gen_tok_s` | 35.74 | 19.92 |

### Holdout funcional

El modelo fine-tuned mostró comportamiento útil y no trivial en los siguientes escenarios:

- `SAFE fallback` — respuestas coherentes con política de seguridad
- `eclipse hold / AI OFF logic` — parcialmente correcto
- `RF fault isolation` — respuestas útiles
- `regulatory refusal de TX ISM desde órbita` — correcto
- `textual image triage` — respuestas útiles
- `policy prompt override` — mejora respecto a iteraciones previas

### Interpretación de resultados

- El fine-tuning mejoró materialmente el comportamiento del payload IA.
- La mejora de `pass_rate_pct` de 14.29 % a 57.14 % es sustancial y suficiente para declarar baseline funcional de banco.
- El `avg_score_ratio` de 0.83 indica respuestas JSON consistentes y semánticamente útiles en la mayoría de los casos.
- La latencia media por inferencia (~6.7 s) es aceptable para el escenario de operación real (duty-cycle corto, no operación continua).

### Defectos residuales (no invalidan el baseline funcional)

Los siguientes aspectos presentan pendientes finos que no han sido completamente resueltos:

1. Control contextual de `ai_payload_state` — adherencia incompleta en casos de transición de estado.
2. Obediencia total en casos de `policy override` — mejora verificada pero no completa.
3. Normalización de `decision_id` — formato inconsistente en algunos casos.

Estos defectos son menores en el contexto del baseline funcional de banco y no invalidan la declaración de base funcional. Deben documentarse como pendientes para iteraciones futuras.

---

## Implicancias

### Documentos a actualizar

- `00_MVP/MVP v2.2.md` — addendum §20 con baseline funcional Granite 350M fine-tuned y evidencia
- `SYSTEM_BASELINE.md` — §3.6 modelo baseline actualizado; §6 cambios recientes
- `architecture.md` — snapshot decisiones con esta ADR; §10 payload IA baseline actualizado
- `README.md` — línea de baseline del payload IA actualizada
- `01_Mission/mission_definition.md` — §13.5 modelo baseline actualizado
- `01_Mission/requirements_matrix.md` — IA-REQ-10 actualizado; IA-REQ-11 nuevo
- `01_Mission/compliance_matrix.md` — estados CX-AI-XX actualizados con evidencia parcial de benchmark
- `01_Mission/validation_plan_and_stage_gates.md` — Gate IA-1 aclarado; Gate IA-2 definido
- `05_Software/ai_payload_architecture.md` — §3 modelo baseline; §nuevo pipeline de entrenamiento; evidencia técnica
- `07_Risk/top_risks.md` — riesgo 20 (recomendaciones erróneas) parcialmente mitigado por evidencia de banco

### Regla de modificación futura del modelo baseline

Cualquier cambio futuro del modelo baseline experimental del payload IA **shall** documentarse mediante una nueva ADR `Accepted`. No se permite cambiar el modelo baseline por edición directa de documentos de subsistema sin ADR.

---

## Pendientes abiertos

1. Validación energética del modelo fine-tuned en CM5 real (idle / active / inference burst) — Gate IA-1.
2. Validación térmica del CM5 en operación con modelo Granite fine-tuned — Gate IA-1 / Gate IA-2.
3. Integración física CM5 + OBC STM32L4 con interfaz OBC↔CM5 definida — Gate IA-2.
4. Métricas de consumo medidas (mA real en bench) — Gate IA-1.
5. Resolución de defectos residuales: `ai_payload_state` contextual, `policy override` completo, `decision_id` normalización.
6. Expansión del dataset JSONL para iteraciones de fine-tuning con más casos de borde.
7. Proceso de reproducibilidad del fine-tuning documentado en herramienta de CI/bench.
8. `CONF-01` permanece abierto — el consumo real del CM5 con Granite fine-tuned no ha sido medido.

---

## Referencias cruzadas

- `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` — ADR base de arquitectura del payload IA (vigente; solo §C actualizado por esta ADR)
- `ADR-20260314-mission-redef-ai-primary.md` — misión primaria IA
- `ADR-20260314-eps-state-4-levels.md` — modelo de estados energéticos
- `00_MVP/MVP v2.2.md` §19 — addendum payload IA como objetivo primario
- `05_Software/ai_payload_architecture.md` — arquitectura detallada del payload IA
- `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md` — evidencia técnica completa de benchmark y holdout
- `01_Mission/validation_plan_and_stage_gates.md` — Gate IA-1 y Gate IA-2
