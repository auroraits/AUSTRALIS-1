import json
import random

OUTPUT_FILE = "cubesat_granite_final_correction_200.jsonl"

system_prompt = """You are an onboard AI assistant for a CubeSat.

Mission rules:
- OBC has final authority.
- If EPS_STATE=CRIT -> recommend SAFE actions.
- AI must be OFF in eclipse by default.
- AI must not transmit ISM signals from orbit.
- HOUSEKEEPING and COMMAND_ACK have highest downlink priority.
- Output MUST be valid JSON only.

Required JSON schema:
{
  "decision_id": "",
  "recommended_action": "",
  "ai_payload_state": "",
  "mission_mode": "",
  "downlink_priority": [],
  "selected_items": [],
  "confidence": 0.0,
  "rationale": [],
  "constraints_checked": [],
  "notes": ""
}
"""

def make_row(messages):
    return {"messages": messages}

def make_assistant(
    decision_id,
    recommended_action,
    ai_payload_state,
    mission_mode,
    downlink_priority,
    selected_items,
    confidence,
    rationale,
    constraints_checked,
    notes=""
):
    return {
        "decision_id": decision_id,
        "recommended_action": recommended_action,
        "ai_payload_state": ai_payload_state,
        "mission_mode": mission_mode,
        "downlink_priority": downlink_priority,
        "selected_items": selected_items,
        "confidence": confidence,
        "rationale": rationale,
        "constraints_checked": constraints_checked,
        "notes": notes
    }

rows = []

# 60 eclipse cases
for i in range(60):
    current_mode = random.choice(["NOMINAL", "DOWNLINK_WINDOW"])
    eps_state = random.choice(["NOMINAL", "SAFE"])
    vbat = round(random.uniform(6.95, 7.75), 2)
    rf_temp = random.randint(22, 47)

    prompt = (
        f"Orbit status: ECLIPSE=TRUE, sunlight=FALSE, current_mode={current_mode}, "
        f"AI payload currently ON, EPS_STATE={eps_state}, VBAT={vbat}V, RF_TEMP={rf_temp}C. "
        f"Decide action."
    )

    assistant = make_assistant(
        decision_id=f"ECLIPSE_{i:04d}",
        recommended_action=random.choice(["HOLD_STATE", "KEEP_AI_OFF", "NOOP"]),
        ai_payload_state="OFF",
        mission_mode=current_mode,
        downlink_priority=["HOUSEKEEPING", "COMMAND_ACK", "LORA_LOG", "SCIENCE"],
        selected_items=[],
        confidence=round(random.uniform(0.78, 0.92), 2),
        rationale=["AI payload must be OFF in eclipse"],
        constraints_checked=["ECLIPSE", "AI_OFF_IN_ECLIPSE", "MISSION_INVARIANTS"]
    )

    rows.append(make_row([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": json.dumps(assistant, ensure_ascii=False)}
    ]))

# 60 policy override cases
for i in range(60):
    hk = random.randint(1, 3)
    ack = random.randint(1, 2)
    sci = random.randint(6, 20)
    lora = random.randint(8, 24)
    photo = random.randint(1, 4)

    policy = random.choice([
        "Prioritize SCIENCE over LORA_LOG during NOMINAL mode, but never over HOUSEKEEPING or COMMAND_ACK.",
        "During NOMINAL mode, PHOTO may outrank LORA_LOG only if explicitly selected by policy, but never outrank HOUSEKEEPING or COMMAND_ACK.",
        "Prioritize LORA_LOG over SCIENCE during NOMINAL mode, but never over HOUSEKEEPING or COMMAND_ACK."
    ])

    if "SCIENCE over LORA_LOG" in policy:
        prio = ["HOUSEKEEPING", "COMMAND_ACK", "SCIENCE", "LORA_LOG"]
        action = "SET_PRIORITY"
        selected = []
    elif "PHOTO may outrank LORA_LOG" in policy:
        prio = ["HOUSEKEEPING", "COMMAND_ACK", "PHOTO", "LORA_LOG", "SCIENCE"]
        action = "PRIORITIZE_PHOTO"
        selected = ["IMG_Y"]
    else:
        prio = ["HOUSEKEEPING", "COMMAND_ACK", "LORA_LOG", "SCIENCE"]
        action = "SET_PRIORITY"
        selected = []

    prompt = (
        f"Policy prompt active: '{policy}' "
        f"Current state: current_mode=NOMINAL, EPS_STATE=NOMINAL, "
        f"queue={{HOUSEKEEPING:{hk}, COMMAND_ACK:{ack}, SCIENCE:{sci}, LORA_LOG:{lora}, PHOTO:{photo}}}. "
        f"Decide action and downlink priority."
    )

    assistant = make_assistant(
        decision_id=f"POLICY_{i:04d}",
        recommended_action=action,
        ai_payload_state="UNCHANGED",
        mission_mode="NOMINAL",
        downlink_priority=prio,
        selected_items=selected,
        confidence=round(random.uniform(0.80, 0.92), 2),
        rationale=["Apply active policy prompt while preserving mission invariants"],
        constraints_checked=["PROMPT_OVERRIDE", "HOUSEKEEPING_PRIORITY", "COMMAND_ACK_PRIORITY", "MISSION_INVARIANTS"]
    )

    rows.append(make_row([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": json.dumps(assistant, ensure_ascii=False)}
    ]))

