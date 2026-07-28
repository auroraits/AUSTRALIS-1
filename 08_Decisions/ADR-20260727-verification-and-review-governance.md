# ADR-20260727-verification-and-review-governance

- **Fecha:** 2026-07-27
- **Estado:** Accepted

## Contexto

Gate A se declaró completo pese a contradicciones de configuración. Los
requisitos carecían de criterios de aceptación y no existía trazabilidad
completa hacia procedimientos, evidencia y riesgos. El plan permitía readiness
con bloqueantes y ensayos ambientales opcionales.

## Decisión

1. Gate A se reabre y queda `Open`.
2. Se adopta una VCRM (Verification Cross-Reference Matrix) machine-readable:
   `ReqID → lifecycle → método → criterio → ProcedureID → configuración
   → EvidenceID/hash → estado → riesgo → gate`. El lifecycle distingue
   requisitos activos de propuestas trazadas aún no adoptadas.
3. Estados de verificación permitidos:
   `Open | Planned | Implemented | Verified | Waived | Blocked by Integrator`.
   Solo `Verified` significa requisito cerrado; `Waived` exige autoridad,
   justificación y riesgo residual.
4. Se adopta la secuencia mínima:
   `SRR → PDR → CDR → TRR → Qualification/Acceptance Review → FRR`.
5. Gate integrado exige dependencias previas completas; “versión preliminar”
   no sustituye un gate. Toda excepción requiere waiver formal.
6. Random vibration, shock si aplica por ICD, thermal cycling/TVAC, EMC,
   despliegue y end-to-end RF son parte del programa de verificación; no se
   cierran como “si disponibles”.
7. Readiness no puede declararse con un ítem de seguridad, regulación,
   integración o lanzamiento en `Open` o `Blocked by Integrator`.
8. Owners son roles responsables hasta asignación nominal; la aprobación de
   cada review requiere registro de autoridad, fecha y configuración.

## Implicancias

- Reestructurar requisitos, compliance, gates, riesgos y evidence pack.
- Un análisis preliminar puede apoyar diseño, pero no verificar un requisito
  sin criterio y evidencia controlada.
