# UHF TTC — plan de verificación de banco, OTA y end-to-end

**Revisión:** 2026-07-27  
**Estado:** Draft — criterios numéricos pendientes de asignación previa al test  
**Trazabilidad:** `04_Communications/link_budget_uhf_preliminary.md`, `04_Communications/rf_subsystem_overview.md`

## 1) Objetivo

Convertir el link budget bidireccional UHF en evidencia reproducible y
demostrar que la waveform, antena, seguridad y estación terrena funcionan como
un sistema. Ningún resultado de este plan autoriza una emisión radiada.

## 2) Precondiciones

Antes de ejecutar un test con radiación:

- `REG-UHF-AMATEUR` cerrado para la configuración y sitio;
- frecuencia, potencia, occupied bandwidth e identificación autorizados;
- procedimiento aprobado, operador habilitado y zona RF segura.

Antes de cualquier test:

- artículo y configuración identificados;
- software/firmware, parámetros y commit registrados;
- instrumentos dentro de calibración;
- límites de protección de DUT, atenuadores, LNA y SDR calculados;
- criterios cuantitativos y tamaño de muestra congelados;
- raw data, timestamps UTC, unidades y hashes definidos.

Los ensayos conducidos deben usar atenuadores/dummy load o caja apantallada para
evitar emisiones no autorizadas.

## 3) Instrumentación mínima

- generador RF vectorial o generador + modulador con potencia trazable;
- analizador de espectro con detector/configuración registrados;
- power meter y sensores adecuados al rango;
- atenuadores, acopladores, terminaciones y cables caracterizados;
- emulador de Doppler o playback IQ;
- cámara térmica o recinto para esquinas de temperatura;
- SDR/radio terrestre y radio orbital candidatos;
- fuente programable con captura de corriente/inrush;
- fixtures conducidos y, para OTA, cámara/área calibrada.

Cada corrida debe registrar modelos, números de serie, fecha de calibración y
la pérdida medida de cada cable/fixture.

## 4) Matriz de pruebas

| ID | Prueba | Método | Criterio a congelar | Evidencia |
|---|---|---|---|---|
| UHF-01 | Potencia TX y EIRP | Conducted + patrón | min/nom/max por V/T | CSV, espectro, calibración |
| UHF-02 | Sensibilidad RX | Potencia escalonada | PER/BER objetivo e IC | frames y curva PER |
| UHF-03 | Uplink completo | Ground TX→orbital RX | PER y ACK autenticado | raw frames/logs |
| UHF-04 | Downlink completo | Orbital TX→ground RX | PER por nivel | raw frames/logs |
| UHF-05 | Doppler | Rampa ±envolvente | adquisición y PER | perfil aplicado + logs |
| UHF-06 | Error de reloj | Doppler + ppm + V/T | margen de adquisición | frecuencia medida |
| UHF-07 | Espectro | TX peor caso | máscara/armónicos/espurias | screenshots + CSV |
| UHF-08 | OTA patrón | Satélite integrado | realized gain/polarización | patrón 3D |
| UHF-09 | Coexistencia | Matriz de agresores | degradación asignada | NF/PER/espectro |
| UHF-10 | Half-duplex | TX/RX switching | protección + tiempo | power/SWR/event log |
| UHF-11 | Seguridad | comandos válidos/adversos | 100 % reglas críticas | corpus y verdicts |
| UHF-12 | End-to-end | OBC↔RF↔ground | producto+ACK persistidos | evidence bundle |

## 5) Sensibilidad, BER y PER

La sensibilidad no se declarará como un único valor de datasheet. Para cada
waveform:

1. fijar tamaño y distribución de frames;
2. aplicar al menos los niveles que cubran transición completa de PER;
3. transmitir el `N` preregistrado por nivel;
4. registrar recibidos, CRC fail, duplicados, fuera de orden y timeouts;
5. reportar intervalo Wilson 95 % y no solo porcentaje puntual;
6. repetir en tensión/temperatura y con interferencia relevante.

El umbral de sensibilidad será el nivel que cumpla el PER preregistrado con la
confianza requerida, no el primer paquete recibido.

## 6) Doppler y waveform

La prueba debe aplicar una rampa representativa del perfil orbital, no solo
offsets estáticos. La envolvente incluye:

- `±11.25 kHz` cinemático de referencia a 438 MHz/7.7 km/s;
- error y deriva térmica de TX y RX;
- error de precompensación/TLE y latencia del scheduler.

Se ensayarán adquisición inicial, pérdida/recuperación de lock y PER durante la
rampa. La configuración exacta debe registrar desviación FSK, filtro, AFC,
preámbulo, sync, whitening, FEC, interleaver y bitrate.

## 7) Antena OTA

El artículo OTA debe representar estructura, paneles, harness, despliegue y
plano de masa. Se medirá:

- ganancia realizada 3D por polarización;
- nulls y percentiles sobre actitudes de CONOPS;
- axial ratio si aplica;
- detuning/S11 en stowed y deployed;
- efecto de cables, paneles y tolerancias;
- repetibilidad antes y después de ambiente.

El resultado alimenta el link budget como pérdida/distribución, no como
“0 dBi” nominal.

## 8) EMC y coexistencia

Ejecutar cada receptor en su nivel de transición de PER mientras se activan:

- UHF TX en potencia/frecuencia extrema;
- LoRa RX y clocks del concentrador;
- CM5 en inferencia/carga máxima;
- EPS/MPPT/DC-DC en modos y cargas extremas;
- storage, buses y actuadores.

Medir noise floor, desense, blocking, intermodulación, espurias, PER y corriente.
No se permite simultaneidad operacional si la degradación excede el margen
preasignado.

## 9) Seguridad y anti-replay

La campaña UHF-11 debe cubrir:

- tag correcto/incorrecto/truncado;
- contador nuevo, repetido, menor y saltos;
- reset y pérdida de energía entre recepción y commit del contador;
- epoch vigente, anterior, futuro y recuperación controlada;
- frame reordenado, duplicado, modificado o de otra misión;
- expiración, comando desconocido y argumentos fuera de rango;
- upload incompleto, digest incorrecto y activación de prompt no autorizada;
- ACK autenticado y correlacionado;
- pérdida de estación sin degradar la autonomía SAFE local.

Las reglas críticas son hard-fail: ningún comando no autenticado o replay puede
producir efecto.

## 10) Ground end-to-end

La prueba debe incluir:

- TLE/orbit data autenticado o con provenance verificada;
- scheduler y rotor con error inyectado;
- hardware arm + PTT gate;
- TX/RX switching;
- decoder y almacenamiento raw append-only;
- comando autenticado, efecto OBC simulado y ACK autenticado;
- fallo de red, proceso, reloj, power/SWR y watchdog.

El servicio de adquisición no debe depender de CDN ni aceptar control LAN sin
autenticación.

## 11) Paquete mínimo de evidencia

Cada `EvidenceID` contiene:

- propósito, requisito y criterio previo;
- DUT/EGSE/configuración;
- procedimiento y desviaciones;
- raw data inmutable;
- script/notebook versionado;
- resultados e intervalo de confianza;
- fotos/diagramas de setup;
- calibraciones;
- commit y hashes SHA-256;
- responsable, fecha y revisión independiente.

Un test exploratorio sin criterio previo se conserva como exploratorio y no
cierra un requisito.

