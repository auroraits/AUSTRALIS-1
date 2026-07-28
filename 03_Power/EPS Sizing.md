# EPS Sizing preliminar — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Preliminary / NOT RELEASED
**Trazabilidad:** `03_Power/Power Budget.md`,
`03_Power/LAUNCH_ELECTRICAL_SAFETY_PRELIMINARY.md`,
`02_Structure/STRUCTURE_BASELINE_PRELIMINARY.md`; topología 2S sujeta a la ADR
vigente y a su revisión correctiva

## 1. Alcance y estado

Este documento define el método de dimensionamiento para el EPS
(Electrical Power System) Flight-Like/Flight. No selecciona celda, panel,
MPPT, regulador, BMS ni PCB.

El proyecto KiCad en `EPS_PCB/EPS_Bench2S_FlightLike/` es un marcador
**NON-FABRICABLE**. No implementa ninguna de las funciones enumeradas aquí.

El banco `EPS_Bench1_1S` sigue siendo Bench: sirve para firmware,
power-gating y metrología funcional con alimentación externa del CM5; no
valida el bus 2S ni el EPS de vuelo.

## 2. Entradas que ya no se consideran válidas

- caja 1.5U de 100×100×150 mm;
- órbita fija 90/60/30 min;
- consumo total de 0.381/0.451/0.516 Wh/orbita;
- margen de generación 3.4–3.6×;
- target `≥1.2 W` o `2–3 W BOL` como diseño cerrado;
- batería 2S1P de ~22 Wh como selección;
- 2S2P de ~44 Wh como mitigación demostrada;
- siete celdas / una pieza en una cara cuadrada como topología realizable;
- un único MPPT común como solución ya aceptable.

Los valores históricos pueden consultarse en Git, pero no son entradas de
diseño.

## 3. Geometría

La referencia conceptual 1.5U es:

- X/Y nominales: 100 mm;
- Z: `170.2 ± 0.1 mm`;
- cara lateral ideal: 0.01702 m²;
- cara extrema ideal: 0.01000 m².

El área útil debe derivarse del CAD e incluir rieles, *keep-outs*, antenas,
sensores, aperturas, tolerancias, adhesivos y rutas térmicas. No se permite
usar toda la caja ideal como área solar o radiativa.

## 4. Dimensionamiento de batería

La arquitectura de bus 2S fija dos celdas en serie como mínimo eléctrico; no
fija paralelo, capacidad, química exacta ni artículo de vuelo.

### 4.1 Cálculo requerido

Para cada caso:

`E_required = Σ(P_load,i × t_i) / η_path,i`

La capacidad utilizable debe considerar:

`E_usable_EOL = E_nameplate × f_temperature × f_age × f_rate × DoD_allowed`

Los factores deben provenir del datasheet/ensayo de la celda exacta, con
incertidumbre. No se empleará un multiplicador genérico `×3`.

Casos mínimos:

- eclipse de diseño y recuperación desde SAFE;
- eclipses consecutivos durante contingencia;
- downlink en peor estado permitido;
- detumbling/ADCS;
- inferencia Gemma 4 e2b en CM5, solo si la política la permite;
- arranque en frío, inrush y brownout;
- pérdida/degradación de un string solar;
- EOL y temperatura hot/cold.

### 4.2 Seguridad del pack

El diseño deberá incluir y verificar:

- OVP/UVP/OCP y protección secundaria independiente;
- fusible y limitación de corriente/latch-up;
- FETs de desconexión con estado seguro;
- balanceo y medición individual de celdas;
- sensores térmicos por ubicación justificada;
- límites de carga/descarga/supervivencia del datasheet;
- inhibición autónoma de carga fuera de temperatura y tensión permitidas;
- estrategia ante sensor inválido;
- aislamiento de fallas, venting y contención;
- recuperación segura después de reset/pérdida de energía.

Un IC de protección aislado no constituye un BMS completo. La selección se
cerrará mediante FMEA, esquema revisado, BOM y V&V.

## 5. Dimensionamiento solar

### 5.1 Condición eléctrica

Para un cargador buck hacia un pack 2S:

`Vmp_string_hot_EOL > Vpack_charge_max + headroom_converter`

Si esto no puede cumplirse en todas las condiciones, debe seleccionarse otra
longitud de string o una topología buck-boost/boost demostrada.

Dos half-cells IBC crudas de aproximadamente 0.5–0.6 V cada una no pueden
cargar directamente un pack 2S mediante buck. Una única pieza AnySolar con
`Vmp≈5–6 V` tampoco alcanza por sí sola para un pack con máximo cercano a
8.4 V mediante buck. Estos son filtros de arquitectura, no selección de
producto.

### 5.2 Topología por cara

La topología permanece `TBD`. Debe comparar:

