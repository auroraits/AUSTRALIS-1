# Índice consolidado de remediación de auditoría — 2026-07-27

**Rama:** `audit/remediation-2026-07-27`  
**Estado:** registro de disposición; no constituye evidencia de vuelo ni cierre
de requisitos  
**Cobertura:** cuatro informes originales: sistema/documentación, COMMS/RF,
software y hardware/EPS/estructura/SIM

## 1. Regla de interpretación

Este índice registra qué se hizo con **cada hallazgo original**. La disposición
de una fila no debe confundirse con el estado de verificación de un requisito:
los estados autoritativos de V&V continúan en
`01_Mission/verification_cross_reference_matrix.csv`.

Cada fila usa exactamente una de estas disposiciones:

- `CORRECTED`: el defecto concreto de fuente, cálculo, software o control
  documental fue corregido y existe una comprobación adecuada a ese defecto.
  No otorga crédito a un diseño físico o ensayo que todavía no existe.
- `CONTROLLED OPEN`: se retiró el cierre falso y el trabajo faltante quedó
  ligado a requisito, riesgo, procedimiento o gate. Sigue abierto hasta aportar
  implementación y evidencia aceptable.
- `SUPERSEDED-EVIDENCE`: el artefacto o resultado anterior fue invalidado como
  evidencia y no puede transferirse a la configuración vigente. Una eventual
  repetición sigue abierta.
- `BLOCKED-EXTERNAL`: la condición de cierre depende principalmente de una
  autoridad, integrador, ICD, coordinación o revisión profesional externa. La
  documentación interna no sustituye esa decisión.

Los registros de frente
`docs/SYSTEM_GOVERNANCE_AUDIT_REMEDIATION_2026-07-27.md` y
`docs/EPS/HARDWARE_AUDIT_REMEDIATION_2026-07-27.md` aportan detalle adicional;
este documento conserva, aun así, una fila por cada punto original.

## 2. Resumen de cobertura y disposición

| Frente original | Hallazgos inventariados |
|---|---:|
| Sistema y documentación | 42 |
| COMMS/RF/regulatorio/ground | 25 |
| Software/IA/ground/embedded/SIM | 20 |
| Hardware/EPS/estructura/SIM | 33 |
| **Total** | **120** |

| Disposición | Cantidad |
|---|---:|
| `CORRECTED` | 49 |
| `CONTROLLED OPEN` | 48 |
| `SUPERSEDED-EVIDENCE` | 19 |
| `BLOCKED-EXTERNAL` | 4 |
| **Total** | **120** |

## 3. Sistema y documentación — 42/42

### Críticos

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| SYS-C01 | Resultados de Granite 3.1 2B atribuidos a Granite 350M. | `SUPERSEDED-EVIDENCE` | `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md` y los scripts Granite están invalidados; `08_Decisions/ADR-20260727-ai-payload-gemma4-e2b-candidate.md`, `IA-REQ-10/11` hacen de `gemma4:e2b` un candidato no validado y prohíben transferir métricas. |
| SYS-C02 | El éxito mínimo por conteos no probaba la hipótesis científica ni seguridad/utilidad de la IA. | `CONTROLLED OPEN` | `01_Mission/mission_definition.md` §§3–4 y `08_Decisions/ADR-20260727-mission-scientific-experiment-baseline.md` exigen hipótesis, control, oráculo, métricas, tamaño muestral y análisis; `SYS-REQ-01`, `MIS-REQ-16/17`, `PROC-AI-001`. El experimento aún no fue prerregistrado ni ejecutado. |
| SYS-C03 | MVP v2.2 contenía simultáneamente SmolLM2 y Granite como baselines vigentes. | `CORRECTED` | `00_MVP/MVP v2.2.md` tiene una única configuración vigente y remite al candidato `gemma4:e2b`; la autoridad se fija en la ADR de candidato IA. |
| SYS-C04 | La ADR orbital Accepted se contradecía entre 600/650 km y LTAN 10:00/9:30. | `SUPERSEDED-EVIDENCE` | `08_Decisions/ADR-20260727-orbit-attitude-analysis-reopened.md` supersede el cierre anterior; `RSK-ORB-01`, `ORB-REQ-01`, `PROC-ORB-001` mantienen órbita y actitud abiertas. |
| SYS-C05 | El barrido denominado SSO no imponía la precesión heliosincrónica. | `CORRECTED` | `05_Software/SIM/borealis_3d_viewer_v9_3_6rad_export.html` deriva inclinación SSO por altitud; `05_Software/SIM/validate_simulation.py` comprueba, entre otros, `iSSO(600/650)=97.787670/97.985997°`. |
| SYS-C06 | CSV archivado, fila seleccionada, radiador y conclusión de la ADR no coincidían. | `SUPERSEDED-EVIDENCE` | Los CSV y la selección orbital/térmica previos quedaron no admisibles en las ADR de reapertura orbital y térmico-potencia; el SIM actual exporta manifest/digest, pero no selecciona configuración. Ver también el registro hardware §§2, 4–5. |
| SYS-C07 | El margen energético 3.4–3.6× no era un balance total y mezclaba unidades/cargas. | `SUPERSEDED-EVIDENCE` | `08_Decisions/ADR-20260727-thermal-power-baselines-reopened.md` invalida el margen; `03_Power/Power Budget.md`, `03_Power/power_budget.py`, `PWR-REQ-01`, `PROC-PWR-001`, `RSK-PWR-01` controlan el nuevo ledger. Entradas medidas BOL/EOL siguen abiertas. |
| SYS-C08 | El strap térmico de contingencia no alcanzaba la conductancia exigida. | `CONTROLLED OPEN` | La red y el cálculo fueron corregidos en la ADR térmica; `THR-REQ-02`, `PROC-THR-001`, `RSK-THR-01` exigen geometría real, contactos, spreading y ensayo calorimétrico. No hay strap seleccionado ni medido. |
| SYS-C09 | El anodizado blanco fallback violaba sus propios límites α/ε. | `CONTROLLED OPEN` | La ADR térmica retiró la equivalencia; `THR-REQ-01/04`, `PROC-MAT-001`, `PROC-THR-001`, `RSK-MAT-01` requieren cupón as-built, valores degradados y outgassing. Material final abierto. |
| SYS-C10 | No existía una ruta formal de revisiones/calificación y “si aplica” permitía readiness sin ambiente. | `CONTROLLED OPEN` | `01_Mission/validation_plan_and_stage_gates.md` y `08_Decisions/ADR-20260727-verification-and-review-governance.md` fijan SRR→PDR→CDR→TRR→Q/AR→FRR y bloquean FRR; `ENV-REQ-01`, `PROC-ENV-001`, `RSK-ENV-01`. Programa físico e ICD siguen abiertos. |

