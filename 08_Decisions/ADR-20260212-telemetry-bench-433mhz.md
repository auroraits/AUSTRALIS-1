# ADR-20260212-telemetry-bench-433mhz

## Contexto
Se requiere un banco de pruebas rápido para telemetría IMU usando hardware disponible (ESP32-S3 + FS1000A + RX433 + Arduino UNO) para validar empaquetado, conteo de pérdidas y logging CSV en tierra.

## Decisión
Adoptar un enlace **solo de laboratorio** en 433 MHz con `RadioHead RH_ASK` a 2000 bps para pruebas de integración SW/HW, separado del baseline orbital del MVP.

## Alternativas consideradas
1. LoRa/UHF orbital-like desde el inicio: mayor fidelidad, mayor complejidad de arranque.
2. Enlace serial cableado: simple pero no valida RF.
3. **Elegida:** ASK/OOK 433 MHz de bajo costo para prueba funcional temprana.

## Tradeoffs / riesgos
- Pro: implementación rápida, hardware económico, métricas de pérdida simples.
- Contra: baja inmunidad a ruido/interferencias, no representativo del enlace orbital final.

## Implicancias (archivos a actualizar)
- `05_Software/embedded/esp32_s3_tx_telemetry/telemetry_tx.ino`
- `05_Software/embedded/uno_rx_logger/rx_logger.ino`
- `05_Software/embedded/platformio.ini`
- `docs/TELEMETRY_433_README.md`
- `architecture.md`
- Impacto en costos/riesgos: **TBD** para cuantificación formal si este banco pasa a fase preintegración.

## Estado
Accepted
