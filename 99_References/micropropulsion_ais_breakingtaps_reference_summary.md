# Micropropulsión para DIY-Nanosat, síntesis de fuentes AIS + Breaking Taps

**Revisión:** 2026-04-06
**Estado:** Preliminary
**Trazabilidad:** fuentes externas de referencia, no normativo

## Objetivo

Resumir lo expuesto por:
- el video de Breaking Taps sobre un thruster de emisión de campo con metal líquido (galio), y
- la web de Applied Ion Systems (AIS), con foco en la familia AIS-VAT1,

para habilitar un trade study posterior sobre la posible implementación de micropropulsión en la misión DIY-Nanosat 1.5U.

## Resumen ejecutivo

- Las fuentes cubren dos ramas distintas de micropropulsión eléctrica:
  1. **Field Emission / Liquid Metal Ion Thruster, tipo FEEP/LMFEE** (video), con **Isp muy alto** y **thrust extremadamente bajo**.
  2. **Micro Vacuum Arc Thruster (VAT)** de AIS, con **Isp menor**, pero arquitectura mucho más simple, combustible sólido metálico, integración más directa y costo mucho más bajo.
- Para una misión **1.5U**, la familia **AIS-VAT1** parece más realista como **COTS/OTS para tech demo, trim fino o compensación pequeña**, que como sistema principal de cambio orbital relevante.
- El video de Breaking Taps es muy valioso para entender **principio físico, limitaciones reales y failure modes** de una micropropulsión iónica de muy alto Isp, pero **no describe un producto de vuelo integrado**.
- En AIS hay una evolución visible de soluciones de micropropulsión: **gPPT orbital heredado, VAT como línea comercial activa, y trabajo paralelo en ILIS y micro End-Hall**. Eso sugiere que el “estado del arte” a esta escala sigue siendo muy dependiente del compromiso entre **Isp, impulso total, simplicidad, potencia y madurez de integración**.
- Hay **inconsistencias públicas** entre páginas de portfolio y página de productos de AIS en **precio** y **lead time**. Antes de cualquier decisión hay que validar con el proveedor el SKU realmente vigente.

## 1. Qué explican las fuentes

### 1.1 Video Breaking Taps: thruster de emisión de campo con galio

El video describe un microthruster que acelera iones de galio usando un campo eléctrico de alrededor de **10 kV**, reportando velocidades iónicas del orden de **0.056% de la velocidad de la luz**. El principio es el típico de la familia **FEEP / liquid metal field emission**: un metal líquido en la punta del emisor forma una estructura tipo menisco/Taylor cone y, cuando el campo es suficiente, emite y acelera iones.

Puntos clave del video:
- La propulsión eléctrica cambia masa de reacción por **eficiencia**: mucho **Isp**, poco thrust, tiempos de maniobra largos.
- El autor distingue familias de emisores capilares, incluyendo **emisor poroso**, **slot anular** y variantes tipo **spike/array**.
- La fabricación del emisor y la estabilidad del sistema son críticas. El video muestra problemas reales de:
  - humectación y cebado del emisor,
  - alineación electrodo-emisor,
  - breakdown/arcing,
  - corriente de fuga,
  - resistencias limitadoras y estabilidad de extracción,
  - repetibilidad de manufactura.
- Se menciona colaboración con **Applied Ion Systems** para maquinar emisores porosos.
- El resultado de banco reportado en el cierre es del orden de **11–15 µN de thrust** con **Isp calculado ~3100 s**.

Lectura técnica útil para el repo:
- Esta rama de micropropulsión es muy atractiva cuando el objetivo es **máxima eficiencia propulsiva** y control ultrafino.
- A cambio, el sistema se vuelve muy sensible a **materiales, HV, contaminación, manufactura del emisor y control de estabilidad**.
- La fuente sirve como **referencia conceptual y de riesgos de implementación**, no como datasheet de un producto listo para vuelo.

### 1.2 Applied Ion Systems: familia AIS-VAT

AIS presenta la familia **VAT** como una solución de micropropulsión eléctrica de bajo costo para **PocketQubes y CubeSats**. El principio no es field emission, sino **vacuum arc thruster**: pulsos de descarga en vacío sobre combustible metálico sólido.

La propuesta de AIS, tal como aparece en la web, enfatiza:
- **electrónica simple**,
- integración con **5V + GND + pulsos lógicos**,
- poco volumen,
- bajo costo relativo,
- disparo confiable,
- utilidad tanto para **banco/pruebas** como para **uso orbital**.

AIS argumenta además que, a esta escala, conviene optimizar por **thrust efficiency** y facilidad de ignición antes que por Isp máximo, por eso la línea VAT1 está basada en **bismuto** y no en titanio.

