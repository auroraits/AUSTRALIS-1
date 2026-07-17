# Architecture Notes — AUSTRALIS-1 / DIY Nanosat

**Revisión:** 2026-07-10
**Estado:** Baseline

Este archivo funciona como mapa del repositorio y snapshot arquitectónico alineado con el baseline y ADRs vigentes. Es la referencia de entrada para cualquier agente (humano o IA) que trabaje sobre el repo.

---

## 1) Precedencia documental

Si hay contradicciones entre documentos, usar este orden estricto:

1. **ADR `Accepted`** en `08_Decisions/` (máxima autoridad)
2. **`00_MVP/MVP v2.2.md`** (baseline consolidado vigente)
3. **`SYSTEM_BASELINE.md`** (resumen de entrada rápida)
4. **Documentación por subsistema** (`01_Mission/` a `07_Risk/`)
5. **Documentos `Draft` / `Proposed` / `Preliminary`** (contexto técnico; no normativos)
6. **Históricos / Superseded** (trazabilidad)

**Regla:** Un documento `Draft`, `Proposed` o `Preliminary` NO puede sobreescribir una decisión bloqueada por ADR `Accepted`.

---

## 2) Estados documentales permitidos

| Estado | Descripción | Puede bloquear decisión |
|---|---|---|
| `Accepted` | ADR bloqueada; normativa | Sí (máxima autoridad) |
| `Baseline` | Documento de referencia del sistema; sincronizado | No directamente; hereda ADRs |
| `Active` | Documento vivo y coherente con baseline | No |
| `Draft` | Trabajo en progreso; no normativo | No |
| `Proposed` | Propuesta formal; requiere ADR para bloquearse | No |
| `Preliminary` | Análisis o dato pre-decisión | No |
| `Superseded` | Reemplazado; conservado para trazabilidad | No |
| `Historical Snapshot` | Instantánea histórica; no normativa | No |

---

## 3) Cabecera mínima recomendada

Todo documento técnico clave debe incluir:

```markdown
**Revisión:** YYYY-MM-DD
**Estado:** [Active | Draft | Proposed | Preliminary | Superseded | Historical Snapshot]
**Trazabilidad:** [ADR / documento fuente]
```

---

## 4) Definición de "Hecho" documental

Un cambio queda "hecho" si:
1. Documento del subsistema actualizado.
2. Referencias cruzadas consistentes.
3. ADR creado/actualizado si cambió una decisión de arquitectura.
4. `06_Costs/*` y `07_Risk/*` ajustados si hay impacto.
5. `00_MVP/MVP v2.2.md`, `SYSTEM_BASELINE.md` y este `architecture.md` sincronizados.
6. `01_Mission/compliance_matrix.md` actualizada si corresponde.
7. `01_Mission/validation_plan_and_stage_gates.md` actualizado si corresponde.

---

## 5) Regla de propagación de cambios

| Cambio en | Propagar a |
|---|---|
| Arquitectura / baseline | `00_MVP/MVP v2.2.md`, `SYSTEM_BASELINE.md`, `architecture.md`, ADR |
| Política DIY / apertura / supply chain | `SYSTEM_BASELINE.md`, `README.md`, `01_Mission/requirements_matrix.md`, `01_Mission/compliance_matrix.md`, `06_Costs/BOM_master.csv`, `06_Costs/bom_overview.md`, `07_Risk/top_risks.md` si corresponde |
| Energía / EPS | `03_Power/*`, `05_Software/ai_payload_architecture.md`, `01_Mission/mission_definition.md`, `01_Mission/compliance_matrix.md`, `01_Mission/validation_plan_and_stage_gates.md`, `06_Costs/*`, `07_Risk/*` |
| COMMS / RF | `04_Communications/*`, `07_Risk/*`, `06_Costs/*` |
| Software / FSW | `05_Software/*`, `00_MVP/MVP v2.2.md` (si cambia comportamiento) |
| BOM / costos | `06_Costs/BOM_master.csv`, `06_Costs/bom_overview.md` |
| Riesgos | `07_Risk/top_risks.md`, matrices específicas |
| Compliance / requisitos | `01_Mission/compliance_matrix.md`, `01_Mission/requirements_matrix.md` |
| **Payload IA** | `05_Software/ai_payload_architecture.md`, `05_Software/software_framework_mvp22.md`, `03_Power/Power Budget.md`, `04_Communications/uplink_data_products_and_downlink_policy.md`, `01_Mission/requirements_matrix.md`, `01_Mission/compliance_matrix.md`, `06_Costs/cost_overview.md`, `07_Risk/top_risks.md` |

