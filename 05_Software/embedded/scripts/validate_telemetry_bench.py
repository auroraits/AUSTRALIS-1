#!/usr/bin/env python3
"""Static, deterministic checks for the versioned 433 MHz bench protocol."""

from __future__ import annotations

import re
from pathlib import Path


EMBEDDED = Path(__file__).resolve().parents[1]
TX = EMBEDDED / "esp32_s3_tx_telemetry" / "telemetry_tx" / "telemetry_tx.ino"
RX = EMBEDDED / "uno_rx_logger" / "rx_logger" / "rx_logger.ino"


def require(pattern: str, text: str, label: str) -> re.Match[str]:
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Missing {label}")
    return match


def main() -> int:
    tx = TX.read_text(encoding="utf-8")
    rx = RX.read_text(encoding="utf-8")

    bitrate = int(require(r"RH_ASK\s+ask\((\d+)", tx, "ASK bitrate").group(1))
    tx_period_us = int(require(r"TX_DT_US\s*=\s*(\d+)UL", tx, "TX period").group(1))
    filter_period_us = int(require(r"FILTER_DT_US\s*=\s*(\d+)UL", tx, "filter period").group(1))
    struct_body = require(
        r"struct\s+TelemetryPacket\s*\{(.*?)\};",
        tx,
        "TelemetryPacket",
    ).group(1)

    type_sizes = {
        "uint8_t": 1,
        "uint16_t": 2,
        "uint32_t": 4,
        "int16_t": 2,
        "float": 4,
    }
    fields = re.findall(
        r"^\s*(uint8_t|uint16_t|uint32_t|int16_t|float)\s+\w+\s*;",
        struct_body,
        flags=re.MULTILINE,
    )
    payload_bytes = sum(type_sizes[field_type] for field_type in fields)

    # RadioHead ASK uses 4-to-6 encoding: 12 bits per frame byte. Account for
    # count/headers/CRC (7 bytes) and eight 6-bit preamble symbols.
    estimated_frame_bits = (payload_bytes + 7) * 12 + 48
    estimated_airtime_us = estimated_frame_bits * 1_000_000 / bitrate
    required_period_us = estimated_airtime_us * 1.25

    assert payload_bytes == 46, f"Unexpected V4 payload size: {payload_bytes}"
    assert payload_bytes <= 60, "RadioHead ASK payload limit exceeded"
    assert tx_period_us >= required_period_us, (
        f"TX period {tx_period_us} us lacks 25% margin over "
        f"{estimated_airtime_us:.0f} us estimated airtime"
    )
    assert filter_period_us == 10_000, "Bench filter is no longer 100 Hz"
    assert "waitPacketSent" not in re.sub(r"//.*", "", tx), "Blocking RF wait restored"
    assert "boot_id" in tx and "boot_id" in rx, "Session identifier missing"
    assert "packetsDuplicate" in rx and "packetsOutOfOrder" in rx

    matrix = {
        name: int(value)
        for name, value in re.findall(r"\b(M[0-2][0-2])\s*=\s*(-?\d+)", tx)
    }
    assert len(matrix) == 9, "Incomplete SENSOR_TO_BODY matrix"
    determinant = (
        matrix["M00"] * (matrix["M11"] * matrix["M22"] - matrix["M12"] * matrix["M21"])
        - matrix["M01"] * (matrix["M10"] * matrix["M22"] - matrix["M12"] * matrix["M20"])
        + matrix["M02"] * (matrix["M10"] * matrix["M21"] - matrix["M11"] * matrix["M20"])
    )
    assert determinant == 1, f"Sensor-to-body transform determinant is {determinant}"

    print(
        "PASS:",
        f"payload={payload_bytes} B",
        f"airtime_est={estimated_airtime_us / 1000:.1f} ms",
        f"period={tx_period_us / 1000:.1f} ms",
        f"rf_rate={1_000_000 / tx_period_us:.2f} Hz",
        f"filter_rate={1_000_000 / filter_period_us:.1f} Hz",
        f"det={determinant}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
