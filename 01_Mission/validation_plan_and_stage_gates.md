# Verification, Validation and Review Plan — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — pre-SRR
**Trazabilidad:** ADR-20260727-verification-and-review-governance

## 1. Política

Secuencia obligatoria:

```text
Gate A → SRR → subsystem evidence gates → PDR → CDR → TRR
       → Qualification/Acceptance Review (QAR) → FRR
```

- Solo un resultado `Verified` en VCRM cierra un requisito.
- “Preliminary”, “bench funcionando” o “documentado” no sustituyen evidencia.
- Una dependencia no puede reemplazarse por una “versión funcional”.
- Waiver exige autoridad, justificación, expiración/condición y RiskID residual.
- `Blocked by Integrator` impide FRR si afecta seguridad/aceptación.
- Todo test usa procedimiento aprobado, artículo/configuración identificados,
  instrumentación calibrada, raw data y digest.

## 2. Artefactos de control

- requisitos: `requirements_matrix.md`;
- VCRM: `verification_cross_reference_matrix.csv`;
- procedimientos: `verification_procedure_index.md`;
- compliance: `compliance_matrix.md`;
- risk register: `../07_Risk/top_risks.md`;
- BOM/configuración: `../06_Costs/BOM_master.csv`.

## 3. Gate A — Configuration Reconciliation

**Estado:** `Open`.

### Entrada

- rama/revisión identificada;
- auditoría integral disponible;
- autoridad de baseline definida.

### Salida

1. cero ADRs `Accepted` incompatibles;
2. todos los documentos activos usan 1.5U CDS y no 150 mm;
3. `gemma4:e2b` es el único candidato IA activo, sin claim de validación;
4. Granite/SmolLM/órbita/radiador/margen históricos dispuestos;
5. Gate A/SRR/PDR/readiness consistentes;
6. 100% de ReqIDs presentes una sola vez en VCRM;
7. estados/document links validados automáticamente;
8. cada conflicto `CONF-*` está resuelto o ligado a RiskID/acción;
9. revisión independiente del diff y acta de cierre.

**Owner role:** Systems/Configuration/QA.
**Authority nominal:** TBD.
**EvidenceID:** TBD.

## 4. SRR — System Requirements Review

**Estado:** `Open`; depende de Gate A `Verified`.

### Salida

- misión, alcance y CONOPS aprobados;
- protocolo científico preregistrado;
- requisitos atómicos con criterios y VCRM completa;
- normativa/ICD/regulatory applicability identificada;
- interfaces y budgets con reglas de margen;
- risk register con owner nominal, triggers y residual;
- plan COTS-to-flight, radiación, ambiente y artículos de ensayo;
- schedule/cost baseline ROM con reservas;
- ningún TBD crítico sin plan/gate de cierre.

## 5. Gates de evidencia de subsistema

Estos gates producen evidencia para PDR/CDR/TRR; no sustituyen las reviews.

### Gate IA-1 — Candidate model evidence

**Estado:** `Open`.

Salida:

- manifest/digest exacto de `gemma4:e2b`, tokenizer, runtime y licencia;
- dataset con provenance, deduplicación y blind split;
- suite con oráculo externo, schemas estrictos y casos adversariales;
- análisis estadístico preregistrado;
- cero transferencia de métricas Granite;
- resultados raw y reproducibles.

### Gate IA-2 — Hardware/supervisor integration

**Estado:** `Open`; depende de IA-1.

Salida:

- hardware/configuración exacta;
- boot/power-cycle/kill/lockout;
- supervisor valida schema, args, clases, pre/postconditions;
- tests negativos: no-action, malformed, prosa envolvente, rango, zero values,
  acción insegura y replay;
- latencia, memoria, energía y térmica medidos;
- OBC opera normalmente con IA apagada;
- storage/prompt shutdown seguro.

### Gate B — LoRa non-radiated feasibility

**Estado:** `Open`.

Salida:

