# Top Risks — AUSTRALIS-1 / DIY Nanosat MVP

**Revisión:** 2026-04-03
**Estado:** Active
**Trazabilidad:** `00_MVP/MVP v2.2.md`, `01_Mission/compliance_matrix.md`

Top riesgos consolidados (técnicos y operativos). Este documento referencia matrices específicas por tema.

## Top risks base (con links)

1) **Uplink LoRa no cierra con nodos típicos** (margen insuficiente, elevación baja)
- Ver: `07_Risk/comms_lora_uplink_feasibility_risk.md`

2) **CFO/Doppler impiden demodulación estable en BW125**
- Ver: `07_Risk/comms_lora_cfo_doppler_risk.md`

3) **Slots desalineados por hora/deriva** → colisiones
- Ver: `07_Risk/comms_uplink_slotting_time_sync_risk.md`

4) **TLE desactualizado** desplaza ventanas y baja recepción
- Ver: `07_Risk/comms_tle_update_risk.md`

5) **Integración de LoRa concentrator** (potencia/EMI/thermal/complexidad)
- Ver: `07_Risk/comms_concentrator_integration_risk.md`

6) **Downlink UHF con margen bajo en elevaciones bajas** (margen “de papel”)
- El enlace a 10° muestra solo **+1 dB teórico**; en la práctica puede ser negativo con pérdidas reales de polarización, body loss y detuning.
- **Máscara operativa provisional:** validación nominal solo para elevaciones ≥20°; operación a <20° es experimental/oportunista.
- Ver: `04_Communications/link_budget_uhf_preliminary.md` §6.2, `ADR-20260313-uhf-downlink-operational-mask.md`

7) **Déficit energético / brownouts** por picos y condiciones térmicas
- Ver: `03_Power/Power Budget.md`, `03_Power/EPS Sizing.md`, `07_Risk/eps_bench1_1s_risks.md`

8) **EMI interna (EPS switching vs RF/UHF)** degrada enlaces
- Ver: `04_Communications/rf_subsystem_overview.md`

9) **Fallas por reset / software no idempotente** (log corruption, modo inseguro)
- Mitigación: watchdog + boot SAFE + logs robustos.

10) **Regulatorio / coordinación de frecuencias** (amateur-sat + operación estación)
- Ver baseline y referencias en `00_MVP/MVP v2.2.md` y `99_References/`

11) **Supply chain TTC UHF** — RFFM6403 (FEM OpenLST original) está EOL; alternativa de PA discreto agrega complejidad de RF layout
- Mitigación: no depender de RFFM6403; definir front-end PA modular.

12) **Compliance con integrador de lanzamiento desconocida** — ICD, inhibiciones RF, fit-check, masa, materiales pendientes de dispenser
- Ver: `01_Mission/compliance_matrix.md`, ítems `Blocked by Integrator`

13) **Regulatorio / IARU sin coordinación cerrada**
- Ver: `01_Mission/compliance_matrix.md` CX-RF-04.

14) **Pico EPS vs consumo TX real desconocido** — estimación ~3 W del baseline vs posibles ~5 W con PA UHF real
- Ver: `architecture.md` CONF-01, `03_Power/Power Budget.md`
- Mitigación: no resolver sin medición real con hardware TX definitivo.

15) **Persistencia de datos de tierra ausente** — estado en memoria como única fuente de verdad impide evidencia reproducible
- Ver: `05_Software/ground_data_architecture.md`
- Mitigación: implementar arquitectura de datos de tierra documentada.

16) **Inmadurez real del hardware RF** — brecha entre madurez documental y hardware real
- El diseño de hardware RF orbital es esencialmente **placeholder**.
- Toda la documentación COMMS describe el diseño objetivo; la implementación real no existe todavía.
- Gate de cierre: Gate C.

