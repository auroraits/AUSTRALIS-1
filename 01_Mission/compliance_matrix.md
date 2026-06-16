# Compliance Matrix — AUSTRALIS-1 / DIY Nanosat MVP

**Revisión:** 2026-04-03
**Estado:** Active
**Trazabilidad:** `08_Decisions/ADR-20260313-compliance-matrix-artefacto-sistema.md`

Este es un artefacto vivo del sistema. Debe actualizarse cuando cambian requisitos, se obtiene evidencia o cambia el estado de un ítem.

Estados permitidos:
- `Open` — requisito identificado; sin evidencia aún.
- `Partial` — evidencia parcial o análisis preliminar disponible.
- `Closed` — evidencia completa y verificada.
- `Blocked by Integrator` — depende de ICD/documentación del integrador de lanzamiento (TBD).

---

## 1) Mecánica y compatibilidad de dispenser

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-M-01 | El satélite shall operar en form factor 1.5U (100×100×150 mm). | `MIS-REQ-01`, CDS Rev 14.1 | Estructura | I (Inspection) | Modelo CAD / medición física | Open | Modelo estructural TBD. |
| CX-M-02 | La masa total del satélite shall cumplir el límite del dispenser (típico ≤2 kg para 1.5U; confirmar con integrador). | CDS Rev 14.1; ICD integrador | Estructura | I | Pesada en banco | Blocked by Integrator | Límite exacto depende del integrador. |
| CX-M-03 | El centro de gravedad (CG) shall estar dentro de los límites del dispenser. | CDS Rev 14.1; ICD integrador | Estructura | A+I | Cálculo + medición | Blocked by Integrator | Depende de ICD integrador. |
| CX-M-04 | Los rails, protrusiones, radio de esquinas y roughness superficial shall cumplir CDS Rev 14.1. | CDS Rev 14.1; ICD integrador | Estructura | I | Inspección física | Blocked by Integrator | Depende de ICD integrador. |
| CX-M-05 | Los deployables (antenas) deben ser retenidos por el **CubeSat mismo** antes del deployment. La retención primaria es responsabilidad del CubeSat, no del dispenser/deployer. | CDS Rev 14.1 §3.3.4; ICD integrador | COMMS/Estructura | I+D | Prueba de despliegue | Open | Mecanismo de retención de antenas TBD. |
| CX-M-06 | El fit-check (CIFP — CubeSat Interface and Form-factor Package) shall completarse antes de integración con el dispenser. | ICD integrador | Estructura | D | Evidencia fit-check | Blocked by Integrator | Requiere dispenser del integrador. |
| CX-M-07 | El dossier de ICD, drawings, mass properties y owners shall completarse antes del PDR (Preliminary Design Review) del integrador. | ICD integrador | Sistema | I | Dossier entregado | Open | TBD con integrador. |
| CX-M-08 | El CubeSat shall incluir al menos un deployment switch que interfiera con el deployer/P-POD para inhibir RF y/o deployables durante el lanzamiento. | CDS Rev 14.1 §3.3.2; ICD integrador | COMMS/Estructura | I+T | Prueba de continuidad y función en banco | Blocked by Integrator | Interfaz mecánica y eléctrica depende del deployer ICD. |
| CX-M-09 | RBF (Remove Before Flight) pin o mecanismo equivalente: permite acceder de forma segura a las baterías del CubeSat antes del lanzamiento. | ICD integrador (si aplica) | EPS/Estructura | I | Inspección física | Blocked by Integrator | Requerimiento y forma dependen del integrador. |
| CX-M-10 | Los deployables (antenas) deben tener al menos **dos inhibiciones mecánicas independientes**, ambas controladas por el CubeSat. | CDS Rev 14.1 §3.3.4 | COMMS/Estructura | I+D | Prueba de retención y despliegue | Open | Diseño de mecanismo de retención TBD. |
| CX-M-11 | El CubeSat shall implementar un tiempo mínimo de espera post-eyección antes de activar cualquier deployable. | CDS Rev 14.1; ICD integrador | FSW/Estructura | T | Prueba de secuencia de boot y activación | Blocked by Integrator | Duración exacta depende del integrador. |
| CX-M-12 | Análisis de venteo (venting): el CubeSat no debe contener volúmenes sellados que puedan causar presurización diferencial durante el lanzamiento. | CDS Rev 14.1 §3.2.2.4 | Estructura/EPS | A | Análisis de diseño mecánico + revisión de enclosures | Open | Analizar caja/compartimentos cerrados. |
| CX-M-13 | Los materiales de estructura, PCB, harness y otros componentes shall cumplir los requisitos de outgassing (típicamente TML ≤1% y CVCM ≤0.1%). | ICD integrador; ASTM E595 o equivalente | Estructura/EPS | I+A | Datasheets de materiales + análisis | Blocked by Integrator | Lista de materiales prohibidos del integrador TBD. |
| CX-M-14 | El paquete de documentación de entrega al integrador shall incluir: esquemáticos, harness/cable drawing, propiedades de masa detalladas y drawings mecánicos. | ICD integrador | Sistema | I | Dossier de entrega completado | Open | Paquete de entrega TBD con integrador. |

