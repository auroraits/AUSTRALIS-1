import json
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# Bench/ground experimentation model. The compact flight-candidate line is
# Granite 350M; 2B is intentionally kept for lab exploration and comparisons.
BASE_MODEL = "ibm-granite/granite-3.1-2b-instruct"
ADAPTER_PATH = "granite_cubesat_lora"
CASES_FILE = "cubesat_holdout_cases.json"

SYSTEM_PROMPT = """You are an onboard AI assistant for a CubeSat.

Mission rules:
- OBC (On-Board Computer) has final authority.
- If EPS_STATE=CRIT -> recommend SAFE actions.
- AI must be OFF in eclipse by default.
- AI must not transmit ISM signals from orbit.
- HOUSEKEEPING and COMMAND_ACK have highest downlink priority.
- Output MUST be valid JSON only.
- Do not echo the prompt.
- Do not include markdown fences.

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

def load_model():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
    )
    model = PeftModel.from_pretrained(model, ADAPTER_PATH)
    model.eval()
    return model, tokenizer

def extract_json(text: str):
    text = text.strip()

    # caso ideal: arranca en {
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except Exception:
            pass

    # buscar primer { y último }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None

def run_case(model, tokenizer, case):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": case["prompt"]},
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[1]

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=220,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output[0][input_len:]
    text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    parsed = extract_json(text)

    return {
        "case_id": case["case_id"],
        "raw_output": text,
        "parsed": parsed,
    }

def main():
    cases = json.loads(Path(CASES_FILE).read_text(encoding="utf-8"))
    model, tokenizer = load_model()

    print("=" * 100)
    print("HOLDOUT EVALUATION")
    print("=" * 100)

    for case in cases:
        result = run_case(model, tokenizer, case)
        print(f"\n--- {result['case_id']} ---")
        if result["parsed"] is None:
            print("RAW:")
            print(result["raw_output"])
            print("\nPARSE: FAILED")
        else:
            print(json.dumps(result["parsed"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
