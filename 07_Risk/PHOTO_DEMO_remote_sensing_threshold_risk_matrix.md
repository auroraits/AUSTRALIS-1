# PHOTO_DEMO — Análisis jurídico‑técnico de umbral regulatorio (amateur vs “remote sensing satellite”)

**Destino en repo:** `07_RISKS/PHOTO_DEMO_remote_sensing_threshold_risk_matrix.md`  
**Fecha de análisis:** 2026-03-05  
**Estado:** v2 (repo‑ready) — para decisión de arquitectura/compliance  
**Ámbito geográfico primario:** Argentina (estación terrena/operación), con referencias a marcos internacionales relevantes (UIT/ONU).  
**Disclaimer:** esto **no** es asesoramiento legal; es un análisis técnico‑jurídico de riesgo para ingeniería de misión.

---

## 0) Contexto del proyecto y constraints ya vigentes

En el baseline del proyecto, `PHOTO_DEMO` es **opcional/no bloqueante** y está encapsulado con los requisitos:

- **MIS-REQ-PH-01**: inicia **OFF** por defecto al boot.
- **MIS-REQ-PH-02**: usa cuota **best‑effort** por pasada sin desplazar housekeeping/comandos.
- **MIS-REQ-PH-03**: downlink por **chunks reanudables** tras selección por uplink.

> Implicación: incluso si `PHOTO_DEMO` existiera físicamente, la arquitectura **ya** exige control operacional estricto y capacidad de “hard-disable” sin degradar TTC/housekeeping.

---

## 1) Pregunta a responder (“umbral”)

**Objetivo:** Identificar **qué características de cámara + operación** aumentan el riesgo de que el satélite sea tratado como un sistema de **observación/teledetección** (“remote sensing”) — con consecuencias típicas: mayores obligaciones regulatorias, revisión por autoridades/partners, y/o exigencias de licenciamiento/coord. adicionales.

**Resultado buscado:** “Guardrails” de diseño + matriz de riesgo que te diga:  
- qué features disparan el riesgo,
- cómo mitigarlo,
- cuándo **parar** y elevar a revisión legal/partner de lanzamiento.

---

## 2) Marco regulatorio relevante (lo que sí es sólido y “hard constraints”)

### 2.1 Telecomunicaciones (Argentina) — servicio de radioaficionados por satélite
Si el downlink está en bandas del **Servicio de Aficionados por Satélite**, aplica el **Reglamento General de Radioaficionados** de ENACOM (Res. 3635/2017) y el encuadre operativo asociado; ENACOM además tiene trámite específico para **Estaciones Espaciales y Terrenas** bajo el régimen de radioaficionados.

Referencias:
- ENACOM Res. 3635/2017 (PDF): https://www.enacom.gob.ar/multimedia/normativas/2017/res3635%20%28octubre%29.pdf
- Trámite ENACOM “Radioaficionados — Estaciones Espaciales y Terrenas”: https://www.enacom.gob.ar/tramites/radioaficionados-estaciones-espaciales-y-terrenas_t137

**Nota clave:** “amateur‑sat” NO significa “sin permisos”. Significa: un camino viable si cumplís reglas del servicio (incl. no uso comercial, identificación, coordinación, etc.).

### 2.2 Gestión/servicios satelitales (Argentina) — reglamento general (SFS/SMS/SRS)
La Resolución 58/2025 (texto ordenado) regula **provisión de facilidades** y **prestación de servicios satelitales** para satélites GEO/no‑GEO en bandas de Servicio Fijo por Satélite (SFS), Servicio Móvil por Satélite (SMS) y Radiodifusión por Satélite (SRS), alineado con UIT y el CABFRA.

Referencia:
- Resolución 58/2025 (texto): https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-58-2025-411419/texto

**Lectura práctica:** aunque un CubeSat amateur típicamente no “vende” capacidad satelital, si el proyecto empieza a parecer un **servicio** (p.ej. distribución sistemática de imágenes con clientes/SLAs), el riesgo de entrar en este paraguas sube.

### 2.3 Registro de objetos lanzados al espacio (Argentina/ONU)
Argentina aprobó el Convenio de Registro (Ley 24.158) y tiene un **Registro Nacional de Objetos Lanzados al Espacio Ultraterrestre** (p.ej. Resolución 260/1999 aprueba el reglamento orgánico y formularios). Esto aparece reiterado en normativa y práctica estatal.

