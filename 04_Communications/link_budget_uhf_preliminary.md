# Link Budget UHF Preliminar — AUSTRALIS-1 / DIY Nanosat MVP

**Fecha de revisión:** 2026-03-14

## 1) Objetivo
Establecer el link budget preliminar del downlink UHF para el MVP.

## 2) Supuestos de diseño

| Parámetro | Valor | Nota |
|---|---|---|
| Frecuencia | 435 MHz | Downlink MVP bloqueado |
| Potencia TX RF | 500 mW (+27 dBm) | Objetivo preliminar |
| Órbita de referencia | 550 km zenith | Supuesto de diseño |
| Rango oblicuo peor caso | ~2 500 km | Elevación mínima 10° |
| Antena satélite | 0 dBi | 1/4 onda o dipolo simple |
| Antena tierra | +10 dBi | Yagi estación Buenos Aires |
| Pérdidas misceláneas | -3 dB | Polarización, cableado, implementación |
| Sensibilidad RX tierra | -120 dBm | Estimación conservadora (FSK 1k2) |

## 3) Cálculo de Free-Space Path Loss
Fórmula:

\[ FSPL = 20\log_{10}\left(\frac{4\pi d}{\lambda}\right) \]

Con:
- \( f = 435\,\text{MHz} \Rightarrow \lambda = c/f \approx 0.689\,\text{m} \)
- Zenith: \( d = 550\,\text{km} = 550000\,\text{m} \)
- Elevación 10°: \( d \approx 2500\,\text{km} = 2500000\,\text{m} \)

Resultados aproximados:
- FSPL(550 km) ≈ **140 dB**
- FSPL(2500 km) ≈ **153 dB**

## 4) Tabla de link budget

| Parámetro | Símbolo | Valor | Unidad | Notas |
|---|---|---:|---|---|
| Potencia TX | Ptx | +27 | dBm | 500 mW RF |
| Ganancia antena TX satélite | Gtx | 0 | dBi | 1/4 onda |
| Ganancia antena RX tierra | Grx | +10 | dBi | Yagi |
| Pérdidas misceláneas | Lmisc | -3 | dB | Cableado/polarización |
| FSPL zenith | Lfs,90 | -140 | dB | 550 km |
| FSPL 10° | Lfs,10 | -153 | dB | ~2500 km |
| Sensibilidad RX | Srx | -120 | dBm | FSK 1k2 (estimado) |

## 5) Resultados por elevación

| Elevación | Distancia slant aprox. | FSPL (dB) | Potencia recibida (dBm) | Margen vs -120 dBm |
|---:|---:|---:|---:|---:|
| 10° | 2500 km | 153 | -119 | +1 dB |
| 30° | 1100 km | 145 | -111 | +9 dB |
| 90° | 550 km | 140 | -106 | +14 dB |

Cálculo de potencia recibida:
\[ P_{rx} = P_{tx} + G_{tx} + G_{rx} - FSPL - L_{misc} \]

## 6) Resultado del cálculo de papel
Con 500 mW RF (+27 dBm), el enlace de papel muestra **+1 dB a 10°** (2500 km) y margen mayor en elevaciones medias/altas.

**Este +1 dB NO es un criterio nominal de operación.** Es un margen de papel esencialmente inoperable con pérdidas reales:
- Pérdidas por polarización / tumbling del satélite: 0–3+ dB.
- Body loss / detuning de antena en satélite: 1–5 dB.
- Cableado + LNA + setup de estación terrena: 0–3 dB.
- Eficiencia real del PA (diferente a la hipótesis de 500 mW RF): variable (ver CONF-01).

**Regla operativa:** tratar la operación a **<20°** como experimental/oportunista, no como criterio nominal de éxito.

## 6.1 Sensibilidad (qué hace caer el margen)
Pérdidas típicas a considerar (orden de magnitud):
- mismatch de polarización (lineal vs circular / orientación variable): 0–3+ dB
- body loss / detuning en satélite: 1–5 dB
- cableado/conectores tierra + LNA/SDR setup: 0–3 dB

Estas pérdidas no medidas implican que el enlace a 10° puede ser **negativo** con hardware real. La operación a 10° es experimental/oportunista.

## 6.2 Máscara de elevación operativa (criterio provisional)

> **Este criterio es provisional** — recomendación conservadora basada en análisis de papel. Debe confirmarse o revisarse tras medir el hardware TX candidato (Gate C). Ver `ADR-20260313-uhf-downlink-operational-mask.md`.

| Rango de elevación | Tratamiento operativo |
|---|---|
| **≥20°** | Zona nominal para validación inicial y criterio de éxito de Gate C |
| **20°–25°** | Zona conservadora/prudente recomendada para primeras operaciones |
| **<20°** | Experimental / oportunista — **no** criterio nominal de éxito del MVP |

**Justificación:** la zona ≥20° tiene ~+9 dB de margen teórico, mucho más robusto a incertidumbres de implementación que el +1 dB teórico a 10°.

**Próximo paso:** Confirmar o revisar esta máscara tras medir con hardware TX real en Gate C.

## 7) Próximos pasos
1. Seleccionar módulo transceptor UHF de vuelo (TBD).
2. Medir potencia RF y eficiencia real de PA en banco.
3. Medir sensibilidad real del receptor de estación terrena.
4. Refinar pérdidas reales de antena/cableado/polarización.
5. Validar perfil de margen por elevación con simulación orbital.
6. Definir una elevación mínima operacional inicial (ej. 20°) hasta cerrar mediciones.

## 8) Referencias
- `08_Decisions/ADR-20260218-uhf-link-budget-preliminary.md`
- `00_MVP/MVP v2.2.md`

## 9) Integración con arbitraje y uplink mínimo
- El cálculo de margen se aplica al tráfico priorizado del Downlink Manager (`HOUSEKEEPING` y `COMMAND_ACK`) como garantía de servicio.
- El resto de colas opera por cuota best-effort con el siguiente orden: `AI_BEHAVIOR_LOG`, `LORA_LOG`, `SCIENCE`, `OPTIONAL_PAYLOAD`.
- El uplink mínimo de control (`SET_MODE`, `POWER_SET`, `DL_SELECT`, `DL_SET_LIMITS`, `REQUEST_STATUS`, `ABORT`) se considera tráfico crítico de comando/ACK.

<!-- FEATURE:PHOTO_DEMO START -->

## 10) [PHOTO_DEMO] Nota de presupuesto de enlace opcional
- [PHOTO_DEMO] utiliza exclusivamente cuota best-effort de `OPTIONAL_PAYLOAD`.
- Si no hay margen de enlace en una pasada, se pospone transferencia sin degradar housekeeping/comandos.

<!-- FEATURE:PHOTO_DEMO END -->