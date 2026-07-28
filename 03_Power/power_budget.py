#!/usr/bin/env python3
"""Deterministic preliminary power-budget calculator for AUSTRALIS-1.

The calculator deliberately reports only the energy of documented legacy load
assumptions. It refuses to label the system budget closed while required loads
remain TBD.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any


INPUT_PATH = Path(__file__).with_name("power_budget_inputs.json")


def load_inputs(path: Path = INPUT_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != 1:
        raise ValueError("schema_version no soportada")
    return data


def orbit_period_min(altitude_km: float, data: dict[str, Any]) -> float:
    constants = data["constants"]
    radius_km = constants["earth_equatorial_radius_km"] + altitude_km
    period_s = 2.0 * math.pi * math.sqrt(
        radius_km**3 / constants["earth_mu_km3_s2"]
    )
    return period_s / 60.0


def beta_zero_eclipse_min(altitude_km: float, data: dict[str, Any]) -> float:
    """Cylindrical-shadow eclipse at beta=0; preliminary sensitivity only."""
    earth_radius = data["constants"]["earth_equatorial_radius_km"]
    orbit_radius = earth_radius + altitude_km
    half_angle_rad = math.asin(earth_radius / orbit_radius)
    return orbit_period_min(altitude_km, data) * half_angle_rad / math.pi


def mode_power_W(mode: str, data: dict[str, Any]) -> float:
    loads = data["loads_W"]
    duties = data["mode_duties"][mode]
    return sum(loads[name] * duty for name, duty in duties.items())


def validate(data: dict[str, Any]) -> None:
    errors: list[str] = []
    loads = data["loads_W"]
    for name, power in loads.items():
        if not isinstance(power, (int, float)) or power < 0:
            errors.append(f"carga inválida {name}={power!r}")

    for mode, duties in data["mode_duties"].items():
        for load, duty in duties.items():
            if load not in loads:
                errors.append(f"{mode}: carga desconocida {load}")
            if not 0 <= duty <= 1:
                errors.append(f"{mode}/{load}: duty fuera de [0,1]")

    for group in data["half_duplex_groups"]:
        duties = data["mode_duties"][group["mode"]]
        total = sum(duties.get(load, 0.0) for load in group["loads"])
        if total > group["max_total_duty"] + 1e-12:
            errors.append(
                f"{group['mode']}: duty half-duplex {total:.3f} "
                f"> {group['max_total_duty']:.3f}"
            )
    if errors:
        raise ValueError("\n".join(errors))


def calculate(data: dict[str, Any]) -> dict[str, Any]:
    validate(data)
    modes = {
        name: mode_power_W(name, data) for name in data["mode_duties"]
    }
    cases: list[dict[str, float]] = []
    dl_min = data["downlink_window_min"]
    for altitude_km in data["orbit_sensitivity_altitudes_km"]:
        period_min = orbit_period_min(altitude_km, data)
        eclipse_min = beta_zero_eclipse_min(altitude_km, data)
        sun_min = period_min - eclipse_min
        if dl_min >= period_min:
            raise ValueError("downlink_window_min debe ser menor que la órbita")
        typical_Wh = (
            modes["safe"] * (period_min - dl_min)
            + modes["downlink_half_duplex"] * dl_min
        ) / 60.0
        science_single_Wh = (
            modes["nominal_science_single"] * sun_min
            + modes["safe"] * eclipse_min
        ) / 60.0
        science_concentrator_Wh = (
            modes["nominal_science_concentrator"] * sun_min
            + modes["safe"] * eclipse_min
        ) / 60.0
        cases.append(
            {
                "altitude_km": altitude_km,
                "period_min": period_min,
                "beta0_eclipse_min": eclipse_min,
                "beta0_sun_min": sun_min,
                "known_typical_Wh": typical_Wh,
                "known_science_single_Wh": science_single_Wh,
                "known_science_concentrator_Wh": science_concentrator_Wh,
            }
        )
    return {
        "status": "INCOMPLETE",
        "mode_known_power_W": modes,
        "orbit_cases": cases,
        "required_unclosed_loads": data["required_unclosed_loads"],
    }


def self_test() -> None:
    data = load_inputs()
    result = calculate(data)
    assert result["status"] == "INCOMPLETE"
    assert abs(result["mode_known_power_W"]["safe"] - 0.1425) < 1e-12
    assert abs(
        result["mode_known_power_W"]["downlink_half_duplex"] - 1.11
    ) < 1e-12
    cases = result["orbit_cases"]
    assert 96.0 < cases[0]["period_min"] < 97.0
    assert 97.0 < cases[1]["period_min"] < 98.5
    assert all(35.0 < case["beta0_eclipse_min"] < 36.5 for case in cases)
    print("PASS — fórmulas, unidades y restricción half-duplex verificadas.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="salida JSON")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0

    result = calculate(load_inputs())
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("AUSTRALIS-1 preliminary known-load budget — INCOMPLETE")
        for name, power in result["mode_known_power_W"].items():
            print(f"{name}: {power:.4f} W known")
        for case in result["orbit_cases"]:
            print(
                f"{case['altitude_km']:.0f} km: "
                f"T={case['period_min']:.3f} min, "
                f"eclipse(beta=0)={case['beta0_eclipse_min']:.3f} min, "
                f"known typical={case['known_typical_Wh']:.4f} Wh/orbit, "
                "known nominal+SAFE="
                f"{case['known_science_single_Wh']:.4f}/"
                f"{case['known_science_concentrator_Wh']:.4f} Wh/orbit"
            )
        print(
            "NOT A CLOSED SYSTEM BUDGET: "
            f"{len(result['required_unclosed_loads'])} required load groups remain TBD."
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        sys.exit(1)
