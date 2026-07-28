# Requirements Matrix — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — baseline pre-SRR
**Trazabilidad:** `00_MVP/MVP v2.2.md` y ADRs `Accepted`

## Convenciones

- `shall` identifica una obligación verificable.
- Método: `T` Test, `A` Analysis, `I` Inspection, `D` Demonstration.
- `Active` significa requisito vigente; no significa verificado.
- El estado de verificación vive en
  `verification_cross_reference_matrix.csv`.
- Todo criterio `TBD` debe cerrarse en SRR/PDR antes de ejecutar la
  verificación correspondiente.

## 1. Misión y sistema

| ID | Requirement | Criterio de aceptación | Método | Fuente | Owner role | Lifecycle |
|---|---|---|---|---|---|---|
| MIS-REQ-01 | El vehículo shall ser compatible con la clase CubeSat 1.5U. | CAD y artículo medido cumplen el dibujo CDS completo; `Z=170.2 ±0.1 mm`; fit-check ICD aprobado. | I+D | ADR-20260727-cubesat-1p5u-cds-envelope | Structure | Active |
| MIS-REQ-02 | El radio LoRa orbital shall ser RX-only y no tendrá camino de TX habilitable. | Inspección de esquema/PCB y prueba negativa de todos los modos muestran cero transmisión LoRa orbital. | I+T | ADR-20260727-rf-regulatory-command-security-baseline | COMMS | Active |
| MIS-REQ-03 | El TTC UHF shall operar únicamente en frecuencia, waveform y potencia coordinadas/autorizadas. | Dossier ENACOM/IARU/ITU aprobado y configuración RF coincide con el dossier y medición OTA. | I+T+D | ADR-20260727-rf-regulatory-command-security-baseline | COMMS/Operations | Active |
| MIS-REQ-04 | Si se autoriza el experimento Tierra→espacio, el sistema shall demostrar recepción store-and-forward con protocolo preregistrado. | Protocolo fija N nodos/frames, PHY, elevación, denominador e IC; resultado cumple threshold aprobado. | T+D+A | Mission Definition §4 | COMMS/Ground | Active |
| MIS-REQ-05 | Cada frame terrestre aceptado shall conservar payload, identidad autenticada si aplica, tiempo, RSSI, SNR, CFO, CRC y provenance. | Export/replay reproduce cada frame y sus quality flags sin campos obligatorios nulos. | T+I | Mission Definition §8 | COMMS/Ground | Active |
| MIS-REQ-06 | La arquitectura EPS flight-like/flight shall usar batería 2S. | Esquema, BOM y artículo muestran dos celdas/grupos en serie y rango compatible; pruebas de protección aprobadas. | I+T | ADR-20260218-battery-topology-2s-flight | EPS | Active |
| MIS-REQ-07 | El Science Pack MVP shall excluir fuentes de alta tensión/radiación Geiger. | BOM, esquema, software y artículo carecen de etapa HV; inspección aprobada. | I | ADR-20260218-geiger-removed-from-mvp | Science/EPS | Active |
| MIS-REQ-08 | El sistema shall bootear en SAFE, usar SAFE por defecto en eclipse y forzar SAFE con `EPS_STATE=CRIT`. | Tests nominales, límites y fallas logran transición dentro del tiempo TBD sin energizar cargas prohibidas. | T | ADR-20260314-eps-state-4-levels | FSW/EPS | Active |
| MIS-REQ-09 | El downlink manager shall priorizar `HOUSEKEEPING`, luego `COMMAND_ACK`, y ubicar `AI_BEHAVIOR_LOG` como mayor prioridad científica best-effort. | Ensayo de colas saturadas preserva prioridades, cuota mínima/aging aprobados y ausencia de starvation crítico. | T+A | ADR-20260218-downlink-arbitration-and-subsystem-power-framework | FSW/COMMS | Active |
| MIS-REQ-10 | El sistema shall exponer health por subsistema y contadores de boot/reset/fault con session ID. | Schema y tests de inyección cubren `EN/PGOOD/FAULT/HB`, estados, contadores, reboot y wrap. | T+I | MVP v2.2 §8 | FSW/EPS | Active |
| MIS-REQ-11 | El TTC shall soportar comandos mínimos de modo, potencia, downlink, status y abort, autenticados y protegidos contra replay. | Suite verifica comando válido y rechaza replay, clave/rol erróneo, frame truncado, rollback y contador perdido. | T | ADR-20260727-rf-regulatory-command-security-baseline | FSW/COMMS | Active |
| MIS-REQ-12 | El sistema shall implementar exactamente `MISSION_MODE=SAFE|NOMINAL|DOWNLINK_WINDOW` y `EPS_STATE=CRIT|LOW|NOMINAL|HIGH`. | State-machine tests cubren todos los estados/transiciones; no aparece `SCIENCE` ni `EPS_STATE=SAFE`. | T+I | ADR-20260314-eps-state-4-levels | FSW/EPS | Active |
| MIS-REQ-13 | Hardware `Bench`, `Flight-Like`, `Flight` y `EGSE` shall permanecer separado en diseño, BOM y evidencia. | Revisión de configuración no encuentra una fila/claim que mezcle artículos o transfiera evidencia entre stages. | I | ADR-20260313-eps-separacion-bench-flightlike-flight | Systems/QA | Active |
| MIS-REQ-14 | El nodo terrestre de prueba shall identificarse por clase técnica y configuración exacta, no por SKU implícito. | Test report registra radio, MCU, potencia, antena, reloj, firmware y calibración; BOM conserva alternativas. | I+T | ADR-20260313-nodo-tipico-lora-clase | Node/COMMS | Active |
| MIS-REQ-15 | Shall existir VCRM y compliance matrix controladas para todo requisito. | Cero ReqID sin método, criterio, ProcedureID, gate, risk/evidence state; revisión independiente aprobada. | I | ADR-20260727-verification-and-review-governance | Systems/QA | Active |
| MIS-REQ-16 | El payload IA shall ejecutar el protocolo científico preregistrado en órbita. | Muestra, escenarios, control y análisis coinciden con protocolo congelado; no conformidades críticas=0. | D+A | Mission Definition §3–4 | AI/Science/Ground | Active |
| MIS-REQ-17 | El sistema shall descargar al menos 100 eventos IA completos y la muestra estadística requerida, si fuera mayor. | Validador de schema acepta 100% de eventos usados; cantidad ≥ máximo(100,N preregistrado). | T+D | Mission Definition §4, §8 | FSW/Ground | Active |
| MIS-REQ-18 | El sistema shall cargar, autenticar, activar y usar al menos un prompt versionado. | Cadena upload→verify→activate→infer→rollback queda correlacionada; replay/alteración son rechazados. | T+D | ADR-20260727-rf-regulatory-command-security-baseline | FSW/COMMS | Active |
| MIS-REQ-19 | El UHF shall emitir un beacon público documentado compatible con la coordinación vigente. | Decoder público reproduce frames capturados; identificación/contenido/intervalo cumplen autorización. | T+D+I | ADR-20260727-rf-regulatory-command-security-baseline | COMMS/Ground | Active |
| MIS-REQ-20 | Downlink operacional y uplink de comando shall usar perfiles controlados con autenticación; no se asumirá confidencialidad por framing cerrado. | Threat model, protocolo y tests demuestran autenticidad/anti-replay; contenido cumple regulación. | A+T+I | ADR-20260727-rf-regulatory-command-security-baseline | Security/COMMS | Active |
| MIS-REQ-21 | La estación shall aislar SatNOGS RX-only de PTT, claves y control AUSTRALIS. | Inspección física/permisos y tests de falla demuestran que el proceso SatNOGS no puede transmitir. | I+T | ADR-20260727-rf-regulatory-command-security-baseline | Ground/COMMS | Active |
| MIS-REQ-22 | La estación shall medir las condiciones ambientales necesarias para operación segura y provenance de cada pasada. | Hazard analysis define sensores/umbrales; logs correlacionados accionan park/inhibit y registran calidad/calibración. | A+T+D | MVP v2.2 §13 | Ground | Active |
| MIS-REQ-23 | El proyecto shall conservar política DIY/low-cost sin reducir seguridad, compliance o trazabilidad. | Cada excepción costosa/EOL/import-only está justificada; ningún criterio de seguridad se degrada por costo. | I+A | ADR-20260710-diy-low-cost-maker-latam-design-policy | Systems/Cost | Active |
| MIS-REQ-24 | BOM y trade studies shall registrar clase, alternativa, fuente/fecha, costo, lead time, stage, riesgo y trazabilidad. | Auditoría de BOM no encuentra campos obligatorios vacíos salvo `TBD` explícito con plan de cierre. | I | ADR-20260710-diy-low-cost-maker-latam-design-policy | Cost/Procurement | Active |

