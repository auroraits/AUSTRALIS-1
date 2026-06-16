# ADR-20260313-uhf-downlink-operational-mask

- **Fecha:** 2026-03-13
- **Estado:** Accepted

---

## Contexto

El link budget preliminar del downlink UHF (`04_Communications/link_budget_uhf_preliminary.md`) muestra que a 10° de elevación el margen teórico de papel es solo +1 dB (con la hipótesis de 500 mW RF). En la práctica, pérdidas no modeladas de polarización, body loss, detuning de antena y pérdidas de implementación pueden consumir fácilmente ese único dB, resultando en margen neto negativo.

La documentación anterior presentaba el "cierre a 10°" como criterio de referencia sin distinguir explícitamente entre enlace de papel y operación nominal real. Esto podría llevar a un agente o planificador a asumir que la operación nominal es posible a cualquier elevación ≥10°, lo cual es incorrecto sin evidencia.

---

## Decisión

Se establece una **máscara de elevación operativa provisional** para el downlink UHF:

| Rango de elevación | Tratamiento operativo |
|---|---|
| **≥20°** | Zona nominal para validación inicial — criterio de éxito de Gate C |
| **20°–25°** | Zona conservadora/prudente recomendada para primeras operaciones |
| **<20°** | Experimental / oportunista — **no** criterio nominal de éxito del MVP |

### Reglas normativas

1. El proyecto **no debe prometer éxito nominal** del downlink UHF a elevaciones <20°.
2. La validación nominal del downlink UHF para Gate C usa como criterio mínimo elevaciones **≥20°**.
3. La operación a <20° se documenta como experimental/oportunista y no cuenta para el criterio mínimo de éxito del MVP.
4. Esta máscara es **provisional**. Debe confirmarse o revisarse tras medir el margen real con hardware TX candidato (Gate C). Si la evidencia demuestra margen suficiente a menores elevaciones, se puede revisar con nueva ADR.

### Lo que esta ADR NO cierra

- No fija 25° como criterio de aceptación cerrado (25° es la zona prudente recomendada, no un requisito duro).
- No decide el hardware TX final ni su eficiencia real.
- No resuelve CONF-01 (pico EPS / consumo DC del PA).
- No promete que la operación a ≥20° sea siempre exitosa; es el criterio de validación inicial, no una garantía.

---

## Justificación

- A 30° (1100 km), el margen teórico es +9 dB — suficientemente robusto a pérdidas de implementación no modeladas.
- A 10° (2500 km), el margen teórico es +1 dB — esencialmente inoperable con pérdidas reales.
- La zona 20°–25° representa un balance conservador entre duración de ventana útil y robustez del enlace.

---

## Alternativas consideradas

1. **Sin máscara (operar desde 0°):** rechazado. El margen de papel a 10° es insuficiente y no debe presentarse como criterio nominal.
2. **Máscara fija en 25° como requisito duro:** rechazado. No hay evidencia de que 25° sea el límite exacto; sería prematura.
3. **Máscara provisional ≥20° con zona 20°–25° conservadora** (elegida): conservadora y revisable con evidencia.
4. **No documentar la máscara:** rechazado. La ausencia de criterio crea ambigüedad operacional.

---

## Tradeoffs / riesgos

- A favor: criterio de éxito claro y conservador; elimina ambigüedad sobre qué es "operación nominal".
- En contra: reduce la ventana nominal de operación (pasa duración menor que si se usara 10°).
- Riesgo residual: si el hardware TX real tiene menor potencia o mayor pérdida de la hipótesis, incluso la zona ≥20° podría ser marginal.
- Mitigación: confirmar o revisar con medición de hardware real en Gate C.

---

## Implicancias (archivos actualizados)

- `04_Communications/link_budget_uhf_preliminary.md` — §6 y §6.2 actualizados con máscara operativa.
- `04_Communications/rf_subsystem_overview.md` — §5 y §9 actualizados.
- `01_Mission/requirements_matrix.md` — §5 Notas actualizado.
- `01_Mission/validation_plan_and_stage_gates.md` — Gate C: criterio de elevación mínima ≥20° para validación.
- `07_Risk/top_risks.md` — R6 actualizado con máscara operativa y margen de +1 dB a 10°.
- `architecture.md` — §10 baseline COMMS y §13 pendientes actualizados.
