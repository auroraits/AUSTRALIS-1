# Simulación orbital/térmica — estado y uso

**Revisión:** 2026-07-27
**Estado:** Preliminary / INCOMPLETE / NOT FOR DESIGN DECISIONS

## Artefacto activo de investigación

`borealis_3d_viewer_v9_3_6rad_export.html` conserva el nombre de archivo por
trazabilidad, pero su identificador interno es
`australis-sim-v10-pre-2026-07-27`.

Correcciones incluidas:

- caja ideal 1.5U 100×100×170.2 mm;
- inclinación SSO circular derivada de altitud imponiendo precesión secular J2;
- integración temporal sin muestra extra;
- iluminación de albedo con la normal terrestre exterior correcta;
- absorptividad IR igual a emisividad y emisión hacia Tierra/espacio;
- extracción eléctrica fotovoltaica restada del nodo de panel;
- energía normalizada a Wh/día;
- eliminación de `thermalKey`, min-max score y “mejor candidato”;
- export CSV + manifest JSON con inputs, revisión fuente y SHA-256.

## Limitaciones que impiden decisiones

- propagador sintético circular/J2 no validado contra Orekit, GMAT o STK;
- actitud LVLH/nadir perfecta, sin error, jitter, tumble, detumbling o SAFE;
- view factors y eclipse conceptuales;
- propiedades ópticas, masas y conductancias no derivadas del CAD/ensayo;
- solo se disipa CM5; faltan OBC, EPS, RF, ADCS, batería y storage;
- `gemma4:e2b`/CM5 usa potencia ingresada por usuario, no evidencia;
- el CM5 se fuerza apagado durante eclipse como hipótesis del modelo;
- `Tmin batt sunlit` es solo un proxy de elegibilidad de carga: no se modelan
  corriente, estado de carga ni charge-inhibit;
- temperatura inicial, substep y clamps numéricos se exportan como hipótesis
  y requieren prueba de convergencia;
- cualquier `NumericalClampHit=true` invalida el resultado térmico;
- no hay correlación thermal balance/TVAC.

Por ello, el simulador exporta todos los casos en orden de entrada, sin
seleccionar órbita, LTAN, actitud, radiador o paneles.

## CSV históricos

Los archivos:

- `borealis_sweep_6rad_2026-03-21T025706.csv`
- `borealis_sweep_6rad_2026-03-21T032025.csv`

son resultados `Historical Snapshot / INVALIDATED`. Usan geometría, SSO,
balance radiativo y score obsoletos. No respaldan las ADR de órbita, radiador,
temperaturas ni energía.

## Reproducibilidad

1. Registrar el commit/tag exacto en la UI.
2. Ejecutar el barrido.
3. Exportar CSV + manifest.
4. Verificar `csvSha256` y conservar ambos archivos.
5. Registrar navegador/versión y dependencias CDN.
6. Ejecutar:

   `python 05_Software/SIM/validate_simulation.py`

La futura herramienta de referencia deberá evitar dependencias de red o
versionarlas con integridad verificable.
