# ADR-20260727-mission-scientific-experiment-baseline

- **Fecha:** 2026-07-27
- **Estado:** Accepted
- **Supersede:** `ADR-20260314-mission-redef-ai-primary.md`

## Contexto

El criterio histórico podía declarar éxito con cinco inferencias, 100 logs, un
prompt y diez paquetes LoRa aun si todas las propuestas IA eran incorrectas,
inútiles o rechazadas. No definía control, oráculo, cobertura, tamaño muestral,
umbrales de seguridad/utilidad, costo de recursos ni análisis estadístico.

## Decisión

1. El objetivo primario es evaluar si un candidato IA aporta utilidad medible
   frente a un baseline determinístico sin adquirir autoridad de vuelo ni
   exceder límites de seguridad, energía, latencia y temperatura.
2. Antes de ejecutar evidencia de cierre se preregistrarán hipótesis nula y
   alternativa, matriz de escenarios/fallas, control, oráculo externo, rúbrica,
   tamaño muestral, métricas, thresholds, intervalos de confianza, exclusiones y
   plan de análisis.
3. Las reglas críticas son hard-fail; no existe tolerancia de mismatch
   "cosmético" para estado, autorización, potencia, modo o acciones.
4. El éxito exige simultáneamente bus seguro, protocolo ejecutado, métricas
   dentro de umbral, evidencia reproducible y ninguna no conformidad crítica
   abierta. Los conteos históricos solo son pisos operacionales.
5. Cada evento correlacionará entrada raw, identidad/digest de modelo, runtime,
   prompt y supervisor, salida raw, parseo, decisión, acción aplicada,
   postestado, latencia, recursos, energía, temperatura y quality flags.
6. `gemma4:e2b` es candidato de evaluación, no modelo validado ni seleccionado
   para vuelo. Granite/SmolLM son históricos/diferidos.
7. El objetivo store-and-forward es secundario, requiere autorización escrita y
   un protocolo experimental propio con denominador, condiciones e intervalo de
   confianza.

## Consecuencias

- Gate A y SRR permanecen abiertos hasta aprobar la preregistración.
- Ningún benchmark histórico cierra requisitos IA o mitiga riesgo de seguridad.
- La evidencia se controla por VCRM, ProcedureID, ConfigurationID, EvidenceID y
  digests.
- La definición operativa está en `01_Mission/mission_definition.md`; requisitos
  y aceptación están en `01_Mission/requirements_matrix.md`.
