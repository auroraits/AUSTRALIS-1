# Uplink LoRa — protocolo slotted experimental

**Revisión:** 2026-07-27
**Estado:** Proposed / regulatory-blocked
**Trazabilidad:** `04_Communications/regulatory_gate_rf.md`, `04_Communications/link_budget_lora_uplink_preliminary.md`

## 1) Estado operacional

El protocolo estudia recepción orbital desde nodos de bajo costo. No habilita
operación radiada.

Hasta cerrar `REG-LORA-915`:

- B1 y B2 se ejecutan solo en coax, caja apantallada o simulación;
- no se emite de forma intencional hacia el satélite;
- no hay canal, potencia ni duty cycle adoptados;
- el objetivo de paquetes desde Buenos Aires permanece bloqueado.

Que el satélite sea RX-only no autoriza al transmisor terrestre.

## 2) Clase de nodo

Clase de referencia, no SKU:

- radio SX1262/SX1276 o equivalente;
- MCU ESP32-S3 o equivalente;
- +20 a +21 dBm, sin PA externo;
- antena simple 0–2 dBi, no direccional;
- cristal comercial ±10 ppm; no se presupone TCXO;
- credencial única por nodo para autenticación.

La selección final debe registrar radio, front-end, reloj, antenna, firmware,
consumo y condiciones regulatorias exactas.

## 3) Modos candidatos

### 3.1 B1 — slotted periódico

El nodo transmite en epochs periódicas sin conocer pasadas. Este modo puede
consumir airtime/energía y causar interferencia continua. **No es fallback
operacional automático**: requiere evaluación y autorización específicas.

### 3.2 B2 — pass-aware slotted

El nodo transmite solo dentro de una ventana calculada a partir de datos
orbitales, sitio y tiempo UTC.

Requiere:

- TLE/elementos orbitales con provenance e identidad del objeto;
- propagador y versión registrados;
- error de predicción y edad máxima derivados de mediciones;
- base temporal dentro del presupuesto;
- ventana recortada por elevación y autorización, no “6 min” fija;
- inhibición si cualquier entrada es inválida o incierta.

B2 reduce airtime fuera de pasada; no mejora link budget ni elimina colisiones.

## 4) PHY candidato

Parámetros para ensayos iniciales:

- LoRa SF12;
- Coding Rate 4/5;
- header explícito;
- CRC PHY habilitado;
- preámbulo 16 símbolos;
- BW125 y BW250 como alternativas;
- payload real `TBD` después de agregar identidad y autenticación.

BW125 aporta mayor sensibilidad de referencia. BW250 aporta mayor tolerancia a
Doppler/CFO a costa de sensibilidad. Ninguno queda adoptado sin evidencia.

### 4.1 Time-on-Air reproducible

Para **12 bytes de payload legado**, Low Data Rate Optimization activa y los
parámetros anteriores:

| BW | ToA exacto de referencia |
|---:|---:|
| 125 kHz | 1.417216 s |
| 250 kHz | 0.708608 s |

Los valores históricos 1.155 s/0.496 s correspondían a otras condiciones de
preámbulo y eran incorrectos para preámbulo 16.

El frame autenticado será mayor a 12 bytes. Por lo tanto, estos ToA **no pueden
dimensionar la configuración final**. Se recalcularán con el payload serializado
exacto usando `docs/COMMS/rf_calculations.py`.

## 5) Canalización

No hay centros de canal adoptados. El plan final debe:

- estar dentro de la autorización escrita;
- usar occupied bandwidth medido, no solo BW nominal;
- incluir tolerancia de osciladores y Doppler;
- impedir solapamiento entre canales que pretendan diversidad;
- considerar selectividad, canal adyacente, blocking e interferencia local.

Los antiguos centros 915.2/915.4 MHz, separados 200 kHz, no sirven como dos
canales independientes si se usa BW250: sus anchos nominales se solapan 50 kHz.

El plan de BW125 y el de BW250 serán artefactos distintos. Un cambio de BW
obliga a recalcular centros, guards, ToA, capacidad, sensibilidad y permiso.

## 6) Slot y guard

Definiciones:

- `ToA_max`: peor ToA de la configuración y longitud máxima autorizada;
- `guard_total`: error total presupuestado antes/después del paquete;
- `slot_len = ToA_max + guard_total`;
- el firmware debe garantizar que el paquete completo queda dentro del slot.

Ejemplo histórico de 12 bytes en una ventana de 240 s:

| BW | ToA | Guard total de estudio | Slot | Slots completos |
|---:|---:|---:|---:|---:|
| 125 kHz | 1.417216 s | 0.500 s | 1.917216 s | 125 |
| 250 kHz | 0.708608 s | 0.300 s | 1.008608 s | 237 |

Los guards son hipótesis de estudio, no criterios aceptados. Deben derivarse de
errores medidos de RTC, GNSS, scheduler, propagación y latencia.

No se usa jitter `±guard/3` sin límites: puede invadir el slot vecino. Si se
adopta dither, su intervalo permitido se define dentro del guard y se verifica
formalmente que `tx_start >= slot_start` y `tx_end <= slot_end`.

## 7) Selección de slot y colisiones

El algoritmo debe estar completamente especificado y versionado. Propuesta de
ensayo:

