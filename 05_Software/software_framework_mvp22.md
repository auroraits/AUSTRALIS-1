# Software Framework MVP 2.2 — Downlink/Fault/Commands

**Revisión:** 2026-03-14 (misión AUSTRALIS-1, `EPS_STATE` 4 niveles y `AI_BEHAVIOR_LOG` repriorizado)
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md`, `08_Decisions/ADR-20260218-downlink-arbitration-and-subsystem-power-framework.md`

## 1) Servicios permanentes de vuelo

### 1.1 DownlinkManager
Responsable de arbitraje por colas:
- `HOUSEKEEPING`
- `COMMAND_ACK`
- `AI_BEHAVIOR_LOG`
- `LORA_LOG`
- `SCIENCE`
- `OPTIONAL_PAYLOAD`

Política por modo:
- SAFE: solo `HOUSEKEEPING` y `COMMAND_ACK`.
- NOMINAL: prioridades críticas + cuotas best-effort.
- DOWNLINK_WINDOW: misma prioridad crítica + mayor cuota no-crítica.

Regla permanente: `AI_BEHAVIOR_LOG` es la cola best-effort de mayor prioridad científica, sin desplazar `HOUSEKEEPING` ni `COMMAND_ACK`.

### 1.2 FaultManager
- Supervisa `PGOOD_x`, `FAULT_x`, `HB_x`.
- Ejecuta aislamiento por subsistema (`EN_x`) ante falla.
- Aplica reintentos acotados y lockout por timeout/uplink.

### 1.3 CommandHandler
Comandos mínimos soportados:
- `SET_MODE`
- `POWER_SET`
- `DL_SELECT`
- `DL_SET_LIMITS`
- `REQUEST_STATUS`
- `ABORT`

## 2) Modelo de telemetría de salud
Campos mínimos por subsistema:
- `EN_x`
- `PGOOD_x`
- `FAULT_x`
- `HB_x`
- `reset_count_x`
- `fault_count_x`
- `last_fault_reason_x`

## 3) Máquina de estados operativa (modelo canónico)

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

### 3.1 MISSION_MODE
- **SAFE**: default / supervivencia; solo `HOUSEKEEPING` + `COMMAND_ACK`.
- **NOMINAL**: operación regular; actividades científicas como actividad interna; LoRa RX en ventanas; payload IA permitido solo bajo condiciones energéticas y de iluminación válidas.
- **DOWNLINK_WINDOW**: descarga priorizada; mayor cuota best-effort; prioridad crítica mantenida.

### 3.2 EPS_STATE
- **CRIT**: fuerza `MISSION_MODE = SAFE`; solo housekeeping mínimo y `COMMAND_ACK`; payload IA OFF.
- **LOW**: conservación; `SAFE` por defecto; GNSS OFF; sin dumps; sin actividad científica; payload IA OFF.
- **NOMINAL**: operación regular; actividad científica y LoRa RX permitidos; payload IA permitido solo en fase de sol.
- **HIGH**: margen amplio; downlink extendido y ventana IA ampliada si condiciones lo permiten.

Transición a SAFE obligatoria ante:
- `EPS_STATE = CRIT`.
- Fault persistente de potencia.
- Brownout o pérdida de supervisión crítica.

> Nota: la denominación "SCIENCE MODE" en versiones anteriores queda supersedada por `MISSION_MODE = NOMINAL` con actividad científica como actividad interna.

<!-- FEATURE:PHOTO_DEMO START -->

## 4) [PHOTO_DEMO] Protocolo opcional de archivo/chunks

### 4.1 [PHOTO_DEMO] Flujo
1. Publicar mini-catálogo de 3–4 thumbnails comprimidos.
2. Esperar selección por uplink (`DL_SELECT`).
3. Transferir archivo por chunks con reanudación (NACK bitmap o lista de faltantes).

### 4.2 [PHOTO_DEMO] Integración en colas
- [PHOTO_DEMO] usa `OPTIONAL_PAYLOAD` exclusivamente.
- Límite por pasada configurable (`DL_SET_LIMITS`).
- Interrupción inmediata por `ABORT` o evento de fault/power.

### 4.3 [PHOTO_DEMO] Criterio de no interferencia
Falla o desactivación de [PHOTO_DEMO] no debe degradar `HOUSEKEEPING`, `COMMAND_ACK`, `LORA_LOG` ni control de modo.

<!-- FEATURE:PHOTO_DEMO END -->

## 5) Componentes lógicos del payload IA (2026-03-14)

Los siguientes componentes lógicos forman la capa de software del payload IA experimental. Se mantienen separados del software de vuelo determinístico del OBC.

| Componente | Corre en | Responsabilidad |
|---|---|---|
| `RuntimeSafetySupervisor` | OBC (determinístico) | Valida o rechaza recomendaciones del payload IA contra reglas de misión. Autoridad final. Parte del FSW. |
| `AIInterface` | OBC | Interfaz de comunicación OBC ↔ CM5. Serializa contexto; deserializa propuesta. Parte del FSW. |
| `PromptStore` | CM5 (Linux) | Almacena prompts versionados; expone prompt activo al modelo; soporta rollback a prompt seguro. Parte del payload. |
| `BehaviorLogger` | CM5 / OBC | Registra cada evento IA: decisión, resultado supervisor, contexto. Flushed al OBC antes de apagado del rail AI. |
| `AIHealthMonitor` | OBC | Supervisa señales de salud del payload: `EN_AI`, `PGOOD_AI`, `FAULT_AI`, `HB_AI`, `reset_count_AI`, `fault_count_AI`. |

**Regla de separación:** el software de vuelo determinístico en el OBC no depende de que el CM5 esté activo. Los componentes que corren en el CM5 son parte del payload experimental.

Para arquitectura detallada, flujo OBC↔IA, estados operativos y riesgos del payload IA, ver: `05_Software/ai_payload_architecture.md`.

## 6) Referencias
- `00_MVP/MVP v2.2.md`
- `03_Power/Power Budget.md`
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/uplink_data_products_and_downlink_policy.md`
- `05_Software/ai_payload_architecture.md`
- `08_Decisions/ADR-20260218-downlink-arbitration-and-subsystem-power-framework.md`
- `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md`
- `08_Decisions/ADR-20260314-eps-state-4-levels.md`