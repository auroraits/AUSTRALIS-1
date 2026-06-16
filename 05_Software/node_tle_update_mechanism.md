# Node TLE Update Mechanism (ESP32) — Especificación mínima

**Fecha de revisión:** 2026-02-20
**Estado:** propuesta (P1)

## 1) Objetivo
Asegurar que los nodos (ESP32) puedan mantener actualizado el **TLE** del satélite para predecir pasadas offline (SGP4) y ejecutar uplink modo B2.

## 2) Requerimientos
- El nodo debe poder almacenar **al menos 1 TLE activo** (ideal: 2, active + previous).
- Debe existir un mecanismo de actualización **out-of-band** (no vía satélite).
- Debe validarse integridad básica del TLE y registrar metadata (fecha de carga, epoch del TLE).

## 3) Formato de almacenamiento (recomendado)

### 3.1 En NVS/Flash
Guardar:
- `tle_line1` (string)
- `tle_line2` (string)
- `tle_loaded_at_utc` (uint32/uint64)
- `tle_epoch_utc` (derivado del TLE)
- `tle_source` (enum: manual|wifi|ble|serial)

Mantener opcional:
- `tle_prev_line1/line2` (para rollback)

## 4) Interfaces de actualización (todas firmware-only)

### 4.1 Manual (archivo/config)
- El usuario carga el TLE en el firmware (build-time) o en un archivo de configuración persistente.
- Útil para primeras pruebas.

### 4.2 WiFi (cuando exista red)
- Endpoint HTTP(s) simple en el nodo (pull) o en un gateway local.
- El nodo consulta 1 vez cada X días.
- No se asume disponibilidad permanente.

### 4.3 BLE/Serial (offline)
- Una app (móvil/PC) empuja el TLE al nodo.
- El nodo confirma recepción y guarda en NVS.

## 5) Validación mínima del TLE
- Longitud y prefix esperados (line1 empieza con '1 ', line2 con '2 ').
- Checksum de línea (si se implementa; recomendado).
- Parsear epoch del TLE y rechazar si está demasiado viejo (policy configurable).

## 6) Política de “staleness” (TBD)
- Inicialmente: warning si `now - tle_epoch > 7 días`.
- Hard-fail (fallback a modo B1) si `now - tle_epoch > 30 días`.

## 7) Telemetría (para operación)
Los nodos deberían exponer localmente (log) y opcionalmente incluir en uplink (muy ocasional):
- `tle_age_days`
- `clock_age_hours` desde último fix GNSS

## 8) Referencias
- `05_Software/node_uplink_scheduler_pass_prediction.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