---

## 6) Snapshot de decisiones vigentes

| ADR | Estado | Decisión corta |
|---|---|---|
| `ADR-20260710-diy-low-cost-maker-latam-design-policy.md` | Accepted | AUSTRALIS-1 queda fijado como proyecto DIY, low cost, publicable/source-available y orientado a componentes maker/COTS disponibles en Argentina/Latinoamerica, con excepciones trazadas. |
| `ADR-20260704-satnogs-public-beacon-private-payload-uplink.md` | Accepted | SatNOGS se adopta como red receive-only para `PUBLIC_BEACON`; payload downlink y uplink de comandos quedan privados/controlados por estacion/es propia/s o autorizada/s. |
| `ADR-20260615-ai-model-roles-granite350m-flight-candidate-2b-experimentation.md` | Accepted | Granite 350M queda como candidato de vuelo / flight candidate; Granite 3.1 2B queda reservado para experimentacion de banco y ground experimentation. |
| `ADR-20260320-orbit-attitude-solar-layout-baseline.md` | Accepted | Órbita SSO 600 km LTAN 10h, actitud 10×10 nadir, layout solar +Y/±X/−Z, radiador −Y, sin desplegables. |
| `ADR-20260320-thermal-design-radiator-cm5-coupling.md` | Accepted | Radiador −Y con AZ-93/anodizado blanco, CM5 acoplado por pad térmico, sin heater de batería. |
| `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md` | Accepted | IBM Granite 350M fine-tuned como baseline funcional de banco del payload IA. Actualiza §C de ADR-20260314 (modelo). Resto de ADR-20260314 vigente. |
| `ADR-20260314-mission-redef-ai-primary.md` | Accepted | AUSTRALIS-1 redefine la misión: payload IA como objetivo primario; IoT store-and-forward pasa a secundario. |
| `ADR-20260314-eps-state-4-levels.md` | Accepted | `EPS_STATE` ampliado a `CRIT | LOW | NOMINAL | HIGH`. |
| `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` | Accepted | Payload IA primario: familia CM5, supervisor determinístico, power-gated. §C (modelo) actualizado por ADR-20260316. |
| `ADR-20260313-gobierno-documental.md` | Accepted | Metodología documental global; jerarquía AGENTS.md; precedencia documental. |
| `ADR-20260313-photo-demo-opcional-no-critico.md` | Accepted | PHOTO_DEMO congelado como opcional, no crítico, off-by-default, best-effort. |
| `ADR-20260313-nodo-tipico-lora-clase.md` | Accepted | Nodo LoRa terrestre definido como clase (sin fijar SKU). |
| `ADR-20260313-eps-separacion-bench-flightlike-flight.md` | Accepted | Separación inequívoca de capas EPS. |
| `ADR-20260313-compliance-matrix-artefacto-sistema.md` | Accepted | Compliance matrix como artefacto vivo obligatorio. |
| `ADR-20260313-b2-uplink-timebase-requirement.md` | Accepted | B2 slotted requiere base temporal validada. |
| `ADR-20260313-uhf-downlink-operational-mask.md` | Accepted | Máscara operativa provisional downlink UHF: validación nominal ≥20°; <20° experimental. |
| `ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx.md` | Accepted (preliminar) | Uplink LoRa P1 en modo B2 slotted y exploración de RX tipo concentrator. |
| `ADR-20260218-uhf-link-budget-preliminary.md` | Accepted (preliminar) | Downlink UHF con objetivo 500 mW RF; margen a 10° corregido a +1 dB de papel. |
| `ADR-20260218-downlink-arbitration-and-subsystem-power-framework.md` | Accepted | Framework permanente: colas de downlink + Fault/Power Manager + set mínimo de comandos. |
| `ADR-20260218-battery-topology-2s-flight.md` | Accepted | Topología batería de vuelo bloqueada en 2S; capacidad de referencia actualizada a ~22 Wh nominal. |
| `ADR-20260218-geiger-removed-from-mvp.md` | Accepted | Se elimina Geiger/HV del Science Pack MVP. |
| `ADR-20260218-eps-bench1s-cots-to-custom-flight-pcb.md` | Accepted | Política permanente COTS bench → custom flight PCB para EPS. |
| `ADR-20260212-telemetry-bench-433mhz.md` | Accepted | Banco 433 MHz ASK limitado a validación de laboratorio SW/HW. |
| `ADR-20260212-quaternion-telemetry-dashboard-theme.md` | Accepted | Telemetría quaternion + dashboard actualizado para pipeline de banco. |
| `ADR-20260212-imu-frames-and-calibration.md` | Accepted | Política de frames IMU y calibración en banco de telemetría. |
| `ADR-20260212-move-embedded-under-05-software.md` | Accepted | Firmware embebido consolidado bajo `05_Software/embedded`. |

