# Compliance Matrix — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — pre-SRR

Este documento cubre normas, regulación e interfaces externas. La verificación
de requisitos internos se controla en
`verification_cross_reference_matrix.csv`.

Estados permitidos:

- `Open`
- `Planned`
- `Implemented`
- `Verified`
- `Waived`
- `Blocked by Integrator`

`Blocked by Integrator` no equivale a cierre y bloquea FRR si afecta seguridad o
aceptación.

## 1. Mecánica e interfaz 1.5U

| ID | Requirement | Source | Verification/Evidence | Status | Disposición |
|---|---|---|---|---|---|
| CX-M-01 | Envolvente CubeSat 1.5U, incluyendo `Z=170.2 ±0.1 mm`. | CDS Rev.14.1 p.24; COMP-REQ-01 | CAD controlado + metrología | Open | Todo modelo de 150 mm debe regenerarse. |
| CX-M-02 | Masa dentro del límite aplicable. | CDS Rev.14.1 Table 1 (referencia 1.5U 3.00 kg); ICD | mass roll-up + pesada | Blocked by Integrator | 3.00 kg es referencia CDS, no promesa del dispenser. |
| CX-M-03 | CG e inercia dentro de límites. | CDS/ICD | CAD + ensayo de mass properties | Blocked by Integrator | Límites exactos TBD por ICD. |
| CX-M-04 | Rails, tabs, corner radius, finish, protrusions y keep-outs conformes. | CDS drawings; ICD | drawing review + metrología | Blocked by Integrator | Diseñar contra CDS; confirmar detalles con integrador. |
| CX-M-05 | Retención de deployables responsabilidad del CubeSat. | CDS Rev.14.1 §2.3/§2.4 | inspección + deployment tests | Open | Mecanismo de antena TBD. |
| CX-M-06 | Fit-check físico aprobado. | ICD integrador | fit-check record | Blocked by Integrator | Obligatorio antes de FRR. |
| CX-M-07 | Dossier mecánico completo. | ICD integrador | drawings, stack, mass/CG/inertia, fasteners, load path | Open | No existe aún CAD activo conforme. |
| CX-M-08 | Al menos un deployment switch desconecta eléctricamente funciones powered hasta eyección. | CDS Rev.14.1 §2.3.1–2.3.2 | esquema + continuity/fault tests | Open | No limitar su alcance a RF/deployables. |
| CX-M-09 | RBF (Remove Before Flight) o mecanismo requerido por CDS/ICD. | CDS Rev.14.1 §2.3.5 | inspección + procedimiento | Open | No es “si aplica” en el baseline CDS. |
| CX-M-10 | Al menos tres inhibiciones para deployables. | CDS Rev.14.1 §2.3.8 | independencia + fault injection | Open | El repo anterior indicaba dos; queda corregido. |
| CX-M-11 | Deployables esperan al menos 30 min post-eyección o el valor más restrictivo del ICD. | CDS Rev.14.1 §2.4.4; ICD | timer/reset/brownout tests | Blocked by Integrator | Implementar mínimo CDS y confirmar ICD. |
| CX-M-12 | Ningún volumen sellado sin análisis de venting. | CDS/ICD | CAD vent analysis | Open | Incluye batería/enclosures/conectores. |
| CX-M-13 | Materiales cumplen outgassing/compatibilidad aplicable. | ICD; ASTM E595 si se invoca | material declaration + datasheet/lot test | Blocked by Integrator | Límite/fuente exactos deben registrarse. |
| CX-M-14 | Entrega incluye esquemas, harness, drawings y mass properties. | ICD integrador | dossier/configuration index | Open | Contenido final condicionado al ICD. |

## 2. Seguridad eléctrica y lanzamiento

| ID | Requirement | Source | Verification/Evidence | Status | Disposición |
|---|---|---|---|---|---|
| CX-LAUNCH-01 | Todas las funciones powered permanecen OFF durante integración/lanzamiento hasta eyección. | CDS Rev.14.1 §2.3.1 | power-path analysis + fault tests | Open | Incluye IA, RF, deployables y cargas. |
| CX-LAUNCH-02 | Al menos tres inhibiciones independientes de RF TX. | CDS Rev.14.1 §2.3.7 | esquema + independencia + fault injection | Open | El ICD puede exigir más, no menos. |
| CX-LAUNCH-03 | No transmitir antes de 45 min post-eyección o valor más restrictivo. | CDS Rev.14.1 §2.4.5; ICD | timer/reset/power-cycle tests | Blocked by Integrator | Mantener contador seguro ante reset. |
| CX-LAUNCH-04 | El sistema protege contra desbalance de celdas. | CDS Rev.14.1 §2.3.6 | BMS design + imbalance tests | Open | KiCad actual no implementa BMS funcional. |
| CX-LAUNCH-05 | Dossier batería aborda transporte, carga, protección y pasivación. | CDS/ICD/transport regulation TBD | dossier + qualification evidence | Blocked by Integrator | Celda y arquitectura completa TBD. |

## 3. RF y regulación