Referencias:
- Ley 24.158: https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/556/norma.htm
- Resolución 260/1999: https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-260-1999-57753
- CONAE “Registro de satélites”: https://www.argentina.gob.ar/ciencia/conae/institucional/registro-de-satelites

**Implicación:** independientemente de `PHOTO_DEMO`, el satélite es un **objeto espacial** y el “lado Estado” (registro/UIT/ONU) existe; tu payload no te exime ni te agrava automáticamente, pero puede aumentar escrutinio.

### 2.4 Definiciones UIT (internacional) — Earth Exploration‑Satellite Service (EESS)
En el ecosistema regulatorio global, lo que se etiqueta como “remote sensing” suele mapear a **EESS (Earth exploration‑satellite service)** y definiciones relacionadas (sensores activos/pasivos, etc.).

Referencias:
- ITU Radio Regulations — Art. 1 (Terms/Definitions), PDF: https://life.itu.int/radioclub/rr/art1.pdf
- ITU‑R Handbook EESS (PDF): https://www.itu.int/dms_pub/itu-r/opb/hdb/R-HDB-56-2011-PDF-E.pdf

**Traducción ingenieril:** si tu sistema se comporta como “medición/observación sistemática de la Tierra” (aunque sea óptica), te aproximás a EESS. Que sea “educativo y abierto” ayuda a intención/uso, pero **no borra** capacidades.

---

## 3) Heurística “realista” de umbral (no hay un único número, sí hay un patrón)

En la práctica (lanzadores, coordinadores de frecuencias, y compliance), la clasificación se decide por una combinación de:

1) **Capacidad de adquisición útil** (resolución/contraste/SNR + óptica)  
2) **Capacidad de apuntado/estabilización** (ADCS: Attitude Determination and Control System) para “targeting”  
3) **Geolocalización y metadata** (time‑tag, geo‑tag, attitude solution)  
4) **Volumen y sistematicidad** (frecuencia de captura, swath, cobertura)  
5) **Tasking / acceso de terceros** (API, pedidos, “ventas”, SLAs)  
6) **Tratamiento y publicación** (difusión que habilita usos sensibles)

> Conclusión: **la cámara sola no te mete** en “remote sensing”; te mete el **sistema** (cámara + ADCS + ops + data product).

---

## 4) Guardrails de diseño para mantener `PHOTO_DEMO` “claramente demo/educativo”

Estos son límites que reducen significativamente el riesgo de que el payload sea interpretado como EO/remote sensing “de facto”.

### 4.1 Óptica / resolución / geometría (hardware)
**PH-GUARD-01 — Wide‑angle “context camera”**
- FOV muy amplio (ideal: >120°) y **sin telefoto**.
- Enfoque fijo (sin autofocus), sin zoom óptico.

**PH-GUARD-02 — GSD deliberadamente baja**
- Diseñar para que el **GSD (Ground Sample Distance)** sea “malo a propósito”.  
  Heurística de seguridad: *GSD objetivo ≥ 500 m/pixel* (mejor aún: ≥ 1–5 km/pixel).  
  Esto te aleja de usos de vigilancia/infraestructura.  
  *Nota:* el umbral exacto no está “en una ley” argentina pública; se usa como control técnico interno.

**PH-GUARD-03 — Sin filtros espectrales útiles**
- Evitar multiespectral/NIR (Near‑Infrared), filtros intercambiables, y calibración radiométrica seria.

### 4.2 ADCS / operación (software + misión)
**PH-GUARD-04 — No targetable**
- Sin modos de “pointing to ground target”.
- Captura solo en ventanas restringidas y con actitud “no optimizada” (p.ej. nadir casual o cualquiera, pero no con pipeline de targeting).

**PH-GUARD-05 — Sin geo‑tag de alta calidad**
- No empaquetar lat/lon “preciso” por pixel.
- Si hay timestamp, dejarlo a nivel coarse (p.ej. minuto), o sin metadata de actitud.

**PH-GUARD-06 — Rate‑limit fuerte**
- Límite duro de capturas por día/pasada (p.ej. 1 frame por pasada, 1–3 por día).
- Downlink capado por cuota (ya alineado con MIS‑REQ‑PH‑02).

**PH-GUARD-07 — No terceros / no servicio**
- No “tasking” por usuarios externos.
- Si se publica: publicar como **demo** (educativo/científico), sin promesa de cobertura ni disponibilidad.

