# EPS_Bench1_1S - Modificaciones para FPM bench + rail IA bench-only

**Revision:** 2026-04-03
**Archivo base:** Fritzing legacy removido del árbol público; este documento conserva la trazabilidad humana de cambios.
**Objetivo:** Extender el bench EPS 1S para Gate IA-2 sin cambiar su naturaleza bench-only

---

## 1) Alcance y no-objetivos

Este documento describe los cambios de netlist y cableado humano para `EPS_Bench1_1S`:
- mantener la cadena bench 1S existente
- conservar Arduino Nano como MCU/FPM del bench
- agregar la rama IA bench-only con inyeccion externa de 5V
- expandir `JP1` a 2x12 para control/sense/telemetria

No-objetivos:
- no convertir el bench en `EPS_Flight_Like_2S_MPPT`
- no rutear la potencia principal del CM5 por `JP1`
- no fijar el MPN final de `SW_AI`
- no depender de exports HTML/BOM generados con rutas locales o metadata privada

---

## 2) Resumen de cambios

| Bloque | Cambio | Resultado |
|---|---|---|
| Cadena base 1S | Sin cambios de topologia | Se preservan CN3065, BMS 1S, `5V_AUX`, `3V3_OBC`, cargas dummy |
| FPM bench | Arduino Nano pasa a cubrir OBC + IA | `EN_AI`, health signals y contadores documentados |
| Potencia IA | Nueva entrada `J_AI_PWR` | `5V_AI_EXT` principal desde fuente externa 5V |
| Proteccion IA | Nuevo `F_AI` | Proteccion dedicada del rail IA bench-only |
| Switch IA | Nuevo `SW_AI` | Conmutacion de `5V_AI_SW` bajo `EN_AI` |
| Sensado IA | Nuevo `5V_AI_SENSE` | Telemetria de rail IA sin usar `JP1` como potencia |
| Interfaz CM5 | Harness a carrier board COTS externa | UART + `HB_AI` + `AI_BOOT_OK` + `AI_THERM` |
| Header de sistema | `JP1` pasa a 2x12 | Header control/sense only |

---

## 3) Topologia actualizada

```text
PV1/PV2 -> D1/D2 -> F1 -> INA219_SOLAR -> CN3065 -> BMS 1S -> RBF -> VBAT_PROT+
                                                            |
                                                            +-> Boost -> 5V_AUX -> Buck -> 3V3_OBC
                                                            |                     |
                                                            |                     +-> JP1 (control/sense)
                                                            |                     +-> Gate SCI -> 3V3_SCI_SW
                                                            |
                                                            +-> Gate 5V -> 5V_LOAD_SW
                                                            +-> Arduino Nano (FPM bench)

J_AI_PWR -> 5V_AI_EXT -> F_AI -> SW_AI -> 5V_AI_SW -> harness -> carrier board COTS externa -> CM5 real
                                           |
                                           +-> 5V_AI_SENSE
                                           +-> AI signals a JP1
```

Regla de cableado:
- `J_AI_PWR` lleva la potencia principal de la rama IA.
- `JP1` solo distribuye control, sensado y telemetria.
- `5V_AI_SENSE` en `JP1` es sense, no alimentacion.

---

## 4) Nuevas nets a crear

| Net | Tipo | Uso |
|---|---|---|
| `J_AI_PWR` | Conector | Entrada externa principal del rail IA |
| `5V_AI_EXT` | Potencia | 5V externa hacia la rama IA |
| `GND_AI` | Potencia | Retorno principal de la rama IA |
| `F_AI` | Proteccion | Fusible/PTC del rail IA |
| `SW_AI` | Switch | Load switch / eFuse de alta corriente para IA |
| `5V_AI_SW` | Potencia | Salida conmutada hacia el CM5 |
| `5V_AI_SENSE` | Sense | Medicion/presencia del rail IA |
| `EN_AI` | Control | Enable de `SW_AI` desde FPM bench |
| `PGOOD_AI` | Health | Power-good IA real o sintetico |
| `FAULT_AI` | Health | Fault IA real o sintetico |
| `HB_AI` | Health | Heartbeat fisico desde CM5 |
| `AI_KILL_N` | Control | Kill/reset de emergencia |
| `AI_BOOT_OK` | Health | Indicacion de boot operativo |
| `AI_UART_TX` | Comms | UART TX desde AI |
| `AI_UART_RX` | Comms | UART RX hacia AI |
| `AI_THERM` | Telemetria | Sensor/sonda termica CM5 |

