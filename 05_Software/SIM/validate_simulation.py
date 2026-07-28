#!/usr/bin/env python3
"""Static regression checks for the AUSTRALIS preliminary simulator."""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
HTML = ROOT / "borealis_3d_viewer_v9_3_6rad_export.html"

MU = 398600.4418
RE = 6378.137
J2 = 1.08262668e-3
TROPICAL_YEAR_SEC = 365.2422 * 86400


def sso_inclination_deg(altitude_km: float) -> float:
    a_km = RE + altitude_km
    mean_motion = math.sqrt(MU / a_km**3)
    target_rate = 2 * math.pi / TROPICAL_YEAR_SEC
    denominator = 1.5 * J2 * (RE / a_km) ** 2 * mean_motion
    return math.degrees(math.acos(-target_rate / denominator))


def main() -> int:
    text = HTML.read_text(encoding="utf-8")
    errors: list[str] = []

    required = {
        "geometry": "0.01702,0.01702,0.01702,0.01702,0.010,0.010",
        "box length": "boxZ = 1.702",
        "SSO derivation": "function sunSynchronousInclinationDeg",
        "exact final integration step": "const sampleDtSec = Math.min(dtSec, durationSec - k*dtSec)",
        "frozen run inputs": "uiParams:{...frozenUiParams}",
        "outward ground normal": "groundOutwardNormal.dot(sunEci)",
        "Kirchhoff IR": "userEarthIR * epsIR[i]",
        "Earth emission": "qradEarthOut",
        "PV heat extraction": "- pface - qradSpace - qradEarthOut",
        "daily normalization": "panelElectricalWhPerDay",
        "manifest": "csvSha256",
        "incomplete status": "INCOMPLETE_NOT_FOR_DESIGN_DECISIONS",
    }
    for label, token in required.items():
        if token not in text:
            errors.append(f"falta {label}: {token}")

    forbidden = {
        "independent inclination sweep": "for(let inc=",
        "wrong albedo sign": "nadirVec.dot(sunEci)",
        "spectrally inconsistent IR array": "earthIRAbs",
        "horizon-dependent energy score": "energyScore =",
        "arbitrary thermal key": "thermalKey",
        "min-max ranking": "normalizeScore(",
        "global score": "totalScore",
        "automatic best radiator": "BestRad",
    }
    for label, token in forbidden.items():
        if token in text:
            errors.append(f"regresión {label}: {token}")

    inc600 = sso_inclination_deg(600)
    inc650 = sso_inclination_deg(650)
    if abs(inc600 - 97.7876695) > 1e-6:
        errors.append(f"SSO 600 km inesperada: {inc600}")
    if abs(inc650 - 97.9859966) > 1e-6:
        errors.append(f"SSO 650 km inesperada: {inc650}")

    old_csv_names = (
        "borealis_sweep_6rad_2026-03-21T025706.csv",
        "borealis_sweep_6rad_2026-03-21T032025.csv",
    )
    readme = (ROOT / "README_SIMULATION.md").read_text(encoding="utf-8")
    for name in old_csv_names:
        if name not in readme or "INVALIDATED" not in readme:
            errors.append(f"CSV histórico no invalidado documentalmente: {name}")

    modelica = (ROOT / "BorealisThermalConcept.mo").read_text(encoding="utf-8")
    run_mos = (ROOT / "run_BorealisThermalConcept.mos").read_text(encoding="utf-8")
    if "HISTORICAL SNAPSHOT" not in modelica:
        errors.append("Modelica no está marcado Historical Snapshot")
    if "simulate(" in run_mos or "loadFile(" in run_mos:
        errors.append("runner Modelica histórico volvió a habilitarse")

    if errors:
        print("FAIL — regresiones del simulador:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS — geometría, SSO, balance térmico estático, no-ranking, "
        "manifest e invalidación histórica verificados; "
        f"iSSO(600/650)={inc600:.6f}/{inc650:.6f}°."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
