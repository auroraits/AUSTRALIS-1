# BOM Overview — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — incompleta, no apta para CDR/procurement de vuelo

## 1. Estado cuantitativo

`BOM_master.csv` contiene 83 filas:

| Stage | Filas |
|---|---:|
| Bench | 22 |
| Flight-Like | 40 |
| EGSE | 21 |
| Flight | 0 |

Brechas estructurales:

- cero filas `Flight`;
- filas placeholder explícitas para ADCS, launch safety, pack y radiación;
- cero costos unitarios numéricos/cotizados;
- masa, potencia y envelope permanecen `TBD`;
- la mayoría de MPNs, lead times y procurement states permanecen `TBD`.

Por ello la BOM no demuestra masa, volumen, potencia, costo ni viabilidad de
procurement.

## 2. Schema obligatorio

Cada fila registra:

- `ItemID` estable;
- subsistema y stage;
- clase de ítem, candidato y alternativa;
- fabricante/MPN/cantidad;
- supplier/región;
- costo/moneda/source date/lead time;
- riesgo y estado;
- masa/potencia/envelope;
- ReqID/RiskID/ADRID/ProcedureID;
- procurement state y EvidenceRef.

`TBD` es válido; una celda vacía o `ROM` usado como precio no lo es. Un precio
solo es válido con fuente, fecha, moneda, cantidad y condiciones.

`Status` describe madurez técnica de la fila: `Proposed`, `Open`, `Partial` o
`Closed`. `Partial` significa que existe un candidato o artículo de banco, pero
que su configuración/evidencia todavía no satisface el requisito asociado; no
significa verificado. `ProcurementState` describe exclusivamente disponibilidad,
cotización, autorización de compra y estado de adquisición. Ambos campos no son
intercambiables.

## 3. Disposiciones de configuración

- Estructura usa CDS 1.5U con `Z=170.2 ±0.1 mm` y referencia de masa máxima
  típica `3.00 kg`; resto del envelope y límite contractual del ICD siguen TBD.
- Pack 2S: celda, capacidad, paralelo, BMS y protección TBD.
- EPS flight-like: fabricación bloqueada; el KiCad actual no es design source.
- Payload IA: `gemma4:e2b` es modelo candidato; plataforma CM5 es banco
  candidato. Hardware flight-like/flight TBD.
- UHF: frecuencia, PA, filtro, antena y LNA dependen de coordinación/trade.
- LoRa: concentrator vs receptor simple reabierto.
- Ground: rotor, T/R e interlock PTT, PA, filtros/limiter, metrología RF,
  terminaciones, protección eléctrica, UPS/PDU y timebase tienen placeholders
  explícitos y permanecen abiertos.
- Solar/radiador/TIM: layout, cantidad, propiedades y selección reabiertos.
- Ninguna parte sin MPN/evidencia se clasifica de bajo riesgo.

## 4. Campos de roll-up

Antes de PDR:

- todas las filas de la configuración preliminar tendrán masa, envelope y
  power mode allocation;
- ADCS, harness, launch inhibits/RBF/deployment, pack parts y mitigación de
  radiación tienen filas placeholder que deberán descomponerse en partes;
- solar interconnect/coverglass, thermal sensors y ground safety se incorporarán;
- cada subsistema tendrá subtotal con reserva y maturity;
- se registrarán alternativas y obsolescencia.

Antes de CDR:

- MPN/alternativa/lifecycle/temperature/derating cerrados;
- BOM de fabricación y as-designed configuration;
- quotes vigentes y lead times;
- spares y lot strategy;
- mass/power/volume roll-ups con margen;
- compliance y test article mapping.

## 5. Riesgo de supply chain

El campo `Risk` es conservador hasta contar con:

- disponibilidad verificada;
- segunda fuente o buy/lifetime strategy;
- lifecycle/EOL;
- rango térmico y derating;
- provenance/traceability;
- impacto de importación, FX y aduana;
- compatibilidad ambiental/radiación aplicable.

Ver `../07_Risk/top_risks.md` (`RSK-SUP-01`, `RSK-COST-01`).
