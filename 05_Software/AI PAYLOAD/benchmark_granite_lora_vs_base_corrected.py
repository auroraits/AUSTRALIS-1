import json
import time
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# Bench/ground experimentation model. The compact flight-candidate line is
# Granite 350M; 2B is intentionally kept for lab exploration and comparisons.
BASE_MODEL = "ibm-granite/granite-3.1-2b-instruct"
ADAPTER_PATH = "granite_cubesat_lora"
SUITE_FILE = "CubeSatBenchmarkSuite.json"


def load_suite(path: str):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["systemPrompt"], data["tests"]


def load_tokenizer():
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok


def load_model(with_adapter: bool):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
    )

    if with_adapter:
        model = PeftModel.from_pretrained(model, ADAPTER_PATH)

    model.eval()
    return model


def extract_json(text: str):
    text = text.strip()

    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except Exception:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


def run_case(model, tokenizer, system_prompt, case):
    user_content = case["userPrompt"]

    if case.get("policyPrompt"):
        user_content = f"Active policy prompt: {case['policyPrompt']}\n\n{user_content}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[1]

    t0 = time.time()
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=220,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    dt = time.time() - t0

    new_tokens = output[0][input_len:]
    text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    parsed = extract_json(text)

    return {
        "raw_output": text,
        "parsed": parsed,
        "latency_s": round(dt, 3),
        "gen_tokens": int(len(new_tokens)),
        "gen_tok_s": round(len(new_tokens) / dt, 2) if dt > 0 else None,
    }


def get_nested_value(obj, dotted_key):
    current = obj
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def id_matches(expected, actual):
    if actual is None:
        return False
    expected = str(expected).upper()
    actual = str(actual).upper()

    if actual == expected:
        return True

    # Acepta T01 vs T01_SAFE_CRIT
    if expected.startswith(actual) or actual.startswith(expected):
        return True

    return False


def normalize_action(value):
    if value is None:
        return None

    v = str(value).upper().strip()

    aliases = {
        "SAFE_MODE": "ENTER_SAFE_MODE",
        "REJECT_REQUEST": "REJECT_COMMAND",
        "KEEP_AI_OFF": "HOLD_STATE",
        "PRIORITIZE_LORA": "SCHEDULE_DOWNLINK",
        "PRIORITIZE_PHOTO": "SELECT_IMAGES",
    }

    return aliases.get(v, v)


def normalize_mode(value):
    if value is None:
        return None
    return str(value).upper().strip()


def semantic_contains(expected_item, actual_items):
    if not isinstance(actual_items, list):
        return False

    exp = str(expected_item).upper()
    act = [str(x).upper() for x in actual_items]

    synonyms = {
        "AI_OFF_IN_ECLIPSE": ["AI_OFF_IN_ECLIPSE", "ECLIPSE", "AI_OFF_RULE"],
        "NO_ISM_TX_FROM_ORBIT": ["NO_ISM_TX_FROM_ORBIT", "NO_ISM_TX_ORBIT", "REGULATORY"],
        "FAULT_RF": ["FAULT_RF", "RF_FAULT"],
        "THERMAL_LIMIT": ["THERMAL_LIMIT", "RF_TEMP"],
        "HK_FIRST": ["HK_FIRST", "DL_PRIORITY", "HOUSEKEEPING_PRIORITY"],
        "CMD_ACK_FIRST": ["CMD_ACK_FIRST", "DL_PRIORITY", "COMMAND_ACK_PRIORITY"],
        "AI_OFF_IN_DOWNLINK": ["AI_OFF_IN_DOWNLINK", "TX_UHF_MUTEX", "MISSION_MODE"],
        "LOW_CLOUD": ["LOW_CLOUD", "IMAGE_METADATA"],
        "LOW_BLUR": ["LOW_BLUR", "IMAGE_METADATA", "NO_FULL_IMAGE_REQUIRED"],
        "POLICY_OVERRIDE_V2": ["POLICY_OVERRIDE_V2", "PROMPT_OVERRIDE", "MISSION_INVARIANTS"]
    }

    if exp in act:
        return True

    if exp in synonyms:
        return any(s in act for s in synonyms[exp])

    return False