---

## 7) Modelo operativo canónico

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

- `SAFE` = modo por defecto post-reset y en eclipse.
- La actividad científica es una actividad dentro de `MISSION_MODE = NOMINAL`; no es un modo independiente.
- Si `EPS_STATE = CRIT` → sistema degrada a `MISSION_MODE = SAFE`.
- Si `EPS_STATE = LOW` → `SAFE` por defecto; `NOMINAL` solo para housekeeping esencial.
- El payload IA solo puede operar con `MISSION_MODE = NOMINAL`, fase de sol y `EPS_STATE >= NOMINAL`.
- La denominación "SCIENCE MODE" de versiones anteriores queda supersedada.

---

## 8) Separación EPS: bench / flight-like / flight

| Capa | Nombre | Descripción |
|---|---|---|
| Bench | `EPS_Bench1_1S` | Validación funcional COTS, 1S, extendida para Gate IA-2 con FPM bench + rail IA bench-only + inyección externa 5V. No es hardware de vuelo. |
| Flight-Like | `EPS_Flight_Like_2S_MPPT` | PCB custom en KiCad, arquitectura 2S + MPPT. No calificado. |
| Flight | `EPS_Flight_2S_MPPT` | Hardware final de vuelo, 2S + MPPT, con política COTS-to-Flight completa. |

---

## 9) Arquitectura del repositorio (estado real)

| Ruta | Rol principal | Estado actual |
|---|---|---|
| `00_MVP/` | Evolución del documento maestro. | Versiones `v1` a `v2.2`; `v2.2` es baseline activo. |
| `01_Mission/` | Definición de misión, requisitos verificables, compliance y validación. | Activo. Incluye `compliance_matrix.md` y `validation_plan_and_stage_gates.md`. |
| `02_Structure/` | Estructura, block diagram e ICD de alto nivel. | `Block Diagram.md` alineado con framework MVP. |
| `03_Power/` | EPS por capas (bench/flight-like/flight), budget, sizing y reglas. | Activo. `EPS_Bench1_1S` extendido para Gate IA-2 con FPM bench + rail IA bench-only + `J_AI_PWR`; batería de referencia **~22 Wh**; solar con IA **TBD**. |
| `04_Communications/` | Arquitectura RF, link budgets, protocolo uplink y política de datos. | Activo. UHF/LoRa preliminar, slotted uplink, resumen-first, análisis OpenLST, arquitectura SatNOGS `PUBLIC_BEACON` y diseno draft de estacion terrena dual-use SatNOGS/AUSTRALIS. |
| `05_Software/` | Framework de vuelo, ops de nodos, firmware bench y dashboard de tierra. | Activo. `ai_payload_architecture.md` documenta la integración bench de Gate IA-2 sobre `EPS_Bench1_1S` extendido. |
| `06_Costs/` | BOM maestra y modelos ROM de costos por subsistema. | Activo. Batería 2S1P de referencia reflejada en BOM; delta bench-only de Gate IA-2 separado del baseline de vuelo; politica maker/LATAM exige proveedor/region/alternativa/riesgo para items nuevos. |
| `07_Risk/` | Riesgos top y matrices específicas de mitigación. | Activo con riesgos IA 17–30 ligados al éxito primario y a la integración bench del CM5. |
| `08_Decisions/` | Registro ADR. | 27 ADRs registrados: 22 `Accepted` o `Accepted (preliminar)`, 1 `Superseded` y 4 sin metadata de estado formal. |
| `99_References/` | Fuentes externas. | Librería activa de soporte. |
| `docs/` | Planes de prueba y notas operativas de banco. | Incluye plan COMMS uplink bench, soporte EPS/telemetría. |
| `SYSTEM_BASELINE.md` | Punto rápido de entrada al baseline. | Sincronizado rev 2026-03-14. |
| `README.md` | Portada del proyecto. | Sincronizado rev 2026-03-14. |
| `AGENTS.md` | Política documental global (raíz). | Rev 2026-03-14. |

