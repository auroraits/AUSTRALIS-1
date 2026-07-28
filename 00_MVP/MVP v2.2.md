# AUSTRALIS-1 — MVP v2.2

**Revisión:** 2026-07-27
**Estado:** Baseline pre-SRR — Gate A abierto
**Trazabilidad:** ADRs `Accepted` vigentes en `08_Decisions/`

> Esta revisión sustituye el cuerpo normativo previo de v2.2. Las versiones
> históricas y el historial Git conservan las decisiones anteriores. Ante una
> contradicción prevalece la ADR `Accepted` más reciente.

## 1. Resumen ejecutivo

AUSTRALIS-1 es un CubeSat 1.5U experimental. La misión primaria estudia un
payload de IA como asesor de vuelo, sin transferir autoridad del OBC
determinístico. El modelo candidato actual es `gemma4:e2b`, todavía sin
validación ni selección de vuelo.

La configuración está en reconciliación después de una auditoría integral. La
geometría, órbita, ADCS, energía, térmica, RF y hardware flight-like contienen
trabajo abierto. Por ello el estado defendible es **pre-SRR**, no PDR/flight
ready.

## 2. Alcance

### Incluido

- bus 1.5U;
- EPS de referencia 2S + MPPT;
- OBC determinístico y almacenamiento;
- TTC UHF coordinado y beacon público;
- receptor experimental de uplink terrestre sujeto a regulación;
- Science Pack sin alta tensión;
- payload IA power-gated;
- ground segment y evidence repository;
- ADCS, estructura, térmico y mecanismos requeridos para una misión real.

### Fuera del éxito mínimo

- `PHOTO_DEMO`;
- Geiger/alta tensión;
- control directo por IA;
- transmisión LoRa/ISM desde órbita;
- cualquier claim comercial, de vuelo o de aprobación no evidenciado.

## 3. Objetivos de misión

### 3.1 Objetivo científico primario

Determinar, mediante un protocolo preregistrado, si el candidato IA y su
supervisor:

1. producen recomendaciones con utilidad medible frente a un baseline
   determinístico;
2. mantienen la tasa de violaciones de reglas críticas dentro del límite
   predefinido;
3. operan dentro de límites de latencia, energía y temperatura medidos;
4. generan evidencia completa y reproducible.

### 3.2 Objetivos secundarios

- demostrar store-and-forward Tierra→órbita→tierra si el enlace resulta
  autorizable;
- recolectar Science Pack;
- evaluar operación y recuperación del sistema en LEO.

## 4. Protocolo científico obligatorio

Antes de SRR deberán quedar congelados:

| Elemento | Contenido mínimo |
|---|---|
| Hipótesis | hipótesis de utilidad y seguridad; hipótesis nula |
| Control | baseline determinístico y/o modelo de referencia |
| Población | matriz de estados, fallas, escenarios nominales/adversariales |
| Oráculo | expected action/constraints definido fuera del modelo |
| Métricas | correctitud, utilidad, unsafe proposal rate, reject/accept, latencia, energía, temperatura |
| Muestra | tamaño y potencia/precisión estadística justificados |
| Umbrales | criterio pass/fail preregistrado; reglas críticas exact-match |
| Datos | schema, unidades, quality flags, raw input/output y correlación |
| Análisis | seeds, intervalos de confianza, manejo de exclusiones/missing data |
| Configuración | hashes de modelo, tokenizer, prompt, supervisor, firmware, dataset y runtime |

Cinco inferencias, cien logs y un prompt son pisos operacionales históricos,
pero no prueban por sí mismos la hipótesis científica.

## 5. Criterio mínimo de éxito

El éxito se declara únicamente si:

1. el bus cumple los criterios de supervivencia y recuperación aprobados;
2. se ejecuta el protocolo científico preregistrado sobre la muestra mínima;
3. todas las reglas críticas se evalúan con oráculo externo;
4. se alcanzan los umbrales de seguridad/utilidad/recursos aprobados;
5. el evidence pack permite reproducir cada inferencia y decisión;
6. se descargan, como mínimo operacional, 100 eventos completos y al menos una
   configuración de prompt autorizada;
7. no existe una violación no resuelta de seguridad, regulación o integridad.

Los valores estadísticos finales son `TBD` y deben cerrarse en SRR. Mientras
sean TBD no puede declararse cumplido el objetivo primario.

## 6. Plataforma y mecánica