- autorización/ruta regulatoria documentada antes de cualquier ensayo radiado;
- ToA y slot capacity corregidos;
- sensibilidad/PDR/CFO/Doppler ramp calibrados;
- clock/TLE error budget, near-far, adjacent/cochannel y coexistencia;
- patrón OTA integrado y criterios con N/IC;
- persistencia/replay de ground data.

### Gate C — UHF TTC candidate

**Estado:** `Open`.

Salida:

- link budgets uplink/downlink corregidos;
- waveform/occupied bandwidth/Doppler/FEC/framing definidos;
- EIRP, sensibilidad, G/T, PER y patrón integrado medidos;
- coexistencia/EMC y spurious emissions;
- beacon público decodificado;
- autenticación/anti-replay integrada;
- dossier ENACOM/IARU/ITU avanzado;
- T/R isolation y SatNOGS RX-only verificados.

### Gate D — EPS flight-like design/release

**Estado:** `Blocked` hasta reconstrucción del diseño.

Salida previa a fabricación:

- esquema funcional sin cortos/placeholders;
- celda, BMS completo, cargador/MPPT, balanceo y secondary protection;
- power paths/gating/telemetry/charge inhibit/launch inhibits;
- ERC/BOM/design review aprobados.

Salida posterior:

- PCB con stackup/DRC/fabrication package;
- pruebas rails, inrush, short/OCP/backfeed/brownout;
- state machine completa;
- budgets medidos por modo;
- dossier batería.

### Gate G — Structure/ADCS/thermal preliminary closure

**Estado:** `Open`.

Salida:

- CAD CDS 1.5U, stack, harness, antenna stowage, mass/CG/inertia;
- CONOPS ADCS, detumble, pointing/jitter y safe attitude;
- simulación SSO validada e incertidumbre;
- budgets solar/térmico/RF con dispersión de actitud;
- thermal model conservativo y test plan correlativo;
- FEA/load path/modes preliminares.

## 6. PDR — Preliminary Design Review

**Estado:** `Open`; depende de SRR y evidencia preliminar IA/B/C/D/G.

Salida:

- arquitectura de cada subsistema y ICD draft;
- trade studies reproducibles;
- budgets masa/potencia/energía/datos/térmico/RF con margen e incertidumbre;
- CAD/layout preliminar conforme CDS;
- FMEA inicial y top risks;
- selección de artículos/prototipos;
- regulatory plan y launch-provider assumptions;
- verificación planificada para 100% de requisitos.

No requiere hardware final, pero no admite un “design source” placeholder
presentado como arquitectura preliminar cerrada.

## 7. CDR — Critical Design Review

**Estado:** `Open`; depende de PDR.

Salida:

- diseño fabricable y configuración congelada;
- esquemas/ERC, PCB/DRC, CAD/drawings, harness e ICD;
- BOM/procurement y derating completos;
- FMEA/FMECA, radiation analysis y fault containment;
- budgets cerrados contra configuración;
- procedimientos TRR/QAR aprobables;
- software/model/runtime manifests;
- todas las acciones PDR críticas cerradas o waived formalmente.

## 8. Gate E — FlatSat integrated

**Estado:** `Open`; depende de IA-2, B, C, D y G completos.

Salida:

- boot SAFE y recuperación;
- EPS/OBC/COMMS/ADCS/payload/ground integrados;
- auth/replay y command roles;
- colas/data budget/persistencia/replay;
- fault injection, power cycling y degraded modes;
- RF por cable/dummy load antes de irradiar;
- configuración del FlatSat registrada.

## 9. TRR — Test Readiness Review

**Estado:** `Open`; depende de CDR y Gate E.

Salida:

- procedimientos aprobados y trazados;
- artículos/seriales/configuración definidos;
- fixtures e instrumentación/calibración;
- criterios pass/fail y abort;
- data acquisition/backup/digests;
- hazard controls y permisos RF;
- NCR/waiver process activo.

## 10. QAR — Qualification/Acceptance Review

**Estado:** `Open`; depende de TRR.

Campaña mínima, adaptada al ICD:

