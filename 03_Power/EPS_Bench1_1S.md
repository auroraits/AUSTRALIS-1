# EPS Bench1 1S - Documentacion Tecnica

**Revision:** 2026-04-03
**Estado:** Active - Bench Only
**Trazabilidad:** `08_Decisions/ADR-20260218-eps-bench1s-cots-to-custom-flight-pcb.md`, `08_Decisions/ADR-20260313-eps-separacion-bench-flightlike-flight.md`, `08_Decisions/ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`
**Scope:** `EPS_Bench1_1S` extendido para Gate IA-2: FPM bench + rail IA bench-only + inyeccion externa de 5V para CM5 real
**Archivo de diseño:** artefacto Fritzing legacy removido del árbol público; ver `03_Power/EPS_PCB/EPS_Bench1S/README.md`.

---

> **IMPORTANTE - SEPARACION DE CAPAS EPS**
>
> Este documento describe exclusivamente el banco `EPS_Bench1_1S`: hardware COTS 1S de validacion funcional. **No es hardware de vuelo.**
>
> Las capas superiores siguen siendo:
> - `EPS_Flight_Like_2S_MPPT`: PCB custom KiCad, 2S + MPPT, no calificado.
> - `EPS_Flight_2S_MPPT`: hardware final de vuelo, 2S + MPPT, TBD.
>
> La extension del bench para Gate IA-2 **no** convierte al banco en flight-like y **no** modifica el baseline de vuelo 2S + MPPT.

---

## 1) Objetivo

`EPS_Bench1_1S` se redefine como banco extendido para Gate IA-2 con dos alcances simultaneos:

1. Mantener la cadena bench 1S existente para validacion funcional de EPS:
   - paneles
   - CN3065
   - BMS 1S
   - boost `5V_AUX`
   - buck `3V3_OBC`
   - cargas dummy
   - Arduino Nano como MCU/FPM del bench
2. Agregar una rama IA separada de potencia, **solo banco**, para integrar un CM5 real sobre carrier board COTS externa usando inyeccion externa de 5V.

El objetivo del agregado IA es cerrar Gate IA-2 en banco para:
- secuenciamiento
- FPM
- logging
- heartbeat
- boot
- kill/reset
- consumo
- termica basica

Este banco **no** debe describirse como si la cadena 1S existente alimentara al CM5 de forma representativa de vuelo. El rail IA bench-only usa `5V_AI_EXT` externo y no valida el rail IA de `EPS_Flight_Like_2S_MPPT`.

---

## 2) Arquitectura bench extendida

### 2.1 Capas y limites

| Capa | Nombre | Proposito |
|---|---|---|
| Bench | `EPS_Bench1_1S` | Validacion funcional COTS 1S. Incluye FPM bench y rail IA bench-only para Gate IA-2. |
| Flight-Like | `EPS_Flight_Like_2S_MPPT` | PCB custom 2S + MPPT con rail IA integrado TBD. |
| Flight | `EPS_Flight_2S_MPPT` | Hardware de vuelo calificado. |

### 2.2 Diagrama de bloques funcional

```text
PV1/PV2 -> D1/D2 -> F1 -> INA219_SOLAR -> CN3065 -> BMS 1S -> RBF -> VBAT_PROT+
                                                            |
                                                            +-> Boost -> 5V_AUX -> Buck -> 3V3_OBC
                                                            |                     |
                                                            |                     +-> OBC_CORE (always-on)
                                                            |                     +-> SCI_3V3 gate -> 3V3_SCI_SW
                                                            |
                                                            +-> LOAD_5V gate -> 5V_LOAD_SW
                                                            |
                                                            +-> Arduino Nano (MCU/FPM bench)

J_AI_PWR (5V_AI_EXT,GND_AI) -> F_AI -> SW_AI -> 5V_AI_SW -> harness -> carrier board COTS externa -> CM5 real
                                               |
                                               +-> 5V_AI_SENSE
                                               +-> PGOOD_AI / FAULT_AI / HB_AI / AI_BOOT_OK / AI_THERM / AI_UART / AI_KILL_N
```

### 2.3 Rails del bench

