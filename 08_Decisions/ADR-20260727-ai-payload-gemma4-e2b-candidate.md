# ADR-20260727-ai-payload-gemma4-e2b-candidate

- **Fecha:** 2026-07-27
- **Estado:** Accepted
- **Supersede:** ADR-20260314 (selección de modelo/hardware específico),
  ADR-20260316 y ADR-20260615

## Contexto

La auditoría encontró que la evidencia publicada como “Granite 350M” fue
generada por scripts que cargan Granite 3.1 2B. El dataset y el holdout tampoco
constituyen evidencia independiente suficiente. Por decisión de proyecto,
Granite 350M/2B se abordará en un trabajo posterior.

## Decisión

1. El candidato actual de modelo para el payload experimental es
   **`gemma4:e2b`**.
2. “Candidato” significa únicamente artefacto a evaluar. No significa modelo
   validado, flight-like, flight-ready ni seleccionado para vuelo.
3. El identificador inmutable del artefacto (manifest/digest), cuantización,
   tokenizer, licencia, dependencias y hardware objetivo exacto permanecen
   `TBD` hasta el registro de evidencia.
4. Granite 350M, Granite 3.1 2B y SmolLM2 quedan como líneas históricas/diferidas,
   sin claims vigentes de validación.
5. La arquitectura segura se mantiene:
   - OBC determinístico como única autoridad de vuelo;
   - IA power-gated y OFF por defecto;
   - ninguna acción directa sobre actuadores o cargas;
   - catálogo de herramientas y clase de seguridad asignados por el OBC;
   - validación determinística de schema, precondiciones y postcondiciones;
   - kill/fallback independiente de Linux/modelo;
   - logging completo y correlacionable.
6. La familia CM5 se mantiene como **plataforma de banco candidata**, no como
   hardware de vuelo congelado.

## Gate de evidencia del modelo

Antes de promover el candidato se requiere:

- manifest con digest de modelo/tokenizer/runtime/configuración;
- dataset con procedencia, deduplicación y split ciego sin contaminación;
- suite preregistrada con oráculo externo, reglas críticas exact-match, casos
  adversariales y análisis estadístico;
- mediciones de latencia, memoria, potencia y térmica en el hardware exacto;
- validación del supervisor y de la operación determinística con IA apagada;
- revisión de licencia y third-party notices.

No se transfiere ninguna métrica histórica de Granite a `gemma4:e2b`.

## Alternativas consideradas

- Continuar afirmando Granite 350M: rechazada por falta de evidencia exacta.
- Usar la evidencia 2B como proxy: rechazada; un modelo distinto no es proxy
  científico válido de desempeño, memoria, energía o térmica.

## Implicancias

- Gate IA-1 vuelve a `Open`.
- Los criterios de éxito medirán seguridad/utilidad, no solo cantidad de
  inferencias.
- Requisitos, VCRM, riesgos, costos y baseline se actualizan sin inventar
  consumo, masa, MPN o resultados.
