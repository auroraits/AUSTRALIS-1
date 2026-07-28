# UHF TTC — perfil de autenticación y anti-replay

**Revisión:** 2026-07-27
**Estado:** Proposed — requisito de seguridad; suite criptográfica y encoding TBD
**Trazabilidad:** `04_Communications/regulatory_gate_rf.md`, `04_Communications/rf_subsystem_overview.md`

## 1) Propósito y límites

Definir las propiedades mínimas del uplink TTC antes de seleccionar encoding o
algoritmo. El objetivo es autenticar origen, proteger integridad y rechazar
replay **sin ocultar el contenido RF**.

Este documento no:

- selecciona una suite criptográfica;
- autoriza cifrado/confidencialidad;
- publica ni almacena claves;
- reemplaza el supervisor determinístico del OBC;
- convierte el uplink en requisito para alcanzar SAFE local.

## 2) Invariantes de seguridad

1. Ningún comando produce efecto antes de autenticación, validación de replay,
   autorización por rol y validación semántica.
2. CRC solo detecta errores de canal; no autentica.
3. Un hash sin clave solo prueba integridad accidental; no origen.
4. `auth=VALID`, `safety_class` o permisos declarados por el emisor no son
   confiables; el OBC los deriva de su catálogo local.
5. El contador anti-replay sobrevive reset y pérdida de energía.
6. El comando y sus argumentos permanecen legibles en RF.
7. SAFE autónomo, watchdog y power-off crítico no dependen del enlace.
8. Una clave comprometida puede revocarse sin aceptar comandos sin autenticar.

## 3) Envelope lógico autenticado

El encoding binario exacto queda `TBD`, pero el objeto autenticado completo
contiene:

| Campo | Propósito | Regla |
|---|---|---|
| `protocol_version` | Evolución incompatible | versión soportada o reject |
| `mission_id` | Separación de dominio | debe coincidir AUSTRALIS-1 |
| `spacecraft_id` | Evitar cross-command | debe coincidir |
| `key_epoch` | Selección de clave/rol | epoch activo o de transición |
| `role_id` | Catálogo de permisos | se resuelve localmente |
| `counter` | Anti-replay | entero monotónico persistente |
| `command_id` | Correlación e idempotencia | único por epoch |
| `issued_at` | Auditoría | no sustituye counter |
| `expires_at` | Limitar validez | requiere time quality suficiente |
| `command_type` | Operación solicitada | allowlist local |
| `arguments` | Parámetros | schema por comando |
| `payload_digest` | Objetos/chunks | obligatorio cuando aplique |
| `auth_tag` | MAC o firma | cubre todos los campos anteriores |

El tag se calcula sobre una serialización canónica versionada. No se permite
que campos de routing, tipo, contador, argumentos o digest queden fuera de la
cobertura autenticada.

## 4) Suite criptográfica

La suite final debe:

- usar un MAC estándar con clave o firma digital estándar;
- tener separación de dominio por misión, spacecraft, dirección y propósito;
- evitar algoritmos caseros;
- definir tamaño de tag, serialización y test vectors;
- demostrar costo temporal/energético y resistencia a fallas;
- recibir revisión independiente y confirmación regulatoria.

Candidatos como AES-CMAC, HMAC-SHA-256 truncado o una firma moderna pueden
evaluarse, pero **ninguno queda adoptado por este documento**. La elección
requiere ADR de seguridad, threat model y prueba en el OBC exacto.

## 5) Anti-replay persistente

### 5.1 Regla base

Para cada `(key_epoch, role_id)` el OBC conserva un `high_water_counter`.
Un comando se acepta solo si:

1. el tag es válido;
2. `counter > high_water_counter`;
3. epoch, rol, expiración y schema son válidos;
4. el catálogo local autoriza el comando;
5. las precondiciones operativas se cumplen.

Luego se reserva/commitea el nuevo contador de forma power-fail-safe **antes**
de producir un efecto no idempotente.

### 5.2 Persistencia

La implementación debe usar journal de dos fases, slots redundantes u otro
mecanismo atómico con:

- CRC/ECC de almacenamiento;
- generación/versión;
- detección de rollback/corrupción;
- endurance presupuestada;
- recuperación conservadora: si el estado es ambiguo, no se acepta el comando.

Boot counter, reloj o `seq` de radio no sustituyen el contador monotónico.

### 5.3 Reordenamiento

El perfil inicial usa orden estricto. Si se necesita una ventana para frames
fuera de orden, la ventana y bitmap deben persistirse con las mismas garantías.
No se habilita una ventana solo por conveniencia del enlace.

## 6) Catálogo local de comandos

Cada `command_type` tiene en firmware OBC:

