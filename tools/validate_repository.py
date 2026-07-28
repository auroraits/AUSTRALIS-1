#!/usr/bin/env python3
"""Deterministic structural checks for AUSTRALIS controlled artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {
    ".git",
    ".pio",
    ".platformio",
    "__pycache__",
    "bin",
    "obj",
    "node_modules",
    "venv",
}
REQ_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)*-\d+$")
CX_RE = re.compile(r"^CX-[A-Z0-9-]+$")
PROC_RE = re.compile(r"PROC-[A-Z]+-\d+")
RISK_RE = re.compile(r"RSK-[A-Z0-9-]+")
ADR_RE = re.compile(r"ADR-\d{8}-[a-z0-9-]+")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*]\(([^)]+)\)")
AUDIT_ROOT_PATH_RE = re.compile(
    r"^(?:\.github/|\d{2}_[^/]+/|docs/|tools/)"
)
VCRM_STATES = {
    "Planned",
    "Implemented",
    "Verified",
    "Waived",
    "Open",
    "Blocked by Integrator",
}
COMPLIANCE_STATES = {
    "Open",
    "Partial",
    "Closed",
    "Planned",
    "Implemented",
    "Verified",
    "Waived",
    "Blocked by Integrator",
}


def controlled_files(suffix: str):
    for path in ROOT.rglob(f"*{suffix}"):
        if not any(part in EXCLUDED_PARTS for part in path.parts):
            yield path


def split_markdown_row(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith(r"\|"):
        row = row[:-1]
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", row)]


def markdown_rows(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*:?-+", line):
            continue
        rows.append(split_markdown_row(line))
    return rows


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def validate_markdown_documents(errors: list[str]) -> tuple[int, int]:
    markdown_count = 0
    table_count = 0

    for path in controlled_files(".md"):
        markdown_count += 1
        expected_columns: int | None = None
        header_columns: int | None = None

        for line_number, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(),
            start=1,
        ):
            if line.lstrip().startswith("|"):
                cells = split_markdown_row(line)
                is_separator = bool(cells) and all(
                    re.fullmatch(r"\s*:?-{3,}:?\s*", cell)
                    for cell in cells
                )
                if is_separator:
                    if header_columns is None:
                        errors.append(
                            f"{path.relative_to(ROOT)}:{line_number}: "
                            "table separator has no header"
                        )
                    elif len(cells) != header_columns:
                        errors.append(
                            f"{path.relative_to(ROOT)}:{line_number}: "
                            f"table separator has {len(cells)} columns; "
                            f"header has {header_columns}"
                        )
                    expected_columns = len(cells)
                    table_count += 1
                elif expected_columns is not None:
                    if len(cells) != expected_columns:
                        errors.append(
                            f"{path.relative_to(ROOT)}:{line_number}: "
                            f"table row has {len(cells)} columns; "
                            f"expected {expected_columns}"
                        )
                else:
                    header_columns = len(cells)
            else:
                expected_columns = None
                header_columns = None

            for raw_target in MARKDOWN_LINK_RE.findall(line):
                raw_target = raw_target.strip()
                if raw_target.startswith("<") and ">" in raw_target:
                    target = raw_target[1 : raw_target.index(">")]
                else:
                    target = raw_target.split(maxsplit=1)[0]
                if (
                    not target
                    or target.startswith("#")
                    or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I)
                ):
                    continue
                target = unquote(target).split("#", 1)[0].split("?", 1)[0]
                if not target:
                    continue
                if target.startswith("/"):
                    destination = ROOT / target.lstrip("/")
                else:
                    destination = path.parent / target
                if not destination.exists():
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: "
                        f"broken local link {raw_target!r}"
                    )

    audit_ledger = ROOT / "docs/AUDIT_REMEDIATION_INDEX_2026-07-27.md"
    if audit_ledger.exists():
        for line_number, line in enumerate(
            audit_ledger.read_text(encoding="utf-8-sig").splitlines(),
            start=1,
        ):
            for token in re.findall(r"`([^`]+)`", line):
                if not AUDIT_ROOT_PATH_RE.match(token):
                    continue
                candidate = token.split(" --", 1)[0]
                candidate = re.sub(r":\d+(?:-\d+)?$", "", candidate)
                if not (ROOT / candidate).exists():
                    errors.append(
                        f"{audit_ledger.relative_to(ROOT)}:{line_number}: "
                        f"nonexistent controlled path {candidate!r}"
                    )

    return markdown_count, table_count


def main() -> int:
    errors: list[str] = []
    json_count = 0
    jsonl_count = 0
    python_count = 0
    markdown_count, table_count = validate_markdown_documents(errors)

    for path in controlled_files(".json"):
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
            json_count += 1
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")

    for path in controlled_files(".jsonl"):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(),
            start=1,
        ):
            if not line.strip():
                continue
            try:
                json.loads(line)
                jsonl_count += 1
            except Exception as exc:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: invalid JSONL: {exc}"
                )

    for path in controlled_files(".py"):
        try:
            source = path.read_text(encoding="utf-8-sig")
            compile(source, str(path), "exec")
            python_count += 1
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid Python: {exc}")

    requirement_rows = [
        row
        for row in markdown_rows(ROOT / "01_Mission/requirements_matrix.md")
        if row and REQ_RE.fullmatch(row[0])
    ]
    requirements = {row[0]: row[-1] for row in requirement_rows}
    if len(requirements) != len(requirement_rows):
        errors.append("requirements_matrix.md contains duplicate ReqID values")

    vcrm = csv_rows(ROOT / "01_Mission/verification_cross_reference_matrix.csv")
    vcrm_ids = [row["ReqID"] for row in vcrm]
    if set(vcrm_ids) != set(requirements):
        errors.append(
            "ReqID/VCRM mismatch: "
            f"missing={sorted(set(requirements) - set(vcrm_ids))}; "
            f"extra={sorted(set(vcrm_ids) - set(requirements))}"
        )
    if len(vcrm_ids) != len(set(vcrm_ids)):
        errors.append("VCRM contains duplicate ReqID values")
    for row in vcrm:
        if row["RequirementLifecycle"] != requirements.get(row["ReqID"]):
            errors.append(
                f"{row['ReqID']}: lifecycle differs between requirement and VCRM"
            )
        if row["VerificationStatus"] not in VCRM_STATES:
            errors.append(
                f"{row['ReqID']}: invalid VCRM state {row['VerificationStatus']!r}"
            )

    compliance_rows = [
        row
        for row in markdown_rows(ROOT / "01_Mission/compliance_matrix.md")
        if row and CX_RE.fullmatch(row[0])
    ]
    compliance = {row[0]: row[-2] for row in compliance_rows}
    if len(compliance) != len(compliance_rows):
        errors.append("compliance_matrix.md contains duplicate ComplianceID values")
    for identifier, state in compliance.items():
        if state not in COMPLIANCE_STATES:
            errors.append(f"{identifier}: invalid compliance state {state!r}")

    cxref = csv_rows(ROOT / "01_Mission/compliance_cross_reference_matrix.csv")
    cxref_ids = [row["ComplianceID"] for row in cxref]
    if set(cxref_ids) != set(compliance):
        errors.append(
            "Compliance/CXREF mismatch: "
            f"missing={sorted(set(compliance) - set(cxref_ids))}; "
            f"extra={sorted(set(cxref_ids) - set(compliance))}"
        )
    if len(cxref_ids) != len(set(cxref_ids)):
        errors.append("compliance cross-reference contains duplicate IDs")
    for row in cxref:
        if row["Status"] not in COMPLIANCE_STATES:
            errors.append(
                f"{row['ComplianceID']}: invalid CXREF state {row['Status']!r}"
            )

    procedure_text = (
        ROOT / "01_Mission/verification_procedure_index.md"
    ).read_text(encoding="utf-8-sig")
    procedures = set(PROC_RE.findall(procedure_text))
    referenced_procedures: set[str] = set()
    referenced_risks: set[str] = set()
    for row in [*vcrm, *cxref]:
        referenced_procedures.update(
            PROC_RE.findall(
                row.get("ProcedureID", "") + " " + row.get("ProcedureIDs", "")
            )
        )
        referenced_risks.update(RISK_RE.findall(row.get("RiskID", "")))
        referenced_risks.update(RISK_RE.findall(row.get("RiskIDs", "")))
    missing_procedures = referenced_procedures - procedures
    if missing_procedures:
        errors.append(
            f"procedure index missing references: {sorted(missing_procedures)}"
        )

    top_risks = set(
        RISK_RE.findall(
            (ROOT / "07_Risk/top_risks.md").read_text(encoding="utf-8-sig")
        )
    )
    missing_risks = referenced_risks - top_risks
    if missing_risks:
        errors.append(f"top risk register missing references: {sorted(missing_risks)}")

    adr_files = {
        path.stem: path
        for path in (ROOT / "08_Decisions").glob("ADR-*.md")
    }
    index_text = (ROOT / "08_Decisions/INDEX.md").read_text(encoding="utf-8-sig")
    indexed_adrs: dict[str, str] = {}
    for row in markdown_rows(ROOT / "08_Decisions/INDEX.md"):
        if not row:
            continue
        match = ADR_RE.search(row[0])
        if match:
            indexed_adrs[match.group()] = row[1]
    if set(adr_files) != set(indexed_adrs):
        errors.append(
            "ADR index mismatch: "
            f"missing={sorted(set(adr_files) - set(indexed_adrs))}; "
            f"extra={sorted(set(indexed_adrs) - set(adr_files))}"
        )
    for identifier, path in adr_files.items():
        header = "\n".join(
            path.read_text(encoding="utf-8-sig").splitlines()[:15]
        )
        state_match = re.search(
            r"\*\*Estado:\*\*\s*(Accepted|Superseded)\b",
            header,
        )
        if not state_match:
            errors.append(f"{identifier}: missing canonical Accepted/Superseded state")
        elif indexed_adrs.get(identifier) != state_match.group(1):
            errors.append(
                f"{identifier}: index state {indexed_adrs.get(identifier)!r} "
                f"!= header {state_match.group(1)!r}"
            )
    for target in ADR_RE.findall(index_text):
        if target not in adr_files:
            errors.append(f"ADR index references nonexistent target {target}")

    if errors:
        print("FAIL - repository structural validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS - repository structure:",
        f"{len(requirements)} requirements/VCRM rows,",
        f"{len(compliance)} compliance/CXREF rows,",
        f"{len(procedures)} procedures,",
        f"{len(top_risks)} parent risks,",
        f"{len(adr_files)} ADRs,",
        f"{markdown_count} Markdown files/{table_count} tables,",
        f"{json_count} JSON files,",
        f"{jsonl_count} JSONL records,",
        f"{python_count} Python files.",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