## 2. Uplink terrestre experimental

| ID | Requirement | Criterio de aceptación | Método | Fuente | Owner role | Lifecycle |
|---|---|---|---|---|---|---|
| COMMS-UL-01 | El experimento shall usar nodos de clase típica sin PA/LNA externo salvo nueva ADR. | Configuración medida y registrada cumple límites de clase aprobados en SRR. | I+T | ADR-20260313-nodo-tipico-lora-clase | COMMS/Node | Active |
| COMMS-UL-02 | B2 slotted shall habilitarse solo con base temporal validada; al perderla el nodo shall quedar fail-silent. B1 solo se permite como modo separado autorizado. | Deriva worst-case permanece dentro del guard aprobado; pérdida de `time_valid` inhibe TX; B1 no se activa sin autorización, airtime y energía aprobados. | T+A | ADR-20260727-rf-regulatory-command-security-baseline | Node FW | Active |
| COMMS-UL-03 | La predicción de pasadas shall usar TLE/SGP4 con autenticidad, object ID, expiry y error budget. | Casos de TLE válido/viejo/firmado erróneo/rollback cumplen ventana y fallback aprobados. | T+A | ADR-20260727-rf-regulatory-command-security-baseline | Node FW/Ground | Active |
| COMMS-UL-04 | El receptor shall registrar tiempo, RSSI, SNR, CFO, CRC, canal/PHY, session y quality flags. | Schema/replay reproduce todos los campos con unidades y calibración identificadas. | T+I | MIS-REQ-05 | COMMS/OBC | Active |
| COMMS-UL-05 | El downlink shall usar resumen por pasada y detalle on-demand con data budget y retención definidos. | Simulación/ensayo de peor carga cumple retención, cuotas y no-starvation aprobadas. | A+T | MIS-REQ-09 | FSW/COMMS | Active |
| COMMS-UL-06 | Slotting, retry y canales shall dimensionarse con ToA correcto y modelo de colisión/near-far. | Cálculo independiente y Monte Carlo/test reproducen capacidad/PDR dentro de tolerancia aprobada. | A+T | ADR-20260727-rf-regulatory-command-security-baseline | COMMS/Node | Active |

