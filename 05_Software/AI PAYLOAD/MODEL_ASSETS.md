# AI model assets

The public repository does not vendor model weights, tokenizer artifacts, LoRA
adapter output directories or generated checkpoints.

Use upstream sources and local regeneration instead:

- IBM Granite 4.0 350M base model: https://huggingface.co/ibm-granite/granite-4.0-350m-base
- IBM Granite 4.0 H 350M model card: https://huggingface.co/ibm-granite/granite-4.0-h-350m
- IBM Granite 3.1 2B Instruct model card: https://huggingface.co/ibm-granite/granite-3.1-2b-instruct
- IBM Granite documentation: https://www.ibm.com/granite/docs/models/granite

## Public tree policy

Keep in Git:

- training, benchmark and holdout scripts;
- dataset schema and project-authored JSON/JSONL datasets;
- benchmark evidence and ADRs.

Do not keep in Git:

- `granite_model/`;
- `granite_cubesat_lora/`;
- `*.safetensors`, `*.bin`, `*.pt`, `*.pth`, checkpoints or tokenizer dumps.

## Model role split

The public AI payload documentation uses an explicit model-role split:

- Granite 350M family: compact flight-candidate line for the CM5 payload. It is
  not flight-ready and cannot be declared final until power, thermal, boot,
  supervisor integration and environmental gates are closed.
- Granite 3.1 2B Instruct: bench and ground experimentation model for broader
  behavior exploration, dataset iteration, benchmark comparison and prompt
  policy testing. It is not the primary flight candidate under the current
  power/thermal budget.

Historical scripts that reference `ibm-granite/granite-3.1-2b-instruct` are
kept as experimentation tools and should not be used as evidence that 2B is the
flight baseline.

See:

- `08_Decisions/ADR-20260615-ai-model-roles-granite350m-flight-candidate-2b-experimentation.md`
