# AUSTRALIS-1 — DIY Nanosat

**Revisión:** 2026-06-15

## Publicación y licencia

Este repositorio es una publicación técnica **source-available no comercial**.
Se comparte para estudio, experimentación personal, educación, investigación no
comercial y colaboración abierta no comercial.

- Código, scripts, firmware y software: **PolyForm Noncommercial 1.0.0**.
- Documentación, diseños, datasets, CAD/PCB y material de arquitectura:
  **CC BY-NC-SA 4.0**.
- Nombre, identidad del proyecto, marcas, descubrimientos patentables y uso
  comercial: **derechos reservados**; requieren permiso o licencia escrita.

Ver:

- `LICENSE.md`
- `COMMERCIAL_USE.md`
- `THIRD_PARTY_NOTICES.md`
- `PUBLICATION_AUDIT.md`
- `PUBLIC_RELEASE_PROCESS.md`
- `LEGAL_ENFORCEMENT_REVIEW.md`
- `CONTRIBUTING.md`

Nota importante: este modelo permite colaboración pública no comercial, pero no
es "open source" OSI porque restringe uso comercial. Para publicar, no cambiar
la visibilidad del repo privado tal cual. La decisión vigente es publicar por
**mirror/export limpio**, sin historial privado.

## Objetivo (MVP)
AUSTRALIS-1 busca poner un payload de inteligencia artificial en órbita LEO, operarlo como asistente de vuelo autónomo bajo supervisión determinística y descargar a tierra datos de comportamiento útiles para entrenamiento futuro.

Objetivos secundarios vigentes:
1. Validar cadena end-to-end IoT: nodo LoRa (Buenos Aires) → satélite (RX-only) → estación terrena (UHF 435 MHz) → backend.
2. Store and forward por pasadas LEO.
3. Science Pack (UV, ALS, magnetómetro, temperatura).
4. `PHOTO_DEMO` opcional, no crítico, best-effort.

- CONOPS: **store and forward** por pasadas LEO.
- Política RF MVP: **no transmitir ISM desde órbita** (LoRa en satélite es RX-only).

## Baseline y mapa del repositorio

| Documento | Rol |
|---|---|
| `00_MVP/MVP v2.2.md` | Fuente de verdad del baseline (documento maestro) |
| `SYSTEM_BASELINE.md` | Resumen rápido del baseline |
| `architecture.md` | Mapa del repo + snapshot arquitectónico |
| `AGENTS.md` | Política documental global (raíz) |
| `01_Mission/mission_definition.md` | Definición de misión y CONOPS |
| `01_Mission/requirements_matrix.md` | Requisitos verificables |
| `01_Mission/compliance_matrix.md` | Compliance matrix viva |
| `01_Mission/validation_plan_and_stage_gates.md` | Plan de validación y stage-gates |
| `08_Decisions/` | ADRs (Architecture Decision Records) |

## Decisiones bloqueadas (resumen)

- **Plataforma:** 1.5U (100 × 100 × 150 mm).
- **EPS vuelo:** topología de batería **2S + MPPT**, referencia **2S1P con 18650 de 3.0 Ah (~22 Wh nominal)**. Ruta de mitigación `2S2P (~44 Wh)` abierta si el power budget con IA lo exige tras Gate IA-1.
- **Solar:** el target **≥1.2 W netos en sol** sigue vigente para el escenario **sin payload IA activo**. Con payload IA activo, el target solar queda **TBD** hasta medición real del CM5 y cierre del duty-cycle orbital.
- **COMMS:**
  - uplink usuario **LoRa 915 RX-only** en órbita,
  - downlink/TTC **UHF 435 MHz FSK 1200 bps**,
  - objetivo inicial UHF TX RF: **500 mW** (preliminar).
- **Modelo operativo:**
  - `MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW`
  - `EPS_STATE = CRIT | LOW | NOMINAL | HIGH`
  - boot siempre en **SAFE**,
  - si `EPS_STATE = CRIT` → degrada a `MISSION_MODE = SAFE`,
  - `LOW` mantiene `SAFE` por defecto; `NOMINAL` solo para housekeeping esencial,
  - ciencia como actividad dentro de `NOMINAL` (no modo independiente),
  - payload IA solo en `MISSION_MODE = NOMINAL`, fase de sol y `EPS_STATE >= NOMINAL`.
- **Operación/FSW:** arbitraje de downlink por colas con prioridad estricta `HOUSEKEEPING` + `COMMAND_ACK`, y con `AI_BEHAVIOR_LOG` como cola best-effort de mayor prioridad científica.
- **Science MVP:** sin Geiger/HV.
- **PHOTO_DEMO:** opcional, no crítico, off-by-default, best-effort, fuera del criterio mínimo MVP.
- **Payload IA:** payload científico primario de misión (familia CM5, IBM Granite 350M como candidato de vuelo / flight candidate, Apache 2.0, supervisor determinístico); Granite 3.1 2B queda reservado para experimentación de banco y ground experimentation. OBC conserva autoridad de vuelo; fallo del payload no mata el bus, pero sí impacta el éxito primario. No declarado flight-ready.

