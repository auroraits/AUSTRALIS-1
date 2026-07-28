# ADR-20260727-telemetry-bench-433-v4

- **Fecha:** 2026-07-27
- **Estado:** Accepted
- **Alcance:** banco terrestre; no evidencia de RF/ADCS orbital

## Contexto

El paquete histórico de 41 bytes a RH_ASK 2000 bit/s requiere al menos 164 ms
solo para sus bits. La configuración documentada de 20 Hz RF era físicamente
imposible y `waitPacketSent()` bloqueaba el filtro. El remapeo por signos podía
tener determinante −1 y el filtro Madgwick IMU terrestre no es una referencia
de actitud en caída libre.

## Decisión

1. Mantener el banco ASK/OOK 433 MHz únicamente para integración temprana.
2. Filtrar IMU a objetivo 100 Hz con envío RF no bloqueante.
3. Configurar telemetría RF a objetivo **2 Hz**, sujeto a medición real de
   `busy/dropped/PER`.
4. Versionar frame V4 con `boot_id` y `quality_flags`.
5. Calcular PER/gaps por boot/session y contabilizar duplicates/out-of-order.
6. Representar sensor→body mediante matriz ortonormal con determinante `+1`;
   usar identidad hasta medir/documentar montaje.
7. Aplicar corrección del acelerómetro Madgwick solo en banco cuando la norma
   está entre `0.5 g` y `1.5 g`.
8. Prohibir explícitamente usar este estimador como evidencia de ADCS orbital:
   en caída libre el acelerómetro no proporciona referencia gravitatoria.
9. El retorno local de `send()` no indica pérdida de canal; el trigger RF es
   PER/gaps/dropped en RX.

## Evidencia requerida

- build reproducible de TX/RX;
- captura con tasa de filtro/RF observadas;
- fixtures boot/wrap/duplicate/out-of-order;
- tests de matriz/quaternion;
- log de calidad y PER end-to-end.

## Implicancias

- `docs/TELEMETRY_433_README.md`
- `07_Risk/telemetry_433_bench_risks.md`
- firmware TX/RX y dashboard parser/stats