---

## 10) Baseline técnico por subsistema

| Subsistema | Bloqueado por baseline/ADR | En evaluación (sin bloquear baseline) |
|---|---|---|
| Mission | **AUSTRALIS-1**: payload IA como objetivo primario; IoT store-and-forward como objetivo secundario; compliance matrix activa. **Órbita: SSO 600 km LTAN 10h (ADR-20260320).** | Ajustes finos de criterios operativos por resultados de banco/campo. Sensibilidad estacional β pendiente. |
| Payload IA | OBC como autoridad de vuelo. Payload IA primario (CM5 family, IBM Granite 350M fine-tuned QLoRA) con RuntimeSafetySupervisor, power-gated, off-by-default en SAFE/eclipse/DOWNLINK_WINDOW. Gate IA-2 usa `EPS_Bench1_1S` extendido con carrier board COTS externa y `5V_AI_EXT` bench-only. | Hardware de vuelo calificado TBD; consumo CM5 real TBD; térmica TBD; Gate IA-2 pendiente sin evidencia T11–T21. |
| EPS | Vuelo 2S+MPPT, banco 1S validación, referencia batería ~22 Wh nominal (2S1P 18650 3.0 Ah), target solar ≥1.2 W solo sin IA activa. `EPS_Bench1_1S` se extiende para Gate IA-2 sin cambiar la capa flight-like/flight. | Cierre del target solar con IA, posible necesidad de 2S2P, conflicto pico ~3 W vs ~5 W (CONF-01). No extrapolar `5V_AI_EXT` bench-only al rail IA de vuelo. |
| COMMS | Uplink LoRa RX-only (915), downlink/TTC UHF (435 FSK 1k2), nodo típico como clase, política resumen-first, `AI_BEHAVIOR_LOG` mayor prioridad best-effort científica, máscara operativa provisional ≥20° downlink. `PUBLIC_BEACON` SatNOGS-friendly publico; `CONTROLLED_DOWNLINK` de payload y `PRIVATE_UPLINK` solo por estacion/es propia/s o autorizada/s. Estacion propia dual-use: SatNOGS receive-only + AUSTRALIS privado con TX aislado. | Selección de módulo UHF final, adopción OpenLST-derived TTC, parámetros finos uplink LoRa, decoder/protocolo del beacon publico, cierre regulatorio de privacidad/cifrado, implementacion fisica de estacion/torre/TX interlocks. |
| FSW/OPS | SAFE por defecto, modelo dual `MISSION_MODE` / `EPS_STATE`, arbitraje por colas, power-gating, health signals, comando mínimo. | Parámetros de cuota/retención/log y tuning operativo post-pruebas. |
| Ground/Bench SW | Pipeline 433 solo laboratorio. Arquitectura de datos de tierra documentada. | Implementación completa de persistencia/replay/export en el dashboard. |
| Costos | BOM maestra activa con stages obligatorios y politica maker/LATAM. | Completar valores numéricos, cotizaciones trazables y alternativas locales/regionales cuando existan. |
| Riesgos | Matrices consolidadas activas. | Cerrar riesgos principales con evidencia de validación. |

---

## 11) Conflictos documentales abiertos (para resolución humana)

| ID | Conflicto | Documentos involucrados | Acción requerida |
|---|---|---|---|
| CONF-01 | Pico EPS: `~3 W` (Power Budget, EPS Sizing) vs estimaciones de hasta `~5 W` en RF_ANALISYS_OPENLST; además el payload IA agrega un pico hipotético total de `6–7 W` y deja el target solar con IA **TBD** | `03_Power/Power Budget.md`, `03_Power/EPS Sizing.md`, `04_Communications/RF_ANALISYS_OPENLST.md` | Medición real con hardware TX final y Gate IA-2. No cerrar hasta tener hardware. |
| CONF-02 | Bitrate UHF: baseline 1200 bps vs OpenLST 7416 baud | `04_Communications/rf_subsystem_overview.md`, `04_Communications/RF_ANALISYS_OPENLST.md` | Definir en ADR de adopción OpenLST si se decide avanzar. |
| CONF-03 | Privacidad/control del downlink de payload: requisito de `CONTROLLED_DOWNLINK` vs posible encuadre amateur-satellite y restricciones de cifrado/contenido | `04_Communications/satnogs_public_beacon_architecture.md`, `04_Communications/uplink_data_products_and_downlink_policy.md`, `08_Decisions/ADR-20260704-satnogs-public-beacon-private-payload-uplink.md` | Cerrar mecanismo de autenticacion/confidencialidad contra ENACOM/IARU/ITU antes de vuelo. |

