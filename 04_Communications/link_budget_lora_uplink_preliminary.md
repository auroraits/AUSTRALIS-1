# Link Budget LoRa Uplink Preliminar (915 MHz) — AUSTRALIS-1 / DIY Nanosat MVP

**Fecha de revisión:** 2026-03-14
**Estado:** preliminar (análisis de factibilidad; requiere medición/decisión)

## 1) Objetivo
Cuantificar, de forma preliminar, si el objetivo secundario de misión “**nodo IoT (Buenos Aires, LoRa 915) → satélite (RX)**” es realista bajo supuestos típicos, y qué márgenes/condiciones se requieren.

> Nota: este documento es **uplink** (tierra → satélite). El downlink UHF se trata en `04_Communications/link_budget_uhf_preliminary.md`.

## 2) Supuestos de diseño (TBD donde aplique)

### 2.0 Nodo “típico” objetivo (clase de nodo — no SKU específico)

El nodo objetivo se define como **clase**, sin fijar SKU de mercado como requisito normativo. Ver `08_Decisions/ADR-20260313-nodo-tipico-lora-clase.md`.

Clase de nodo de referencia para este link budget:

| Parámetro | Valor de clase | Nota |
|---|---:|---|
| Frecuencia terrestre | 915–928 MHz | AU915 o equivalente (Argentina) |
| Órbita de referencia | 550 km zenith | Supuesto de diseño |
| Rango oblicuo peor caso | ~2 500 km | Elevación mínima 10° (geométrico) |
| Potencia TX (nodo) | +20 a +21 dBm | Clase típica sin PA externo |
| Antena TX tierra (nodo) | 0–2 dBi | Monopolo/dipolo; sin antena direccional |
| Antena RX satélite | 0–2 dBi | Dipolo/monopolo/patch simple |
| Cristal | ±10 ppm | Comercial típico; sin TCXO |
| Pérdidas misceláneas | 4–10 dB | Polarización, body loss, desintonía, implementación |
| LoRa BW | **TBD** (125 kHz o 250 kHz) | **BW definitivo TBD hasta Gate B.** BW250 es el **candidato preferente** por robustez frente a CFO+Doppler. |
| LoRa SF | SF12 (caso robusto) | Para sensibilidad máxima |
| Sensibilidad RX (referencia típica) | ~−137 dBm (SF12, BW125) | Orden de magnitud de datasheets SX127x; **medir/confirmar** |

Ejemplos de clase (referencia comercial, no normativa): RFM95W, SX1276-based, módulos Heltec ESP32+SX1262, y equivalentes.

### 2.1 Free-Space Path Loss (FSPL)
Usando la aproximación estándar:

\[ FSPL(dB) = 32.44 + 20\log_{10}(f_{MHz}) + 20\log_{10}(d_{km}) \]

Para 915 MHz:
- FSPL(550 km) ≈ **146.5 dB**
- FSPL(2500 km) ≈ **159.6 dB**

## 3) Cálculo (casos)

Ecuación:
\[ P_{rx} = P_{tx} + G_{tx} + G_{rx} - FSPL - L_{misc} \]

### 3.1 Caso A — “Nodo mínimo / legacy”
- Ptx = +14 dBm
- Gtx = +0 dBi
- Grx = +0 dBi
- Lmisc = 6 dB (polarización + body loss + implementación)

> Nota: este caso representa un nodo con potencia mínima (**+14 dBm**), por debajo de la clase de nodo objetivo (**+20 a +21 dBm**). Se conserva como referencia de peor caso extremo.

| Elevación | FSPL (dB) | P_rx (dBm) |
|---:|---:|---:|
| 90° (550 km) | 146.5 | **−138.5** |
| 10° (2500 km) | 159.6 | **−151.6** |

**Lectura:**
- A zenith queda **en el borde** incluso para SF12 (~−137 dBm típico). Sin margen.
- A 10° es **inviable** con nodo mínimo.