#### VAT1-PQ
- Formato mínimo orientado a **1.5P PocketQube hasta 1U CubeSat**.
- Publicado con:
  - **2.5 W o 5 W**
  - **26 µN BOL** (página de productos)
  - **0.13 Ns** de impulso total
  - **87 s** de Isp
  - **42 x 42 x 21 mm**
  - **56 g**

#### VAT1-DUO
- Dos módulos VAT1 en paralelo.
- Publicado con:
  - **5 W o 10 W**
  - **52 µN BOL**
  - **0.26 Ns**
  - **87 s** de Isp
  - **84 x 42 x 21 mm**
  - **84 g**

#### VAT1-QUAD
- Cuatro módulos VAT1 en paralelo.
- Publicado con:
  - **10 W o 20 W**
  - **104 µN BOL**
  - **0.52 Ns**
  - **87 s** de Isp
  - **84 x 84 x 21 mm**
  - **177 g**

## 2. Estado del arte, leído desde estas fuentes

Las fuentes muestran bien que, a escala nano/picosat, no existe una única “mejor” micropropulsión. Hay familias con compromisos muy distintos:

### 2.1 Field emission / liquid metal ion thrusters
**Fortalezas**
- Isp muy alto.
- Excelente para control fino y delta-v acumulado cuando el tiempo no es crítico.
- Conceptualmente muy atractivo para misiones con fuerte restricción de masa de propelente.

**Debilidades**
- Integración compleja: HV, emisor, estabilidad, contaminación, manufactura.
- Más difícil de llevar desde demostrador de laboratorio a hardware de vuelo robusto.
- La fuente revisada no aporta todavía cierre de lifetime, neutralización, ICD ni calificación ambiental.

### 2.2 Vacuum arc thrusters (AIS VAT)
**Fortalezas**
- Arquitectura mucho más simple.
- Combustible sólido metálico, sin tanque ni regulación de presión.
- Interfaz eléctrica sencilla.
- Buen encaje como plataforma de entrada, bajo costo y bajo volumen.

**Debilidades**
- Isp claramente menor que en field emission.
- Impulso total publicado todavía modesto para una misión 1.5U que necesite delta-v significativo.
- La web pública no alcanza para cerrar riesgos de plume, compatibilidad ambiental, EMI/EMC ni calificación.

### 2.3 Otras líneas de AIS que ayudan a leer madurez y dirección tecnológica
La propia web de AIS sugiere una evolución del portfolio:
- **AIS-gPPT3-1C**: línea anterior de pulsed plasma thruster, con herencia orbital, luego **retirada** a favor de VAT.
- **ILIS1-BQ**: reportes públicos sobre una familia de **liquid ion source**, más cercana conceptualmente al video.
- **AIS-EHT1**: micro **End-Hall thruster** en reportes/IEPC.
- **SWAG**: warm gas de muy baja escala, no eléctrico, pero sí alternativa de micropropulsión para nanosats.

Conclusión de estado del arte a partir de estas fuentes: a esta escala, el trade dominante sigue siendo:
- **Isp máximo** vs **simplicidad y madurez de integración**,
- **impulso total útil** vs **potencia/volumen**,
- **demostrador interesante** vs **producto COTS utilizable**.

## 3. Relevancia para DIY-Nanosat 1.5U

### 3.1 Lectura rápida de encaje

Si el objetivo de misión fuera:
- **tech demo de propulsión**,
- **trim fino**,
- **micro-correcciones pequeñas**,
- **payload demostrador de EP**,

la familia **VAT1** sí merece trade study.

Si el objetivo fuera:
- **cambio orbital significativo**,
- **deorbit authority** no trivial,
- **maniobras de varios m/s**,

los VAT1 publicados parecen **insuficientes como solución principal** y habría que abrir trade con opciones de mayor impulso total, incluyendo warm-gas u otras familias EP más maduras.

### 3.2 Screening por impulso total publicado

Usando la aproximación ideal **ΔV ≈ I_total / m_sat**:

- **VAT1-PQ, 0.13 Ns**
  - a 2 kg: **0.065 m/s**
  - a 3 kg: **0.043 m/s**
- **VAT1-DUO, 0.26 Ns**
  - a 2 kg: **0.13 m/s**
  - a 3 kg: **0.087 m/s**
- **VAT1-QUAD, 0.52 Ns**
  - a 2 kg: **0.26 m/s**
  - a 3 kg: **0.173 m/s**

Esto refuerza una lectura importante: **la familia VAT1, tal como está publicada, parece más adecuada para demostración/trim fino que para propulsión primaria de una 1.5U**.

