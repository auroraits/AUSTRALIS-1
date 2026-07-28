# COMMS/OPS — Riesgo de TLE y predicción de pasadas

**Revisión:** 2026-07-27
**Estado:** Active

| ID | ParentRiskID | Riesgo | Prob. | Impacto | Owner role | Mitigación | Trigger | Due gate |
|---|---|---|---|---|---|---|---|---|
| OPS-TLE-01 | RSK-COMMS-03 | TLE viejo desplaza ventana | Media | Alta | Node FW/Ground | convertir error/edad a incertidumbre de tiempo/elevación; invalidar según budget | error excede allocation | Gate B |
| OPS-TLE-02 | RSK-COMMS-03; RSK-SEC-02 | Fuente falsa/object ID incorrecto/rollback | Media | Alta | Security/Node/Ground | fuente autenticada, object ID, expiry y monotonic update | firma/ID/epoch inválidos | Gate B |
| OPS-TLE-03 | RSK-COMMS-02; RSK-REG-01 | Fallback B1 eleva airtime/interferencia | Media | Alta | COMMS/Regulatory | análisis regulatorio/energético y rate limit antes de habilitar | duty/airtime supera autorización | Gate B |

Los umbrales fijos de edad no sustituyen un error budget.
