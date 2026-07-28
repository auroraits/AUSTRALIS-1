# System Baseline — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Baseline pre-SRR — configuración en reconciliación
**Gate de configuración:** A = `Open`

## 1. Regla de lectura

Este documento separa decisión, candidato, hipótesis y evidencia. Las palabras
`Accepted` o `Baseline` no significan `Verified`.

| Etiqueta | Significado |
|---|---|
| Decidido | ADR `Accepted` vigente |
| Candidato | opción elegida para evaluar; puede fallar |
| Hipótesis | valor usado para análisis; no requisito |
| Verified | criterio satisfecho por evidencia controlada |
| TBD | falta decisión o evidencia |

## 2. Misión

**Objetivo primario:** evaluar rigurosamente si un payload IA puede producir
recomendaciones útiles bajo un supervisor determinístico, sin adquirir
autoridad de vuelo.

**Objetivos secundarios:** store-and-forward experimental, paquete de sensores
y `PHOTO_DEMO` opcional.

El protocolo científico debe fijar antes de SRR: hipótesis/nula, baseline
determinístico, oráculo, escenarios, tamaño muestral, métricas, umbrales,
intervalos de confianza y plan de análisis. Los conteos de inferencias/logs son
pisos de datos, no prueba suficiente de utilidad o seguridad.

## 3. Baseline decidido

### 3.1 Plataforma y seguridad

- Formato: CubeSat **1.5U**.
- Longitud externa de referencia: `170.2 ± 0.1 mm`, CDS Rev. 14.1.
- Envolvente completa, masa, CG, rails/keep-outs e interfaces: ICD integrador
  `TBD`.
- Boot y fallback: `MISSION_MODE = SAFE`.
- Estados: `MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW`;
  `EPS_STATE = CRIT | LOW | NOMINAL | HIGH`.
- OBC determinístico como única autoridad.
- Separación `Bench | Flight-Like | Flight | EGSE`.
- `PHOTO_DEMO`: opcional, OFF por defecto, best-effort.

### 3.2 Payload IA

- Modelo candidato actual: **`gemma4:e2b`**.
- Hardware de banco candidato: familia CM5; SKU y configuración inmutable TBD.
- Modelo y hardware de vuelo: TBD.
- Granite 350M/2B y SmolLM2: históricos/diferidos.
- Estado de evidencia: **Open**. No se heredan métricas históricas.
- Toda herramienta/acción deberá validarse por schema y reglas del OBC; la
  clase de seguridad no puede provenir del modelo.

### 3.3 EPS

- Arquitectura de referencia: batería Li-ion 2S + carga con seguimiento de
  punto de máxima potencia.
- Capacidad, celda, BMS, cargador, rails, MPPT por cara/string y hardware final:
  TBD.
- El KiCad flight-like actual no es fabricable; fabricación bloqueada hasta
  revisión de esquema, ERC, BOM, DRC y liberación controlada.
- Límites de carga/descarga/supervivencia y heater dependen de la celda/BMS y de
  modelo térmico correlacionado.

### 3.4 RF y operaciones

- Satélite no transmite LoRa/ISM 915 MHz en órbita.
- UHF coordinada dentro de la atribución aplicable: frecuencia exacta, waveform,
  bitrate, potencia, hardware y máscara TBD.
- `PUBLIC_BEACON` documentado; SatNOGS receive-only.
- Comandos y prompts: autenticación, integridad y anti-replay obligatorios;
  confidencialidad sujeta a regulación.
- Experimento LoRa 915 MHz Tierra→espacio: condicionado a autorización escrita
  de la administración competente.

## 4. Baselines reabiertos

| Dominio | Estado | Razón principal | Evidencia necesaria |
|---|---|---|---|
| Órbita/LTAN | Open | barrido no imponía SSO y CSV no reproducía ADR | propagación validada + manifest |
| Actitud/ADCS | Open | LVLH perfecto sin arquitectura ADCS | CONOPS, hardware, control y dispersión |
| Solar/energía | Open | geometría/cargas/pérdidas incompletas | ledger BOL/EOL por modo |
| Térmica | Open | balance físico inconsistente | modelo conservativo + correlación |
| Radiación | Open | TID/SEE/SEL no analizados | entorno, shielding, mitigación y test |
| Estructura | Open | sin CAD conforme ni mass properties | CAD, stack, FEA y fit-check |
| EPS | Open | BMS/charger/rails no implementados | diseño revisado y ensayos |
| RF | Open | link budgets/hardware/regulación abiertos | budgets bidireccionales + OTA |
| Ground data | Open | persistencia/replay incompletos | raw+metadata+replay+export |

`600 km / LTAN 10:00 / LVLH perfecto` puede aparecer solo como **caso de
análisis etiquetado**, no como configuración confirmada.

## 5. Presupuestos

Todos los budgets cuantitativos están `Open` hasta contar con una configuración
controlada.

- **Potencia/energía:** cargas min/nom/max, inrush, conversión, MPPT,
  sol/eclipse, BOL/EOL, incertidumbre y batería.
- **Térmico:** disipaciones, propiedades espectrales, view factors, interfaces,
  límites de carga de batería y correlación.
- **Masa/volumen/CG/inercia:** derivados de CAD/BOM.
- **Datos:** producción, overhead, contacto útil, retención, pérdida admisible,
  cuotas y aging.
- **RF:** uplink y downlink separados, EIRP/G/T, Doppler, waveform, patrón,
  coexistencia, PER/BER e incertidumbre.

Se retiran como claims vigentes `4.5 Wh/órbita`, `72–76 Wh/día`,
`3.4×–3.6×`, “radiador −Y confirmado” y “heater no requerido”.

## 6. Verificación y reviews

- VCRM: `01_Mission/verification_cross_reference_matrix.csv`.
- Compliance externo: `01_Mission/compliance_matrix.md`.
- Reviews: `01_Mission/validation_plan_and_stage_gates.md`.
- Riesgos: `07_Risk/top_risks.md`.

Readiness requiere todos los requisitos de seguridad, regulación, ambiental e
integrador en `Verified` o un waiver formal admisible. `Blocked by Integrator`
impide FRR.

## 7. Próximas decisiones de sistema

1. cerrar Gate A con cero contradicciones de parámetros/estados;
2. aprobar protocolo científico y VCRM en SRR;
3. corregir geometría en CAD/SIM y recalcular budgets;
4. caracterizar `gemma4:e2b` exacto con benchmark limpio;
5. seleccionar arquitectura ADCS y COTS-to-flight;
6. reconstruir EPS y RF antes de fabricar;
7. obtener ruta regulatoria ENACOM/IARU/ITU por escrito;
8. ejecutar programa ambiental y end-to-end antes de FRR.
