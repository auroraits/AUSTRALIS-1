# Diseño térmico preliminar — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Preliminary / NOT RELEASED
**Trazabilidad:** `05_Software/SIM/README_SIMULATION.md`,
`02_Structure/ENVIRONMENTAL_VERIFICATION_PRELIMINARY.md`

## 1. Dictamen

No existe todavía una solución térmica cerrada para AUSTRALIS-1. En
particular, quedan retiradas como afirmaciones de diseño:

- la selección de la cara `−Y` como radiador;
- la equivalencia del anodizado blanco con una superficie
  `αsolar ≤ 0.20` y `εIR ≥ 0.88`;
- una conductancia CM5–radiador demostrada de `0.60 W/K` o `1.5 W/K`;
- el strap de cobre de `10 mm² × 40 mm` como contingencia capaz de entregar
  `0.60 W/K`;
- la conclusión “sin heater” para la batería;
- cualquier temperatura Accepted producida por los barridos históricos.

Los resultados del simulador actual son análisis de sensibilidad incompletos.
No seleccionan material, coating, cara radiadora, interfaz térmica ni
configuración de vuelo.

## 2. Propiedades ópticas

`αsolar` y `εIR` deben provenir de la superficie exacta, el proceso, el lote y
el estado BOL/EOL. No se aceptan valores genéricos de una familia de
tratamientos como evidencia de cumplimiento.

La alternativa histórica “anodizado blanco”, con rango declarado
`αsolar = 0.20–0.35` y `εIR = 0.82–0.86`, no cumple la pareja de límites
`αsolar ≤ 0.20` y `εIR ≥ 0.88`: solo toca el límite de absorptancia en el
extremo favorable y no alcanza la emisividad requerida. Por lo tanto, no es
un fallback equivalente. Si se conserva como candidata, requiere requisitos
propios y un análisis nuevo con valores medidos y degradados.

Cada candidata debe registrar:

- fabricante, producto, proceso, sustrato, espesor, lote y orientación;
- `αsolar` y `εIR` medidos con incertidumbre;
- variación por temperatura, UV, radiación, contaminación y ciclo de vida;
- compatibilidad de vacío, outgassing, adhesión y conductividad eléctrica;
- ensayo de cupón antes y después del ambiente aplicable.

## 3. Red de conductancias CM5–radiador

La red debe separar, como mínimo:

1. junction/case del CM5 y carrier;
2. contacto CM5–TIM;
3. TIM;
4. contacto TIM–spreader;
5. spreading en carrier/spreader/tapa;
6. fasteners y presión de montaje;
7. strap, si existe;
8. contacto con panel/radiador;
9. panel y superficie radiativa.

No se puede asignar una única conductancia sin documentar esas resistencias,
su variación de montaje y su incertidumbre.

### 3.1 Comprobación del pad histórico

Para un pad ideal con `k = 17 W/(m·K)`, área `30 × 22 mm` y espesor `1 mm`:

`Gpad,ideal = k A / L = 17 × (0.030 × 0.022) / 0.001 = 11.22 W/K`

Ese valor no demuestra una conductancia de sistema de `1.5 W/K`: los
contactos y el spreading pueden dominar. Tampoco justifica el valor
`0.60 W/K` usado por un modelo. Ambos valores requieren una red física
trazable y correlación experimental.

### 3.2 Comprobación del strap histórico

Para un strap ideal de cobre con `k ≈ 400 W/(m·K)`, sección `10 mm²` y
longitud `40 mm`:

`Gstrap,ideal = 400 × 10e-6 / 0.040 ≈ 0.10 W/K`

Esto es seis veces menor que `0.60 W/K`, antes de sumar resistencias de
contacto. Para alcanzar solo el valor ideal de `0.60 W/K` a `40 mm`:

`Aideal = G L / k = 0.60 × 0.040 / 400 = 60 mm²`

La sección real debería ser mayor al incluir interfaces, tolerancias y
degradación. Este cálculo no selecciona una nueva sección: invalida el
fallback anterior y obliga a rediseñar y ensayar.

## 4. Batería

Los límites térmicos deben provenir del datasheet y de la caracterización de
la celda/BMS exactos. Se definirán por separado:

- temperatura mínima y máxima de carga;
- temperatura mínima y máxima de descarga;
- límites de supervivencia;
- gradientes entre celdas y sensores;
- histéresis y tolerancia de medición;
- inhibición autónoma de carga;
- comportamiento ante sensor inválido.

Demostrar solo `Tmin ≥ −10 °C` durante descarga no autoriza la carga. No se
puede retirar un heater ni cerrar la inhibición de carga con el modelo actual.

## 5. Balance térmico mínimo

El modelo de diseño deberá incluir:

- radiación solar directa, albedo y longwave terrestre con geometría válida;
- emisión neta hacia espacio y Tierra;
- propiedades espectrales coherentes;
- extracción de energía eléctrica de las celdas;
- disipación de OBC, EPS, convertidores, batería, RF/PA, storage, ADCS,
  science y CM5/`gemma4:e2b` por modo;
- eclipses, actitud nominal/degradada, tumble y error de apuntamiento;
- BOL/EOL, hot/cold y tolerancias;
- masas y capacidades derivadas del CAD/BOM, sin doble conteo;
- contactos, conducción interna y acoplamientos medidos;
- condiciones iniciales y convergencia a régimen periódico.

La conservación de energía se verificará en cada nodo y para el sistema
completo con tests de regresión.

## 6. Verificación

| ID | Verificación | Criterio de aceptación |
|---|---|---|
| THR-VV-01 | Propiedades ópticas de cupón | `αsolar/εIR` medidos, incertidumbre y estado BOL/EOL trazables |
| THR-VV-02 | Conductancia de interfaz | `G` medida calorimétricamente con montaje representativo |
| THR-VV-03 | Sensibilidad/tolerancias | límites hot/cold positivos en todos los casos requeridos |
| THR-VV-04 | Thermal balance | correlación modelo–ensayo dentro de tolerancia preregistrada |
| THR-VV-05 | TVAC operacional | funcionalidad hot/cold, SAFE, arranque y carga/inhibición |
| THR-VV-06 | Inspección post-ambiente | sin degradación de TIM, strap, coating o preload fuera de criterio |

Hasta completar estas verificaciones, radiador, coating, strap y heater
permanecen `TBD`.
