# AUSTRALIS-1 / DIY Nanosat - AGENTS.md Raiz (Politica Documental Global)

**Revision:** 2026-03-14

Este archivo es la autoridad raiz de gobierno documental del proyecto. Todos los `AGENTS.md` de subsistema deben ser coherentes con estas reglas y solo pueden agregar restricciones locales, nunca contradecirlas.

---

## 1) Objetivo del repositorio

Este repositorio es la **fuente de verdad** de documentacion tecnica del proyecto DIY Nanosat y de la mision **AUSTRALIS-1**.

La identidad vigente de mision es:
**AUSTRALIS-1 - Experimental Autonomic Flight AI-Assisted CubeSat**

El objetivo primario documentado del sistema es poner un payload de inteligencia artificial en orbita LEO, operarlo como asistente de vuelo autonomo bajo supervision deterministica, y recolectar datos de desempeno del modelo para entrenar versiones futuras de IA para CubeSats.

Los cambios deben mantener coherencia sistemica entre:
- mision -> requisitos -> arquitectura -> costos -> riesgos -> decisiones (ADR)
- y evitar contradicciones entre subsistemas (EPS, COMMS, FSW, estructura, termico, etc.)

---

## 2) Jerarquia documental (precedencia)

Ante cualquier contradiccion, prevalece el documento de mayor jerarquia:

1. **ADR `Accepted`** en `08_Decisions/` (maxima autoridad)
2. **`00_MVP/MVP v2.2.md`** (baseline consolidado vigente - fuente de verdad del sistema)
3. **`SYSTEM_BASELINE.md`** (resumen de entrada rapida al baseline)
4. **Documentacion por subsistema** (`01_Mission/` a `07_Risk/`)
5. **Documentos `Draft` / `Proposed` / `Preliminary` / `Propuesta`** (aportan contexto tecnico; NO sobreescriben baseline)
6. **Historicos / Superseded** (trazabilidad y contexto)

**Regla clave:** Un documento `Draft`, `Proposed` o `Preliminary` NO puede declarar una decision de arquitectura como bloqueada. Requiere ADR `Accepted`.

---

## 3) Estados documentales permitidos

| Estado | Significado |
|---|---|
| `Accepted` | Decision bloqueada; normativa. Solo para ADRs. |
| `Baseline` | Documento de referencia del sistema; sincronizado con ADRs vigentes. |
| `Active` | Documento vivo y coherente con el baseline. |
| `Draft` | Trabajo en progreso; no normativo; puede contradecirse. |
| `Proposed` | Propuesta formal; requiere ADR para bloquearse. |
| `Preliminary` | Analisis o dato pre-decision; no cierra decision. |
| `Superseded` | Reemplazado por version posterior; conservado para trazabilidad. |
| `Historical Snapshot` | Instantanea historica; no normativa. |

---

## 4) Cabecera minima recomendada para documentos clave

```markdown
**Revision:** YYYY-MM-DD
**Estado:** [Active | Draft | Proposed | Preliminary | Superseded | Historical Snapshot]
**Trazabilidad:** [ADR / documento fuente que origina o actualiza este doc]
```

---

## 5) Estructura del repositorio

```
00_MVP/         - Historial + baseline consolidado (MVP v2.2.md = fuente de verdad)
01_Mission/     - Mision, orbita, payload, requisitos, compliance, validacion
02_Structure/   - Mecanica, termico, vibracion, Block Diagram
03_Power/       - EPS: bench, flight-like, flight; paneles, bateria, budget, sizing
04_Communications/ - LoRa RX-only, UHF TTC, antenas, ground station
05_Software/    - Flight software, ground control, dashboard, firmware bench
06_Costs/       - BOM maestra, modelos ROM de costos por subsistema
07_Risk/        - Matrices de riesgo, top-risks, FMEA liviano
08_Decisions/   - ADRs (Architecture Decision Records)
99_References/  - Standards, papers, referencias tecnicas
docs/           - Planes de prueba y notas operativas de banco
```

---

## 6) Reglas de edicion (Markdown)

