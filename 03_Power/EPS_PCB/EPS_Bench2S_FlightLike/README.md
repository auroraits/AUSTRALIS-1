# EPS Bench 2S Flight-Like (KiCad)

## Propósito
Este proyecto KiCad crea una base inicial del **Sistema Eléctrico de Potencia (EPS, Electrical Power System)** de banco para arquitectura **2S1P Li-ion** (2×18650 en serie), alineada con la migración futura a PCB custom.

## Alcance (banco vs vuelo)
- **Banco (actual):** módulos COTS (Commercial Off-The-Shelf) para prototipado rápido: MPPT (Maximum Power Point Tracking) tipo BQ24650-family, BMS (Battery Management System) 2S, medición con INA219 externos.
- **Vuelo (futuro):** integración de controladores/monitores equivalentes en PCB propia. Este diseño **no** implica calificación de vuelo.

## Escalabilidad solar 2→4 paneles
Se modela como:
- String A activo: 2 paneles en serie (P1, P2).
- String B reservado (futuro): 2 paneles en serie (P3, P4).
- Ambos strings convergen por diodo Schottky por string hacia `PV_BUS_P`.

## Apertura en KiCad
1. Abrir `EPS_Bench2S_FlightLike.kicad_pro`.
2. En Esquemático, el flujo jerárquico es:
   - `EPS_Bench2S_FlightLike.kicad_sch` → `00_Top.kicad_sch` → subhojas `01..06`.
3. Ejecutar ERC (Electrical Rules Check) cuando se reemplacen placeholders por símbolos definitivos.
4. En PCB, ejecutar DRC (Design Rules Check) después de asignar footprints finales y reglas de fabricación.

## Próximos pasos sugeridos
- Reemplazar bloques de conectores por símbolos/footprints finales de cada módulo.
- Definir net classes para potencia y sensado.
- Completar restricciones mecánicas reales del stack de banco.
- Migrar gradualmente COTS a integración de ICs equivalentes.

## Referencia de política COTS-to-Flight
Ver política en:
- `00_MVP/MVP v2.2.md` (baseline vigente)
- `SYSTEM_BASELINE.md` (resumen canónico)
- `03_Power/EPS Sizing.md` (alineación de arquitectura)
- `03_Power/Power Budget.md` (supuestos y límites)