## 3. Compliance de lanzamiento y regulación

| ID | Requirement | Criterio de aceptación | Método | Fuente | Owner role | Lifecycle |
|---|---|---|---|---|---|---|
| COMP-REQ-01 | El vehículo shall cumplir envolvente, masa y propiedades mecánicas CDS/ICD para 1.5U. | Dossier + medición + fit-check aceptados por integrador. | I+D | CDS Rev.14.1; ICD TBD | Structure | Active |
| COMP-REQ-02 | La arquitectura de launch safety shall incluir deployment switch sobre funciones powered, RBF, al menos tres inhibits RF y tres de deployables, y timers mínimos CDS o más restrictivos del ICD. | Inspección y fault-injection prueban independencia; deployables permanecen inhibidos ≥30 min y TX ≥45 min post-eyección aun con reset/brownout; integrador acepta. | I+T | CDS Rev.14.1 §§2.3–2.4; ICD TBD | EPS/COMMS | Active |
| COMP-REQ-03 | El satélite shall permanecer sin transmisión ISM orbital. | Análisis de caminos y prueba negativa de software/hardware completados. | I+T | MIS-REQ-02 | COMMS | Active |
| COMP-REQ-04 | Bandplan amateur-satellite shall contar con coordinación IARU y trámite UIT vía administración. | Dossier escrito con estado de coordinación/notificación antes de congelar RF. | I+D | IARU/ITU/ENACOM | Operations | Active |
| COMP-REQ-05 | Materiales y volúmenes shall cumplir venting/outgassing/compatibilidad de vacío aplicables. | Material declaration y análisis/ensayos aceptados por ICD; sin volumen sellado no analizado. | I+A+T | CDS/ICD; ASTM E595 si aplica | Structure/Materials | Active |
| COMP-REQ-06 | Shall existir dossier de batería completo y aceptado. | Incluye celda, lotes, BMS, carga, balanceo, protecciones, térmica, transporte, tests y pasivación. | I+T | CDS/ICD | EPS/Safety | Active |

