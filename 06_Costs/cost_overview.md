# Cost Overview — AUSTRALIS-1 / DIY Nanosat MVP (ROM)

**Revisión:** 2026-04-03
**Estado:** ROM (Rough‑Order‑of‑Magnitude), sin cotizaciones cerradas.

> Publicación: los exports DOCX/PDF/XLSX de proyección de costos no se
> versionan en el árbol público. Mantener aquí solo el resumen ROM y la BOM
> trazable sin cotizaciones cerradas.

Objetivo: tener una vista por subsistema y cost drivers, sin inventar precios.

## 1) Principios
- No inventar: si no hay dato → **TBD**.
- Usar rangos solo cuando exista fuente/experiencia/cotización.
- Separar "bench" vs "vuelo".

## 2) Estructura de costos (por subsistema)

### Estructura / térmico
- Estructura 1.5U (rail/frame), tornillería, separadores
- Prototipos (impresión 3D / CNC)
- Ensayos (vibración / thermal-vac)

### EPS
- Banco: ver `06_Costs/eps_bench1_1s_cost_model.md`
- `EPS_Bench1_1S` extendido para Gate IA-2: FPM bench + rail IA bench-only + inyección externa 5V para CM5 real
- Vuelo (2S): PCB + ICs de carga/MPPT + DC/DC + sensado + protección
- Batería de referencia actual: **2S1P con 18650 de 3.0 Ah (~22 Wh nominal)**
- Ruta de mitigación abierta: **2S2P (~44 Wh)** si Gate IA-2 demuestra necesidad real
- Target solar con payload IA activo: **TBD**
- La rama IA bench-only **no** pasa a baseline de vuelo por esta actualización documental

### OBC + storage
- MCU (STM32L4 class), watchdog, RTC, NOR + microSD, conectores

### COMMS
- UHF TRX + PA + filtros + conmutación RF + antena deployable
- **Uplink LoRa RX**: LoRa concentrator (si se adopta) y front-end RF

### GNSS-A
- Módulo GNSS + antena + RF matching

### Science Pack
- Sensores I2C (UV/ALS/MAG/temp) + acondicionamiento

### AI Payload experimental

| Stage | Descripción | Candidato | Costo |
|---|---|---|---|
| Bench | CM5 8 GB sobre carrier board COTS externa + integración con `EPS_Bench1_1S` extendido (`J_AI_PWR`, harness, control/sense) | Raspberry Pi CM5 8 GB — familia tecnológica adoptada; sourcing TBD | TBD |
| Flight-Like | CM5 4 GB + eMMC | Raspberry Pi CM5 4 GB + eMMC — familia tecnológica adoptada; sourcing TBD | TBD |
| Flight | CM5 class, hardware calificado | TBD — pendiente de Gate IA-2 y análisis de calificación | TBD |
| EGSE/Bench tools | Herramientas de desarrollo, breakout board para CM5, metrología de banco para `T20` / `T21` | TBD | TBD |

Delta bench-only a mantener separado del vuelo:
- conector `J_AI_PWR`
- harness de inyección externa 5V
- protección `F_AI`
- `SW_AI` como switch/eFuse/load-switch de alta corriente con MPN final TBD
- carrier board COTS para CM5
- adaptación de niveles UART / interfaz
- telemetría térmica básica del CM5
- medición adicional bench-only (`INA219` opcional o metrología externa)

### Ground segment
- Antena Yagi/Cross‑Yagi, LNA, receptor SDR/radio, tracking, PC

## 3) Cost drivers (lo que más mueve la aguja)
- Payload IA experimental (CM5 + carrier + almacenamiento + integración).
- Extensión bench-only de `EPS_Bench1_1S` para Gate IA-2 (harness, protección, switch IA, telemetría térmica y sensado).
- Selección de UHF (módulo/PA/filtros) + compliance.
- Ensayos ambientales.
- PCB assembly y retrabajos.
- Importación/disponibilidad local (Argentina).
- Cierre del camino EPS definitivo si la batería debe escalar de 2S1P a 2S2P o si hacen falta deployables solares.

## 4) Próximos pasos P2
- Crear BOM por subsistema con partes candidatas.
- Añadir fuente/fecha para cada rango.
- Separar BOM bench vs flight-like vs flight.
- Mantener explícitamente qué parte del delta IA es bench-only y no migra al baseline de vuelo.
- Cotizar explícitamente batería de referencia 2S1P y la ruta 2S2P.
- Cotizar el delta bench-only de Gate IA-2 (`J_AI_PWR`, harness, `F_AI`, `SW_AI`, carrier board, interfaz y termometría).
- Mantener `TBD` el impacto económico del cierre solar con payload IA hasta Gate IA-2.
