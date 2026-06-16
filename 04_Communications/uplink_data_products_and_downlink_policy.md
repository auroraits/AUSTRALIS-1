# Uplink LoRa — Productos de datos y política de downlink (resumen vs detalle)

**Fecha de revisión:** 2026-03-14 (repriorización AI_BEHAVIOR_LOG y misión AUSTRALIS-1)
**Estado:** Active

## 1) Problema
El uplink LoRa puede producir muchos paquetes por pasada si escalamos nodos.
El downlink UHF (baseline 1k2) es el cuello de botella. Por lo tanto, el sistema debe:
- registrar todo a bordo,
- **bajar por defecto solo resúmenes**,
- permitir “drill-down” a detalle bajo comando,
- y garantizar que el dataset primario del payload IA conserve prioridad científica superior.

## 2) Productos de datos

### 2.1 Resumen por pasada (default)
Estructura lógica (ejemplo):
- `pass_id` (timestamp/contador)
- `window_start/end`
- `elevation_max_est` (si se tiene)
- `rx_total`, `rx_crc_ok`, `rx_crc_fail`
- `per_node[]` (para N nodos, limitado a top-K):
  - `node_id`
  - `ok_count`, `fail_count`
  - `seq_min/seq_max` (o último seq)
  - `rssi_avg`, `snr_avg`
  - `cfo_avg` (y/o min/max)

Downlink: en cola `HOUSEKEEPING` o `LORA_LOG` con prioridad baja pero garantizando “al menos un resumen por pasada”.

### 2.2 Catálogo (índice de paquetes) por nodo
Para selección posterior:
- por `node_id`: lista compacta de `(seq, t_rx, flags)` o hashes.

### 2.3 Detalle (on-demand)
- últimos K paquetes de un `node_id`, o rango de tiempo.
- transferencia por chunks reanudables (idéntico patrón conceptual al [PHOTO_DEMO]).

## 3) Comandos (TTC UHF) necesarios
Sin definir el encoding todavía, el set mínimo conceptual:
- `LORA_SUMMARY_GET(pass_id)`
- `LORA_NODE_CATALOG_GET(node_id, since)`
- `LORA_NODE_DUMP(node_id, last_k | time_range)`
- `DL_SET_LIMITS(queue=LORA_LOG, quota)`
- `ABORT`

## 4) Implicancias
- El flight software debe persistir:
  - payload + metadata por paquete (timestamp, RSSI/SNR/CFO, CRC status).
- Se requiere política de retención (rolling buffer) si el storage es limitado.

## 5) Prioridad de colas de downlink (actualizado 2026-03-14)

Con la redefinición de misión AUSTRALIS-1, la prioridad de colas del Downlink Manager queda:

| Prioridad | Cola | Descripción |
|---|---|---|
| 1 (estricta) | `HOUSEKEEPING` | Telemetría de salud y housekeeping del sistema. Prioridad absoluta. |
| 2 (estricta) | `COMMAND_ACK` | Acuses de recibo de comandos. Prioridad absoluta. |
| 3 (best-effort) | `AI_BEHAVIOR_LOG` | Logs de comportamiento del payload IA. Dato científico primario de misión. |
| 4 (best-effort) | `LORA_LOG` | Logs de paquetes LoRa recibidos. |
| 5 (best-effort) | `SCIENCE` | Telemetría científica del Science Pack. |
| 6 (best-effort) | `OPTIONAL_PAYLOAD` | Cargas opcionales (PHOTO_DEMO). Mínima prioridad. |

**Regla permanente:** ninguna cola de prioridad menor puede bloquear o desplazar `HOUSEKEEPING` ni `COMMAND_ACK`.

## 6) Uplink para payload IA (Prompt uplink)

Con la decisión de incorporar el payload IA como objetivo científico primario, el sistema debe soportar:

### 6.1 Uplink de prompts versionados

El sistema debe poder recibir por uplink UHF **system prompts / policy prompts versionados** para modificar el comportamiento del modelo IA en órbita sin reemplazar el modelo.

Comandos conceptuales (TBD encoding):
- `AI_PROMPT_UPLOAD(version, content)` — sube nuevo prompt versionado.
- `AI_PROMPT_ACTIVATE(version)` — activa un prompt almacenado.
- `AI_PROMPT_RESET_SAFE` — revierte al prompt seguro por defecto.
- `AI_PROMPT_STATUS` — consulta prompt activo + versión.
- `AI_POWER_SET(ON/OFF)` — enciende / apaga rail AI.

Los prompts se almacenan persistentemente en el CM5 (PromptStore). El OBC registra qué prompt estaba activo en cada decisión del Behavior Logger.

### 6.2 Downlink de AI behavior logs

Los logs del Behavior Logger del payload IA se descargan por la cola `AI_BEHAVIOR_LOG` como **dato científico primario de misión**.

- Política: best-effort, sin desplazar colas de prioridad estricta.
- Capacidad de la cola y cuota por pasada: TBD (depende del duty-cycle del payload IA).
- Formato: estructura de evento mínimo con campos: timestamp, model_version, prompt_version, decision_id, recommended_action, confidence, supervisor_result, MISSION_MODE, EPS_STATE, state_snapshot_hash.

## 7) Referencias
- `05_Software/software_framework_mvp22.md` (DownlinkManager/FaultManager)
- `05_Software/ai_payload_architecture.md` (arquitectura payload IA)
- `04_Communications/uplink_lora_slotted_protocol.md`
- `01_Mission/mission_definition.md`
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md`