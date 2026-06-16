# ADR-20260218-geiger-removed-from-mvp

- **Fecha:** 2026-02-18
- **Estado:** Accepted

## Contexto
El Science Pack del MVP v2.1 incluía un contador Geiger con convertidor de alta tensión (HV).
Este componente era el segundo mayor consumidor eléctrico del satélite (0.70 W, 33% duty en
SCI MODE) y añadía complejidad de diseño de convertidor HV, reglas operativas restrictivas
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
   reduce consumo en SCI MODE en ~0.231 W promedio, elimina reglas EMI Geiger/TX, y no afecta
   el criterio de éxito mínimo del MVP.

## Impacto en presupuesto de potencia
- SCIENCE avg: 0.610 W → **~0.299 W** (reducción de ~51%)
- SAFE avg: 0.193 W → **~0.143 W** (reducción por UHF TX recalculado)
- Caso típico por órbita: 0.55 Wh → **~0.381 Wh** (mejor margen energético)

## Implicancias (archivos actualizados)
- `00_MVP/MVP v2.1.md`
- `03_Power/Power Budget.md`
- `03_Power/EPS Sizing.md`
- `07_Risk/` — eliminar riesgos específicos de Geiger/HV
- `architecture.md`
