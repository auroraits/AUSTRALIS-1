# Power Budget — AUSTRALIS-1 / DIY Nanosat MVP

**Revisión:** 2026-03-14 (corrección SCI 0.371→0.451 Wh; escenario AI payload experimental; escenario LoRa concentrator SX1303 por especificación)
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md` §8, `08_Decisions/ADR-20260218-battery-topology-2s-flight.md`

> Nota histórica: este documento fue originalmente "MVP v1.4 — Power Budget". El número de versión queda como referencia histórica; el contenido es vigente.

> Nota de modo operativo: la columna `duty_sci` y la sección "SCIENCE MODE" en este documento son de cálculo histórico. La nomenclatura canónica es `MISSION_MODE = NOMINAL` con actividad científica como actividad interna. No se cambian los números unitarios; solo se reexpresa la denominación.

## Hardware Strategy Policy (COTS-to-Flight)
- All bench prototypes will use commercially available, low-cost COTS (Commercial Off-The-Shelf) modules whenever possible.
- These COTS components must always reflect the architectural principles required for the final flight hardware.
- Bench hardware selections are not final flight components but must:
  - Respect the same voltage topology (e.g., 2S vs 1S decisions).
  - Follow the same MPPT vs linear charging philosophy.
  - Preserve battery chemistry and cell configuration decisions.
  - Maintain realistic current and power margins.
- Every COTS module selected must be evaluated as:
  1) Bench-valid
  2) Architecture-aligned
  3) Replaceable by custom flight-grade PCB in later phases.

### Component Selection Rule
- Every component recommendation must include:
  - Bench Option (COTS)
  - Flight Architecture Equivalent
  - Migration Path

Política COTS-to-Flight: ver sección específica en `architecture.md`. Este documento define únicamente el presupuesto de potencia y sus reglas operativas.

## 0) Convenciones y supuestos

### 0.1 Unidades
- Potencia en **W**.
- Energía en **Wh/orbita**.

### 0.2 Perfil orbital para cálculo
- **Periodo orbital:** 90 min.
- **Iluminación:** 60 min sol / 30 min eclipse.

### 0.3 Política operativa bloqueada
- **SCI opera exclusivamente en fase de sol; en eclipse la política es SAFE por defecto.**

## 1) Tabla de cargas por bloque (MVP vigente)

| Bloque | Rail | Potencia (W) | Notas |
|---|---|---:|---|
| OBC (STM32L4 run) | 3V3_OBC | 0.10 | CPU activa moderada |
| OBC (sleep) | 3V3_OBC | 0.02 | RTC + low-power |
| SPI NOR write | 3V3_OBC | 0.05 | picos breves |
| microSD write | 3V3_OBC | 0.30 | picos; evitar en eclipse |
| LoRa RX 915 MHz (single-channel SX126x/SX127x class) | 3V3_RF | 0.06 | RX durante ventana; referencia simple/degradada |
| LoRa RX 915 MHz (concentrator SX1303 HAT class) | 3V3_RF/5V | 0.495 | Escenario de especificación COTS: 99 mA @ 5 V con GNSS ON. Requiere rail switchable y OFF real fuera de ventana. No es hardware de vuelo seleccionado. |
| UHF RX 435 MHz | 3V3_RF | 0.15 | ACK/NACK |
| UHF TX 435 MHz | 3V3_RF/5V | 1.50 | **eléctrico** (500 mW RF obj., PA η≈33%); medir en banco |
| GNSS-A | 3V3/5V_AUX | 0.10 | best-effort; duty-cycle |
| Science I2C (UV+ALS+MAG+temps) | 3V3_SCI | 0.05 | sensores I2C; sin HV en MVP |

## 2) Potencia promedio por modo

### 2.1 SAFE MODE
- OBC: 20% run / 80% sleep → 0.10×0.20 + 0.02×0.80 = **0.036 W**
- UHF TX: 4% → 1.50×0.04 = **0.060 W**
- UHF RX: 3% → 0.15×0.03 = **0.005 W**
- GNSS: 20% → 0.10×0.20 = **0.020 W**
- Otros (storage mínimo, márgenes): **0.022 W**

**SAFE avg: 0.143 W** (objetivo ≤0.20 W)

### 2.2 Actividad científica en NOMINAL (solo en sol)
> Nota: denominado "SCIENCE MODE" en versiones anteriores. La nomenclatura canónica es `MISSION_MODE = NOMINAL` con actividad científica activa.
- OBC: 100% run → **0.100 W**
- SCI I2C sensors: 100% → **0.050 W**
- LoRa RX: 15% (ventanas)
  - Single-channel SX126x/SX127x class: 0.06×0.15 = **0.009 W**
  - Concentrator SX1303 HAT class: 0.495×0.15 = **0.074 W** (escenario de especificación; OFF real fuera de ventana)
- UHF TX beacon+summary: 8% → 1.50×0.08 = **0.120 W**
- GNSS: 20% → 0.10×0.20 = **0.020 W**
- Margen storage/otros: **0.080 W**

**SCIENCE avg (single-channel): 0.379 W** (objetivo ≤0.5 W)
**SCIENCE avg (concentrator SX1303 spec): 0.444 W** (escenario de sizing preliminar; objetivo ≤0.5 W)

### 2.3 DOWNLINK WINDOW (ventana 10 min dentro de la órbita)
- OBC run: **0.10 W**
- UHF TX: 1.5 W a 60% duty → **0.90 W**
- UHF RX: 0.15 W a 60% duty → **0.09 W**
- Otros: **0.05 W**

**DOWNLINK window avg: 1.14 W**

## 3) Energía por órbita (perfil 90 min)

### 3.1 Caso típico: SAFE 80 min + DOWNLINK 10 min
- SAFE: 0.143 W × (80/60) h = **~0.191 Wh**
- DOWNLINK: 1.14 W × (10/60) h = **~0.190 Wh**

**Total: ~0.381 Wh/orbita**

### 3.2 Caso NOMINAL con ciencia (sol) + SAFE (eclipse)
> Denominado "Caso SCI" en cálculos históricos. Corresponde a `MISSION_MODE = NOMINAL` con actividad científica en sol + `MISSION_MODE = SAFE` en eclipse.
- Actividad científica en NOMINAL, sol (60 min):
  - single-channel: 0.379 W × 1 h = **0.379 Wh**
  - concentrator SX1303 spec: 0.444 W × 1 h = **0.444 Wh**
- SAFE en eclipse (30 min): 0.143 W × 0.5 h = **~0.072 Wh**

**Perfil operativo bloqueado (single-channel): ~0.451 Wh/orbita**
**Perfil operativo con concentrator SX1303 spec: ~0.516 Wh/orbita**

> **Corrección 2026-03-14:** total SCI+SAFE corregido de **0.371** a **0.451 Wh**; el error previo provenía de un `P_SCI` desincronizado (**0.299 W** vs **0.379 W**).

## 4) Pico soportable EPS — CONF-01 abierto

> **⚠ CONF-01 abierto:** el pico de potencia EPS está en conflicto. Ver `architecture.md` §11.

- **Objetivo de diseño preliminar sin payload IA: ~3 W** (UHF TX eléctrico ~1.5 W + OBC + escritura microSD + margen).
- **Peor caso plausible (no medido):** si el PA UHF real opera con eficiencia menor a η≈33%, el consumo DC puede superar los 3 W. Estimaciones de análisis preliminar sitúan el rango potencial en ~4–5 W DC según la solución de PA final.
- **Con payload IA activo:** el objetivo arquitectónico de pico transitorio total asciende a **6–7 W** (hipótesis de análisis; **no medido**). Esto contempla la sumatoria de la carga existente más el CM5 en inferencia.
- **Con LoRa concentrator RX:** el escenario SX1303 HAT agrega ~0.495 W durante RX. No cierra hardware de vuelo; exige medición de banco, power-gating OFF real y política de no simultaneidad con UHF TX/microSD hasta validar rails.
- **TX LoRa desde órbita sigue prohibido en MVP.** El caso de TX del COTS concentrator no forma parte del CONOPS; specs COTS reportan consumos de orden ~3.55 W y no deben incorporarse como operación nominal.
- **El payload IA no opera de forma continua.** Solo en ventanas experimentales en fase de sol. El EPS no necesita soportar 6–7 W de forma sostenida.
- **Este presupuesto NO está cerrado respecto al pico TX ni al pico IA.** No declarar como cerrado hasta medición real de hardware.
- Cierre de CONF-01: medición en banco con hardware PA/TTC UHF candidato (Gate C / Gate D) + medición de consumo CM5 (Gate IA-1).

## 4.1) Escenario AI payload experimental (sin valores cerrados)

> Todos los valores de esta sección son **hipótesis de análisis / TBD**. No existe medición real. No usar como presupuesto de diseño cerrado.

| Escenario | Potencia AI payload (hipótesis) | Notas |
|---|---|---|
| IA idle (CM5 encendido, sin inferencia) | TBD | Depende de configuración Linux + RAM activa. |
| IA activo (procesando contexto) | TBD | Depende de carga de CPU y modelo cargado. |
| IA inference burst (inferencia activa INT4) | TBD | Pico máximo esperado; duración breve. |

**Objetivo arquitectónico de pico transitorio total (hipótesis):** 6–7 W.
**Operación continua del payload IA: NO asumida.**
**Duración operativa por órbita: TBD.**

El EPS deberá contemplar este pico como objetivo de arquitectura para las fases de diseño del rail AI, **sin cerrarlo como requisito hasta tener medición real** (Gate IA-1).

## 5) Requerimiento solar (dimensionamiento inicial)
- Caso típico: 0.381 Wh / 1.5h = 0.254 W avg → **P_solar_req ≥ 0.381 W** → target **≥1.2 W**.
- Caso SCI single-channel: 0.451 Wh / 1.5h = 0.301 W avg → **P_solar_req ≥ 0.451 W** → target **≥1.2 W**.
- Caso SCI con concentrator SX1303 spec: 0.516 Wh / 1.5h = 0.344 W avg → **P_solar_req ≥ 0.516 W** → target **≥1.2 W**.

**Conclusión:** el target **≥1.2 W netos en sol** sigue holgado para el escenario **sin payload IA activo**.

> Con payload IA activo, el target solar queda **TBD** — pendiente de medición de consumo real del CM5 y definición del duty-cycle orbital en Gate IA-1. La opción de deployables o celdas más eficientes queda abierta como ruta de mitigación.

## 6) Política de gobernanza energética

### 6.1 Estados de energía

| Alias histórico | EPS_STATE canónico | Política |
|---|---|---|
| `E0` | `CRIT` | SAFE estricto; degrada `MISSION_MODE` a `SAFE`; solo housekeeping mínimo y `COMMAND_ACK`; payload IA OFF. |
| `E1` | `LOW` | SAFE por defecto; GNSS OFF; sin dumps; sin actividad científica; payload IA OFF. |
| `E2` | `NOMINAL` | Actividad científica y LoRa RX permitidos; downlink estándar; payload IA permitido solo en ventana experimental de sol. |
| `E3` | `HIGH` | Downlink window extendido; payload IA con ventana ampliada si condiciones lo permiten. |

### 6.2 Reglas automáticas
- Downlink solo si SOC estimado suficiente y elevación favorable.
- LoRa RX en ventanas de pasada.
- microSD writes: preferir en sol, evitar en eclipse.
- `EPS_STATE = CRIT` fuerza `MISSION_MODE = SAFE` sin excepción.
- `EPS_STATE = LOW` mantiene `SAFE` por defecto; `NOMINAL` solo para housekeeping esencial.

## 7) CSV exportable

```csv
block,rail,power_W,duty_safe,duty_sci,duty_dl,notes
AI Payload CM5 idle,AI_RAIL,TBD,0.00,TBD,0.00,rail dedicado power-gated; valores TBD hasta Gate IA-1
AI Payload CM5 inference,AI_RAIL,TBD,0.00,TBD,0.00,pico burst breve; solo en ventana experimental sol
OBC run,3V3_OBC,0.10,0.20,1.00,1.00,CPU activa moderada
OBC sleep,3V3_OBC,0.02,0.80,0.00,0.00,RTC + low-power
SPI NOR write,3V3_OBC,0.05,0.00,0.00,0.00,picos breves
microSD write,3V3_OBC,0.30,0.00,0.00,0.00,picos; evitar en eclipse
LoRa RX 915 MHz single-channel,3V3_RF,0.06,0.00,0.15,0.00,RX durante ventana; referencia simple/degradada
LoRa RX 915 MHz concentrator SX1303 HAT,3V3_RF/5V,0.495,0.00,0.15,0.00,"escenario spec COTS: 99 mA @ 5 V con GNSS ON; requiere OFF real"
UHF RX 435 MHz,3V3_RF,0.15,0.03,0.00,0.60,ACK/NACK
UHF TX 435 MHz,3V3_RF/5V,1.50,0.04,0.08,0.60,eléctrico (500 mW RF obj., PA η≈33%)
GNSS-A,3V3/5V_AUX,0.10,0.20,0.20,0.00,best-effort; duty-cycle
Science I2C (UV+ALS+MAG+temps),3V3_SCI,0.05,0.00,1.00,0.00,sensores I2C; sin HV en MVP
```
