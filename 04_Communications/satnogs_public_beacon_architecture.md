# SatNOGS public beacon architecture

**Revisión:** 2026-07-27
**Estado:** Active
**Trazabilidad:** `04_Communications/regulatory_gate_rf.md`, `04_Communications/rf_subsystem_overview.md`

## 1) Objetivo

Incorporar SatNOGS como red receive-only para evidencia pública sin entregar
control del satélite ni presentar un enlace amateur como confidencial.

SatNOGS aporta:

- recepción distribuida del beacon;
- observaciones independientes;
- publicación de frecuencia/waveform/decoder cuando estén coordinados;
- mediciones comunitarias de cobertura.

SatNOGS no aporta:

- licencia o coordinación;
- uplink;
- autenticación de comandos;
- estación propia para TTC;
- autorización para publicar o transmitir datos sensibles.

## 2) Perfiles

| Perfil | Dirección | Operación | Contenido |
|---|---|---|---|
| `PUBLIC_BEACON` | Satélite→tierra | Público/SatNOGS | identificación y salud mínima |
| `CONTROLLED_DOWNLINK` | Satélite→tierra | Programado por estación autorizada | payload/dumps permitidos |
| `PRIVATE_UPLINK` | Tierra→satélite | Solo operador autorizado | comandos y objetos autenticados |
| `LORA_USER_UPLINK` | Tierra→satélite | Bloqueado regulatoriamente | experimento de nodos |

Los nombres `CONTROLLED` y `PRIVATE` describen quién opera, no secreto del
canal. Si se usa amateur-satellite:

- cualquier receptor puede observar las emisiones;
- identificación, waveform, framing y decoder se publican cuando lo exija el
  régimen;
- no se presupone cifrado ni confidencialidad;
- datos incompatibles con ese marco no se transmiten.

## 3) Frecuencia y hardware

No se agrega una radio solo para SatNOGS. El candidato es un único TRX UHF con:

- asignación coordinada `TBD` dentro de 435–438 MHz;
- 2-FSK 1200 bit/s como perfil de ingeniería, no waveform cerrada;
- modo beacon públicamente decodificable;
- downlink controlado y receptor TTC;
- TCXO/referencia, PA, filtros y switch T/R por seleccionar;
- antena compartida con patrón integrado por verificar.

`435.000 MHz` no es centro de diseño. El hardware final sigue `TBD`.

## 4) Identificación

No basta poner callsign en el beacon. **Toda emisión UHF** debe cumplir la
identificación y periodicidad exigidas por su autorización, incluidos:

- beacon;
- payload/dumps;
- ACK/NACK;
- emisiones de prueba;
- uplink desde tierra.

El callsign no se inventa ni se fija antes de la asignación. El frame reserva
un campo de identificación versionado y el scheduler debe impedir emisiones
que no puedan satisfacer la regla aplicable.

## 5) Contenido del beacon

Campos candidatos:

- callsign/identificación asignada;
- `protocol_version`;
- spacecraft/mission ID;
- boot counter y contador de frame;
- timestamp o tiempo relativo con quality flag;
- `MISSION_MODE` y `EPS_STATE`;
- batería/temperatura resumidas;
- health flags agregados;
- versión pública de firmware;
- CRC.

No contiene:

- claves, tags reutilizables o material de provisioning;
- prompts;
- raw AI inputs/outputs;
- paquetes LoRa crudos o identificadores personales;
- dumps de memoria;
- información cuya publicación comprometa seguridad;
- contenido no permitido por el expediente.

El schema, ejemplos y decoder deben publicarse antes de operación.

## 6) Downlink controlado

Puede transportar, si el régimen lo permite:

- `AI_BEHAVIOR_LOG`;
- `LORA_LOG`;
- `SCIENCE`;
- `OPTIONAL_PAYLOAD`;
- catálogos y dumps solicitados.

No se usa un “decoder cerrado” como mecanismo de privacidad. Si un producto
necesita confidencialidad, se omite o se migra a un servicio/autorización que
la permita.

El downlink conserva prioridad, cuota, fragmentación, CRC/FEC y metadata
públicamente documentables. Los ACK relacionados con comandos están
autenticados según `04_Communications/uhf_command_security_protocol.md`.

## 7) Uplink autorizado, no secreto

`PRIVATE_UPLINK` se redefine operativamente como uplink de un **operador
autorizado**:

- comando y argumentos en claro;
- MAC/firma sobre envelope completo;
- contador anti-replay persistente;
- roles y schemas derivados localmente por OBC;
- ACK/NACK autenticado;
- nada de control por SatNOGS.

CRC/hash sin clave no autentican. La suite exacta necesita revisión técnica y
confirmación regulatoria.

## 8) Separación SatNOGS/TX

La estación dual-use debe mantener una frontera física:

- SDR/host SatNOGS dedicado y RX-only;
- sin credenciales, claves, GPIO, PTT ni dispositivo TX accesible;
- controlador TX separado;
- hardware arm y PTT gate;
- switch T/R fail-safe a RX;
- IPC mínimo, autenticado y allow-listed desde operaciones AUSTRALIS;
- logs independientes.

Compartir rotor/antena/scheduler no otorga al cliente SatNOGS una ruta de TX.
Diseño: `04_Communications/ground_station_dual_use_satnogs_australis.md`.

## 9) Evidencia de compatibilidad

Antes de registro operacional en SatNOGS:

- frecuencia y callsign coordinados;
- transmitter entry preparada;
- waveform/framing documentados;
- decoder reproducible con test vectors;
- beacon recibido localmente por SDR;
- Doppler/frequency error dentro del rango demostrado;
- paquete de licencia/coordinación referenciado;
- revisión de contenido público;
- prueba de que SatNOGS no puede activar TX.

Gate end-to-end:

- captura IQ/raw;
- frame decodificado con versión;
- persistencia y hash;
- timestamp/time quality;
- correlación con transmisión conducida o autorizada;
- repetición por tercero a partir de documentación pública.

## 10) Estado regulatorio

Todos los gates permanecen abiertos a la fecha de revisión. Ver
`04_Communications/regulatory_gate_rf.md`.

SatNOGS DB y una coordinación IARU no reemplazan la autorización ENACOM ni el
trámite UIT. No se publica una frecuencia como operacional antes del cierre.

## 11) Referencias

- `04_Communications/regulatory_gate_rf.md`
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/uhf_command_security_protocol.md`
- `04_Communications/ground_station_dual_use_satnogs_australis.md`
- `04_Communications/uplink_data_products_and_downlink_policy.md`
