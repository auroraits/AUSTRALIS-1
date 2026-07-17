# BOM Overview — AUSTRALIS-1 / DIY Nanosat MVP

**Revisión:** 2026-07-10
**Estado:** Active
**Trazabilidad:** `06_Costs/BOM_master.csv`, `00_MVP/MVP v2.2.md`, `SYSTEM_BASELINE.md`, `ADR-20260710-diy-low-cost-maker-latam-design-policy.md`

---

## 1) Propósito

Este documento es el overview humano de la BOM (Bill of Materials) maestra del proyecto.
La fuente de datos estructurada es `06_Costs/BOM_master.csv`.

---

## 2) Estructura de la BOM

La BOM maestra separa explícitamente por:

| Column | Descripción |
|---|---|
| `Subsystem` | Subsistema del sistema |
| `Stage` | **Bench** / **Flight-Like** / **Flight** / **EGSE** |
| `ItemClass` | Descripción genérica del ítem |
| `PreferredCandidate` | Candidato preferido actual |
| `AltCandidate` | Alternativa documentada |
| `Manufacturer` / `MPN` | Fabricante y número de parte (o TBD) |
| `Qty` | Cantidad |
| `Supplier` / `SupplierRegion` | Proveedor y región |
| `UnitCost` / `Currency` | Costo unitario |
| `QuoteDate` | Fecha de cotización |
| `LeadTime` | Tiempo de entrega estimado |
| `Risk` | Low / Medium / High |
| `Status` | Open / Partial / Closed |
| `Notes` | Notas de trazabilidad |

**Regla crítica:** No mezclar bench y flight-like en la misma fila.

---

## 2.1) Politica maker / LATAM / low cost

Para items nuevos o revisados, la BOM debe sostener la politica DIY low cost del proyecto:

- Preferir componentes maker/COTS con disponibilidad en Argentina o Latinoamerica para banco, FlatSat, EGSE y prototipos.
- Registrar proveedor, region, alternativa y riesgo de disponibilidad en cada fila relevante.
- Definir clases tecnicas cuando sea posible; evitar bloquear el diseno a un SKU unico de marketplace.
- Marcar como excepcion cualquier componente caro, exotico, EOL, import-only sin alternativa regional o dependiente de un unico proveedor.
- Mantener separada la ruta `Bench` / `Flight-Like` / `Flight`: un modulo maker comprado localmente puede cerrar evidencia de banco, pero no se convierte automaticamente en componente de vuelo.
- Para `Flight-Like` y `Flight`, agregar evidencia de ambiente, compliance, masa, consumo, termica, vibracion/outgassing cuando aplique.

Fuente: `08_Decisions/ADR-20260710-diy-low-cost-maker-latam-design-policy.md`.

---

## 3) Subsistemas cubiertos

| Subsistema | Stage activo | Notas |
|---|---|---|
| Structure/Thermal | Bench + Flight-Like | Estructura 1.5U TBD. |
| EPS | Bench (parcial) + Flight-Like (TBD) | `EPS_Bench1_1S` extendido para Gate IA-2: FPM bench + rail IA bench-only + `J_AI_PWR`. Referencia flight-like actual: **2S1P con 18650 de 3.0 Ah (~22 Wh)**. Ruta `2S2P` abierta como mitigación. Solar con IA: TBD. |
| OBC + Storage | Flight-Like (TBD) | STM32L4 clase. |
| COMMS UHF TTC | Flight-Like (TBD) | Hardware final TBD. OpenLST como base candidata. |
| LoRa RX orbital | Flight-Like (TBD) | SX1302-based concentrator en exploración. |
| GNSS | Flight-Like (TBD) | Módulo GNSS TBD. |
| Science Pack | Bench (parcial) + Flight-Like (TBD) | Sensores UV/ALS/MAG/temp TBD. |
| Ground Segment | EGSE (parcial) | Dashboard .NET activo. Estacion terrena dual-use SatNOGS/AUSTRALIS en diseno: SDR RX dedicado para SatNOGS/public beacon, SDR transceiver separado para modem AUSTRALIS, torre/mastil, linea coaxial UHF y estacion meteorologica local como candidatos abiertos. |
| Test/Tools | EGSE (parcial) | Fuente + multímetro existentes. |
| **AI Payload experimental** | **Bench + Flight-Like (TBD)** | **Familia CM5 adoptada. Bench: CM5 8 GB + carrier board COTS externa sobre `EPS_Bench1_1S` extendido. Flight-like: CM5 4 GB + eMMC.** |

---

## 4) Estado general de la BOM

- La mayoría de los ítems de Flight-Like y Flight tienen `Status = Open` y costo `TBD`.
- Los ítems de Bench tienen `Status = Partial` para los ya adquiridos.
- No se han inventado MPNs, precios ni fechas.

---

## 5) Alertas de supply chain

| Componente | Alerta |
|---|---|
| Qorvo RFFM6403 (FEM OpenLST original) | **EOL**. No usar como componente de diseño final. |
| CC1110 (base OpenLST) | Verificar disponibilidad antes de committer. |
| SAW filter STA1120A | Necesita variante centrada en 435-438 MHz. |

---

## 6) Cost drivers principales

1. Selección de UHF TTC (módulo/PA/filtros) + compliance.
2. Payload IA (CM5 + carrier + integración).
3. Delta bench-only de Gate IA-2 (`J_AI_PWR`, harness 5V, protección, `SW_AI`, interfaz y termometría).
4. Ensayos ambientales.
5. PCB assembly y re-trabajos (flight-like).
6. Importación/disponibilidad local.
7. Posible escalado EPS a `2S2P` y/o mitigación solar si Gate IA-2 lo exige.

---

## 7) Próximos pasos P2

1. Completar MPNs y cotizaciones para Flight-Like EPS y OBC.
2. Definir estrategia de front-end PA para TTC UHF.
3. Obtener cotizaciones de estructura 1.5U.
4. Completar líneas de COMMS y LoRa RX con candidatos evaluados.
5. Añadir fuente/fecha para cada rango de costo.
6. Separar BOM de EGSE para ensayos ambientales.
7. Ground Station: confirmar candidatos locales para SDR RX, PlutoSDR, torre/mastil, coaxial, rotor, LNA, filtros, estacion meteorologica local, T/R switch digital e interlocks.
8. **AI Payload:** cotizar bench y flight-like.
9. **EPS:** cotizar batería de referencia `2S1P` y dejar `2S2P` como ruta de mitigación abierta.
10. **Bench Gate IA-2:** mantener separado qué ítems son bench-only y no migran a `EPS_Flight_Like_2S_MPPT`.

---

## 8) Referencias cruzadas

- `06_Costs/BOM_master.csv`
- `04_Communications/ground_station_dual_use_satnogs_australis.md`
- `06_Costs/eps_bench1_1s_cost_model.md`
- `03_Power/EPS_Bench1_1S.md` §7
- `04_Communications/RF_ANALISYS_OPENLST.md` §11
- `SYSTEM_BASELINE.md`
- `architecture.md`