### Altos

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| SYS-A01 | No había trazabilidad requisito→V&V→riesgo. | `CORRECTED` | `01_Mission/verification_cross_reference_matrix.csv`, `verification_procedure_index.md` y `tools/validate_repository.py` verifican cobertura, IDs y estados; ninguna fila recibe por ello estado `Verified`. |
| SYS-A02 | Los requisitos carecían de criterios de aceptación SMART. | `CORRECTED` | `01_Mission/requirements_matrix.md` incorpora criterio de aceptación, método, fuente, owner y lifecycle para cada ReqID; VCRM uno-a-uno y validador estructural. Los parámetros físicamente TBD permanecen abiertos. |
| SYS-A03 | La compliance matrix usaba estados fuera de su propio modelo. | `CORRECTED` | `01_Mission/compliance_matrix.md`, `compliance_cross_reference_matrix.csv` y `tools/validate_repository.py` normalizan/validan estados y trazabilidad. |
| SYS-A04 | Gate A estaba cerrado pese a contradicciones de configuración. | `CORRECTED` | Gate A fue reabierto en `validation_plan_and_stage_gates.md`; `RSK-CONF-01`, `SYS-REQ-02/04/05` impiden cierre por evidencia preliminar. |
| SYS-A05 | Las dependencias de gates permitían saltar madurez mediante versiones preliminares. | `CORRECTED` | El DAG estricto y los criterios de entrada/salida están en `validation_plan_and_stage_gates.md` y la ADR de gobierno de verificación; waivers requieren riesgo residual. |
| SYS-A06 | Benchmark IA de 7 casos, tolerante a mismatches, se usaba como mitigación de seguridad. | `SUPERSEDED-EVIDENCE` | El scorer, holdout y resultado marzo están invalidados/quarantined; `05_Software/AI PAYLOAD/AgenticBenchmarkRunner_v1.py` y sus tests son una herramienta `Proposed/diagnostic`, no evidencia del candidato. |
| SYS-A07 | El log IA no podía reproducir una inferencia ni correlacionar su efecto. | `CONTROLLED OPEN` | `mission_definition.md` §8, `IA-REQ-07`, `MIS-REQ-17`, `PROC-AI-001` exigen raw input/output, hashes, runtime/decoding, supervisor, energía/térmica, acción y postestado. Implementación de vuelo abierta. |
| SYS-A08 | CM5/modelo se promovían antes de cerrar COTS-to-flight, radiación y fault containment. | `CONTROLLED OPEN` | La ADR Gemma lo limita a candidato; `IA-REQ-09/10`, `RAD-REQ-01`, `PROC-RAD-001`, `RSK-AI-01`, `RSK-RAD-01`. No hay promoción flight-ready. |
| SYS-A09 | El requisito térmico de batería cubría descarga pero no carga. | `CONTROLLED OPEN` | `THR-REQ-03`, ADR térmica, `PROC-THR-001` y `RSK-THR-02` separan carga/descarga/storage/survival e interlocks; celda, límites y TVAC siguen abiertos. |
| SYS-A10 | `EPS_STATE` era una taxonomía sin máquina de estados verificable. | `CONTROLLED OPEN` | `EPS-REQ-01`, `PROC-FSW-001`, `RSK-FSW-01` requieren thresholds, histéresis, dwell, boot/unknown, sensor inválido y pruebas de frontera. La ADR histórica no recibe crédito de implementación. |
| SYS-A11 | Link budget UHF Accepted dependía de sensibilidad, pérdidas y PA no demostrados. | `SUPERSEDED-EVIDENCE` | La ADR 20260218 quedó antecedente superseded; `04_Communications/link_budget_uhf_preliminary.md`, `docs/COMMS/uhf_ttc_bench_testing_plan.md`, `PROC-RF-001`, `RSK-RF-01` mantienen mediciones y cierre OTA abiertos. |
| SYS-A12 | La decisión de concentrador LoRa no demostraba la ventaja de sensibilidad y chocaba con BW posterior. | `SUPERSEDED-EVIDENCE` | La ADR LoRa 20260220 quedó superseded por `ADR-20260727-rf-regulatory-command-security-baseline.md`; `rf_subsystem_overview.md`, protocolo y plan `PROC-RF-002` tratan receptor/BW/canales como trade y ensayo abiertos. |
| SYS-A13 | Faltaban requisitos de autenticación e anti-replay. | `CONTROLLED OPEN` | `SEC-REQ-01/02`, `MIS-REQ-11/18/20`, `COMMS-UL-07`, `04_Communications/uhf_command_security_protocol.md`, `PROC-SEC-001`; implementación, key management y pruebas de artículo siguen abiertas. |
| SYS-A14 | El risk register no tenía owners/triggers/gates y cerraba riesgos con evidencia inválida. | `CORRECTED` | `07_Risk/top_risks.md` contiene riesgos abiertos con P/I, owner role, trigger, due gate y cierre exigido; `tools/validate_repository.py` comprueba referencias VCRM/riesgo. |
| SYS-A15 | BOM/costos no permitían evaluar viabilidad económica. | `CONTROLLED OPEN` | `06_Costs/BOM_master.csv`, `life_cycle_cost_register.csv`, `cost_overview.md`, `PROC-COST-001`, `RSK-COST-01` dan estructura y reserva; precios, FX, quotes y total viable siguen `TBD`, sin cifras inventadas. |
| SYS-A16 | BOM mezclaba gates/alternativas y clasificaba bajo riesgo sin MPN/evidencia. | `CORRECTED` | La BOM de 27 columnas usa ItemID, stage, ReqID/RiskID/ProcedureID, selección y supply status explícitos; alternativas no equivalentes y placeholders no reciben crédito de vuelo. |
| SYS-A17 | Estación meteorológica se convirtió en shall desde un Draft sin ADR Accepted. | `CORRECTED` | `MIS-REQ-22` volvió a `Proposed — EGSE`; `ground_station_dual_use_satnogs_australis.md` sigue Draft y exige ADR/hazard analysis antes de adopción. |
| SYS-A18 | Las inhibiciones RF congelaban una interpretación no controlada del CDS. | `CORRECTED` | `COMP-REQ-02`, compliance/VCRM y `ADR-20260727-cubesat-1p5u-cds-envelope.md` separan mínimos CDS de restricciones adicionales `Blocked by Integrator`. |

