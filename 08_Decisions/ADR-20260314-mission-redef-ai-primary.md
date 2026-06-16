# ADR-20260314-mission-redef-ai-primary

- **Fecha:** 2026-03-14
- **Estado:** Accepted

---

## Contexto

El proyecto comenzó con foco primario en una misión store-and-forward IoT:

`Nodo LoRa terrestre -> satélite RX -> downlink UHF -> backend`

La incorporación del payload IA experimental y la evaluación del valor científico esperado mostraron que la demostración de autonomía asistida en vuelo ofrece:
- mayor originalidad científica,
- dataset de alto valor para entrenamiento futuro,
- y una identidad de misión más clara que la cadena IoT por sí sola.

El operador humano decidió el 2026-03-14 redefinir el objetivo primario de misión y fijar una identidad explícita de proyecto/misión.

---

## Decisión

La misión pasa a denominarse:

**AUSTRALIS-1 — Experimental Autonomic Flight AI-Assisted CubeSat**

### Objetivo primario

Poner un payload de inteligencia artificial en órbita LEO (Low Earth Orbit), operarlo como asistente de vuelo autónomo bajo supervisión determinística y recolectar datos de desempeño del modelo para entrenar futuras versiones de IA para CubeSats.

### Objetivos secundarios

1. Validar cadena end-to-end IoT: nodo LoRa (Buenos Aires) → satélite (RX) → estación terrena (UHF) → backend.
2. Store-and-forward por pasadas LEO.
3. Science Pack (UV, ALS, magnetómetro, temperatura).
4. `PHOTO_DEMO` opcional, no crítico, best-effort.

### Criterio de éxito mínimo actualizado

1. **Primario:** el payload IA (CM5 + SmolLM2-360M-Instruct INT4) completa al menos **5 ciclos de inferencia** en órbita con propuestas validadas por el `RuntimeSafetySupervisor`, con logging completo descargado a tierra.
2. **Primario:** se recolectan y descargan al menos **100 registros `AI_BEHAVIOR_LOG`** válidos.
3. **Primario:** al menos **1 prompt versionado** es recibido por uplink, aplicado por `PromptStore` y usado en inferencia con resultado registrado.
4. **Secundario:** recepción en órbita de al menos **10 paquetes LoRa** originados en Buenos Aires y descargados a tierra por UHF con métricas.
5. Evidencia reproducible con correlación a ventanas de pasada orbital.

### Criterio de éxito extendido (MVP+)

- Operación estable del payload IA durante **>=30 días**.
- **>=1 000 registros `AI_BEHAVIOR_LOG`** descargados.
- Al menos **3 versiones de prompt** operadas y comparadas en órbita.
- Dataset post-vuelo útil para análisis y fine-tuning.
- **>=70%** de paquetes LoRa válidos por pasada en configuración robusta.
- Telemetría histórica y trending operativo.

### Reglas aclaratorias

- El payload IA sigue siendo **no mission-critical para la supervivencia del bus**.
- Su falla no impide que el satélite sobreviva ni opere en modo determinístico.
- Pero su falla **sí impacta directamente el criterio de éxito primario** de la misión.
- `AI_BEHAVIOR_LOG` pasa a ser la cola científica de mayor prioridad best-effort del Downlink Manager:
  1. `HOUSEKEEPING`
  2. `COMMAND_ACK`
  3. `AI_BEHAVIOR_LOG`
  4. `LORA_LOG`
  5. `SCIENCE`
  6. `OPTIONAL_PAYLOAD`

---

## Alternativas consideradas

1. **Mantener IoT store-and-forward como objetivo primario e IA como payload subordinado**:
   - Rechazada. Subrepresenta el valor científico diferencial del payload IA.
2. **Eliminar el objetivo IoT y convertirlo en fuera de alcance**:
   - Rechazada. La cadena IoT sigue siendo valiosa como objetivo secundario y validación de arquitectura.
3. **Redefinir la misión con IA como objetivo primario e IoT como secundario**:
   - Elegida.

---

## Tradeoffs / riesgos

| Factor | Consideración |
|---|---|
| A favor | Mayor valor científico, identidad de misión más clara, dataset orbital útil para futuras IAs satelitales. |
| En contra | Mayor riesgo técnico y dependencia de Gate IA-1 para el éxito primario. |
| Riesgo principal | El payload IA aún no tiene validación de banco cerrada; consumo, térmica y EMC siguen TBD. |
| Mitigación | Supervisor determinístico, power-gating, criterios de gate explícitos, fallback a operación determinística del bus. |

---

## Implicancias (archivos a actualizar)

- `01_Mission/mission_definition.md` — objetivo, secundarios y criterios de éxito.
- `01_Mission/requirements_matrix.md` — nuevos requisitos primarios IA.
- `01_Mission/compliance_matrix.md` — trazabilidad de criterios primarios IA.
- `01_Mission/validation_plan_and_stage_gates.md` — `Gate IA-1` pasa a gate crítico.
- `00_MVP/MVP v2.2.md` — título, objetivo, criterios de éxito, colas y payload IA.
- `SYSTEM_BASELINE.md` — objetivo de misión y resumen ejecutivo.
- `architecture.md` — identidad de misión, snapshot ADR y pendientes.
- `README.md` — nueva identidad AUSTRALIS-1.
- `AGENTS.md` — objetivo del repositorio y modelo canónico asociado.
- `05_Software/ai_payload_architecture.md` — payload IA como objetivo científico primario.
- `05_Software/software_framework_mvp22.md` — prioridad de `AI_BEHAVIOR_LOG`.
- `04_Communications/uplink_data_products_and_downlink_policy.md` — prioridad de colas.
- `07_Risk/top_risks.md` — riesgos 17–23 pasan a impactar el éxito primario.