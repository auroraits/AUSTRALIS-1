# EPS Bench 1 – 1S Architecture

**Review date:** 2026-02-18
**Scope:** Banco de pruebas EPS 1S (validación funcional, no vuelo)
**Estado documental:** snapshot histórico.

> Fuente canónica vigente para EPS Bench1 1S: `03_Power/EPS_Bench1_1S.md` (rev 2026-02-27 o superior).
> Este archivo se conserva por trazabilidad y no debe usarse como fuente única para baseline.

## Objetivo
Banco funcional para validar:
- Carga solar.
- Protección de batería.
- Generación de +5V.
- Generación de +3V3.
- Separación de buses.
- Telemetría futura.

## Strategy: COTS for Validation → Custom Flight PCB
- Para banco de pruebas se utilizan módulos COTS comerciales, económicos y disponibles.
- Cada módulo COTS debe preservar la topología arquitectónica del EPS objetivo.
- El banco no es el diseño final de vuelo, sino una plataforma de validación funcional y de integración.
- Cada módulo COTS deberá mapearse posteriormente a:
  - IC equivalente.
  - Topología eléctrica equivalente.
  - Versión discreta o integrada para PCB custom.

## Arquitectura General
```text
PV Panels (paralelo)
    ↓
Schottky (1N5817)
    ↓
Fuse 1A
    ↓
CN3065 (Solar charger 1S)
    ↓
BMS 1S (protección)
    ↓
Boost 5V
    ↓
Buck 3V3
```

## Bloques utilizados

### Solar Charger
- **Modelo:** CN3065.
- **Modo:** 1S Li-ion.
- **Uso:** Solo banco (NO MPPT real).

Notas de conexión:
- `Solar+` y `Solar−` desde paneles.
- `Batt+` y `Batt−` conectados a `P+` / `P−` del BMS.
- `C6 = 10uF` en entrada solar.
- Capacitor `100nF` cercano al módulo.

### BMS 1S 5A
Conexiones:
- `B+` → Batería `+`.
- `B−` → Batería `−`.
- `P+` → Entrada/salida protegida (hacia cargador y boost).
- `P−` → Retorno protegido.

Regla obligatoria de integración:
- El cargador **NO** debe conectarse directo a la batería.
- Debe conectarse al lado `P+`/`P−` del BMS para que la protección (OVP/UVP/OCP) sea efectiva también durante carga/descarga.

### Boost 5V
- **Entrada:** desde `P+` / `P−` (salida protegida del BMS).
- **Salida:** `+5V_BUS`.
- `C5 = 470uF`.
- `C8 = 100nF`.

### Buck 3V3
- **Entrada:** desde `+5V_BUS`.
- **Salida:** `+3V3_BUS`.
- `C4 = 470uF`.
- `C7 = 100nF`.

## Arquitectura de protección (BMS)
### Diferencia entre B+/B− vs P+/P−
- `B+` / `B−`: terminales directos de celda; sin desacople funcional de las cargas del sistema.
- `P+` / `P−`: lado protegido por el BMS; punto correcto para intercambio energético del sistema.

### Criterio técnico
- Cargador y cargas deben conectarse sobre `P+`/`P−`.
- Nunca se debe cablear cargador o cargas en paralelo directo sobre la celda (`B+`/`B−`) porque se pierde cobertura de protección en escenarios de falla.

### Diagrama conceptual ASCII
```text
       +-----------------------------+
PV --->| CN3065 charger              |
       | Batt+  Batt-                |
       +----|------|-----------------+
            |      |
            v      v
         P+ o------o P-    (lado protegido del BMS, I/O del sistema)
            |      |
     +------+      +------------------+
     |                                |
 +---v---+                        +---v---+
 | Boost |--> +5V_BUS ----------->| Buck  |--> +3V3_BUS
 +-------+                        +-------+

         BMS 1S protection board
           B+ o---------------> Batería +
           B- o---------------> Batería -
```

## Limitaciones del banco
- CN3065 no es MPPT real.
- No hay control térmico activo.
- No hay redundancia.
- No hay balanceo activo.
- No hay telemetría integrada aún.
- No es diseño espacial ni flight-qualified.

## Migration Plan: Fritzing → KiCad
En la PCB custom de evolución:
- CN3065 será reemplazado por cargador buck solar real.
- BMS será integrado en la PCB.
- Boost/Buck migrarán a IC dedicados.
- Se eliminarán módulos enchufables.

### Roadmap EPS asociado
1. `EPS_Bench1_1S` (actual, banco funcional COTS).
2. `EPS_Flight_Like` (KiCad, integración por IC y telemetría de potencia).
3. `EPS_Flight` (calificación, validación ambiental y márgenes de misión).
