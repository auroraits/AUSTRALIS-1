# ADR-20260320-thermal-design-radiator-cm5-coupling

- **Fecha:** 2026-03-20
- **Estado:** Accepted

---

## Contexto

El simulador v9.2 modela un balance térmico de nodos concentrados (6 caras + frame +
batería + CM5) con radiación solar, albedo modulado, IR terrestre y disipación interna.
Los resultados muestran que todas las configuraciones del sweet spot orbital mantienen
Tmax CM5 ≤ 44°C y Tmin batería ≥ 12°C, con amplio margen respecto a límites operativos
(CM5 ≤ 80°C, Li-ion descarga ≥ −10°C).

---

## Decisión

### Cara radiadora
- **−Y** para LTAN 10h (antisolar). Se invierte a +Y si LTAN resulta 14h.
- Área: 150 cm² (cara rectangular 10×15 cm del 1.5U).
- Propiedades ópticas de diseño: α_solar ≤ 0.20, ε_IR ≥ 0.88.

### Recubrimiento del radiador
- **Preferido:** AZ-93 (AZ Technology) — pintura blanca cerámica inorgánica.
  - α_solar = 0.13–0.17, ε_IR = 0.89–0.93. Heritage: ISS, LDEF, MISSE.
  - Degradación en LEO: <4% en absortancia solar tras >700 ESH (Equivalent Sun Hours).
  - Aplicación: spray o pincel sobre aluminio limpio.
  - **TBD — verificar disponibilidad y costo para Argentina. Alternativa: importar vía distribuidor USA.**
- **Fallback:** Aluminio anodizado blanco (α_solar = 0.20–0.35, ε_IR = 0.82–0.86).
  - Disponible en anodizado local AR. Menor performance pero cierra el modelo térmico.
- Ambas opciones deben cumplir outgassing CDS Rev. 14.1 §2.1.7 (TML ≤ 1.0%, CVCM ≤ 0.1%).

### Acoplamiento térmico CM5 → radiador
- Ruta: CM5 SoC → pad térmico → pared interior cara −Y → recubrimiento exterior → espacio.
- Pad térmico: ~1 mm, tipo Fujipoly XR-Um (k ≈ 17 W/m·K) o equivalente.
  - Conductancia estimada: ~1.5 W/K para área de contacto 30×22 mm.
  - Suficiente para 4.5 W pico con ΔT ≤ 3°C en la interfaz.
- **TBD — validar ΔT real en banco con prototipo mecánico.** La conductancia G_cm5_radiador = 0.60 W/K del modelo es conservadora. Si la medición real es peor, evaluar heat strap de Cu flexible (sección ≥ 10 mm², largo ≤ 40 mm).
- Si la geometría del stack de PCBs no permite montaje directo del CM5 contra la pared −Y, usar heat strap como ruta alternativa documentada.

### Batería
- C_batt del modelo térmico: 100 J/K (2× 18650 ~90g @ ~1100 J/(kg·K)).
- Tmin batería en eclipse: ~20°C para configuración óptima. Amplio margen sobre −10°C.
- No se requiere calentador de batería (heater) para el baseline.

---

## Alternativas consideradas

1. **Radiador en +Z (nadir):** Buen view factor a espacio frío pero sacrifica cara útil para antenas. Rechazada.
2. **Sin radiador dedicado (todas las caras con panel):** Riesgo de sobrecalentamiento CM5. Rechazada.
3. **MLI (Multi-Layer Insulation):** No efectivo en CubeSats por volumen y edge effects (ref: NASA SmallSat Thermal SoA 2024). Rechazada.
4. **Heat pipe:** Sobredimensionado para 4.5 W. Masa y costo innecesarios. Rechazada.

---

## Tradeoffs / riesgos

- Si el CM5 consume más de ~6 W pico (a medir en Gate IA-1), el ΔT en la interfaz sube y puede requerir heat strap en vez de pad. Riesgo mitigable.
- AZ-93 puede no estar disponible fácilmente en Argentina. El fallback (anodizado blanco) cierra igualmente pero con menor margen (α_solar 0.25 vs 0.15 = ~7°C más caliente en caso peor).
- La variación estacional del β no está capturada en el barrido de 24h. Un β alto (~60°+) reduce eclipse y puede calentar caras normalmente frías. Correr sensibilidad.

---

## Documentos impactados

- `00_MVP/MVP v2.2.md` — §2 (estructura/térmico), §8 (targets EPS térmicos)
- `SYSTEM_BASELINE.md` — §thermal
- `02_Structure/` — crear o actualizar documento de diseño térmico
- `03_Power/Power Budget.md` — nota sobre margen térmico de batería
- `01_Mission/requirements_matrix.md` — THR-REQ-01 a THR-REQ-04
- `01_Mission/compliance_matrix.md` — entradas térmicas
- `06_Costs/BOM_master.csv` — AZ-93 o anodizado (TBD), pad térmico (TBD)

---

## Addendum — Validación térmica anual (2026-03-21)

### Datos térmicos actualizados (barrido anual 8760h, rad=−Y, LTAN 9.5h, 650 km, 10×10 nadir)
- **Tcm5 promedio sweet spot:** 43.1°C (margen 37°C al límite 80°C). Barrido 24h reportaba 40.1°C.
- **Tbat promedio sweet spot:** 17.5°C (margen 28°C al límite −10°C). Barrido 24h reportaba 20.7°C.
- **Peor caso global anual (todos los LTANs/altitudes):** Tcm5 = 59.2°C (margen 21°C), Tbat = 8.5°C (margen 18°C).
- La variación respecto al barrido de 24h es de +3°C en Tcm5 y −3°C en Tbat. Los márgenes operativos siguen amplios.
- Heater de batería sigue siendo **no requerido** (margen ≥ 18°C en peor caso global).

### Comparación directa −Y vs +Z como radiador (datos anuales, sweet spot)
| Métrica | −Y | +Z | Δ |
|---|---|---|---|
| Wh/día | 69.9 | 70.0 | −0.1% |
| Tcm5 | 43.1°C | 44.9°C | −Y 1.8°C mejor |
| Tbat | 17.5°C | 16.4°C | −Y 1.1°C mejor |
| Peor Tcm5 global | 59.2°C (margen 21°C) | 68.0°C (margen 12°C) | −Y 9°C mejor |
| Peor Tbat global | 8.5°C (margen 18°C) | 2.2°C (margen 12°C) | −Y 6°C mejor |
| Área radiador | 150 cm² | 100 cm² | −Y 50% mayor |

### Acoplamiento CM5 → −Y confirmado
La ruta CM5 → pad térmico → pared interior −Y sigue vigente. El incremento de Tcm5 de 40°C (24h) a 43°C (anual) no cambia el dimensionamiento del pad. El margen de 37°C al límite operativo es amplio.
- `07_Risk/top_risks.md` — riesgo térmico CM5, disponibilidad AZ-93