### Medios y de gobierno

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| SYS-M01 | ADRs UHF/LoRa usaban estado híbrido “Accepted (preliminar)”. | `CORRECTED` | `08_Decisions/INDEX.md` y headers ADR usan un único estado formal; decisiones antiguas quedaron `Superseded` y los análisis técnicos `Preliminary`. |
| SYS-M02 | Cuatro ADR de 2026-02-12 carecían de fecha/estado formal al inicio. | `CORRECTED` | Los cuatro archivos tienen metadata formal y aparecen en `08_Decisions/INDEX.md`; el validador comprueba estados y objetivos de supersession. |
| SYS-M03 | MVP v1.x/v2.0/v2.1 seguían presentándose como vigentes/finales. | `CORRECTED` | Todas las revisiones históricas tienen banner `Historical/Superseded`; la única autoridad operativa es `00_MVP/MVP v2.2.md`. |
| SYS-M04 | Había `filecite` corruptos y una referencia a v1.2 inexistente en historia documental. | `SUPERSEDED-EVIDENCE` | Las revisiones afectadas están explícitamente históricas y no son fuente de evidencia; referencias activas se resolvieron. No se reescribió historia para aparentar provenance inexistente. |
| SYS-M05 | MVP v2.2 conservaba fecha de corte anterior a addenda posteriores. | `CORRECTED` | `MVP v2.2.md` fue emitido como revisión atómica vigente y elimina el patrón de addenda contradictoria. |
| SYS-M06 | `architecture.md` declaraba sincronización vieja y conservaba resultados térmicos incompatibles. | `CORRECTED` | `architecture.md`, `SYSTEM_BASELINE.md`, MVP y ADRs activas remiten a baselines reabiertos y no publican el CSV viejo como resultado vigente. |
| SYS-M07 | Requisitos térmicos y valores Accepted se contradecían (CM5/batería). | `SUPERSEDED-EVIDENCE` | Los números previos quedaron invalidados; `THR-REQ-01/02/03`, ADR térmica y SIM incompleto requieren nueva configuración/correlación. |
| SYS-M08 | “Deshabilitar IA en cualquier momento” era físicamente imposible fuera de contacto. | `CORRECTED` | `IA-REQ-08` separa kill local autónomo y comando autenticado en la siguiente oportunidad de enlace, con latencia por definir/verificar. |
| SYS-M09 | Documento de time sync aún permitía NTP contra el baseline posterior. | `CORRECTED` | `ADR-20260313-b2-uplink-timebase-requirement.md`, `COMMS-UL-02` y documentos TLE/scheduler exigen base temporal validada y fail-silent; ninguna fuente de tiempo recibe aceptación por nombre. |
| SYS-M10 | Owners de gates eran tentativos, sin responsables nominales ni autoridad/firma. | `CONTROLLED OPEN` | `SYS-REQ-06`, `RSK-PROG-01` y plan de reviews asignan owner roles y exigen nombre, autoridad, fecha y firma antes de cada review; nominaciones aún abiertas. |
| SYS-M11 | Informes de auditoría de marzo parecían actuales aunque sus entradas habían cambiado. | `SUPERSEDED-EVIDENCE` | `docs/informe_revision_integral_nanosat_2026-03-12.md` y su CSV están identificados como snapshots históricos; este índice y los registros de frente controlan la disposición vigente. |
| SYS-M12 | PHOTO_DEMO mezclaba heurísticas técnicas con conclusiones legales. | `BLOCKED-EXTERNAL` | `07_Risk/PHOTO_DEMO_remote_sensing_threshold_risk_matrix.md` declara sus umbrales heurísticos/no estatutarios; `RSK-PH-01`, `PROC-PH-001` requieren especialista/autoridad. |
| SYS-M13 | El mirror ya era público mientras auditorías legales/publicación conservaban blockers previos. | `CONTROLLED OPEN` | `PUBLIC_RELEASE_PROCESS.md`, `PUBLICATION_AUDIT.md` y `LEGAL_ENFORCEMENT_REVIEW.md` distinguen snapshots y exigen sign-off/claim scan por release; la disposición retrospectiva no equivale a aprobación legal. |
| SYS-M14 | Licencia, titular, SPDX, contacto comercial, SBOM y provenance legal eran incompletos. | `BLOCKED-EXTERNAL` | `LICENSE.md`, `COMMERCIAL_USE.md`, proceso de release y `RSK-LEGAL-01` dejan titular/contacto/chain-of-title/revisión profesional abiertos; no se concede permiso por inferencia. |

## 4. COMMS/RF/regulatorio/ground — 25/25