### 4.3 Publicación y privacidad (tierra)
**PH-GUARD-08 — Política de publicación conservadora**
- Publicación **best‑effort** y con retraso (time delay) para evitar “near‑real‑time”.
- Evitar publicar material que pueda identificar personas/vehículos o instalaciones sensibles.  
  (Aunque con GSD alto esto se vuelve improbable, el guardrail se mantiene.)

---

## 5) “Criterios de disparo” (trigger) para escalar a revisión legal/partner

Si cualquiera de estos se cumple, **se considera que `PHOTO_DEMO` dejó de ser una demo inocua** y debe elevarse a revisión:

- **TRG‑01 (Resolución alta):** diseño o medición en órbita sugiere GSD < 250 m/pixel.
- **TRG‑02 (Targeting):** existe modo de apuntado a targets (lista de coordenadas / schedule).
- **TRG‑03 (Geo‑products):** se generan ortomosaicos, mapas, georreferenciación robusta o “productos EO”.
- **TRG‑04 (Cadencia):** >10 imágenes/día sostenidas o “campañas” sistemáticas.
- **TRG‑05 (Acceso de terceros):** API/cola de pedidos de imagen por usuarios o clientes.
- **TRG‑06 (Comercialización):** monetización directa/indirecta de imágenes o del servicio.
- **TRG‑07 (Near‑real‑time):** publicación o entrega con latencia < 24 h como comportamiento normal.

---

## 6) Matriz de riesgo principal — “clasificación como remote sensing / EO”

### 6.1 Escala
- **Probabilidad (P):** 1 Muy baja … 5 Muy alta  
- **Impacto (I):** 1 Bajo … 5 Crítico  
- **Severidad (S):** P×I (1–25)  
- **Niveles:** 1–5 Bajo, 6–10 Medio, 11–15 Alto, 16–25 Crítico

### 6.2 Tabla

| ID | Riesgo | P | I | S | Drivers (qué lo dispara) | Mitigación (diseño/ops) | Trigger (acción) |
|---|---|---:|---:|---:|---|---|---|
| PH-REG-01 | “De facto EO”: se interpreta como satélite de observación/teledetección por **capacidad** (no por intención) | 3 | 4 | 12 | GSD bajo + óptica narrow + pipeline de productos | PH‑GUARD‑01/02/03 + no multispectral + documentación explícita “demo” | TRG‑01/03 ⇒ **freeze** cambios + revisión legal/partner |
| PH-REG-02 | Se interpreta como “servicio satelital” (prestación a terceros / comercial) | 2 | 5 | 10 | tasking, SLAs, clientes, monetización | PH‑GUARD‑07 + política “no service” | TRG‑05/06 ⇒ stop + rediseño de objetivos |
| PH-REG-03 | Incumplimiento de reglas de servicio de radioaficionados por satélite por uso “no amateur” (p.ej. comercial) | 2 | 4 | 8 | monetización, contenido comercial, operación fuera de reglas | Operación estricta amateur + apoyo de radioclub + compliance ENACOM/IARU | TRG‑06 ⇒ detener emisión / re‑encuadrar |
| PH-REG-04 | Aumento de escrutinio por lanzamiento/registro por declarar payload óptico (paperwork extra, demoras) | 3 | 3 | 9 | documentación insuficiente, ambigüedad de propósito/capacidad | ICD + “capability statement” limitado + guardrails medibles | Si partner pide info ⇒ entregar “capability pack” (Anexo A) |

---

## 7) Matriz de riesgo secundaria — privacidad/datos (publicación de imágenes)

> Aunque un CubeSat “context camera” con GSD deliberadamente alto **no** debería captar personas identificables, el riesgo “legal/social” aparece por publicación irresponsable o por malentendidos. En Argentina hay jurisprudencia reciente y recurrente sobre privacidad/imagen en contextos de captura/publicación (no espacial), que sirve como señal de sensibilidad social/judicial.

| ID | Riesgo | P | I | S | Drivers | Mitigación | Trigger |
|---|---|---:|---:|---:|---|---|---|
| PH-DATA-01 | Publicación de imagen que se interpreta como invasiva (personas/propiedad/instalación sensible) | 1 | 4 | 4 | publicación automática, sin revisión humana | PH‑GUARD‑08 + revisión humana + delay | Cualquier reporte/queja ⇒ retirar + post‑mortem |
| PH-DATA-02 | Percepción pública “vigilancia” aunque técnicamente no lo sea (riesgo reputacional / bloqueo de partners) | 3 | 3 | 9 | comunicación ambigua (“spy satellite”), demos virales | framing educativo + “capability statement” | Viralización negativa ⇒ pausa publicación |

