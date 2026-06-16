# ADR-20260615-ai-model-roles-granite350m-flight-candidate-2b-experimentation

- **Fecha:** 2026-06-15
- **Estado:** Accepted

---

## Contexto

Durante la auditoria de publicacion se detecto una tension documental: los
documentos de mision hablan de Granite 350M como baseline funcional de banco,
mientras que scripts historicos de entrenamiento y benchmark referencian
`ibm-granite/granite-3.1-2b-instruct`.

La decision de producto es conservar ambos caminos, pero con roles distintos y
sin declararlos como modelo final de vuelo.

---

## Decision

### Granite 350M

Granite 350M queda como **candidato de vuelo / flight candidate** para el payload
IA, por su tamano, narrativa institucional, licencia Apache 2.0 y mejor encaje
esperado con la familia CM5 y restricciones de energia/termica.

Estado:

- candidato de vuelo;
- baseline funcional de banco para la linea de desarrollo compacta;
- no flight-ready;
- no modelo final congelado.

### Granite 3.1 2B

`ibm-granite/granite-3.1-2b-instruct` queda como **modelo de experimentacion de
banco y ground experimentation**, util para exploracion, comparativas, dataset
iteration, prompt policy y validaciones de comportamiento, pero no es el
candidato primario de vuelo.

Estado:

- experimentacion de banco;
- herramienta de comparacion y entrenamiento;
- no candidato primario de vuelo bajo el presupuesto actual;
- no modelo flight-ready.

---

## Consecuencias

1. Los scripts que referencian Granite 3.1 2B se mantienen como herramientas de
   experimentacion y deben etiquetarse como tales.
2. La documentacion publica debe presentar Granite 350M como candidato de vuelo,
   no como promesa flight-ready.
3. Cualquier declaracion de modelo final de vuelo requiere gates de energia,
   termica, boot reproducible, RuntimeSafetySupervisor integrado, inferencia en
   hardware real y campana ambiental.
4. Los pesos, tokenizers, adapters y checkpoints no se versionan en el repo
   publico.

---

## Gates minimos antes de declarar modelo de vuelo

- inferencia reproducible en CM5 objetivo;
- medicion de consumo y termica en duty-cycle representativo;
- validacion con RuntimeSafetySupervisor;
- politica OFF/ON integrada con EPS/OBC;
- comportamiento JSON contractual en benchmark y holdout;
- downlink de `AI_BEHAVIOR_LOG`;
- decision de empaquetado y supply-chain de modelo;
- revision de licencia y third-party notices.