---

## 2) RF, comunicaciones y regulatorio

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-RF-01 | El satélite shall NO transmitir en ISM desde órbita. El uplink LoRa orbital es RX-only en el MVP. | `MIS-REQ-02`, `COMP-REQ-03`, `00_MVP/MVP v2.2.md` | COMMS | T | Test de banco (no TX en modo RX-only) | Open | Verificar que el FW no activa TX LoRa en modo orbital. |
| CX-RF-02 | Los RF inhibits del TX UHF shall ser ≥3 inhibiciones independientes según requerimiento típico de integrador CubeSat. | CDS Rev 14.1; ICD integrador | COMMS/EPS | I+T | Prueba de inhibición en banco | Blocked by Integrator | Número y tipo exacto depende del ICD. |
| CX-RF-03 | Las emisiones espurias y armónicos del TX UHF shall cumplir límites regulatorios aplicables. | ENACOM/ITU; ICD integrador | COMMS | T+A | Medición de espectro en banco | Open | Requiere medición con analizador de espectro cuando se tenga hardware TX. |
| CX-RF-04 | Shall existir evidencia de coordinación IARU para la banda amateur-sat antes de cerrar el bandplan. | ITU/IARU; `04_Communications/RF_ANALISYS_OPENLST.md` | Operaciones | D | Documentación IARU | Open | TBD. |
| CX-RF-05 | La operación de la estación terrena shall cumplir el camino regulatorio ENACOM aplicable. | ENACOM; `04_Communications/RF_ANALISYS_OPENLST.md` §4.1 | Operaciones | D | Documentación ENACOM | Open | TBD. |
| CX-RF-06 | El CubeSat shall NO transmitir RF dentro de un tiempo mínimo post-eyección (wait time). | CDS Rev 14.1 §3.3.2; ICD integrador | COMMS/FSW | T | Prueba de secuencia de boot + inhibición RF | Blocked by Integrator | Duración exacta depende del ICD. |

---

