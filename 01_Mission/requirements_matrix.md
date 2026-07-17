# Requirements Matrix — AUSTRALIS-1 / DIY Nanosat MVP

**Revisión:** 2026-07-10
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md`, ADRs Accepted en `08_Decisions/`, `ADR-20260710-diy-low-cost-maker-latam-design-policy.md`

Matriz de requisitos verificables (IDs, statement, rationale, verificación, dueño y trazabilidad).

Convención:
- **"shall"** = requisito normativo verificable.
- Fuente normativa: ADR `Accepted` → `00_MVP/MVP v2.2.md` → documentación de subsistema.
- Las referencias a `EPS_DESIGN_RULES.md` son de contexto técnico (draft, no normativo).
- Verificación: **T**(Test), **A**(Analysis), **I**(Inspection), **D**(Demonstration).

## 1) Requisitos de misión / sistema

| ID | Requisito (shall) | Rationale | Verif. | Dueño | Trazabilidad |
|---|---|---|---|---|---|
| MIS-REQ-01 | El satélite shall operar en formato 1.5U (100×100×150 mm). | Compatibilidad mecánica | I | Estructura | `00_MVP/MVP v2.2.md` |
| MIS-REQ-02 | El uplink de usuario shall usar LoRa RX-only en 915 MHz en órbita. | Objetivo secundario de misión / riesgo regulatorio | T | COMMS | `01_Mission/mission_definition.md` |
| MIS-REQ-03 | El downlink/TTC shall usar UHF 435 MHz, FSK, 1200 bps (baseline). | Robustez y ecosistema | T | COMMS | `ADR-20260218-uhf-link-budget-preliminary.md`, `00_MVP/MVP v2.2.md` |
| MIS-REQ-04 | El sistema shall registrar ≥10 paquetes LoRa recibidos en órbita como objetivo secundario de misión. | Evidencia secundaria end-to-end | D | COMMS/OBC | `00_MVP/MVP v2.2.md`, `ADR-20260314-mission-redef-ai-primary.md` |
| MIS-REQ-05 | El sistema shall descargar a tierra evidencia de los paquetes LoRa recibidos (payload + métricas). | Auditoría end-to-end | D | COMMS/Ground | `04_Communications/uplink_data_products_and_downlink_policy.md` |
| MIS-REQ-06 | El EPS de vuelo shall usar topología de batería 2S. | Márgenes y arquitectura EPS | I | EPS | `ADR-20260218-battery-topology-2s-flight.md` |
| MIS-REQ-07 | El Science Pack MVP shall excluir HV de radiación. | Reducción de riesgo/potencia | I | Science/EPS | `ADR-20260218-geiger-removed-from-mvp.md` |
| MIS-REQ-08 | El sistema shall operar en SAFE en eclipse por defecto, degradar a `MISSION_MODE=SAFE` cuando `EPS_STATE=CRIT` y tratar `EPS_STATE=LOW` como condición de conservación con `SAFE` por defecto. | Supervivencia energética y seguridad operacional | T | FSW/EPS | `01_Mission/mission_definition.md`, `ADR-20260314-eps-state-4-levels.md` |
| MIS-REQ-09 | El OBC (On-Board Computer) shall implementar arbitraje de downlink por colas con prioridad estricta `HOUSEKEEPING` y `COMMAND_ACK`, y con `AI_BEHAVIOR_LOG` como cola best-effort de mayor prioridad científica. | Control y seguridad operativa + dato científico primario | T | FSW/COMMS | `ADR-20260218-downlink-arbitration-and-subsystem-power-framework.md`, `ADR-20260314-mission-redef-ai-primary.md` |
| MIS-REQ-10 | El sistema shall exponer health mínimo por subsistema (`PGOOD_x`,`EN_x`,`FAULT_x`,`HB_x`), `EPS_STATE` (`CRIT`,`LOW`,`NOMINAL`,`HIGH`) y contadores de reset/fault. | Diagnóstico / tolerancia a fallas | T | EPS/FSW | `00_MVP/MVP v2.2.md`, `ADR-20260314-eps-state-4-levels.md` |
| MIS-REQ-11 | El uplink mínimo shall soportar `SET_MODE`, `POWER_SET`, `DL_SELECT`, `DL_SET_LIMITS`, `REQUEST_STATUS`, `ABORT`. | Control manual | T | COMMS/FSW | `04_Communications/rf_subsystem_overview.md` |
| MIS-REQ-12 | El sistema shall implementar modelo canónico de modos: `MISSION_MODE` (`SAFE`,`NOMINAL`,`DOWNLINK_WINDOW`) y `EPS_STATE` (`CRIT`,`LOW`,`NOMINAL`,`HIGH`). La actividad científica shall ejecutarse como actividad dentro de `NOMINAL`, no como modo independiente. | Coherencia CONOPS/energía; modelo operativo único | T | FSW/EPS | `01_Mission/mission_definition.md`, `ADR-20260314-eps-state-4-levels.md` |
| MIS-REQ-13 | El EPS de vuelo shall implementar arquitectura 2S + MPPT (Maximum Power Point Tracking). El banco `EPS_Bench1_1S` es validación funcional, no hardware de vuelo. | Separación inequívoca bench/flight-like/flight | I | EPS | `08_Decisions/ADR-20260313-eps-separacion-bench-flightlike-flight.md` |
| MIS-REQ-14 | El nodo típico LoRa terrestre shall pertenecer a la clase definida (radio clase SX1262/SX1276, MCU clase ESP32-S3, +20–21 dBm, sin PA/LNA/TCXO externo, antena 0–2 dBi). No se fija SKU de mercado como requisito normativo. | Compatibilidad/costo; evitar dependencia de SKU | I/D | COMMS/Node | `08_Decisions/ADR-20260313-nodo-tipico-lora-clase.md` |
| MIS-REQ-15 | Shall existir una compliance matrix viva (`01_Mission/compliance_matrix.md`) que trace requisitos clave del sistema con estado, owner y evidencia. | Gobierno documental y trazabilidad de requisitos | I | Sistema | `08_Decisions/ADR-20260313-compliance-matrix-artefacto-sistema.md` |
| MIS-REQ-16 | El sistema shall completar al menos 5 ciclos de inferencia del payload IA en órbita (con el modelo baseline vigente según ADR más reciente) con logging completo descargado a tierra. | Criterio de éxito primario | D | FSW/Ground | `ADR-20260314-mission-redef-ai-primary.md`, `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`, `00_MVP/MVP v2.2.md` |
| MIS-REQ-17 | El sistema shall recolectar y descargar al menos 100 registros `AI_BEHAVIOR_LOG` con datos válidos. | Dataset científico primario | D | FSW/Ground | `ADR-20260314-mission-redef-ai-primary.md`, `05_Software/ai_payload_architecture.md` |
| MIS-REQ-18 | El sistema shall recibir, aplicar y utilizar en inferencia al menos 1 prompt versionado subido por uplink. | Validación de reconfiguración en órbita | D | COMMS/FSW | `ADR-20260314-mission-redef-ai-primary.md`, `04_Communications/uplink_data_products_and_downlink_policy.md` |
| MIS-REQ-19 | La arquitectura UHF shall soportar un `PUBLIC_BEACON` compatible con SatNOGS, documentado y decodificable por terceros, limitado a telemetria minima no sensible. | Recepcion distribuida publica sin exponer payload/operacion | T/D | COMMS/Ground | `ADR-20260704-satnogs-public-beacon-private-payload-uplink.md`, `04_Communications/satnogs_public_beacon_architecture.md` |
| MIS-REQ-20 | El downlink de payload/operacion y el uplink de comandos shall operar como perfiles privados/controlados (`CONTROLLED_DOWNLINK`, `PRIVATE_UPLINK`) mediante estacion/es propia/s o autorizada/s, no mediante SatNOGS. | Seguridad operacional, control de mision y separacion publico/privado | T/D | COMMS/FSW/Ground | `ADR-20260704-satnogs-public-beacon-private-payload-uplink.md`, `04_Communications/uplink_data_products_and_downlink_policy.md` |
| MIS-REQ-21 | La estacion terrena propia shall separar fisica/logicamente el modo SatNOGS receive-only del modo AUSTRALIS privado/controlado, impidiendo que SatNOGS tenga acceso al transmisor, PTT, credenciales de comando o camino de uplink. | Evitar TX accidental y preservar seguridad operacional | T/D/I | Ground/COMMS | `04_Communications/ground_station_dual_use_satnogs_australis.md`, `ADR-20260704-satnogs-public-beacon-private-payload-uplink.md` |
| MIS-REQ-22 | La estacion terrena propia shall incluir instrumentacion meteorologica local para viento, lluvia, temperatura, humedad, presion y ambiente interior de gabinete, integrada al logging y a las inhibiciones/park automatico. | Autonomia segura, proteccion mecanica/electronica y evidencia contextual de pasadas | T/D/I | Ground | `04_Communications/ground_station_dual_use_satnogs_australis.md` |
| MIS-REQ-23 | El proyecto shall mantener una politica de diseno DIY, low cost y de publicacion abierta/source-available no comercial, priorizando componentes maker/COTS ampliamente disponibles en Argentina y Latinoamerica para banco, FlatSat, EGSE y prototipos. | Reproducibilidad, costo, colaboracion abierta y viabilidad regional | I/A | Sistema | `ADR-20260710-diy-low-cost-maker-latam-design-policy.md`, `SYSTEM_BASELINE.md` |
| MIS-REQ-24 | La BOM y los trade studies shall definir componentes por clase tecnica cuando sea posible, registrar proveedor/region/alternativa/riesgo, y justificar cualquier SKU unico, componente caro, exotico, EOL o de baja disponibilidad regional. | Evitar lock-in de supply chain y mantener ruta maker -> flight-like -> flight | I/A | Sistema/Costos | `ADR-20260710-diy-low-cost-maker-latam-design-policy.md`, `06_Costs/bom_overview.md` |

## 2) Requisitos P1 — Uplink con nodos típicos (success-first)

| ID | Requisito (shall) | Rationale | Verif. | Dueño | Trazabilidad |
|---|---|---|---|---|---|
| COMMS-UL-01 | El uplink LoRa shall soportar nodos de clase típica (+20–21 dBm, sin PA externo, antena 0–2 dBi) con mejoras solo de antena+firmware. No se fija SKU de mercado como requisito. | Compatibilidad/costo con clase objetivo | D | COMMS | `ADR-20260313-nodo-tipico-lora-clase.md`; análisis de soporte: `04_Communications/link_budget_lora_uplink_preliminary.md` (Preliminary) |
| COMMS-UL-02 | Los nodos shall operar en modo B2 slotted (pass-aware) para reducir colisiones cuando dispongan de base temporal válida. Sin base temporal validada, shall hacer fallback a B1. | Escalabilidad + integridad de slots | T | Node FW | `ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx.md`; ver también `ADR-20260313-b2-uplink-timebase-requirement.md` |
| COMMS-UL-03 | Los nodos shall poder predecir pasadas offline usando TLE+SGP4. | Sin NTP | T | Node FW | `ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx.md` |
| COMMS-UL-04 | El receptor orbital shall registrar por paquete: timestamp, RSSI, SNR, CFO y CRC status. | Evidencia / debug | T | COMMS/OBC | `01_Mission/mission_definition.md` |
| COMMS-UL-05 | El sistema shall bajar por defecto un resumen por pasada (agregado) y permitir detalle on-demand. | Cuello de downlink | T | FSW/COMMS | `04_Communications/uplink_data_products_and_downlink_policy.md` |
| COMMS-UL-06 | El modo B2 (pass-aware slotted) shall disponer de una base temporal validada (deriva dentro del guard time) antes de considerarse aceptado. Opciones: base validada experimentalmente, cristal/RTC externo adecuado, o resincronización activa ≤24 h antes de la pasada. Sin base temporal validada, el nodo shall operar en B1. | Evitar desalineación de slots por deriva de RTC no validada | T | Node FW | `ADR-20260313-b2-uplink-timebase-requirement.md`; ver `04_Communications/uplink_lora_slotted_protocol.md` §10 |

## 3) Requisitos de compliance y validación

| ID | Requisito (shall) | Rationale | Verif. | Dueño | Trazabilidad |
|---|---|---|---|---|---|
| COMP-REQ-01 | El sistema shall operar dentro de form factor 1.5U (100×100×150 mm) con masa, CG (Centro de Gravedad) y propiedades mecánicas según ICD del integrador. | Compatibilidad dispenser | I | Estructura | `01_Mission/compliance_matrix.md`, ICD integrador (TBD) |
| COMP-REQ-02 | Los TX shall implementar los RF inhibits (mínimo 3 inhibiciones independientes) requeridos por el integrador de lanzamiento. | Seguridad de lanzamiento | I | COMMS/EPS | `01_Mission/compliance_matrix.md`, CDS Rev 14.1 (placeholder) |
| COMP-REQ-03 | El satélite shall NO transmitir desde ISM (LoRa) en órbita durante el MVP. El uplink LoRa orbital es RX-only. | Riesgo regulatorio | T | COMMS | `00_MVP/MVP v2.2.md`, `01_Mission/compliance_matrix.md` |
| COMP-REQ-04 | Shall existir evidencia de coordinación IARU antes de cerrar el bandplan amateur-sat para operación. | Regulatorio internacional | D | Operaciones | `01_Mission/compliance_matrix.md` (CX-RF-04) |
| COMP-REQ-05 | Los materiales de estructura y PCB shall cumplir requisitos de venting, outgassing y compatibilidad de vacío del integrador (TBD). | Seguridad dispenser / vacío | I | Estructura | `01_Mission/compliance_matrix.md` |
| COMP-REQ-06 | Shall existir dossier de batería y carga para topología 2S + MPPT (incluyendo quimismo, capacidad, curvas de carga/descarga y certificaciones si aplica). | Seguridad / compliance batería | I/D | EPS | `01_Mission/compliance_matrix.md` |

## 4) Requisitos de feature opcional PHOTO_DEMO

| ID | Requisito (shall) | Rationale | Verif. | Dueño | Trazabilidad |
|---|---|---|---|---|---|
| MIS-REQ-PH-01 | El payload [PHOTO_DEMO] shall iniciar OFF por defecto al boot. | Off-by-default | T | FSW/EPS | `08_Decisions/ADR-20260313-photo-demo-opcional-no-critico.md` |
| MIS-REQ-PH-02 | El payload [PHOTO_DEMO] shall usar cuota best-effort por pasada sin desplazar housekeeping/comandos/LORA_LOG. | Aislamiento cadena principal | T | FSW/COMMS | `08_Decisions/ADR-20260313-photo-demo-opcional-no-critico.md` |
| MIS-REQ-PH-03 | El payload [PHOTO_DEMO] shall transferir imagen por chunks reanudables tras selección uplink. | Robustez de transferencia | T | FSW/COMMS | `00_MVP/MVP v2.2.md` §17 |
| MIS-REQ-PH-04 | La falla de [PHOTO_DEMO] shall no degradar la cadena principal de misión. | Aislamiento | T | FSW | `08_Decisions/ADR-20260313-photo-demo-opcional-no-critico.md` |

## 5) Requisitos del payload IA experimental

| ID | Requisito (shall) | Rationale | Verif. | Dueño | Trazabilidad |
|---|---|---|---|---|---|
| IA-REQ-01 | El payload IA shall ser power-gated de forma independiente en un rail dedicado. | Aislamiento eléctrico; carga no crítica para supervivencia. | T | EPS/FSW | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-02 | El payload IA shall iniciar en estado OFF por defecto al boot. | Seguridad operacional; off-by-default. | T | FSW | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-03 | El payload IA shall estar OFF en `MISSION_MODE = SAFE`, en eclipse y cuando `EPS_STATE` sea `CRIT` o `LOW`. | Supervivencia energética; SAFE primero. | T | FSW/EPS | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md`, `ADR-20260314-eps-state-4-levels.md` |
| IA-REQ-04 | El payload IA shall nunca sobreescribir ni bypass las reglas de seguridad determinísticas de misión. | OBC es autoridad de vuelo. | T | FSW | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-05 | El OBC (On-Board Computer) shall validar toda recomendación del payload IA a través del Runtime Safety Supervisor antes de ejecutarla. | Supervisor determinístico obligatorio. | T | FSW | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-06 | El sistema shall soportar uplink de system prompts / policy prompts versionados para modificar el comportamiento del payload IA en órbita sin reemplazar el modelo. | Adaptabilidad en órbita; separación modelo/política. | T | COMMS/FSW | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-07 | El sistema shall registrar telemetría de comportamiento del payload IA por evento (timestamp, model_version, prompt_version, decision_id, recommended_action, confidence, supervisor_result, MISSION_MODE, EPS_STATE). | Dataset científico de la misión. | T | FSW/Ground | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-08 | El payload IA shall poder ser deshabilitado desde tierra en cualquier momento. | Control operacional; ground safety. | T | COMMS/FSW | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-09 | La familia de hardware baseline del payload IA shall ser CM5 (Raspberry Pi Compute Module 5). No se fija SKU de marketplace como requisito normativo. | Familia tecnológica adoptada; sin dependencia de SKU. | I | EPS/SYS | `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` |
| IA-REQ-10 | El modelo baseline funcional del payload IA shall ser IBM Granite 350M fine-tuned (LoRA/QLoRA), con licencia Apache 2.0, hasta que una nueva ADR `Accepted` lo reemplace. El modelo final de vuelo es TBD y no se declara hasta Gate IA-2. | Baseline funcional definido por ADR-20260316; evita cambio de modelo sin trazabilidad formal. | I | FSW/SYS | `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md` |
| IA-REQ-11 | El modelo baseline experimental del payload IA shall modificarse únicamente mediante una nueva ADR `Accepted`. No se permite cambio de modelo por edición directa de documentos de subsistema. | Gobierno del baseline de modelo; trazabilidad de cambios de comportamiento IA. | I | SYS | `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md` |