Referencias (sensibilidad privacidad):
- Nota/jurisprudencia pública sobre Street View (ejemplo de estándar social de intimidad):  
  https://tn.com.ar/tecno/novedades/2025/07/23/google-debera-indemnizar-a-un-argentino-que-aparecio-desnudo-en-street-view/  
  (usar solo como “señal de sensibilidad”, no como analogía legal directa)

---

## 8) Requisitos adicionales recomendados (para cerrar el riesgo con ingeniería)

Estos se sugieren como “mini‑requirements” locales del payload:

- **PH-REQ-01 (Cap de resolución):** el diseño óptico + órbita deberá asegurar **GSD ≥ 500 m/pixel** (objetivo) y nunca < 250 m/pixel (límite duro).  
- **PH-REQ-02 (No targeting):** no existirá comando de “capture at lat/lon”; solo `CAPTURE_NOW` sujeto a modo/ventana y rate‑limit.  
- **PH-REQ-03 (Metadata limitada):** no se downlinkea orientación/posición a resolución que permita georreferenciar robustamente la escena.  
- **PH-REQ-04 (Rate limit):** máx. 1 imagen por pasada y 3 por día; enforcement por FSW.  
- **PH-REQ-05 (Safe default):** alineado con MIS‑REQ‑PH‑01, el payload inicia OFF y requiere comando explícito + timeout.  
- **PH-REQ-06 (Kill‑switch):** el EPS/FSW puede deshabilitar el rail del payload (hard power‑gate) ante fault o por comando.

---

## 9) Evidencia que conviene preparar (“capability pack” para launch provider / compliance)

**Anexo A — Capability Statement (1–2 páginas):**
- Objetivo: “demo educativa” + ejemplo de imágenes de referencia (simuladas).
- Óptica: FOV, focal, sensor, **GSD esperado** (con cálculo simple).
- Operación: OFF default, rate‑limit, sin targeting, sin geo‑products.
- Data: tamaño de imagen, compresión, chunks, cuota best‑effort.
- Reglas de publicación: delay, revisión humana.

---

## 10) Decisión recomendada (criterio objetivo)

Si querés **minimizar** riesgo de caer en “remote sensing”:

1) Diseñar `PHOTO_DEMO` como **context camera** (wide‑angle, baja resolución deliberada).  
2) Prohibir por diseño: **targeting**, **geo‑products**, **near‑real‑time**, **tasking**.  
3) Mantenerlo estrictamente “opt‑in”, con **kill‑switch** y cuotas (ya en baseline).  
4) Documentar “capability statement” desde el día 1 para evitar fricción con partners.

Si el objetivo evoluciona a “fotos lindas” con GSD baja, pointing y publicación sistemática: **eso ya es otro proyecto** (EO/remote sensing) y hay que re‑encuadrarlo con asesoría legal y coordinación regulatoria desde el inicio.

---

## 11) Referencias principales (linkables)

- ENACOM Res. 3635/2017 — Reglamento General de Radioaficionados:  
  https://www.enacom.gob.ar/multimedia/normativas/2017/res3635%20%28octubre%29.pdf
- ENACOM trámite Estaciones Espaciales y Terrenas (Radioaficionados):  
  https://www.enacom.gob.ar/tramites/radioaficionados-estaciones-espaciales-y-terrenas_t137
- Res. 58/2025 — Reglamento General de Gestión y Servicios Satelitales:  
  https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-58-2025-411419/texto
- Ley 24.158 — Convenio sobre Registro de Objetos Lanzados al Espacio:  
  https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/556/norma.htm
- Res. 260/1999 — Reglamento orgánico del Registro Nacional de Objetos Lanzados al Espacio:  
  https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-260-1999-57753
- CONAE — Registro de satélites (contacto):  
  https://www.argentina.gob.ar/ciencia/conae/institucional/registro-de-satelites
- ITU Radio Regulations — Artículo 1 (Terms/Definitions):  
  https://life.itu.int/radioclub/rr/art1.pdf
- ITU‑R Handbook — Earth Exploration‑Satellite Service (EESS):  
  https://www.itu.int/dms_pub/itu-r/opb/hdb/R-HDB-56-2011-PDF-E.pdf
