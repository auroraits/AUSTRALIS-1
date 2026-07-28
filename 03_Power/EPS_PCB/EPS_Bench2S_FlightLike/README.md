# EPS 2S Flight-Like — marcador KiCad no fabricable

**Revisión:** 2026-07-27
**Estado:** Draft / NON-FABRICABLE
**Liberación de fabricación:** BLOQUEADA

> **NO FABRICAR, NO CONECTAR UNA BATERÍA Y NO USAR COMO NETLIST.** Los
> archivos KiCad de este directorio son marcadores gráficos de interfaces, no
> un diseño eléctrico. Las hojas funcionales se mantienen deliberadamente
> desconectadas y la PCB no contiene pads, cobre, vías, zonas ni un outline de
> fabricación válido.

## Propósito
Este proyecto conserva la partición conceptual del **Sistema Eléctrico de
Potencia (EPS, Electrical Power System)** para una arquitectura 2S. No
implementa un cargador, Battery Management System (BMS), reguladores,
power-gating, telemetría, inhibiciones de lanzamiento ni protecciones.

## Alcance (banco vs vuelo)
- **Marcador actual:** conectores y nombres de interfaz sin circuito funcional.
- **Flight-Like futuro:** esquemático y PCB custom completos, todavía `TBD`.
- **Vuelo futuro:** diseño derivado y calificado, todavía `TBD`.

## Escalabilidad solar 2→4 paneles
La intención histórica se representaba como:
- String A activo: 2 paneles en serie (P1, P2).
- String B reservado (futuro): 2 paneles en serie (P3, P4).
- Ambos strings convergen por diodo Schottky por string hacia `PV_BUS_P`.

Esto no cierra la topología solar. El número de entradas MPPT, configuración
serie/paralelo por cara, `Voc/Vmp/Isc` en BOL/EOL y hot/cold, bypass,
OR-ing, arranque y tolerancia a sombreado siguen `TBD`.

## Apertura en KiCad
1. Abrir `EPS_Bench2S_FlightLike.kicad_pro`.
2. En Esquemático, el flujo jerárquico es:
   - `EPS_Bench2S_FlightLike.kicad_sch` → `00_Top.kicad_sch` → subhojas `01..06`.
3. No interpretar una hoja abierta sin cables como diseño incompleto
   fabricable: es una desconexión intencional de seguridad.
4. Ejecutar el bloqueo estático:

   `python validate_eps_placeholder.py`

El script debe aprobar mientras este directorio sea un marcador. Cuando
comience el diseño eléctrico real, debe retirarse solo en un cambio revisado
que incluya la evidencia de liberación indicada abajo.

## Bloqueos de liberación

Antes de crear Gerbers o pedir una PCB deben existir, como mínimo:

- esquema del pack 2S completo: celdas, fusible, protección primaria y
  secundaria, FETs, balanceo, sensado por celda y temperatura;
- cargador CC/CV y MPPT con límites de carga/descarga derivados del datasheet
  de la celda elegida, incluyendo *charge inhibit* por temperatura;
- reguladores reales con eficiencia, estabilidad, compensación, inrush,
  UVLO/OVP/OCP, PGOOD/FAULT y derating;
- switches high-side reales con estado seguro por defecto, límite de corriente
  y aislamiento de fallas; el OBC always-on no debe depender de un control
  software para arrancar;
- RBF, deployment switch e inhibiciones mínimas CDS, sujetos al ICD;
- telemetría Kelvin del pack, celdas, rails y temperaturas;
- referencias anotadas, MPN/footprints controlados, BOM y datasheets;
- ERC sin errores/exclusiones no justificadas;
- stackup y reglas por corriente/caída/temperatura/fabricante;
- PCB con pads, cobre, vías, zonas, outline mecánico controlado y DRC limpio;
- revisión independiente de esquema, layout y FMEA antes de liberar.

## Próximos pasos sugeridos
- Seleccionar celda, arquitectura de protección y cargador mediante requisitos
  verificables; no seleccionar un IC aislado como si fuera el BMS.
- Definir la topología solar por cara y el número de MPPT después de medir o
  disponer de curvas I-V trazables.
- Elaborar esquema, FMEA y plan V&V antes del layout.
- Completar restricciones mecánicas reales del stack.

## Referencia de política COTS-to-Flight
Ver política en:
- `00_MVP/MVP v2.2.md` (baseline vigente)
- `SYSTEM_BASELINE.md` (resumen canónico)
- `03_Power/EPS Sizing.md` (alineación de arquitectura)
- `03_Power/Power Budget.md` (supuestos y límites)