### Críticos

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| COM-C01 | Uplink LoRa 915 MHz Tierra→espacio sin atribución/autorización demostrada. | `BLOCKED-EXTERNAL` | `04_Communications/regulatory_gate_rf.md`, ADR RF, `MIS-REQ-03/04`, `COMP-REQ-04`, `PROC-REG-001`, `RSK-REG-02`: operación radiada queda inhibida hasta respuesta escrita ENACOM/coordinación aplicable. RX-only orbital no autoriza al nodo terrestre. |
| COM-C02 | TTC y prompt uplink permitían comandos sin protocolo concreto de autenticación/anti-replay. | `CONTROLLED OPEN` | `uhf_command_security_protocol.md`, `SEC-REQ-01/02`, `MIS-REQ-11/18/20`, `PROC-SEC-001`, `RSK-SEC-01/02`; el contrato está especificado, pero implementación, provisioning, rotación, recovery y suite en artículo siguen abiertos. |

### Altos

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| COM-H01 | “435 MHz” se usaba como carrier literal en el borde de 435–438 MHz. | `CORRECTED` | `rf_subsystem_overview.md`, link budget UHF, ADR RF y `MIS-REQ-03` usan frecuencia coordinada TBD dentro de la banda, con guard para ocupación, tolerancia y Doppler. |
| COM-H02 | El camino amateur-satellite omitía licencia responsable, autorización espacial, UIT, identificación y límites de contenido. | `BLOCKED-EXTERNAL` | `regulatory_gate_rf.md`, `satnogs_public_beacon_architecture.md`, `COMP-REQ-04`, `PROC-REG-001`, `RSK-REG-01` enumeran expediente ENACOM/IARU/UIT e identificación; aprobación y criterio jurídico sobre contenido/autenticación siguen externos. |
| COM-H03 | Geometría/FSPL y margen a 20° del link budget UHF eran incorrectos. | `CORRECTED` | `04_Communications/link_budget_uhf_preliminary.md` y `docs/COMMS/rf_calculations.py --self-test` usan slant range esférico y curvas 550/600/650 km; la medición física permanece abierta bajo `PROC-RF-001`. |
| COM-H04 | Sensibilidad, pérdidas, BER/PER, disponibilidad e incertidumbre UHF no estaban demostradas. | `CONTROLLED OPEN` | Link budget se limita a `Preliminary`; `docs/COMMS/uhf_ttc_bench_testing_plan.md`, `PROC-RF-001`, `RSK-RF-01` exigen EIRP, sensibilidad, G/T, patrón, PER y peor caso medidos. |
| COM-H05 | Faltaba link budget independiente del uplink UHF. | `CONTROLLED OPEN` | El link budget y plan UHF separan Tierra→satélite de satélite→Tierra; inputs de estación/receptor, peor orientación, Doppler y PER aún requieren medición y autorización. |
| COM-H06 | Doppler y waveform UHF no estaban especificados para compatibilidad/ancho ocupado. | `CONTROLLED OPEN` | `rf_subsystem_overview.md`, link budget y `uhf_ttc_bench_testing_plan.md` controlan desviación, BW, AFC/TCXO, preámbulo, coding/FEC, framing y Doppler; selección/ensayo RF siguen abiertos. |
| COM-H07 | Un monopolo +Z podía colocar su nulo axial hacia la estación. | `CONTROLLED OPEN` | `rf_subsystem_overview.md`, `STR-REQ-02`, `ADCS-REQ-02`, `PROC-RF-001` requieren geometría, patrón 3D integrado, polarización, pointing/body loss y OTA; antena/despliegue no seleccionados. |
| COM-H08 | ToA LoRa y capacidad de slots usaban preámbulo equivocado. | `CORRECTED` | `uplink_lora_slotted_protocol.md` y `rf_calculations.py --self-test` calculan el ToA desde PHY exacta y eliminan 145/300 slots como cifras aceptadas. |
| COM-H09 | Conflicto BW125/BW250 y canales solapados sin ADR superseding. | `CORRECTED` | ADR RF supersede la decisión 20260220; protocolo y plan de ensayo condicionan canalización a BW exacto y prohíben tratar canales solapados como diversidad. |
| COM-H10 | El frame LoRa no probaba origen ni el criterio experimental era reproducible. | `CONTROLLED OPEN` | `COMMS-UL-07`, `MIS-REQ-04/05`, `uplink_lora_slotted_protocol.md`, `PROC-RF-002`, `RSK-SEC-03` exigen identidad/versionado, MIC, anti-replay, provisioning, denominador, condiciones e IC. Implementación/experimento abiertos. |
| COM-H11 | Slotting podía producir colisiones persistentes y capacidad sobreestimada. | `CONTROLLED OPEN` | `COMMS-UL-06`, protocolo, `docs/COMMS/uplink_lora_bench_testing_plan.md` y `PROC-RF-002` exigen modelo/Monte Carlo y pruebas collision/near-far/retry; no hay capacidad adoptada. |
| COM-H12 | Faltaba presupuesto de datos end-to-end y había riesgo de starvation. | `CONTROLLED OPEN` | `uplink_data_products_and_downlink_policy.md`, `COMMS-UL-05`, `MIS-REQ-09`, `PROC-RF-001/002`, `RSK-DATA-01` exigen producción, overhead, contactos, retención, cuotas/aging y no-starvation. |
| COM-H13 | El plan LoRa no podía cerrar sensibilidad, Doppler dinámico, PDR/confianza, interferencia ni OTA/EMC. | `CONTROLLED OPEN` | `docs/COMMS/uplink_lora_bench_testing_plan.md` incorpora fuente calibrada, ramp Doppler, esquinas, muestra/IC, near-far/blocking, coexistencia y OTA; ejecución permanece bloqueada por selección y gate regulatorio. |