Como contraste, la familia **SWAG** publicada en la misma web sí entra en territorio de varios m/s ideales para masas tipo nanosat, pero con penalización importante en masa, volumen, preheat y simplicidad del sistema.

## 4. Riesgos y preguntas que hay que cerrar antes de considerar implementación

1. **Necesidad real de misión**
   - ¿Se busca demo tecnológica o delta-v operativo real?
2. **Presupuesto de potencia**
   - ¿El EPS puede sostener 5/10/20 W con márgenes, más picos y térmica asociada?
3. **Presupuesto geométrico**
   - ¿Hay cara libre, línea de pluma aceptable y brazo de momento tolerable?
4. **Contaminación/plume interactions**
   - Paneles solares, sensores, ópticas, antenas, superficies térmicas.
5. **Camino regulatorio e integrador**
   - No todos los integradores aceptan igual cualquier sistema de propulsión.
6. **Madurez documental del proveedor**
   - ICD, vib/shock, TVAC, EMC/EMI, lifetime, FDIR, handling, export.
7. **Consistencia comercial**
   - La web pública tiene discrepancias de precio/lead time entre páginas.

## 5. Recomendación preliminar para el trade study

- **Candidato más razonable para estudiar primero:** **AIS-VAT1-DUO**.
  - Motivo: punto medio entre volumen, potencia y utilidad frente a PQ y QUAD.
- **AIS-VAT1-PQ** es atractivo por tamaño y costo, pero probablemente demasiado justo en impulso total para algo más que demo.
- **AIS-VAT1-QUAD** mejora thrust/impulso dentro de la misma familia, pero ya presiona más fuerte en volumen y potencia.
- **El thruster del video** conviene tratarlo como **referencia conceptual/futura línea R&D**, no como candidato near-term de implementación en misión.

## 6. Tabla de dispositivos y precios publicados en la web de referencia

> **Nota importante:** los precios abajo son **precios publicados** en la web consultada el 2026-04-06. **No equivalen a cotización vigente.** En varios productos hay diferencias entre la página de portfolio y la página general de productos.

| Dispositivo | Tipo | Potencia | Datos publicados clave | Precio publicado | Estado | Observación |
|---|---|---:|---|---:|---|---|
| AIS-VAT0-DEMO | DIY Micro Vacuum Arc Thruster Learning Kit | 2.5 W | >300,000 shots @ 50 mTorr; 60,000 shots @ 10^-6 Torr; 50x50x21 mm | **USD 900 domestic / 1050 international** (Products) | Available | Página portfolio más vieja publica **USD 570 / 720 shipped** |
| AIS-VAT1-PQ | Micro Vacuum Arc Thruster | 2.5 / 5 W | 26 µN BOL; 0.13 Ns; 87 s; 42x42x21 mm; 56 g | **USD 3500** (Products) | Available | Página portfolio publica **USD 2500** |
| AIS-VAT1-DUO | Dual Micro Vacuum Arc Cluster | 5 / 10 W | 52 µN BOL; 0.26 Ns; 87 s; 84x42x21 mm; 84 g | **USD 5500** (Products) | Available | Página portfolio publica **USD 4800** |
| AIS-VAT1-QUAD | Quad Micro Vacuum Arc Cluster | 10 / 20 W | 104 µN BOL; 0.52 Ns; 87 s; 84x84x21 mm; 177 g | **USD 8000** (Products) | Available | Página portfolio publica **USD 6500** |
| AIS-gPPT3-1C Integrated Module | Gridded Pulsed Plasma Thruster module | ~0.5 W promedio | Heritage orbital; 5V input; línea retirada a favor de VAT | **USD 2500** (portfolio histórico) | Retired | Útil como referencia de madurez/historia tecnológica |
| AIS-SWAG1-PQ | Sublimation Warm Gas Thruster | 5 W | 120 µN; 3 Ns; 20 s; 42x42x54 mm; 214 g | **USD 6500** | Available | No es EP, pero sí opción de micropropulsión publicada por AIS |
| AIS-SWAG1-DUO | Sublimation Warm Gas Thruster | 10 W | 240 µN; 6 Ns; 20 s; 86x42x54 mm; 430 g | **USD 9500** | Available | Más impulso total, más masa/volumen |
| AIS-SWAG1-QUAD | Sublimation Warm Gas Thruster | 20 W | 480 µN; 12 Ns; 20 s; 86x86x54 mm; 860 g | **USD 12,500** | Available | Alternativa si el problema real es delta-v y no pureza EP |
| AIS-SWAG2-X4 | Sublimation Warm Gas Thruster | TBD | 588 µN; impulso total TBD; 92x92x67 mm | **USD 14,500** | In development | Publicado como en desarrollo |

