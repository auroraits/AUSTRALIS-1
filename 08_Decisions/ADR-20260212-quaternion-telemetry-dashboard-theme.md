# ADR-20260212-quaternion-telemetry-dashboard-theme

## Contexto
El banco RF 433 MHz de laboratorio ya transmitía IMU cruda (`ax..gz`), pero la visualización 3D del dashboard estimaba actitud con aproximaciones Euler, introduciendo gimbal lock y poca estabilidad en pitch/roll. Se requiere enviar orientación fusionada y mejorar la UX del dashboard sin agregar toolchains pesados.

## Decisión
1. Extender el paquete de telemetría TX/RX para incluir quaternion `q0..q3` (float32) y `dt_ms` de debug en TX.
2. Implementar filtro Madgwick IMU (acelerómetro + giroscopio) local en firmware TX (`header-only`) con `MADGWICK_BETA=0.12` y ciclo de cálculo 100 Hz / envío RF 20 Hz.
3. Mantener compatibilidad en RX/dash con formato legacy de 8 campos y nuevo de 12 campos CSV.
4. Aplicar tema dark responsive y layout modernizado en Blazor con CSS variables (sin introducir Tailwind/npm), con toggle light/dark.
5. Renderizar orientación 3D consumiendo quaternion directo (`w,x,y,z` a Three.js `x,y,z,w`).

## Alternativas consideradas
1. **Mahony AHRS**: válido, pero se priorizó Madgwick por simplicidad y tuning directo con beta.
2. **Quaternion cuantizado int16 (Q15)**: menor payload, pero mayor complejidad y riesgo de errores de escala para MVP actual.
3. **Tailwind + pipeline npm**: look moderno, pero agrega toolchain extra no necesaria para el alcance actual.

## Tradeoffs / riesgos
- Pro: mejor estabilidad visual en pitch/roll, evita gimbal lock, pipeline más coherente entre firmware y dashboard.
- Contra: payload RF más grande (float32), mayor sensibilidad a throughput en ASK/OOK.
- Riesgo conocido: yaw drift por ausencia de magnetómetro (documentado y aceptado para banco).

## Implicancias (archivos a actualizar)
- `05_Software/embedded/esp32_s3_tx_telemetry/telemetry_tx/telemetry_tx.ino`
- `05_Software/embedded/uno_rx_logger/rx_logger/rx_logger.ino`
- `05_Software/embedded/common/filters/MadgwickAHRS.h`
- `05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Core/*`
- `05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web/*`
- `docs/TELEMETRY_433_README.md`
- `05_Software/GroundTelemetryDashboard/docs/README.md`
- `07_Risk/telemetry_433_bench_risks.md`
- `00_MVP/MVP v2.1.md`
- `README.md`
- `architecture.md`

## Estado
Accepted
