# Riesgos — Banco de telemetría 433 MHz

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|---|
| R-433-01 | Alta interferencia en 433 MHz en laboratorio | Media | Media | Reducir distancia, mejorar antena 1/4 onda, filtrar fuente, repetir pruebas por franjas horarias | >20% `dropped` sostenido |
| R-433-02 | Alimentación ruidosa en FS1000A/RX433 degrada enlace | Alta | Media | Desacople 10uF + 100nF cerca de módulos, masa común corta | TX `status=fail` frecuente |
| R-433-03 | Desalineación de pines/board en ESP32-S3 | Media | Media | Mantener pines configurables y checklist de cableado | No inicia I2C o no hay tramas RX |
| R-433-04 | Confusión entre banco 433 y arquitectura orbital | Baja | Alta | Documentar explícitamente “solo laboratorio” + ADR | Uso de esta configuración fuera de banco |
| R-433-05 | Deriva de yaw por filtro IMU sin magnetómetro | Alta | Baja-Media | Documentar limitación, calibrar bias gyro, usar yaw solo para tendencia | Giro en yaw acumula error en pruebas largas |
| R-433-06 | Mismatch de ejes/frame entre IMU y modelo 3D | Media | Media | Remapeo explícito de ejes en TX + zero reference en dashboard + HUD/axis debug | Roll/pitch invierten signo al mover en pruebas manuales |

## Riesgo residual
- Residual actual: Medio (aceptable para validación temprana de banco).

## Referencia
- `08_Decisions/ADR-20260212-telemetry-bench-433mhz.md`.
- `08_Decisions/ADR-20260212-quaternion-telemetry-dashboard-theme.md`.
- `08_Decisions/ADR-20260212-imu-frames-and-calibration.md`.
