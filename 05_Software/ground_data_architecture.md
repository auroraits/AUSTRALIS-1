# Arquitectura de Datos de Software de Tierra — DIY Nanosat

**Revisión:** 2026-03-13
**Estado:** Proposed (arquitectura objetivo; implementación TBD)
**Trazabilidad:** `05_Software/software_framework_mvp22.md`, `00_MVP/MVP v2.2.md` §14

> Este documento define la **arquitectura objetivo** de persistencia y manejo de datos del software de tierra (Ground Segment SW). No describe la implementación actual del dashboard (`05_Software/GroundTelemetryDashboard/`), que actualmente opera con estado en memoria como principal fuente de datos.
>
> **El estado en memoria no debe ser la única fuente de verdad del sistema de banco.** Este documento define la arquitectura que debe implementarse para soportar trazabilidad, replay y análisis post-sesión.

---

## 1) Contexto

El dashboard de telemetría actual (`.NET 8 + Blazor Server + SignalR`) opera con:
- Lectura de COM serial (banco 433 MHz) o futura entrada RF orbital.
- Visualización en tiempo real (3D, CSV, plots).
- Estado en memoria durante la sesión.

**Problema:** sin persistencia estructurada, los datos de banco se pierden al cerrar la sesión y no hay trazabilidad de evidencia reproducible.

**Objetivo:** definir una arquitectura de datos que permita:
- Log raw append-only durante la sesión.
- Almacenamiento persistente de muestras parseadas.
- Replay de sesiones pasadas.
- Export a CSV/JSON para análisis externo.
- Registro de eventos de operación.
- Separación entre cache de UI y persistencia real.

---

## 2) Principios de diseño

1. **Raw log primero:** todo dato que llega del hardware se loguea en forma cruda antes de cualquier parseado. Si el parser falla, el raw log permite recuperar.
2. **Append-only:** los logs raw no se modifican. Solo se puede agregar.
3. **Sesión como unidad:** cada sesión de operación (conexión → desconexión) tiene su propia estructura de datos y metadata.
4. **Separación de responsabilidades:** la UI usa un cache en memoria actualizado por eventos; la persistencia es independiente y no depende del estado de la UI.
5. **Trazabilidad de evidencia:** cada sesión debe poder citarse como evidencia reproducible en la compliance matrix.

---

## 3) Componentes de la arquitectura objetivo

### 3.1 Raw Log por sesión (append-only)

- Un archivo de log raw por sesión, con nombre basado en timestamp de inicio: `session_YYYYMMDD_HHMMSS.raw.log`.
- Cada línea: `[timestamp_iso] [source] <raw_data>`.
- Nunca se sobreescribe; solo append.
- Ubicación sugerida: `data/sessions/YYYYMMDD/`.

### 3.2 Almacenamiento persistente de muestras parseadas

- Base de datos liviana (SQLite o archivos JSON/CSV indexados).
- Estructura por sesión: `session_id`, `timestamp`, `seq`, campos del frame (ax, ay, az, gx, gy, gz, q0-q3 si aplica), flags de parseo.
- Las muestras parsadas son inmutables (append-only).
- En caso de error de parseo: registrar raw + flag de error; no descartar.

### 3.3 Metadata de sesión

Por cada sesión, un archivo de metadata: `session_YYYYMMDD_HHMMSS.meta.json`.

Campos mínimos:
```json
{
  "session_id": "YYYYMMDD_HHMMSS",
  "start_time_iso": "...",
  "end_time_iso": "...",
  "source": "COM3 / 115200 | UDP:<ip>:<port> | ...",
  "frame_type": "legacy_csv_8 | quaternion_csv_12 | ...",
  "total_frames": 0,
  "parse_errors": 0,
  "notes": ""
}
```

### 3.4 Replay de sesiones

- Capacidad de cargar una sesión pasada (por session_id) y reproducirla en la UI como si fuera en tiempo real.
- Usar los datos parseados almacenados, no el raw log.
- Velocidad de replay: configurable (1x, 5x, 10x o instantáneo).

### 3.5 Export a CSV/JSON

- Export a CSV con headers compatibles con los formatos soportados (legacy 8 cols, quaternion 12 cols).
- Export a JSON con la sesión completa (metadata + muestras).
- Activado por UI (botón) o por CLI.

### 3.6 Registro de eventos de operación

Además de las muestras de telemetría, registrar eventos:
- Reconexión del puerto serie.
- Errores de parseo (con raw data).
- Notas manuales del operador (campo libre).
- Power-cycle del hardware (detectable por pérdida de heartbeat).
- Cambios de modo o configuración.

