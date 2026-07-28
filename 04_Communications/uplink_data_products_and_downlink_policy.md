# Productos de datos y política de downlink

**Revisión:** 2026-07-27
**Estado:** Active — tamaños, tasas y cuotas pendientes de medición
**Trazabilidad:** `04_Communications/rf_subsystem_overview.md`, `04_Communications/uhf_command_security_protocol.md`

## 1) Principio

UHF 1200 bit/s es un recurso escaso. Ningún producto puede declararse
descargable hasta demostrar:

```text
producción + backlog inicial
<= capacidad neta de contactos autorizados
   - reservas críticas
   - retransmisiones
```

El sistema conserva raw data a bordo, baja resúmenes primero y permite
drill-down por comandos autenticados. La retención y la evidencia de misión no
dependen de que “quede tiempo” después de housekeeping.

## 2) Capacidad física

Para bitrate \(R\), contacto \(T\), fracción TX \(D\) y eficiencia total
\(\eta\):

\[
B_{net}=R\,T\,D\,\eta/8
\]

\(\eta\) incluye preámbulo, framing, identificación, autenticación cuando
aplique, FEC, ARQ, gaps y Packet Error Rate (PER). No se adopta un valor hasta
medir la waveform.

Ejemplo aritmético a 1200 bit/s y 8 min:

| Uso TX | Bytes antes de overhead | KiB |
|---:|---:|---:|
| 100 % | 72 000 B | 70.31 |
| 60 % | 43 200 B | 42.19 |
| 30 % | 21 600 B | 21.09 |

`70.3 KiB` es techo bruto continuo, no volumen de pasada garantizado. La
duración útil debe derivarse de elevación, actitud, patrón, autorización y
link budget; no de “visibilidad” geométrica total.

## 3) Ledger obligatorio

Antes de Gate E, cada fila debe tener valores medidos o límites justificados:

| ProductID | Bytes/evento min/nom/max | Eventos/día | Producción/día | Retención | Pérdida admisible | Cuota/contacto | Evidencia |
|---|---:|---:|---:|---:|---:|---:|---|
| `PUBLIC_BEACON` | TBD | TBD | TBD | N/A | TBD | TBD | TBD |
| `HOUSEKEEPING` | TBD | TBD | TBD | TBD | TBD | reserva estricta | TBD |
| `COMMAND_ACK` | TBD | por comando | TBD | TBD | 0 para comando aceptado | reserva estricta | TBD |
| `AI_BEHAVIOR_LOG` | TBD | duty IA medido | TBD | TBD | criterio misión TBD | mínimo protegido | TBD |
| `LORA_PASS_SUMMARY` | TBD | por ventana | TBD | TBD | TBD | mínimo protegido | TBD |
| `LORA_RAW` | TBD | tráfico recibido | TBD | TBD | TBD | on-demand | TBD |
| `SCIENCE` | TBD | TBD | TBD | TBD | TBD | mínimo protegido | TBD |
| `OPTIONAL_PAYLOAD` | TBD | opcional | TBD | TBD | best-effort | residual | TBD |

El ledger incluye:

- versión exacta de schema y serialización;
- overhead por capa;
- compresión y costo de índices;
- duplicación/ACK/ARQ;
- crecimiento de logs de sistema;
- días sin contacto;
- peor caso de producción;
- storage reservado, high-water mark y margen.

## 4) Colas y no-starvation

Orden lógico:

1. `HOUSEKEEPING`;
2. `COMMAND_ACK`;
3. `AI_BEHAVIOR_LOG`;
4. `LORA_LOG`;
5. `SCIENCE`;
6. `OPTIONAL_PAYLOAD`.

`HOUSEKEEPING` y `COMMAND_ACK` tienen prioridad estricta, pero también límites
de producción y frames acotados. Si crecen sin límite, el sistema entra en
fault en vez de consumir toda la pasada.

Las colas best-effort usan:

- reserva mínima configurable por producto crítico de misión;
- cuota máxima por contacto;
- aging/deadline para evitar starvation;
- prioridad dinámica por retención restante;
- preemption solo en frontera de frame/chunk;
- métricas de backlog, edad del dato y drops por causa.

`OPTIONAL_PAYLOAD` nunca consume la reserva de otra cola.

## 5) Productos LoRa

### 5.1 Resumen por ventana

Incluye:

- `protocol_version`, `pass_id`;
- start/end y time quality;
- TLE/source/hash y configuración RX;
- elevación estimada y su incertidumbre;
- `rx_total`, `crc_ok/fail`, `auth_ok/fail`, `replay/duplicate`;
- por nodo: counts, secuencia, RSSI/SNR/CFO con quality flags;
- configuración SF/BW/CR/canal;
- digest del catálogo/raw set.

El resumen va en `LORA_LOG`, no se disfraza como housekeeping. Una bandera
compacta de salud del experimento puede derivarse para beacon.

