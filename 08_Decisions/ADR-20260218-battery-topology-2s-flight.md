# ADR-20260218-battery-topology-2s-flight

- **Fecha:** 2026-02-18
- **Estado:** Accepted

## Contexto
El MVP v2.1 y los documentos de dimensionamiento EPS mencionaban celdas Li-ion "en paralelo"
(1S2P) en algunos párrafos, mientras que el esquemático KiCad en
`03_Power/EPS_PCB/EPS_Bench2S_FlightLike` ya implementa BMS 2S (serie). Esta inconsistencia
requería una decisión formal que bloquee la topología para todos los documentos de vuelo.

Actualización 2026-03-14: la incorporación del payload IA obliga a revisar la **capacidad objetivo**
sin cambiar la decisión de topología. La topología bloqueada sigue siendo 2S; lo que cambia es
el target de energía almacenada y la ruta de mitigación.

## Decisión
Adoptar **topología 2S** (dos celdas Li-ion en serie) como arquitectura de batería para
`EPS_Flight_Like` y `EPS_Flight`.

- Tensión nominal de bus: **7.4 V** (rango operativo 6.0–8.4 V)
- Capacidad objetivo baseline actualizada: **~22 Wh nominal** con referencia **18650 de 3.0 Ah** en configuración **2S1P**
- Ruta de mitigación abierta: **2S2P (~44 Wh)** si el power budget con payload IA y la corriente de descarga lo requieren tras medición real en Gate IA-1
- Banco `EPS_Bench1_1S` mantiene 1S; la migración a 2S ocurre en la fase `EPS_Flight_Like`.

## Alternativas consideradas
1. **1S2P (dos celdas en paralelo):**
   - Ventaja: bus de 3.7 V, BMS más simple.
   - Desventaja: requiere boost converter para 5 V, menor eficiencia de DC/DC step-down,
     mayor corriente en el bus para misma potencia.
2. **2S2P (cuatro celdas):**
   - Ventaja: mayor capacidad total.
   - Desventaja: volumen y masa extra en 1.5U; queda abierta solo como ruta de mitigación
     si el payload IA demuestra requerimiento real superior al 2S1P de referencia.
3. **2S (elegida):**
   - Mayor eficiencia de conversión DC/DC (ratio menor desde 7.4 V a 3.3 V).
   - Menor corriente de bus para misma potencia → menor I²R en cableado.
   - BMS 2S maduro y disponible en módulos COTS y ICs dedicados.
   - Alineado con esquemático KiCad existente.

## Tradeoffs / riesgos
- **A favor:** eficiencia, disponibilidad de ICs (por ejemplo, BQ29700, S-8261), coherencia
  con KiCad existente.
- **En contra:** BMS más complejo que 1S; requiere balanceo de celdas.
- **Riesgo técnico:** desbalanceo de celdas en condiciones de temperatura extrema en LEO.
  Mitigación: usar celdas del mismo lote y BMS con balanceo pasivo o activo.

## Implicancias (archivos actualizados por esta decisión)
- `00_MVP/MVP v2.2.md` — decisión bloqueada de batería y target actualizado
- `SYSTEM_BASELINE.md` — §3.2 energía
- `03_Power/EPS Sizing.md` — secciones 1.4 y 9
- `03_Power/Power Budget.md` — referencias de batería
- `06_Costs/BOM_master.csv` — batería flight-like 2S1P de referencia y ruta 2S2P TBD
- `README.md` — descripción de EPS
- `architecture.md` — EPS Evolution Roadmap