## 4. PHOTO_DEMO opcional

| ID | Requirement | Criterio de aceptación | Método | Fuente | Owner role | Lifecycle |
|---|---|---|---|---|---|---|
| MIS-REQ-PH-01 | `PHOTO_DEMO` shall iniciar OFF. | 100% de boots/resets ensayados mantienen rail y función OFF. | T | ADR-20260313-photo-demo-opcional-no-critico | FSW/EPS | Active |
| MIS-REQ-PH-02 | `PHOTO_DEMO` shall ser best-effort sin desplazar colas críticas/científicas prioritarias. | Saturación/falla inducida no viola cuotas/prioridades. | T | ADR-20260313-photo-demo-opcional-no-critico | FSW/COMMS | Active |
| MIS-REQ-PH-03 | Si se incluye, la transferencia shall ser reanudable e íntegra. | Pérdida/reset/reorder produce archivo final con digest correcto o descarte seguro. | T | ADR-20260313-photo-demo-opcional-no-critico | FSW/Ground | Active |
| MIS-REQ-PH-04 | Su falla shall no degradar el bus ni el éxito primario. | Fault injection demuestra aislamiento de potencia, CPU, storage y colas. | T | ADR-20260313-photo-demo-opcional-no-critico | Systems/FSW | Active |

## 5. Payload IA

| ID | Requirement | Criterio de aceptación | Método | Fuente | Owner role | Lifecycle |
|---|---|---|---|---|---|---|
| IA-REQ-01 | El payload IA shall usar rail power-gated independiente de cargas críticas. | Esquema/PCB y pruebas de short/inrush/backfeed prueban fault containment. | I+T | ADR-20260727-ai-payload-gemma4-e2b-candidate | EPS/FSW | Active |
| IA-REQ-02 | El payload IA shall iniciar OFF. | 100% de boots, resets y brownouts mantienen IA OFF hasta autorización válida. | T | ADR-20260727-ai-payload-gemma4-e2b-candidate | FSW/EPS | Active |
| IA-REQ-03 | IA shall estar OFF en SAFE, eclipse y EPS CRIT/LOW. | Boundary/fault tests cubren todas las combinaciones sin bypass. | T | ADR-20260727-ai-payload-gemma4-e2b-candidate | FSW/EPS | Active |
| IA-REQ-04 | IA shall no sobreescribir reglas ni estado autoritativo del OBC. | Interfaces no ofrecen write directo; adversarial tests no alteran estado sin supervisor. | I+T | ADR-20260727-ai-payload-gemma4-e2b-candidate | FSW/Safety | Active |
| IA-REQ-05 | El OBC shall validar schema, tool, argumentos, clase, precondiciones y postcondiciones antes de actuar. | Suite negativa produce hard-fail para salida envuelta, campos/rangos inválidos y acciones prohibidas. | T | ADR-20260727-ai-payload-gemma4-e2b-candidate | FSW/Safety | Active |
| IA-REQ-06 | Prompts/policies shall ser versionados, autenticados, staged y activados separadamente. | Tests de upload/activate/rollback/replay/corrupción cumplen protocolo. | T | ADR-20260727-rf-regulatory-command-security-baseline | FSW/Security | Active |
| IA-REQ-07 | Cada inferencia shall generar el registro científico completo definido en Mission Definition §8. | Validador schema acepta 100% de eventos usados en análisis y liga raw/postestado. | T+I | Mission Definition §8 | FSW/Ground | Active |
| IA-REQ-08 | El payload shall disponer de disable local autónomo y de comando autenticado aplicable en la siguiente oportunidad de contacto. | Kill local cumple tiempo máximo TBD; comando válido deshabilita/lockout; ausencia de contacto no compromete seguridad. | T | ADR-20260727-ai-payload-gemma4-e2b-candidate | FSW/COMMS | Active |
| IA-REQ-09 | La plataforma candidata shall registrar configuración exacta y no se promoverá a vuelo sin COTS-to-flight. | Manifest de hardware y dossier de radiación/térmica/EMC/almacenamiento aprobados antes de CDR. | I+A+T | ADR-20260727-ai-payload-gemma4-e2b-candidate | Systems/AI | Active |
| IA-REQ-10 | `gemma4:e2b` shall tratarse como candidato no validado hasta cumplir su gate de evidencia. | Digest/licencia/dataset/suite/mediciones completos; review autoriza cualquier promoción. | I+T+A | ADR-20260727-ai-payload-gemma4-e2b-candidate | AI/Science | Active |
| IA-REQ-11 | Todo cambio de candidato/modelo shall realizarse mediante ADR y nueva configuración de evidencia. | Auditoría no encuentra cambio de tag/digest sin ADR; métricas no se transfieren entre artefactos. | I | ADR-20260727-ai-payload-gemma4-e2b-candidate | Systems/QA | Active |

