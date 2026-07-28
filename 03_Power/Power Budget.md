# Power Budget preliminar — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Preliminary / INCOMPLETE
**Trazabilidad:** `power_budget_inputs.json`, `power_budget.py`; órbita, ADCS,
hardware RF y EPS final abiertos

## 1. Dictamen

No existe todavía un balance total de potencia/energía del satélite. Los
resultados de este documento cubren únicamente cargas históricas conocidas y
no justifican un margen de sistema, un target solar, una capacidad de batería
ni una configuración térmica cerrados.

Quedan retiradas como conclusiones vigentes:

- la órbita fija de 90 min con 60 min de sol y 30 min de eclipse;
- el margen energético `3.4–3.6×`;
- `4.5 Wh/orbita` como generación confirmada;
- `1.34 Wh/orbita` como consumo total con IA;
- `≥1.2 W netos` como target solar demostrado;
- cualquier afirmación de que el EPS cierra con el payload IA.

El nuevo candidato de modelo es **Gemma 4 e2b** sobre CM5. Sus potencias
idle/inferencia, energía por tarea, inrush, latencia y duty orbital son `TBD`
hasta medir la revisión exacta de hardware, runtime y modelo.

## 2. Método reproducible

Entradas controladas:

- `03_Power/power_budget_inputs.json`

Calculadora determinista, sin dependencias externas:

- `python 03_Power/power_budget.py --self-test`
- `python 03_Power/power_budget.py`
- `python 03_Power/power_budget.py --json`

La calculadora:

1. deriva el período con dinámica de dos cuerpos para sensibilidades de 600 y
   650 km;
2. calcula un eclipse de sombra cilíndrica a beta=0 como caso conceptual;
3. verifica que TX y RX UHF no excedan duty total 1 en half-duplex;
4. integra las cargas conocidas por modo;
5. devuelve siempre `INCOMPLETE` mientras falten cargas obligatorias.

No reemplaza un propagador validado, un CONOPS temporal ni datos medidos.

## 3. Supuestos de carga conocidos

Todos son estimaciones históricas no verificadas salvo que se incorpore una
fuente/medición en una revisión futura.

| Carga | Potencia usada | Estado / limitación |
|---|---:|---|
| OBC run | 0.10 W | estimación; medir min/nom/max |
| OBC sleep | 0.02 W | estimación; incluye RTC de forma no trazada |
| SPI NOR write | 0.05 W | estimación de pico |
| microSD write | 0.30 W | estimación de pico/inrush incompleta |
| LoRa RX single-channel | 0.06 W | candidato, no hardware seleccionado |
| LoRa concentrator COTS | 0.495 W | 99 mA @ 5 V, escenario de datasheet |
| UHF RX | 0.15 W | estimación, receptor final TBD |
| UHF TX DC | 1.50 W | hipótesis de 500 mW RF y ~33% PA; no incluye toda la cadena |
| GNSS | 0.10 W | estimación |
| sensores Science I2C | 0.05 W | estimación |

Los campos `legacy_unallocated_allowance`, `nominal_storage_allowance` y
`downlink_other_allowance` se conservan en el JSON para reproducir la
aritmética histórica. Son provisiones, no cargas físicas ni margen.

## 4. Potencia conocida por modo

Resultado de la revisión 2026-07-27:

| Perfil | Potencia conocida | Cobertura |
|---|---:|---|
| SAFE | 0.1425 W | cargas históricas parciales |
| NOMINAL + ciencia, LoRa single | 0.3790 W | sin IA/ADCS/EPS completo |
| NOMINAL + ciencia, concentrator | 0.4443 W | sin IA/ADCS/EPS completo |
| DOWNLINK half-duplex | 1.1100 W | TX 60% + RX hasta 40% |

La versión anterior sumaba 60% TX y 60% RX en la misma ventana half-duplex.
Eso implicaba 120% de ocupación. Ahora `TX_duty + RX_duty ≤ 1`; cualquier
tiempo idle reduce RX, no se suma.

## 5. Sensibilidad orbital de las cargas conocidas

Con radio terrestre ecuatorial 6378.137 km, `μ=398600.4418 km³/s²` y eclipse
beta=0 de sombra cilíndrica:

| Altitud | Período | Eclipse beta=0 | SAFE+DL 10 min | NOMINAL+SAFE single | NOMINAL+SAFE concentrator |
|---:|---:|---:|---:|---:|---:|
| 600 km | 96.687 min | 35.488 min | 0.3909 Wh/orbita | 0.4709 Wh/orbita | 0.5374 Wh/orbita |
| 650 km | 97.728 min | 35.380 min | 0.3934 Wh/orbita | 0.4779 Wh/orbita | 0.5457 Wh/orbita |

Estos valores son **energía de cargas conocidas**, no consumo total. El caso
beta=0 no representa toda la campaña anual; el perfil final debe venir del
propagador orbital validado y del CONOPS.

## 6. Cargas obligatorias todavía abiertas

El presupuesto no puede cerrarse hasta incorporar:

