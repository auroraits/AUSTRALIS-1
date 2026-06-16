# EPS Sizing — AUSTRALIS-1 / DIY Nanosat MVP (Paneles + Batería + MPPT)

**Revisión:** 2026-03-14 (incluye escenario LoRa concentrator SX1303 por especificación)
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md` §8, `08_Decisions/ADR-20260218-battery-topology-2s-flight.md`

> Nota histórica: este documento fue originalmente "MVP v1.4 — A2". El número de versión queda como referencia histórica; el contenido es vigente como guía de dimensionamiento.

## Separación de capas EPS

- Este documento de sizing aplica a las capas **Flight-Like** (`EPS_Flight_Like_2S_MPPT`) y **Flight** (`EPS_Flight_2S_MPPT`).
- El banco `EPS_Bench1_1S` (1S, sin MPPT real) sirve solo para validación funcional de firmware y power-gating. No es representativo del sizing de vuelo.
- La arquitectura de vuelo es **2S + MPPT** (bloqueada por ADR).

> Nota de modo operativo: este documento referenciaba "SCIENCE MODE" como modo de cálculo. Esa nomenclatura queda supersedada. Los cálculos de energía asociados a "SCI" corresponden a la actividad científica dentro de `MISSION_MODE = NOMINAL`. Las columnas de cálculo se mantienen por compatibilidad numérica.

## 0) Inputs fijos (del Power Budget)

### 0.1 Perfil orbital de cálculo
- Periodo: **90 min**.
- Sol / eclipse: **60 / 30 min**.

### 0.2 Casos de operación a cubrir
- Caso TÍPICO (recomendado): SAFE 80 min + DOWNLINK 10 min → **~0.381 Wh/orbita**.
- Caso SCI (sol) + SAFE (eclipse), LoRa RX single-channel: **~0.451 Wh/orbita**.
- Caso SCI (sol) + SAFE (eclipse), LoRa RX concentrator SX1303 HAT spec: **~0.516 Wh/orbita**.

### 0.3 Objetivos de diseño de potencia
- Potencia disponible en sol objetivo para el escenario sin IA activa: **≥ 1.2 W netos**.
- Target solar con payload IA activo: **TBD** hasta Gate IA-1.

## 1) Dimensionamiento de batería (Wh)

### 1.1 Requisito mínimo por eclipse
En eclipse (30 min) no hay generación solar.

Si el satélite cae a SAFE en eclipse:
- P_SAFE_avg ≈ **0.143 W**
- E_eclipse_SAFE = 0.143 W × 0.5 h = **0.0715 Wh**

SCI solo se ejecuta en sol:
- P_SCI_avg ≈ **0.379 W**
- P_SCI_avg con concentrator SX1303 HAT spec ≈ **0.444 W** (99 mA @ 5 V con GNSS ON, duty 15%, OFF real fuera de ventana)

Regla bloqueada: en eclipse, por defecto **SAFE**.

### 1.2 Requisito por picos — CONF-01 abierto

> **⚠ CONF-01 abierto:** el pico real de consumo TX UHF no está medido. Ver `architecture.md` §11 y `03_Power/Power Budget.md` §4.

La batería debe sostener:
- UHF TX pico: **~1.5 W** (estimación preliminar con η≈33%; no medido con hardware real).
- OBC + márgenes de escritura microSD simultánea.
- LoRa concentrator RX, si se adopta esa clase: **~0.495 W en RX** (SX1303 HAT spec; no medido en integración propia).

Target pico de diseño:
- **~3 W** (objetivo de diseño preliminar, no límite cerrado).
- **Peor caso plausible:** si el PA real tiene menor eficiencia, el consumo DC puede superar ~3 W. Dimensionar con margen explícito hasta tener medición real.
- **Con concentrator RX:** exigir rail switchable, OFF real fuera de ventana y no simultaneidad inicial con UHF TX/microSD hasta validar estabilidad de rails.
- **TX LoRa desde órbita:** prohibido en MVP; no dimensionar operación nominal con TX LoRa del COTS concentrator.
- **Con payload IA activo:** el objetivo arquitectónico de pico transitorio total sube a **6–7 W** (hipótesis de análisis; no medido).

### 1.3 Margen de batería
- No descargar más de 30–40% por órbita en nominal.
- Considerar degradación y cold-soak.

### 1.4 Target de capacidad
- 4 eclipses SAFE consecutivos:
  - E_4eclipses = 4 × 0.0715 = **0.286 Wh**
- Con margen ×3:
  - **Batería target ≥ 0.86 Wh**

Recomendación de diseño para 1.5U:
- **~22 Wh nominal** con referencia **2S1P, 18650 de 3.0 Ah**.
- **2S2P (~44 Wh)** queda abierta como ruta de mitigación si el power budget con payload IA y la corriente de descarga lo requieren tras medición real en Gate IA-1.

> En práctica: 2× celdas Li-ion en **serie** (2S, topología de vuelo). Ver ADR de topología de batería.

## 2) Dimensionamiento de paneles solares (W)

### 2.1 Fórmula de potencia neta disponible
\[ P_{net} = P_{EOL} \times \eta_{EPS} \]

Donde:
- **P_EOL**: potencia de paneles al End Of Life.
- **η_EPS**: eficiencia neta (MPPT + DC/DC + cableado + pérdidas), rango 0.75–0.85.

### 2.2 Restricción geométrica (1.5U)
- Cuerpo: **10×10×15 cm**.
- Caras disponibles: 4 laterales + 2 bases.

### 2.3 Modelo simple de potencia orbital
\[ E_{gen} = P_{net,sol} \times t_{sol} \]

Con t_sol = 1 h.

Para ser energy-positive:
\[ P_{net,sol} \ge E_{load/orb} / 1h \]

- Caso típico: E_load ~0.381 Wh → **P_net,sol ≥ 0.381 W**.
- Caso SCI+SAFE single-channel: E_load ~0.451 Wh → **P_net,sol ≥ 0.451 W**.
- Caso SCI+SAFE concentrator SX1303 spec: E_load ~0.516 Wh → **P_net,sol ≥ 0.516 W**.

Target bloqueado para escenario sin IA activa: **P_net,sol ≥ 1.2 W**.

> Con payload IA activo, el dimensionamiento solar actual **no está cerrado**. El target solar se declara **TBD** hasta medir consumo real del CM5 y definir el duty-cycle orbital del payload IA.

### 2.4 Heurística de paneles
Si η_EPS = 0.8:
\[ P_{EOL,sol} \ge 1.2/0.8 = 1.5 W \]

Recomendación MVP sin IA activa:
- Diseñar para **2–3 W BOL** efectivos en sol.

> Mantener abierta la opción de **deployables** o celdas más eficientes si el cierre del power budget con IA lo requiere.

## 3) MPPT vs PWM (decisión de arquitectura EPS)

### 3.1 Requisito mínimo
- Control de carga seguro para Li-ion (CC/CV), protección y medición.

### 3.2 Recomendación
- MPPT recomendado para 1.5U con downlink UHF y margen energético.
- CN3065 de banco se mantiene como cargador lineal de validación (no MPPT de vuelo).

## 4) Regulación de potencia y rails

### 4.1 Topología recomendada
- VBAT (Li-ion) → buck a 3V3_OBC always-on.
- VBAT → buck a 3V3_RF (switchable).
- VBAT → buck/boost a 5V_AUX (switchable) para GNSS.
- VBAT → rail AI dedicado power-gated (TBD en detalle de diseño).
- Si el RX orbital usa un concentrator COTS con rail 5 V, tratarlo como carga switchable del dominio RF/AUX y verificar OFF real; no extrapolar el consumo de sleep COTS como consumo aceptable de vuelo.

### 4.2 Reglas de integridad
- Separar 3V3_RF de 3V3_SCI.
- Soft-start en rails switchables.
- Medición de corriente por rail.

## 5) Sizing por corriente pico

### 5.1 Peor caso permitido
Durante DOWNLINK:
- UHF TX ON
- UHF RX ON
- OBC ON
- RF rail ON
- Science OFF

Potencia aproximada:
- DOWNLINK avg ~1.14 W
- UHF TX pico: 1.5 W

### 5.2 Target de capacidad de entrega
- Dimensionar rail RF y batería para soportar **~3 W** pico como objetivo preliminar de diseño sin IA activa.
- **CONF-01 abierto:** hasta medir el consumo DC del PA real y el consumo del payload IA, dimensionar con margen conservador. No declarar este sizing como cerrado.

## 6) Energy Balance recomendado

### 6.1 Caso típico con 1.2 W net en sol
- Energía generada: 1.2 W × 1 h = **1.2 Wh**
- Energía consumida: **~0.381 Wh**
- Margen por órbita: **~+0.819 Wh**

### 6.2 Caso SCI+SAFE con 1.2 W net
- Energía consumida single-channel: **~0.451 Wh**
- Margen por órbita single-channel: **~+0.749 Wh**
- Energía consumida concentrator SX1303 spec: **~0.516 Wh**
- Margen por órbita concentrator SX1303 spec: **~+0.684 Wh**

## 7) Reglas de operación energética
1. Eclipse = SAFE por defecto.
2. DOWNLINK solo si VBAT y SOC lo permiten.
3. microSD: preferir en sol; en eclipse solo logs críticos.
4. Payload IA solo en fase de sol, `MISSION_MODE = NOMINAL`, `EPS_STATE >= NOMINAL`.
5. LoRa RX concentrator, si se usa, opera solo en ventanas previstas, con OFF real fuera de ventana.
6. TX LoRa desde órbita permanece prohibido en el MVP.

## 8) Checklist de verificación en banco

### 8.1 Medidas mínimas
- Corriente real UHF TX (500 mW RF objetivo).
- Corriente real LoRa RX single-channel y/o concentrator candidato.
- Corriente real de sleep/off del concentrator candidate y fuga del rail con power-gating.
- Consumo OBC en sleep/run.
- Eficiencia DC/DC bajo carga real.
- Consumo CM5 en idle / activo / inferencia.

### 8.2 Prueba de robustez EPS
- Simular brownouts + resets.
- Activar TX en el peor punto de VBAT.
- Verificar no simultaneidad inicial: UHF TX vs LoRa concentrator RX vs microSD write.
- Verificar estabilidad de supervisor.
- Verificar power-gating limpio del rail AI.

## 9) Targets finales

### Batería
- Capacidad nominal objetivo de referencia: **~22 Wh**.
- Configuración base: **2S1P con 18650 de 3.0 Ah**.
- Ruta de mitigación: **2S2P (~44 Wh)** si el power budget con IA lo exige.
- Topología de batería de vuelo: **2S** (decisión bloqueada).

### Solar
- P_net en sol objetivo sin IA activa: **≥1.2 W**.
- P_EOL en sol objetivo sin IA activa: **≥1.5–2.0 W**.
- Target solar con payload IA activo: **TBD**.

### EPS
- MPPT recomendado.
- Rails medidos + switchables.
- Pico máximo soportable: **~3 W** sin IA activa; cierre con IA pendiente por `CONF-01` y Gate IA-1.

---

**FIN — EPS Sizing A2 (actualizado 2026-03-14)**

## 10) Framework permanente de power-gating y health
- Diseño EPS preparado para control selectivo `EN_x` por subsistema.
- Señales mínimas para FaultManager: `PGOOD_x`, `FAULT_x`, `HB_x` y contadores de fault/reset.
- Requisito de aislamiento: cualquier subsistema no-crítico debe poder apagarse sin comprometer SAFE.

<!-- FEATURE:PHOTO_DEMO START -->

## 11) [PHOTO_DEMO] Carga opcional encapsulada
- [PHOTO_DEMO] no modifica sizing base del MVP 2.2; usa cuota energética best-effort.
- Presupuesto de potencia por ventana: **TBD** con límite configurable y lockout por fault.
- Remoción del feature no requiere cambio en topología base EPS 2S.

<!-- FEATURE:PHOTO_DEMO END -->
