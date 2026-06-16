# Research memo — celdas solares low-cost para vuelo y arrays desplegables de referencia

**Proyecto:** DIY Nanosat  
**Fecha:** 2026-03-10  
**Estado:** documento de research / referencia histórica  
**Carácter:** **no implica decisión tomada**; resume hallazgos, comparaciones y criterios técnicos discutidos en la sesión.

---

## 1) Propósito del documento

Este documento consolida la investigación realizada en la sesión sobre:

- el antecedente **IRVINE01 1U** y su sistema desplegable EXA,
- la viabilidad de usar **mono-Si (monocrystalline silicon) low cost** en una ruta de vuelo,
- alternativas basadas en **SunPower / Maxeon IBC (Interdigitated Back Contact)**,
- comparación con la familia **AnySolar IXOLAR**,
- y el encaje geométrico-eléctrico preliminar dentro del baseline actual del proyecto.

La intención es **preservar contexto técnico** para futuras sesiones, evitando rediscutir desde cero lo ya analizado.

---

## 2) Baseline del proyecto relevante para esta investigación

Este research se interpretó contra el baseline vigente del proyecto, no contra un CubeSat genérico.

### 2.1 Parámetros de sistema que condicionan la decisión solar

- **Form factor actual:** **1.5U** (100 × 100 × 150 mm).
- **Topología de batería de vuelo:** **2S Li-ion**.
- **Objetivo de potencia neta disponible en sol:** **≥ 1.2 W**.
- **Recomendación de diseño para margen:** apuntar a **2–3 W BOL (Beginning Of Life)** efectivos en sol.
- **MPPT (Maximum Power Point Tracking):** recomendado para la arquitectura de vuelo.
- **Body-mounted vs deployables:** el baseline admite ambas rutas; deployables no están descartados.
- **Bench 1S con CN3065:** válido como banco funcional, **no** como arquitectura de vuelo.

### 2.2 Consecuencia práctica

La selección de celdas/paneles no puede evaluarse sólo por disponibilidad o costo unitario. Debe cerrar simultáneamente:

1. **geometría real 1.5U**,  
2. **bus 2S**,  
3. **margen de generación solar**,  
4. **complejidad de integración**,  
5. **riesgo de materiales y proceso para vuelo**.

---

## 3) Hallazgos sobre IRVINE01 y el sistema desplegable EXA

### 3.1 Qué quedó razonablemente establecido

La investigación sobre **IRVINE01** apuntó a que el satélite utilizó una variante de los arreglos desplegables **EXA DSA** y no una solución body-mounted simple.

Hallazgos principales:

- La documentación pública de EXA asocia explícitamente el hardware DSA con **IRVINE01**.
- El sistema DSA ofrecía dos caminos de celdas:
  - **low cost solar cells**,
  - **GaAs triple-junction AzurSpace 3G-30**.
- El mecanismo de despliegue se describe como una solución basada en:
  - **titanium scaffold**,
  - **shape-memory / artificial muscle actuation**,
  - estructura ultrafina compatible con restricciones P-POD / 1U.

### 3.2 Lo que **no** quedó cerrado con suficiente evidencia pública

No se obtuvo evidencia pública inequívoca que confirme si **IRVINE01** voló finalmente con:

- la variante **low cost mono-Si / low-cost space-grade**, o
- la variante **high power AzurSpace 3G-30**.

### 3.3 Qué aporta como referencia al proyecto

IRVINE01 es relevante como **caso de arquitectura**, no como confirmación de una celda exacta.

Lección útil:

- un **1U/1.5U** con necesidades energéticas no triviales puede requerir **deployables** incluso cuando se persigue una filosofía low-cost;
- el antecedente valida la idea de que **low-cost no equivale necesariamente a “sin despliegue”**.

---

## 4) Tesis principal de la sesión: “mono-Si low cost para vuelo”

### 4.1 Conclusión técnica general

La sesión llevó a una conclusión clara:

> **Sí existe una ruta técnicamente defendible para volar con mono-Si low cost, pero no pasa por usar paneles maker/hobby tal como vienen.**

### 4.2 Qué quedó descartado conceptualmente

No se considera serio, para vuelo, usar directamente:

- panelitos hobby encapsulados en **epoxy / PET / laminados de bajo costo** “as-is”,
- productos maker como si su encapsulado comercial ya fuera “flight-ready”,
- cualquier celda/panel sin screening, matching y control de proceso.

### 4.3 Ruta low-cost considerada más seria

La ruta más razonable discutida fue:

1. **comprar celdas mono-Si de buena eficiencia** como célula base,  
2. **no usar el producto comercial final tal cual**,  
3. diseñar un **panel custom propio**,  
4. controlar adhesivos, interconexión, venting y protección frontal,  
5. validar con ensayos y screening.

En esa lógica, la candidata conceptual que salió más fuerte fue la familia **SunPower / Maxeon IBC**.

---

## 5) SunPower / Maxeon E60 C60 como ruta low-cost de vuelo

### 5.1 Por qué aparecieron como candidatas fuertes

Se evaluaron positivamente por:

- alta eficiencia dentro de silicio mono-Si,
- arquitectura **IBC** sin fingers frontales tradicionales,
- posibilidad de conseguirse como **células sueltas** o pre-cortadas,
- mejor compatibilidad con un panel custom que un panel hobby encapsulado.

### 5.2 Punto crítico: tamaño

El principal problema detectado fue geométrico:

- una celda completa tipo **125 × 125 mm** no encaja limpiamente como unidad principal en caras de un **1.5U 100 × 100 × 150 mm**.

Eso llevó a la discusión sobre **celdas cortadas**.

### 5.3 ¿Se pueden cortar?

La respuesta técnica consolidada fue:

- **sí**, las celdas IBC pueden utilizarse en formatos **half-cut / 1/3 / 1/6**,
- **pero no** debe asumirse que eso equivale a “cortarlas a mano en taller sin proceso controlado”.

### 5.4 Conclusión práctica sobre corte

Se estableció como criterio prudente:

- **no** basar el camino de vuelo en comprar full-cells para luego improvisar corte manual;
- **sí** considerar celdas ya **pre-cut** o cortadas con proceso controlado;
- el corte en IBC es viable, pero introduce riesgo de **microgrietas**, pérdidas de borde y sensibilidad al trayecto exacto del corte.

### 5.5 Recomendación resultante

Si se siguiera esta ruta, lo lógico sería:

- comprar celdas **pre-cortadas** o con corte externo controlado,
- diseñar tiles / strings compatibles con el volumen real del 1.5U,
- evitar tratar la celda IBC como si fuera una lámina flexible “recortable libremente”.

---

## 6) AnySolar IXOLAR como familia alternativa

### 6.1 Por qué se consideró

La familia **AnySolar IXOLAR** apareció como opción interesante porque evita el problema del gran formato 125 mm.

Ventajas percibidas en la sesión:

- piezas ya pequeñas y modulares,
- buena tensión por pieza para su tamaño,
- más fáciles de distribuir en caras de 1.5U,
- eliminan la necesidad de cortar wafers grandes.

### 6.2 Reserva importante

La objeción principal fue de posicionamiento y pedigree:

- la línea IXOLAR está orientada por el fabricante a **energy harvesting / consumer / industrial portable**,
- no a una línea explícitamente **space-grade**.

Por lo tanto, quedó posicionada como:

- **interesante para route study**,  
- **posible flight-like experimental**,  
- pero **no equivalente** a una assembly espacial con coverglass y proceso calificado.

---

## 7) Comparativa geométrico-eléctrica preliminar para 1.5U

Se compararon tres modelos AnySolar:

- **SM141K10TF**
- **SM261K10TF**
- **SM351K09TF**

### 7.1 Datos base usados en la comparación