### Medios y estado de hardware

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| COM-M01 | Link budget LoRa repetía geometría errónea y sensibilidad de un receptor distinto. | `CORRECTED` | `link_budget_lora_uplink_preliminary.md` usa geometría corregida y separa receptor de referencia del hardware final; su estado sigue `Preliminary` y la sensibilidad del módulo exacto queda en `PROC-RF-002`. |
| COM-M02 | SX1302/SX1303 HAT/BOM/front-end/TCXO no eran una configuración coherente. | `CONTROLLED OPEN` | `rf_subsystem_overview.md`, BOM y plan LoRa tratan concentrador, front-end, reloj y receptor completo como selección/configuración a medir; ningún HAT de banco recibe crédito de vuelo. |
| COM-M03 | EMC/coexistencia UHF–LoRa–EPS–CM5 solo se trataba cualitativamente. | `CONTROLLED OPEN` | Planes UHF/LoRa y `ENV-REQ-01`, `PROC-ENV-001`, `PROC-RF-001/002`, `RSK-RF-02` exigen matriz de modos, aislamiento, blockers, espurias, desense y noise floor integrados. |
| COM-M04 | La seguridad de la ground station era política, no una frontera física demostrada. | `CONTROLLED OPEN` | `ground_station_dual_use_satnogs_australis.md`, `docs/COMMS/ground_station_verification_plan.md`, `MIS-REQ-21`, `PROC-GND-001`, `RSK-GND-01/02` exigen RX-only dedicado, PTT gate/arm físico, permisos y fault injection. |
| COM-M05 | La BOM de estación omitía rotor, T/R, PA/filtros, protección, tiempo, energía y estructura. | `CONTROLLED OPEN` | `06_Costs/BOM_master.csv`, `bom_overview.md`, diseño y plan ground incorporan placeholders trazables; MPN, cantidades, costos, integración y ensayo siguen TBD. |
| COM-M06 | El power model half-duplex sumaba 60% TX + 60% RX y subestimaba el rail. | `CORRECTED` | `03_Power/Power Budget.md` y `power_budget.py --self-test` modelan estados/modos y conversiones sin simultaneidad imposible; potencias medidas del radio final siguen abiertas bajo `PWR-REQ-01`. |
| COM-M07 | TLE/scheduler carecían de autenticidad, anti-rollback y error budget; fallback B1 era inseguro. | `CONTROLLED OPEN` | `05_Software/node_tle_update_mechanism.md` y `node_uplink_scheduler_pass_prediction.md`, `COMMS-UL-02/03`, `PROC-RF-002`, `RSK-COMMS-03` especifican envelope firmado, A/B atómico, error medido, ventana recortada y fail-silent. Implementación y campaña abiertas. |
| COM-M08 | “Deshabilitar IA en cualquier momento” no era verificable con contacto LEO intermitente. | `CORRECTED` | `IA-REQ-08` y ADR Gemma distinguen disable local de comando aplicable en próxima oportunidad autenticada; la seguridad no depende del uplink. |
| COM-M09 | La herencia OpenLST/Dove se transfería indebidamente a una placa modificada. | `CORRECTED` | `RF_ANALISYS_OPENLST.md` y `rf_subsystem_overview.md` están `Preliminary`, tratan OpenLST como referencia/candidato y exigen revalidación completa de PA/SAW/layout/waveform. |
| COM-M10 | El proyecto KiCad RF era un placeholder vacío que no podía sostener claims de diseño. | `CONTROLLED OPEN` | `04_Communications/PCBs/Satellite RF KiCad/README.md` lo bloquea como `Placeholder / not fabricable`; `EPS-REQ-02`, `PROC-RF-001` y criterios de reemplazo requieren esquema, ERC, layout, DRC y ensayos reales. |

## 5. Software/IA/ground/embedded/SIM — 20/20

### Críticos

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| SW-C01 | Pipeline 2B se presentaba como validación de Granite 350M. | `SUPERSEDED-EVIDENCE` | Scripts Granite y registro marzo están explícitamente invalidados y bloqueados por guard; ADR Gemma e `IA-REQ-10/11` prohíben reutilizar resultados. Granite 350M queda fuera del candidato actual, sin afirmar que fue evaluado. |
| SW-C02 | Dataset tenía duplicados, estados/políticas inválidos y holdout contaminado. | `SUPERSEDED-EVIDENCE` | `cubesat_granite_dataset_schema.md`, corpus y holdout son históricos/no admisibles; `AGENTIC_DATASET_SCHEMA.md` define split por escenarios/provenance/metadata. No existe aún corpus científico aprobado para Gemma. |
| SW-C03 | Scorer histórico aprobaba fallos de seguridad y el holdout no tenía oráculo/assertions. | `SUPERSEDED-EVIDENCE` | `benchmark_granite_lora_vs_base_corrected.py`, `test_granite_lora_holdout.py` y PowerShell legacy están quarantined; el 1/7→4/7 no se usa como mitigación ni evidencia. |
| SW-C04 | El benchmark agentic podía dar 100/100 a tools inválidas, ausencia de acción y valores cero mal leídos. | `CORRECTED` | `AgenticBenchmarkRunner_v1.py` aplica JSON estricto, schemas/tool allowlists, tipos/rangos, clases OBC, pre/postcondiciones y hard-fail; `tests/test_agentic_benchmark_runner.py` cubre casos adversariales. Sigue siendo diagnóstico `Proposed`, no validación del modelo. |
| SW-C05 | El simulador software llamaba SSO a órbitas que no preservaban LTAN. | `CORRECTED` | `05_Software/SIM/validate_simulation.py` y el HTML actual imponen precesión solar por altitud; la selección orbital permanece abierta en ADR orbital/`PROC-ORB-001`. |

