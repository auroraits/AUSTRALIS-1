# ADR-20260218-eps-bench1s-cots-to-custom-flight-pcb

- **Fecha:** 2026-02-18
- **Estado:** Accepted

> **Alcance aclarado 2026-07-27:** el banco 1S valida únicamente objetivos de
> aprendizaje y medición locales. No constituye precursor eléctrico equivalente
> del EPS 2S, no transfiere evidencia de compliance y no obliga a conservar
> familias de IC/topologías. El diseño flight-like se deriva independientemente
> de sus requisitos, análisis de seguridad y review.

## Contexto
Se requiere consolidar una arquitectura EPS de banco 1S (`EPS_Bench1_1S`) para validar funciones eléctricas básicas con componentes COTS disponibles, manteniendo coherencia con la evolución a PCB custom en KiCad.

## Decisión
Adoptar de forma explícita la estrategia:
**COTS for Bench Learning → Independent Flight-Like Design**.

Para `EPS_Bench1_1S`:
- Usar CN3065 + BMS 1S + Boost 5V + Buck 3V3 como banco funcional.
- Tratar el banco como plataforma de validación, no como diseño de vuelo.
- Mapear cada módulo COTS a una función, objetivo de medición y limitación del
  banco. Una comparación con funciones futuras puede orientar el trade, pero
  nunca acredita equivalencia eléctrica, topológica, ambiental o de vuelo.
- Definir rutas de madurez separadas: `EPS_Bench1_1S` aporta aprendizaje;
  `EPS_Flight_Like` nace de requisitos 2S y reviews propios; `EPS_Flight`
  requiere configuración, calificación y aceptación independientes.

## Alternativas consideradas
1. **Mantener banco COTS sin roadmap formal**
   - Ventaja: menor documentación inmediata.
   - Desventaja: alto riesgo de divergencia con arquitectura de vuelo.
2. **Saltar directo a diseño de vuelo en KiCad**
   - Ventaja: converge antes al hardware final.
   - Desventaja: mayor complejidad, mayor costo y menor velocidad de validación temprana.

## Tradeoffs / riesgos
- **A favor:** rapidez de validación y disponibilidad de hardware de banco.
- **En contra:** módulos de banco no equivalen a calificación espacial.
- **Riesgos técnicos:** falsa sensación de madurez, ausencia de MPPT real en CN3065 y brecha entre cableado de banco y PCB final.

## Implicancias (archivos a actualizar)
- `architecture.md`.
- `docs/EPS/EPS_Bench1_1S.md`.
- `docs/EPS/BOM_EPS_Bench1_1S.md`.
- `06_Costs/eps_bench1_1s_cost_model.md`.
- `07_Risk/eps_bench1_1s_risks.md`.
- `00_MVP/MVP v2.1.md`.
