#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/validate_telemetry_bench.py
python -m platformio run --project-dir esp32_s3_tx_telemetry -e esp32s3_supermini_tx
python -m platformio run --project-dir uno_rx_logger -e uno_rx_logger
