# Architecture Map — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Baseline map — pre-SRR

## 1. Precedencia y control de configuración

1. ADR `Accepted` más reciente.
2. `00_MVP/MVP v2.2.md`.
3. `SYSTEM_BASELINE.md`.
4. requisitos/VCRM/compliance.
5. documentación de subsistema.
6. análisis `Draft/Proposed/Preliminary`.
7. histórico/superseded.

Una decisión solo puede ser `Accepted` en una ADR. Una verificación solo puede
ser `Verified` en VCRM con procedimiento, configuración y evidencia.

## 2. Partición de sistema

```text
Ground segment
  ├─ recepción pública (SatNOGS, RX-only)
  ├─ estación AUSTRALIS autorizada (TTC autenticado)
  └─ repositorio de evidencia (raw + metadata + replay + export)
          ⇅ RF coordinada
Space segment — CubeSat 1.5U
  ├─ launch safety / inhibits / RBF / deployment
  ├─ EPS 2S reference + power/fault manager
  ├─ OBC determinístico (única autoridad)
  │    ├─ Runtime Safety Supervisor
  │    ├─ state machine / command / queues
  │    └─ critical log
  ├─ payload IA power-gated (`gemma4:e2b` candidate)
  ├─ COMMS UHF TTC + LoRa RX candidate
  ├─ ADCS TBD
  ├─ Science Pack
  └─ estructura / térmico / almacenamiento
```

## 3. Estado por subsistema

| Dominio | Decidido | Abierto/bloqueante |
|---|---|---|
| Mission | IA asesora; OBC determinístico; objetivos secundarios | protocolo experimental y métricas |
| Structure | clase 1.5U; Z CDS 170.2 ±0.1 mm | CAD, stack, mass properties, FEA, fit-check |
| EPS | referencia 2S + MPPT; separación de stages | esquema/PCB, celda/BMS/cargador, budgets |
| COMMS | LoRa orbital RX-only; SatNOGS RX-only; seguridad TTC requerida | regulación, bandas, hardware, waveform, links |
| OBC/FSW | estados canónicos, SAFE boot, supervisor | implementación y pruebas integradas |
| AI payload | `gemma4:e2b` candidato; power-gated | digest/licencia/dataset/benchmark/potencia/térmica |
| ADCS | ninguno | CONOPS, sensores/actuadores, control, presupuesto |
| Thermal | requisitos se derivarán de componentes | modelo físico/correlación/TVAC |
| Ground | dashboard compila; arquitectura objetivo | persistencia, autenticación, tests, E2E |
| Regulatory | ruta ENACOM/IARU/ITU obligatoria | autorizaciones/coordination/notificación |

## 4. Interfaces de seguridad

- El modelo nunca controla hardware directamente.
- El OBC valida estructura, tipos, rangos, precondiciones, autorización y
  postcondiciones.
- `EPS_STATE=CRIT` fuerza `MISSION_MODE=SAFE`.
- Comandos/prompts usan autenticación y anti-replay; CRC no autentica.
- SatNOGS no tiene PTT, credenciales ni IPC hacia el transmisor.
- Launch inhibits, deployment switch, RBF y timers se diseñan contra CDS/ICD;
  no se difieren por completo al integrador.
- Una carga no crítica no puede comprometer rail, boot o storage crítico.

## 5. Fuentes activas

| Artefacto | Rol |
|---|---|
| `00_MVP/MVP v2.2.md` | baseline maestro |
| `SYSTEM_BASELINE.md` | resumen de estado |
| `01_Mission/requirements_matrix.md` | requisitos |
| `01_Mission/verification_cross_reference_matrix.csv` | trazabilidad V&V |
| `01_Mission/compliance_matrix.md` | normas/ICD/regulación |
| `01_Mission/validation_plan_and_stage_gates.md` | reviews/gates |
| `06_Costs/BOM_master.csv` | configuración/procurement |
| `07_Risk/top_risks.md` | risk register |
| `08_Decisions/` | decisiones |

## 6. ADR correctivas vigentes

| ADR | Decisión |
|---|---|
| ADR-20260727-cubesat-1p5u-cds-envelope | corrige geometría 1.5U |
| ADR-20260727-ai-payload-gemma4-e2b-candidate | candidato IA y límites de claim |
| ADR-20260727-orbit-attitude-analysis-reopened | reabre órbita/actitud/layout |
| ADR-20260727-thermal-power-baselines-reopened | reabre energía/térmica |
| ADR-20260727-rf-regulatory-command-security-baseline | RF/regulación/seguridad TTC |
| ADR-20260727-verification-and-review-governance | VCRM y reviews formales |

Los documentos superseded conservan historia, no autoridad normativa.

## 7. Conflictos de configuración abiertos

| ID | Conflicto | Disposición |
|---|---|---|
| CONF-01 | budgets físicos basados en 150 mm | regenerar con CDS |
| CONF-02 | 600/650 km y LTAN 9:30/10:00 | no hay órbita congelada |
| CONF-03 | Granite 350M claim vs scripts 2B | claim invalidado; Gemma candidate |
| CONF-04 | EPS KiCad citado como implementación | placeholder/no fabricable |
| CONF-05 | BW125/BW250/frecuencias | TBD tras regulación y ensayos |
| CONF-06 | radiador −Y vs CSV +Z | no hay radiador seleccionado |
| CONF-07 | power/thermal Modelica vs HTML | ninguna fuente validada |
| CONF-08 | private/controlled vs autenticación | protocolo criptográfico TBD |

Gate A permanece abierto hasta resolver o disponer formalmente cada conflicto.

## 8. Definition of Done documental

Un cambio de baseline exige:

1. ADR y requisitos afectados;
2. VCRM, riesgos y budgets actualizados;
3. BOM/costos si cambia configuración;
4. fuentes/datos/hipótesis identificados;
5. enlaces y estados consistentes;
6. revisión independiente del diff.