| Rail / Net | Origen | Tipo | Estado | Uso |
|---|---|---|---|---|
| `VBAT_PROT+` | BMS P+ via RBF | Bus protegido 1S | Always-on con RBF | Distribucion bench 1S |
| `5V_AUX` | Boost desde `VBAT_PROT+` | 5V regulado | Always-on | MCU/FPM bench y cargas 5V |
| `3V3_OBC` | Buck desde `5V_AUX` | 3V3 regulado | Always-on | OBC core bench e I2C |
| `5V_LOAD_SW` | Gate desde `5V_AUX` | 5V switchable | FPM bench | Carga dummy / `LOAD_5V` |
| `3V3_SCI_SW` | Gate desde `3V3_OBC` | 3V3 switchable | FPM bench | Carga dummy / `SCI_3V3` |
| `5V_AI_EXT` | Fuente externa por `J_AI_PWR` | 5V bench-only | Externo | Alimentacion principal del CM5 real en banco |
| `5V_AI_SW` | `SW_AI` desde `5V_AI_EXT` | 5V switchable | FPM bench | Rail IA bench-only hacia carrier board |
| `5V_AI_SENSE` | Derivacion de sensado de `5V_AI_SW` | Sense | Bench-only | Telemetria de presencia/caida de rail IA |

### 2.4 Rama IA bench-only

La rama IA agregada al bench se define como:

```text
J_AI_PWR -> 5V_AI_EXT -> F_AI -> SW_AI -> 5V_AI_SW -> harness -> carrier board COTS externa -> CM5 real
                                              |
                                              +-> 5V_AI_SENSE
```

Reglas obligatorias:
- El rail IA es **bench-only**.
- La potencia principal del rail IA entra por `J_AI_PWR`.
- `JP1` es **solo** para control, sensado y telemetria.
- La potencia principal del rail IA **no** debe rutearse por `JP1`.
- El switch principal `SW_AI` queda como componente bench-only de alta corriente con MPN final **TBD**.
- `TPS22918` puede aparecer como referencia de familia, pero **no** queda congelado como switch final del rail IA.

---

## 3) Fault/Power Manager (FPM) bench

### 3.1 Subsistemas supervisados

| Subsistema | Enable / Control | Health minima | Contadores |
|---|---|---|---|
| `OBC_CORE` | `OBC_RST_N` | `OBC_HB`, `PGOOD_3V3` | `reset_count_OBC`, `fault_count_OBC` |
| `LOAD_5V` | `EN_5V` | Telemetria de rail y corriente dummy | `fault_count_OBC` si afecta bus controlado |
| `SCI_3V3` | `EN_SCI` | `PGOOD_3V3` + estado de switch | `fault_count_OBC` si afecta bus controlado |
| `AI_PAYLOAD` | `EN_AI`, `AI_KILL_N` | `PGOOD_AI`, `FAULT_AI`, `HB_AI`, `AI_BOOT_OK`, `AI_THERM`, `5V_AI_SENSE` | `fault_count_AI` |

### 3.2 Senales bench del FPM

Senales ya existentes:
- `EN_5V`
- `EN_SCI`
- `OBC_HB`
- `OBC_RST_N`
- `PGOOD_3V3`

Senales nuevas para la rama IA bench-only:
- `EN_AI`
- `PGOOD_AI`
- `FAULT_AI`
- `HB_AI`
- `AI_KILL_N`
- `AI_BOOT_OK`
- `AI_UART_TX`
- `AI_UART_RX`
- `AI_THERM`
- `5V_AI_SENSE`

### 3.3 Logica bench del FPM

Logica minima documentada para el bench:
1. deteccion de anomalia
2. apagado inmediato del subsistema afectado
3. `1-3` reintentos configurables
4. lockout hasta `POWER_SET`, `ABORT`, accion bench-local `CLEAR_LOCKOUT` o timeout

Notas:
- `PGOOD_AI` y `FAULT_AI` pueden ser sinteticos por firmware mientras no exista supervisor dedicado en la rama IA del bench.
- `PGOOD_3V3` se mantiene con el workaround actual: jumper/supervisor futuro segun lo ya documentado.
- `CLEAR_LOCKOUT` se documenta aqui como accion local de banco; no cambia por si sola el set minimo canonico de comandos de vuelo.

---

## 4) Netlist e interfaces

### 4.1 Nets de potencia

