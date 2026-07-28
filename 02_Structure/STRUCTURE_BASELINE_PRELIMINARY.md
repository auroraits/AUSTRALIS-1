# Base mecánica preliminar — AUSTRALIS-1 1.5U

**Revisión:** 2026-07-27  
**Estado:** Preliminary  
**Trazabilidad:** CubeSat Design Specification Rev. 14.1; sujeto al ICD del
integrador

## 1. Dictamen y límites de uso

AUSTRALIS-1 no dispone aún de una configuración mecánica liberable. Este
documento corrige la base geométrica para los análisis y enumera la evidencia
necesaria; no selecciona estructura, material, proveedor ni artículo de vuelo.

La aproximación `100×100×150 mm` usada históricamente es incorrecta para un
1.5U conforme al CDS y queda prohibida como entrada de CAD, térmica, potencia,
masa, centro de gravedad (CG), inercia o *fit-check*.

## 2. Base geométrica de referencia

Fuente primaria:

- *CubeSat Design Specification Rev. 14.1*, Cal Poly SLO, Appendix B,
  dibujo 1.5U; el historial de cambios de la p. 24 registra la longitud
  `170.2 ± 0.1 mm`.
- URL oficial:
  <https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS+REV14_1+2022-02-09.pdf>

Para cálculos conceptuales de área solamente:

| Parámetro | Valor de referencia | Uso |
|---|---:|---|
| X exterior nominal | 100 mm | área conceptual; confirmar dibujo/ICD |
| Y exterior nominal | 100 mm | área conceptual; confirmar dibujo/ICD |
| Z exterior 1.5U | `170.2 ± 0.1 mm` | longitud de referencia CDS |
| Cara lateral nominal | 0.01702 m² | térmica/solar conceptual |
| Cara extrema nominal | 0.01000 m² | térmica/solar conceptual |
| Área exterior de caja ideal | 0.08808 m² | sin restar rieles ni *keep-outs* |

Respecto de la caja histórica de 150 mm, cada cara lateral aumenta 13.47% y
el área total ideal aumenta 10.10%. Esas diferencias obligan a repetir los
análisis dependientes de superficie; no deben aplicarse como un factor de
corrección a resultados antiguos.

## 3. Requisitos mecánicos no cerrados

Permanecen `TBD` hasta disponer del diseño y del ICD aplicable:

- estructura, aleación, tratamiento superficial y proveedor;
- masa, margen, CG, productos de inercia y tolerancias de integración;
- stack, separación entre placas, conectores y arnés;
- orientación, almacenamiento y despliegue de antenas;
- ruta física CM5–interfaz térmica–radiador;
- primer modo propio, cargas cuasiestáticas, vibración aleatoria y shock;
- mecanismos, inhibiciones, Remove Before Flight (RBF) y switches de
  despliegue;
- áreas solares/radiativas efectivas después de rieles, aperturas, antenas,
  celdas, adhesivos y *keep-outs*;
- compatibilidad con el dispensador y límites finales de masa/CG.

El valor de 3.00 kg de la tabla 1 del CDS es una referencia típica máxima
para 1.5U, no un límite de misión. El ICD del integrador prevalecerá.

## 4. Hipótesis de actitud y ADCS

El repositorio no contiene todavía una arquitectura ADCS (Attitude
Determination and Control System) implementable ni presupuesto de sensores,
actuadores, potencia o masa. Por lo tanto:

- nadir/LVLH perfecto solo puede usarse como caso ideal etiquetado;
- no puede fijarse radiador, generación solar o patrón de antena usando
  actitud perfecta como evidencia;
- todo análisis debe incluir, como mínimo, dispersión de apuntamiento, tumble
  inicial, detumbling, modo degradado y actitud segura, con valores `TBD`
  hasta cerrar el CONOPS ADCS.

## 5. Plan de verificación mecánica

| ID | Verificación | Criterio de aceptación | Evidencia |
|---|---|---|---|
| STR-VV-01 | Auditoría dimensional CDS/ICD | Cada cota y *keep-out* trazado a revisión, página y cláusula | checklist firmado + CAD |
| STR-VV-02 | Roll-up de masa/CG/inercia | Cierre contra límites del ICD con incertidumbre y margen | reporte versionado |
| STR-VV-03 | *Fit-check* | Sin interferencias en peor caso de tolerancias | reporte + capturas/medición |
| STR-VV-04 | Antenas/desplegables | Almacenamiento, liberación y envolvente sin colisiones | procedimiento + video/datos |
| STR-VV-05 | Análisis estructural | Márgenes positivos contra casos del ICD | modelo, inputs y revisión |
| STR-VV-06 | Ambiente mecánico | Funcionalidad pre/post y criterios del plan de ensayo | raw data + reporte |
| STR-VV-07 | Correlación térmico-mecánica | Masas/conductancias derivadas del CAD y ensayo | manifest + reporte |

Ningún ítem puede marcarse cerrado mediante inspección documental únicamente.
