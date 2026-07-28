# ADR-20260727-orbit-attitude-analysis-reopened

- **Fecha:** 2026-07-27
- **Estado:** Accepted
- **Supersede:** `ADR-20260320-orbit-attitude-solar-layout-baseline.md`

## Contexto

El barrido archivado como SSO (Sun-Synchronous Orbit) combinó altitud,
inclinación y LTAN como variables independientes sin exigir que la precesión J2
mantuviera sincronismo solar. Además, el CSV archivado no reproduce el radiador
ni el ranking descritos por la ADR anterior. La misión rideshare tampoco
controla necesariamente la órbita final.

## Decisión

1. **No existe órbita, LTAN, actitud, layout solar ni cara radiadora congelados.**
2. Para estudios de sensibilidad se conserva una envolvente de trabajo
   `550–650 km`, circular LEO/SSO candidata, pero no como requisito de
   lanzamiento ni como rango ya autorizado.
3. El punto `600 km / LTAN 10:00` puede usarse como caso de análisis etiquetado,
   nunca como órbita confirmada.
4. Para cada altitud SSO, la inclinación deberá derivarse de la condición de
   precesión heliosincrónica y se reportará el drift de LTAN.
5. El análisis deberá incluir caso nominal, extremos del integrador, dispersión,
   fechas/épocas, actitud degradada y error/jitter ADCS.
6. La actitud LVLH perfecta es una hipótesis ideal; no se atribuye al diseño
   hasta existir arquitectura ADCS, presupuesto y evidencia.
7. El propagador y los resultados se validarán contra una implementación
   independiente (por ejemplo Orekit, GMAT o equivalente), con tolerancias
   definidas.

## Evidencia mínima para una nueva decisión orbital

- configuración y commit del simulador;
- manifest de inputs, época, horizonte, paso e hipótesis;
- hashes de artefactos y fila exacta que sustenta la selección;
- verificación de conservación/unidades y tests de regresión;
- análisis de deorbit/reentry y restricciones del integrador;
- impacto en energía, térmica, ADCS, COMMS y radiación.

## Implicancias

- Gate A y riesgo orbital quedan abiertos.
- Los budgets existentes son estudios históricos y no evidencia de cierre.
- La selección final requiere una ADR posterior.
