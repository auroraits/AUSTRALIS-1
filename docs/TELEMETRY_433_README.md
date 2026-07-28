# Telemetry Bench 433 MHz — V4

**Revisión:** 2026-07-27
**Estado:** Active — banco terrestre, no orbital

## Alcance

Banco ESP32-S3 + IMU + TX ASK/OOK 433 MHz → RX/UNO → ground dashboard. Sirve
para validar framing, sesión, quality flags, pérdida y visualización. No valida
TTC UHF, patrón orbital, Doppler, microgravedad ni ADCS.

## Configuración vigente

- RadioHead `RH_ASK`: 2000 bit/s.
- Filtro IMU: objetivo 100 Hz.
- Telemetría RF: objetivo **2 Hz**.
- Envío: no bloqueante para que RF no detenga el filtro.
- Frame: V4, con `boot_id` y `quality_flags`.

El frame histórico de 41 bytes necesita `41×8/2000 = 164 ms` antes de overhead
de framing/codificación. Por eso 20 Hz era imposible. Dos hertz dejan margen y
deben verificarse con timestamps y contadores; no se declaran validados sin log.

## Métricas

RX/ground deben distinguir:

- sesión y `boot_id`;
- sequence gap;
- duplicate;
- out-of-order;
- wrap;
- malformed/CRC/quality flags;
- `busy/dropped` TX cuando corresponda.

El retorno local de `send()` no mide el canal RF. Fuente/ruido/interferencia se
evalúan con PER/gaps/dropped end-to-end.

## Frames y actitud

- `sensor→body` es una matriz ortonormal con determinante `+1`.
- Se usa identidad hasta medir la orientación física del montaje.
- Quaternion se valida por finitud y norma.
- La corrección accel de Madgwick se admite solo si `0.5 g ≤ |a| ≤ 1.5 g`.
- En órbita/caída libre el acelerómetro no es una referencia gravitatoria; este
  estimador **no puede citarse como solución ni evidencia ADCS orbital**.

## Validación mínima

1. build TX/RX reproducible;
2. filtro observado cercano a 100 Hz bajo RF activo;
3. RF observada cercana a 2 Hz sin bloquear;
4. power-cycle cambia `boot_id`;
5. fixtures de gap/duplicate/out-of-order/wrap;
6. matriz `RᵀR=I`, `det(R)=+1`;
7. quaternion finite/norm;
8. pérdida por fuente/interferencia visible en métricas RX.

## Referencias

- `../08_Decisions/ADR-20260727-telemetry-bench-433-v4.md`
- `../07_Risk/telemetry_433_bench_risks.md`
- `../05_Software/embedded/platformio.ini`
