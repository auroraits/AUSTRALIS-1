# BorealisThermalConcept — guía rápida

## Archivos
- `BorealisThermalConcept.mo` — paquete principal Modelica.
- `run_BorealisThermalConcept.mos` — script mínimo para cargar y simular.

## Convención de caras
1. `+X` = ram
2. `-X` = wake
3. `+Y`
4. `-Y`
5. `+Z` = nadir (cara Tierra)
6. `-Z` = zenith (cara espacio / radiador preferido)

## Modelos incluidos
- `BorealisThermalConcept.LEO500kmNadir_1p5U`
- `BorealisThermalConcept.Example_CM5_To_ZenithRadiator`
- `BorealisThermalConcept.Example_Battery_MoreIsolated`
- `BorealisThermalConcept.Example_Battery_WarmingBias`

## Cómo abrirlo en OMEdit
1. Copiá los archivos a una carpeta local en tu PC.
2. En OMEdit: `File > Open Directory` y elegí esa carpeta.
3. En el panel izquierdo abrí `BorealisThermalConcept.mo`.
4. Hacé doble clic en `BorealisThermalConcept.LEO500kmNadir_1p5U`.
5. Presioná `Simulate`.

## Setup recomendado de simulación
- Start Time: `0`
- Stop Time: `18000` s (~3.2 órbitas a 500 km)
- Interval: `10` s
- Solver: `dassl`
- Tolerance: `1e-6`

## Variables útiles para graficar
### Temperaturas
- `T_cm5_C`
- `T_batt_C`
- `T_frame_C`
- `T_face_C[1]` ... `T_face_C[6]`

### Ambiente orbital
- `eclipseFlag`
- `orbitAngle_deg`
- `sunInc[1]` ... `sunInc[6]`
- `Q_sun[1]` ... `Q_sun[6]`
- `Q_albedo[1]` ... `Q_albedo[6]`
- `Q_earthIR[1]` ... `Q_earthIR[6]`
- `Q_radToSpace[1]` ... `Q_radToSpace[6]`

### Potencia solar
- `panelPowerFace[1]` ... `panelPowerFace[6]`
- `P_panelGross`
- `P_panelNet`
- `E_panelGross_Wh`
- `E_panelNet_Wh`

### Cargas internas
- `P_cm5`
- `E_cm5_Wh`
- `Q_frameToFace[1]` ... `Q_frameToFace[6]`
- `Q_cm5ToFace[1]` ... `Q_cm5ToFace[6]`
- `Q_battToFace[1]` ... `Q_battToFace[6]`

## Qué tocar primero para tus trade studies
### 1) Radiador en cara zenith
- Bajá `alphaSolar[6]`
- Subí `epsIR[6]`
- Subí `G_frame_face[6]`
- Subí `G_cm5_face[6]`

### 2) Más aislamiento térmico de batería
- Bajá `G_batt_frame`
- Bajá `G_batt_face[:]`

### 3) Usar parte del calor del bus para templar batería
- Subí levemente `G_batt_frame`
- Subí levemente `G_batt_face[5]`
- No lo subas demasiado: vas a arrastrar transitorios del CM5 al pack

### 4) Probar distintas campañas solares
- Cambiá `beta_deg`
  - `0`: peor caso térmico cíclico / eclipse más severo
  - `15` a `30`: escenario más favorable

### 5) Probar distintos duty cycles del CM5
- `pulseCM5 = true`
- `cm5Duty = 0.1`, `0.2`, `0.4`
- `cm5Cycle = 300` o `600`

## Barrido manual sugerido
- Caso A: base
- Caso B: `G_cm5_face[6] = 0.6`, `G_frame_face[6] = 1.0`
- Caso C: Caso B + `G_batt_frame = 0.04`
- Caso D: Caso B + `G_batt_frame = 0.14`

Compará:
- pico y promedio de `T_cm5_C`
- mínimo de `T_batt_C`
- `P_panelNet`
- calor radiado por `Q_radToSpace[6]`

## Limitaciones
Esto no es un modelo de calificación térmica. Sirve para decidir layout conceptual, rutas de conducción y cara radiativa preferida. Para pasar a un modelo serio vas a necesitar:
- beta-angle real vs fecha
- actitud/ADCS real
- propiedades termo-ópticas medidas o trazables
- masas térmicas reales
- conductancias de contacto reales
- view factors geométricos mejores
