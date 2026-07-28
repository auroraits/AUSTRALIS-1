# Life-Cycle Cost Overview — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Open — sin baseline numérico

No existe aún estimación ROM defendible: la BOM no tiene precios numéricos y la
configuración flight-like/flight está abierta. No se publican totales hasta
tener basis of estimate.

## 1. Reglas

- Registrar `low / most likely / high`, no un punto sin incertidumbre.
- Cada valor requiere fuente, fecha, moneda, FX date, cantidad y alcance.
- Separar NRE (Non-Recurring Engineering) de recurring.
- Separar Bench / Flight-Like / Qualification / Flight / EGSE / Operations.
- Incluir mano de obra aunque se reporte por separado.
- No usar `ROM` como valor de `UnitCost`; usar `TBD`.
- Mantener reservas técnicas, de schedule y programáticas explícitas.

## 2. WBS de costo completo

El registro `life_cycle_cost_register.csv` cubre:

- sistemas/project management/QA;
- diseño y prototipos de cada subsistema;
- software, modelo/dataset y cómputo;
- artículos engineering/qualification/flight y spares;
- ground station/EGSE/fixtures/metrología;
- ensayos ambientales/EMC/RF y acceso a laboratorios;
- regulación, coordinación, seguros y asesorías;
- integración, transporte, importación, impuestos/FX;
- launch service/deployer/integrator;
- operaciones, data/hosting y end-of-life.

## 3. Criterio de madurez

| Review | Costo requerido |
|---|---|
| SRR | WBS completa, drivers y método de estimación |
| PDR | low/likely/high por WBS, reservas y schedule linkage |
| CDR | quotes de long-lead/configuración, procurement plan y spares |
| FRR | actuals/estimate-to-complete y costos operativos financiados |

## 4. Cost drivers abiertos

- rediseño EPS y pack seguro;
- CAD/estructura/ADCS no definidos;
- selección RF y estación;
- caracterización `gemma4:e2b`/CM5;
- qualification/acceptance ambiental;
- ruta regulatoria/launch integration;
- importación y disponibilidad regional.

Ninguno tiene valor cerrado.