### Embedded y banco 433

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| SW-H06 | Tasas declaradas de 20 Hz RF/100 Hz eran imposibles con 41 bytes a 2 kbps y envío bloqueante. | `CORRECTED` | `telemetry_tx.ino`, `docs/TELEMETRY_433_README.md`, `ADR-20260727-telemetry-bench-433-v4.md` separan filtro 100 Hz de RF 2 Hz; `validate_telemetry_bench.py` comprueba payload/airtime/período. |
| SW-H07 | El trigger de riesgo miraba `send()` fail aunque la pérdida real aparecía en RX. | `CORRECTED` | `07_Risk/telemetry_433_bench_risks.md` usa PER, gaps, duplicates/out-of-order y evidencia RX; dashboard/registrador conservan los contadores. |
| SW-H08 | El remapeo sensor→body tenía determinante −1 y no permitía permutar ejes. | `CORRECTED` | Firmware usa matriz 3×3 controlada; `validate_telemetry_bench.py` exige ortonormalidad y determinante +1. La calibración física del montaje sigue siendo evidencia de banco, no ADCS de vuelo. |
| SW-H09 | La documentación de Madgwick omitía que un acelerómetro en caída libre no referencia roll/pitch orbital. | `CORRECTED` | `embedded/common/filters/MadgwickAHRS.h`, README 433 y ADR de banco limitan la interpretación a bench; ninguna salida se promueve a ADCS orbital. |
| SW-H10 | `platformio.ini` no apuntaba al árbol real y no había compilación reproducible. | `CONTROLLED OPEN` | `05_Software/embedded/esp32_s3_tx_telemetry/platformio.ini` y `05_Software/embedded/uno_rx_logger/platformio.ini` fijan `src_dir` por proyecto; `.github/workflows/validation.yml` define PlatformIO 6.1.19 para ambos entornos. El build CI del head vigente debe quedar verde antes de recibir crédito de compilación. |

### Ground software

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| SW-G11 | La solución compilaba pero no tenía pruebas automatizadas. | `CORRECTED` | `GroundTelemetryDashboard.Tests/TelemetryPipelineTests.cs`, proyecto de tests y workflow ejecutan parser, estadísticas, evidencia, tamper y control token; esto no reemplaza prueba E2E con hardware. |
| SW-G12 | Dashboard guardaba datos solo en RAM y no producía evidencia persistente. | `CORRECTED` | `EvidenceRecorder.cs`, `EvidenceVerifier.cs` y `ground_data_architecture.md` implementan raw/clasificado append-only, manifest, close seal y hash local. Firma externa, timestamp confiable y provenance de build permanecen acciones abiertas explícitas. |
| SW-G13 | PER inferida por gaps confundía reboot, wrap, duplicados y reordenamiento. | `CORRECTED` | `StatsCalculator.cs`, schema V4 con `boot_id`, clock monotónico y tests distinguen sesión, wrap, duplicate, out-of-order y time regression. |
| SW-G14 | El parser aceptaba sintaxis sin rangos, finitud, quaternion, versión/unidades/calidad. | `CORRECTED` | `SerialLineParser.cs`, `TelemetrySample.cs`, protocolo V4 y tests validan versión/layout, finite/ranges, sensor/quality flags, `dt_ms` y norma de quaternion; datos válidos se etiquetan “uncalibrated”, no calibrados. |
| SW-G15 | Cambiar COM podía mostrar un puerto mientras el proceso leía otro. | `CORRECTED` | `SerialConnectionManager.cs`, `SerialTelemetryHostedService.cs` y `ConnectionStatus.cs` usan generación y estados `REQUESTED→OPENING→OPEN/FAULT`, con reopen y UI conectada solo después de `SerialPort.Open`. |
| SW-G16 | Bind LAN, endpoints de control y dependencias CDN carecían de controles/reproducibilidad. | `CORRECTED` | `appsettings.json` limita hosts a loopback, `Program.cs`/`ControlRequestToken.cs` exigen token aleatorio same-origin para acciones, y Chart.js/SignalR están vendorizados/versionados. Operación remota autenticada no se declara soportada. |

### Reproducibilidad general

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| SW-R01 | Entrenamiento legacy usaba todo como train, sin split/seed/lock/revisión de modelo. | `SUPERSEDED-EVIDENCE` | Pipeline y generador legacy están bloqueados como provenance-only; `AGENTIC_DATASET_SCHEMA.md`, `MODEL_ASSETS.md`, ADR Gemma y `SYS-REQ-01/02` definen condiciones de la futura campaña. |
| SW-R02 | Pesos/adapters no se publicaban y tampoco había manifest/digests para reconstruir evidencia. | `CONTROLLED OPEN` | `MODEL_ASSETS.md` exige digest de bytes/tokenizer/runtime/dataset/config; runner genera manifest diagnóstico. El bundle exacto de `gemma4:e2b`, licencia y artefactos de una campaña aceptable aún debe producirse. |
| SW-R03 | Transporte OBC↔IA carecía de framing/límites/reset/retry y un campo `auth` podía fingir autoridad. | `CONTROLLED OPEN` | `AI_AGENT_PROTOCOL.md` §7, `IA-REQ-12`, `PROC-AI-002` fijan AIA-UART/1, tamaño, CRC, session/sequence, reset/wrap, idempotencia y auth derivada por OBC. Implementación y suite de transporte siguen abiertas. |
| SW-R04 | No existía una suite automatizada transversal para IA, SIM, ground y embedded. | `CORRECTED` | `.github/workflows/validation.yml` define validación de repositorio/SIM/EPS/RF, tests IA/ground y builds PlatformIO pinned; las suites locales viven en `test_agentic_benchmark_runner.py`, `TelemetryPipelineTests.cs`, `validate_simulation.py` y `validate_telemetry_bench.py`. El workflow debe pasar en cada head y no reemplaza HIL, hardware ni calificación. |

## 6. Hardware/EPS/estructura/SIM — 33/33