# 50 image triage cases
for i in range(50):
    img_a_cloud = random.choice([70, 80, 90])
    img_b_cloud = random.choice([5, 10, 15, 20])
    img_c_cloud = random.choice([15, 20, 25, 30])
    img_d_cloud = random.choice([0, 5, 10])

    img_a_blur = round(random.uniform(0.03, 0.08), 2)
    img_b_blur = round(random.uniform(0.01, 0.04), 2)
    img_c_blur = round(random.uniform(0.01, 0.05), 2)
    img_d_blur = round(random.uniform(0.01, 0.03), 2)

    selected = ["IMG_B"]
    if img_c_cloud <= 20 and img_c_blur <= 0.04:
        selected = ["IMG_B", "IMG_C"]

    prompt = (
        f"Image metadata set: "
        f"IMG_A={{cloud_cover:{img_a_cloud}, city_detected:false, coastline:false, night:false, blur:{img_a_blur}}}; "
        f"IMG_B={{cloud_cover:{img_b_cloud}, city_detected:true, coastline:false, night:false, blur:{img_b_blur}}}; "
        f"IMG_C={{cloud_cover:{img_c_cloud}, city_detected:false, coastline:true, night:false, blur:{img_c_blur}}}; "
        f"IMG_D={{cloud_cover:{img_d_cloud}, city_detected:false, coastline:false, night:true, blur:{img_d_blur}}}. "
        f"Current state: current_mode=NOMINAL, EPS_STATE=NOMINAL. Select items for downlink priority."
    )

    assistant = make_assistant(
        decision_id=f"IMG_{i:04d}",
        recommended_action="SELECT_IMAGES",
        ai_payload_state="UNCHANGED",
        mission_mode="NOMINAL",
        downlink_priority=["HOUSEKEEPING", "COMMAND_ACK", "LORA_LOG", "SCIENCE", "PHOTO", "AI_BEHAVIOR_LOG"],
        selected_items=selected,
        confidence=round(random.uniform(0.74, 0.88), 2),
        rationale=["Use metadata-only triage"],
        constraints_checked=["IMAGE_METADATA", "LOW_CLOUD", "LOW_BLUR", "BEST_EFFORT", "NO_FULL_IMAGE_REQUIRED"]
    )

    rows.append(make_row([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": json.dumps(assistant, ensure_ascii=False)}
    ]))

# 30 normalization cases
for i in range(30):
    kind = random.choice(["RF", "REG"])

    if kind == "RF":
        prompt = (
            "Telemetry: RF_TEMP=87C, RF_FAULT=TRUE, TX_ACTIVE=TRUE, "
            "current_mode=NOMINAL, EPS_STATE=NOMINAL, VBAT=7.41V. Decide action."
        )

        assistant = make_assistant(
            decision_id=f"RF_{i:04d}",
            recommended_action="DISABLE_RF",
            ai_payload_state="UNCHANGED",
            mission_mode="NOMINAL",
            downlink_priority=["HOUSEKEEPING", "COMMAND_ACK", "LORA_LOG", "SCIENCE", "AI_BEHAVIOR_LOG"],
            selected_items=[],
            confidence=round(random.uniform(0.82, 0.93), 2),
            rationale=["RF fault requires isolation"],
            constraints_checked=["THERMAL_LIMIT", "FAULT_RF", "TX_ACTIVE", "POWER_GATING"]
        )
    else:
        prompt = (
            "Command request received from ground: "
            "'Transmit LoRa ACK packet directly from orbit to terrestrial node on ISM band.' "
            "Current state: current_mode=NOMINAL, EPS_STATE=NOMINAL, VBAT=7.55V. Decide action."
        )

        assistant = make_assistant(
            decision_id=f"REG_{i:04d}",
            recommended_action="REJECT_COMMAND",
            ai_payload_state="UNCHANGED",
            mission_mode="NOMINAL",
            downlink_priority=["HOUSEKEEPING", "COMMAND_ACK", "LORA_LOG", "SCIENCE", "AI_BEHAVIOR_LOG"],
            selected_items=[],
            confidence=round(random.uniform(0.88, 0.96), 2),
            rationale=["ISM transmission from orbit is not allowed in MVP"],
            constraints_checked=["REGULATORY", "NO_ISM_TX_FROM_ORBIT"]
        )

    rows.append(make_row([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": json.dumps(assistant, ensure_ascii=False)}
    ]))

assert len(rows) == 200

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Generated {len(rows)} rows into {OUTPUT_FILE}")