31) **SatNOGS / separacion publico-privado mal definida**
- Riesgo: publicar demasiado en el beacon, asumir privacidad por framing cerrado, o introducir cifrado/contenido restringido sin cerrar compatibilidad regulatoria.
- Impacto: exposicion de datos de payload/operacion, rechazo regulatorio o dependencia indebida de una red receive-only para funciones de control.
- Mitigacion: `PUBLIC_BEACON` limitado a telemetria minima no sensible; `CONTROLLED_DOWNLINK` y `PRIVATE_UPLINK` solo por estacion/es propia/s o autorizada/s; revision regulatoria antes de fijar cifrado/confidencialidad.
- Ver: `08_Decisions/ADR-20260704-satnogs-public-beacon-private-payload-uplink.md`, `04_Communications/satnogs_public_beacon_architecture.md`.
- Gate de cierre: Gate C para beacon/decoder; Gate E/F para operacion segura end-to-end.

32) **Estacion terrena dual-use mal aislada o mal instalada**
- Riesgo: una estacion construida para SatNOGS receive-only se extiende a uplink privado sin interlocks, conmutacion T/R fail-safe, control de TX, puesta a tierra o calculo estructural adecuados.
- Impacto: TX accidental/no autorizado, dano de LNA/SDR/PA, evidencia de pruebas no confiable, riesgo fisico por torre/antena y baja disponibilidad operacional.
- Mitigacion: diseno dual-use desde fase 1; SatNOGS sin acceso al transmisor; switch T/R digital fail-safe; secuenciador con interlocks; pruebas por dummy load/coax antes de TX radiado; calculo estructural de torre/anclajes; puesta a tierra y proteccion de linea.
- Ver: `04_Communications/ground_station_dual_use_satnogs_australis.md`.
- Gate de cierre: Gate C para RX/beacon y T/R bench; Gate E/F para operacion end-to-end con uplink autorizado.

---

## Riesgos de diseño orbital y térmico (ADR-20260320)

| ID | Descripción | Probabilidad | Impacto | Consecuencia | Mitigación | ADR fuente |
|---|---|---|---|---|---|---|
| RSK-THR-01 | CM5 consume >6 W pico en Gate IA-2 | Media | Alto | Pad térmico insuficiente, requiere heat strap o reducción de duty-cycle. | Medir consumo real CM5 en Gate IA-2. Preparar heat strap de Cu flexible (sección ≥10 mm², largo ≤40 mm) como contingencia documentada. | `ADR-20260320-thermal-design-radiator-cm5-coupling.md` |
| RSK-THR-02 | AZ-93 no disponible en Argentina | Baja | Bajo | Usar Al anodizado blanco (menor performance, cierra modelo térmico con ~7°C adicionales en caso peor). | Cotizar AZ-93 importación USA (distribuidor AZ Technology). Evaluar anodizado local como fallback antes de PDR mecánico. | `ADR-20260320-thermal-design-radiator-cm5-coupling.md` |
| RSK-SOL-01 | Celda solar final tiene η < 20% | Baja | Medio | Margen energético baja de 3.4× a <2.5×. Puede requerir deployables o reducción de duty-cycle IA. | No cerrar selección de celda sin validar η real. Evaluar alternativas IBC antes de Gate IA-1. | `ADR-20260320-orbit-attitude-solar-layout-baseline.md` |
| RSK-ORB-01 | Variación estacional β reduce energía >15% | Cerrado | — | — | **Cerrado (2026-03-21).** Barrido anual (8760h, v9.3) ejecutado. La variación estacional real es < 5% en energía y < 7°C en temperaturas respecto al barrido de 24h. Margen 3.6× confirmado para ciclo completo. Peor caso térmico global: Tcm5 59°C (margen 21°C), Tbat 8.5°C (margen 18°C). | `ADR-20260320-orbit-attitude-solar-layout-baseline.md` |

---

## Riesgos del payload IA experimental (impactan el criterio de éxito primario)

17) **Sobreconsumo del payload IA no previsto** — consumo real del CM5 en inferencia desconocido hasta banco
- Riesgo: el pico real puede exceder el objetivo 6–7 W, comprometer el EPS o violar el power budget.
- Mitigación: no declarar consumo cerrado sin medición (Gate IA-2); duty-cycle corto; power-gating; fallback a sistema sin IA.
- Gate de cierre: Gate IA-2.

