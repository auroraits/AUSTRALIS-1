# ADR-20260218-battery-topology-2s-flight

- **Fecha:** 2026-02-18
- **Estado:** Accepted

## Contexto
El MVP v2.1 y los documentos de dimensionamiento EPS mencionaban celdas Li-ion
"en paralelo" (1S2P) en algunos párrafos. La topología necesitaba una decisión
de sistema independiente de la madurez del esquema.

> **Corrección 2026-07-27:** el proyecto KiCad
> `03_Power/EPS_PCB/EPS_Bench2S_FlightLike` es un placeholder no fabricable y
> no implementa un BMS/cargador 2S funcional. Esta ADR decide una topología de
> referencia; no acredita el diseño eléctrico existente.

Actualización 2026-03-14: la incorporación del payload IA obliga a revisar la **capacidad objetivo**
sin cambiar la decisión de topología. La topología bloqueada sigue siendo 2S; lo que cambia es
el target de energía almacenada y la ruta de mitigación.

## Decisión
Adoptar **topología 2S** (dos celdas Li-ion en serie) como arquitectura de batería para
`EPS_Flight_Like` y `EPS_Flight`.

- `2S` significa dos grupos electroquímicos en serie; química, celda, tensión
  nominal/límites, capacidad, formato y eventual paralelo permanecen `TBD`.
- La selección se realizará después de cerrar presupuesto de energía/corriente,
  límites térmicos, seguridad, degradación y dossier de batería.
- Banco `EPS_Bench1_1S` mantiene 1S; la migración a 2S ocurre en la fase `EPS_Flight_Like`.

## Alternativas consideradas
1. **1S2P (dos celdas en paralelo):**
   - Ventaja: bus de 3.7 V, BMS más simple.
   - Desventaja: requiere boost converter para 5 V, menor eficiencia de DC/DC step-down,
     mayor corriente en el bus para misma potencia.
2. **2S2P (cuatro celdas):**
   - Ventaja: mayor capacidad total.
   - Desventaja: volumen y masa extra en 1.5U; queda abierta solo como ruta de mitigación
     si el ledger BOL/EOL y la seguridad demuestran la necesidad.
3. **2S (elegida):**
   - Menor relación de conversión hacia rails de baja tensión que una
     arquitectura 1S con boost a 5 V, sujeta a selección real.
   - Menor corriente de bus para misma potencia → menor I²R en cableado.
   - Existen familias de protección/carga 2S, sujetas a trade y evidencia.

## Tradeoffs / riesgos
- **A favor:** menor corriente de bus para una potencia dada y conversión buck
  compatible con los rails previstos.
- **En contra:** BMS más complejo que 1S; requiere balanceo de celdas.
- **Riesgo técnico:** desbalanceo de celdas en condiciones de temperatura extrema en LEO.
  Mitigación: pack completo con protección primaria/secundaria, FETs, fusible,
  balanceo, medición por grupo, sensores, charge inhibit, lot control, FMEA y
  ensayos de falla/TVAC. Ningún IC aislado constituye el BMS completo.

## Implicancias (archivos actualizados por esta decisión)
- `00_MVP/MVP v2.2.md` — decisión bloqueada de batería y target actualizado
- `SYSTEM_BASELINE.md` — §3.2 energía
- `03_Power/EPS Sizing.md` — secciones 1.4 y 9
- `03_Power/Power Budget.md` — referencias de batería
- `06_Costs/BOM_master.csv` — arquitectura de pack 2S abierta y trazada
- `README.md` — descripción de EPS
- `architecture.md` — EPS Evolution Roadmap