- Mantener estilo tecnico, conciso, con secciones y listas.
- Preferir tablas para comparaciones (costo, tradeoffs, riesgos).
- **No inventar cifras:** si falta dato, marcar como `TBD` con hipotesis explicita.
- Cada decision relevante de arquitectura debe quedar en un ADR en `08_Decisions/`.
- Idioma principal: **espanol**. Primera aparicion de sigla relevante: expandir entre parentesis.
- No usar emojis salvo solicitud explicita del usuario.

---

## 7) Regla de coherencia sistemica (obligatoria)

Cuando se modifica algo en un subsistema, verificar impacto y actualizar si aplica:

| Cambio en | Actualizar tambien |
|---|---|
| Arquitectura / baseline | `00_MVP/MVP v2.2.md`, `SYSTEM_BASELINE.md`, `architecture.md`, ADR |
| Energia / EPS | `03_Power/*`, `06_Costs/*`, `07_Risk/*` |
| COMMS / RF | `04_Communications/*`, `07_Risk/*`, `06_Costs/*` |
| Software / FSW | `05_Software/*`, `00_MVP/MVP v2.2.md` si cambia comportamiento |
| Costos / BOM | `06_Costs/BOM_master.csv`, `06_Costs/bom_overview.md` |
| Riesgos | `07_Risk/top_risks.md`, matrices especificas |
| Cualquier decision de arquitectura | `08_Decisions/ADR-YYYYMMDD-<slug>.md` |

---

## 8) Modelo operativo canonico

El sistema tiene un modelo de modos operativos unico, canonico y obligatorio:

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

**Reglas:**
- `SAFE` es el modo por defecto post-reset y en eclipse.
- La actividad cientifica **NO** es un modo operativo independiente; se ejecuta como actividad dentro de `MISSION_MODE = NOMINAL` bajo condiciones energeticas adecuadas.
- Si `EPS_STATE = CRIT`, el sistema degrada automaticamente a `MISSION_MODE = SAFE`.
- Si `EPS_STATE = LOW`, el sistema permanece en `SAFE` por defecto; `MISSION_MODE = NOMINAL` solo se admite para housekeeping esencial explicitamente permitido.
- El payload IA solo puede operar con `MISSION_MODE = NOMINAL`, fase de sol y `EPS_STATE >= NOMINAL`.
- Documentos que refieran a un "SCIENCE MODE" canonico son historicos o estan desactualizados.

> Nota historica: versiones anteriores del documento MVP usaban la denominacion "SCIENCE MODE" como tercer modo. Esa nomenclatura queda supersedada por `MISSION_MODE = NOMINAL` con actividad cientifica como actividad interna. El presupuesto de potencia mantiene la columna `duty_sci` por compatibilidad de calculo.

---

## 9) Separacion obligatoria bench / flight-like / flight

Toda documentacion y BOM deben distinguir explicitamente:

| Capa | Descripcion |
|---|---|
| `Bench` | Hardware COTS de validacion funcional y desarrollo de firmware. No es hardware de vuelo. |
| `Flight-Like` | Arquitectura electrica en PCB custom; integracion y pruebas de sistema. No calificado de vuelo. |
| `Flight` | Hardware final de vuelo con politica COTS-to-Flight completa y calificacion. |
| `EGSE` | Equipo de soporte en tierra (Electrical Ground Support Equipment). |

**Regla:** No mezclar bench y flight-like en la misma linea de BOM ni en el mismo analisis normativo.

---

## 10) Politica PHOTO_DEMO

`PHOTO_DEMO` esta congelado como:
- **Opcional** y **no critico**
- **OFF por defecto** al boot (off-by-default)
- **Best-effort** bajo Downlink Manager (cola `OPTIONAL_PAYLOAD`)
- Encapsulado por feature flag (`<!-- FEATURE:PHOTO_DEMO START/END -->`)
- Fuera del criterio minimo de exito del MVP
- Su falla no degrada la cadena principal

Referencia: `08_Decisions/ADR-20260313-photo-demo-opcional-no-critico.md`

---

## 11) Nodo tipico LoRa terrestre (clase, no SKU)

El "nodo tipico" objetivo para uplink LoRa se define como **clase de nodo**, no como SKU de mercado:

