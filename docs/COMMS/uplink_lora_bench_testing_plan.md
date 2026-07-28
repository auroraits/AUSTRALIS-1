# LoRa uplink — plan de ensayo de banco

**Revisión:** 2026-07-27
**Estado:** Draft — ejecución radiada bloqueada por `REG-LORA-915`
**Trazabilidad:** `04_Communications/uplink_lora_slotted_protocol.md`, `04_Communications/link_budget_lora_uplink_preliminary.md`
**ProcedureID:** `PROC-RF-002`, `PROC-DATA-001`, `PROC-REG-001`

## 1) Propósito

Determinar si un nodo de clase objetivo puede ser recibido por el receptor
orbital candidato y si slotting, autenticación, scheduler y pipeline de datos
funcionan con rigor reproducible.

El plan no selecciona BW, canal, concentrador ni hardware de vuelo.

## 2) Restricción regulatoria

Hasta cerrar `REG-LORA-915`:

- ensayos por coax, atenuadores, dummy load o caja apantallada;
- ninguna emisión dirigida al satélite;
- ninguna prueba outdoor radiada salvo autorización experimental específica;
- B1/B2 deshabilitados operacionalmente.

La evidencia técnica no cierra el gate legal.

## 3) Preregistro

Antes de cada campaña se congela:

- TestID, hipótesis y requisitos;
- Device Under Test (DUT), firmware, commit y configuración;
- variable independiente/dependiente;
- tamaño de muestra y niveles;
- PDR/PER objetivo e intervalo de confianza;
- criterio pass/fail;
- plan de exclusiones y manejo de outliers;
- calibraciones, raw format y hash esperado.

Un barrido exploratorio sin criterio previo se etiqueta `Exploratory` y no
cierra baseline.

## 4) Instrumentación

- generador RF/modulador o segundo radio caracterizado;
- step attenuator y atenuadores fijos calibrados;
- power meter y analizador de espectro;
- combinadores/acopladores y terminaciones;
- emulador de Doppler o playback IQ;
- recinto/cámara de temperatura para TX/RX;
- fuente programable y captura de corriente;
- referencia de frecuencia trazable;
- concentrador y receptor single-channel candidatos;
- al menos tres nodos para bring-up; cantidad final según preregistro;
- para OTA, instalación calibrada y artículo representativo.

Se registra pérdida de cables/fixtures en cada frecuencia, modelo/serie,
calibración y uncertainty.

## 5) Configuraciones mínimas

Comparar, como mínimo:

- SF12/BW125/CR4/5/header explícito/CRC/preamble16;
- SF12/BW250 con iguales condiciones;
- payload legado de 12 B para regresión de Time-on-Air (ToA);
- frame autenticado real con longitud final;
- single-channel vs concentrador con front-end/reloj reales.

El canal usado en coax es una frecuencia de test. No se lo presenta como canal
orbital.

## 6) Matriz de ensayos

| TestID | ReqID principal |
|---|---|
| `LORA-01` | COMMS-UL-06 |
| `LORA-02` | MIS-REQ-04, COMMS-UL-01/06 |
| `LORA-03` | COMMS-UL-03/06 |
| `LORA-04` | COMMS-UL-06 |
| `LORA-05` | MIS-REQ-04, COMMS-UL-06 |
| `LORA-06` | COMMS-UL-02/03 |
| `LORA-07` | MIS-REQ-05/20 |
| `LORA-08` | MIS-REQ-04 |
| `LORA-09` | MIS-REQ-04 |
| `LORA-10` | MIS-REQ-02/04 |
| `LORA-11` | MIS-REQ-05/09, COMMS-UL-04/05 |

### LORA-01 — Configuración y ToA

- Capturar waveform y medir ToA.
- Referencias de 12 B: 1.417216 s BW125 y 0.708608 s BW250.
- Recalcular frame autenticado exacto.
- Verificar preámbulo, header, CRC, CR, BW y occupied bandwidth.

**Criterio:** error máximo `TBD` preregistrado contra cálculo y configuración
decodificada consistente.

### LORA-02 — Sensibilidad absoluta

1. Medir potencia en plano de referencia RX.
2. Barrer la transición completa de PDR.
3. Ejecutar `N` frames preregistrados por nivel.
4. Reportar PDR/PER e intervalo Wilson 95 %.
5. Repetir BW125/BW250, temperaturas y tensión.

La sensibilidad es el nivel que cumple el PDR preregistrado con confianza, no
el primer paquete recibido. Comparar concentrador y single-channel bajo el
mismo fixture.

### LORA-03 — Doppler y osciladores

Aplicar una rampa temporal, no solo offsets estáticos:

- envolvente cinemática de referencia ±23.5 kHz a 915 MHz;
- ppm TX + ppm RX;
- deriva térmica y tensión;
- error residual de scheduler/predicción.

Medir adquisición, pérdida/recuperación de lock, CFO estimado y PDR a lo largo
de la rampa. Repetir para ambos BW.