---

## 5) Pin map sugerido del Arduino Nano / FPM bench

| Pin Nano | Net | Direccion |
|---|---|---|
| `A0` | `VBAT_SENSE` | Input |
| `A1` | `AI_THERM` | Input |
| `A2` | `5V_AI_SENSE` | Input |
| `A4` | `OBC_I2C_SDA` | Bidir |
| `A5` | `OBC_I2C_SCL` | Bidir |
| `D0/RX` | `AI_UART_TX` | Input |
| `D1/TX` | `AI_UART_RX` | Output |
| `D2` | `OBC_HB` | Input |
| `D3` | `OBC_RST_N` | Output |
| `D4` | `EN_5V` | Output |
| `D5` | `EN_SCI` | Output |
| `D6` | `STATUS_LED` | Output |
| `D7` | `PGOOD_3V3` | Input |
| `D8` | `EN_AI` | Output |
| `D9` | `PGOOD_AI` | Input |
| `D10` | `FAULT_AI` | Input |
| `D11` | `HB_AI` | Input |
| `D12` | `AI_KILL_N` | Output |
| `D13` | `AI_BOOT_OK` | Input |

Notas:
- `PGOOD_AI` y `FAULT_AI` pueden cablearse a una salida de supervisor dedicado o a una fuente sintetica de firmware bench.
- `D0/D1` quedan reservados a UART AI durante integracion CM5; el debug USB serial no se asume en simultaneo.

---

## 6) Cambios de wiring en Fritzing

### Paso A - Conservar la cadena 1S existente

No tocar:
- paneles + diodos de OR-ing
- `F1`
- `INA219_SOLAR`
- `CN3065`
- BMS 1S
- RBF
- boost `5V_AUX`
- buck `3V3_OBC`
- gates de `5V_LOAD_SW` y `3V3_SCI_SW`

### Paso B - Agregar `J_AI_PWR`

Agregar un conector 2 pines dedicado:
- pin 1 -> `5V_AI_EXT`
- pin 2 -> `GND_AI`

Este conector representa la entrada principal de 5V externa para el CM5 real en banco.

### Paso C - Insertar `F_AI`

Entre `5V_AI_EXT` y `SW_AI` insertar un elemento de proteccion:
- fusible rapido, PTC o proteccion equivalente bench-only
- net de entrada: `5V_AI_EXT`
- net de salida: entrada a `SW_AI`

No fijar MPN final si la corriente del CM5 aun no esta cerrada.

### Paso D - Agregar `SW_AI`

Agregar un bloque de switch/eFuse/load-switch de alta corriente:
- entrada desde `F_AI`
- salida a `5V_AI_SW`
- enable controlado por `EN_AI`

Reglas:
- `SW_AI` es bench-only
- no declarar este bloque como representativo del rail IA de vuelo
- si se usa un load switch generico en Fritzing, documentarlo como placeholder

### Paso E - Agregar `5V_AI_SENSE`

Crear una derivacion de sensado desde `5V_AI_SW`:
- la derivacion entra al FPM bench
- exponer tambien la net en `JP1` pin 19
- esta net es solo sense y no debe alimentar la carrier board

### Paso F - Harness hacia carrier board COTS externa

Desde el bench hacia el CM5 real documentar dos grupos de cableado:

**Potencia**
- `5V_AI_SW`
- `GND_AI`

**Control / health**
- `PGOOD_AI`
- `FAULT_AI`
- `HB_AI`
- `AI_KILL_N`
- `AI_BOOT_OK`
- `AI_UART_TX`
- `AI_UART_RX`
- `AI_THERM`

La carrier board del CM5 permanece externa al bench. El harness se considera parte del bench extendido para Gate IA-2.

### Paso G - Expandir `JP1` a 2x12

Reemplazar el header 2x5 por un header 2x12.

