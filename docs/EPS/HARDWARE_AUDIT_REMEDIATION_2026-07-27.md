# Trazabilidad de remediación — hardware, EPS, estructura y simulación

**Fecha:** 2026-07-27
**Rama:** `audit/remediation-2026-07-27`
**Estado:** revisión técnica de cierre del frente; no equivale a hardware
Flight-Ready

## 1. Criterio de cierre

En un proyecto en desarrollo, “abordado” no significa inventar evidencia que
todavía no existe. Un hallazgo se considera tratado cuando:

1. se corrige la fuente, fórmula o implementación defectuosa; o
2. se retira la afirmación no sustentada, se declara el estado abierto y se
   define un criterio verificable para cerrarlo.

Un diseño físico pendiente sigue `Open`, pero ya no puede promoverse como
`Accepted`, confirmado, conforme o fabricable.

## 2. Matriz de cobertura

| # | Hallazgo auditado | Tratamiento en este frente | Estado técnico |
|---:|---|---|---|
| 1 | Envolvente 1.5U de 150 mm | Base corregida a `170.2 ± 0.1 mm`; áreas históricas invalidadas | Corregido |
| 2 | Cortos explícitos en KiCad EPS | Wires peligrosos eliminados; proyecto bloqueado y validado como placeholder sin cobre | Corregido / diseño real Open |
| 3 | BMS y charger no implementados | Pass-throughs eliminados; funciones y gate de diseño explícitos | Controlado Open |
| 4 | Balance térmico/radiativo no físico | Albedo, IR, emisión Tierra/espacio y extracción FV corregidos; modelo marcado incompleto | Corregido / correlación Open |
| 5 | Barrido “SSO” sin condición SSO | Inclinación derivada por altitud imponiendo precesión J2 solar | Corregido |
| 6 | Actitud perfecta sin ADCS | LVLH perfecto queda solo como sensibilidad ideal; requisitos ADCS/dispersiones abiertos | Controlado Open |
| 7 | PCB EPS vacío presentado como fuente | Hard lock `NON-FABRICABLE`, sin outline/pads/cobre y checklist de liberación | Corregido / diseño real Open |
| 8 | Power-gating bypassed y telemetría flotante | Pass-throughs retirados; funciones exigidas antes de ERC/DRC/fabricación | Corregido / diseño real Open |
| 9 | Topología solar no realizable | Selección de siete celdas/MPPT común retirada; criterios eléctricos por cara/string | Controlado Open |
| 10 | Score cambia con el horizonte | `thermalKey`, min-max y ranking automático eliminados; energía en Wh/día | Corregido |
| 11 | CSV y ADR no reproducibles | CSV antiguos invalidados; export CSV+manifest con inputs, commit y SHA-256 | Corregido / rerun Open |
| 12 | ADR orbital contradictoria | Simulador ya no selecciona órbita; requiere propagación a ADR/baseline canónicos | In-scope corregido / propagación requerida |
| 13 | Modelica obsoleto usado como evidencia | Marcado Historical Snapshot; runner desactivado hasta reconstrucción/correlación | Corregido |
| 14 | Fallback térmico viola `α/ε` | Anodizado blanco retirado como equivalente; cupón y EOL requeridos | Corregido / selección Open |
| 15 | Conductancia térmica sin trazabilidad | Red de resistencias definida; pad/strap recalculados; ensayo calorimétrico requerido | Corregido / diseño Open |
| 16 | Seguridad térmica de batería incompleta | Límites separados carga/descarga/supervivencia e interlock exigidos | Controlado Open |
| 17 | Mínimos eléctricos CDS mal definidos | Requisitos §2.3–2.4, inhibiciones y timers explicitados con V&V | Corregido / implementación Open |
| 18 | Arquitectura de batería no cumple ADR | BMS completo, balanceo, protección secundaria, FMEA y V&V exigidos | Controlado Open |
| 19 | Sin ingeniería estructural verificable | CAD ausente tratado como blocker; plan de CAD, masa/CG/inercia, modos y fit-check | Controlado Open |
| 20 | Plan ambiental opcional/insuficiente | Matriz ambiental obligatoria y reglas de evidencia configurada | Corregido / niveles ICD Open |
| 21 | Sin análisis de radiación | Plan COTS-to-flight TID/SEE/SEL/almacenamiento/derating incorporado | Controlado Open |
| 22 | Power budget inconsistente/incompleto | Ledger paramétrico por modo, órbita física, unidades y missing loads fail-open | Corregido / mediciones Open |
| 23 | Solar sin degradación/mismatch | Ledger BOL/EOL, I-V, MPPT, sombra, pérdida de string y cupón requeridos | Controlado Open |
| 24 | Risk register cerraba riesgos inválidos | Evidencia orbital/térmica histórica invalidada; requiere propagación al registro canónico | Propagación requerida |
| 25 | Masa típica 1.5U incorrecta | Referencia CDS corregida a 3.00 kg, subordinada al ICD | Corregido / propagación requerida |
| 26 | Block Diagram obsoleto usado como ICD | Marcado Historical Snapshot / no usar para diseño o fabricación | Corregido |
| 27 | Reglas PCB contradictorias | Mínimo/default de track normalizados; release requiere netclasses verificadas | Corregido |
| 28 | KiCad RF vacío | Fuera de este frente (`04_Communications`); debe quedar placeholder explícito | Propietario COMMS |
| 29 | “Promedio” usado para extrema | Artefactos antiguos invalidados; outputs actuales nombran rangos/extremos | Corregido / propagación requerida |
| 30 | Capacidades térmicas sin provenance | Placeholders identificados y exportados; CAD/BOM/ensayo requeridos sin doble conteo | Controlado Open |
| 31 | BOM sin cierre de masa/volumen/compliance | Entradas requeridas definidas; actualización de `06_Costs` corresponde al frente BOM | Propagación requerida |
| 32 | Citas CDS desactualizadas | Nueva trazabilidad a Rev. 14.1 §§2.3–2.4 y pp. 14–15 | Corregido / propagación requerida |
| 33 | Fuentes Borealis/Australis divergentes | Modelo activo identificado `australis-sim-v10-pre`; Borealis queda histórico | Corregido |