### 5.2 Catálogo

Índice versionado para selección:

- `node_id`, `boot_epoch`, rango `seq`;
- timestamp/time quality;
- estado CRC/auth/replay;
- offset/longitud en storage;
- digest del registro.

### 5.3 Raw/on-demand

Cada registro raw conserva bytes recibidos más metadata RF y provenance. La
transferencia es por chunks reanudables, con digest de objeto y ACK autenticado.

Un `node_id` autenticado no prueba ubicación física. La evidencia “originado en
Buenos Aires” requiere correlación con inventario, sitio y log TX local.

## 6) Producto de comportamiento IA

El producto es independiente del modelo candidato. Cada evento debe permitir
reproducir la inferencia y la decisión:

- event/decision ID;
- tiempo y quality;
- snapshot de entrada completo o referencia inmutable + digest;
- raw model output;
- modelo, revisión/digest, cuantización y runtime;
- prompt/policy digest;
- decoding, seed y parámetros;
- supervisor/guardrail version;
- recomendación, autorización/rechazo y razón;
- comando/acción efectivamente aplicada;
- estado/resultados posteriores;
- latencia, energía y temperaturas;
- OBC/CM5 firmware/configuration IDs.

`confidence` solo se conserva si tiene definición y calibración. No se usa un
número arbitrario como evidencia.

La demostración de `N` logs requiere probar:

- producción esperada;
- espacio y retención;
- contactos útiles;
- cuota mínima;
- transferencia íntegra;
- decodificación y correlación en ground.

## 7) Comandos de datos

Todos usan `04_Communications/uhf_command_security_protocol.md`:

- `LORA_SUMMARY_GET(pass_id)`;
- `LORA_NODE_CATALOG_GET(node_id, since)`;
- `LORA_NODE_DUMP(selector)`;
- `AI_LOG_CATALOG_GET(selector)`;
- `OBJECT_DOWNLOAD_REQUEST(object_id, range)`;
- `DL_SET_LIMITS(queue, quota)`;
- `ABORT`.

El OBC valida schema, rol, rangos y disponibilidad. Un comando no puede fijar
cuota negativa, eliminar reservas críticas ni seleccionar memoria fuera del
catálogo.

## 8) Persistencia a bordo

La arquitectura debe definir:

- record framing y schema versionados;
- append-only journal y recuperación tras power loss;
- boot/session ID;
- checksums/ECC;
- índices reconstruibles;
- política de wrap y protección de datos no descargados;
- wear/endurance;
- timestamps con quality;
- digest de objetos y chunks;
- counters de drop por causa.

No se elimina un producto requerido hasta recibir ACK de ground autenticado y
verificar la política de retención.

## 9) Ground y evidencia

Ground conserva:

- raw RF/IQ cuando aplique;
- frames pre/post decode;
- configuración de receptor/decoder;
- TLE, scheduler y time source;
- comandos/ACK;
- objetos/chunks y hashes;
- métricas de contacto;
- software/commit y calibraciones.

Una UI en memoria no es evidencia persistente. La adquisición debe escribir
raw append-only antes de alimentar dashboards y permitir replay determinista.

## 10) Seguridad, contenido y SatNOGS

- `PUBLIC_BEACON` es público y mínimo.
- `CONTROLLED_DOWNLINK` no es confidencial por nombre.
- Si se opera en amateur-satellite, waveform/framing/identificación/decoder se
  publican según el régimen.
- Productos que requieran secreto no se transmiten sin servicio/autorización
  compatible.
- Comandos y ACK usan autenticación sin cifrado hasta decisión distinta
  autorizada.

## 11) Criterio de cierre del data budget

El presupuesto cierra solo si un análisis reproducible demuestra, en caso
nominal y peor caso:

- producción diaria por ProductID;
- capacidad neta por contacto con PER/overhead;
- calendario de contactos bajo máscara operativa;
- backlog/retención y días sin contacto;
- reservas y ausencia de starvation;
- recuperación de todos los datos del criterio mínimo;
- margen explícito y sensibilidad a fallas.

El análisis debe citar commit, inputs, script, raw results y hash.

<!-- FEATURE:PHOTO_DEMO START -->

## 12) [PHOTO_DEMO]

`PHOTO_DEMO` permanece opcional, off-by-default y en `OPTIONAL_PAYLOAD`. Usa
solo capacidad residual, chunks reanudables y nunca reduce reservas de misión.

<!-- FEATURE:PHOTO_DEMO END -->

## 13) Referencias

- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/uplink_lora_slotted_protocol.md`
- `04_Communications/uhf_command_security_protocol.md`
- `04_Communications/satnogs_public_beacon_architecture.md`
- `04_Communications/ground_station_dual_use_satnogs_australis.md`
- `docs/COMMS/rf_calculations.py`
