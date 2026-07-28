# Link Budget LoRa uplink preliminar — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Preliminary — factibilidad técnica condicionada; operación no autorizada
**Trazabilidad:** `08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`, `04_Communications/regulatory_gate_rf.md`, `docs/COMMS/rf_calculations.py`

## 1) Condición regulatoria previa

Este cálculo no autoriza transmisiones. Que el satélite sea `RX-only` en
915–928 MHz evita una emisión orbital en esa banda, pero **no autoriza** que un
nodo terrestre emita deliberadamente Tierra→espacio.

Hasta obtener dictamen escrito de ENACOM que identifique servicio, banda,
dirección, potencia, antena y condiciones:

- el enlace LoRa orbital se considera **no autorizado**;
- solo se permiten ensayos conducidos, en caja apantallada o bajo autorización
  experimental específica;
- B1/B2 y el criterio de paquetes desde Buenos Aires no son operables.

Ver `04_Communications/regulatory_gate_rf.md`.

## 2) Propósito técnico

Cuantificar el enlace de papel para una clase de nodo, sin seleccionar SKU ni
receptor orbital. Los resultados no representan sensibilidad del concentrador
SX1302/SX1303, patrón de antena ni Packet Delivery Ratio (PDR) medidos.

La frecuencia exacta es `TBD` y depende del cierre regulatorio. Se usa
`915.0 MHz` solo como referencia numérica; no es un canal adoptado.

## 3) Geometría y FSPL

Se usa la geometría esférica y ecuaciones reproducibles de
`docs/COMMS/rf_calculations.py`.

| Altitud | Elevación | Distancia oblicua | FSPL a 915 MHz |
|---:|---:|---:|---:|
| 550 km | 10° | 1815.1 km | 156.85 dB |
| 550 km | 20° | 1293.6 km | 153.90 dB |
| 550 km | 30° | 992.8 km | 151.61 dB |
| 550 km | 90° | 550.0 km | 146.48 dB |
| 600 km | 10° | 1931.6 km | 157.39 dB |
| 600 km | 20° | 1392.2 km | 154.54 dB |
| 600 km | 30° | 1075.1 km | 152.30 dB |
| 600 km | 90° | 600.0 km | 147.23 dB |
| 650 km | 10° | 2044.7 km | 157.88 dB |
| 650 km | 20° | 1488.8 km | 155.13 dB |
| 650 km | 30° | 1156.4 km | 152.93 dB |
| 650 km | 90° | 650.0 km | 147.93 dB |

El valor histórico de 2500 km a 550 km/10° era incorrecto.

## 4) Clase de nodo y receptor

| Parámetro | Clase de referencia | Estado |
|---|---:|---|
| Potencia TX | +20 a +21 dBm | Sin PA externo; medir |
| Ganancia TX | 0 a +2 dBi | Antena simple; medir patrón |
| Cristal | ±10 ppm | Sin asumir TCXO |
| Ganancia RX orbital | 0 a +2 dBi | Hipótesis; patrón integrado TBD |
| Pérdidas | 4 a 10 dB | Rango de estudio, no ledger validado |
| PHY | SF12, CR 4/5, header explícito, CRC | Candidato de ensayo |
| BW | 125 o 250 kHz | TBD por banco y autorización |

Las sensibilidades `−137 dBm` (BW125) y `−134 dBm` (BW250) se conservan
únicamente como referencias de orden de magnitud de transceptores LoRa. No se
pueden atribuir al concentrador orbital: deben medirse con el módulo,
front-end, filtro, reloj, temperatura y criterio PDR exactos.

## 5) Casos de papel a 600 km

Ecuación:

\[
P_{RX}=P_{TX}+G_{TX}+G_{RX}-FSPL-L_{misc}
\]

### 5.1 Caso nominal explícito

Supuestos: `Ptx=+20 dBm`, `Gtx=0 dBi`, `Grx=0 dBi`, `Lmisc=6 dB`.

| Elevación | Potencia recibida | Margen BW125 vs −137 | Margen BW250 vs −134 |
|---:|---:|---:|---:|
| 10° | −143.39 dBm | −6.39 dB | −9.39 dB |
| 20° | −140.54 dBm | −3.54 dB | −6.54 dB |
| 30° | −138.30 dBm | −1.30 dB | −4.30 dB |
| 90° | −133.23 dBm | +3.77 dB | +0.77 dB |

Este caso solo cierra sobre el papel cerca de zenith y con la sensibilidad de
referencia; no incluye confianza ni variación de patrón.

### 5.2 Envolvente favorable/adversa a 20°

| Caso | Ptx | Gtx | Grx | Pérdidas | Prx | Margen BW125 | Margen BW250 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Favorable | +21 | +2 | +2 | 4 | −133.54 | +3.46 | +0.46 |
| Nominal | +20 | 0 | 0 | 6 | −140.54 | −3.54 | −6.54 |
| Adverso | +20 | 0 | 0 | 10 | −144.54 | −7.54 | −10.54 |

El enlace no tiene margen robusto demostrado. Una antena direccional o mayor
potencia convertiría al nodo en otra clase y exigiría nuevo análisis técnico y
regulatorio.

## 6) Doppler, osciladores y ancho de banda

A 915 MHz y 7.7 km/s, la cota cinemática es aproximadamente `±23.5 kHz`. Un
oscilador de ±10 ppm aporta aproximadamente `±9.2 kHz` por equipo; el error
combinado debe incluir ambos relojes y temperatura.

Por eso:

- BW125 no se puede adoptar sin prueba de rampa Doppler + error de osciladores;
- BW250 intercambia aproximadamente 3 dB de sensibilidad de referencia por
  mayor tolerancia al offset;
- la decisión requiere PDR medido en toda la ventana, no solo CFO estático.

## 7) Condiciones para una conclusión científica

Antes de promover una configuración deben existir:

- autorización escrita para el enlace Tierra→espacio o una banda/servicio
  alternativo autorizado;
- receptor orbital exacto y sensibilidad absoluta calibrada;
- patrón OTA integrado, incluyendo orientación y estructura;
- rampa Doppler, error térmico de ambos osciladores y canalización real;
- PDR/PER con tamaño de muestra e intervalo de confianza predefinidos;
- pruebas near-far, co-canal, canal adyacente, blocking y coexistencia;
- configuración, raw data, calibraciones, versión y hashes archivados.

## 8) Dictamen preliminar

La recepción desde nodos típicos sigue siendo una hipótesis experimental de
alto riesgo, no un enlace cerrado. Técnicamente puede ser observable cerca de
máxima elevación, pero el margen es insuficiente para garantizar el objetivo.
Regulatoriamente permanece bloqueado.

## 9) Referencias

- `04_Communications/regulatory_gate_rf.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
- `docs/COMMS/uplink_lora_bench_testing_plan.md`
- `docs/COMMS/rf_calculations.py`