- Banda terrestre objetivo: `915-928 MHz` (AU915 o equivalente)
- Radio clase `SX1262` o `SX1276` o equivalente
- Microcontrolador clase `ESP32-S3` o equivalente
- Potencia tipica: `+20 a +21 dBm`
- Antena simple: `0-2 dBi`
- Cristal comercial tipico: `+/-10 ppm`
- Sin PA (Power Amplifier) externo
- Sin LNA (Low-Noise Amplifier) externo
- Sin antena direccional
- Sin asumir TCXO (Temperature-Compensated Crystal Oscillator)

Referencias de mercado (no normativas): modulos Heltec, RFM95W y similares son ejemplos de esta clase.

Parametros TBD (no cerrados aun):
- elevacion minima operativa
- canalizacion exacta dentro de 915-928 MHz
- BW definitivo (125 vs 250 kHz)
- criterio numerico final de aceptacion uplink

---

## 12) Estado TTC UHF y OpenLST

Baseline operativo vigente: **UHF 435 MHz FSK 1200 bps**

OpenLST queda como:
- Base de desarrollo / candidato derivado para TTC UHF
- Analisis tecnico activo (`04_Communications/RF_ANALISYS_OPENLST.md`)
- **NO** adoptado como baseline final; **NO** adoptar "tal cual" (componente RFFM6403 es EOL)
- Hardware final TTC UHF sigue `TBD`
- Para cerrar adopcion: requiere ADR nueva en estado `Accepted`

---

## 13) ADRs (Architecture Decision Records)

Formato de nombre: `ADR-YYYYMMDD-<slug>.md`

Contenido minimo:
```markdown
- Fecha
- Estado: Proposed | Accepted | Superseded
- Contexto
- Decision
- Alternativas consideradas
- Tradeoffs / riesgos
- Implicancias (archivos a actualizar)
```

Si una decision ya existe parcialmente, actualizar la ADR existente en vez de duplicarla.

---

## 14) Flujo de trabajo con Git

- Commits pequenos y descriptivos.
- Formato de mensaje: `<subsistema>: <intencion>`
  - Ej: `EPS: formaliza separacion bench/flight-like/flight`
  - Ej: `COMMS: actualiza definicion de nodo tipico como clase`

---

## 15) Que NO hacer

- No inventar numeros, piezas, costos, MPNs, fechas, owners ni resultados de ensayo.
- No agregar binarios grandes sin justificacion.
- No reestructurar carpetas masivamente sin ADR.
- No borrar historia: reetiquear como `Superseded` o `Historical Snapshot`.
- No declarar resultados de validacion que no existen.
- No asumir requerimientos finales del integrador / launch provider.
- No cambiar codigo fuente funcional salvo documentacion asociada.
- No dejar documentos importantes sin referencias cruzadas.
- No fijar SKUs de mercado como requisitos formales.
- No promover OpenLST a radio final seleccionada sin ADR.
- No convertir `EPS_DESIGN_RULES.md` en documento normativo.

---

## 16) Definicion de "Hecho" (DoD) para cambios documentales

Un cambio queda "hecho" si:
1. Documento del subsistema actualizado.
2. Referencias cruzadas consistentes.
3. ADR creado/actualizado si cambio una decision de arquitectura.
4. Costos (`06_Costs/*`) y riesgos (`07_Risk/*`) ajustados si corresponde.
5. `00_MVP/MVP v2.2.md`, `SYSTEM_BASELINE.md` y `architecture.md` sincronizados si corresponde.
6. Compliance matrix (`01_Mission/compliance_matrix.md`) actualizada si corresponde.
7. Plan de validacion (`01_Mission/validation_plan_and_stage_gates.md`) actualizado si corresponde.

---

## 17) AGENTS.md de subsistemas

Los `AGENTS.md` de cada carpeta de subsistema:
- **Heredan** todas las reglas de este archivo raiz.
- **Solo pueden agregar** restricciones o convenciones locales al subsistema.
- **No pueden contradecir** ninguna regla raiz.
- Si hay conflicto, prevalece este archivo raiz.

Subsistemas con AGENTS.md propios:
- `00_MVP/AGENTS.md`
- `01_Mission/AGENTS.md`
- `02_Structure/AGENTS.md`
- `03_Power/AGENTS.md`
- `04_Communications/AGENTS.md`
- `05_Software/AGENTS.md`
- `06_Costs/AGENTS.md`
- `07_Risk/AGENTS.md`
- `08_Decisions/AGENTS.md`
- `99_References/AGENTS.md`