# ADR-20260314-eps-state-4-levels

- **Fecha:** 2026-03-14
- **Estado:** Accepted

---

## Contexto

El modelo operativo canónico del baseline documentaba `EPS_STATE = NOMINAL | SAFE | CRIT`, pero el presupuesto de potencia vigente ya trabajaba con cuatro escalones energéticos (`E0` a `E3`) para gobernanza práctica del sistema.

La incorporación del payload IA (Inteligencia Artificial) y la necesidad de discriminar mejor entre supervivencia, conservación, operación regular y operación con margen alto hacen insuficiente el modelo de 3 niveles.

Sin una ampliación formal del estado energético, distintos documentos pueden seguir usando:
- una taxonomía de 3 niveles en misión/software/baseline,
- y una taxonomía de 4 niveles en EPS/power budget,

lo que rompe la coherencia operativa del sistema.

---

## Decisión

Se amplía el modelo canónico de estado energético a:

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

Semántica normativa:

| EPS_STATE | Descripción | Política |
|---|---|---|
| `CRIT` | Estado de carga crítico; supervivencia | Fuerza `MISSION_MODE = SAFE` sin excepción. Solo housekeeping mínimo y `COMMAND_ACK`. Payload IA OFF. |
| `LOW` | Estado de carga bajo; conservación | `SAFE` por defecto. Puede mantenerse `NOMINAL` solo para housekeeping esencial explícitamente permitido. GNSS OFF, sin dumps, sin actividad científica, payload IA OFF. |
| `NOMINAL` | Estado de carga adecuado | Actividad científica y LoRa RX permitidos. Downlink estándar. Payload IA permitido solo en ventana experimental y fase de sol. |
| `HIGH` | Estado de carga alto; margen amplio | Downlink window extendido. Payload IA con ventana ampliada si condiciones térmicas y operativas lo permiten. |

Reglas de transición:

1. `EPS_STATE = CRIT` obliga a `MISSION_MODE = SAFE`.
2. `EPS_STATE = LOW` mantiene `SAFE` por defecto; una permanencia en `NOMINAL` solo se admite para housekeeping esencial explícitamente permitido.
3. El payload IA solo puede operar con `EPS_STATE >= NOMINAL`, `MISSION_MODE = NOMINAL` y fase de sol.
4. La nomenclatura histórica `E0/E1/E2/E3` puede mantenerse como alias de cálculo en EPS, pero debe mapearse explícitamente a `CRIT/LOW/NOMINAL/HIGH`.

---

## Alternativas consideradas

1. **Mantener 3 niveles (`SAFE/NOMINAL/CRIT`)**:
   - Rechazada. No representa la granularidad operativa ya usada en EPS ni la necesaria para el payload IA.
2. **Agregar un solo nivel extra sin semántica explícita**:
   - Rechazada. Agrega complejidad sin cerrar políticas operativas.
3. **Modelo de 4 niveles `CRIT/LOW/NOMINAL/HIGH`**:
   - Elegida. Mantiene claridad operativa, alinea EPS con FSW y evita ambigüedad en reglas de habilitación.

---

## Tradeoffs / riesgos

| Factor | Consideración |
|---|---|
| A favor | Coherencia entre Power Budget, baseline, misión y FSW; mejor control energético para payload IA y downlink. |
| En contra | Requiere sincronización transversal de documentación y futuros artefactos de software/telemetría. |
| Riesgo | Que sobrevivan referencias al modelo de 3 niveles en documentos activos. |
| Mitigación | Actualización explícita de baseline, misión, software, compliance y arquitectura en esta pasada. |

---

## Implicancias (archivos a actualizar)

- `AGENTS.md` — modelo operativo canónico.
- `00_MVP/MVP v2.2.md` — §3.2 y reglas operativas.
- `SYSTEM_BASELINE.md` — §3.4 modelo operativo.
- `architecture.md` — §7 modelo canónico, §10 baseline FSW/OPS.
- `01_Mission/mission_definition.md` — CONOPS.
- `01_Mission/requirements_matrix.md` — MIS-REQ-08, MIS-REQ-10, MIS-REQ-12.
- `01_Mission/compliance_matrix.md` — ítems que referencien `EPS_STATE`.
- `03_Power/Power Budget.md` — §6.1, mapeo `E0/E1/E2/E3`.
- `05_Software/software_framework_mvp22.md` — modelo de estados y transiciones.
- `05_Software/ai_payload_architecture.md` — políticas operativas del payload IA.