#!/usr/bin/env bash
set -euo pipefail

# Ejemplo de uso:
#   ./flash_examples.sh /dev/ttyACM0 /dev/ttyUSB0
ESP32_PORT="${1:-/dev/ttyACM0}"
UNO_PORT="${2:-/dev/ttyUSB0}"

cd "$(dirname "$0")/.."
python -m platformio run \
  --project-dir esp32_s3_tx_telemetry \
  -e esp32s3_supermini_tx \
  -t upload \
  --upload-port "$ESP32_PORT"
python -m platformio run \
  --project-dir uno_rx_logger \
  -e uno_rx_logger \
  -t upload \
  --upload-port "$UNO_PORT"
