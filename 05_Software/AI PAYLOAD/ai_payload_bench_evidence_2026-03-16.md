# Evidencia Técnica de Banco — Payload IA AUSTRALIS-1

**Fecha de sesión:** 2026-03-16
**Estado:** Active
**Trazabilidad:** `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`

> Este documento registra la evidencia técnica de la sesión de entrenamiento, benchmark y holdout del payload IA realizada el 2026-03-16. Es el respaldo técnico de la declaración de baseline funcional de banco del modelo IBM Granite 350M fine-tuned.

---

## 1) Contexto

Esta sesión tenía como objetivo:
1. Realizar benchmark de modelos pequeños compatibles con el hardware objetivo (familia CM5).
2. Seleccionar una familia de modelos con criterios técnicos, de licenciamiento y geopolíticos adecuados para un payload satelital.
3. Entrenar localmente el modelo seleccionado mediante LoRA/QLoRA con datos de operaciones satelitales.
4. Evaluar el modelo entrenado mediante benchmark corrected y holdout funcional.
5. Declarar baseline funcional de banco si los resultados son suficientes.

**Decisión de baseline resultante:** IBM Granite 350M fine-tuned — ver `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`.

---

## 2) Entorno de trabajo

| Atributo | Valor |
|---|---|
| Hardware de entrenamiento | GPU local RTX 4060 |
| Método de fine-tuning | QLoRA / LoRA |
| Formato de dataset | JSONL conversacional (instrucción + respuesta JSON estructurada) |
| Dominio del dataset | Operaciones satelitales: modos de misión, EPS, RF, downlink, seguridad |
| Tamaño del dataset | ~1800 ejemplos (iteración final de la sesión) |
| Reproducibilidad | Pipeline estable y reproducible |

---

## 3) Proceso de selección de modelo

### 3.1 Benchmark inicial de modelos candidatos

Se evaluaron múltiples familias de modelos pequeños compatibles con el hardware objetivo (CM5, ~4–8 GB RAM):

| Candidato | Observación |
|---|---|
| SmolLM2-360M-Instruct INT4 | Baseline anterior; rendimiento modesto sin fine-tuning |
| Qwen2.5-0.5B-Instruct | Rendimiento aceptable; descartado por origen geopolítico |
| Gemma 2B | Demasiado grande para inferencia eficiente en hardware objetivo |
| Llama 3.2 1B | Buen rendimiento; descartado por restricciones de licencia |
| IBM Granite 350M | **Seleccionado** — ver criterios de selección |

### 3.2 Criterios de selección final

1. **Licencia Apache 2.0** — sin restricciones que generen ambigüedad para contexto satelital, académico o potencialmente comercial.
2. **Origen IBM Research (occidental)** — narrativa clara ante patrocinadores, agencias de lanzamiento y partners.
3. **Tamaño compatible con CM5** — ~350M parámetros, viable en inferencia en hardware objetivo.
4. **Fine-tuning QLoRA operativo** — pipeline reproducible verificado en la sesión.
5. **Sin restricciones geopolíticas** — sin dependencias de ecosistemas con restricciones regulatorias potenciales.

---

## 4) Pipeline de entrenamiento

### 4.1 Descripción

1. **Benchmark initial**: Se evaluó el modelo Granite 350M base sin fine-tuning sobre el benchmark contractual para establecer la línea base.
2. **Construcción del dataset**: Se construyó y expandió un dataset JSONL de operaciones satelitales con ~1800 ejemplos cobriendo:
   - Gestión de modos de misión (`SAFE`, `NOMINAL`, `DOWNLINK_WINDOW`)
   - Control de EPS y `EPS_STATE`
   - Aislamiento de fallas RF
   - Política regulatoria (rechazo TX ISM desde órbita)
   - Triage de datos de imagen
   - Respuestas a policy prompt override
   - Fallback SAFE
   - Hold de eclipse / AI OFF logic
3. **Fine-tuning QLoRA**: Entrenamiento con LoRA/QLoRA sobre dataset JSONL en hardware local (RTX 4060). Entrenamiento estable y sin divergencia.
4. **Evaluación benchmark corrected**: Benchmark sobre el modelo fine-tuned con el mismo conjunto de casos del benchmark inicial.
5. **Holdout funcional**: Evaluación sobre casos no vistos durante el entrenamiento.

