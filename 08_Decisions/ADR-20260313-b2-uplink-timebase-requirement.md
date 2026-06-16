# ADR-20260313-b2-uplink-timebase-requirement

- **Fecha:** 2026-03-13
- **Estado:** Accepted

---

## Contexto

El modo B2 (pass-aware slotted) del uplink LoRa requiere que los nodos transmitan en slots determinísticos calculados por firmware. Esto exige que el nodo tenga una base temporal suficientemente precisa: si la hora del nodo difiere de la esperada por el satélite en más del guard time del slot, los paquetes caerán fuera de su slot asignado y colisionarán con los de otros nodos.

La documentación anterior reconocía el riesgo de deriva temporal pero era permisiva con el supuesto "ESP32 + RTC + GNSS ocasional", sin especificar condiciones de aceptación para B2 ni acción de fallback obligatoria.

Esta ADR formaliza la restricción: B2 NO puede depender implícitamente de una base temporal no validada.

---

## Decisión

El modo B2 (pass-aware slotted) queda sujeto a las siguientes reglas normativas:

### Regla 1 — Condiciones de aceptación para B2
Para que un nodo opere en B2, debe cumplir **al menos una** de las siguientes condiciones:

1. **Base temporal validada experimentalmente:** deriva del RTC/cristal medida y documentada como dentro del guard time bajo condiciones de temperatura representativas del despliegue real.
2. **Cristal/RTC externo adecuado:** fuente de tiempo de baja deriva conocida (p. ej. 32.768 kHz con especificación de histéresis térmica) que garantice error dentro del guard time.
3. **Resincronización activa:** el nodo disciplina su RTC con una fuente confiable (GNSS u otra) con periodicidad suficiente para mantener la precisión requerida para el presupuesto de slot.
4. **Otra estrategia documentada y validada:** cualquier otro mecanismo que garantice el error temporal dentro del guard time, con evidencia experimental.

### Regla 2 — Fallback obligatorio
Si ninguna de las condiciones de la Regla 1 se cumple → el nodo **shall operar en B1** (always-on slotted) hasta que la base temporal sea validada.

### Regla 3 — No fijar cifras de deriva sin evidencia
No se fijan números exactos de ppm de deriva de RTC en esta ADR. Las cifras de deriva dependen del hardware específico, temperatura y condiciones reales. Deben medirse con el hardware de clase nodo real.

### Regla 4 — Requisito de verificación
La validación de la base temporal es criterio de salida explícito de Gate B. Ver `01_Mission/validation_plan_and_stage_gates.md` Gate B y `01_Mission/requirements_matrix.md` COMMS-UL-06.

---

## Alternativas consideradas

1. **Sin restricción (permisivo):** dejar que cualquier nodo intente B2. Rechazado: implica desalineación silenciosa de slots y pérdida de capacidad sin diagnóstico.
2. **Solo TCXO / GPS-disciplined:** demasiado restrictivo para el objetivo de "nodo de clase típica bajo costo". Rechazado.
3. **Condiciones de aceptación + fallback obligatorio a B1** (elegida): permite B2 con cualquier estrategia válida, asegura diagnóstico explícito y fallback controlado.

---

## Tradeoffs / riesgos

- A favor: B2 se mantiene viable con hardware bajo costo si se valida experimentalmente; fallback a B1 garantiza operación siempre.
- Riesgo residual: si el hardware de clase nodo tiene deriva mayor a la esperada bajo condiciones reales (temperatura, ruido), B1 puede ser el único modo viable.
- Mitigación: diseñar el guard time con margen conservador (§6 del protocolo); medir deriva real antes de Gate B.

---

## Implicancias (archivos actualizados)

- `04_Communications/uplink_lora_slotted_protocol.md` — §10 reescrito con condiciones de aceptación y fallback.
- `01_Mission/requirements_matrix.md` — COMMS-UL-06 agregado; COMMS-UL-02 actualizado.
- `01_Mission/validation_plan_and_stage_gates.md` — Gate B actualizado con criterio de validación de base temporal.
- `architecture.md` — §13 pendiente #10.
- `07_Risk/top_risks.md` — R3 (slots desalineados) referencia esta ADR.
