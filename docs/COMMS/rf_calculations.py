#!/usr/bin/env python3
"""Cálculos de referencia reproducibles para la documentación COMMS.

Este módulo no representa hardware validado. Centraliza únicamente las
ecuaciones de geometría, FSPL, LoRa Time-on-Air y capacidad bruta que se citan
en los documentos preliminares de AUSTRALIS-1.
"""

from __future__ import annotations

import argparse
import math


EARTH_RADIUS_KM = 6371.0
SPEED_OF_LIGHT_M_S = 299_792_458.0


def slant_range_km(
    altitude_km: float,
    elevation_deg: float,
    earth_radius_km: float = EARTH_RADIUS_KM,
) -> float:
    """Distancia oblicua para observador a nivel del radio terrestre."""
    if altitude_km <= 0:
        raise ValueError("altitude_km must be positive")
    if not 0 <= elevation_deg <= 90:
        raise ValueError("elevation_deg must be in [0, 90]")
    elevation_rad = math.radians(elevation_deg)
    return (
        math.sqrt(
            (earth_radius_km + altitude_km) ** 2
            - (earth_radius_km * math.cos(elevation_rad)) ** 2
        )
        - earth_radius_km * math.sin(elevation_rad)
    )


def fspl_db(frequency_mhz: float, distance_km: float) -> float:
    """Free-Space Path Loss con frecuencia en MHz y distancia en km."""
    if frequency_mhz <= 0 or distance_km <= 0:
        raise ValueError("frequency and distance must be positive")
    return (
        32.44
        + 20.0 * math.log10(frequency_mhz)
        + 20.0 * math.log10(distance_km)
    )


def max_doppler_hz(frequency_mhz: float, radial_velocity_km_s: float) -> float:
    """Cota no relativista |Δf|=f|v_r|/c."""
    if frequency_mhz <= 0 or radial_velocity_km_s < 0:
        raise ValueError("invalid Doppler inputs")
    return frequency_mhz * 1e6 * radial_velocity_km_s * 1e3 / SPEED_OF_LIGHT_M_S


def lora_time_on_air_s(
    *,
    spreading_factor: int,
    bandwidth_hz: int,
    coding_rate_index: int,
    payload_bytes: int,
    preamble_symbols: int,
    explicit_header: bool = True,
    crc_enabled: bool = True,
    low_data_rate_optimization: bool = True,
) -> float:
    """LoRa ToA según la ecuación de Semtech.

    ``coding_rate_index=1`` representa CR 4/5; 4 representa CR 4/8.
    """
    if spreading_factor not in range(6, 13):
        raise ValueError("spreading_factor must be in [6, 12]")
    if bandwidth_hz <= 0 or payload_bytes < 0 or preamble_symbols < 0:
        raise ValueError("invalid LoRa parameters")
    if coding_rate_index not in range(1, 5):
        raise ValueError("coding_rate_index must be in [1, 4]")

    ih = 0 if explicit_header else 1
    crc = 1 if crc_enabled else 0
    de = 1 if low_data_rate_optimization else 0
    symbol_time_s = (2**spreading_factor) / bandwidth_hz
    numerator = (
        8 * payload_bytes
        - 4 * spreading_factor
        + 28
        + 16 * crc
        - 20 * ih
    )
    denominator = 4 * (spreading_factor - 2 * de)
    payload_symbols = 8 + max(
        math.ceil(numerator / denominator) * (coding_rate_index + 4),
        0,
    )
    return (
        preamble_symbols + 4.25 + payload_symbols
    ) * symbol_time_s


def gross_capacity_bytes(
    bitrate_bps: float,
    contact_s: float,
    tx_duty: float = 1.0,
) -> float:
    """Capacidad bruta; todavía no descuenta framing, FEC, ARQ ni gaps."""
    if bitrate_bps < 0 or contact_s < 0 or not 0 <= tx_duty <= 1:
        raise ValueError("invalid capacity inputs")
    return bitrate_bps * contact_s * tx_duty / 8.0


def wilson_interval(successes: int, trials: int, z: float = 1.95996398454) -> tuple[float, float]:
    """Intervalo Wilson bilateral; por defecto, 95 %."""
    if trials <= 0 or successes < 0 or successes > trials:
        raise ValueError("invalid binomial sample")
    p_hat = successes / trials
    denominator = 1 + z**2 / trials
    center = (p_hat + z**2 / (2 * trials)) / denominator
    margin = (
        z
        * math.sqrt(
            p_hat * (1 - p_hat) / trials + z**2 / (4 * trials**2)
        )
        / denominator
    )
    return center - margin, center + margin


def run_self_test() -> None:
    """Regresiones numéricas usadas por la documentación."""
    assert math.isclose(slant_range_km(550, 10), 1815.1, abs_tol=0.1)
    assert math.isclose(fspl_db(436.5, slant_range_km(600, 20)), 148.11, abs_tol=0.01)
    assert math.isclose(fspl_db(915.0, slant_range_km(600, 20)), 154.54, abs_tol=0.01)
    assert math.isclose(max_doppler_hz(438.0, 7.7), 11249.8, abs_tol=0.1)
    assert math.isclose(
        lora_time_on_air_s(
            spreading_factor=12,
            bandwidth_hz=125_000,
            coding_rate_index=1,
            payload_bytes=12,
            preamble_symbols=16,
        ),
        1.417216,
        abs_tol=1e-9,
    )
    assert math.isclose(
        lora_time_on_air_s(
            spreading_factor=12,
            bandwidth_hz=250_000,
            coding_rate_index=1,
            payload_bytes=12,
            preamble_symbols=16,
        ),
        0.708608,
        abs_tol=1e-9,
    )
    assert gross_capacity_bytes(1200, 8 * 60, 0.30) == 21_600


def print_reference() -> None:
    print("UHF reference: 436.5 MHz")
    for altitude_km in (550, 600, 650):
        for elevation_deg in (10, 20, 30, 90):
            distance_km = slant_range_km(altitude_km, elevation_deg)
            print(
                f"h={altitude_km} km el={elevation_deg:>2} deg "
                f"d={distance_km:7.1f} km "
                f"FSPL={fspl_db(436.5, distance_km):6.2f} dB"
            )
    for bandwidth_hz, guard_s in ((125_000, 0.5), (250_000, 0.3)):
        toa_s = lora_time_on_air_s(
            spreading_factor=12,
            bandwidth_hz=bandwidth_hz,
            coding_rate_index=1,
            payload_bytes=12,
            preamble_symbols=16,
        )
        slots = math.floor(240 / (toa_s + guard_s))
        print(
            f"LoRa BW={bandwidth_hz // 1000} kHz "
            f"ToA={toa_s:.6f} s slots/240s={slots}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="ejecuta regresiones numéricas antes de imprimir la referencia",
    )
    args = parser.parse_args()
    if args.self_test:
        run_self_test()
        print("self-test: PASS")
    print_reference()


if __name__ == "__main__":
    main()
