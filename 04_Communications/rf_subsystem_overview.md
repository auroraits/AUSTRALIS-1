# RF Subsystem Overview — AUSTRALIS-1 / DIY Nanosat MVP

**Revisión:** 2026-03-14
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md`, `08_Decisions/ADR-20260220-lora-uplink-slotted-mode-b-and-concentrator-rx.md`, `08_Decisions/ADR-20260218-uhf-link-budget-preliminary.md`

## 1) Arquitectura RF del satélite
El subsistema RF del MVP utiliza dos canales:
- **LoRa RX 915 MHz** para uplink de nodos IoT en tierra (RX-only en satélite).
- **UHF TRX 435 MHz** para downlink/TTC con estación terrena.

Decisión P1 (ver ADR): para maximizar probabilidad de uplink con nodos típicos, el RX orbital se explora como **LoRa concentrator** y el acceso múltiple se hace por **slotting (modo B2)**.

Nota de integración EPS: el escenario de sizing para un concentrator COTS de clase SX1303 HAT usa **0.495 W en RX** (99 mA @ 5 V con GNSS ON) y exige **OFF real** fuera de ventana; ver `03_Power/Power Budget.md` y `07_Risk/comms_concentrator_integration_risk.md`. Esto no selecciona hardware de vuelo ni habilita TX LoRa desde órbita.

## 2) Arbitraje de downlink y prioridad de tráfico (permanente)
El downlink UHF es gestionado por Downlink Manager en OBC con colas:
- `HOUSEKEEPING`
- `COMMAND_ACK`
- `AI_BEHAVIOR_LOG`
- `LORA_LOG`
- `SCIENCE`
- `OPTIONAL_PAYLOAD`

Reglas:
- Prioridad estricta para `HOUSEKEEPING` y `COMMAND_ACK` en todos los modos.
- `AI_BEHAVIOR_LOG` es la cola best-effort de mayor prioridad científica.
- `LORA_LOG`, `SCIENCE` y cola opcional operan en best-effort por cuota.
- En SAFE se limita a housekeeping/comandos.

## 3) Uplink mínimo de comando (permanente)
Comandos mínimos soportados en TTC:
- `SET_MODE`
- `POWER_SET`
- `DL_SELECT`
- `DL_SET_LIMITS`
- `REQUEST_STATUS`
- `ABORT`

## 4) LoRa Uplink

| Parámetro | Valor |
|---|---|
| Frecuencia terrestre | 915–928 MHz (AU915 o equivalente, Argentina) |
| Modulación | LoRa |
| SF/BW | SF12 / BW **TBD** — BW250 candidato preferente |
| Modo en satélite | **RX-only** (sin TX ISM desde órbita en MVP) |
| Ventanas de operación | Solo durante pasadas previstas |
| RX orbital explorado | Concentrator class como P1, con modo degradado single-channel si potencia/EMI no cierran |
| Antena candidata | Patch o dipolo impreso |

### 4.1 Nodo típico terrestre (clase de nodo — no SKU)

El nodo típico objetivo se define como **clase**, no como SKU de mercado específico:

| Parámetro | Valor de clase |
|---|---|
| Radio | Clase SX1262 o SX1276 o equivalente |
| MCU | Clase ESP32-S3 o equivalente |
| Potencia TX | +20 a +21 dBm |
| Antena | Simple, 0–2 dBi |
| Cristal | Comercial típico, ±10 ppm |
| PA externo | No |
| LNA externo | No |
| Antena direccional | No |
| TCXO | No asumido |

Referencias de clase (ejemplos, no normativas): módulos Heltec, RFM95W, SX1262-based y similares.

Referencia: `08_Decisions/ADR-20260313-nodo-tipico-lora-clase.md`

**Parámetros TBD:** elevación mínima operativa, canalización exacta dentro de 915–928 MHz, BW definitivo, criterio de aceptación numérico.

**Nota de factibilidad:** con nodos de clase típica, el enlace puede quedar al borde incluso a zenith. La estrategia realista es operar solo en elevaciones altas y **reducir colisiones por slotting** (modo B2).

## 5) UHF Downlink/TTC

| Parámetro | Valor |
|---|---|
| Frecuencia | 435 MHz |
| Modulación | FSK |
| Data rate | 1 200 bps |
| Potencia TX objetivo | 500 mW RF |
| Potencia eléctrica estimada TX | ~1.5 W (preliminar; ver CONF-01 en `architecture.md`) |
| Integridad | Framing + CRC + secuencia |
| Tramas | BEACON / AI_BEHAVIOR_LOG / SCIENCE_SUMMARY / LORA_LOG / ACK-NACK |

**Máscara de elevación operativa (provisional):** la validación nominal del downlink UHF se establece provisionalmente para elevaciones **≥20°**. Operación a <20° es experimental/oportunista. A 10° el margen teórico de papel es solo **+1 dB**.

## 6) Selección de módulo UHF (TBD)

Candidatos documentados (no baseline final):
- CC1110 (base OpenLST) — ver `04_Communications/RF_ANALISYS_OPENLST.md`
- AX5043
- CC1101 + PA externo
- Si4463

**Hardware TTC UHF final:** TBD. Requiere ADR de adopción cuando se tome la decisión.
**OpenLST:** candidato técnico en análisis. No copiar "tal cual" (componente RFFM6403 es EOL).

## 7) Antena del satélite
- Alternativa base: antena 1/4 onda deployable.
- Alternativa secundaria: dipolo.
- Restricción principal: volumen mecánico disponible en 1.5U y compatibilidad con despliegue.

## 8) EMC / separación RF interna
- Mantener separación física y de layout entre cadenas LoRa y UHF.
- Controlar retorno de masa común y rutas de corriente de TX.
- Evitar acoplamientos con fuentes switching del EPS y con el payload IA.

## 9) Estado actual — inmadurez de hardware RF

> **Brecha hardware/documentación:** la madurez documental del subsistema COMMS supera significativamente la madurez del hardware RF real.

- **Módulo UHF orbital definitivo: TBD** — no seleccionado; sin esquemático KiCad de RF orbital funcional.
- **LoRa RX orbital (concentrator o módulo): TBD** — no seleccionado.
- **PCB RF orbital (TTC UHF + LoRa RX):** esquemático KiCad esencialmente **placeholder**.
- Toda la documentación de link budget, protocolo y arquitectura RF describe el **diseño objetivo**, no el hardware existente.
- Gate de madurez de hardware RF: Gate C (TTC UHF dev base cerrado).

<!-- FEATURE:PHOTO_DEMO START -->

## 10) [PHOTO_DEMO] Integración opcional de tráfico
- La cola `OPTIONAL_PAYLOAD` del Downlink Manager se asigna al catálogo/transferencia de [PHOTO_DEMO].
- Siempre best-effort, con cuota por pasada configurable con `DL_SET_LIMITS`.
- Transferencia por chunks reanudables, posterior a selección uplink de imagen.

<!-- FEATURE:PHOTO_DEMO END -->

## 11) Referencias cruzadas
- `04_Communications/link_budget_uhf_preliminary.md`
- `08_Decisions/ADR-20260212-telemetry-bench-433mhz.md`
- `08_Decisions/ADR-20260218-downlink-arbitration-and-subsystem-power-framework.md`
- `08_Decisions/ADR-20260314-mission-redef-ai-primary.md`