## 3) EPS, batería y energía

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-EPS-01 | La topología de batería de vuelo shall ser 2S Li-ion. | `MIS-REQ-06`, `ADR-20260218-battery-topology-2s-flight` | EPS | I | Diseño PCB flight-like | Partial | Banco 1S activo; PCB 2S en KiCad. |
| CX-EPS-02 | Shall existir dossier de batería y carga para topología 2S + MPPT: quimismo, capacidad, curvas de carga/descarga, certificaciones si aplica. | `COMP-REQ-06`; ICD integrador | EPS | I | Dossier batería | Open | Dossier TBD. |
| CX-EPS-03 | El EPS shall soportar pico de ~3 W sin brownout en el escenario sin IA activa. El cierre de pico total con payload IA permanece abierto bajo `CONF-01`. | `00_MVP/MVP v2.2.md` §8 | EPS/COMMS | T+A | Medición banco + `T20` en `EPS_Bench1_1S` extendido | Open | El bench extendido usa `5V_AI_EXT` para medir el CM5 real, pero no cierra el rail IA de vuelo ni el target solar con IA activa. |
| CX-EPS-04 | Los materiales de PCB y estructura shall cumplir requisitos de venting, outgassing y compatibilidad de vacío del integrador. | `COMP-REQ-05`; ICD integrador | Estructura/EPS | I | Datasheet de materiales + análisis | Blocked by Integrator | Requiere lista de materiales prohibidos del integrador. |
| CX-EPS-05 | Pasivación y mitigación de debris: para misiones LEO, shall evaluarse si aplican requisitos de pasivación de batería y/o venting de gases post-misión. | ICD integrador; IADC Guidelines | EPS/Sistema | A | Análisis de pasivación documentado | Open | Depende del integrador y regulación aplicable. |
| CX-EPS-06 | La telemetría EPS shall exponer `EPS_STATE` en la taxonomía canónica `CRIT / LOW / NOMINAL / HIGH`. | `MIS-REQ-10`, `MIS-REQ-12`, `ADR-20260314-eps-state-4-levels.md` | EPS/FSW | T | Test de telemetría y transición de estados | Open | `EPS_Bench1_1S` extendido agrega `5V_AI_SENSE` y señales IA en `JP1` control-only, pero `EPS_STATE` canónico sigue pendiente de implementación/verificación. |

---

## 4) Software y operaciones

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-SW-01 | El sistema shall boot determinista en `MISSION_MODE = SAFE`. | `MIS-REQ-08`, `00_MVP/MVP v2.2.md` §9 | FSW | T | Test de boot en banco | Open | Verificar en banco con firmware de vuelo. |
| CX-SW-02 | El arbitraje de downlink shall implementar prioridad estricta `HOUSEKEEPING` + `COMMAND_ACK` y `AI_BEHAVIOR_LOG` como cola best-effort de mayor prioridad científica. | `MIS-REQ-09`, ADR downlink, ADR misión primaria | FSW/COMMS | T | Test de saturación de colas | Open | TBD en banco. |
| CX-SW-03 | Shall existir persistencia de logs: raw append-only por sesión, muestras parseadas, metadata, replay y export. | `05_Software/ground_data_architecture.md` | Ground SW | T | Test de persistencia/replay | Open | Arquitectura documentada; implementación TBD. |

---

## 5) PHOTO_DEMO (payload opcional)

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-PH-01 | [PHOTO_DEMO] shall iniciar OFF al boot. | `MIS-REQ-PH-01`, ADR-20260313-photo-demo | FSW | T | Test de boot | Open | Off-by-default. |
| CX-PH-02 | [PHOTO_DEMO] shall ser best-effort; su falla shall no degradar cadena principal. | `MIS-REQ-PH-04`, ADR-20260313-photo-demo | FSW | T | Test de falla inducida | Open | Aislamiento verificable en banco. |

---

