# Link Budget UHF bidireccional preliminar — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Preliminary — cálculo de factibilidad, no evidencia de hardware
**Trazabilidad:** `08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`, `04_Communications/regulatory_gate_rf.md`, `docs/COMMS/rf_calculations.py`

## 1) Alcance y límites

Este documento calcula por separado:

- downlink satélite → tierra;
- uplink de Telemetría, Seguimiento y Comando (TTC) tierra → satélite.

No demuestra disponibilidad de servicio, Bit Error Rate (BER), Packet Error
Rate (PER), cumplimiento espectral ni compatibilidad SatNOGS. La potencia,
sensibilidad, patrón de antena y pérdidas siguen sin medirse en el hardware
integrado.

La frecuencia no es `435.000 MHz`. Es una **asignación coordinada TBD dentro de
435–438 MHz**, sujeta a ENACOM, coordinación IARU y trámite UIT. Para que el
cálculo sea reproducible se usa `436.5 MHz` únicamente como frecuencia de
referencia; no es una asignación ni una autorización.

## 2) Geometría correcta

Para una Tierra esférica de radio \(R_E=6371\,km\), altitud \(h\) y elevación
\(e\), la distancia oblicua es:

\[
d=\sqrt{(R_E+h)^2-(R_E\cos e)^2}-R_E\sin e
\]

La Free-Space Path Loss (FSPL) se calcula como:

\[
FSPL[dB]=32.44+20\log_{10}(f_{MHz})+20\log_{10}(d_{km})
\]

Resultados a 436.5 MHz:

| Altitud | Elevación | Distancia oblicua | FSPL |
|---:|---:|---:|---:|
| 550 km | 10° | 1815.1 km | 150.42 dB |
| 550 km | 20° | 1293.6 km | 147.48 dB |
| 550 km | 30° | 992.8 km | 145.18 dB |
| 550 km | 90° | 550.0 km | 140.05 dB |
| 600 km | 10° | 1931.6 km | 150.96 dB |
| 600 km | 20° | 1392.2 km | 148.11 dB |
| 600 km | 30° | 1075.1 km | 145.87 dB |
| 600 km | 90° | 600.0 km | 140.80 dB |
| 650 km | 10° | 2044.7 km | 151.45 dB |
| 650 km | 20° | 1488.8 km | 148.70 dB |
| 650 km | 30° | 1156.4 km | 146.50 dB |
| 650 km | 90° | 650.0 km | 141.50 dB |

El valor histórico de 2500 km a 550 km/10° era incorrecto. Los cálculos y
regresiones están en `docs/COMMS/rf_calculations.py`.

## 3) Downlink — caso de referencia, no validado

### 3.1 Supuestos aritméticos

| Término | Valor de papel | Estado |
|---|---:|---|
| Potencia RF satelital | +27 dBm | Objetivo; medir conducted y EIRP |
| Ganancia TX satelital | 0 dBi | Hipótesis; patrón integrado TBD |
| Ganancia RX terrestre | +10 dBi | Hipótesis; patrón y pointing TBD |
| Pérdidas agrupadas | 3 dB | Placeholder, no presupuesto cerrado |
| Sensibilidad terrestre | −120 dBm | Hipótesis; medir a PER objetivo |
| Altitud de referencia | 600 km | Punto de cálculo, órbita final no congelada |

La convención de signos es:

\[
P_{RX}=P_{TX}+G_{TX}+G_{RX}-L_{FS}-L_{misc}
\]

donde todas las pérdidas \(L\) son magnitudes positivas.

### 3.2 Resultado de papel a 600 km

| Elevación | FSPL | Potencia recibida | Margen contra −120 dBm |
|---:|---:|---:|---:|
| 10° | 150.96 dB | −116.96 dBm | +3.04 dB |
| 20° | 148.11 dB | −114.11 dBm | +5.89 dB |
| 30° | 145.87 dB | −111.87 dBm | +8.13 dB |
| 90° | 140.80 dB | −106.80 dBm | +13.20 dB |

Por lo tanto, la afirmación anterior de “~+9 dB a 20°” era incorrecta: bajo
estos supuestos el resultado es **+5.9 dB**, antes de incertidumbres no
asignadas. La máscara de 20° solo puede mantenerse como máscara de
planificación provisional, no como garantía ni criterio verificado.

## 4) Uplink TTC — presupuesto que faltaba

El uplink requiere presupuesto propio porque el transmisor terrestre, el
receptor orbital y sus patrones no son los mismos del downlink.

### 4.1 Caso de referencia simétrico

Hasta seleccionar hardware, se conserva un caso aritmético explícito:

| Término | Valor de papel | Evidencia requerida |
|---|---:|---|
| Potencia TX terrestre | +27 dBm | Medición en puerto y límite autorizado |
| Ganancia TX terrestre | +10 dBi | Patrón/calibración de la antena |
| Ganancia RX satelital | 0 dBi | Patrón integrado en actitud nominal/degradada |
| Pérdidas agrupadas | 3 dB | Ledger de cable, polarización, pointing y body loss |
| Sensibilidad orbital | −120 dBm | Medición a BER/PER y temperatura definidos |

Con esos valores el resultado numérico coincide con la tabla de §3.2, pero
esto **no demuestra simetría del enlace real**. En particular deben cerrarse:

- EIRP permitido de la estación;
- sensibilidad del receptor orbital con el front-end y filtro finales;
- pérdida por orientación corporal y nulo de antena;
- ruido/desensibilización durante operación integrada;
- probabilidad de recepción y PER de comando;
- ACK autenticado de cada comando aceptado o rechazado.

No se considera verificable ningún comando crítico hasta cerrar este uplink.

## 5) Pérdidas e incertidumbre que deben presupuestarse

No se permite esconder todos los efectos dentro de “3 dB”. El ledger final
debe separar, con nominal, peor caso e incertidumbre:

- cable, conectores, switch T/R, filtro y mismatch;
- polarización;
- pointing y patrón de la estación;
- patrón realizado del satélite, body loss y detuning;
- tolerancia de potencia del PA con tensión y temperatura;
- ruido de implementación, Noise Figure (NF) y temperatura de antena;
- fading, interferencia, Doppler residual y error de osciladores;
- degradación de hardware y margen de implementación.

La sensibilidad debe derivarse o medirse para una waveform exacta, ancho de
filtro, BER/PER objetivo, tamaño de frame, Forward Error Correction (FEC) y
confianza estadística. `−120 dBm` no es todavía un requisito verificable.

## 6) Doppler y waveform provisional

A 438 MHz y una cota de velocidad radial de 7.7 km/s:

\[
|\Delta f| \leq f\,|v_r|/c \approx 11.25\,kHz
\]

La asignación coordinada debe dejar guardas para Doppler y tolerancia del
oscilador. El perfil de ingeniería conserva:

- 2-FSK;
- 1200 bit/s;
- framing versionado y CRC para detección de errores;
- autenticación criptográfica y anti-replay para comandos.

Siguen `TBD` hasta medición y decisión:

- desviación FSK y occupied bandwidth;
- preámbulo, sync word, whitening y line coding;
- FEC/interleaver;
- ancho de filtro, rango de adquisición y Automatic Frequency Control (AFC);
- precompensación Doppler en tierra;
- MTU, fragmentación, ARQ y timeout.

El diseño debe demostrar adquisición con rampa Doppler orbital más error
combinado de osciladores y cumplir el ancho ocupado autorizado. En el marco
amateur-satellite argentino, el límite aplicable a digimodos y la frecuencia
exacta deben confirmarse en el expediente regulatorio.

## 7) Antena y actitud

`0 dBi` es una hipótesis de cálculo, no un patrón isotrópico real. Un monopolo
normal a la cara nadir presenta un nulo axial aproximadamente hacia la estación
en pasadas de alta elevación. Antes de seleccionar antena se debe:

1. definir los frames mecánico, corporal y de antena;
2. comparar dipolo, monopolo tangencial y alternativas desplegables;
3. simular el patrón 3D con estructura, paneles, harness y radiales;
4. medir realized gain, polarización y detuning en modelo integrado;
5. propagar el patrón por actitud nominal, error, tumble y modo seguro.

El link budget final debe usar el percentil/pérdida de patrón correspondiente,
no una ganancia escalar de 0 dBi.

## 8) Criterios de cierre

Este análisis puede pasar de `Preliminary` a evidencia de diseño solo si:

- existe asignación/coordinación y autorización aplicable;
- downlink y uplink tienen waveform y hardware identificados;
- EIRP, sensibilidad, patrón y pérdidas están medidos;
- BER/PER y disponibilidad tienen criterio previo y tamaño muestral;
- se ejecutan Doppler, temperatura, coexistencia y pruebas OTA integradas;
- los resultados se guardan con configuración, calibraciones, raw data y hash.

## 9) Referencias

- `04_Communications/regulatory_gate_rf.md`
- `04_Communications/uhf_command_security_protocol.md`
- `04_Communications/rf_subsystem_overview.md`
- `docs/COMMS/rf_calculations.py`
- `docs/COMMS/uhf_ttc_bench_testing_plan.md`
