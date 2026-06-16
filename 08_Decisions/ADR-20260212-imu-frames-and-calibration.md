# ADR-20260212-imu-frames-and-calibration

## Contexto
La rotación visual del widget 3D no coincidía con el movimiento real del módulo GY-521 (MPU6050). El problema combinaba bias de gyro, posibles signos/ejes inconsistentes y falta de referencia visual de cero.

## Decisión
1. Mantener Madgwick IMU y agregar calibración de bias gyro en boot + comando runtime (`CAL`/`RECAL`).
2. Definir remapeo explícito sensor->body en TX con constantes de signo editables.
3. Versionar paquete RF (V3) con `magic/version/sensor_type` para robustez.
4. En dashboard, aplicar quaternion en orden Three.js correcto (`qx,qy,qz,qw`).
5. Agregar zero visual en UI: `q_display = inverse(q_ref) * q_current` con persistencia local.
6. Agregar controles de cámara (OrbitControls), modo follow y herramientas debug (HUD + axis debug).

## Alternativas consideradas
- Resolver solo en frontend con offsets visuales: insuficiente para bias y consistencia de frame.
- Cambiar a Mahony: no necesario para resolver mismatch actual.

## Tradeoffs / riesgos
- Pro: alineación reproducible entre sensor real y visualización.
- Contra: más campos en paquete V3 y configuración adicional de signos.
- Riesgo residual: yaw drift por ausencia de magnetómetro.

## Implicancias (archivos a actualizar)
- `05_Software/embedded/esp32_s3_tx_telemetry/telemetry_tx/telemetry_tx.ino`
- `05_Software/embedded/uno_rx_logger/rx_logger/rx_logger.ino`
- `05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web/wwwroot/js/dashboard.js`
- `05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web/Pages/Index.razor`
- `05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web/Pages/_Host.cshtml`
- `docs/TELEMETRY_433_README.md`
- `05_Software/GroundTelemetryDashboard/docs/README.md`
- `architecture.md`

## Estado
Accepted
