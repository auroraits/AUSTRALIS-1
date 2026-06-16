# ADR-20260313-nodo-tipico-lora-clase

- **Fecha:** 2026-03-13
- **Estado:** Accepted

---

## Contexto

La documentación existente (en particular `04_Communications/link_budget_lora_uplink_preliminary.md` y `04_Communications/uplink_lora_slotted_protocol.md`) referenciaba módulos de mercado específicos (RFM95W, SX1276) como si fueran requisitos normativos del "nodo típico". Esto creaba dependencia de SKUs específicos y no capturaba correctamente el objetivo: cualquier nodo de bajo costo de clase equivalente que cumpla características eléctricas y de RF similares.

---

## Decisión

El "nodo típico LoRa terrestre" para el uplink del MVP se define como **clase de nodo**, no como SKU de mercado específico.

**Clase de nodo:**
- Banda terrestre objetivo: `915–928 MHz` (AU915 o equivalente)
- Radio: clase `SX1262` o `SX1276` o equivalente
- Microcontrolador: clase `ESP32-S3` o equivalente
- Potencia TX típica: `+20 a +21 dBm`
- Antena: simple, `0–2 dBi`; sin antena direccional
- Cristal: comercial típico, `±10 ppm`
- Sin PA (Power Amplifier) externo
- Sin LNA (Low-Noise Amplifier) externo
- Sin TCXO (Temperature-Compensated Crystal Oscillator)

**Referencias de mercado** (ejemplos de la clase, no normativos): módulos Heltec ESP32+SX1262, RFM95W, SX1276-based, y equivalentes.

**Parámetros TBD (no cerrados por esta ADR):**
- Elevación mínima operativa.
- Canalización exacta dentro de 915–928 MHz.
- BW definitivo (125 vs 250 kHz).
- Criterio numérico final de aceptación de uplink.

**Baseline operativo mantenido:**
- Modo B2 slotted / pass-aware.
- Predicción de pasadas con TLE + SGP4.

---

## Alternativas consideradas

1. **Fijar SKU específico (RFM95W)**: rechazada. Crea dependencia de producto de mercado que puede descontinuarse o no estar disponible localmente.
2. **No definir clase**: rechazada. Sin definición, no hay punto de referencia para link budget y validación.
3. **Clase de nodo sin límites técnicos**: rechazada. Demasiado vaga para link budget.
4. **Clase de nodo con parámetros clave** (elegida): balance entre especificidad y flexibilidad.

---

## Tradeoffs / riesgos

- A favor: mayor flexibilidad de implementación; no se depende de un SKU de mercado que puede cambiar de disponibilidad o precio.
- En contra: la validación debe realizarse con hardware específico de la clase; los resultados dependen de qué módulo se usa en la práctica.
- Riesgo residual: diferencias de rendimiento entre módulos de la misma clase (±1-2 dB de sensibilidad). Mitigación: documentar el módulo específico usado en cada ensayo.

---

## Implicancias (archivos actualizados)

- `04_Communications/rf_subsystem_overview.md` — §4 actualizado con definición de clase.
- `04_Communications/link_budget_lora_uplink_preliminary.md` — §2.0 actualizado con descripción de clase.
- `04_Communications/uplink_lora_slotted_protocol.md` — §2 actualizado con descripción de clase.
- `AGENTS.md` — §11 política nodo típico.
- `SYSTEM_BASELINE.md` — §3.3 actualizado.
- `01_Mission/requirements_matrix.md` — MIS-REQ-14 agregado.