## 7. Referencias

### Fuentes principales consultadas
- Breaking Taps, **“Accelerating Gallium Ions to 0.056% light speed”**  
  https://www.youtube.com/watch?v=dfYSBlV90NQ
- Applied Ion Systems, **Home**  
  https://appliedionsystems.com/
- Applied Ion Systems, **Products**  
  https://appliedionsystems.com/products/
- Applied Ion Systems, **AIS-VAT1-PQ Micro Vacuum Arc Thruster**  
  https://appliedionsystems.com/portfolio/ais-vat1-pq-micro-vacuum-arc-thruster/
- Applied Ion Systems, **AIS-VAT1-DUO Dual Micro Vacuum Arc Thruster**  
  https://appliedionsystems.com/portfolio/ais-vat1-duo-dual-micro-vacuum-arc-thruster/
- Applied Ion Systems, **AIS-VAT1-QUAD Quad Micro Vacuum Arc Thruster**  
  https://appliedionsystems.com/portfolio/ais-vat1-quad-quad-micro-vacuum-arc-thruster/
- Applied Ion Systems, **AIS-VAT0-DEMO Educational DIY Micro Vacuum Arc Thruster Kit**  
  https://appliedionsystems.com/portfolio/ais-vat0-demo-educational-diy-micro-vacuum-arc-thruster-kit/
- Applied Ion Systems, **AIS-gPPT3-1C Series Integrated Propulsion Module**  
  https://appliedionsystems.com/portfolio/ais-gppt3-1c-series-integrated-propulsion-module/

### Fuentes adicionales mencionadas o enlazadas desde las anteriores
- Applied Ion Systems, **AIS-VAT1-PQ Qualification Videos**  
  https://www.youtube.com/playlist?list=PLci4UwOQX29PJfOHKdAMuXuYSI5L_jqLl
- Applied Ion Systems, **AIS-VAT1-DUO Qualification Videos**  
  https://www.youtube.com/playlist?list=PLci4UwOQX29OnyXsgOj4TKGgy0U95ZYX9
- Applied Ion Systems, **AIS-VAT1-QUAD Qualification Videos**  
  https://www.youtube.com/playlist?list=PLci4UwOQX29ODAbXjtB4ojp84GYg8v1HM
- Applied Ion Systems, **Reports**  
  https://appliedionsystems.com/reports/
- Applied Ion Systems, **Preliminary Operational Results of the AIS-EHT1 Micro End-Hall Thruster (IEPC-2022-349)**  
  https://appliedionsystems.com/wp-content/uploads/2022/10/IEPC-2022-349-Preliminary-Operational-Results-of-the-AIS-EHT1-Micro-End-Hall-Thruster.pdf
- Applied Ion Systems, **Final Design of the AIS-ILIS1-BQ Series Liquid Ion Source Module**  
  https://appliedionsystems.com/wp-content/uploads/2022/10/AIS-TR-010-Final-Design-of-the-AIS-ILIS1-BQ-Series-Liquid-Ion-Source-Module.pdf
- Applied Ion Systems, **Preliminary Testing of the AIS-ILIS1-BQ Series Liquid Ion Source Module**  
  https://appliedionsystems.com/wp-content/uploads/2022/10/AIS-TR-011-Preliminary-Testing-of-the-AIS-ILIS1-BQ-Series-Liquid-Ion-Source-Module.pdf
- Applied Ion Systems, **Initial Fueling Procedure and Results for the AIS-ILIS1-BQ Series Liquid Ion Source Module**  
  https://appliedionsystems.com/wp-content/uploads/2022/10/AIS-TR-014-Initial-Fueling-Procedure-and-Results-for-the-AIS-ILIS1-BQ-Series-Liquid-Ion-Source-Module.pdf
- Applied Ion Systems, **Initial Vacuum Ignition Tests of the AIS-ILIS1-BQ Series Liquid Ion Source Module**  
  https://appliedionsystems.com/wp-content/uploads/2022/10/AIS-TR-015-Initial-Vacuum-Ignition-Tests-of-the-AIS-ILIS1-BQ-Series-Liquid-Ion-Source-Module.pdf

## 8. Nota final de uso

Este documento debe tratarse como **insumo de referencia para un trade study**, no como cierre de selección. Si se decide avanzar, el siguiente paso correcto es abrir una evaluación formal con:
- necesidad de misión,
- presupuesto de potencia/masa/volumen,
- riesgos de integración,
- contacto directo con proveedor para ICD y datos de calificación.
