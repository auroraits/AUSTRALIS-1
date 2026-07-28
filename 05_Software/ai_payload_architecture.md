# AUSTRALIS-1 AI payload architecture

**Revision:** 2026-07-27
**Status:** Preliminary / pre-SRR
**Current candidate:** `gemma4:e2b` (bench candidate only)

No AI model is currently a validated baseline or flight-ready component. The
March Granite evidence is historical and invalidated; Granite 350M is deferred.

## 1. Purpose and authority

The payload investigates whether a compact language model can produce useful,
safe recommendations from bounded spacecraft state. It is not a flight
controller.

The authority chain is:

1. OBC acquires and validates spacecraft state.
2. OBC constructs a versioned, bounded context snapshot.
3. The AI runtime proposes an `AgentDecisionEnvelope`.
4. A deterministic OBC validator checks syntax, tool schemas and policy.
5. `RuntimeSafetySupervisor` accepts, modifies or rejects each proposal.
6. Only deterministic flight software may execute an allowed action.
7. Inputs, raw output, decision, supervisor result and observed effect are
   correlated in the scientific log.

The OBC can power-gate or reset the AI computer. Loss, corruption, timeout or
misbehavior of the AI must not prevent SAFE operation, TTC or housekeeping.

## 2. Hardware status

- Raspberry Pi CM5 family: bench/flight-like candidate, not qualified hardware.
- Exact CM5 memory/carrier/storage configuration: configuration controlled by
  the test manifest.
- Flight power rail, protection, watchdog, storage recovery and mechanical/
  thermal implementation: TBD.
- Radiation, latch-up, TID/SEE, EMC and environmental qualification: open.

Results from a desktop/GPU host cannot be extrapolated to CM5 power, latency,
memory or thermal performance.

## 3. Model roles

- `gemma4:e2b`: primary candidate for the next strict agentic benchmark and CM5
  characterization.
- Granite 3.1 2B scripts/data: invalidated historical experiment retained for
  provenance.
- Granite 350M: deferred; no current evidence.
- Any comparison model: control only unless an Accepted ADR changes its role.

Promotion requires an exact artifact digest, license/provenance review,
reproducible benchmark, CM5 measurements and an Accepted ADR. A tag such as
`gemma4:e2b` is not by itself an immutable model identifier.

## 4. Runtime partition

### OBC deterministic partition

- mission mode and EPS state machines;
- sensor plausibility and freshness checks;
- command authentication/anti-replay result;
- tool catalog and argument validation;
- safety invariants, timeouts and resource limits;
- final action authority, fault management and logging.

### AI partition

- bounded inference process;
- read-only context input;
- structured recommendation output;
- no direct GPIO, actuator, RF, EPS or filesystem authority;
- no access to command keys;
- resource limits and watchdog heartbeat.

### Interface

The logical contract is defined in `AI PAYLOAD/AI_AGENT_PROTOCOL.md`. Bench
transport may use framed UART/JSONL; a flight-like implementation may use a
bounded binary encoding. Transport selection must preserve:

- explicit version and length;
- sequence/correlation identifier;
- integrity check;
- timeout and idempotency;
- reject-on-parse-error behavior;
- authenticated command state supplied by OBC, never a model assertion.

## 5. Safety invariants

At minimum, the deterministic supervisor enforces:

- `EPS_STATE=CRIT`: SAFE/survival actions only; AI and nonessential loads OFF.
- `EPS_STATE=LOW`, mission SAFE or eclipse: AI OFF by default.
- OBC core, EPS core and watchdog cannot be switched by AI tools.
- LoRa/ISM transmission from orbit is not exposed as a tool.
- UHF operation requires valid profile, geometry, power, thermal and RF state.
- unauthenticated/replayed prompt or command cannot activate content;
- housekeeping and command acknowledgements cannot be displaced;
- model-reported `confidence` never authorizes an action;
- unknown, malformed, extra or out-of-range fields fail closed;
- missing a required safe action is an evaluation failure;
- any supervisor-rejected proposal is a benchmark hard failure.

The complete transition thresholds, hysteresis and sensor-invalid behavior
belong to the deterministic EPS/mode specifications, not the model prompt.

## 6. Scientific log

Every inference proposed as mission evidence must persist a versioned record
containing:

- event, orbit/pass and correlation identifiers;
- monotonic and UTC timestamps with time-quality flag;
- full bounded input snapshot plus canonical hash;
- raw prompt/context bytes and raw model output;
- parsed decision and schema-validation diagnostics;
- exact model/tokenizer/template/adapter digests;
- quantization, context length, decoding settings and seed;
- runtime, OS, OBC/AI software and supervisor revisions;
- tool catalog/policy revision;
- supervisor decision and reason codes per tool call;
- action actually applied, acknowledgement and resulting state;
- latency, token counts, peak memory and timeout state;
- voltage/current/energy for the inference window when instrumented;
- CM5, battery, EPS and RF temperatures relevant to the event;
- pre/post fault flags and any reset, undervoltage or throttling indication.

Hashes alone are insufficient if the underlying input/raw output is not
recoverable. Sensitive fields may be encrypted or access-controlled on ground,
but the scientific archive must retain an auditable canonical form.

`confidence` is an uncalibrated model output until a separate calibration study
defines its meaning and error bounds.

## 7. Benchmark and dataset

The active proposal is:

- strict runner: `AI PAYLOAD/AgenticBenchmarkRunner_v1.py`;
- suite: `AI PAYLOAD/AgenticBenchmarkSuite.v1.json`;
- protocol: `AI PAYLOAD/AI_AGENT_PROTOCOL.md`;
- data rules: `AI PAYLOAD/AGENTIC_DATASET_SCHEMA.md`.

The runner validates exact JSON and tool schemas, derives safety class from the
OBC catalog, applies deterministic policy/postconditions and contains
adversarial unit tests. This validates the evaluator implementation only; it
does not validate a model.

The legacy Granite dataset and holdout are quarantined. A new corpus requires
scenario-family splits, provenance, expert-reviewed oracles and leakage checks.

## 8. Experimental protocol required before flight design closure

The mission experiment must be preregistered with:

- falsifiable hypothesis about usefulness and safety;
- deterministic/non-AI control policy;
- representative state/fault matrix and sampling plan;
- blinded oracle and review procedure;
- primary metrics: safe-action failure rate, supervisor rejection rate,
  required-action omission rate and correct postcondition rate;
- secondary metrics: latency, energy, memory, thermal response and data volume;
- sample size, confidence interval method and stopping/abort rules;
- explicit acceptance limits approved before results are observed.

Five inferences or one hundred logs alone cannot demonstrate usefulness or
safety. The supervisor rejecting every proposal also cannot count as AI mission
success.

## 9. Verification gates

### IA-0 — protocol readiness

- hypothesis, control and statistical plan approved;
- dataset/holdout provenance and leakage checks pass;
- tool catalog, schemas, oracles and negative tests reviewed.

### IA-1 — candidate comparison

- immutable manifests and raw outputs captured;
- preregistered `gemma4:e2b` campaign completed;
- no hard safety failure within the approved acceptance rule;
- independent reproduction on a second clean environment.

### IA-2 — CM5 characterization

- stable, instrumented power path without undervoltage/throttling;
- boot, heartbeat, timeout, reset and storage recovery verified;
- latency, peak memory, energy and temperature measured across modes;
- worst-case context and repeated-inference thermal test completed.

### IA-3 — OBC/supervisor integration

- physical interface and fault containment verified;
- malformed/truncated/replayed inputs and resets injected;
- every critical invariant and boundary transition tested;
- evidence log reconstructed end-to-end.

### IA-4 — flight-like qualification input

- EMC, vibration and TVAC configuration controlled;
- post-environment functional/safety regression passes;
- radiation/SEE strategy and destructive latch-up protection reviewed;
- residual risks accepted by the designated authority.

No later gate may close while an earlier mandatory gate is open except through
a documented waiver with owner, rationale, residual risk and expiry.

## 10. Failure behavior

On timeout, invalid output, missing heartbeat, supervisor rejection, thermal/
power limit or storage fault:

1. discard the proposed action;
2. preserve deterministic OBC operation;
3. log the failure and context;
4. request graceful shutdown when possible;
5. power-cycle/lock out the AI rail only through deterministic policy;
6. require an authenticated ground command or approved autonomous recovery
   condition before re-enabling after repeated faults.

## 11. Current limitations

- no accepted model benchmark exists;
- no clean blind holdout exists;
- CM5 power/thermal measurements for `gemma4:e2b` are not yet acceptance data;
- flight rail, carrier, storage and radiation strategy are open;
- supervisor integration is a proposed bench architecture;
- environmental qualification has not been performed.

These limitations are project work items, not evidence of failure. They must
remain explicit until measured and reviewed.