### 3.2 Caso B — “Nodo típico + módulo más fuerte”
- Ptx = +20 dBm
- Gtx = +2 dBi
- Grx = +0 dBi
- Lmisc = 6 dB

| Elevación | FSPL (dB) | P_rx (dBm) |
|---:|---:|---:|
| 90° (550 km) | 146.5 | **−130.5** |
| 10° (2500 km) | 159.6 | **−143.6** |

**Lectura:**
- Zenith: factible con margen (si la sensibilidad real es ~−137 dBm).
- 10°: sigue quedando muy lejos.

### 3.3 Caso C — “Gateway dedicado” (más realista para objetivo orbital)
Ejemplo:
- Ptx = +27 dBm (0.5 W) (TBD legal/operativo)
- Gtx = +10 dBi (Yagi)
- Grx = +0 dBi
- Lmisc = 6 dB

| Elevación | FSPL (dB) | P_rx (dBm) |
|---:|---:|---:|
| 90° (550 km) | 146.5 | **−115.5** |
| 10° (2500 km) | 159.6 | **−128.6** |

**Lectura:**
- Esto cierra con margen amplio incluso a elevaciones bajas.
- Implica que el “nodo IoT” se comporta más como una **estación/gateway dedicado**.

## 4) Implicancias para el MVP

### 4.1 Riesgo principal
El criterio secundario de éxito “≥10 paquetes LoRa originados en Buenos Aires” **no está garantizado** si se interpreta “nodo” como dispositivo LoRa típico y si se pretende operar a elevaciones bajas.

Para “nodos típicos”, el diseño realista es:
- intentar recepción **solo** en la porción alta de la pasada (cerca de zenith),
- maximizar robustez LoRa y usar repetición de tramas,
- recuperar dB con una antena bien implementada (sin volverlo direccional).

### 4.2 Doppler + error de cristal (impacto en decisión de BW)
Orden de magnitud para 915 MHz:
- Doppler LEO (v≈7.5 km/s): **~±23 kHz**.
- Error de cristal ±10 ppm: **±9 kHz**.

Combinados, el offset puede ser del orden de **~30 kHz** durante una pasada real.

Implicancias:
- **BW125**: frágil sin calibración adecuada del hardware. **Solo adoptar si la evidencia de banco/campo lo respalda.**
- **BW250**: mayor tolerancia al offset combinado (a costa de ~3 dB de sensibilidad). **Candidato preferente** mientras no haya evidencia que respalde BW125.
- **BW definitivo: TBD** hasta Gate B.
- Medida complementaria: **diversidad de frecuencia por firmware** puede ayudar en ambos casos.

### 4.3 Opciones de mitigación (permitidas sin “gateway dedicado”)
1) **Elevar elevación mínima operacional**.
2) **Mejorar antena del nodo** (sin direccional).
3) **Firmware (nodo):** SF alto, payload corto, preámbulo largo, repetición de paquetes.
4) **Firmware (satélite RX):** ventanas de escucha centradas en máxima elevación.

### 4.4 Alternativa (si no cierra)
Si tras cerrar números/mediciones no hay margen con nodos típicos, la alternativa es redefinir el “nodo” como estación/gateway dedicado o cambiar el uplink.

## 5) Próximos pasos (P1)
1. Seleccionar radio LoRa candidato y fijar una tabla de sensibilidad real por BW/SF/CR.
2. Definir legal/operativo: potencia y antena del “nodo” (o gateway) en Argentina (ENACOM).
3. Validar en banco sensibilidad RX real, tolerancia a CFO/Doppler y tasa de paquetes esperable por ventana.
4. Decidir/actualizar requisitos de misión para que el criterio secundario de éxito sea verificable y realista.

## 6) Referencias cruzadas
- `01_Mission/mission_definition.md`
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/link_budget_uhf_preliminary.md`