> **Nota:** Los requisitos IA-REQ-xx son verificables en banco a partir de Gate IA-2 (para CM5 real). La plataforma de banco prevista para esa verificación es `EPS_Bench1_1S` extendido, con rail IA bench-only por `J_AI_PWR` y `JP1` reservado a control/sense/telemetría. IA-REQ-10 tiene evidencia funcional de banco (benchmark corrected + holdout, 2026-03-16). El modelo Granite 350M fine-tuned ha alcanzado el estado de baseline funcional de banco; queda pendiente validación en hardware CM5 real. No se fijan consumos, masa ni térmica como requisitos cerrados ni se valida aquí el rail IA de vuelo.

## 6) Requisitos estructurales y térmicos (2026-03-20)

| ID | Requisito (shall) | Rationale | Verif. | Dueño | Trazabilidad |
|---|---|---|---|---|---|
| STR-REQ-01 | El layout de caras shall asignar paneles solares a +Y, ±X, −Z y radiador a −Y (LTAN 10h). | Maximizar energía solar con disipación térmica efectiva. | A / I | Structure | `ADR-20260320-orbit-attitude-solar-layout-baseline.md` |
| STR-REQ-02 | La actitud nominal shall ser 10×10 nadir (+Z Tierra, +X ram). | Score máximo en barrido orbital. | A | Mission/ADCS | `ADR-20260320-orbit-attitude-solar-layout-baseline.md` |
| THR-REQ-01 | El recubrimiento del radiador shall tener α_solar ≤ 0.20 y ε_IR ≥ 0.88. | Mantener Tmax CM5 ≤ 40°C en condiciones nominales. | T / A | Structure/Thermal | `ADR-20260320-thermal-design-radiator-cm5-coupling.md` |
| THR-REQ-02 | El CM5 shall estar acoplado térmicamente al panel radiador con G ≥ 0.60 W/K. | Disipar hasta 4.5 W pico con ΔT ≤ 8°C. | T | Structure/Thermal | `ADR-20260320-thermal-design-radiator-cm5-coupling.md` |
| THR-REQ-03 | La temperatura mínima de batería en eclipse shall ser ≥ −10°C. | Límite operativo Li-ion en descarga. | A / T | EPS/Thermal | `ADR-20260320-thermal-design-radiator-cm5-coupling.md` |
| THR-REQ-04 | El recubrimiento del radiador shall cumplir TML ≤ 1.0% y CVCM ≤ 0.1%. | CDS Rev. 14.1 §2.1.7 outgassing. | I / T | Structure/Thermal | CDS Rev. 14.1 §2.1.7 |