| Net | Descripcion | Origen | Destino(s) |
|---|---|---|---|
| `SOLAR_RAW+` | OR-ing paneles | D1/D2 | `F1` |
| `SOLAR_FUSED+` | Solar post-fusible | `F1` | `INA219_SOLAR` |
| `SOLAR_SENSED+` | Solar post-sensado | `INA219_SOLAR` | `CN3065` |
| `VBAT_PROT+` | Bus 1S protegido | BMS P+ via RBF | Boost, divisores y sensado bench |
| `5V_AUX` | Rail 5V always-on | Boost 1S | Buck 3V3, MCU/FPM bench, `LOAD_5V` gate |
| `3V3_OBC` | Rail 3V3 always-on | Buck desde `5V_AUX` | Bus OBC/I2C, `SCI_3V3` gate |
| `5V_LOAD_SW` | Rail 5V conmutado | Gate 5V | Carga dummy 5V |
| `3V3_SCI_SW` | Rail 3V3 conmutado | Gate 3V3 | Carga dummy 3V3 |
| `5V_AI_EXT` | Entrada externa 5V | `J_AI_PWR` pin 1 | `F_AI` |
| `GND_AI` | Retorno rama IA | `J_AI_PWR` pin 2 | Carrier board / referencia de sensado |
| `5V_AI_SW` | Rail IA bench-only conmutado | `SW_AI` | Harness hacia carrier board COTS externa |
| `5V_AI_SENSE` | Sense de rail IA | Derivacion de `5V_AI_SW` | FPM bench / `JP1` |

### 4.2 Nets de control y telemetria

| Net | Tipo | Direccion | Descripcion |
|---|---|---|---|
| `VBAT_SENSE` | Analogica | Input FPM | Divisor de bateria 1S |
| `OBC_I2C_SDA` | I2C | Bidir | Sensado bench y futura integracion |
| `OBC_I2C_SCL` | I2C | Bidir | Sensado bench y futura integracion |
| `OBC_HB` | Digital | Input FPM | Heartbeat OBC |
| `OBC_RST_N` | Digital | Output FPM | Reset activo-bajo al OBC bench |
| `EN_5V` | Digital | Output FPM | Enable de `5V_LOAD_SW` |
| `EN_SCI` | Digital | Output FPM | Enable de `3V3_SCI_SW` |
| `PGOOD_3V3` | Digital | Input FPM | Power-good 3V3 bench |
| `EN_AI` | Digital | Output FPM | Enable de `SW_AI` |
| `PGOOD_AI` | Digital | Input FPM | Power-good IA bench, real o sintetico |
| `FAULT_AI` | Digital | Input FPM | Fault IA bench, real o sintetico |
| `HB_AI` | Digital | Input FPM | Heartbeat fisico separado del CM5 |
| `AI_KILL_N` | Digital | Output FPM | Kill/reset de emergencia hacia la rama IA |
| `AI_BOOT_OK` | Digital | Input FPM | Indicacion de boot operativo del CM5 |
| `AI_UART_TX` | Digital | Input FPM | TX desde AI hacia FPM/OBC |
| `AI_UART_RX` | Digital | Output FPM | RX hacia AI |
| `AI_THERM` | Analogica / sensor | Input FPM | Telemetria termica basica del CM5 |
| `5V_AI_SENSE` | Analogica | Input FPM | Sense del rail IA bench-only |

### 4.3 `JP1` - header 2x12 / 24 pines

`JP1` se redefine como header de control/sense/telemetria. **No** transporta la potencia principal del rail IA.

| Pin | Net | Descripcion |
|---|---|---|
| 1 | `3V3_OBC` | Rail 3V3 always-on |
| 2 | `GND` | Tierra |
| 3 | `5V_AUX` | Rail 5V always-on |
| 4 | `GND` | Tierra |
| 5 | `OBC_I2C_SDA` | I2C SDA |
| 6 | `OBC_I2C_SCL` | I2C SCL |
| 7 | `OBC_HB` | Heartbeat OBC |
| 8 | `OBC_RST_N` | Reset hacia OBC |
| 9 | `VBAT_SENSE` | Sentido de bateria |
| 10 | `PGOOD_3V3` | Power-good 3V3 bench |
| 11 | `EN_AI` | Enable rail IA bench-only |
| 12 | `PGOOD_AI` | Power-good IA |
| 13 | `FAULT_AI` | Fault IA |
| 14 | `HB_AI` | Heartbeat IA |
| 15 | `AI_KILL_N` | Kill/reset IA |
| 16 | `AI_BOOT_OK` | Boot OK IA |
| 17 | `AI_UART_TX` | UART TX desde AI |
| 18 | `AI_UART_RX` | UART RX hacia AI |
| 19 | `5V_AI_SENSE` | Sense de rail IA |
| 20 | `AI_THERM` | Telemetria termica IA |
| 21 | `SPARE` | Reserva bench |
| 22 | `GND` | Tierra |
| 23 | `SPARE` | Reserva bench |
| 24 | `GND` | Tierra |