- Clase: CubeSat 1.5U.
- Longitud externa de referencia CDS Rev. 14.1: `170.2 ± 0.1 mm`.
- La simplificación histórica `100 × 100 × 150 mm` queda invalidada.
- Envolvente completa, rails, keep-outs, protrusiones, masa, CG e interfaz:
  CDS + ICD del integrador.
- CAD conforme, stack, harness, load path, modos propios, FEA, stowage de
  antena y fit-check: `TBD`.

## 7. Órbita y ADCS

- No existe órbita confirmada.
- Envolvente preliminar de estudio: LEO/SSO candidata `550–650 km`, sujeta a
  integrador, debris/reentry y regulación.
- `600 km / LTAN 10:00` es un caso etiquetado de análisis.
- Cada SSO deberá derivar inclinación por altitud y demostrar drift LTAN.
- LVLH perfecto no es baseline de actitud.
- Arquitectura ADCS, detumbling, sensores, actuadores, pointing, jitter,
  consumo, masa y safe attitude: `TBD`.

## 8. Modelo operativo y autoridad

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

- Boot/reset en `SAFE`.
- `EPS_STATE=CRIT` fuerza `SAFE`.
- `LOW` conserva cargas críticas y bloquea IA por defecto.
- Ciencia es actividad dentro de `NOMINAL`, no un modo.
- El OBC es la única autoridad de vuelo.
- La máquina EPS deberá definir entradas, umbrales, histéresis, dwell,
  boot/unknown, sensores inválidos y precedencia de fallas antes de PDR.

## 9. Payload IA

### 9.1 Candidato

- Modelo: `gemma4:e2b`.
- Estado: candidato para evaluación.
- Digest/revisión, cuantización, tokenizer, licencia y runtime: `TBD`.
- Hardware bench: familia CM5 candidata; configuración exacta TBD.
- Hardware flight-like/flight: TBD.

Granite 350M/2B y SmolLM2 quedan históricos/diferidos. No se reutilizan sus
métricas como evidencia del candidato actual.

### 9.2 Contención

- power-gated y OFF por defecto;
- OFF en SAFE, eclipse y EPS CRIT/LOW;
- mutua exclusión con TX salvo caso validado;
- watchdog/kill/fallback independientes;
- catálogo de tools, clases y permisos definido por OBC;
- JSON/schema/rangos/precondiciones/postcondiciones validados;
- ninguna tool call directa desde el modelo al hardware.

### 9.3 Registro científico

Cada evento debe correlacionar:

- event/session/boot ID y timestamps;
- input/snapshot completo y su hash;
- raw output y parse result;
- model/tokenizer/adapter/runtime/config digests;
- prompt/policy/supervisor/firmware versions;
- decoding/seed/parámetros;
- tool solicitada, validación, decisión y razón;
- acción aplicada y postestado;
- latencia, memoria, energía y temperaturas;
- calidad de datos y anomalías.

`confidence` solo será métrica si existe definición y calibración.

## 10. EPS y energía

- Topología de referencia: batería 2S + MPPT.
- Celda, capacidad, paralelo, BMS, cargador, secondary protection, fusible,
  balanceo, charge inhibit y rails: TBD.
- El proyecto KiCad actual es placeholder/no fabricable; fabricación bloqueada.
- El power budget deberá usar el período orbital real del caso, todos los modos,
  min/nom/max, inrush, quiescent, conversiones, BOL/EOL e incertidumbre.
- No hay target solar, margen energético ni duty IA confirmados.
- Límites térmicos de batería incluyen carga, descarga, supervivencia y máximos
  según celda/BMS final.

## 11. Térmico

- No hay cara radiadora, coating, conductancia ni heater decididos.
- El modelo debe conservar energía y derivar geometría/masa del CAD/BOM.
- Incluir radiación solar/albedo/IR terrestre, view factors, extracción FV,
  todas las disipaciones, interfaces y degradación.
- Propiedades ópticas se verificarán en material/cupón real.
- Un fallback fuera de especificación es una configuración nueva.
- Thermal balance/TVAC correlaciona el modelo antes de readiness.

## 12. Comunicaciones y seguridad

### 12.1 UHF

- frecuencia coordinada dentro de la atribución aplicable: TBD;
- hardware, waveform, bitrate, FEC, potencia y máscara: TBD;
- link budget uplink/downlink separado y medido;
- patrón de antena integrado, Doppler, coexistencia y PER incluidos.

### 12.2 Enlace terrestre experimental