## 6. Estructura, ADCS y térmico

| ID | Requirement | Criterio de aceptación | Método | Fuente | Owner role | Lifecycle |
|---|---|---|---|---|---|---|
| STR-REQ-01 | El layout de caras shall derivarse de CAD y análisis orbital/térmico/solar corregido, y congelarse por ADR. | Modelo reproducible, requisitos absolutos y review seleccionan layout; no depende de score arbitrario. | A+I | ADR-20260727-orbit-attitude-analysis-reopened | Structure/Thermal | Active |
| STR-REQ-02 | El diseño shall incluir arquitectura ADCS capaz de los pointing/stability limits aprobados. | Error budget, simulación con dispersión y pruebas HIL satisfacen límites TBD en SRR/PDR. | A+T | ADR-20260727-orbit-attitude-analysis-reopened | ADCS | Active |
| THR-REQ-01 | Toda superficie térmica shall tener α/ε medidos y cumplir el modelo correlacionado. | Cupón/material as-built medido; valores worst-case degradados mantienen límites aprobados. | T+A | ADR-20260727-thermal-power-baselines-reopened | Thermal/Materials | Active |
| THR-REQ-02 | La ruta térmica IA→estructura shall alcanzar la conductancia asignada por el modelo. | Ensayo calorimétrico incluye TIM, contactos, spreading y tolerancias; G medida ≥ allocation TBD. | T | ADR-20260727-thermal-power-baselines-reopened | Thermal/Structure | Active |
| THR-REQ-03 | Batería/cargador shall respetar límites de carga, descarga, almacenamiento y supervivencia de la celda final. | TVAC/cycling y fault tests prueban interlocks en todos los umbrales con tolerancia. | T+A | ADR-20260727-thermal-power-baselines-reopened | EPS/Thermal | Active |
| THR-REQ-04 | Material térmico shall cumplir outgassing del ICD. | Datasheet/lot test aceptado; TML/CVCM conforme límite aplicable. | I+T | COMP-REQ-05 | Materials | Active |

## 7. Requisitos de aseguramiento incorporados por auditoría