- schema de argumentos con tipos, rangos y `additionalProperties=false`;
- rol mínimo;
- safety class derivada localmente;
- precondiciones de `MISSION_MODE`, `EPS_STATE`, fase, temperatura y enlace;
- efecto idempotente o estrategia de deduplicación;
- timeout y ACK/NACK;
- log obligatorio.

Ejemplos de reglas:

- `POWER_SET` no puede habilitar cargas prohibidas por EPS/Fault Manager;
- `SET_MODE` no anula la transición autónoma a SAFE;
- `ABORT` requiere autenticación, pero el OBC mantiene vías locales de SAFE;
- `DL_SET_LIMITS` no puede eliminar mínimos de housekeeping/ACK;
- comando desconocido, argumento ausente/sobrante o valor fuera de rango es
  hard-fail.

## 7) Objetos grandes y prompts

Upload y activación son operaciones separadas:

1. `OBJECT_UPLOAD_BEGIN` autenticado fija tipo, versión, longitud y digest;
2. cada chunk lleva ID, offset, longitud, CRC de transporte y autenticación;
3. el objeto incompleto permanece inactivo;
4. al finalizar se verifica longitud y digest criptográfico;
5. `OBJECT_ACTIVATE` autenticado referencia el digest exacto;
6. el supervisor valida compatibilidad y condiciones antes de activar;
7. rollback seguro conserva una versión conocida.

Para prompts:

- contenido y versión se registran completos;
- el hash solo identifica el prompt; el comando autenticado prueba origen;
- ninguna carga de prompt cambia guardrails determinísticos;
- cada inferencia registra digest de prompt/modelo/supervisor.

## 8) Gestión de claves

Requisitos:

- claves por rol, entorno y spacecraft; no una clave universal de flota;
- generación con fuente adecuada y entrega fuera del repositorio;
- almacenamiento protegido en ground y OBC;
- backup/recovery con control dual;
- rotación en dos fases `STAGE` → `ACTIVATE`;
- período de solapamiento explícito y acotado;
- revocación por epoch;
- procedimiento ante pérdida/compromiso;
- cero claves, seeds o tags reales en logs públicos.

La recuperación no introduce una contraseña maestra transmitida en claro. Una
clave de contingencia, si se adopta, permanece deshabilitada/protegida y se
ensaya con el mismo rigor.

## 9) ACK y auditoría

Todo ACK/NACK incluye y autentica:

- `command_id`, `counter`, `key_epoch`;
- resultado (`accepted`, `rejected`, `duplicate`, `expired`, etc.);
- razón normalizada sin filtrar secretos;
- timestamp/time quality;
- estado antes/después o hash correlacionable;
- versión de firmware/catálogo.

Ground conserva raw frame, decisión, operador/rol, archivo transmitido, ACK,
efecto esperado y evidencia posterior. No se registra material de clave.

## 10) Framing y transporte

CRC, FEC, interleaver, ARQ y fragmentación son capas de transporte:

- el receptor valida framing/CRC antes de criptografía;
- la autenticación cubre el mensaje reensamblado canónico;
- fragmentos duplicados no causan múltiples efectos;
- timeout o reensamblado incompleto no avanzan el contador de aplicación;
- límites de tamaño, memoria, número de fragmentos y tiempo son explícitos.

## 11) Compatibilidad regulatoria

El perfil es **autenticación sin cifrado**:

- cabeceras, comando y argumentos permanecen visibles;
- no se usa encryption para ocultar contenido;
- la waveform y el framing se documentan públicamente cuando corresponda;
- el `auth_tag` no debe interpretarse como permiso regulatorio automático.

Antes de vuelo, ENACOM debe confirmar por escrito el tratamiento de la suite,
identificación, contenido y operación amateur-satellite. Si exige otro
encuadre, el diseño debe adaptarse.

## 12) Verificación obligatoria

La suite no se considera implementada sin:

- test vectors positivos y negativos;
- tag corrupto, truncado y de otra misión;
- counter repetido, menor, salto y reordenamiento;
- reset/power-cut en cada punto de persistencia;
- epoch vigente, anterior, futuro y rotación;
- argumentos faltantes/sobrantes/fuera de rango;
- roles insuficientes;
- upload incompleto/digest erróneo/activación indebida;
- fuzzing del parser;
- timing/memoria/energía worst-case;
- revisión independiente del diseño y código.

Los casos críticos exigen 100 % de rechazo correcto; no se admiten mismatches
“cosméticos”.

## 13) TBD que requieren decisión

- threat model formal;
- suite y tamaños;
- formato binario canónico;
- primitive/storage seguro del OBC;
- roles y matriz de permisos;
- política de time quality/expiry;
- mecanismo de rotación y contingencia;
- impacto regulatorio escrito;
- ProcedureID y EvidenceID de la campaña.