- rail IA: CM5 + Gemma 4 e2b, idle/inferencia/inrush;
- sensores y actuadores ADCS, incluido detumbling;
- controlador EPS y corrientes quiescentes de todos los convertidores;
- BMS, protección, balanceo y cadena de medición;
- eficiencia MPPT/DC-DC como función de tensión, corriente y temperatura;
- eFuses, switches high-side y protección contra latch-up;
- heaters e inhibición de carga por temperatura;
- mecanismos de liberación, RBF e inhibiciones de lanzamiento;
- lógica del transceiver RF, regulador y PA fuera de la hipótesis de 1.5 W;
- arnés, fugas, autodescarga y degradación EOL.

También faltan potencia pico, duración y simultaneidad de cada carga. No se
debe reemplazar un `TBD` por un porcentaje genérico.

## 7. Ledger requerido para cierre

Cada fila futura debe incluir:

| Campo | Contenido requerido |
|---|---|
| LoadID / rail | identificador estable y dominio de potencia |
| Modo/estado | SAFE, NOMINAL, DOWNLINK y condición EPS |
| min/nom/max | W o A con tensión y tolerancia |
| duración/duty | distribución temporal y simultaneidad permitida |
| inrush | amplitud, duración y energía |
| fuente | datasheet con revisión o EvidenceID de medición |
| temperatura/voltaje | condiciones de la cifra |
| BOL/EOL | degradación y margen de incertidumbre |
| conversión | eficiencia de cada etapa, no un único factor global |
| verificación | procedimiento, artículo, instrumento y criterio |

## 8. Reglas de operación energética

- `EPS_STATE = CRIT` fuerza `MISSION_MODE = SAFE`.
- IA solo puede habilitarse en sol, `MISSION_MODE = NOMINAL`,
  `EPS_STATE >= NOMINAL`, rail estable y límites térmicos satisfechos.
- La seguridad no depende de un comando de tierra: el EPS/OBC debe apagar
  localmente cargas no críticas ante undervoltage, sobrecorriente,
  sobretemperatura o telemetría inválida.
- UHF es half-duplex; TX/RX no se presupuestan como simultáneos salvo que el
  hardware final demuestre que son cadenas eléctricas concurrentes.
- LoRa 915 MHz permanece RX-only en órbita.
- microSD y payloads no críticos deben poder diferirse o apagarse.
- Ninguna carga se habilita sin límite de corriente, inrush y recuperación de
  brownout definidos.

## 9. Batería y térmica

La topología de bus 2S no selecciona celda, capacidad ni BMS. El cierre exige:

- datasheet y lote/celda final;
- límites de carga, descarga y supervivencia, mínimos y máximos;
- *charge inhibit* autónomo por temperatura y tensión de cada celda;
- OVP/UVP/OCP, protección secundaria, fusible, dual FET, balanceo y sensores;
- capacidad BOL/EOL a corriente y temperatura de misión;
- profundidad de descarga, envejecimiento, dispersión y fallas;
- correlación en thermal-vacuum (TVAC).

El límite histórico `Tmin ≥ -10 °C` de descarga no autoriza carga a esa
temperatura. No se puede retirar un heater ni cerrar la batería con ese único
umbral.

## 10. Solar y criterio de cierre

El target solar permanece `TBD`. Debe derivarse después de cerrar:

1. energía total por órbita y por campaña, con incertidumbre;
2. peor caso de actitud/apuntamiento y pérdida de una cara/string;
3. curvas I-V hot/cold y BOL/EOL;
4. coverglass, adhesivo, interconexión, mismatch, sombras y radiación;
5. eficiencia/arranque del MPPT y conversiones;
6. límites de batería y energía de recuperación desde SAFE.

Un margen será defendible únicamente como:

`(energía EOL disponible - energía worst-case requerida) / energía requerida`

con numerador y denominador construidos sobre el mismo intervalo, configuración
y conjunto de cargas. No se comparará generación orbital contra consumo
parcial de la IA.

## 11. Verificación

| ID | Prueba | Criterio |
|---|---|---|
| PWR-VV-01 | Unit test de calculadora | `--self-test` PASS |
| PWR-VV-02 | Medición de cada rail | min/nom/max, inrush y energía con incertidumbre |
| PWR-VV-03 | Secuencia half-duplex | ocupación TX+RX≤1 y sin brownout |
| PWR-VV-04 | CM5 + Gemma 4 e2b | potencia/energía/latencia/temperatura para revisión exacta |
| PWR-VV-05 | MPPT/DC-DC | eficiencia y estabilidad en matriz V/I/T |
| PWR-VV-06 | Batería | protecciones y charge-inhibit en límites |
| PWR-VV-07 | Campaña orbital | energía BOL/EOL y recuperación SAFE |
| PWR-VV-08 | Integración | peor caso simultáneo sin reset ni sobretemperatura |

Hasta cerrar PWR-VV-02 a PWR-VV-08, el estado permanece `Preliminary /
INCOMPLETE`.