| Modelo | Dimensiones | Pmax | Vmp | Comentario |
|---|---:|---:|---:|---|
| SM141K10TF | 70 × 23 × 1.5 mm | 0.307 W | 5.58 V | Muy modular, mucha interconexión |
| SM261K10TF | 64 × 45 × 1.5 mm | 0.571 W | 5.58 V | Mejor equilibrio geométrico / eléctrico |
| SM351K09TF | 57 × 64 × 1.2 mm | 0.6946 W | 5.02 V | Más potencia por pieza, peor aprovechamiento en 1.5U |

### 7.2 Restricción de bus

Dado que la arquitectura de vuelo está bloqueada en **2S**, se concluyó que:

- **una sola pieza** de estas familias no es un string principal suficiente;
- la topología natural es **2 piezas en serie por string**.

Strings base discutidos:

| Modelo | String 2S (2 piezas en serie) | Potencia nominal por string |
|---|---:|---:|
| SM141K10TF | 11.16 Vmp | 0.614 W |
| SM261K10TF | 11.16 Vmp | 1.142 W |
| SM351K09TF | 10.04 Vmp | 1.389 W |

### 7.3 Cara lateral 100 × 150 mm (estimación ideal)

| Modelo | Unidades por cara | Potencia por cara | Observación |
|---|---:|---:|---|
| SM141K10TF | 8 | 2.456 W | Máxima potencia por cara, pero mayor complejidad de interconexión |
| SM261K10TF | 4 | 2.284 W | Muy cerca de SM141 con la mitad de piezas |
| SM351K09TF | 2 | 1.389 W | Peor aprovechamiento de área |

### 7.4 Cara 100 × 100 mm (estimación ideal)

**Nota:** en la sesión se discutió que la **SM141K10TF** puede llegar a **5 unidades** con layout mixto favorable; si se impone layout ortogonal uniforme, el conteo baja.

| Modelo | Unidades por cara | Potencia por cara | Observación |
|---|---:|---:|---|
| SM141K10TF | 5 teórico mixto | 1.535 W | Muy buena explotación geométrica, pero layout más exigente |
| SM261K10TF | 2 | 1.142 W | Limpio y simple |
| SM351K09TF | 1 | 0.695 W | Cara incómoda para strings 2S autónomos |

### 7.5 Lectura técnica consolidada

#### SM141K10TF

Fortaleza:

- mejor aprovechamiento del área y máximo margen energético por cara.

Debilidad:

- dispara la cantidad de interconexiones y puntos de falla.

#### SM261K10TF

Fortaleza:

- mejor compromiso entre potencia, geometría, manufactura e integración.

Debilidad:

- pierde frente a SM141 si el problema dominante pasa a ser exprimir cada mm².

#### SM351K09TF

Fortaleza:

- mayor potencia por string individual.

Debilidad:

- peor encaje geométrico en tapas y caras pequeñas del 1.5U.

### 7.6 Resultado de la comparación

La conclusión más equilibrada de la sesión fue:

> **SM261K10TF** quedó como la mejor referencia preliminar de compromiso.  
> **SM141K10TF** quedó como opción para un escenario donde el margen energético por cara pese más que la complejidad de integración.  
> **SM351K09TF** no quedó bien posicionada como baseline principal.

---

## 8) ¿Existe una serie “parecida a SM261K10TF” pero más adecuada para vuelo?

### 8.1 Respuesta corta

Sí, pero la respuesta depende de qué se entienda por “más adecuada para vuelo”.

### 8.2 Alternativa inmediata dentro de AnySolar

Se identificó como variante cercana:

- **SM261K10L**

Interpretación de la sesión:

- misma lógica geométrica-eléctrica que la **SM261K10TF**,
- diferente acabado / rigidez,
- mejora de integración mecánica potencial,
- **pero no cambia la categoría del producto**: sigue sin equivaler a una solución espacial calificada.

### 8.3 Conclusión sobre la familia IXOLAR

Optimizar entre **TF vs L** dentro de IXOLAR se evaluó como **discusión secundaria**.