- MPPT independiente por cara/string;
- MPPT multi-input con canales realmente independientes;
- OR-ing/bypass y tolerancia a string abierto/cortocircuitado;
- strings entre caras, penalizados por iluminación desigual;
- body-mounted frente a deployables.

No se conectarán caras ortogonales en serie sin demostrar el efecto de
sombreado/mismatch. Un MPPT común no sigue simultáneamente máximos distintos
de caras ortogonales.

### 5.3 Ledger BOL/EOL

Por cada candidata se registrará:

- revisión de datasheet, lote y dimensiones;
- curva I-V BOL hot/cold y después de irradiación/EOL;
- `Voc`, `Vmp`, `Isc`, `Imp` con tolerancias;
- coverglass, adhesivo, interconnect y diodos;
- mismatch, sombras, pointing y contaminación;
- eficiencia/arranque MPPT por condición;
- pérdida de una cara/string;
- área y masa derivadas del CAD;
- evidencia de ensayo de cupón/panel.

La potencia simulada sin esos factores es un upper bound conceptual.

## 6. Rails y distribución

El esquema futuro debe definir:

| Dominio | Estado seguro | Funciones mínimas |
|---|---|---|
| OBC always-on | ON después de autorización de despliegue | UVLO, OCP, PGOOD, watchdog |
| RF | OFF | high-side switch, inrush, FAULT, aislamiento |
| Science | OFF | high-side switch, OCP, telemetría |
| IA/CM5 | OFF | switch independiente, hard kill, inrush, current limit |
| ADCS | según CONOPS | dominio separado o justificación |
| heaters | OFF | control independiente y límites hardware |

Antes de la eyección, todas las funciones powered deben permanecer apagadas
según el CDS/ICD aplicable. El diseño debe incluir RBF, deployment switch y,
como base mínima, tres inhibiciones RF independientes y tres inhibiciones para
cada función desplegable. Las interfaces finales se confirman con el
integrador, pero esos mínimos no pueden omitirse del esquema y la BOM. La
trazabilidad completa se controla en
`03_Power/LAUNCH_ELECTRICAL_SAFETY_PRELIMINARY.md`.

Cada rail requiere min/nom/max, eficiencia, estabilidad, compensación, layout,
retorno, caída, inrush, corriente de falla, PGOOD/FAULT, telemetría y
comportamiento ante reset.

## 7. Modelo de estados EPS

`EPS_STATE = CRIT | LOW | NOMINAL | HIGH` no está cerrado hasta definir:

- SOC/Vbat/temperatura y sensores de entrada;
- umbrales con tolerancias;
- histéresis, dwell/debounce y prioridad de fallas;
- boot/unknown y sensor inválido;
- transiciones y acciones locales;
- carga permitida/prohibida por temperatura;
- recuperación y logging.

El power-gating no puede depender de una recomendación IA. La autoridad
determinística del OBC/EPS prevalece.

## 8. Plan de V&V

| ID | Nivel | Verificación | Criterio |
|---|---|---|---|
| EPS-VV-01 | análisis | power ledger completo | cero carga obligatoria TBD |
| EPS-VV-02 | esquema | ERC + revisión independiente | cero error/exclusión injustificada |
| EPS-VV-03 | layout | DRC + revisión térmica/PI | reglas trazadas a fabricante/corriente |
| EPS-VV-04 | batería | protecciones y charge-inhibit | opera en cada límite y falla segura |
| EPS-VV-05 | convertidores | matriz V/I/T | eficiencia/estabilidad dentro de criterio |
| EPS-VV-06 | solar | curvas I-V y MPPT | arranque/seguimiento hot/cold/BOL/EOL |
| EPS-VV-07 | rails | inrush/OCP/brownout | sin reset de dominios críticos |
| EPS-VV-08 | integración | peor caso simultáneo | buses estables y fallas contenidas |
| EPS-VV-09 | ambiente | TVAC/vibración/EMC | funcional pre/durante/post según plan |
| EPS-VV-10 | campaña | energy balance | margen positivo con incertidumbre EOL |

## 9. Gates de liberación

### Gate de esquema

- celda, BMS, cargador, rails e interfaces seleccionados;
- FMEA y requisitos trazables;
- ERC y revisión independiente completos.

### Gate de PCB

- CAD/stack mecánico controlado;
- BOM/footprints/datasheets y reglas de fabricación;
- DRC, power integrity y análisis térmico completos.

### Gate Flight-Like

- placa fabricada e inspeccionada;
- bring-up con fuente limitada y simulador de batería/panel;
- todos los EPS-VV aplicables ejecutados con raw data;
- ninguna evidencia Bench 1S usada como sustituto.

### Gate Flight

- configuración congelada;
- derating/radiación/ambiente/EMC cerrados;
- aceptación del integrador y V&V de artículo controlado.

Hasta entonces, EPS permanece `Preliminary / NOT RELEASED`.