---

## 12) Cambios recientes incorporados

- 2026-07-10 (politica DIY / low cost / maker LATAM): nueva ADR `ADR-20260710-diy-low-cost-maker-latam-design-policy.md`. El baseline queda alineado a proyecto DIY, low cost, publicable/source-available no comercial y reproducible con componentes maker/COTS disponibles en Argentina/Latinoamerica. Actualizados: `SYSTEM_BASELINE.md`, `README.md`, `01_Mission/mission_definition.md`, `01_Mission/requirements_matrix.md`, `01_Mission/compliance_matrix.md`, `06_Costs/bom_overview.md`, `07_Risk/top_risks.md`.
- 2026-07-05 (Ground segment dual-use): agregado diseno draft `04_Communications/ground_station_dual_use_satnogs_australis.md`. Define estacion UHF direccional con rotor AZ/EL, SatNOGS receive-only, AUSTRALIS controlled downlink/private uplink, switch T/R digital fail-safe, recomendacion inicial de torre y linea de transmision.
- 2026-07-04 (COMMS/RF SatNOGS y visibilidad de datos): nueva ADR `ADR-20260704-satnogs-public-beacon-private-payload-uplink.md`. SatNOGS queda como red receive-only para `PUBLIC_BEACON`; payload downlink (`PHOTO_DEMO`, performance IA, `AI_BEHAVIOR_LOG`, `SCIENCE`, `LORA_LOG`) y uplink de comandos quedan privados/controlados por estacion/es propia/s o autorizada/s. Agregado documento `04_Communications/satnogs_public_beacon_architecture.md`.
- 2026-04-03 (actualización documental bench IA/EPS): `EPS_Bench1_1S` queda extendido como bench-only para Gate IA-2 con FPM bench, rail IA bench-only, `J_AI_PWR` e inyección externa de 5V para CM5 real. Actualizados: `03_Power/EPS_Bench1_1S.md`, `03_Power/EPS_PCB/EPS_Bench1S/eps_bench_mods.md`, `05_Software/ai_payload_architecture.md`, `01_Mission/mission_definition.md`, `01_Mission/requirements_matrix.md`, `01_Mission/compliance_matrix.md`, `01_Mission/validation_plan_and_stage_gates.md`, `06_Costs/BOM_master.csv`, `06_Costs/cost_overview.md`, `06_Costs/bom_overview.md`, `06_Costs/eps_bench1_1s_cost_model.md`, `07_Risk/top_risks.md`, `00_MVP/MVP v2.2.md`, `architecture.md`. No cambia el baseline de vuelo 2S + MPPT.
- 2026-03-20 (barrido orbital/térmico, simulador v9.2 auditado): nuevas ADRs `ADR-20260320-orbit-attitude-solar-layout-baseline.md` y `ADR-20260320-thermal-design-radiator-cm5-coupling.md`. Órbita bloqueada en SSO 600 km LTAN 10h, eclipse ~34%. Actitud 10×10 nadir. Layout solar body-mounted +Y/±X/−Z (484 cm²), radiador −Y (AZ-93 o anodizado blanco). Generación simulada ~72 Wh/24h con η=24%, margen 3.4× con IA payload al 20% duty. Diseño térmico: CM5 acoplado a pared −Y por pad térmico (G≈1.5 W/K), Tmax CM5 ≤ 40°C, Tmin batt ≥ 20°C, sin heater. Actualizados: `00_MVP/MVP v2.2.md`, `SYSTEM_BASELINE.md`, `01_Mission/requirements_matrix.md`, `01_Mission/compliance_matrix.md`, `06_Costs/BOM_master.csv`, `07_Risk/top_risks.md`.
- 2026-03-16 (sesión de entrenamiento y benchmark IA): nueva ADR `ADR-20260316-ai-payload-granite350m-baseline-funcional-banco.md`. IBM Granite 350M fine-tuned adoptado como nuevo baseline funcional de banco del payload IA. SmolLM2-360M-Instruct INT4 pasa a baseline histórico/superseded. Pipeline QLoRA operativo en RTX 4060. Benchmark corrected: pass_rate BASE 14.29 % → FINE_TUNED 57.14 %; avg_score_ratio 0.3163 → 0.8313. Holdout funcional completado. Evidencia técnica en `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`. ADRs actualizadas: ADR-20260314 §C superseded por ADR-20260316. Gate IA-2 definido.
- 2026-03-14 (pasada correctiva + redefinición de misión): nuevas ADRs `ADR-20260314-mission-redef-ai-primary.md` y `ADR-20260314-eps-state-4-levels.md`. Corregidos: SCI+SAFE **0.371 → 0.451 Wh/orbita**, FSPL UHF 10° **152 → 153 dB**, margen UHF 10° **+2 → +1 dB**, Caso A LoRa renombrado a **nodo mínimo / legacy**, batería de referencia **~22 Wh nominal**, target solar con IA marcado **TBD**, prioridad de `AI_BEHAVIOR_LOG` elevada, misión redefinida como AUSTRALIS-1.
- 2026-03-14: ADR `ADR-20260314-ai-payload-cm5-smollm2-360m-runtime-supervision.md` — payload IA aceptado.
- 2026-03-13 (correctiva): pasada correctiva de trazabilidad. Corregidas: fuentes normativas de `requirements_matrix.md`; BW decisión abierta con BW250 como candidato preferente; máscara operativa downlink UHF ≥20° provisional; RF hardware immaturity documentado como riesgo R16.
- 2026-03-13: sincronización transversal completa. Nuevas ADRs: gobierno documental, PHOTO_DEMO opcional, nodo típico como clase, separación EPS capas, compliance matrix.
- 2026-03-05: sincronización transversal de `architecture.md`, `SYSTEM_BASELINE.md`, `README.md` y `00_MVP/MVP v2.2.md`.
- 2026-03-03: `04_Communications/RF_ANALISYS_OPENLST.md` agrega evaluación técnica OpenLST.
- 2026-02-27: ampliación `03_Power/EPS_Bench1_1S.md` con netlist, power-gating, telemetría y plan de pruebas.
- 2026-02-20: paquete COMMS P1.