| ID | Requirement | Criterio de aceptación | Método | Fuente | Owner role | Lifecycle |
|---|---|---|---|---|---|---|
| SYS-REQ-01 | El experimento IA shall tener protocolo preregistrado antes de SRR. | Documento aprobado contiene todos los elementos de Mission Definition §3–4. | I | ADR-20260727-verification-and-review-governance | Science/Systems | Active |
| SYS-REQ-02 | Todo claim cuantitativo shall citar configuración, unidades, artefacto y resultado exacto. | Muestreo de claims activos tiene trazabilidad completa; cero resultado transferido por analogía. | I | AGENTS.md §13.1 | QA/Systems | Active |
| SYS-REQ-03 | Readiness shall seguir SRR→PDR→CDR→TRR→Q/AR→FRR sin dependencias preliminares. | Review records y entrance/exit criteria completos; waivers controlados. | I | ADR-20260727-verification-and-review-governance | Systems/QA | Active |
| SYS-REQ-04 | Shall existir configuración identificada del artículo ensayado. | Cada EvidenceID liga BOM/CAD/FW/model/config hashes y serial/lote aplicables. | I | ADR-20260727-verification-and-review-governance | Configuration/QA | Active |
| SYS-REQ-05 | Ningún requisito shall cerrarse por análisis preliminar sin criterio/evidencia controlada. | VCRM usa `Verified` solo con ProcedureID, configuración y EvidenceID aprobado. | I | ADR-20260727-verification-and-review-governance | QA | Active |
| SYS-REQ-06 | Owners shall ser roles asignados nominalmente antes de ejecutar su review. | Acta de review registra nombre, autoridad, fecha y firma/aprobación. | I | ADR-20260727-verification-and-review-governance | Project Management | Active |
| SYS-REQ-07 | Hallazgos y waivers shall conservar disposición, autoridad y riesgo residual. | Registro auditado sin hallazgo crítico huérfano; waiver liga RiskID y expiración/condición. | I | ADR-20260727-verification-and-review-governance | QA/Risk | Active |
| EPS-REQ-01 | `EPS_STATE` shall ser una máquina verificable con thresholds, histéresis, dwell y fallas de sensor. | Especificación y boundary tests cubren boot/unknown, ruido, debounce y precedencia. | I+T | MVP v2.2 §8 | EPS/FSW | Active |
| EPS-REQ-02 | El diseño EPS shall pasar revisión de esquema/ERC/BOM/DRC antes de fabricación. | Cero corto/ERC/DRC bloqueante; checklist y release package firmados. | I | ADR-20260727-thermal-power-baselines-reopened | EPS/QA | Active |
| ADCS-REQ-01 | ADCS shall detumble desde la envolvente de tasas de liberación del ICD. | HIL/analysis satisface tiempo y energía TBD para todos los casos aprobados. | A+T | STR-REQ-02 | ADCS | Active |
| ADCS-REQ-02 | Budgets solar/térmico/RF shall incluir pointing error, jitter y safe/degraded attitude. | Sensibilidad/worst-case muestra cumplimiento sin actitud perfecta implícita. | A | STR-REQ-02 | ADCS/Systems | Active |
| DATA-REQ-01 | Ground shall persistir raw append-only, metadata, parsed data, replay y export. | Power-loss/restart/replay produce dataset íntegro con digests y sin depender de RAM. | T | Mission Definition §6 | Ground SW | Active |
| DATA-REQ-02 | Métricas de pérdida shall distinguir session/boot, wrap, duplicados y reordenamiento. | Tests unitarios con todos los casos producen PER/gaps esperados. | T | DATA-REQ-01 | Ground SW | Active |
| SEC-REQ-01 | TTC y prompts shall usar autenticación criptográfica y anti-replay. | Suite negativa completa aprobada; CRC/hash simple no es la única protección. | T+A | ADR-20260727-rf-regulatory-command-security-baseline | Security/FSW | Active |
| SEC-REQ-02 | El threat model shall cubrir spoofing, replay, key compromise, DoS y recovery. | Review de seguridad aprueba assets, adversarios, mitigaciones y riesgos residuales. | A+I | ADR-20260727-rf-regulatory-command-security-baseline | Security | Active |
| RAD-REQ-01 | Shall existir análisis/mitigación TID, DDD, SEE y SEL para hardware COTS. | Entorno, shielding, derating, latch-up/EDAC y test/heritage aprobados antes de CDR. | A+T+I | MVP v2.2 §14 | Radiation/Systems | Active |
| ENV-REQ-01 | El artículo flight-like/flight shall completar el programa ambiental aplicable. | Pre/post funcional, vibration, TVAC/thermal balance, EMC, deployment y RF E2E aprobados según ICD. | T | ADR-20260727-verification-and-review-governance | AIT/QA | Active |

## 8. Regla de cambio

Cambiar statement, criterio o lifecycle exige:

1. actualizar VCRM;
2. evaluar riesgos/budgets/interfaces;
3. ADR si cambia arquitectura o misión;
4. registrar revisión y autoridad.
