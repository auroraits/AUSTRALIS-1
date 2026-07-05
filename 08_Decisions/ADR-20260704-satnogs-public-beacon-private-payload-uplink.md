# ADR-20260704-satnogs-public-beacon-private-payload-uplink

- **Fecha:** 2026-07-04
- **Estado:** Accepted

---

## Contexto

AUSTRALIS-1 mantiene como baseline de comunicaciones:

- Uplink de usuario LoRa 915 MHz RX-only en orbita.
- Downlink/TTC UHF 435 MHz FSK 1200 bps.
- Hardware TTC UHF final TBD, con OpenLST como candidato tecnico/base de desarrollo.

Se evaluo incorporar SatNOGS como red global receive-only para recibir downlink publico. SatNOGS puede aportar cobertura, observaciones independientes y recepcion distribuida de beacon/telemetria, pero no reemplaza:

- licencias y coordinacion ENACOM/IARU/ITU,
- estacion terrena propia para comando/control,
- definicion de seguridad, autenticacion y privacidad de datos operativos.

---

## Decision

Adoptar una arquitectura UHF que soporte tres perfiles de enlace sobre una plataforma TTC derivada de OpenLST u otra radio UHF equivalente:

1. **Beacon publico compatible con SatNOGS**
   - Downlink publico, periodico, documentado y decodificable.
   - Pensado para SatNOGS Network / SatNOGS DB / decoders publicos.
   - Incluye solo telemetria minima no sensible: identificacion, contador/tiempo, modo, estado basico de EPS/OBC/RF y flags publicos.

2. **Downlink privado/controlado de payload y operacion**
   - Transferencia de datos de payload y operacion completa solo hacia estacion/es terrena/s propia/s o autorizada/s.
   - Incluye, como minimo, `PHOTO_DEMO` imagenes, datos de performance del payload IA, `AI_BEHAVIOR_LOG` detallado, `SCIENCE`, `LORA_LOG`, respuestas operativas completas y dumps bajo demanda.
   - No se publica decoder ni esquema completo de estos frames como interfaz SatNOGS por defecto.

3. **Uplink privado/controlado**
   - Comandos TTC, prompts versionados del payload IA, seleccion de downlink, limites de cuota y comandos de seguridad solo desde estacion/es propia/s o autorizada/s.
   - Requiere autenticacion, control de acceso y procedimientos operativos propios.
   - SatNOGS no se usa como infraestructura de uplink/control.

La arquitectura debe permitir que el mismo UHF TRX de vuelo transmita el beacon publico y el downlink controlado, sin requerir una radio adicional solo por SatNOGS. El hardware final sigue TBD hasta Gate C.

---

## Reglas normativas

1. SatNOGS se considera una capa complementaria de recepcion publica, no una autoridad de control del satelite.
2. El beacon publico debe ser decodificable por terceros con informacion publicada suficiente.
3. Los datos de payload y operacion detallada quedan en un perfil privado/controlado y no forman parte del producto publico SatNOGS.
4. El uplink de comandos queda restringido a estaciones propias o explicitamente autorizadas.
5. La privacidad RF no debe asumirse por oscuridad del protocolo: cualquier transmision UHF puede ser capturada por terceros.
6. Cifrado, autenticacion y restricciones de contenido deben cerrarse contra el encuadre regulatorio aplicable antes de vuelo, especialmente si se opera bajo amateur-satellite.
7. La publicacion en SatNOGS DB debe realizarse solo con datos coherentes con la coordinacion/licencia vigente: frecuencia, modo, baudrate, servicio, estado y referencia publica.

---

## Implicancias tecnicas

- El hardware RF no cambia por incorporar SatNOGS, siempre que el UHF TRX soporte el modo publico definido.
- La seleccion OpenLST-derived debe contemplar:
  - estabilidad de frecuencia suficiente,
  - PA/front-end filtrado y espectro limpio,
  - modo robusto de baja tasa para beacon,
  - posibilidad de publicar decoder o adaptar un decoder existente.
- El `PUBLIC_BEACON` se trata como producto derivado de `HOUSEKEEPING`, no como payload cientifico.
- Los perfiles privados/controlados pueden compartir radio y antena con el beacon, pero deben estar separados por framing, IDs de servicio, autenticacion y politica de decoder.
- Operacion es half-duplex: uplink y downlink se planifican por ventanas/slots; no se asume comando y dump simultaneos.

---

## Implicancias regulatorias

- SatNOGS no licencia ni coordina el transmisor del satelite.
- ENACOM/IARU/ITU siguen siendo camino obligatorio segun banda, servicio y administracion.
- Si se usa amateur-satellite, el contenido, cifrado y caracter privado de tramas debe revisarse antes de declarar cumplimiento.
- La arquitectura permite payload downlink privado/controlado como requisito de mision, pero el mecanismo exacto de confidencialidad queda TBD hasta cierre regulatorio.

---

## Alternativas consideradas

1. **No usar SatNOGS**
   - Rechazada como decision principal. Pierde recepcion distribuida y valor comunitario para beacon publico.

2. **Usar SatNOGS para todo el downlink**
   - Rechazada. Expondria payload/operacion completa y no resuelve uplink/control.

3. **Radio separada solo para beacon SatNOGS**
   - Rechazada por masa, potencia, complejidad RF y volumen en 1.5U.

4. **Un UHF TRX con perfiles publico/controlado** (elegida)
   - Mantiene simplicidad de hardware y separa productos por politica de enlace.

---

## Riesgos

- Dependencia excesiva en estaciones SatNOGS de calidad variable.
- Confusion entre "privado" y "no decodificado publicamente"; RF sigue siendo observable.
- Posible incompatibilidad entre cifrado/privacidad y encuadre amateur-satellite.
- Necesidad de mantener un decoder publico para el beacon si se elige framing no estandar.

---

## Implicancias (archivos actualizados)

- `04_Communications/satnogs_public_beacon_architecture.md`
- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/uplink_data_products_and_downlink_policy.md`
- `00_MVP/MVP v2.2.md`
- `SYSTEM_BASELINE.md`
- `architecture.md`
- `01_Mission/requirements_matrix.md`
- `01_Mission/validation_plan_and_stage_gates.md`
- `07_Risk/top_risks.md`
