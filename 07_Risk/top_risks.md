# Risk Register — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — pre-SRR

## 1. Escala y reglas

Probabilidad:

- `1` improbable;
- `2` baja;
- `3` media;
- `4` alta;
- `5` casi cierta.

Impacto:

- `1` menor;
- `2` bajo;
- `3` medio;
- `4` alto;
- `5` crítico para seguridad/misión/legalidad.

`Score=P×I`: 1–5 bajo, 6–10 medio, 11–15 alto, 16–25 crítico.

Un riesgo solo puede cerrarse con `EvidenceID`, review y riesgo residual
aceptado. Todos los owners son **roles** hasta asignación nominal en la review.
No hay riesgos cerrados en esta revisión. Los scores de la tabla son
exposición inicial; la exposición residual y la fecha calendario permanecen
`TBD`. La columna `Due gate` es el hito máximo y en SRR se asignarán nombre y
fecha sin inventarlos en esta revisión.

## 2. Registro consolidado

| ID | Causa → evento → impacto | P | I | Score | Owner role | Trigger | Mitigación / evidencia de cierre | Due gate | Estado |
|---|---|---:|---:|---:|---|---|---|---|---|
| RSK-CONF-01 | Fuentes activas incompatibles → configuración equivocada → decisiones/test inválidos | 4 | 5 | 20 | Systems/QA | parámetro/estado con dos valores activos | Gate A, checks automáticos, ADR disposition, VCRM 1:1 | Gate A | Open |
| RSK-MECH-01 | Geometría 150 mm propagada/CAD o masa ausentes → no conformidad/fit failure | 5 | 5 | 25 | Structure | modelo activo usa 150 mm, supera referencia CDS 3.00 kg/límite ICD o no existe fit CAD | regenerar CAD/budgets con CDS 170.2 mm; mass roll-up, metrología/fit-check | PDR/FRR | Open |
| RSK-LAUNCH-01 | Inhibits/RBF/deployment incompletos → activación en launcher | 4 | 5 | 20 | EPS/Structure/COMMS | diseño sin switch/RBF/3 RF/3 deployable inhibits | diseño CDS+ICD, fault injection, timers y integrator acceptance | CDR/FRR | Open |
| RSK-EPS-01 | Esquema EPS placeholder con cortos/sin BMS/charger → daño o batería insegura | 5 | 5 | 25 | EPS/QA | fabricación o sourcing antes de design review/ERC | bloquear fabricación; reconstruir esquema, ERC/BOM/DRC/tests | Gate D | Open |
| RSK-EPS-02 | Celda/BMS/temperatura no definidos → plating, runaway o pérdida de energía | 4 | 5 | 20 | EPS/Safety | carga fuera de datasheet o sin sensor/interlock | celda/lote, full BMS, charge inhibit, TVAC/fault tests | CDR/QAR | Open |
| RSK-EPS-03 | State machine sin thresholds/histéresis → chatter/mode unsafe | 4 | 4 | 16 | EPS/FSW | transición no determinista en límites/sensor inválido | spec completa y boundary/noise/fault tests | CDR/TRR | Open |
| RSK-ORB-01 | Barrido no heliosincrónico y artefactos incoherentes → órbita/budgets erróneos | 5 | 4 | 20 | Mission/Analysis | drift LTAN o resultado no reproducible | derivar SSO, manifest, validación Orekit/GMAT equivalente | PDR | Open |
| RSK-ADCS-01 | Actitud perfecta asumida sin ADCS → energía/térmica/RF no alcanzables | 5 | 5 | 25 | ADCS/Systems | budget depende de LVLH perfecto | CONOPS, detumble, hardware, HIL/Monte Carlo y degraded cases | Gate G/TRR | Open |
| RSK-THR-01 | Modelo viola balance físico/geometría → temperaturas/radiador falsos | 5 | 5 | 25 | Thermal | energy residual/test de regresión falla | modelo conservativo, CAD/BOM provenance y correlation | CDR/QAR | Open |
| RSK-THR-02 | Conductancia/interfaces no caracterizadas → sobretemperatura IA | 4 | 4 | 16 | Thermal/Structure | ΔT/G medidos fuera de allocation | stack térmico real + calorimetría/TVAC | QAR | Open |
| RSK-RAD-01 | COTS sin TID/SEE/SEL → corrupción, latch-up o falla destructiva | 4 | 5 | 20 | Radiation/Systems | ausencia de environment/parts analysis | shielding/derating/current limit/EDAC/test/heritage | PDR/CDR | Open |
| RSK-ENV-01 | Sin qualification/acceptance ambiental → falla en lanzamiento/órbita | 4 | 5 | 20 | AIT/QA | FRR sin vibration/TVAC/EMC/deployment | programa ICD, pre/post y QAR | QAR/FRR | Open |
| RSK-MAT-01 | Materiales/venting no conformes → contaminación/daño/rechazo | 3 | 5 | 15 | Materials/Structure | material sin declaration o volumen sellado | material declaration, vent analysis, datasheet/lot test | CDR/FRR | Open |
| RSK-AI-01 | Candidato/dataset/benchmark no reproducibles → hipótesis científica inválida | 5 | 5 | 25 | AI/Science | digest/split/oráculo/threshold ausente | preregistration, clean blind split, external oracle, statistics | IA-1/SRR | Open |
| RSK-AI-02 | IA/CM5 excede energía/térmica o no recupera → bus degradado | 4 | 4 | 16 | AI/EPS/FSW | boot/power/temp/kill fuera de allocation | medición exacta, power-gate, watchdog, lockout y fallback | IA-2 | Open |
| RSK-AI-03 | Supervisor acepta tool inválida/unsafe → acción peligrosa | 4 | 5 | 20 | FSW/Safety | malformed/no-action/unsafe obtiene pass | strict schema, OBC-owned class, state simulator, negative tests | IA-2/TRR | Open |
| RSK-FSW-01 | Reset/state machine no idempotente → modo/carga insegura | 3 | 5 | 15 | FSW/EPS | reset/brownout no vuelve SAFE | watchdog, transactional state, boot/boundary fault tests | TRR | Open |
| RSK-FSW-02 | Health/session counters ambiguos → diagnóstico incorrecto | 3 | 3 | 9 | FSW | reboot/wrap no distinguible | session/boot IDs, monotonic counters, schema/tests | TRR | Open |
| RSK-DATA-01 | Ground solo RAM/sin raw replay → evidencia científica perdida | 5 | 5 | 25 | Ground SW | restart/power loss pierde sesión | append-only raw, metadata, digests, replay/export | Gate E/TRR | Open |
| RSK-DATA-02 | Colas/data budget sin cuotas → starvation de logs científicos | 4 | 4 | 16 | FSW/COMMS | backlog/age supera retention | production/contact budget, quotas, aging, worst-case test | PDR/TRR | Open |
| RSK-DATA-03 | PER por gaps confunde boot/wrap/reorder → claim RF falso | 4 | 3 | 12 | Ground SW | fixtures producen pérdidas artificiales | modular/session-aware statistics + unit tests | TRR | Open |
| RSK-REG-01 | 915 MHz Tierra→espacio no autorizable → objetivo secundario ilegal | 4 | 5 | 20 | Regulatory/COMMS | no hay respuesta ENACOM escrita | consulta formal; migrar banda/servicio o redefinir objetivo | SRR/Gate B | Open |
| RSK-REG-02 | UHF/IARU/ITU/ENACOM incompletos → no operar/aceptar misión | 4 | 5 | 20 | Operations/Regulatory | bandplan congelado sin dossier | responsable habilitado, coordination/filing/licensing | PDR/FRR | Open |
| RSK-SEC-01 | TTC/prompts sin auth/replay → spoofing/DoS/ciencia corrupta | 5 | 5 | 25 | Security/FSW | CRC/hash simple o contador no persistente | MAC/signature TBD, counter/key epoch/roles/recovery tests | CDR/TRR | Open |
| RSK-SEC-02 | Threat model/key lifecycle incompletos → mitigación ineficaz | 4 | 4 | 16 | Security | key compromise/reset/recovery no cubierto | threat model review, provisioning/rotation/revocation | CDR | Open |
| RSK-COMMS-01 | Link LoRa sin margen robusto → cero paquetes orbitales | 4 | 4 | 16 | COMMS | calibrated worst-case margin/PDR bajo threshold | link budget + OTA/PDR + fallback mission | Gate B | Open |
| RSK-COMMS-02 | CFO/Doppler/ToA/slots mal modelados → colisiones/demod failure | 4 | 4 | 16 | COMMS/Node | ramp/collision test bajo threshold | correct ToA, Doppler ramp, Monte Carlo, measured clocks | Gate B | Open |
| RSK-COMMS-03 | TLE/time source falso/viejo → ventanas erróneas | 3 | 4 | 12 | Node FW/Ground | age/error excede budget o rollback aceptado | signed source, object ID, expiry, error-based fallback | Gate B | Open |
| RSK-RF-01 | UHF link/pattern/waveform no cierra → pérdida TTC | 4 | 5 | 20 | COMMS | measured PER/EIRP/G/T no cumple | bidirectional budgets, integrated pattern/Doppler/OTA | Gate C | Open |
| RSK-RF-02 | EMI/desense entre EPS/CM5/UHF/LoRa → enlaces degradados | 4 | 4 | 16 | COMMS/EMC | noise floor/PER cambia por modo | mode matrix, isolation/filtering/blocker/EMC tests | Gate C/QAR | Open |
| RSK-GND-01 | SatNOGS accede a TX/control → emisión accidental | 3 | 5 | 15 | Ground/COMMS | proceso RX puede abrir PTT/IPC/credentials | physical TX gate, privilege isolation, failure tests | Gate C/TRR | Open |
| RSK-GND-02 | Viento/clima/torre sin control → daño/indisponibilidad | 3 | 5 | 15 | Ground/Structure | hazard threshold sin park/inhibit | structural/weather analysis, calibrated sensors, E-stop | TRR | Open |
| RSK-COST-01 | BOM/LCC sin totales/fuentes → proyecto inviable tardíamente | 4 | 4 | 16 | Cost/PM | review sin low/likely/high y reserves | WBS/LCC, BOE, FX/date, NRE, launch/tests/spares | PDR/CDR | Open |
| RSK-SUP-01 | EOL/import-only/single source → rediseño/schedule slip | 4 | 3 | 12 | Procurement | no alternativa/lead/lifecycle | regional alternatives, quotes, lifecycle and spares | PDR/CDR | Open |
| RSK-LEGAL-01 | Titularidad/licencias/provenance ambiguas → distribución o licencia no autorizada | 4 | 5 | 20 | Legal/Configuration | release sin chain of title, textos exactos, SPDX/manifest o contacto autorizado | revisión profesional, manifest de provenance/licencias y sign-off de release | Before release | Open |
| RSK-PROG-01 | Owner/authority/schedule indefinidos → acciones nunca cierran | 4 | 4 | 16 | PM/QA | review sin responsable nominal/due date | assign names at SRR, action register and reserves | SRR/each review | Open |
| RSK-PH-01 | PHOTO_DEMO deriva a EO/legal/privacy scope → compliance/schedule impact | 2 | 4 | 8 | Payload/Legal | targeting, products, tasking or commercialization | keep optional/off; capability review with specialist/authority | PDR if included | Open |

## 3. Disposiciones específicas

### IA

La evidencia histórica atribuida a Granite 350M queda invalidada para cierre.
No existe mitigación parcial demostrada del riesgo `RSK-AI-01/03`. El candidato
actual es `gemma4:e2b` y empieza en estado de evidencia `Open`.

### Órbita, energía y térmica

`RSK-ORB-01` se reabre. No se usa el barrido anual histórico para cerrar
variación estacional, margen energético, radiador o heater.

### Hardware

Fabricación EPS queda bloqueada. Los proyectos EPS/RF actuales son placeholders;
no constituyen evidencia de implementación.

### Riesgo legal PHOTO_DEMO

Las cifras heurísticas de GSD/cadencia en el análisis histórico no son umbrales
legales. Cualquier inclusión requiere revisión profesional y con las autoridades
o partners aplicables.

## 4. Revisión

En cada review se actualizarán:

- P/I inicial y residual con base documentada;
- owner nominal y due date;
- trigger y leading indicator;
- acciones, ProcedureID/EvidenceID;
- riesgo aceptado/waiver y autoridad.
