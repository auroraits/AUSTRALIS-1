# RF Subsystem Overview — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active
**Trazabilidad:** `08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`, `04_Communications/regulatory_gate_rf.md`, documentos de link budget de este subsistema

## 1) Arquitectura RF y estado real

El subsistema propuesto tiene dos cadenas:

- **LoRa RX 915–928 MHz:** experimento de uplink desde nodos terrestres. El
  satélite es RX-only, pero la transmisión deliberada Tierra→espacio está
  **bloqueada hasta dictamen escrito de ENACOM**.
- **UHF TRX en una asignación coordinada TBD dentro de 435–438 MHz:** beacon
  público, downlink/TTC y uplink autenticado desde estaciones autorizadas.
  `435.000 MHz` no es una frecuencia asignada ni un centro de diseño válido.

La exploración P1 estudia un concentrador LoRa y acceso por slotting. No implica
que un concentrador sea más sensible que un receptor single-channel ni que B2
sea legal u operable. La comparación debe medir sensibilidad, consumo,
blocking, Doppler/CFO y capacidad.

Estado de madurez:

- módulo UHF orbital: `TBD`;
- receptor LoRa orbital: `TBD`;
- antenas y despliegue: `TBD`;
- KiCad RF: **placeholder/no design**, sin circuito, netlist, footprints,
  outline ni ruteo fabricable;
- link budgets y protocolos: análisis de diseño, no evidencia de hardware.

## 2) Arbitraje de downlink

El Downlink Manager del OBC gestiona:

1. `HOUSEKEEPING` — prioridad estricta;
2. `COMMAND_ACK` — prioridad estricta;
3. `AI_BEHAVIOR_LOG` — mayor prioridad científica best-effort;
4. `LORA_LOG` — best-effort;
5. `SCIENCE` — best-effort;
6. `OPTIONAL_PAYLOAD` — best-effort mínimo.

Las prioridades estrictas no deben causar starvation permanente. El presupuesto
de datos debe reservar mínimos configurables, aplicar aging a colas
best-effort y demostrar que cierra los productos de éxito de misión. Ver
`04_Communications/uplink_data_products_and_downlink_policy.md`.

## 3) Uplink TTC y seguridad

Comandos conceptuales mínimos:

- `SET_MODE`;
- `POWER_SET`;
- `DL_SELECT`;
- `DL_SET_LIMITS`;
- `REQUEST_STATUS`;
- `ABORT`;
- carga/activación de prompts y consulta de estado.

Todos los comandos, incluido `ABORT`, deben llevar autenticación criptográfica
y protección anti-replay. CRC, hash sin clave, `node_id` o un canal
“privado” no autentican origen.

El contenido se mantiene en claro mientras no exista autorización expresa de
confidencialidad. La especificación de seguridad está en
`04_Communications/uhf_command_security_protocol.md`.

## 4) LoRa uplink experimental

| Parámetro | Estado de diseño |
|---|---|
| Banda | Canalización TBD dentro de 915–928 MHz, sujeta a autorización |
| Dirección | Tierra→satélite; satélite RX-only |
| PHY candidato | LoRa SF12, CR 4/5; BW125/BW250 en trade |
| Receptor orbital | Concentrador vs single-channel, `TBD` por ensayo |
| Ventana | `TBD`; derivada de elevación y error de predicción |
| Antena | `TBD`; patrón integrado obligatorio |
| Protocolo | Frame versionado, identidad autenticada, anti-replay |

Clase de nodo de referencia, no SKU:

- radio SX1262/SX1276 o equivalente;
- MCU ESP32-S3 o equivalente;
- +20 a +21 dBm, sin PA externo;
- antena simple 0–2 dBi;
- cristal comercial ±10 ppm; no se presupone TCXO.

**Bloqueo regulatorio:** RX-only en órbita no autoriza al transmisor terrestre.
No se realizarán transmisiones radiadas dirigidas al satélite hasta cerrar
`REG-LORA-915` en `04_Communications/regulatory_gate_rf.md`.

**Factibilidad:** el enlace de nodo típico puede quedar al borde incluso cerca
de zenith. Slotting reduce colisiones, pero no mejora el link budget ni prueba
origen. Los números corregidos están en
`04_Communications/link_budget_lora_uplink_preliminary.md`.

## 5) UHF TTC

| Parámetro | Estado de diseño |
|---|---|
| Frecuencia | Asignación coordinada `TBD` dentro de 435–438 MHz |
| Modulación | 2-FSK, perfil de ingeniería |
| Tasa | 1200 bit/s, pendiente de waveform completa |
| Potencia RF | 500 mW objetivo de papel; medir |
| Integridad de canal | Framing versionado + CRC + secuencia |
| Seguridad de comando | MAC/firma + contador anti-replay persistente |
| Hardware | `TBD`; OpenLST es candidato, no baseline final |

El presupuesto UHF debe cerrar por separado downlink y uplink. La geometría
corregida y ambos cálculos están en
`04_Communications/link_budget_uhf_preliminary.md`.

La máscara `≥20°` se conserva únicamente para planificación. Con el caso de
papel a 600 km, el margen es aproximadamente `+5.9 dB` a 20° y `+3.0 dB` a
10°, antes de incertidumbres no asignadas. No es garantía de servicio.

