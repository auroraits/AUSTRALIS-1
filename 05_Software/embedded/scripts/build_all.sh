#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
platformio run -e esp32s3_supermini_tx
platformio run -e uno_rx_logger
