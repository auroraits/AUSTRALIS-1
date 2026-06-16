# Node Uplink Scheduler — Predicción de pasadas offline (ESP32)

**Fecha de revisión:** 2026-02-20
**Estado:** propuesta (P1)

## 1) Objetivo
Permitir que nodos “típicos” (ESP32 + RFM95W) transmitan solo cuando el satélite esté en una geometría favorable (elevación alta), sin depender de NTP.

## 2) Supuestos
- Nodo tiene ESP32.
- Nodo tiene RTC (o la hora del ESP32) y puede disciplinarlo con **GNSS 1 vez/día** (aceptable).
- Nodo conoce su ubicación (lat/lon) por GNSS (ocasional) o configuración inicial.
- Nodo tiene acceso (alguna vez) a un **TLE** del satélite (o de un satélite de prueba) cargado manualmente o por internet cuando esté disponible.

## 3) Algoritmo propuesto
### 3.1 Inputs
- `TLE` (2 líneas)
- `site_lat`, `site_lon`, `site_alt`
- `t_now_utc` (desde RTC/GNSS)
- Umbral de elevación `el_min` (baseline sugerido: 30°)

### 3.2 Propagación
- Usar propagador estándar **SGP4**.
- Calcular posición/velocidad del satélite y vector de observación desde el sitio.
- Convertir a coordenadas topocéntricas (az/el/range).

### 3.3 Detección de pasadas
- Escanear el día (o próximas 24–48 h) con paso grueso (ej. 10–30 s).
- Detectar cruces de elevación `el_min` (inicio/fin de ventana útil).
- Refinar el máximo (TCA / max elevación) con búsqueda local.

### 3.4 Ventana de transmisión
- Definir ventana centrada en `t_peak` (máxima elevación): baseline 6 min total.
- Dentro de la ventana, aplicar slotting determinístico (modo B).

## 4) Actualización de TLE (operación)
- Para buena predicción, el TLE debe actualizarse con frecuencia (ideal cada pocos días; depende de órbita/drag).
- Mecanismos posibles (sin satélite):
  - WiFi cuando haya red disponible,
  - carga manual (archivo/config),
  - app móvil/PC que empuje TLE por BLE/Serial.

## 5) Fallos y degradación
- Si no hay TLE válido o hora válida → fallback a B1 (always-on slotted) con periodo bajo para limitar colisiones.

## 6) Referencias
- `04_Communications/uplink_lora_slotted_protocol.md`
- `01_Mission/mission_definition.md`