## 6) Payload IA experimental

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-AI-01 | El payload IA shall estar separado del OBC determinístico; el OBC conserva autoridad de vuelo. | `IA-REQ-04`, `IA-REQ-05`, `ADR-20260314` | FSW/SYS | T+I | Test de supervisor + inspección de arquitectura | Open | Gate IA-2 pendiente (integración física). |
| CX-AI-02 | El payload IA shall ser power-gated en un rail dedicado, independiente de cargas críticas. | `IA-REQ-01`, `ADR-20260314` | EPS | T+I | Inspección de arquitectura `J_AI_PWR -> F_AI -> SW_AI -> 5V_AI_SW` + ensayos `T11-T12` | Partial | `EPS_Bench1_1S` extendido documenta el rail IA bench-only con `5V_AI_EXT`; falta evidencia de ejecución y no aplica extrapolación automática a vuelo. |
| CX-AI-03 | Shall existir kill switch software y hardware del payload IA. | `IA-REQ-08`, `ADR-20260314` | EPS/FSW | T | `AI_KILL_N` + `SW_AI` documentados; prueba de kill en `T15` / `T21` | Partial | Kill switch bench documentado en el FPM del banco. Falta evidencia de prueba integrada y no cierra hardware de vuelo. |
| CX-AI-04 | El sistema shall soportar uplink de prompts versionados para el payload IA. | `IA-REQ-06`, `MIS-REQ-18`, `ADR-20260314` | COMMS/FSW | T | Test de uplink de prompt simulado | Open | Gate IA-2 pendiente. |
| CX-AI-05 | Shall existir Behavior Logger del payload IA con campos mínimos (timestamp, model_version, prompt_version, decision_id, recommended_action, confidence, supervisor_result, MISSION_MODE, EPS_STATE). | `IA-REQ-07`, `MIS-REQ-17`, `ADR-20260314` | FSW | T | Test de logging persistente | Open | `EPS_STATE` debe seguir la taxonomía de 4 niveles. Pendiente de integración con hardware. |
| CX-AI-06 | El consumo eléctrico del payload IA shall ser medido en banco (idle / active / inference) antes de declarar presupuesto energético cerrado. | `ADR-20260314` §H, `CONF-01` | EPS | T | `T20` sobre `EPS_Bench1_1S` extendido + metrología externa si el `INA219` inline no cierra | Open | Ningún valor queda cerrado hasta medir CM5 real en Gate IA-2; `5V_AI_EXT` bench-only no valida el rail IA de vuelo. |
| CX-AI-07 | Shall existir monitoreo de salud del payload IA: `EN_AI`, `PGOOD_AI`, `FAULT_AI`, `HB_AI`, `reset_count_AI`, `fault_count_AI`. | `ADR-20260314` §G | FSW/EPS | T | Señales bench documentadas + ensayos `T14-T15` / `T17` | Partial | `EPS_Bench1_1S` extendido y `ai_payload_architecture.md` documentan señales y contadores mínimos; falta evidencia de ejecución. |
| CX-AI-08 | La política de mutua exclusión IA ↔ TX UHF shall implementarse en el Runtime Safety Supervisor. | `ADR-20260314` §D | FSW | T | `T19` en banco integrado | Open | Gate IA-2 pendiente; el bench extendido define la evidencia esperada pero no hay prueba cargada aún. |
| CX-AI-09 | Propiedades térmicas del payload IA shall evaluarse antes de declarar viabilidad térmica en órbita. | `ADR-20260314` §H | EPS/SYS | A+T | `AI_THERM` + `T21` + análisis térmico correlativo | Open | El bench extendido agrega telemetría térmica básica del CM5. No existe todavía evidencia suficiente para declarar viabilidad térmica orbital. |
| CX-AI-10 | Propiedades de masa del payload IA shall documentarse cuando estén disponibles los diseños mecánicos. | `ADR-20260314` | Estructura/SYS | I | Medición masa | Open | TBD — sin diseño mecánico aún. |
| CX-AI-11 | El sistema shall demostrar en órbita al menos 5 ciclos de inferencia del payload IA con logging completo descargado a tierra. | `MIS-REQ-16`, `ADR-20260314-mission-redef-ai-primary.md` | FSW/Ground | D | Dataset orbital + logs correlacionados | Open | Criterio de éxito primario. |
| CX-AI-12 | El sistema shall descargar al menos 100 registros `AI_BEHAVIOR_LOG` válidos. | `MIS-REQ-17`, `ADR-20260314-mission-redef-ai-primary.md` | Ground/FSW | D | Export de logs + verificación de campos | Open | Criterio de éxito primario. |
| CX-AI-13 | El sistema shall demostrar recepción, activación y uso en inferencia de al menos 1 prompt versionado subido por uplink. | `MIS-REQ-18`, `ADR-20260314-mission-redef-ai-primary.md` | COMMS/FSW | D | Evidencia uplink + log de inferencia | Open | Criterio de éxito primario. |
| CX-AI-14 | El modelo baseline funcional del payload IA shall ser IBM Granite 350M fine-tuned hasta que una nueva ADR `Accepted` lo reemplace. El modelo shall seleccionarse con criterios explícitos de licencia y origen. | `IA-REQ-10`, `IA-REQ-11`, `ADR-20260316` | FSW/SYS | I | Verificación de ADR vigente + modelo cargado | Partial | Evidencia de banco completada (benchmark corrected + holdout 2026-03-16). Pendiente validación en CM5 real. |
| CX-AI-15 | Shall existir benchmark funcional del modelo baseline del payload IA como evidencia de banco antes de Gate IA-2. | `ADR-20260316`, `IA-REQ-10` | FSW/SYS | T | Resultados de benchmark + holdout documentados | Partial | Completado para Granite 350M fine-tuned (2026-03-16): pass_rate 57.14 %, avg_score_ratio 0.83. Pendiente validación en hardware CM5 real. |

