# Verification Procedure Index — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — procedimientos planificados

Un `ProcedureID` identifica el procedimiento que deberá desarrollarse y
aprobarse antes de TRR. Este índice no es evidencia de ejecución.

| ProcedureID | Alcance | Entregable mínimo | Review de aprobación |
|---|---|---|---|
| PROC-DOC-001 | control de configuración, claims, VCRM, waivers | checklist + diff + acta | SRR/cada review |
| PROC-MECH-001 | envolvente, masa, CG, CAD y fit-check | report + drawings + datos | PDR/FRR |
| PROC-EPS-001 | batería, rails, states, fault containment | esquema/release + report raw | PDR/CDR/TRR |
| PROC-FSW-001 | estados, boot, health, colas y recovery | tests + logs + coverage | CDR/TRR |
| PROC-RF-001 | UHF uplink/downlink, beacon y OTA | budgets + captures + report | PDR/TRR |
| PROC-RF-002 | LoRa RX/slotting/store-forward | calibrated RF test + analysis | TRR |
| PROC-REG-001 | ENACOM/IARU/ITU/ICD | dossier y correspondencia | PDR/FRR |
| PROC-SEC-001 | auth, anti-replay, roles y key recovery | threat model + negative tests | CDR/TRR |
| PROC-GND-001 | aislamiento de estación y ambiente | inspection + interlock tests | TRR |
| PROC-DATA-001 | persistencia, schema, replay y métricas | fixtures + replay/export hashes | TRR |
| PROC-SCI-001 | protocolo científico y análisis | preregistration + statistical report | SRR/post-mission |
| PROC-AI-001 | manifest, dataset y benchmark del modelo | digests + blind/adversarial results | PDR/TRR |
| PROC-AI-002 | integración IA/supervisor/kill/recursos | hardware logs + fault injection | TRR |
| PROC-PH-001 | aislamiento PHOTO_DEMO | failure/saturation tests | TRR si se incluye |
| PROC-ADCS-001 | detumble, pointing y HIL | error budget + Monte Carlo + HIL | PDR/TRR |
| PROC-THR-001 | modelo térmico, interfaces y TVAC | correlated model + raw chamber data | CDR/QAR |
| PROC-MAT-001 | materiales, venting y outgassing | declaration + datasheets/tests | PDR/CDR |
| PROC-RAD-001 | TID/DDD/SEE/SEL | environment + mitigation/test report | PDR/CDR |
| PROC-ENV-001 | vibración, TVAC, EMC, deployment | approved procedures + pre/post data | QAR |
| PROC-COST-001 | BOM, LCC y procurement | audited roll-up + sources | cada review |
| PROC-REV-001 | entrada/salida de reviews | minutes + actions + signatures | cada review |

Cada procedimiento ejecutado deberá registrar:

- revisión del procedimiento;
- artículo/serial/lote y `ConfigurationID`;
- equipos de prueba y calibración;
- fecha, operadores y condiciones;
- datos raw inmutables y digest;
- cálculo reproducible;
- resultado por ReqID;
- anomalías, NCR/waiver y aprobación.