18) **Fallo de Linux / boot del CM5**
- Riesgo: el CM5 no bootea o no carga el modelo, dejando el payload IA inoperativo.
- Mitigación: watchdog supervisado por OBC (HB_AI); kill switch; AIHealthMonitor; misión continúa sin IA.
- Gate de cierre: Gate IA-2.

19) **Corrupción del PromptStore**
- Riesgo: el modelo usa un prompt inválido o desconocido, generando recomendaciones no deseadas.
- Mitigación: prompt seguro por defecto siempre disponible; hash de integridad en uplink; revertir con `AI_PROMPT_RESET_SAFE`.
- Gate de cierre: Gate IA-2.

20) **Recomendaciones erróneas del modelo**
- Riesgo: el modelo propone acciones peligrosas o incoherentes con el estado real del satélite.
- Mitigación: RuntimeSafetySupervisor rechaza propuestas que violen reglas determinísticas de misión; ninguna acción se ejecuta sin validación.
- **Mitigación parcial de banco alcanzada (2026-03-16):** el modelo Granite 350M fine-tuned mostró comportamiento útil y no trivial en holdout funcional, incluyendo regulatory refusal, SAFE fallback y RF fault isolation. pass_rate 57.14 %, avg_score_ratio 0.83. Defectos residuales menores en `ai_payload_state` contextual y `policy override` total — no invalidan el baseline funcional. El riesgo de recomendaciones erróneas en hardware real sigue abierto hasta Gate IA-2 (integración con RuntimeSafetySupervisor en CM5 real).
- Gate de cierre: IA-1 (parcial, evidencia de banco alcanzada) / IA-2 (cierre con hardware real).

21) **Deriva térmica del payload IA**
- Riesgo: el CM5 en operación activa genera calor; en órbita sin convección puede saturar límite térmico.
- Mitigación: análisis térmico pendiente (TBD); límites de tiempo de operación por ventana; power-gating para ciclos de enfriamiento. **No operar sin análisis térmico básico.**
- Gate de cierre: Gate IA-2 / E.

22) **Acoplamiento EMI / switching / ruido digital**
- Riesgo: ruido digital del CM5 se acopla en la banda UHF o LoRa, degradando sensibilidad del receptor.
- Mitigación: mutua exclusión IA ↔ TX UHF; evaluación de EMC en banco integrado; apantallamiento si corresponde.
- Gate de cierre: Gate IA-2 / E.

23) **Dependencia indebida del CONOPS en la IA**
- Riesgo: decisiones de diseño u operación se construyen asumiendo que la IA siempre estará disponible, invalidando el fallback determinístico.
- Mitigación: documentar explícitamente que el sistema siempre opera en modo determinístico sin el CM5; verificar operación normal del OBC con CM5 apagado en Gate IA-2.
- Gate de cierre: Gate IA-2.

24) **Extrapolación indebida del bench 1S al rail IA de vuelo**
- Riesgo: asumir que la rama `5V_AI_EXT` bench-only representa el rail IA final y contaminar decisiones de `EPS_Flight_Like_2S_MPPT` o `EPS_Flight_2S_MPPT`.
- Mitigación: documentar explícitamente que `EPS_Bench1_1S` usa inyección externa de 5V solo para Gate IA-2 y no valida el rail de vuelo 2S + MPPT.
- Gate de cierre: Gate IA-2 / D.

25) **Backfeed entre `5V_AI_EXT` y rails del bench**
- Riesgo: la inyección externa del CM5 retroalimenta `5V_AUX`, `3V3_OBC` o la cadena 1S bench, invalidando mediciones y creando fallas de seguridad.
- Mitigación: `J_AI_PWR` dedicado, `F_AI`, `SW_AI`, verificación explícita de no backfeed en `T11`.
- Gate de cierre: Gate IA-2.

26) **Potencia principal IA rutada por `JP1`**
- Riesgo: usar `JP1` como camino de potencia del CM5, sobrecargando el header y mezclando control con distribución principal.
- Mitigación: `JP1` definido como control/sense only y `J_AI_PWR` como entrada principal del rail IA.
- Gate de cierre: Gate IA-2.