| ID | Hallazgo original | Disposición | Evidencia y estado vigente |
|---|---|---|---|
| HW-01 | Envolvente 1.5U modelada como 100×100×150 mm. | `CORRECTED` | `ADR-20260727-cubesat-1p5u-cds-envelope.md`, `MIS-REQ-01`, `COMP-REQ-01`, CAD policy y SIM usan `Z=170.2 ±0.1 mm`; fit-check/ICD siguen abiertos. |
| HW-02 | KiCad EPS contenía cortos explícitos PV+/PV− y batería→rails/GND. | `CORRECTED` | Wires peligrosos retirados; `03_Power/EPS_PCB/EPS_Bench2S_FlightLike/validate_eps_placeholder.py` impone placeholder sin cobre y `NON-FABRICABLE`. No existe aún diseño EPS real. |
| HW-03 | BMS y charger eran conectores/pass-through, sin protección ni CC/CV. | `CONTROLLED OPEN` | Placeholder ya no simula implementación; `MIS-REQ-06`, `COMP-REQ-06`, `EPS-REQ-02`, ADR térmica/BOM, `PROC-EPS-001`, `RSK-EPS-02/03` requieren arquitectura completa y ensayos. |
| HW-04 | Modelo térmico violaba albedo, Kirchhoff, emisión a Tierra, extracción FV y disipaciones. | `CORRECTED` | HTML/SIM corrige balance y `validate_simulation.py` verifica invariantes; modelo declara cargas/properties incompletas y requiere correlación `PROC-THR-001`. |
| HW-05 | Barrido SSO no mantenía sincronismo solar. | `CORRECTED` | Inclinación se deriva de altitud y el validador comprueba tasa/inclinaciones; validación independiente del propagador y selección orbital siguen en `PROC-ORB-001`. |
| HW-06 | Se asumía LVLH perfecto sin ADCS existente. | `CONTROLLED OPEN` | `STR-REQ-02`, `ADCS-REQ-01/02`, `PROC-ADCS-001`, `RSK-ADCS-01` convierten LVLH perfecto en sensibilidad ideal y exigen detumble/pointing/jitter/degraded attitude. |
| HW-07 | PCB EPS vacía se presentaba como fuente de una PCB custom flight-like. | `CONTROLLED OPEN` | README/validador la bloquean como mock-up no fabricable; `EPS-REQ-02`, `PROC-EPS-001` exigen schematic review, ERC, BOM, stackup, DRC y fabrication outputs antes de fabricar. |
| HW-08 | Power-gating estaba bypassed y telemetría flotante. | `CONTROLLED OPEN` | Pass-throughs fueron retirados del placeholder; `IA-REQ-01/02`, `EPS-REQ-02`, `PROC-EPS-001` exigen switches reales, default-off, eFuse/inrush/PGOOD/FAULT y sense Kelvin. |
| HW-09 | Topología solar Accepted no podía cargar 2S ni manejar caras ortogonales con MPPT común. | `CONTROLLED OPEN` | Selección de siete celdas/MPPT común fue retirada; `03_Power/EPS_DESIGN_RULES.md`, Power Budget, `PWR-REQ-01`, `PROC-PWR-001`, `RSK-PWR-01` exigen curvas I–V, strings/MPPT/bypass por configuración. |
| HW-10 | El score orbital cambiaba de significado con el horizonte y usaba min-max/pesos arbitrarios. | `CORRECTED` | SIM elimina `thermalKey`/ranking/min-max y reporta requisitos absolutos y Wh/día; `validate_simulation.py` verifica ausencia de selección automática. |
| HW-11 | CSV/ADR anual no eran reproducibles ni coherentes. | `SUPERSEDED-EVIDENCE` | CSV antiguos están invalidados; export actual liga revisión, inputs, manifest y SHA-256 y se marca `INCOMPLETE_NOT_FOR_DESIGN_DECISIONS`. Rerun/correlación siguen abiertos. |
| HW-12 | ADR orbital contenía dos baselines incompatibles. | `SUPERSEDED-EVIDENCE` | ADR orbital 20260727 supersede la decisión; `RSK-ORB-01`, `ORB-REQ-01`, `PROC-ORB-001` mantienen nominal/envolvente sin congelar. |
| HW-13 | Modelica era obsoleto y no reproducía el HTML/CSV Accepted. | `SUPERSEDED-EVIDENCE` | `BorealisThermalConcept.mo`, README y runner están `Historical Snapshot`/deshabilitados; no pueden cerrar V&V. Fuente activa identificada por manifest SIM. |
| HW-14 | Material fallback térmico no cumplía α≤0.20/ε≥0.88. | `CONTROLLED OPEN` | Equivalencia retirada; `THR-REQ-01/04`, `PROC-MAT-001`, `RSK-MAT-01` exigen selección y cupón medido/degradado. |
| HW-15 | Conductancia térmica no tenía red física trazable y los cálculos pad/strap eran inconsistentes. | `CONTROLLED OPEN` | ADR térmica separa TIM/contact/spreading/fasteners y recalcula geometría; `THR-REQ-02`, `PROC-THR-001` exigen ΔT/ensayo calorimétrico. |
| HW-16 | Seguridad térmica de batería omitía carga, máximo e interlock. | `CONTROLLED OPEN` | `THR-REQ-03`, `PROC-THR-001`, `RSK-THR-02` cubren carga/descarga/storage/survival con celda final y fault tests; selección/TVAC abiertos. |
| HW-17 | Mínimos CDS de deployment switch, RBF, inhibits y timers estaban incompletos/opcionales. | `CONTROLLED OPEN` | `COMP-REQ-02`, compliance/VCRM, `PROC-EPS-001`, `RSK-LAUNCH-01` registran mínimos Rev.14.1 y tiempos; hardware e aceptación del integrador siguen abiertos. |
| HW-18 | Arquitectura/BOM de batería no implementaba el ADR ni un BMS 2S completo. | `CONTROLLED OPEN` | BOM ya no trata ICs 1S/alternativas como BMS completo; `COMP-REQ-06`, `PROC-EPS-001` exigen FMEA, FETs, fusible, secondary OVP, balance, sensores e inhibits. |
| HW-19 | No había CAD, stack, CG/inercia, load path, FEA o despliegue verificable. | `CONTROLLED OPEN` | `02_Structure/CAD/README.md`, `MIS-REQ-01`, `COMP-REQ-01/05`, `PROC-MECH-001`, `RSK-MECH-01` tratan ausencia de CAD como blocker y fijan fit/mass/CG/modes/deployment. |
| HW-20 | Plan ambiental era opcional y sin niveles/ciclos/criterios. | `CONTROLLED OPEN` | `02_Structure/ENVIRONMENTAL_VERIFICATION_PRELIMINARY.md`, `ENV-REQ-01`, `PROC-ENV-001`, `RSK-ENV-01` hacen el programa obligatorio; niveles finales dependen del ICD. |
| HW-21 | No había análisis vigente de TID/DDD/SEE/SEL para COTS. | `CONTROLLED OPEN` | `RAD-REQ-01`, `PROC-RAD-001`, `RSK-RAD-01` exigen entorno, shielding, derating, latch-up/EDAC/scrubbing y test/heritage antes de CDR. |
| HW-22 | Power budget usaba órbita 90 min, omitía cargas/pérdidas y mezclaba dimensiones. | `CONTROLLED OPEN` | `Power Budget.md`/`power_budget.py --self-test` usan órbita física y ledger modal fail-open; `PWR-REQ-01`, `PROC-PWR-001` requieren potencias exactas, inrush, eficiencia, simultaneidad e incertidumbre medidas. |
| HW-23 | Cierre solar ignoraba EOL, radiación/UV, coverglass, mismatch, sombras y fallo de string. | `CONTROLLED OPEN` | Power ledger/design rules y `PWR-REQ-01`, `RAD-REQ-01`, `PROC-PWR-001` exigen BOL/EOL, I–V hot/cold, degradación, MPPT y casos de fallo. |
| HW-24 | Risk register cerraba órbita con evidencia inválida y omitía riesgos principales. | `CORRECTED` | `07_Risk/top_risks.md` reabre `RSK-ORB-01` y agrega ADCS, BMS, ambiente, radiación, launch, mecánica, potencia y seguridad; todos permanecen Open. |
| HW-25 | Masa “típica” CDS 1.5U se declaraba ≤2 kg en vez de 3.00 kg. | `CORRECTED` | Baseline/compliance usan referencia CDS Rev.14.1 de 3.00 kg, subordinada al ICD; masa del artículo sigue TBD. |
| HW-26 | Block Diagram v1.4 obsoleto se podía usar como ICD activo. | `SUPERSEDED-EVIDENCE` | `02_Structure/Block Diagram.md` está `Historical Snapshot / not an active ICD`; interfaces activas deben provenir de baseline/CAD/ICD controlados. |
| HW-27 | Reglas PCB tenían track mínimo 0.25 mm pero default 0.20 mm. | `CORRECTED` | `.kicad_pro` normaliza reglas; release real requiere netclasses por corriente/sense/RF, ERC/DRC y fabricante bajo `EPS-REQ-02`. |
| HW-28 | KiCad RF estaba completamente vacío. | `CONTROLLED OPEN` | README RF declara `Placeholder / not fabricable`; `PROC-RF-001`, `EPS-REQ-02` y checklist exigen netlist, outline, footprints/tracks/zones, ERC/DRC antes de crédito de diseño. |
| HW-29 | Documentos llamaban “promedio” a máximos/mínimos. | `SUPERSEDED-EVIDENCE` | Outputs/manifest actuales nombran extrema/rango; resultados antiguos quedaron históricos y no se reinterpretan como promedio. |
| HW-30 | Áreas/capacidades térmicas no tenían provenance y podían doble-contar masa. | `CONTROLLED OPEN` | SIM exporta parámetros como placeholders; `SYS-REQ-04`, `THR-REQ-01/02`, `PROC-THR-001` requieren derivación desde CAD/BOM/material y correlación. |
| HW-31 | BOM maestra no cerraba masa/volumen/potencia/compliance y omitía Flight/ADCS/harness/safety. | `CONTROLLED OPEN` | BOM incorpora columnas y placeholders trazables para ADCS, pack, launch safety, harness y márgenes; descomposición, selección y roll-ups numéricos siguen TBD bajo `PROC-COST-001`. |
| HW-32 | Citas CDS apuntaban a secciones incorrectas/desactualizadas. | `CORRECTED` | ADR de envolvente, requirements/compliance y registro hardware citan CDS Rev.14.1 §§2.3–2.4, páginas y checksum de fuente. |
| HW-33 | Nombres/fuentes Borealis y AUSTRALIS divergían sin estado de autoridad. | `CORRECTED` | Modelo activo se identifica como `australis-sim-v10-pre`; Borealis queda nombre histórico/snapshot y los manifests declaran source revision/status. |