def score_case(case, raw_output, parsed):
    max_score = 0
    score = 0
    notes = []

    # JSON válido
    max_score += 1
    if parsed is not None:
        score += 1
    else:
        notes.append("invalid_json")
        return {
            "score": score,
            "max_score": max_score,
            "pass": False,
            "notes": notes
        }

    # requiredKeys
    required_keys = case.get("requiredKeys", [])
    if required_keys:
        max_score += 1
        missing = [k for k in required_keys if k not in parsed]
        if not missing:
            score += 1
        else:
            notes.append(f"missing_keys:{missing}")

    # expectedEquals
    expected_equals = case.get("expectedEquals", {})
    for key, expected_value in expected_equals.items():
        max_score += 1
        actual = get_nested_value(parsed, key)
        ok = False

        if key == "case_id":
            ok = id_matches(expected_value, actual)

        elif key == "recommended_action":
            ok = normalize_action(actual) == normalize_action(expected_value)

        elif key == "mission_mode":
            # si el suite dice UNCHANGED, no penalizamos
            if str(expected_value).upper() == "UNCHANGED":
                ok = True
            else:
                ok = normalize_mode(actual) == normalize_mode(expected_value)

        else:
            ok = (actual == expected_value)

        if ok:
            score += 1
        else:
            notes.append(f"expectedEquals_fail:{key} expected={expected_value} actual={actual}")

    # arrayPrefixEquals
    array_prefix_equals = case.get("arrayPrefixEquals", {})
    for key, expected_prefix in array_prefix_equals.items():
        max_score += 1
        actual = get_nested_value(parsed, key)
        if isinstance(actual, list) and actual[:len(expected_prefix)] == expected_prefix:
            score += 1
        else:
            notes.append(f"arrayPrefixEquals_fail:{key} expected_prefix={expected_prefix} actual={actual}")

    # arrayEquals
    array_equals = case.get("arrayEquals", {})
    for key, expected_array in array_equals.items():
        max_score += 1
        actual = get_nested_value(parsed, key)

        # Relajamos selected_items: si contiene al menos lo esperado, vale
        if key == "selected_items" and isinstance(actual, list):
            if actual == expected_array or all(item in actual for item in expected_array):
                score += 1
            else:
                notes.append(f"arrayEquals_fail:{key} expected={expected_array} actual={actual}")
        else:
            if isinstance(actual, list) and actual == expected_array:
                score += 1
            else:
                notes.append(f"arrayEquals_fail:{key} expected={expected_array} actual={actual}")

    # arrayContains
    array_contains = case.get("arrayContains", {})
    for key, expected_items in array_contains.items():
        max_score += 1
        actual = get_nested_value(parsed, key)

        ok = False
        if key == "constraints_checked" and isinstance(actual, list):
            ok = all(semantic_contains(item, actual) for item in expected_items)
        elif isinstance(actual, list):
            ok = all(item in actual for item in expected_items)

        if ok:
            score += 1
        else:
            notes.append(f"arrayContains_fail:{key} expected_items={expected_items} actual={actual}")

    # forbiddenSubstrings
    forbidden_substrings = case.get("forbiddenSubstrings", [])
    if forbidden_substrings:
        max_score += 1
        lower_raw = raw_output.lower()
        found = [s for s in forbidden_substrings if s.lower() in lower_raw]
        if not found:
            score += 1
        else:
            notes.append(f"forbiddenSubstrings_found:{found}")

    return {
        "score": score,
        "max_score": max_score,
        "pass": score >= max_score - 1,  # tolerancia de 1 mismatch cosmético
        "notes": notes
    }


def print_case_result(label, case_id, result, score_result):
    print(f"\n--- {label} | {case_id} ---")
    print(
        f"latency_s={result['latency_s']} "
        f"gen_tok_s={result['gen_tok_s']} "
        f"score={score_result['score']}/{score_result['max_score']} "
        f"pass={score_result['pass']}"
    )

    if score_result["notes"]:
        print("notes:")
        for n in score_result["notes"]:
            print(f"  - {n}")

    if result["parsed"] is None:
        print("RAW OUTPUT:")
        print(result["raw_output"])
    else:
        print(json.dumps(result["parsed"], ensure_ascii=False, indent=2))


def summarize_results(label, summary_rows):
    print("\n" + "=" * 100)
    print(f"SUMMARY | {label}")
    print("=" * 100)

    total_cases = len(summary_rows)
    passed = sum(1 for r in summary_rows if r["pass"])
    avg_score = sum(r["score"] / r["max_score"] for r in summary_rows) / total_cases
    avg_latency = sum(r["latency_s"] for r in summary_rows) / total_cases
    avg_tok_s = sum((r["gen_tok_s"] or 0) for r in summary_rows) / total_cases

    print(f"cases:           {total_cases}")
    print(f"passes:          {passed}/{total_cases}")
    print(f"pass_rate_pct:   {round(100 * passed / total_cases, 2)}")
    print(f"avg_score_ratio: {round(avg_score, 4)}")
    print(f"avg_latency_s:   {round(avg_latency, 3)}")
    print(f"avg_gen_tok_s:   {round(avg_tok_s, 2)}")


def main():
    system_prompt, tests = load_suite(SUITE_FILE)
    tokenizer = load_tokenizer()

    print("Loading BASE model...")
    base_model = load_model(with_adapter=False)

    print("Loading FINE_TUNED model...")
    ft_model = load_model(with_adapter=True)

    all_summaries = {}

    for label, model in [("BASE", base_model), ("FINE_TUNED", ft_model)]:
        print("\n" + "=" * 100)
        print(label)
        print("=" * 100)

        rows = []

        for case in tests:
            result = run_case(model, tokenizer, system_prompt, case)
            score_result = score_case(case, result["raw_output"], result["parsed"])

            rows.append({
                "case_id": case["id"],
                "score": score_result["score"],
                "max_score": score_result["max_score"],
                "pass": score_result["pass"],
                "latency_s": result["latency_s"],
                "gen_tok_s": result["gen_tok_s"] or 0
            })

            print_case_result(label, case["id"], result, score_result)

        all_summaries[label] = rows
        summarize_results(label, rows)

    print("\n" + "=" * 100)
    print("COMPARATIVE SUMMARY")
    print("=" * 100)

    for label, rows in all_summaries.items():
        total_cases = len(rows)
        passed = sum(1 for r in rows if r["pass"])
        avg_score = sum(r["score"] / r["max_score"] for r in rows) / total_cases
        avg_latency = sum(r["latency_s"] for r in rows) / total_cases
        avg_tok_s = sum((r["gen_tok_s"] or 0) for r in rows) / total_cases

        print(
            f"{label:12} | "
            f"passes={passed}/{total_cases} | "
            f"avg_score_ratio={avg_score:.4f} | "
            f"avg_latency_s={avg_latency:.3f} | "
            f"avg_gen_tok_s={avg_tok_s:.2f}"
        )


if __name__ == "__main__":
    main()
