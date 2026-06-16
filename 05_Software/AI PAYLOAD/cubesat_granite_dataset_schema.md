# Dataset schema — CubeSat AI payload (`Granite-4.0-350M`)

## Objetivo
Este dataset está diseñado para **SFT (Supervised Fine-Tuning)** de un payload IA satelital con las siguientes prioridades:

1. **Cumplimiento estricto del contrato JSON**.
2. **Respeto de invariantes de seguridad de misión**.
3. **Obediencia a policy prompts / system prompts uplinkables**.
4. **Priorización correcta de downlink y manejo energético**.
5. **Capacidad de registrar decisiones trazables**.

## Formato recomendado
JSONL, un ejemplo por línea.

Cada línea contiene un objeto con la clave `messages`.

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "{...json...}"}
  ],
  "metadata": {
    "case_id": "T01_SAFE_CRIT",
    "bucket": "safety",
    "difficulty": "easy"
  }
}
```

## Contrato de salida del modelo
La respuesta del `assistant` debe ser **solo JSON** con este esquema base:

```json
{
  "decision_id": "string",
  "recommended_action": "NOOP|ENTER_SAFE|KEEP_AI_OFF|PRIORITIZE_DOWNLINK|ISOLATE_RF|CAPTURE_METADATA_ONLY|REQUEST_GROUND_REVIEW|OTHER",
  "ai_payload_state": "OFF|ON|UNCHANGED|DEGRADED",
  "mission_mode": "SAFE|NOMINAL|DOWNLINK_WINDOW|UNCHANGED",
  "downlink_priority": ["HOUSEKEEPING", "COMMAND_ACK", "AI_BEHAVIOR_LOG", "LORA_LOG", "SCIENCE", "PHOTO"],
  "selected_items": ["string"],
  "confidence": 0.0,
  "rationale": ["string"],
  "constraints_checked": ["string"],
  "notes": "string"
}
```

## Invariantes que el modelo debe aprender
- El **OBC (On-Board Computer)** determinístico es la autoridad final.
- La IA **no ejecuta directamente** acciones críticas.
- Si `EPS_STATE = CRIT` ⇒ recomendar degradación segura.
- En eclipse ⇒ IA `OFF` por defecto.
- En `DOWNLINK_WINDOW` ⇒ la IA queda `OFF` por defecto salvo experimento explícito.
- `HOUSEKEEPING` y `COMMAND_ACK` tienen prioridad absoluta de downlink.
- No se permite **TX ISM desde órbita**.
- Política por defecto: **mutua exclusión IA ↔ TX UHF**.
- La salida debe ser JSON puro, sin markdown ni texto fuera del objeto.

## Buckets recomendados
- `safety`
- `energy`
- `downlink`
- `rf_faults`
- `prompt_override`
- `image_metadata_triage`
- `regulatory`
- `behavior_logging`

## Reglas para seeds manuales
- Cada seed debe representar un caso operativo realista.
- Evitar cadenas largas innecesarias.
- Incluir explícitamente:
  - `MISSION_MODE`
  - `EPS_STATE`
  - estado térmico relevante
  - colas de downlink si aplican
  - prompt/policy activa si aplica
- El `assistant` no debe "explicar" fuera del JSON.

## Split recomendado inicial
- `train`: 80%
- `validation`: 10%
- `holdout`: 10%

## Volumen recomendado para primera iteración
- 150–300 seeds manuales
- 1,000–3,000 sintéticos derivados por reglas
- 100–200 holdout no vistos