> **Nota:** STR-REQ-xx y THR-REQ-xx son verificables a partir de Gate IA-1 (térmica CM5) y PDR mecánico. THR-REQ-03 tiene evidencia preliminar del simulador v9.2 (Tmin batt ≥ 20°C); cierre requiere TVAC o ensayo en banco térmico.

## 7) Notas
- Requisitos numéricos finos (elevación mínima, canales exactos, BW125 vs BW250) quedan como **TBD** hasta completar `docs/COMMS/uplink_lora_bench_testing_plan.md`.
- **BW final del uplink LoRa sigue TBD.** BW250 es el candidato preferente para robustez frente a CFO/Doppler; BW125 requiere evidencia de banco/campo con margen suficiente.
- **Criterio provisional de downlink UHF:** la validación nominal del downlink UHF se establece provisionalmente para elevaciones ≥20°. Operación a <20° es experimental/oportunista, no criterio nominal de éxito del MVP. Ver `04_Communications/link_budget_uhf_preliminary.md` §6.2 y `ADR-20260313-uhf-downlink-operational-mask.md`.
- **SatNOGS / visibilidad de datos:** SatNOGS se usa solo para `PUBLIC_BEACON` receive-only. Payload, ciencia, PHOTO_DEMO, logs IA detallados y uplink de comandos quedan en perfiles privados/controlados. Cifrado/autenticacion y restricciones de contenido quedan sujetos al cierre regulatorio final.
- **Estacion dual-use:** la estacion propia puede compartir antena/rotor con SatNOGS, pero el modo SatNOGS queda estrictamente receive-only y sin acceso al transmisor. Ver `04_Communications/ground_station_dual_use_satnogs_australis.md`.
- El target solar con payload IA activo queda **TBD** hasta medición real del CM5 y cierre del duty-cycle orbital.
- `SOLAR_ONLY` se considera contingencia en evaluación; no requisito bloqueado de aceptación MVP hasta nueva ADR `Accepted`.
- Requisitos marcados con "ICD integrador (TBD)" quedan como `Blocked by Integrator` en la compliance matrix hasta recibir documentación del integrador de lanzamiento.
- Las referencias a documentos `Preliminary` o `Proposed` en la columna de trazabilidad son **análisis de soporte**, no fuente normativa única. El `shall` se respalda en ADR `Accepted` o baseline cuando existe.