Formato: `events_YYYYMMDD_HHMMSS.log` junto a la sesión.

### 3.7 Separación cache de UI / persistencia

```
[Hardware / Serial / UDP]
        ↓
[Raw Log Writer (append-only)] ──→ session_*.raw.log
        ↓
[Frame Parser]
        ↓
[Sample Writer (append-only)] ──→ DB / JSON / CSV persistente
        ↓
[In-Memory Cache] ──→ [SignalR / Blazor UI]
```

La UI accede solo al cache en memoria. La persistencia es independiente y no bloquea la UI.

---

## 4) Formatos de frame soportados (actual)

| Nombre | Campos | Descripción |
|---|---|---|
| `legacy_csv_8` | `seq,t_ms,ax,ay,az,gx,gy,gz` | Formato original del banco 433 MHz |
| `quaternion_csv_12` | `seq,t_ms,ax,ay,az,gx,gy,gz,q0,q1,q2,q3` | Con quaternion Madgwick |

Formatos futuros (TBD cuando se tenga hardware RF orbital):
- Frame UHF BEACON
- Frame UHF LORA_LOG
- Frame UHF SCIENCE_SUMMARY

---

## 5) Estado de implementación

| Componente | Estado |
|---|---|
| Raw log append-only | No implementado (TBD) |
| DB/persistencia de muestras | No implementado (TBD) |
| Metadata de sesión | No implementado (TBD) |
| Replay de sesiones | No implementado (TBD) |
| Export CSV/JSON | No implementado (TBD) |
| Registro de eventos | No implementado (TBD) |
| Cache en memoria (UI actual) | Implementado (Blazor/SignalR) |

> **Nota:** el dashboard actual opera correctamente para el caso de uso de banco en tiempo real. Esta arquitectura objetivo es el siguiente paso para soportar trazabilidad de evidencia y análisis post-sesión.

---

## 6) Relación con compliance y validación

- La evidencia de ensayos de banco (T1-T10 EPS, uplink P1 LoRa, FlatSat) debe quedar como sesiones persistentes exportables.
- La compliance matrix (`01_Mission/compliance_matrix.md`) referencia evidencia de sesiones de banco.
- La arquitectura aquí definida es el habilitador para el evidence pack del plan de validación (`01_Mission/validation_plan_and_stage_gates.md`).

---

## 7) Referencias

- `05_Software/GroundTelemetryDashboard/docs/README.md`
- `01_Mission/compliance_matrix.md`
- `01_Mission/validation_plan_and_stage_gates.md`
- `00_MVP/MVP v2.2.md` §14 (Addendum software de banco)

---

## 8) Gap actual y criterio de Gate B

### 8.1 Brecha entre documentación y software real

> **Brecha explícita:** esta arquitectura está completamente especificada como objetivo, pero **no está implementada** en el dashboard actual (`05_Software/GroundTelemetryDashboard/`). El estado en memoria sigue siendo la única fuente de verdad del sistema de banco.

Impactos concretos de este gap:
- Los ensayos de banco actuales **no generan raw logs persistentes** ni muestras parseadas recuperables post-sesión.
- No es posible citar sesiones de ensayo como **evidencia reproducible** para la compliance matrix (`01_Mission/compliance_matrix.md` CX-SW-03, CX-EP-01).
- Sin persistencia estructurada, los criterios de éxito de Gate B no pueden cerrarse.

Estado actual del dashboard: opera correctamente para visualización en tiempo real (caso de uso de banco inmediato). No es un problema funcional hoy, pero es un bloqueador para trazabilidad de evidencia.

### 8.2 Criterio obligatorio en Gate B

> **Gate B (Cierre uplink P1) no puede cerrarse** sin implementación funcional de los siguientes componentes de esta arquitectura:

| Componente | Obligatorio para Gate B |
|---|---|
| Raw log append-only por sesión (§3.1) | **Sí** |
| Almacenamiento persistente de muestras parseadas (§3.2) | **Sí** |
| Metadata de sesión (§3.3) | **Sí** |
| Export CSV/JSON básico (§3.5) | **Sí** |
| Separación cache UI / persistencia (§3.7) | **Sí** |
| Replay de sesiones (§3.4) | Deseable; puede diferirse a Gate E |
| Registro de eventos de operación (§3.6) | Deseable; puede diferirse a Gate E |

**Owner:** Ground SW. Ver `01_Mission/validation_plan_and_stage_gates.md` Gate B.