### 4.4 `J_AI_PWR` - conector de potencia principal IA

| Pin | Net | Descripcion |
|---|---|---|
| 1 | `5V_AI_EXT` | Entrada principal 5V externa |
| 2 | `GND_AI` | Retorno principal de la rama IA |

---

## 5) Integracion CM5 en banco

### 5.1 Interfaz CM5 / bench

La integracion de Gate IA-2 en banco usa:
- CM5 real sobre carrier board COTS externa
- alimentacion principal por inyeccion externa de 5V via `J_AI_PWR`
- harness dedicado entre el bench y la carrier board
- UART como interfaz primaria de banco
- adaptacion de niveles si corresponde
- `HB_AI` como linea fisica separada
- `AI_BOOT_OK` como linea fisica separada
- `AI_THERM` como telemetria termica basica del CM5

Esta configuracion valida integracion de banco y FPM, pero **no** valida el rail IA de vuelo 2S + MPPT.

### 5.2 Secuenciamiento documentado del CM5

**Encendido**
1. `SW_AI` habilita `5V_AI_SW`
2. validar `PGOOD_AI`
3. habilitar/controlar la interfaz hacia el CM5
4. generar pulso de encendido si corresponde
5. esperar `AI_BOOT_OK`
6. exigir `HB_AI`

**Apagado normal**
1. pedir shutdown logico
2. esperar caida de `HB_AI` o timeout
3. cortar `SW_AI`

**Apagado de emergencia**
1. afirmar `AI_KILL_N`
2. esperar timeout corto
3. cortar `SW_AI`

---

## 6) Telemetria y sensado

### 6.1 Sensado bench existente

| Canal | Implementacion | Estado |
|---|---|---|
| Solar | `INA219_SOLAR` | Activo en bench |
| Carga 1S bench | `INA219_LOAD` | Activo en bench |
| `VBAT_SENSE` | Divisor resistivo + ADC | Activo en bench |
| `PGOOD_3V3` | Workaround con jumper o supervisor futuro | Parcial / workaround |

### 6.2 Sensado de la rama IA

| Canal | Implementacion | Estado |
|---|---|---|
| `5V_AI_SENSE` | Sense dedicado del rail IA conmutado | Documentado para bench |
| `AI_THERM` | Sensor o sonda termica basica en CM5 | Bench-only |
| Corriente principal CM5 | Metrologia externa de banco o instrumentacion dedicada | Requerida para T20 |
| `PGOOD_AI` / `FAULT_AI` | Supervisor dedicado o firmware sintetico | TBD / bench-only |

**Nota de metrologia:** un `INA219` extra en serie con el rail principal del CM5 puede usarse solo como `bench option`. Si la caida en el shunt compromete boot o estabilidad del CM5, la alternativa valida es metrologia externa de banco. No se congela un sensado inline como arquitectura final.

---

## 7) BOM bench relevante

### 7.1 Cadena bench 1S preservada

| Ref / Item | Funcion | Capa |
|---|---|---|
| CN3065 | Carga solar 1S | Bench |
| BMS 1S | Proteccion de celda | Bench |
| Boost `5V_AUX` | Rail 5V always-on | Bench |
| Buck `3V3_OBC` | Rail 3V3 always-on | Bench |
| 2x INA219 | Solar y load bench | Bench |
| Arduino Nano | MCU/FPM bench | Bench |
| Power gates 5V / 3V3 | `LOAD_5V` y `SCI_3V3` | Bench |

### 7.2 Delta bench-only para Gate IA-2

