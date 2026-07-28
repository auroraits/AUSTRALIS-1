# ADR-20260727-cubesat-1p5u-cds-envelope

- **Fecha:** 2026-07-27
- **Estado:** Accepted

## Contexto

El baseline usaba `100 × 100 × 150 mm` como envolvente externa de un CubeSat
1.5U. Esa simplificación geométrica no coincide con la dimensión longitudinal
1.5U de `170.2 ± 0.1 mm` indicada por CubeSat Design Specification (CDS)
Revision 14.1. El error se propagó a requisitos, CAD conceptual, áreas solares y
radiativas, volumen, masa, centro de gravedad e inercia.

## Decisión

1. La plataforma continúa siendo **1.5U**.
2. Para diseño preliminar se usará la envolvente CDS 1.5U y, en particular, la
   longitud externa `Z = 170.2 ± 0.1 mm`.
3. No se congelan por esta ADR todas las demás cotas: rieles, tabs, keep-outs,
   protrusiones, accesos, rugosidad, masa y centro de gravedad se tomarán del
   dibujo completo CDS y del Interface Control Document (ICD) del integrador.
   La masa máxima típica CDS de referencia para 1.5U es `3.00 kg`; no sustituye
   el límite contractual del dispenser.
4. Todo modelo basado en `150 mm` queda **invalidado para cierre** hasta ser
   regenerado con la geometría completa.
5. Un fit-check físico con el integrador es obligatorio antes de readiness.

## Alternativas consideradas

- Mantener 150 mm como “volumen útil”: rechazada porque se presentaba como
  envolvente externa y contaminaba análisis físicos.
- Adoptar una estructura comercial específica: diferida; proveedor y dispenser
  siguen TBD.

## Implicancias

- Reabrir Gate A y la verificación mecánica.
- Regenerar CAD, layout, áreas, budgets, masa/CG/inercia y análisis térmico.
- Actualizar `MIS-REQ-01`, `COMP-REQ-01` y compliance.

## Fuente

- CubeSat Design Specification Revision 14.1, p. 24:
  <https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS+REV14_1+2022-02-09.pdf>
- SHA-256 de la copia consultada:
  `221fbbbd4f632b16f3e219d1a5e2c2b04e1998c12025b793e6dfc6181af66b5d`.
