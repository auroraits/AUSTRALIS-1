# SatNOGS Public Beacon Architecture

**Revision:** 2026-07-04
**Estado:** Active
**Trazabilidad:** `08_Decisions/ADR-20260704-satnogs-public-beacon-private-payload-uplink.md`, `04_Communications/rf_subsystem_overview.md`, `04_Communications/uplink_data_products_and_downlink_policy.md`

---

## 1) Objetivo

Definir como se incorpora SatNOGS al segmento terreno de AUSTRALIS-1 sin cambiar el principio de seguridad operacional:

- SatNOGS recibe beacon publico y telemetria minima.
- El payload downlink completo queda privado/controlado.
- El uplink de comandos queda privado/controlado.
- La estacion terrena propia sigue siendo el camino de TTC operacional.

---

## 2) Rol de SatNOGS

SatNOGS se usa como red global receive-only para observaciones publicas del satelite.

Uso previsto:

- recepcion distribuida de beacon UHF,
- confirmacion independiente de presencia orbital,
- mediciones de cobertura/recepcion por estaciones externas,
- publicacion de transmisor en SatNOGS DB,
- soporte comunitario para telemetria publica no sensible.

No se usa para:

- uplink de comandos,
- control de modo,
- carga de prompts IA,
- seleccion de imagenes o dumps,
- transferencia de payload privado,
- reemplazo de estacion terrena propia.

---

## 3) Perfiles de enlace

| Perfil | Direccion | Visibilidad | Contenido | Estacion |
|---|---|---|---|---|
| `PUBLIC_BEACON` | Satelite -> tierra | Publica | ID, tiempo/contador, modo, EPS/OBC/RF minimo, flags publicos | SatNOGS + propia |
| `CONTROLLED_DOWNLINK` | Satelite -> tierra | Privada/controlada | `PHOTO_DEMO`, `AI_BEHAVIOR_LOG` detallado, performance IA, `SCIENCE`, `LORA_LOG`, dumps | Propia/autorizada |
| `PRIVATE_UPLINK` | Tierra -> satelite | Privada/controlada | comandos TTC, prompts IA, cuotas, seleccion de dumps, abort/safe | Propia/autorizada |
| `LORA_USER_UPLINK` | Nodos -> satelite | Operacional RX-only | paquetes LoRa de nodos terrestres | Nodos LoRa, no SatNOGS |

Nota: "privada/controlada" significa que no es producto publico SatNOGS ni interfaz comunitaria. No implica confidencialidad criptografica por si sola; cualquier emision RF puede ser capturada.

---

## 4) Impacto en hardware de vuelo

No se requiere una radio adicional solo para SatNOGS.

La arquitectura esperada usa un unico UHF TRX de TTC, preferentemente derivado de OpenLST o equivalente, con:

- frecuencia coordinada en UHF amateur-satellite o banda aprobada,
- modo robusto de baja tasa para beacon publico,
- modo de downlink controlado para payload,
- receptor de uplink para estaciones propias,
- TCXO o referencia estable,
- front-end UHF con PA, filtrado y switching TX/RX adecuados,
- antena UHF compartida por beacon, downlink controlado y uplink.

El hardware final sigue TBD. Esta decision fija la capacidad arquitectonica, no el MPN final del transceptor ni del PA.

---

## 5) Requisitos de compatibilidad SatNOGS

Para que SatNOGS aporte valor real, el `PUBLIC_BEACON` debe tener:

- frecuencia publicada,
- modo/modulacion publicado,
- baudrate publicado,
- frame schema publico,
- CRC o integridad simple,
- identificador de mision/satelite,
- decoder disponible o compatible con tooling existente,
- documentacion suficiente para SatNOGS DB.

Preferencia tecnica:

1. Modo publicamente decodificable con tooling existente.
2. Si se usa framing OpenLST-derived, publicar decoder solo para el `PUBLIC_BEACON`.
3. Mantener el beacon corto y robusto; no depender de estaciones con enlace excelente.

---

## 6) Datos publicos vs privados/controlados

### Publico

Permitido en `PUBLIC_BEACON`:

- callsign/identificacion coordinada,
- contador de boot/pasada,
- timestamp o contador relativo,
- `MISSION_MODE`,
- `EPS_STATE`,
- bateria/temperatura resumida,
- flags de salud agregados,
- version publica de firmware/protocolo,
- checksum/CRC.

### Privado/controlado

No va en el beacon publico por defecto:

- imagenes `PHOTO_DEMO`,
- datos completos o crudos del payload IA,
- `AI_BEHAVIOR_LOG` detallado,
- prompts/policy prompts,
- paquetes LoRa crudos o identificables,
- datos detallados de Science Pack,
- respuestas de comando completas,
- dumps de memoria/logs operativos,
- estado interno de seguridad que facilite abuso.

---

## 7) Regulacion y seguridad

SatNOGS no reemplaza coordinacion ni licencias.

Pendientes regulatorios:

- ENACOM / administracion nacional,
- coordinacion IARU si se usa amateur-satellite,
- filings/encuadre ITU segun aplique,
- definicion de contenido permitido en el downlink,
- tratamiento de cifrado/autenticacion para uplink y downlink controlado.

La arquitectura separa perfiles, pero la politica exacta de cifrado queda TBD hasta cierre regulatorio. En particular, si el encuadre final es amateur-satellite, se debe verificar que cualquier mecanismo de confidencialidad sea aceptable.

---

## 8) Verificacion

Gate C debe demostrar, como minimo:

- beacon UHF transmitido por hardware candidato,
- recepcion local con SDR/estacion propia,
- decodificacion reproducible del frame publico,
- medicion de frecuencia/deriva suficiente para el modo elegido,
- evidencia de que el beacon no contiene datos privados/controlados,
- plan de publicacion SatNOGS DB preparado.

Gate E/F deben demostrar:

- operacion de estacion propia con comandos privados/controlados,
- separacion entre productos publicos y controlados,
- politica de uplink autenticado,
- procedimiento para abort/safe sin depender de SatNOGS.
