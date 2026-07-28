# AUSTRALIS-1 — DIY Nanosat

**Revisión:** 2026-07-27
**Estado:** Active — desarrollo pre-SRR; Gate A abierto
**Release público:** `public-v0.2` es el último snapshot publicado y no contiene
necesariamente las correcciones de esta rama.

Sitio oficial: <https://australis.aurora.ar/>

## Propósito

AUSTRALIS-1 es un proyecto CubeSat 1.5U experimental cuyo objetivo científico
primario es evaluar un payload de inteligencia artificial como **asesor** de
vuelo bajo supervisión determinística. El OBC (On-Board Computer) conserva toda
la autoridad; el modelo no acciona cargas ni actuadores directamente.

Objetivos secundarios:

1. evaluar una cadena store-and-forward Tierra→órbita→tierra, sujeta a cierre
   regulatorio;
2. operar un paquete de sensores ambientales;
3. mantener `PHOTO_DEMO` como demostración opcional, OFF por defecto y fuera del
   éxito mínimo.

## Dictamen de madurez vigente

El proyecto es **experimental/pre-SRR**. La documentación ya no declara como
confirmados resultados que la evidencia disponible no reproduce.

- **Modelo IA candidato:** `gemma4:e2b`, pendiente de identificación inmutable,
  licencia, benchmark limpio y mediciones en hardware. No está validado ni
  seleccionado para vuelo.
- **Granite 350M/2B y SmolLM2:** históricos/diferidos, sin claim vigente de
  validación. La evidencia rotulada Granite 350M fue ejecutada con Granite 2B.
- **Plataforma:** CubeSat 1.5U; longitud externa de referencia CDS Rev. 14.1
  `170.2 ± 0.1 mm`. La envolvente completa y el fit-check dependen del CDS y del
  ICD del integrador.
- **Órbita, LTAN, actitud, ADCS, layout solar y radiador:** abiertos. `600 km /
  LTAN 10:00` es solamente un caso de análisis.
- **Energía y térmica:** abiertos. No existe margen `3.4×–3.6×` confirmado ni
  conclusión válida de “sin heater”.
- **EPS y RF flight-like:** los proyectos KiCad actuales son placeholders y no
  son fabricables/liberables.
- **COMMS:** frecuencia UHF coordinada, waveform, potencia y máscara son TBD.
  El experimento LoRa Tierra→espacio en 915 MHz depende de autorización escrita.
- **Readiness:** no puede declararse con requisitos de seguridad, regulación,
  ambiente o integrador abiertos/bloqueados.

## Decisiones correctivas principales

- `08_Decisions/ADR-20260727-cubesat-1p5u-cds-envelope.md`
- `08_Decisions/ADR-20260727-ai-payload-gemma4-e2b-candidate.md`
- `08_Decisions/ADR-20260727-orbit-attitude-analysis-reopened.md`
- `08_Decisions/ADR-20260727-thermal-power-baselines-reopened.md`
- `08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`
- `08_Decisions/ADR-20260727-verification-and-review-governance.md`

## Fuentes de verdad

1. ADRs `Accepted` más recientes en `08_Decisions/`.
2. `00_MVP/MVP v2.2.md`, baseline consolidado.
3. `SYSTEM_BASELINE.md`, resumen del estado.
4. `01_Mission/requirements_matrix.md` y
   `01_Mission/verification_cross_reference_matrix.csv`.
5. Documentos de subsistema.

`Baseline` significa configuración de referencia, no evidencia de verificación.
Un análisis `Preliminary`, un prototipo `Bench` o un esquema placeholder nunca
se interpretan como hardware flight-like verificado.

## Mapa del repositorio

| Ruta | Contenido |
|---|---|
| `00_MVP/` | Baseline maestro e historia |
| `01_Mission/` | Misión, requisitos, VCRM, compliance y reviews |
| `02_Structure/` | Estructura, CAD y mecánica |
| `03_Power/` | EPS, batería, solar y budgets |
| `04_Communications/` | RF, enlaces y ground segment |
| `05_Software/` | FSW, simulación, IA, firmware y ground software |
| `06_Costs/` | BOM y Life-Cycle Cost (LCC) |
| `07_Risk/` | Risk register y análisis específicos |
| `08_Decisions/` | Architecture Decision Records (ADR) |
| `99_References/` | Normas y referencias |
| `docs/` | Planes de prueba y notas operativas |

## Flujo de madurez

`SRR → PDR → CDR → TRR → Qualification/Acceptance Review → FRR`

Cada cierre requiere requisito, criterio, procedimiento, configuración del
artículo y evidencia identificada/hash. Un waiver debe conservar justificación,
autoridad y riesgo residual.

## Publicación y licencia

El repositorio es **source-available no comercial**, no “open source” OSI:

- software/código: PolyForm Noncommercial 1.0.0;
- documentación/diseños/datasets: CC BY-NC-SA 4.0;
- terceros: rigen sus licencias y notices.

Ver `LICENSE.md`, `THIRD_PARTY_NOTICES.md`, `COMMERCIAL_USE.md` y
`CONTRIBUTING.md`. Modelo, dataset y artefactos deberán registrar provenance,
licencia y digest antes de distribuirse o usarse como evidencia.