### LORA-04 — Interferencia y near-far

Ensayar:

- co-canal;
- canal adyacente;
- blocking fuera de canal;
- dos canales simultáneos;
- near-far y capture;
- múltiples SF si el receptor lo soporta;
- canalización BW125 y BW250 por separado.

Registrar potencia deseada/agresor en el plano RX. No usar canales que se
solapan como evidencia de diversidad.

### LORA-05 — ALOHA vs slotted

Para cargas preregistradas:

- ALOHA aleatorio como control;
- slotting B1 simulado;
- B2 con schedules independientes;
- uno y dos retries;
- colisiones deliberadas;
- nodos con drift/latencia.

Métricas:

- intentos, únicos, duplicates, auth fail, replay;
- PDR por nodo y percentiles;
- collision/capture estimados;
- fairness y starvation;
- latencia y airtime.

Comparar contra el modelo analítico y Monte Carlo. No asumir retries
independientes sin comprobarlo.

### LORA-06 — Timebase, TLE y scheduler

Inyectar:

- error de UTC/RTC y drift térmico;
- GNSS ausente/degradado;
- TLE correcto, viejo, de otro object ID, rollback y corrupto;
- error de propagación;
- ventana que cruza elevación mínima;
- actualización a mitad de schedule;
- reboot/power loss.

**Hard-fail:** ante provenance, object ID, time quality o uncertainty inválidos,
el nodo no transmite. B1 no se activa automáticamente.

### LORA-07 — Frame, identidad y anti-replay

Casos:

- MAC/tag correcto, incorrecto, truncado;
- misión/network/node equivocados;
- boot epoch nuevo, repetido o rollback;
- seq nuevo, duplicate, fuera de ventana y wrap;
- payload/metadata modificados;
- key epoch vigente, anterior, revocado;
- reset/power-cut del receptor.

CRC OK con auth fail debe rechazarse. Los casos críticos requieren 100 % de
rechazo correcto.

### LORA-08 — Antena OTA integrada

Medir patrón 3D, polarización, detuning y realized gain con estructura, paneles,
harness y configuración de despliegue. Repetir antes/después de ambiente.

El patrón debe convertirse en pérdida para actitud nominal/degradada del link
budget.

### LORA-09 — EMC/coexistencia

Ejecutar el receptor en la transición de PDR mientras se activan:

- UHF TX/RX/idle;
- EPS/MPPT/DC-DC;
- CM5 en carga/inferencia;
- storage/buses/actuadores;
- switching de rails e inrush.

Medir desense, noise floor, espurias, PDR y corriente. No se autoriza
simultaneidad si excede el margen asignado.

### LORA-10 — Potencia e integración

- consumo min/nom/max RX;
- GNSS on/off;
- startup/inrush;
- power gating OFF real;
- brownout/reset;
- temperatura;
- logging continuo sin pérdida.

El resultado alimenta EPS; una cifra de HAT de referencia no sustituye la
medición del módulo final.

### LORA-11 — Pipeline de datos

Demostrar:

- raw append-only;
- resumen/catálogo/dump;
- metadata RF y auth/replay;
- reboot/session IDs;
- digest/chunks;
- downlink simulado bajo cuotas;
- replay determinista en ground;
- correlación con log TX/site para criterio de origen.

## 7) Métricas y schema raw

Por transmisión:

- campaign/TestID/run ID;
- node/boot/seq/key epoch;
- UTC y time quality;
- TX configuration/power;
- RX configuration/input power;
- Doppler/CFO aplicado y estimado;
- RSSI/SNR con quality/calibración;
- CRC/auth/replay verdict;
- raw frame;
- temperatura/tensión/corriente;
- agresores EMC;
- software/firmware/hash.

Agregados:

- PDR/PER e intervalo;
- distribución por nodo;
- duplicates/replays;
- fairness;
- energía por intento/éxito;
- sensibilidad y degradación por condición.

## 8) Evidence bundle

Cada corrida conserva:

- preregistro;
- diagrama/fotos de setup;
- instrumento/calibración;
- configuración serializada;
- raw data inmutable;
- script de análisis;
- resultados y uncertainty;
- desviaciones;
- commit y SHA-256.

## 9) Criterio de salida

Solo se propone baseline si:

- autorización/encuadre existe;
- PDR y confianza cumplen el criterio;
- BW/canal resisten Doppler y osciladores;
- frame autenticado y anti-replay pasan casos adversos;
- capacidad multi-node cumple carga definida;
- patrón y EMC integrados preservan margen;
- potencia y data budget cierran;
- evidencia fue revisada independientemente.

Si no cierra, alternativas:

- banda/servicio autorizado distinto;
- receptor/antena distintos;
- nodo/gateway bajo otra clase y permiso;
- retirar o reformular el objetivo secundario.

## 10) Referencias

- `04_Communications/regulatory_gate_rf.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `04_Communications/uplink_data_products_and_downlink_policy.md`
- `docs/COMMS/rf_calculations.py`