| Item | Funcion | Estado |
|---|---|---|
| `J_AI_PWR` | Entrada principal 5V externa del rail IA | Bench-only |
| Harness 5V / control hacia carrier board | Interconexion banco <-> CM5 real | Bench-only |
| `F_AI` | Proteccion del rail IA | Bench-only |
| `SW_AI` | Switch / eFuse / load switch de alta corriente | **TBD** |
| Carrier board COTS externa para CM5 | Soporte de CM5 real en banco | Bench-only |
| Adaptacion de niveles UART / interfaz | Interfaz FPM/OBC <-> CM5 | Bench-only / TBD segun carrier |
| Sensor o sonda `AI_THERM` | Telemetria termica basica | Bench-only |
| `JP1` 2x12 | Control, sense y telemetria | Bench-only |
| `INA219` extra | Opcion de banco, no obligatoria | TBD / bench option |

### 7.3 Componentes abiertos a proposito

| Item | Motivo | Estado |
|---|---|---|
| MPN final de `SW_AI` | Corriente de arranque del CM5 no cerrada | TBD |
| Supervisor dedicado `PGOOD_AI` / `FAULT_AI` | Puede resolverse por firmware bench inicialmente | TBD |
| Estrategia final de metrologia de corriente inline | Riesgo de caida en shunt | TBD |

---

## 8) Arduino Nano como MCU/FPM bench

### 8.1 Pin map bench sugerido

| Pin Nano | Net | Direccion | Uso |
|---|---|---|---|
| `A0` | `VBAT_SENSE` | Input | Sense bateria |
| `A1` | `AI_THERM` | Input | Telemetria termica CM5 |
| `A2` | `5V_AI_SENSE` | Input | Sense rail IA |
| `A4` | `OBC_I2C_SDA` | Bidir | I2C bench |
| `A5` | `OBC_I2C_SCL` | Bidir | I2C bench |
| `D0/RX` | `AI_UART_TX` | Input | UART desde AI |
| `D1/TX` | `AI_UART_RX` | Output | UART hacia AI |
| `D2` | `OBC_HB` | Input | Heartbeat OBC |
| `D3` | `OBC_RST_N` | Output | Reset OBC |
| `D4` | `EN_5V` | Output | Gate 5V |
| `D5` | `EN_SCI` | Output | Gate 3V3 SCI |
| `D6` | `STATUS_LED` | Output | Estado FPM bench |
| `D7` | `PGOOD_3V3` | Input | PGOOD 3V3 bench |
| `D8` | `EN_AI` | Output | Enable rail IA |
| `D9` | `PGOOD_AI` | Input | PGOOD IA |
| `D10` | `FAULT_AI` | Input | Fault IA |
| `D11` | `HB_AI` | Input | Heartbeat IA |
| `D12` | `AI_KILL_N` | Output | Kill/reset IA |
| `D13` | `AI_BOOT_OK` | Input | Boot OK IA |

### 8.2 Notas de implementacion

- `D0/D1` quedan reservados a `AI_UART_*` durante integracion CM5; el debug USB serial no se asume simultaneo.
- `reset_count_OBC`, `fault_count_OBC` y `fault_count_AI` viven en firmware bench y deben persistirse en logging de pruebas.
- Las dos senales `SPARE` de `JP1` quedan reservadas para futuras extensiones bench sin implicar cambio de capa.

---

## 9) Plan de pruebas bench

### 9.1 Ensayos existentes T1-T10

Los ensayos T1-T10 se mantienen vigentes para la cadena bench 1S base:

| ID | Ensayo | Objetivo |
|---|---|---|
| `T1` | Status inicial | Validar rails always-on y estados por defecto |
| `T2` | I2C scan | Detectar sensado solar/load |
| `T3` | Activar `LOAD_5V` | Validar gate 5V |
| `T4` | Medir corriente en `LOAD_5V` | Verificar sensado de carga dummy |
| `T5` | Desactivar `LOAD_5V` | Confirmar corte limpio |
| `T6` | Activar `SCI_3V3` | Validar gate 3V3 |
| `T7` | Desactivar `SCI_3V3` | Confirmar corte limpio |
| `T8` | Test RBF | Confirmar apagado total del bench 1S |
| `T9` | `STATUS_LED` | Validar firmware bench |
| `T10` | Carga solar | Verificar cadena PV -> CN3065 |

### 9.2 Extension Gate IA-2 - ensayos T11-T21

Los siguientes ensayos se agregan al plan del bench extendido. Al 2026-04-03 quedan **documentados, no ejecutados** en este repositorio:

