import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

# Bench/ground experimentation model. The compact flight-candidate line is
# Granite 350M; 2B is intentionally kept for lab exploration and comparisons.
model_id = "ibm-granite/granite-3.1-2b-instruct"
data_file = "cubesat_granite_v3_1800.jsonl"
output_dir = "granite_cubesat_lora"

# Dataset conversacional nativo: {"messages": [...]}
dataset = load_dataset("json", data_files=data_file)

tokenizer = AutoTokenizer.from_pretrained(model_id)

# Algunos tokenizers no traen pad_token configurado
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)

# LoRA conservador para 4060 8GB
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
)

training_args = SFTConfig(
    output_dir=output_dir,
    max_length=1024,
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    logging_steps=5,
    save_strategy="epoch",
    report_to="none",
    bf16=True,
    fp16=False,
    gradient_checkpointing=True,
    packing=False,
    max_grad_norm=0.0,
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    peft_config=peft_config,
)

trainer.train()
trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)