- funcional eléctrico/RF pre/post;
- random vibration y cargas/sine aplicables;
- shock si aplica;
- thermal cycling y TVAC/thermal balance;
- EMC/coexistencia;
- deployment después de ambiente;
- end-to-end RF/ground;
- correlación de modelos;
- acceptance del artículo de vuelo.

“Si disponible” no es un criterio válido para thermal-vac o evidencia ambiental
requerida.

## 11. FRR — Flight Readiness Review

**Estado:** `Open`; depende de QAR e ICD final.

Salida:

- requisitos de seguridad/mission success `Verified`;
- compliance matrix sin bloqueantes;
- IARU/ITU/ENACOM e integrador aprobados;
- fit-check y mass properties;
- battery/launch safety dossier;
- CONOPS, procedures, staffing y ground segment listos;
- anomalies/waivers aceptados con riesgo residual;
- as-built/as-flown configuration y evidence pack congelados.

No se declara readiness con ítems críticos `Open`, `Planned`,
`Implemented` o `Blocked by Integrator`.

## 12. Cobertura de requisitos

La VCRM contiene una fila por cada ID. Esta enumeración permite auditar que el
plan referencia el universo completo:

- misión/sistema:
  `MIS-REQ-01`, `MIS-REQ-02`, `MIS-REQ-03`, `MIS-REQ-04`, `MIS-REQ-05`,
  `MIS-REQ-06`, `MIS-REQ-07`, `MIS-REQ-08`, `MIS-REQ-09`, `MIS-REQ-10`,
  `MIS-REQ-11`, `MIS-REQ-12`, `MIS-REQ-13`, `MIS-REQ-14`, `MIS-REQ-15`,
  `MIS-REQ-16`, `MIS-REQ-17`, `MIS-REQ-18`, `MIS-REQ-19`, `MIS-REQ-20`,
  `MIS-REQ-21`, `MIS-REQ-22`, `MIS-REQ-23`, `MIS-REQ-24`;
- uplink:
  `COMMS-UL-01`, `COMMS-UL-02`, `COMMS-UL-03`, `COMMS-UL-04`,
  `COMMS-UL-05`, `COMMS-UL-06`;
- compliance:
  `COMP-REQ-01`, `COMP-REQ-02`, `COMP-REQ-03`, `COMP-REQ-04`,
  `COMP-REQ-05`, `COMP-REQ-06`;
- PHOTO_DEMO:
  `MIS-REQ-PH-01`, `MIS-REQ-PH-02`, `MIS-REQ-PH-03`, `MIS-REQ-PH-04`;
- IA:
  `IA-REQ-01`, `IA-REQ-02`, `IA-REQ-03`, `IA-REQ-04`, `IA-REQ-05`,
  `IA-REQ-06`, `IA-REQ-07`, `IA-REQ-08`, `IA-REQ-09`, `IA-REQ-10`,
  `IA-REQ-11`;
- estructura/térmico:
  `STR-REQ-01`, `STR-REQ-02`, `THR-REQ-01`, `THR-REQ-02`, `THR-REQ-03`,
  `THR-REQ-04`;
- assurance:
  `SYS-REQ-01`, `SYS-REQ-02`, `SYS-REQ-03`, `SYS-REQ-04`, `SYS-REQ-05`,
  `SYS-REQ-06`, `SYS-REQ-07`, `EPS-REQ-01`, `EPS-REQ-02`,
  `ADCS-REQ-01`, `ADCS-REQ-02`, `DATA-REQ-01`, `DATA-REQ-02`,
  `SEC-REQ-01`, `SEC-REQ-02`, `RAD-REQ-01`, `ENV-REQ-01`.

## 13. Resumen de estado

| Review/Gate | Estado |
|---|---|
| Gate A | Open |
| SRR | Open |
| IA-1 | Open |
| IA-2 | Open |
| B | Open |
| C | Open |
| D | Blocked — design source no fabricable |
| G | Open |
| PDR | Open |
| CDR | Open |
| E | Open |
| TRR | Open |
| QAR | Open |
| FRR | Open |