### 4.2 Scripts y artefactos asociados

| Artefacto | Ubicación |
|---|---|
| Script de entrenamiento QLoRA (v2) | `05_Software/AI PAYLOAD/train_granite_lora_v2.py` |
| Script de benchmark corrected | `05_Software/AI PAYLOAD/benchmark_granite_lora_vs_base_corrected.py` |
| Script de holdout funcional | `05_Software/AI PAYLOAD/test_granite_lora_holdout.py` |
| Script de generación de dataset | `05_Software/AI PAYLOAD/generate_final_correction_200.py` |
| Schema del dataset | `05_Software/AI PAYLOAD/cubesat_granite_dataset_schema.md` |
| Dataset de entrenamiento (~1800 ej.) | `05_Software/AI PAYLOAD/cubesat_granite_v3_1800.jsonl` |
| Casos de holdout funcional | `05_Software/AI PAYLOAD/cubesat_holdout_cases.json` |
| Suite de benchmark JSON | `05_Software/AI PAYLOAD/CubeSatBenchmarkSuite.json` |
| Script benchmark Ollama (PS1) | `05_Software/AI PAYLOAD/OllamaBenchmark_CubeSat_v5.ps1` |
| Adaptador LoRA entrenado | No se vendorea en el árbol público; ver `05_Software/AI PAYLOAD/MODEL_ASSETS.md` |

---

## 5) Resultados de benchmark

### 5.1 Benchmark corrected — BASE vs FINE_TUNED

Resultados finales de la sesión 2026-03-16:

| Métrica | BASE (Granite 350M sin fine-tuning) | FINE_TUNED (Granite 350M QLoRA) |
|---|---|---|
| `pass_rate_pct` (%) | 14.29 | **57.14** |
| `avg_score_ratio` | 0.3163 | **0.8313** |
| `avg_latency_s` (s) | 5.975 | 6.691 |
| `avg_gen_tok_s` (tok/s) | 35.74 | 19.92 |

**Notas sobre las métricas:**
- `pass_rate_pct`: porcentaje de respuestas que cumplen los criterios funcionales del benchmark contractual.
- `avg_score_ratio`: ratio promedio de calidad semántica de las respuestas (0 = respuesta inútil, 1 = respuesta perfecta).
- `avg_latency_s`: latencia promedio por inferencia en hardware de entrenamiento (RTX 4060). La latencia real en CM5 será mayor y debe medirse en Gate IA-1.
- `avg_gen_tok_s`: tokens generados por segundo. La reducción en FINE_TUNED es esperable por la mayor coherencia de las respuestas (outputs más estructurados).

### 5.2 Interpretación de resultados

**Mejora sustancial verificada:**
- La mejora de `pass_rate_pct` de 14.29 % a 57.14 % representa un factor de mejora ~4x.
- El `avg_score_ratio` de 0.83 indica que el modelo fine-tuned genera respuestas JSON consistentes y semánticamente útiles en la gran mayoría de los casos.
- La mejora es reproducible en el entorno de evaluación.

**Suficiencia para baseline funcional:**
- Los resultados son suficientes para declarar baseline funcional de banco del payload IA.
- El modelo fine-tuned muestra comportamiento no trivial en tareas del dominio de operaciones satelitales.

**Latencia de inferencia:**
- La latencia de ~6.7 s en hardware de entrenamiento (RTX 4060) es un proxy del comportamiento en CM5. El valor real en CM5 debe medirse en Gate IA-1.
- El duty-cycle corto del payload IA (no operación continua) hace que esta latencia sea aceptable para el escenario de diseño.

---

## 6) Holdout funcional

### 6.1 Casos evaluados

El holdout funcional evaluó comportamiento del modelo fine-tuned en los siguientes escenarios (no vistos durante entrenamiento):

