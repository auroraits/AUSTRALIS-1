# BorealisThermalConcept — instantánea histórica

**Revisión:** 2026-07-27
**Estado:** Historical Snapshot / INVALID FOR CURRENT BASELINE

`BorealisThermalConcept.mo` se conserva para trazabilidad, pero no debe
simularse ni citarse como evidencia de AUSTRALIS-1.

No reproduce el simulador HTML actual y contiene, entre otras, estas
suposiciones obsoletas:

- órbita circular de 500 km;
- geometría 1.5U con Z=0.15 m;
- radiador -Z y cinco caras solares preseleccionados;
- propiedades, masas y conductancias sin provenance;
- potencia CM5 idle fuera del duty;
- albedo/IR/extracción eléctrica no reconciliados con v10-pre.

`run_BorealisThermalConcept.mos` está deliberadamente deshabilitado para
evitar que una ejecución accidental genere resultados con apariencia vigente.

## Reapertura futura

Solo debe crearse un nuevo modelo Modelica activo cuando:

1. comparta un único manifest de inputs con el simulador de referencia;
2. use geometría CDS/CAD controlada;
3. implemente el mismo balance de energía y propiedades espectrales;
4. modele todas las cargas internas y estados de batería;
5. tenga tests de conservación energética;
6. se valide contra una herramienta independiente y se correlacione con
   thermal balance/TVAC;
7. reproduzca casos golden con tolerancias declaradas.

Hasta entonces, no existe un source model Modelica vigente.