| Pin | Net |
|---|---|
| 1 | `3V3_OBC` |
| 2 | `GND` |
| 3 | `5V_AUX` |
| 4 | `GND` |
| 5 | `OBC_I2C_SDA` |
| 6 | `OBC_I2C_SCL` |
| 7 | `OBC_HB` |
| 8 | `OBC_RST_N` |
| 9 | `VBAT_SENSE` |
| 10 | `PGOOD_3V3` |
| 11 | `EN_AI` |
| 12 | `PGOOD_AI` |
| 13 | `FAULT_AI` |
| 14 | `HB_AI` |
| 15 | `AI_KILL_N` |
| 16 | `AI_BOOT_OK` |
| 17 | `AI_UART_TX` |
| 18 | `AI_UART_RX` |
| 19 | `5V_AI_SENSE` |
| 20 | `AI_THERM` |
| 21 | `SPARE` |
| 22 | `GND` |
| 23 | `SPARE` |
| 24 | `GND` |

Regla obligatoria:
- **No** rutear `5V_AI_EXT` ni `5V_AI_SW` principal por `JP1`.

### Paso H - Net labels a crear o actualizar

Crear o actualizar los siguientes net labels en Fritzing:
- `5V_AI_EXT`
- `5V_AI_SW`
- `5V_AI_SENSE`
- `EN_AI`
- `PGOOD_AI`
- `FAULT_AI`
- `HB_AI`
- `AI_KILL_N`
- `AI_BOOT_OK`
- `AI_UART_TX`
- `AI_UART_RX`
- `AI_THERM`
- `J_AI_PWR`

---

## 7) Metrologia de corriente del CM5

El sensado principal de corriente del CM5 queda abierto como decision de banco:

| Opcion | Estado | Nota |
|---|---|---|
| `INA219` extra inline en el rail principal | TBD / bench option | Puede introducir caida en shunt y afectar boot del CM5 |
| Metrologia externa de banco | Valida | Fuente de laboratorio, medidor inline o instrumento externo |

Regla:
- si el `INA219` inline degrada el arranque o la estabilidad del CM5, la referencia valida para `T20` pasa a ser metrologia externa de banco.

---

## 8) Delta de BOM bench-only

| Item | Funcion | Estado |
|---|---|---|
| Conector `J_AI_PWR` | Entrada 5V externa | Nuevo |
| Harness 5V + control | Conexion bench <-> carrier board | Nuevo |
| `F_AI` | Proteccion rail IA | Nuevo |
| `SW_AI` | Switch/eFuse/load-switch alta corriente | Nuevo / TBD |
| Carrier board COTS CM5 | Soporte del CM5 real | Nuevo |
| Adaptacion de niveles UART | Interfaz bench | Nuevo / TBD |
| Sensor `AI_THERM` | Telemetria termica basica | Nuevo |
| `INA219` extra | Opcion de banco, no obligatoria | TBD |

---

## 9) Checklist de verificacion posterior al rewiring

- [ ] `J_AI_PWR` pin 1 termina en `5V_AI_EXT`
- [ ] `J_AI_PWR` pin 2 termina en `GND_AI`
- [ ] `5V_AI_EXT` no tiene continuidad accidental con `5V_AUX`
- [ ] `5V_AI_EXT` no tiene continuidad accidental con `3V3_OBC`
- [ ] `JP1` pin 19 esta cableado a `5V_AI_SENSE`, no a la potencia principal
- [ ] `SW_AI` abre/cierra `5V_AI_SW` bajo `EN_AI`
- [ ] `HB_AI`, `AI_BOOT_OK` y `AI_THERM` llegan al FPM bench
- [ ] `PGOOD_AI` y `FAULT_AI` estan definidos como reales o sinteticos
- [ ] El harness de potencia a carrier board usa `5V_AI_SW` + `GND_AI`
- [ ] No queda ningun tramo de potencia principal IA pasando por `JP1`

---

## 10) Nota sobre artefactos generados

- La fuente documental humana a mantener es este archivo y `03_Power/EPS_Bench1_1S.md`.
- Los exports HTML/BOM generados no se versionan en el árbol público si contienen rutas locales o metadata privada.