## 3. Evidencia por commit

- `aa4d662` — base mecánica 1.5U y requisitos estructurales.
- `97ac3c1` — normalización de formato de la base estructural.
- `9c893d2` — bloqueo fail-closed del placeholder KiCad EPS.
- `a6ea1b2` — ledger EPS, batería, solar y radiación.
- `034d698` — verificación ambiental obligatoria.
- `56f4095` — SSO, física térmica, no-ranking y reproducibilidad.
- `fb71c6f` — materiales, coating, coupling, strap y batería térmica.
- `dac4cae` — mínimos CDS de lanzamiento e inhibiciones.
- `48cd2a2` — matriz de cobertura 33/33.
- `6983227` — identificador exacto del candidato `gemma4:e2b`.
- `d86b05f` — retiro de constantes heurísticas residuales de diseño EPS.
- `762e42f` — checksum de fuente CDS y redacción exacta de inhibiciones.
- `dd8e32d` — controles mecánicos y ambientales trazados al CDS.
- `24e7a2c` — extremos térmicos all-state y métricas de batería.
- `ed6243c` — detección visible de saturación por clamp numérico.

## 4. Verificación ejecutable

Desde la raíz del repositorio:

```powershell
python -B 03_Power/EPS_PCB/EPS_Bench2S_FlightLike/validate_eps_placeholder.py
python -B 03_Power/power_budget.py --self-test
python -B 05_Software/SIM/validate_simulation.py
```

Estos checks verifican la documentación y los modelos actuales. No sustituyen
ERC/DRC nativo, CAD/FEA, ensayo eléctrico, thermal balance, TVAC, ambiente,
EMC ni calificación.

Verificación de cierre ejecutada el 2026-07-27:

- validador del placeholder KiCad: `PASS`;
- calculadora de potencia `--self-test`: `PASS`;
- validador SIM: `PASS`, con
  `iSSO(600/650)=97.787670/97.985997°`;
- parse de JSON y sintaxis del módulo JavaScript con Node: `PASS`;
- carga real del HTML y módulos CDN en Edge headless: `PASS`;
- barrido runtime de un caso 600 km/9.5 h LTAN: una fila, seis radiadores,
  sin ranking, fatal ni clamp;
- export runtime: CSV y manifest con 58 columnas, una fila, revisión fuente,
  estado `INCOMPLETE_NOT_FOR_DESIGN_DECISIONS` y SHA-256 coincidente;
- `git diff --check` en las rutas del frente: `PASS`.

El barrido runtime fue una prueba funcional efímera del software, no evidencia
de selección orbital/térmica; sus archivos temporales se eliminaron.

## 5. Bloqueos físicos remanentes

- `kicad-cli` y un diseño EPS real siguen ausentes: no existe ERC/DRC de una
  placa fabricable.
- OpenModelica (`omc`) no está instalado y, en cualquier caso, el artefacto
  Modelica actual está deshabilitado por ser histórico.
- No existe CAD estructural controlado ni ADCS implementado.
- No hay selección de celda/BMS/MPPT/coating/strap ni datos de artículo.
- El propagador y el modelo térmico no están validados contra herramienta
  independiente ni correlacionados con ensayo.
- Los niveles ambientales y criterios finales dependen del ICD.

Estos bloqueos son parte explícita del estado del proyecto y no pueden
cerrarse mediante documentación solamente.