Fuente de decisiones: `08_Decisions/` (ADRs).

## Separación EPS: bench / flight-like / flight

| Capa | Nombre | Propósito |
|---|---|---|
| Bench | `EPS_Bench1_1S` | Validación funcional COTS, 1S. No es hardware de vuelo. |
| Flight-Like | `EPS_Flight_Like_2S_MPPT` | PCB custom KiCad, 2S + MPPT. No calificado. |
| Flight | `EPS_Flight_2S_MPPT` | Hardware de vuelo definitivo. TBD. |

## Nodo típico LoRa (clase, no SKU)

Radio clase SX1262/SX1276, MCU clase ESP32-S3, +20–21 dBm, antena 0–2 dBi, sin PA/LNA externo, sin TCXO. Banda: 915–928 MHz. Ejemplos de clase: Heltec, RFM95W y similares.

## Estado TTC UHF (OpenLST)

Baseline operativo vigente: **UHF 435 MHz FSK 1200 bps**.
OpenLST: candidato en análisis, no baseline final. Hardware TTC UHF final: **TBD**.

## Estado actual (2026-03-16)

- El proyecto incluye un payload IA experimental con **IBM Granite 350M como candidato de vuelo / flight candidate** y línea compacta de banco (sesión 2026-03-16). Licencia Apache 2.0. No declarado flight-ready.
- Granite 3.1 2B queda como modelo de experimentación de banco, comparativas y ground experimentation; no es candidato primario de vuelo bajo el presupuesto actual.
- Benchmark corrected: pass_rate BASE 14 % → FINE_TUNED 57 %; avg_score_ratio 0.32 → 0.83. Holdout funcional completado.
- SmolLM2-360M-Instruct INT4 pasa a baseline histórico/superseded para la función de modelo IA.
- **22 ADRs `Accepted`** en total (incluye ADR-20260316-ai-payload-granite350m-baseline-funcional-banco y ADR-20260615-ai-model-roles-granite350m-flight-candidate-2b-experimentation).
- Misión redefinida como **AUSTRALIS-1 — Experimental Autonomic Flight AI-Assisted CubeSat** (desde 2026-03-14).
- Payload IA es el objetivo científico primario; IoT store-and-forward es objetivo secundario.
- `EPS_STATE` en cuatro niveles: `CRIT | LOW | NOMINAL | HIGH`.
- `AI_BEHAVIOR_LOG` es la mayor prioridad best-effort del Downlink Manager.

## Documentos clave por subsistema

**Mission:**
- `01_Mission/mission_definition.md`
- `01_Mission/requirements_matrix.md`
- `01_Mission/compliance_matrix.md`
- `01_Mission/validation_plan_and_stage_gates.md`

**Structure:** `02_Structure/Block Diagram.md`

**Power/EPS:**
- `03_Power/Power Budget.md`
- `03_Power/EPS Sizing.md`
- `03_Power/EPS_Bench1_1S.md` (bench)
- `03_Power/EPS_PCB/EPS_Bench2S_FlightLike/` (flight-like KiCad)
- `03_Power/EPS_DESIGN_RULES.md` (draft, no normativo)

**Communications:**
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/link_budget_uhf_preliminary.md`
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/uplink_data_products_and_downlink_policy.md`
- `04_Communications/RF_ANALISYS_OPENLST.md` (análisis/candidato, no baseline final)

**Software:**
- `05_Software/software_framework_mvp22.md`
- `05_Software/node_uplink_scheduler_pass_prediction.md`
- `05_Software/node_tle_update_mechanism.md`
- `05_Software/ground_data_architecture.md`
- `05_Software/ai_payload_architecture.md`
- `05_Software/GroundTelemetryDashboard/`

**Costos:** `06_Costs/BOM_master.csv`, `06_Costs/bom_overview.md`, `06_Costs/cost_overview.md`

**Riesgos:** `07_Risk/top_risks.md`

**Decisiones:** `08_Decisions/`

## Pendientes de cierre (TBD)

1. Selección de módulo UHF final y eficiencia PA medida.
2. Cierre de factibilidad uplink LoRa con nodos típicos (CFO/Doppler).
3. Parámetros finos uplink LoRa: elevación mínima, canalización exacta, BW definitivo.
4. Cierre del power budget del payload IA con consumo real del CM5 y definición de duty-cycle orbital.
5. Cierre del target solar con payload IA activo; evaluar deployables o celdas más eficientes si hace falta.
6. Confirmar si la batería de referencia `2S1P` alcanza o si debe escalarse a `2S2P` tras Gate IA-1.
7. Completar BOM con valores trazables y cotizaciones.
8. Coordinación IARU y camino regulatorio ENACOM.
9. ICD completo con integrador (inhibición RF, fit-check, masa, etc.).

## Notas de consistencia

- Si hay conflicto documental, prevalece ADR `Accepted` más reciente.
- `Draft`, `Proposed` o `Preliminary` no reemplazan decisiones bloqueadas hasta tener ADR.
- El repo técnico sigue llamándose **DIY Nanosat**; **AUSTRALIS-1** es el nombre vigente de misión/proyecto.
- Ver política completa en `AGENTS.md`.
