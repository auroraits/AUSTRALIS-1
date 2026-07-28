# ADR-20260218-geiger-removed-from-mvp

- **Fecha:** 2026-02-18
- **Estado:** Accepted

> **Alcance aclarado 2026-07-27:** solo permanece aceptada la exclusión del
> Geiger/HV. Modos, consumos y márgenes históricos de esta ADR no son
> allocations vigentes ni evidencia del power budget.

## Contexto
El Science Pack del MVP v2.1 incluía un contador Geiger con convertidor de alta tensión (HV).
Este componente tenía una estimación histórica de consumo/duty y añadía
complejidad de diseño de convertidor HV, reglas operativas restrictivas
(HV OFF durante UHF TX para evitar EMI) y riesgos de interferencia. El criterio de éxito
mínimo del MVP no depende del Geiger.

## Decisión
**Eliminar el contador Geiger (y su convertidor HV) del Science Pack del MVP** en todas sus
versiones (mínimo y extendido MVP+).

Science Pack MVP resultante:
- Sensor UV (I2C)
- Sensor ALS/visible (I2C)
- Magnetómetro 3 ejes (I2C)
- Sensores de temperatura multipunto (I2C o 1-Wire)

El Geiger puede reincorporarse en una versión post-MVP como carga útil opcional, sujeto a
disponibilidad de presupuesto de potencia y volumen.

## Alternativas consideradas
1. **Mantener Geiger con duty-cycle reducido:** ahorra algo de potencia pero no elimina la
   complejidad del HV converter ni las reglas de mutex con UHF TX.
2. **Reemplazar por detector de radiación de estado sólido:** válido para versiones futuras;
   más liviano, sin HV, pero mayor costo y disponibilidad. No priorizado en MVP.
3. **Eliminar del MVP (elegida):** simplifica EPS (elimina convertidor HV del 5V_AUX path),
   elimina una carga y reglas EMI Geiger/TX, y no afecta
   el criterio de éxito mínimo del MVP.

## Impacto en presupuesto de potencia

La exclusión elimina la carga HV, pero su efecto cuantitativo se recalculará en
el ledger integrado BOL/EOL. Los valores históricos no se propagan.

## Implicancias (archivos actualizados)
- `00_MVP/MVP v2.1.md`
- `03_Power/Power Budget.md`
- `03_Power/EPS Sizing.md`
- `07_Risk/` — eliminar riesgos específicos de Geiger/HV
- `architecture.md`