| ID | Requirement | Source | Verification/Evidence | Status | Disposición |
|---|---|---|---|---|---|
| CX-RF-01 | El satélite no transmite LoRa/ISM 915 MHz. | MIS-REQ-02/COMP-REQ-03 | schematic/FW inspection + spectrum test | Planned | RX-only orbital permanece decidido. |
| CX-RF-02 | Frecuencia UHF exacta dentro de atribución y coordinación aplicables. | ENACOM/IARU/ITU | dossier + measured occupied bandwidth | Open | `435.000 MHz` no es centro congelado. |
| CX-RF-03 | Emisiones, occupied bandwidth y espurias cumplen autorización. | ENACOM/ITU | calibrated spectrum report | Open | Hardware/waveform TBD. |
| CX-RF-04 | Coordinación IARU documentada. | IARU Amateur Satellite Frequency Coordination | correspondence/dossier | Open | Necesaria antes de congelar bandplan. |
| CX-RF-05 | Estación espacial y operador cumplen trámite ENACOM/UIT. | Resolución ENACOM 3635-E/2017 §9.14 | licencia, autorización, filing/notification | Open | Responsable legal nominal TBD. |
| CX-RF-06 | Toda emisión incluye identificación/callsign con periodicidad aplicable. | ENACOM 3635-E/2017 §§1.5.8, 13.3.9 | frame/air capture + procedure | Open | Aplicar a todos los perfiles, no solo beacon. |
| CX-RF-07 | Contenido/modulación/decodificación cumplen reglas amateur aplicables. | ENACOM 3635-E/2017 §§1.5.9, 13.4.2 | protocol/legal review | Open | Autenticación no debe convertirse en cifrado de contenido sin aprobación. |
| CX-RF-08 | Uplink 915 MHz Tierra→espacio tiene autorización escrita antes de radiarse. | CABFRA/ENACOM; ADR-20260727 RF | respuesta administrativa que describe banda, dirección, potencia, antena y duty | Open | RX-only orbital no autoriza al transmisor terrestre. |
| CX-RF-09 | Comandos/prompts tienen autenticación, integridad y anti-replay. | SEC-REQ-01 | threat model + negative test suite | Open | CRC/hash simple no autentica. |
| CX-RF-10 | SatNOGS permanece receive-only y sin PTT/claves. | MIS-REQ-21 | physical/logical isolation tests | Planned | No sustituye licencia ni estación de control. |
| CX-RF-11 | Link budgets uplink/downlink y patrón integrado están verificados. | MIS-REQ-03 | measured EIRP/G/T/sensitivity/PER + uncertainty | Open | ADRs de link/máscara anteriores superseded. |

## 4. EPS, térmico, radiación y ambiente

| ID | Requirement | Source | Verification/Evidence | Status | Disposición |
|---|---|---|---|---|---|
| CX-EPS-01 | Arquitectura de referencia 2S; protección/carga completas. | MIS-REQ-06/COMP-REQ-06 | reviewed schematic + battery tests | Open | No fabricar el diseño placeholder. |
| CX-EPS-02 | Límites de carga/descarga/supervivencia de celda final implementados. | THR-REQ-03 | datasheet allocation + TVAC/fault tests | Open | Incluir no-charge cold/hot interlock. |
| CX-EPS-03 | Power/energy budget BOL/EOL cerrado. | ADR-20260727 thermal/power | ledger + measurements + uncertainty | Open | No existe margen confirmado. |
| CX-THR-01 | Thermal model correlacionado y límites verificados. | THR-REQ-01..04 | thermal balance/TVAC + model correlation | Open | Radiador/heater/coating TBD. |
| CX-RAD-01 | TID/DDD/SEE/SEL analizados y mitigados. | RAD-REQ-01 | environment/parts/mitigation/test report | Open | Watchdog no mitiga SEL/TID por sí solo. |
| CX-ENV-01 | Programa ambiental ejecutado sobre artículo/configuración controlados. | ENV-REQ-01; ICD | vibration/TVAC/EMC/deployment/pre-post | Blocked by Integrator | Niveles finales dependen del ICD; programa no es opcional. |

## 5. Evidencia, reviews y readiness

| ID | Requirement | Source | Verification/Evidence | Status | Disposición |
|---|---|---|---|---|---|
| CX-EP-01 | Evidence pack liga ReqID→ProcedureID→ConfigurationID→EvidenceID/hash. | MIS-REQ-15/SYS-REQ-04 | VCRM audit | Implemented | Estructura creada; evidencia de ensayo sigue abierta. |
| CX-EP-02 | Reviews siguen SRR→PDR→CDR→TRR→QAR→FRR. | SYS-REQ-03 | signed review records | Implemented | Gate A permanece Open. |
| CX-EP-03 | Ningún `Blocked by Integrator` crítico permanece en FRR. | ADR-20260727 verification governance | FRR checklist | Open | Bloquea readiness. |
| CX-EP-04 | Waivers registran autoridad y riesgo residual. | SYS-REQ-07 | waiver/NCR register | Planned | No existen waivers aprobados. |
| CX-AI-01 | Experimento IA tiene protocolo, manifest y benchmark limpio. | SYS-REQ-01/IA-REQ-10 | preregistration + digests + results | Open | `gemma4:e2b` es candidato no validado. |

## 6. Fuentes primarias

- CDS Rev.14.1:
  <https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS+REV14_1+2022-02-09.pdf>
- ENACOM Resolución 3635-E/2017:
  <https://www.enacom.gob.ar/multimedia/normativas/2017/res3635%20(octubre).pdf>
- IARU:
  <https://www.iaru.org/wp-content/uploads/2019/12/short_info_paper.pdf>
- ITU-R small satellite support:
  <https://www.itu.int/en/ITU-R/space/support/smallsat/Pages/default.aspx>

Las citas deberán confirmarse contra la revisión controlada del documento antes
de SRR. El ICD del integrador prevalecerá cuando sea más restrictivo.