---

## 7) Evidence Pack y documentación de entrega

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-EP-01 | Shall existir un evidence pack con resultados de ensayos de banco, campo, FlatSat y ambiental antes de PDR/CDR del integrador. | `01_Mission/validation_plan_and_stage_gates.md` | Sistema | I+D | Evidence pack documentado | Open | Plan en `validation_plan_and_stage_gates.md`. |
| CX-EP-02 | La compliance matrix (este documento) shall estar actualizada al cierre de cada stage-gate. | ADR-20260313-compliance-matrix-artefacto-sistema | Sistema | I | Revisión de matriz | Partial | Matriz inicial creada; en proceso de completar evidencias. |

---

## 8) Estructura, layout solar y térmico (2026-03-20)

| ID | Requirement | Source | Owner | Verification | Evidence | Status | Notes |
|---|---|---|---|---|---|---|---|
| CX-STR-01 | Layout de caras: paneles solares a +Y, ±X, −Z; radiador a −Y (LTAN 10h). | `STR-REQ-01`, `ADR-20260320-orbit-attitude-solar-layout-baseline.md` | Structure | A / I | Layout mecánico + análisis orbital | Pending | A/I — verificar en diseño mecánico final. |
| CX-STR-02 | Actitud nominal 10×10 nadir (+Z Tierra, +X ram). | `STR-REQ-02`, `ADR-20260320-orbit-attitude-solar-layout-baseline.md` | Mission/ADCS | A | Análisis ADCS + validación orbital | Pending | A — verificar con ADCS seleccionado. |
| CX-THR-01 | Recubrimiento del radiador: α_solar ≤ 0.20, ε_IR ≥ 0.88 (AZ-93 o Al anodizado blanco). | `THR-REQ-01`, `ADR-20260320-thermal-design-radiator-cm5-coupling.md` | Structure/Thermal | T / A | Medición α/ε post-aplicación de recubrimiento | Pending | T — medir propiedades ópticas en muestra tratada antes de vuelo. |
| CX-THR-02 | Conductancia térmica CM5 → radiador: G ≥ 0.60 W/K. | `THR-REQ-02`, `ADR-20260320-thermal-design-radiator-cm5-coupling.md` | Structure/Thermal | T | Medición ΔT en banco con prototipo mecánico | Pending | T — medir ΔT en banco con prototipo integrado (Gate IA-1). |
| CX-THR-03 | Temperatura mínima de batería en eclipse ≥ −10°C. | `THR-REQ-03`, `ADR-20260320-thermal-design-radiator-cm5-coupling.md` | EPS/Thermal | A + T | Simulación térmica + TVAC si disponible | Pending | Evidencia preliminar: simulador v9.2 muestra Tmin ≥ 20°C. Requiere validación en banco integrado. |
| CX-THR-04 | Recubrimiento del radiador: TML ≤ 1.0% y CVCM ≤ 0.1% (outgassing). | `THR-REQ-04`, CDS Rev. 14.1 §2.1.7 | Structure/Thermal | I | Datasheet del material (AZ-93 o anodizado) | Pending | I — verificar hoja de datos del fabricante antes de aplicar. |

---

## Notas generales

- Los ítems marcados `Blocked by Integrator` quedan como placeholder de diseño hasta disponer del ICD del integrador de lanzamiento.
- Los ítems `Open` sin ICD de integrador se documentan con la referencia al estándar más aplicable (típicamente CDS Rev 14.1).
- No se inventan requisitos específicos del launch provider; se usa `TBD` o `Blocked by Integrator`.
- Al recibir ICD del integrador: actualizar todos los ítems correspondientes y crear ADR si hay impacto de arquitectura.