## 7. Verificación de cobertura y límites

La numeración reproduce la estructura de los informes originales:

- sistema/documentación: `SYS-C01..C10`, `SYS-A01..A18`,
  `SYS-M01..M14` = 42;
- COMMS: `COM-C01..C02`, `COM-H01..H13`, `COM-M01..M10` = 25; `COM-M10`
  conserva el punto adicional “Estado del hardware” que seguía a los nueve
  medios;
- software: `SW-C01..C05`, `SW-H06..H10`, `SW-G11..G16`,
  `SW-R01..R04` = 20; las cuatro filas `SW-R` conservan los defectos adicionales
  de reproducibilidad y automatización señalados después de los numerados;
- hardware: `HW-01..HW-33` = 33.

No se contabilizan como hallazgos las fortalezas verificadas, las descripciones
de alcance ni las limitaciones de la propia auditoría.

Las comprobaciones automatizadas citadas validan software, estructura y
consistencia documental. No sustituyen diseño/fabricación, ERC/DRC sobre una
placa real, CAD/FEA/fit-check, calibración, RF OTA/EMC, TVAC/vibración/shock,
análisis de radiación, validación independiente del propagador, autorización
regulatoria, aceptación del integrador ni revisión legal. Esos ítems permanecen
`CONTROLLED OPEN` o `BLOCKED-EXTERNAL` según la tabla.