```text
seed = SHA-256(
  "AUSTRALIS-LORA-SLOT-v1" ||
  mission_id || network_id || node_id ||
  boot_epoch || seq || pass_id || retry_index ||
  channel_plan_version
)
slot_index = uint32_be(seed[0:4]) mod S
```

SHA-256 aquí distribuye slots; **no autentica**. La autenticación usa la
credencial del nodo.

Incluir `retry_index` y canal evita que un par que colisionó repita
necesariamente el mismo slot. Aun así se debe modelar la correlación real.

Con `N` nodos y `S` slots uniformes, la probabilidad ideal de que un intento no
colisione es:

\[
P_{solo}=(1-1/S)^{N-1}
\]

Para `N=100`, `S=125`, es aproximadamente 45 %. Dos intentos independientes
darían alrededor de 70 % de al menos un éxito, pero independencia, captura,
near-far y PDR físico no están garantizados. La capacidad final requiere
Monte Carlo + ensayo.

## 8) Frame lógico autenticado

El frame legado de 12 bytes (`node_id`, `seq`, sensores) no prueba origen,
misión, versión ni replay. El frame candidato contiene:

| Campo | Función |
|---|---|
| `protocol_version` | Parsing y evolución |
| `mission_id` / `network_id` | Separación de dominio |
| `message_type` | METEO/GNSS/STATUS |
| `node_id` | Identidad provisionada |
| `key_epoch` | Rotación/revocación |
| `boot_epoch` | Distinguir resets sin reutilizar nonce |
| `seq` | Orden y anti-replay por nodo |
| `time_quality` / `timestamp` | Correlación; no única defensa |
| `payload_len` / `payload` | Datos tipados y versionados |
| `auth_tag` | MAC o firma sobre header + payload |

El CRC PHY detecta corrupción; el `auth_tag` autentica. El contenido permanece
en claro. Algoritmo, tamaño del tag y encoding quedan `TBD` mediante revisión de
seguridad y dictamen regulatorio.

### 8.1 Anti-replay de nodos

El receptor mantiene por `(node_id, key_epoch)`:

- último `boot_epoch` aceptado;
- ventana de `seq` y bitmap si admite reordenamiento;
- estado persistente o política explícita de reconstrucción;
- contadores de duplicate/replay/auth fail.

`boot_epoch` debe ser monotónico persistente o único con mecanismo demostrado.
Un reset que vuelva a cero no se acepta silenciosamente.

### 8.2 Ubicación de origen

Un MAC prueba que transmitió una credencial, **no que el transmisor estaba en
Buenos Aires**. La evidencia del criterio de misión debe correlacionar:

- inventario/provisioning del nodo;
- sitio de prueba y responsable;
- tiempo UTC;
- logs TX locales firmados o preservados;
- predicción de pasada;
- frame recibido/ACK de evidencia.

No se infiere ubicación física solo de `node_id`.

## 9) Base temporal y datos orbitales

B2 requiere un presupuesto completo:

```text
error_total =
  error_reloj_nodo
  + error_sincronizacion
  + error_propagador/TLE
  + latencia_scheduler
  + incertidumbre_ejecucion
```

El nodo debe almacenar junto al schedule:

- source URL/provider;
- object/catalog ID;
- epoch orbital;
- `fetched_at`;
- hash y firma/provenance disponibles;
- versión del parser/SGP4;
- ventana de validez derivada de medición;
- error predicho en tiempo/elevación.

HTTPS protege transporte, pero no sustituye firma/provenance, object ID,
expiry ni rollback protection. Los umbrales de 7/30 días no se adoptan sin
convertir edad de TLE en error de ventana para la órbita real.

Si el error puede llevar la transmisión fuera de la ventana autorizada o del
slot, el nodo no transmite. B1 no se activa automáticamente.

## 10) Receptor orbital y logging

La comparación concentrador vs single-channel debe medir:

- sensibilidad absoluta por SF/BW/CR;
- tolerancia a rampa Doppler/CFO;
- número real de demoduladores/canales para la configuración;
- blocking, near-far, canal adyacente y co-canal;
- consumo e inrush;
- ruido/EMC con UHF, EPS y CM5;
- disponibilidad del front-end, TCXO y filtros;
- logging de RSSI/SNR/CFO y sus calibraciones.

Por paquete se conserva raw frame, resultado CRC/auth/replay, timestamp/time
quality, RF metrics, receptor/configuración y `pass_id`.

## 11) Criterio de adopción

Antes de adoptar B1/B2, BW o canalización:

- `REG-LORA-915` cerrado;
- PDR/PER y confianza preregistrados;
- cantidad de nodos/carga/retries definida;
- simulación de colisiones y ensayo multi-node;
- sensibilidad y Doppler medidos;
- seguridad/autenticación validada;
- data budget y retención cerrados;
- evidencia raw/versionada/hasheada.

## 12) Puntos abiertos

- banda/servicio autorizado o alternativa;
- receptor y antena orbital;
- BW/canales/occupied bandwidth;
- tamaño y encoding del frame autenticado;
- suite de autenticación/provisioning;
- capacidad máxima y política de retries;
- elevación/ventana derivada de evidencia;
- estrategia de TLE/timebase.

## 13) Referencias

- `04_Communications/regulatory_gate_rf.md`
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `04_Communications/uplink_data_products_and_downlink_policy.md`
- `docs/COMMS/uplink_lora_bench_testing_plan.md`
- `docs/COMMS/rf_calculations.py`