### 5.1 Waveform y Doppler

A 438 MHz, usando 7.7 km/s como cota radial, el Doppler máximo de primer orden
es aproximadamente `±11.25 kHz`. Antes de congelar la waveform deben definirse
y ensayarse:

- desviación 2-FSK y ancho ocupado;
- preámbulo, sync, whitening, line coding, FEC e interleaver;
- filtro RX, Automatic Frequency Control (AFC) y rango de adquisición;
- tolerancia de ambos osciladores y precompensación Doppler;
- MTU, fragmentación, ARQ, timeouts y comportamiento half-duplex.

La validación debe aplicar una rampa Doppler orbital más el error combinado de
osciladores y verificar el ancho autorizado. Un offset estático no basta.

### 5.2 Perfiles de operación

- `PUBLIC_BEACON`: beacon corto, identificado, públicamente documentado y
  decodificable por SatNOGS/terceros.
- `CONTROLLED_DOWNLINK`: downlink operado por estaciones autorizadas para
  payload y dumps. Si se usa amateur-satellite, waveform, framing,
  identificación y contenido deben satisfacer el régimen abierto aplicable.
- `PRIVATE_UPLINK`: nombre histórico del uplink TTC. Significa **operador
  autorizado**, no enlace secreto. Los comandos son legibles en RF pero
  autenticados y protegidos contra replay.

Cada emisión debe cumplir callsign/identificación y las condiciones del
expediente. La autenticación sin cifrado protege origen e integridad sin
ocultar el texto; su implementación requiere confirmación regulatoria.

SatNOGS es receive-only y no reemplaza licencia, coordinación ni estación
propia.

## 6) Candidatos UHF

Candidatos en análisis, no adoptados:

- CC1110/OpenLST-derived;
- AX5043;
- CC1101 + front-end;
- Si4463.

OpenLST aporta una referencia útil, pero la herencia del diseño original no se
transfiere automáticamente a una placa derivada con PA, filtro, layout,
potencia y waveform distintos. RFFM6403 está EOL y no puede ser dependencia del
diseño final. La adopción requiere ADR y nueva campaña de V&V.

## 7) Antena del satélite

Candidatos: dipolo desplegable, monopolo tangencial u otra geometría compatible
con el dispenser; ninguno está seleccionado.

Un monopolo normal a la cara nadir tendría un nulo axial aproximadamente hacia
tierra en pasadas de alta elevación, por lo que esa orientación no se adopta.
La selección requiere:

1. frames mecánico, corporal y de antena;
2. patrón 3D con estructura, paneles, harness y radiales;
3. realized gain, polarización y detuning medidos;
4. deployment verificado después de ambiente;
5. propagación del patrón por actitud nominal, error, tumble y modo seguro.

El `0 dBi` de los link budgets es una hipótesis aritmética, no un patrón real.

## 8) EMC y coexistencia

La compatibilidad electromagnética no se cierra con reglas cualitativas. Debe
existir una matriz de modos que cubra:

- UHF TX → LoRa RX, SDR/LNA y sensores;
- LoRa RX con UHF idle/RX/TX;
- EPS, convertidores, CM5, storage, buses y actuadores en peor actividad;
- armónicos, espurias, intermodulación, desense, blocking y ruido conducido;
- estados nominales, brownout, inrush y conmutación de rails.

Para cada combinación se registrarán aislamiento/S-parameters cuando aplique,
noise floor, sensibilidad/PER antes y durante el agresor, espectro y corriente.
El criterio cuantitativo debe asignarse antes del ensayo desde el margen del
enlace; permanece `TBD` hasta cerrar hardware y presupuesto.

No se permite UHF TX simultáneo con recepción LoRa salvo evidencia específica.

## 9) Gates de cierre

El subsistema no puede declararse cerrado hasta:

- resolver `REG-UHF-AMATEUR` y `REG-LORA-915`;
- seleccionar hardware y antenas con ADR;
- medir link budgets bidireccionales, patrón, Doppler y PER;
- cerrar protocolo autenticado, anti-replay y recuperación de claves;
- cerrar data budget, retención y descarga;
- superar EMC/coexistencia, OTA y end-to-end ground;
- producir evidencia identificada, raw, calibrada y hasheada.

<!-- FEATURE:PHOTO_DEMO START -->

## 10) [PHOTO_DEMO] Tráfico opcional

`PHOTO_DEMO` usa exclusivamente `OPTIONAL_PAYLOAD`, por chunks reanudables y
sin desplazar housekeeping, ACK ni el producto científico primario.

<!-- FEATURE:PHOTO_DEMO END -->

## 11) Referencias

- `04_Communications/link_budget_uhf_preliminary.md`
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/uhf_command_security_protocol.md`
- `04_Communications/regulatory_gate_rf.md`
- `04_Communications/satnogs_public_beacon_architecture.md`
- `04_Communications/ground_station_dual_use_satnogs_australis.md`
- `docs/COMMS/uhf_ttc_bench_testing_plan.md`
- `docs/COMMS/uplink_lora_bench_testing_plan.md`
