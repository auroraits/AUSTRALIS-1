# Ground station — verification and fault-injection plan

**Revisión:** 2026-07-27
**Estado:** Draft
**Trazabilidad:** `04_Communications/ground_station_dual_use_satnogs_australis.md`
**ProcedureID:** `PROC-GND-001`, `PROC-SEC-001`, `PROC-DATA-001`

## 1) Objetivo

Demostrar que la estación dual-use recibe, persiste y reproduce evidencia; que
SatNOGS no puede transmitir; y que todo TX AUSTRALIS requiere autorización,
autenticación e interlocks físicos.

No se realiza TX radiado hasta cerrar los gates regulatorios. Las pruebas de TX
se ejecutan en dummy load/coax/caja apantallada salvo permiso específico.

## 2) Preregistro y configuración

Cada TestID fija antes de ejecutar:

- hardware/software/firmware y diagramas;
- red, cuentas, firewall y credenciales de test;
- instrumentos/calibraciones;
- inputs, faults y orden;
- criterio pass/fail;
- raw evidence y hash;
- responsable y revisión independiente.

## 3) Matriz

| TestID | ReqID | Objetivo | Fallas/estímulo | Hard-fail |
|---|---|---|---|---|
| `GS-01` | MIS-REQ-21 | Aislamiento SatNOGS | scan USB/red, requests maliciosos | host RX obtiene capacidad TX |
| `GS-02` | MIS-REQ-03/21 | Secuencia T/R | kill proceso/red/power en cada paso | PTT queda activo o LNA expuesto |
| `GS-03` | MIS-REQ-03 | Protección RF | SWR alto, no load, sensor fail | TX no se corta |
| `GS-04` | MIS-REQ-21 | Armado | sin llave, permiso expirado, rol inválido | cualquier RF TX |
| `GS-05` | MIS-REQ-11/18/20 | Command security | tag/replay/epoch/schema adversos | comando produce efecto |
| `GS-06` | COMMS-UL-03 | Orbit data | wrong object, rollback, stale, corrupt | TX/track aceptado fuera de budget |
| `GS-07` | MIS-REQ-22/COMMS-UL-03 | Tiempo/rotor | GNSS/NTP fail, encoder error, viento | TX fuera de ventana/pointing |
| `GS-08` | MIS-REQ-05/17 | Persistencia | disk full, power cut, reboot | evidencia aceptada sin raw |
| `GS-09` | MIS-REQ-05/17 | Replay | dataset conocido | resultado no reproducible |
| `GS-10` | MIS-REQ-21 | Red/UI | LAN no autenticada, session hijack | connect/PTT/config modificable |
| `GS-11` | MIS-REQ-21 | Operación offline | Internet/CDN/DNS down | adquisición/seguridad fallan |
| `GS-12` | MIS-REQ-22 | UPS/watchdog | mains fail, process hang | estado no vuelve seguro |
| `GS-13` | MIS-REQ-22 | Clima | viento/lluvia/sensor invalid | track/TX no se inhiben |
| `GS-14` | MIS-REQ-19 | SatNOGS RX | observación pública | no decodifica schema publicado |
| `GS-15` | MIS-REQ-11/19/20 | End-to-end | frame→OBC sim→ACK→storage | falta correlación o autenticidad |

## 4) GS-01 — frontera RX-only

Preparación:

- host SatNOGS con SDR RX-only;
- TX controller separado;
- firewall deny-by-default;
- inventario USB/PCI/red.

Pruebas:

1. Enumerar dispositivos y APIs desde usuario/proceso SatNOGS.
2. Intentar GPIO/PTT/serial/TCP al TX controller.
3. Comprometer proceso SatNOGS de test e intentar pivot.
4. Solicitar rotor fuera de allowlist/ventana.
5. Reiniciar servicios en distintos órdenes.

Pass:

- no existe dispositivo/path TX utilizable;
- todo request no permitido es rechazado y logueado;
- rotor puede park/inhibir, nunca armar PTT;
- la frontera se conserva después de update/reboot.

## 5) GS-02/03/04 — hardware safety

Inyectar pérdida de control/power en cada paso:

```text
RX -> isolate LNA -> switch TX -> enable PA -> PTT
PTT off -> PA off -> switch RX -> enable LNA
```