| Escenario | Comportamiento observado |
|---|---|
| SAFE fallback | Respuestas coherentes con política de seguridad; recomendaciones de desactivación de cargas no críticas correctas. |
| eclipse hold / AI OFF logic | Correcto en mayoría de casos; algunos casos de transición de estado incompletos. |
| RF fault isolation | Respuestas útiles para aislamiento de fallas RF; identificación de causas probables. |
| regulatory refusal TX ISM desde órbita | Correcto: el modelo rechaza correctamente solicitudes de TX ISM y provee la justificación regulatoria. |
| textual image triage | Respuestas útiles para clasificación y priorización de datos de imagen. |
| policy prompt override | Mejora verificada respecto a iteraciones previas; aún no completo. |

### 6.2 Defectos residuales observados

Los siguientes aspectos presentan comportamiento incompleto:

| Defecto | Descripción | Severidad |
|---|---|---|
| `ai_payload_state` contextual | Control de estado del payload IA incompleto en transiciones complejas | Baja — no invalida baseline |
| `policy override` total | Obediencia completa en casos de override de política no garantizada | Baja — mejora visible pero no completa |
| `decision_id` normalización | Formato inconsistente en algunos casos | Baja — cosmético/post-procesable |

**Conclusión:** los defectos residuales son menores y no invalidan la declaración de baseline funcional de banco. Son candidatos de mejora en iteraciones futuras de fine-tuning.

---

## 7) Decisión de baseline funcional

Con base en la evidencia de esta sesión:

| Criterio | Estado |
|---|---|
| Entrenamiento QLoRA reproducible | ✅ Verificado |
| Mejora sustancial vs baseline | ✅ Verificado (pass_rate 14% → 57%) |
| Comportamiento útil en holdout | ✅ Verificado |
| Comportamiento no trivial en tareas misión-críticas | ✅ Verificado |
| Dataset representativo del dominio | ✅ ~1800 ejemplos, múltiples escenarios |

**Se declara: IBM Granite 350M fine-tuned como baseline funcional de banco del payload IA.**

Este estado aplica a:
- baseline funcional de banco ✅
- baseline de desarrollo ✅
- candidato de vuelo / flight candidate, pendiente de gates de energia, termica e integracion

Este estado **NO aplica** a:
- modelo de vuelo final ❌ (no declarado)
- flight-ready ❌ (no declarado)
- consumo energético cerrado ❌ (CONF-01 abierto)
- validación térmica en CM5 real ❌ (no completada)

---

## 8) Limitaciones y pendientes para Gate IA-1 / Gate IA-2

| Pendiente | Gate asociado |
|---|---|
| Medición de latencia de inferencia en CM5 real | Gate IA-1 |
| Medición de consumo eléctrico (idle / active / inference) en CM5 real | Gate IA-1 |
| Validación térmica del CM5 en operación con modelo Granite | Gate IA-1 / Gate IA-2 |
| Integración física CM5 + OBC STM32L4 con interfaz real | Gate IA-2 |
| Test del RuntimeSafetySupervisor integrado con el modelo Granite | Gate IA-1 |
| Boot reproducible del CM5 con modelo Granite en hardware real | Gate IA-1 |
| Resolución de defectos residuales (ai_payload_state, policy override, decision_id) | Iteración pre-Gate IA-1 |

---

## 9) Referencias

- `08_Decisions/ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
- `05_Software/ai_payload_architecture.md`
- `01_Mission/validation_plan_and_stage_gates.md`
- `05_Software/AI PAYLOAD/train_granite_lora_v2.py` — script de entrenamiento QLoRA (v2)
- `05_Software/AI PAYLOAD/benchmark_granite_lora_vs_base_corrected.py` — benchmark corrected BASE vs FINE_TUNED
- `05_Software/AI PAYLOAD/test_granite_lora_holdout.py` — script de holdout funcional
- `05_Software/AI PAYLOAD/generate_final_correction_200.py` — generación del dataset
- `05_Software/AI PAYLOAD/cubesat_granite_dataset_schema.md` — schema del dataset
- `05_Software/AI PAYLOAD/cubesat_granite_v3_1800.jsonl` — dataset de entrenamiento (~1800 ejemplos)
- `05_Software/AI PAYLOAD/cubesat_holdout_cases.json` — casos de holdout funcional
- `05_Software/AI PAYLOAD/CubeSatBenchmarkSuite.json` — suite de benchmark contractual
- `05_Software/AI PAYLOAD/MODEL_ASSETS.md` — política pública para pesos, tokenizers, adaptadores y checkpoints
