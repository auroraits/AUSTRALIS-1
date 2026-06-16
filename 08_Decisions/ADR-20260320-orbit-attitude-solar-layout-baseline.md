# ADR-20260320-orbit-attitude-solar-layout-baseline

- **Fecha:** 2026-03-20
- **Estado:** Accepted

---

## Contexto

Se ejecutó un barrido paramétrico de 400 candidatos orbitales/térmicos con el simulador
AUSTRALIS v9.2 (auditado y corregido: eclipse cónico con penumbra, albedo modulado por
posición subsolar, view factors analíticos por altitud, CM5 con estado OFF fuera de
duty-cycle, C_batt corregido a 100 J/K, η solar parametrizable). Parámetros del barrido:
η=24% (IBC/Maxeon), albedo=0.30, IR terrestre=237 W/m², horizonte 24h, dt=120s.

Los resultados fueron validados por sanity check (todas las métricas dentro de rangos
físicos esperados) y por simetría LTAN (10h vs 14h producen energía idéntica con
radiadores opuestos).

---

## Decisión

### Órbita target
- **Tipo:** SSO (Sun-Synchronous Orbit)
- **Inclinación:** ~98° (rango óptimo 97.6°–98.8°)
- **Altitud de diseño:** 600 km (rango aceptable 550–650 km; sube de 550 km baseline previo)
- **LTAN:** 10:00h preferido (simétrico con 14:00h; 10h preferido por mayor disponibilidad de rideshare SSO matutinos)
- **Eclipse nominal:** ~34%

### Actitud nominal
- **10×10 nadir:** cara cuadrada +Z apuntando a Tierra (nadir), eje +X en dirección de avance (ram).
- Justificación: +2 Wh/24h vs 10×15 nadir; cara cuadrada nadir facilita antenas UHF desplegables estándar.

### Layout de paneles solares (body-mounted)
- **Paneles:** +Y (150 cm²), −X (150 cm²), +X (150 cm²), −Z (100 cm²) — 4 caras, ~484 cm² activa (packing 88%).
- **Radiador:** −Y (150 cm²) para LTAN 10h (cara antisolar).
- **Cara nadir +Z:** libre para antenas UHF desplegables, sensores, opción de panel futuro.
- **Paneles desplegables:** no necesarios para baseline. El power budget cierra con body-mounted.

### Energía
- Generación simulada: ~72 Wh/24h (~4.5 Wh/órbita) con η=24%.
- Consumo con AI payload (20% duty, 4.5W activo, 0W off): ~1.34 Wh/órbita.
- Margen: 3.4× energy-positive. **TBD — validar con η real de celda seleccionada y consumo real CM5 medido en Gate IA-1.**

### Celdas solares
- Baseline funcional: IBC (Interdigitated Back Contact) tipo SunPower/Maxeon, η~24%.
- 7 celdas: 3 caras rectangulares × 2 half-cut + 1 cara cuadrada × 1 celda.
- **TBD — familia de celda final no seleccionada.** Opciones abiertas: IBC premium (24%), mono-Si genérico (20%), AnySolar IXOLAR. Ver investigación solar en `03_Power/`.

---

## Alternativas consideradas

1. **10×15 nadir:** Score 72.5 vs 74.2. Menor energía (−2 Wh/24h). Rechazada.
2. **LTAN 12:00h (mediodía):** Peor score (43.5). Eclipse máxima, energía mínima. Rechazada.
3. **Altitud 500 km:** Score 68.9 vs 74.2. Menor energía y vida orbital más corta. Rechazada.
4. **Altitud 650 km:** Score 74.2 (máximo). Aceptable pero 600 km ofrece balance entre energía y deorbit compliance. Se elige 600 km como target nominal, 650 km como aceptable.

---

## Tradeoffs / riesgos

- El barrido evalúa 24h en fecha fija. La variación estacional del ángulo β no está capturada. Riesgo: caso peor estacional podría reducir energía ~15%. Mitigación: correr barrido en solsticios antes de congelar LTAN.
- La eficiencia de 24% no está cerrada. Si se usa mono-Si (20%), el margen baja de 3.4× a ~2.8×. Sigue cerrando.
- CONF-01 (pico EPS con TX UHF) sigue abierto. No afecta esta decisión orbital pero sí el power budget final.

---

## Documentos impactados

- `00_MVP/MVP v2.2.md` — §4 (órbita), §2.1 (layout/estructura), §8 (EPS targets)
- `SYSTEM_BASELINE.md` — §orbit, §structure, §power
- `architecture.md` — §6 snapshot de decisiones
- `01_Mission/mission_definition.md` — parámetros orbitales
- `02_Structure/` — layout de caras, asignación de paneles/radiador
- `03_Power/EPS Sizing.md` — configuración solar, área activa
- `03_Power/Power Budget.md` — validación con simulador
- `01_Mission/requirements_matrix.md` — agregar STR-REQ y THR-REQ
- `01_Mission/compliance_matrix.md` — entradas de layout solar y órbita
- `06_Costs/BOM_master.csv` — celdas solares (Stage: Flight-Like, 7 unidades, TBD MPN/precio)

---

## Addendum — Validación por barridos semestral y anual (2026-03-21)

### Barridos ejecutados
- **Semestral (4320h / 180 días):** simulador v9.2, 400 candidatos. Captura variación estacional de β. Un hallazgo intermedio sugería +Z como radiador alternativo, pero se identificó sesgo de fase estacional por cubrir solo medio ciclo.
- **Anual (8760h / 365 días):** simulador v9.3 con exportación de los 6 radiadores evaluados por candidato. Cubre ciclo completo de β. Comparación directa cara a cara.

### Resultado: decisiones confirmadas sin cambios

**Radiador −Y confirmado.** Para LTAN 9.5–10.0h y 650 km:
- −Y y +Z son equivalentes en energía anual (Δ = −0.1 Wh/día, −0.1%).
- −Y tiene Tcm5 1.8°C menor (43.1 vs 44.9°C) y Tbat 1.1°C mayor (17.5 vs 16.4°C).
- −Y tiene peor caso global más robusto: margen Tcm5 21°C vs 12°C, margen Tbat 18°C vs 12°C.
- −Y tiene 50% más área de radiador (150 cm² vs 100 cm²).
- −Y deja cara +Z libre para antenas UHF desplegables.
- +X fue evaluada como tercera opción: inferior en energía (−13 Wh/día vs −Y) y márgenes térmicos más ajustados.

**Órbita SSO 650 km, LTAN 9:30h confirmada.** El top-30 anual converge a 650 km. LTAN 9.5h es el óptimo; simétrico con 14.0h (Δ energía < 1%).

**Actitud 10×10 nadir confirmada.** Sigue superando a 10×15 nadir en score y energía.

**Paneles +Y, ±X, −Z confirmados.** Sin cambio.

**Margen energético anual: 3.6×** (consistente con 3.4× del barrido 24h — la variación estacional no degrada el margen).

### Riesgo RSK-ORB-01 cerrado
El riesgo "variación estacional β reduce energía >15%" queda cerrado con evidencia del barrido anual. La variación real es < 5% entre el barrido de 24h y el promedio anual.
