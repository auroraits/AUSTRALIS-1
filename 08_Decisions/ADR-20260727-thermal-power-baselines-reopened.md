# ADR-20260727-thermal-power-baselines-reopened

- **Fecha:** 2026-07-27
- **Estado:** Accepted
- **Supersede:** `ADR-20260320-thermal-design-radiator-cm5-coupling.md`

## Contexto

La auditoría identificó errores de balance radiativo y energético, geometría
1.5U incorrecta, cargas omitidas, propiedades espectrales inconsistentes y
resultados no reproducibles. También se usó un consumo IA aritméticamente
inconsistente para declarar márgenes `3.4×–3.6×`.

## Decisión

1. No se consideran cerrados:
   - generación o margen energético;
   - duty-cycle IA;
   - área/layout solar o necesidad de desplegables;
   - cara/área/recubrimiento de radiador;
   - conductancia CM5→estructura;
   - temperaturas operativas;
   - conclusión de heater no requerido;
   - configuración 2S1P/2S2P.
2. El power budget será un ledger único por modo y fase orbital, con todos los
   consumos, inrush, pérdidas, eficiencias, sol/eclipses, BOL/EOL,
   incertidumbre y fuentes de cada valor.
3. El modelo térmico deberá conservar energía nodo a nodo, usar propiedades
   espectrales consistentes, incluir intercambio con Tierra/espacio, extracción
   eléctrica FV, todas las disipaciones y masas/capacidades derivadas de
   CAD/BOM.
4. Los límites de batería se derivarán de la celda/BMS final e incluirán carga,
   descarga, supervivencia, máximos, sensores e interlock de no-carga.
5. Un fallback que no cumpla los mismos requisitos no se considerará
   equivalente; se analizará como configuración separada.
6. Ningún resultado será `Closed` sin correlación experimental proporcional al
   nivel de madurez, incluyendo TVAC/thermal balance para flight-like.

## Implicancias

- Reabrir requisitos térmicos y energéticos.
- Tratar las cifras históricas solo como resultados de modelos no validados.
- La selección posterior requerirá ADR y evidencia reproducible.