| ID | Ensayo | Resultado esperado |
|---|---|---|
| `T11` | Presencia de `5V_AI_EXT` con rail IA apagado y sin backfeed | `5V_AI_EXT` presente en `J_AI_PWR`, `5V_AI_SW` en OFF, sin retroalimentacion hacia `5V_AUX` ni `3V3_OBC` |
| `T12` | `EN_AI` / `SW_AI` ON y verificacion de `PGOOD_AI` | `5V_AI_SW` habilitado y `PGOOD_AI` valido (real o sintetico) |
| `T13` | Boot reproducible del CM5 real x5 | Cinco ciclos consecutivos de arranque sin fallo latente |
| `T14` | `HB_AI` valido | Heartbeat fisico estable luego de `AI_BOOT_OK` |
| `T15` | Perdida de `HB_AI` -> kill + retry + lockout | FPM bench apaga, reintenta `1-3` veces y entra en lockout controlado |
| `T16` | Prompt versionado cargado y usado en inferencia | El prompt activo cambia y queda reflejado en inferencia/log |
| `T17` | `AI_BEHAVIOR_LOG` persistente con campos minimos | Logs con `timestamp`, `model_version`, `prompt_version`, `decision_id`, `recommended_action`, `confidence`, `supervisor_result`, `MISSION_MODE`, `EPS_STATE` |
| `T18` | Un caso `accepted` y un caso `rejected` del supervisor | Runtime Safety Supervisor demuestra ambos resultados |
| `T19` | Mutua exclusion IA <-> TX UHF | No se habilitan simultaneamente IA y TX UHF durante el ensayo |
| `T20` | Medicion real de consumo | Valores medidos de idle / activo / inferencia burst en CM5 real |
| `T21` | Medicion termica basica + fallback deterministico con CM5 apagado | Telemetria `AI_THERM` registrada y OBC/FPM continúan operativos con CM5 apagado |

---

## 10) Limitaciones y no-claims

1. `EPS_Bench1_1S` sigue siendo un banco 1S COTS. No es flight-like ni flight.
2. La rama IA usa `5V_AI_EXT` externo. No representa la alimentacion 2S + MPPT de vuelo.
3. La potencia principal del CM5 **no** debe pasar por `JP1`.
4. El riesgo de backfeed entre `5V_AI_EXT` y los rails del bench debe verificarse en `T11`.
5. El switch principal `SW_AI` queda abierto como seleccion `TBD` hasta medir corriente real del CM5.
6. Un `INA219` inline en el rail principal del CM5 sigue siendo una opcion de banco, no una decision cerrada.
7. `PGOOD_3V3` continua con workaround de jumper o supervisor futuro, segun lo ya documentado.

---

## 11) Roadmap EPS

```text
EPS_Bench1_1S
  - Banco COTS 1S
  - FPM bench
  - Rail IA bench-only con 5V externo para Gate IA-2
        |
        v
EPS_Flight_Like_2S_MPPT
  - PCB custom 2S + MPPT
  - Integracion de sistema
  - Rail IA integrado TBD
        |
        v
EPS_Flight_2S_MPPT
  - Hardware final de vuelo
  - Politica COTS-to-Flight completa
```

---

## 12) Archivos relacionados

| Ruta | Contenido |
|---|---|
| `03_Power/EPS_Bench1_1S.md` | Documento canonico actual |
| `03_Power/EPS_PCB/EPS_Bench1S/eps_bench_mods.md` | Cambios de netlist / wiring del bench |
| `05_Software/ai_payload_architecture.md` | Integracion del CM5 en banco y Gate IA-2 |
| `01_Mission/validation_plan_and_stage_gates.md` | Gate IA-2 y criterios T11-T21 |
| `06_Costs/BOM_master.csv` | Items bench-only del rail IA |
| `07_Risk/top_risks.md` | Riesgos de backfeed, secuenciamiento y extrapolacion |

---

## 13) Proximos pasos

1. Actualizar la documentación de cableado del bench y, si se reintroduce un archivo EDA, confirmar licencia/origen antes de publicarlo.
2. Implementar `SW_AI`, `F_AI` y el harness hacia carrier board COTS externa.
3. Instrumentar `PGOOD_AI`, `FAULT_AI`, `HB_AI`, `AI_BOOT_OK`, `AI_THERM` y `5V_AI_SENSE`.
4. Ejecutar T11-T21 y registrar evidence pack sin declarar cierre antes de medir.
5. Mantener separacion estricta entre evidencia bench y arquitectura `EPS_Flight_Like_2S_MPPT`.