- satélite 915 MHz RX-only;
- transmisión intencional Tierra→espacio requiere respuesta/autorización escrita;
- PHY, canales, slots y receptor permanecen TBD;
- si no es autorizable se migra servicio/banda o se redefine el objetivo.

### 12.3 TTC seguro

Comandos/prompts requieren autenticación, integridad y anti-replay: tag
criptográfico, contador persistente, key epoch, roles, upload/activate separado,
ACK autenticado, rotación y recovery. CRC/hash simple no autentica.

SatNOGS se limita a recepción pública y nunca accede a PTT/credenciales.

## 13. Software, datos y ground

- Persistencia raw append-only por sesión.
- Datos parseados conservan schema, unidades, quality flags y provenance.
- Replay determinístico y export verificable.
- Estadísticas distinguen boot/session, wrap, duplicados y out-of-order.
- Parser valida rangos, finitud, monotonía y consistencia física.
- Interfaces de adquisición/control se autentican si se exponen en LAN.
- Dependencias quedan bloqueadas/versionadas para operación offline.

## 14. COTS-to-flight, radiación y ambiente

Antes de CDR:

- FMEA/FMECA y single-point failures;
- TID/DDD/SEE/SEL, shielding y mitigaciones;
- latch-up current limiting/power-cycle;
- EDAC/scrubbing/redundancia de datos;
- derating, temperatura, lifecycle y provenance de partes;
- estrategia de artículos qualification/acceptance.

Programa mínimo:

- inspección/funcional pre/post;
- random vibration y sine/launch loads según ICD;
- shock si aplica;
- thermal cycling y TVAC/thermal balance;
- EMC/coexistencia;
- deployment después de ambiente;
- RF end-to-end y fit-check.

## 15. Downlink y datos

Prioridad:

1. `HOUSEKEEPING`;
2. `COMMAND_ACK`;
3. `AI_BEHAVIOR_LOG` como mayor prioridad científica best-effort;
4. otros productos con cuota/aging.

El data budget deberá demostrar producción diaria, overhead, contacto útil,
retención, pérdida tolerable y ausencia de starvation.

## 16. Costos y procurement

- BOM separada `Bench | Flight-Like | Flight | EGSE`.
- Cada fila: clase, candidato/alternativa, fuente/fecha, costo, lead time,
  estado, masa/potencia/volumen, trazabilidad y riesgo.
- `TBD` donde no exista evidencia; `ROM` no es un precio.
- Life-Cycle Cost incluye NRE, integración, regulación, ensayos, lanzamiento,
  transporte/importación, spares, mano de obra y reservas.

## 17. Top riesgos

Bloqueantes actuales:

1. configuración/documentación inconsistente;
2. geometría 1.5U errónea propagada;
3. EPS no fabricable y batería sin protección completa;
4. experimento IA sin protocolo/benchmark limpio;
5. órbita/SSO y modelos físicos no validados;
6. ADCS inexistente;
7. RF/regulación/seguridad TTC abiertos;
8. ausencia de budgets integrados;
9. ausencia de estrategia radiación/ambiente;
10. CAD/BOM/costos/schedule incompletos.

Registro controlado: `07_Risk/top_risks.md`.

## 18. Reviews y gates

`SRR → PDR → CDR → TRR → Qualification/Acceptance Review → FRR`

- Gate A: Open.
- No se aceptan dependencias “preliminares” para integración.
- Waiver requiere autoridad, justificación y riesgo residual.
- `Blocked by Integrator` bloquea FRR si afecta seguridad/readiness.

Ver `01_Mission/validation_plan_and_stage_gates.md`.

## 19. Trazabilidad

- requisitos: `01_Mission/requirements_matrix.md`;
- VCRM: `01_Mission/verification_cross_reference_matrix.csv`;
- compliance: `01_Mission/compliance_matrix.md`;
- costs/BOM: `06_Costs/`;
- riesgos: `07_Risk/`;
- ADRs: `08_Decisions/`.

## 20. Disposición de claims históricos

No son claims vigentes:

- Granite 350M “validado”;
- mejora `14 % → 57 %` como evidencia de seguridad;
- órbita `600/650 km` o LTAN `9:30/10:00` confirmados;
- radiador `−Y` confirmado;
- `3.4×–3.6×` de margen;
- heater no requerido;
- EPS/RF KiCad como diseños fabricables;
- banco 433 MHz a 20 Hz RF/100 Hz de filtro;
- Madgwick IMU terrestre como evidencia de ADCS orbital.

Estos datos solo pueden citarse con etiqueta histórica/invalidada y su
limitación explícita.