Verificar:

- default físico RX/TX disabled;
- watchdog corta PTT en tiempo preregistrado;
- llave/hardware arm ausente impide TX;
- SWR/potencia/sensor fault interrumpen;
- E-stop funciona sin software;
- timeout máximo y energía RF quedan bajo límites de seguridad;
- event log preserva orden y timestamps.

## 6) GS-05 — comandos

Usar el corpus de `04_Communications/uhf_command_security_protocol.md`:

- tag válido/incorrecto/truncado;
- counter nuevo/repetido/menor;
- reset durante persistencia;
- key epoch y roles;
- schema/argumentos;
- objeto/prompt incompleto;
- ACK autenticado.

Todo caso crítico exige 100 % de rechazo correcto.

## 7) GS-06/07 — orbit data, tiempo y rotor

Dataset mínimo:

- elemento orbital correcto;
- otro catalog ID;
- epoch rollback;
- firma/provenance ausente;
- archivo truncado/corrupto;
- edades crecientes;
- error UTC/GNSS/NTP;
- error y stall de rotor;
- ventana que cruza elevación mínima.

El test debe convertir error orbital en tiempo/azimut/elevación/Doppler y
compararlo con el presupuesto. No se usa “TLE <7 días” como proxy sin campaña.

Pass:

- TX solo cuando toda la ventana está dentro de autorización/máscara;
- uncertainty inválida inhibe;
- inputs y decisión quedan en evidence store.

## 8) GS-08/09 — evidencia

La adquisición escribe raw antes del dashboard. Inyectar:

- disk full/read-only;
- power cut entre raw/index/decode;
- duplicates, out-of-order, wrap y reboot;
- versión de decoder distinta;
- reloj degradado.

Replay:

1. instalar commit/configuración registrada;
2. cargar raw + metadata;
3. regenerar frames/métricas;
4. comparar bit a bit o por tolerancia preregistrada;
5. producir hash del resultado.

PER debe segmentarse por session/boot y política modular; no inferirse de gaps
sin distinguir resets y reordenamiento.

## 9) GS-10/11 — red y operación offline

- UI/control local-only por defecto;
- autenticación/authorization por acción;
- TLS/VPN y firewall para acceso remoto;
- CSRF/session timeout/rate limits;
- dependencias JS/CSS locales y versionadas;
- operación sin Internet/DNS/CDN;
- logs de login/config/control.

Ningún usuario LAN no autenticado puede cambiar puerto, desconectar adquisición,
modificar scheduler, armar o transmitir.

## 10) GS-12/13 — autonomía segura

Inyectar:

- mains fail/UPS low battery;
- service hang y watchdog;
- sensor meteorológico stuck/missing/out-of-range;
- humedad/temperatura/wind thresholds;
- pérdida de enlace de rotor.

La estación debe persistir estado, volver a RX, cortar PTT y park según el
procedimiento. Thresholds se fijan por hardware/estructura, no por placeholders.

## 11) GS-14/15 — compatibilidad y end-to-end

SatNOGS:

- captura de beacon conducido/autorizado;
- decoder público desde entorno limpio;
- test vectors y schema versionado;
- frequency/Doppler observables;
- prueba de ausencia de acceso TX.

End-to-end:

```text
operador autorizado
-> command envelope
-> ground TX controller
-> RF/coax channel
-> radio/OBC simulator
-> supervisor/effect
-> authenticated ACK
-> ground raw store
-> replay/report
```

Correlacionar command ID, counter, raw frames, efecto y ACK.

## 12) Evidence bundle

- preregistro y TestID;
- configuración exportada;
- diagramas/fotos;
- raw network/RF/control logs;
- fault timeline;
- instrumentos/calibraciones;
- resultados y uncertainty;
- commit y SHA-256;
- desviaciones y revisión.

## 13) Criterio de cierre

La estación no está ready hasta:

- gates regulatorios cerrados;
- todos los hard-fail pasan;
- RX/TX boundary revisada independientemente;
- persistence/replay demostrados;
- seguridad y anti-replay verificados;
- RF/link/OTA/EMC cerrados;
- procedimiento operacional y de emergencia ensayado.