27) **Switch IA insuficiente para la corriente de arranque del CM5**
- Riesgo: `SW_AI` entra en protección, colapsa tensión o no permite boot reproducible.
- Mitigación: no congelar MPN final antes de medir corriente real; usar `T12`, `T13` y `T20` para seleccionar margen.
- Gate de cierre: Gate IA-2.

28) **Caída excesiva si se usa `INA219` inline en el rail principal**
- Riesgo: el shunt degrada el arranque del CM5 o falsea la representatividad de las mediciones.
- Mitigación: tratar `INA219` inline como bench option y permitir metrología externa de banco como alternativa válida.
- Gate de cierre: Gate IA-2.

29) **Secuenciamiento incorrecto del CM5**
- Riesgo: habilitar interfaces o cortar energía fuera de orden genera boot incompleto, fallos espurios o lockouts falsos.
- Mitigación: secuencia explícita de encendido/apagado/kill (`T12`–`T15`) y monitoreo de `PGOOD_AI`, `AI_BOOT_OK` y `HB_AI`.
- Gate de cierre: Gate IA-2.

30) **Corrupción por apagado brusco del CM5**
- Riesgo: pérdida de integridad en logs, PromptStore o filesystem al cortar el rail IA sin shutdown lógico.
- Mitigación: apagado normal documentado, `AI_KILL_N` con timeout corto para emergencia y verificación de fallback determinístico en `T21`.
- Gate de cierre: Gate IA-2.

---

## Estado de mitigación de riesgos del payload IA (actualización 2026-04-03)

| Riesgo | Mitigación parcial alcanzada en banco | Pendiente |
|---|---|---|
| 17 — Sobreconsumo CM5 | No. Sin medición en CM5 real. | Gate IA-2 |
| 18 — Fallo Linux / boot | No. Sin prueba en CM5 real. | Gate IA-2 |
| 19 — Corrupción PromptStore | No. Sin prueba en CM5 real. | Gate IA-2 |
| 20 — Recomendaciones erróneas | **Sí, parcial.** Holdout funcional en banco mostró comportamiento útil y no trivial (pass_rate 57 %, avg_score_ratio 0.83). Defectos residuales menores documentados. | Gate IA-2 (integración supervisor real) |
| 21 — Deriva térmica | No. Sin análisis térmico en CM5 real. | Gate IA-2 / E |
| 22 — Acoplamiento EMI | No. Sin medición integrada. | Gate IA-2 / E |
| 23 — Dependencia CONOPS en IA | No. Sin prueba en hardware integrado. | Gate IA-2 |
| 24 — Extrapolación bench 1S -> rail IA de vuelo | No. Sin evidencia de T11–T21 ni transición a flight-like. | Gate IA-2 / D |
| 25 — Backfeed `5V_AI_EXT` -> rails bench | No. Falta ensayo T11. | Gate IA-2 |
| 26 — Potencia IA por `JP1` | Parcial documental. `JP1` quedó definido como control/sense only, falta inspección de wiring real. | Gate IA-2 |
| 27 — `SW_AI` insuficiente | No. Corriente de arranque CM5 no medida. | Gate IA-2 |
| 28 — `INA219` inline introduce caída excesiva | No. Falta decidir entre inline y metrología externa según T20. | Gate IA-2 |
| 29 — Secuenciamiento incorrecto CM5 | No. Falta ejecutar T12–T15. | Gate IA-2 |
| 30 — Corrupción por apagado brusco | No. Falta ejecutar apagado normal/emergencia y verificar logs. | Gate IA-2 |

## Próximos pasos
- Cada riesgo debe tener owner + evidencia de mitigación en planes de prueba.
- Verificar explícitamente T11–T21 sobre `EPS_Bench1_1S` extendido antes de cerrar riesgos 24–30.
- Ver plan de validación y stage-gates: `01_Mission/validation_plan_and_stage_gates.md`.
- Ver compliance matrix: `01_Mission/compliance_matrix.md`.
- Ver arquitectura detallada del payload IA: `05_Software/ai_payload_architecture.md`.
- Ver evidencia técnica de banco: `05_Software/AI PAYLOAD/ai_payload_bench_evidence_2026-03-16.md`.
