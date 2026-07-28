# CAD asset policy

**Revisión:** 2026-07-27
**Estado:** Active

## Estado de diseño

No existe actualmente un CAD mecánico de AUSTRALIS-1 apto para *fit-check*,
análisis estructural ni fabricación. La ausencia es un bloqueo explícito, no
evidencia de conformidad.

La base dimensional de referencia está documentada en
`../STRUCTURE_BASELINE_PRELIMINARY.md`. En particular, un 1.5U conforme con
CubeSat Design Specification (CDS) Rev. 14.1 no debe modelarse como una caja de
150 mm: la longitud exterior de referencia es `170.2 ± 0.1 mm`. El dibujo
completo de Appendix B y el ICD del integrador controlan rieles, *keep-outs*,
accesos, tolerancias y envolvente desplegada.

CAD artifacts are public only when origin, authorship and license are clear.

The previous `bac_Rail_1.5U_v1r1.3mf` file was removed from the public tree
because its origin metadata was not sufficient for publication review. Re-add
CAD files only after confirming that they are project-authored or properly
licensed for redistribution under the project license.

## Criterios mínimos para aceptar un CAD futuro

El CAD seguirá en estado `Preliminary` hasta que una revisión mecánica registre:

- configuración y revisión del CDS y del ICD de dispensador utilizados;
- envolvente, rieles, superficies de contacto, accesos y *keep-outs*;
- stack completo, conectores, arnés, rutas RF, batería, CM5 y ruta térmica;
- antenas/mecanismos en estado almacenado y desplegado, con barridos de
  interferencia;
- materiales, acabados, tornillería, precargas y rutas de carga;
- roll-up trazable de masa, centro de gravedad e inercias, con incertidumbre;
- márgenes de tolerancia y un *fit-check* contra un modelo controlado del
  dispensador;
- análisis estructural modal/cargas y plan de vibración/shock, con niveles TBD
  hasta disponer del ICD;
- revisión de manufacturabilidad y control de configuración.

No se fijan aquí masas, frecuencias naturales ni niveles ambientales: siguen
`TBD` hasta selección del hardware, CAD y requisitos del integrador.
