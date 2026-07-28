#!/usr/bin/env python3
"""Fail closed if the EPS KiCad placeholder looks fabricable or regresses.

This is intentionally a placeholder validator, not ERC/DRC and not an
electrical design verifier. It prevents the current marker files from being
mistaken for released hardware.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent

SCHEMATIC_FILES = (
    "EPS_Bench2S_FlightLike.kicad_sch",
    "00_Top.kicad_sch",
    "01_PV_Input.kicad_sch",
    "02_MPPT_Charger.kicad_sch",
    "03_Battery_BMS_2S.kicad_sch",
    "04_Power_Rails_5V_3V3.kicad_sch",
    "05_Power_Gating.kicad_sch",
    "06_Telemetry_TestPoints.kicad_sch",
)

# UUIDs of the unsafe pass-throughs/shorts removed on 2026-07-27. Keeping the
# UUID list makes an accidental revert fail even if surrounding formatting
# changes.
FORBIDDEN_WIRE_UUIDS = {
    "c1664f79-e3e7-4417-89c1-c19f01d78a29",  # PV_BUS_P to PV_BUS_N
    "07622ab2-e584-4daf-926e-5e96a058f0bd",
    "11cd0818-a5c6-4e53-ac5e-cea33f7d6b4d",
    "bea95a67-9ce3-4920-aca7-e4a629bd19e5",
    "f247973e-8c66-4eb5-9f25-37d4ea601dfd",
    "0fd59da8-636f-48da-8a7b-8e6f4fe222a2",
    "396ea9fd-c3b3-46e1-b92a-8af55c2062eb",
    "c3a2649d-f1e3-4b35-8d6c-17732fb37bfd",
    "080c4471-fe08-4c96-9309-abb4e3db5f46",
    "0eedeea2-d010-4b32-b4b7-b9d7d640a9b0",
    "d88b7872-7a3a-4d9b-b78c-9a867c08bfef",
    "a94ee559-ec46-4d3a-a947-e162818a0236",
    "ae3a014a-363b-4d54-a839-34511a51b966",
    "c774ea2b-6c65-4968-9205-702963b5ec63",
    "e80c9bff-af07-49b4-b04a-56100a6ccff0",
}


def count_form(text: str, form: str) -> int:
    return len(re.findall(rf"(?m)^\s*\({re.escape(form)}(?:\s|$)", text))


def sexpr_is_balanced(text: str) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not in_string


def main() -> int:
    errors: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "NO FABRICAR" not in readme or "NON-FABRICABLE" not in readme:
        errors.append("README no conserva el bloqueo de fabricación")

    all_schematic_text = ""
    for name in SCHEMATIC_FILES:
        text = (ROOT / name).read_text(encoding="utf-8")
        all_schematic_text += text
        if "NO FABRICAR" not in text:
            errors.append(f"{name}: falta advertencia NO FABRICAR")
        if not sexpr_is_balanced(text):
            errors.append(f"{name}: S-expression desbalanceada")

    restored = sorted(uuid for uuid in FORBIDDEN_WIRE_UUIDS if uuid in all_schematic_text)
    if restored:
        errors.append("se restauraron conexiones inseguras: " + ", ".join(restored))

    pcb = (ROOT / "EPS_Bench2S_FlightLike.kicad_pcb").read_text(encoding="utf-8")
    if not sexpr_is_balanced(pcb):
        errors.append("PCB: S-expression desbalanceada")
    forbidden_counts = {
        "pad": count_form(pcb, "pad"),
        "segment": count_form(pcb, "segment"),
        "via": count_form(pcb, "via"),
        "zone": count_form(pcb, "zone"),
        "Edge.Cuts": len(re.findall(r'\(layer\s+"Edge\.Cuts"\)', pcb)),
    }
    for element, count in forbidden_counts.items():
        if count:
            errors.append(f"PCB placeholder contiene {count} elemento(s) {element}")

    project = (ROOT / "EPS_Bench2S_FlightLike.kicad_pro").read_text(
        encoding="utf-8"
    )
    min_width = re.search(r'"min_track_width":\s*([0-9.]+)', project)
    default_width = re.search(r'"track_width":\s*([0-9.]+)', project)
    if not min_width or not default_width or min_width.group(1) != default_width.group(1):
        errors.append("reglas de ancho mínimo/default continúan inconsistentes")

    if errors:
        print("FAIL — EPS placeholder inseguro o ambiguo:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS — marcador EPS no fabricable: sin conexiones prohibidas, "
        "sin cobre/pads/outline y con bloqueo documental."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