---

## 13) Pendientes abiertos (TBD)

1. Selección final de módulo/transceptor UHF y medición real de eficiencia PA.
2. Cierre medido del uplink LoRa con nodos típicos bajo CFO/Doppler. **BW definitivo TBD**; BW250 candidato preferente.
3. Confirmar si la línea OpenLST-derived TTC pasa de evaluación a decisión (ADR pendiente).
4. Definir protocolo/decoder del `PUBLIC_BEACON` y paquete SatNOGS DB.
5. Completar valores numéricos del modelo ROM de costos y BOM.
6. Cerrar parámetros de uplink LoRa: elevación mínima, canalización exacta, BW definitivo, criterio de aceptación.
7. Resolución de CONF-01: pico EPS real con hardware TX final y consumo real del CM5. **No declarar cerrado sin medición.**
8. Cierre del target solar con payload IA activo.
9. Confirmar si la batería de referencia `2S1P` alcanza o si debe escalarse a `2S2P`.
10. Coordinación IARU y camino regulatorio ENACOM, incluyendo tratamiento de privacidad/cifrado para `CONTROLLED_DOWNLINK` y `PRIVATE_UPLINK`.
11. Dossier de batería y topología 2S+MPPT para compliance con integrador.
12. Definir ICD completo con integrador.
13. Validación experimental de base temporal del modo B2.
14. Confirmación o revisión de máscara operativa downlink UHF ≥20° con hardware TX real.
15. Implementación de `ground_data_architecture.md` antes de Gate B.
16. **Gate IA-2 — Payload IA en hardware CM5 real sobre `EPS_Bench1_1S` extendido:** boot reproducible con Granite fine-tuned, inferencia en CM5 real, medición de consumo (idle/active/inference), validación térmica básica, integración OBC↔CM5 física, RuntimeSafetySupervisor integrado.
17. Análisis térmico y de masa del payload IA (TBD — sin ensayo en hardware real).
18. Selección de interfaz OBC ↔ CM5 (UART / SPI / I2C — TBD).
19. Resolución de defectos residuales del fine-tuning: `ai_payload_state` contextual, `policy override` total, normalización de `decision_id`.
