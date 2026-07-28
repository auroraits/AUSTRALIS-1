# COMMS/OPS — Riesgo de TLE y predicción de pasadas

**Revisión:** 2026-07-27
**Estado:** Active

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| OPS-TLE-01 | TLE viejo desplaza ventana | Media | Alta | convertir error/edad a incertidumbre de tiempo/elevación; invalidar según budget | error excede allocation |
| OPS-TLE-02 | Fuente falsa/object ID incorrecto/rollback | Media | Alta | fuente autenticada, object ID, expiry y monotonic update | firma/ID/epoch inválidos |
| OPS-TLE-03 | Fallback B1 eleva airtime/interferencia | Media | Alta | análisis regulatorio/energético y rate limit antes de habilitar | duty/airtime supera autorización |

Los umbrales fijos de edad no sustituyen un error budget.