La discusión principal real es:

- **módulo IXOLAR con polímeros y lógica de harvesting terrestre**, versus
- **celda/assembly espacial con coverglass, adhesivos y proceso orientado a espacio**.

### 8.4 Alternativas conceptualmente más aptas para vuelo

Se destacaron como referencias más alineadas con vuelo real:

- **Sharp Silicon Space Solar Cells** (ruta espacial en silicio, con sizes customizables y coverglass configurable).
- **AZUR SPACE / Spectrolab / otras CIC-SCA** (Cell-Interconnect-Coverglass / Solar Cell Assembly), aunque ya salen del enfoque low-cost estricto.

### 8.5 Lectura resultante

Si el objetivo es **seguir en silicio** pero mejorar la seriedad de la ruta de vuelo, la discusión importante pasa a ser:

- seguir explorando **AnySolar como opción experimental**, o
- estudiar una migración futura a **silicio espacial con coverglass**.

---

## 9) Proveedores y abastecimiento local discutidos

### 9.1 Hallazgo principal

En Argentina se detectó disponibilidad local visible de:

- **panelitos mono-Si maker / robótica**,
- publicaciones de **Mercado Libre** con celdas tipo **SunPower E60/C60**,
- pero **no** un canal local fuerte y claramente trazable de célula espacial mono-Si.

### 9.2 Interpretación

Los proveedores locales sirven para:

- prototipos,
- screening destructivo,
- aprendizaje de proceso,
- y compras rápidas.

Pero no cierran por sí solos el problema de una supply chain “flight-ready”.

### 9.3 Criterio consolidado

Para una ruta de vuelo low-cost, la estrategia implícita que surgió fue:

- **abastecimiento local** para prototipos y exploración inicial,
- **importación / compra internacional** para materiales críticos, celdas o assemblies más serias.

---

## 10) Qué quedó razonablemente firme al terminar la sesión

### 10.1 Puntos de consenso técnico

1. **Mono-Si low cost para vuelo no está descartado**.  
2. La vía sensata **no** es volar paneles hobby tal cual vienen.  
3. **SunPower / Maxeon IBC** sigue siendo una ruta técnicamente fuerte, pero depende de corte controlado o celdas pre-cortadas.  
4. **AnySolar IXOLAR** es atractiva geométrica y eléctricamente, especialmente **SM261K10TF**, pero permanece en una zona más experimental para vuelo.  
5. Si el proyecto necesita mayor robustez material / espacial, hay que mirar eventualmente **silicio espacial con coverglass** o assemblies tipo **CIC/SCA**.  
6. El antecedente **IRVINE01 / EXA** valida que el despliegue puede ser parte natural de una arquitectura low-cost cuando el power budget lo exige.

### 10.2 Lo que deliberadamente **no** quedó decidido

- No se eligió una familia de celda final.  
- No se eligió un proveedor final.  
- No se definió aún si la arquitectura solar de vuelo será:
  - sólo **body-mounted**,
  - **body-mounted + deployables**,
  - o una ruta híbrida por fases.

---

## 11) Riesgos identificados durante la investigación

### 11.1 Riesgo de autoengaño por “low cost marketing”

Confundir:

- “monocristalino”,
- “ETFE”,
- “high efficiency”,
- “flexible”,

con una arquitectura apta para LEO.

### 11.2 Riesgo de geometría optimista

Elegir celdas por potencia unitaria sin cerrar:

- rail keepouts,
- routing,
- conectores,
- antenas,
- thermal / structure,
- sombras parciales.

### 11.3 Riesgo de proceso

Incluso con buena celda, una mala integración puede arruinar el resultado:

- microgrietas,
- voids,
- delaminación,
- adhesivo inadecuado,
- contaminación por materiales no aptos.

### 11.4 Riesgo de subestimar el bus 2S

Varias soluciones compactas parecen atractivas por tamaño, pero su tensión por pieza obliga a:

- strings en serie,
- más routing,
- más bypass / protección,
- más complejidad del MPPT.

---

## 12) Próximos temas naturales que quedaron abiertos

Este research dejó planteadas como líneas futuras de trabajo:

1. **layout real cara por cara** del 1.5U con keepouts verdaderos,  
2. cálculo más realista de **sombras, packing factor y pérdidas**,  
3. análisis de **body-mounted puro vs deployable simple**,  
4. screening y supply chain de **SunPower/Maxeon pre-cut**,  
5. análisis más profundo de **Sharp Silicon Space Solar Cells**,  
6. definición del **proceso de panel custom** (adhesivos, cover, venting, interconexión),  
7. eventual tabla costo-riesgo entre:
   - AnySolar,
   - SunPower/Maxeon,
   - silicon space cells,
   - CIC/SCA.

---

## 13) Conclusión ejecutiva

La sesión no cerró una decisión, pero sí ordenó el espacio de soluciones.

### 13.1 Imagen general resultante

- **IRVINE01 / EXA** quedó como antecedente útil para justificar deployables low-cost.  
- **SunPower / Maxeon IBC** quedó como la ruta low-cost de vuelo más prometedora dentro de silicio, siempre que se controle el tema del corte y del proceso.  
- **AnySolar IXOLAR**, especialmente **SM261K10TF**, quedó como la mejor familia comercial modular evaluada en esta sesión para encajar geométrica y eléctricamente en 1.5U.  
- **SM141K10TF** quedó como opción de mayor margen energético por cara, a costa de integración más compleja.  
- Si más adelante el proyecto prioriza robustez espacial sobre costo, la discusión debe migrar hacia **silicon space cells** o **CIC/SCA** con coverglass.

### 13.2 Mensaje final útil para continuidad

La investigación dejó una idea central que conviene preservar:

> **El problema ya no es “si usar mono-Si low cost o no”, sino cuál es la ruta de integración más defendible para convertirlo en hardware volable sin engañarse con soluciones maker.**

---

## 14) Fuentes y referencias usadas / citadas en la sesión

### 14.1 Documentación del proyecto

- `CONSOLIDADO.md`
- `CDS REV14.1` (CubeSat Design Specification)
- `CubeSat 101` (NASA CubeSat Launch Initiative)
- Halliwell abstract — low-cost open-source customizable CubeSat solar panels (referencia externa; no vendorear PDF en el árbol público)
- LACW-24-07-04 — low-cost solar simulator for CubeSats (referencia externa; no vendorear PDF en el árbol público)

### 14.2 Referencias externas relevantes discutidas

#### IRVINE01 / EXA
- EXA DSA 1A drawing
- EXA DSA brochure / product option forms
- paper sobre deployable multi-panel solar array for low-cost 1U CubeSat missions

#### Corte y uso de IBC
- trabajo de TU Delft sobre **cut losses** en IBC solar cells
- documentación pública Maxeon / SunPower sobre uso de solar cells y strings

#### AnySolar / IXOLAR
- página **Gen3** de AnySolar
- fichas DigiKey para:
  - SM141K10TF
  - SM261K10TF
  - SM351K09TF
  - SM641K10TF

#### Alternativas más orientadas a vuelo
- Sharp Silicon Space Solar Cells
- AZUR SPACE CIC / assemblies
- Spectrolab CIC / assemblies

#### Mercado / suministro local explorado
- Candy-HO
- Tienda Virtual
- Mercado Libre Argentina (SunPower E60/C60 y paneles maker)

---

## 15) Nota de uso dentro del repo

Este documento debe leerse como:

- **research memo**,  
- **documento base de discusión**,  
- **registro de exploración técnica**,  
- **sin carácter de ADR (Architecture Decision Record)**.

Si en el futuro se toma una decisión de arquitectura solar, convendría derivar desde este memo:

1. una **ADR**,  
2. un documento de **trade study comparativo**,  
3. y un documento de **procurement / test plan**.
