# RF_ANALISYS_OPENLST.md — Análisis OpenLST como Base para TTC UHF

**Proyecto:** DIY Nanosat (Buenos Aires, AR)
**Revisión:** 2026-03-03 (sin cambios de contenido al 2026-03-13)
**Estado:** Preliminary — análisis técnico de factibilidad
**Trazabilidad:** `04_Communications/rf_subsystem_overview.md`, `SYSTEM_BASELINE.md`

---

> **Estado documental (2026-03-13):**
>
> Este documento es un análisis técnico de factibilidad. **No reemplaza el baseline ni ninguna decisión ADR.**
>
> Posición del proyecto al 2026-03-13:
> - Baseline operativo vigente: **UHF 435 MHz FSK 1200 bps**.
> - OpenLST: **candidato técnico en análisis / base de desarrollo**. No es baseline final.
> - Hardware TTC UHF final: **TBD**.
> - **No adoptar OpenLST "tal cual"**: componente RFFM6403 (FEM — Front-End Module) está EOL (End of Life).
> - Para cerrar adopción: requiere ADR nueva en estado `Accepted` + resolución de supply chain del front-end.
> - Decisión adicional 2026-07-04: la arquitectura UHF candidata debe permitir `PUBLIC_BEACON` compatible con SatNOGS y separar `CONTROLLED_DOWNLINK` / `PRIVATE_UPLINK` para payload y comandos. Ver `08_Decisions/ADR-20260704-satnogs-public-beacon-private-payload-uplink.md`.
>
> **No se debe:** citar este análisis como si fuera decisión de baseline. No se debe fijar RFFM6403 como componente de diseño final.

---

## 0) Resumen ejecutivo (1 pantalla)

**OpenLST** es una implementación open-source (HW + FW + tooling) liberada por Planet Labs, derivada del **LST (Low‑Speed Transceiver)** usado como radio UHF TTC en la constelación **Dove**. El repositorio principal declara **>200 satélites** y **>200 años satélite acumulados** de operación en órbita, con **COTS** y costo de componentes **< USD 50** (solo BOM de RF+MCU, sin PCB/ensamble).  
Fuentes primarias: repositorios oficiales `OpenLST/openlst` y `OpenLST/openlst-hw`.  

**Encaje con el MVP actual del proyecto:**  
- El baseline del DIY Nanosat define **UHF ~435 MHz (FSK 1200 bps)** como downlink y TTC, y **LoRa 915 MHz RX-only** para uplink usuario (`00_MVP/MVP v2.2.md`, `SYSTEM_BASELINE.md`).  
- OpenLST apunta exactamente a **70 cm (≈437 MHz)** y usa **2‑FSK** con bitrates del orden de **7.4 kbps** (configurable).  
- Por ende, OpenLST es un **candidato fuerte** como punto de partida de una **radio TTC UHF** más “flight‑heritage‑like” que módulos maker típicos.

**Riesgo principal 2026:** el diseño de referencia incorpora un **FEM (Front-End Module)**, **Qorvo RFFM6403**, **discontinuado** (EOL anunciado 2019). Esto obliga a rediseñar el front‑end (PA/LNA/switching/filtrado) o a depender de stock residual.  

**Recomendación:**  
- **Sí** tomar OpenLST como **candidato técnico prioritario** (PHY, framing, tooling, arquitectura y layout RF “con herencia”).  
- **No** copiar el diseño “tal cual” (por obsolescencia del FEM y por adaptar a regulaciones/coord. de satélite).  
- En práctica: fork del hardware y crear una **OpenLST‑Derived TTC Board** con: CC1110 (o migración a CC13xx si decidimos), front‑end modular (PA + SAW + switch/LNA), y compliance (inhibits RF, identificador, coordinación).
- Si los resultados son positivos, formalizar adopción mediante ADR nueva antes de considerarlo baseline.

---

## 1) Resultados de la investigación (qué encontré)

### 1.1 Qué es OpenLST
- OpenLST es la liberación open-source (firmware + herramientas + referencia de hardware) de Planet, basada en su radio LST para TTC en UHF.  
  - Repositorio oficial: https://github.com/OpenLST/openlst  
  - Repositorio hardware (KiCad): https://github.com/OpenLST/openlst-hw  

### 1.2 Qué incluye
Según el repo oficial:
- Proyecto de firmware (bootloader + aplicación) para 70 cm (UHF).  
- Herramientas Python para test/operación.  
- Referencia de hardware basada en **TI CC1110** (MCU 8051 + transceiver sub‑GHz).  

Según el repo de hardware:
- KiCad 4.0, esquemático PDF, BOM, gerbers.  
- Diseñado para **437 MHz**, y explícitamente indica que “puede modificarse a otras frecuencias” (dentro de la familia sub‑GHz).

### 1.3 Parámetros de enlace publicados en fuentes externas
- Artículos técnicos describen configuración típica 2‑FSK alrededor de 437 MHz con bitrate ~7416 baud y FEC/whitening (como aparece en material académico que analiza/modifica OpenLST).  
- Una nota periodística técnica (2018) menciona 3.5 kbps de user data para el radio UHF OpenLST.

---

## 2) Background y Flight Heritage

### 2.1 Origen (Planet Labs)
Planet desarrolló LST como radio UHF TTC para sus **Dove**. OpenLST “draws on” esa experiencia y declara >100 Doves con LST, y >200 Doves acumulados con cientos de “satellite-years”.  
- Fuente: README oficial OpenLST `openlst` (Planet claim).  

### 2.2 Evidencia secundaria (papers/tesis)
Hay publicaciones académicas que usan OpenLST como plataforma de estudio/modificación (p. ej. migración a AX.25), lo que además indica que el stack es “real” y replicable.  
- Ejemplo: tesis/paper de Georgia Tech sobre modificar el firmware de OpenLST para compatibilidad con AX.25 (amateur packet radio).

### 2.3 Implicancia
Para un proyecto DIY, OpenLST ofrece algo raro: **herencia de vuelo masiva** en un stack abierto. Eso reduce el riesgo técnico frente a “módulos genéricos” sin historial orbital.

---

## 3) Compatibilidad con nuestro proyecto (MVP DIY Nanosat)

### 3.1 Requisitos de COMMS del proyecto (baseline actual)
En la documentación consolidada del proyecto:
- Uplink usuario: **LoRa 915 MHz RX‑only en órbita** (mitigación regulatoria).  
- Downlink/TTC: **UHF 435 MHz**, baseline **FSK 1200 bps** (amateur-sat, con coordinación/encuadre).  

> Esto implica que OpenLST se evalúa como candidato para **UHF TTC**, no para LoRa 915.

### 3.2 Encaje técnico
OpenLST:
- Trabaja en el orden de 400–470 MHz con mínimo cambio de filtrado (SAW) según su guía.  
- Usa 2‑FSK (compatible con el concepto “FSK robusto” del MVP).  
- Brinda tooling (Python) y un stack de framing/protocolo que puede adaptarse a nuestras tramas (BEACON, STATUS, LORA_LOG, ACK/NACK).

**Conclusión:** alta compatibilidad conceptual y de banda (UHF).

### 3.3 Encaje operativo (CONOPS)
OpenLST se adapta a “store & forward + ventanas de downlink”. El mayor bitrate potencial (~7.4 kbps raw, user ~3.5 kbps) mejora margen operativo (más datos por pasada o menor duty).

---

## 4) Análisis legal (Argentina + internacional)

> Nota: esto NO es asesoramiento legal; es un checklist técnico-regulatorio para guiar diseño y trámites.

### 4.1 Argentina (ENACOM)
- La operación en el **Servicio de Radioaficionados** y **Servicio de Radioaficionados por Satélite** está regulada por ENACOM (reglamento general, plan de bandas, licencias/categorías).  
- Para un downlink UHF “amateur-sat”, el camino típico es:
  1) encuadre de misión bajo “amateur-satellite service” (sin fines de lucro, experimentación),
  2) licencia/estación (propia o a través de radio club),
  3) coordinación de frecuencia (ver IARU en 4.2),
  4) cumplimiento de identificaciones, emisiones, potencia, etc.

Fuentes:
- ENACOM – página “nuevo reglamento de radioaficionados”: https://www.enacom.gob.ar/nuevo-reglamento-de-radioficionados_p3301  
- Texto reglamentario PDF (ENACOM): https://www.enacom.gob.ar/multimedia/noticias/archivos/201711/archivo_20171107072645_3234.pdf  
- Resolución nacional (actualizaciones al régimen): https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-1186-2024-406719/texto  

### 4.2 Internacional (ITU + IARU)
- Para satélites, además de la licencia nacional, se requiere encuadre en el **International Telecommunication Union (ITU)** (coordinación de asignaciones, filings, etc.) dependiendo del perfil de misión y del país de administración.  
- En bandas amateur-sat, es práctica estándar requerir prueba de coordinación IARU (International Amateur Radio Union) para el launch provider y para operación ordenada.  
- Esto coincide con requisitos típicos de integradores/lanzadores: “provide documentation of proper licenses… for amateur frequency use, requires proof of frequency coordination by the IARU”.

Fuente de requisito de coordinación (CubeSat Design Specification Rev 14.1, Cal Poly): ver CDS Rev 14.1.

### 4.3 Implicancia para elegir banda “óptima”
En nuestro MVP ya está tomada la decisión macro:
- **No transmitir ISM desde órbita** (LoRa RX-only).  
- Downlink/TTC por **UHF amateur-sat**.

Por ende, “optimizar banda” en el corto plazo significa optimizar **dentro del marco amateur-sat** (435–438 MHz típicamente), no saltar a bandas comerciales/space-ops (lo cual dispara complejidad de licensing/frequency filing).

---

## 5) Factibilidad de implementación en custom PCB (partiendo del diseño original)

### 5.1 Qué tan “copiable” es openlst-hw
El repo `openlst-hw` es un KiCad completo (esquemático + layout + BOM + gerbers). Eso habilita un fork y una placa derivada sin empezar de cero.

### 5.2 Qué partes “rompen” al migrar/retocar
El stack puede dividirse en 4 bloques:

1) **SoC RF+MCU:** TI **CC1110** (transceiver sub‑GHz + 8051).  
2) **Referencia + reloj:** TCXO (≈27 MHz en diseños reportados) + matching/baluns.  
3) **Front-end RF:** PA (power amplifier) + switching TX/RX + LNA/bypass + filtrado armónicos.  
4) **Filtrado de banda:** SAW (custom) centrado en 446 MHz con ~20 MHz BW (según user guide).

La guía de usuario indica que, para moverse en 400–470 MHz, el componente que típicamente cambia es el **SAW filter** (el resto del diseño “funciona” en ese rango, sujeto a matching/PA).  

**Convergencia con nuestro proyecto:** queremos 435–438 MHz. Esto está *dentro* del rango 400–470, pero es probable que convenga un SAW centrado más cerca de ~435–437, o al menos que cubra 435–438 dentro del pasabanda.

### 5.3 “No reinventar el RF”
Para un custom PCB pragmático:
- Mantener CC1110 + su red RF lo más intacta posible.
- Cambiar:
  - SAW filter a uno que cubra 435–438 (o centrado ~436/437).
  - Front-end PA/FEM por alternativa vigente (ver §6).
- Mantener footprints/placement de RF siguiendo la herencia (planos, keepouts, SMA, etc.).

---

## 6) Componentes discontinuados y alternativas de mínimo impacto

### 6.1 FEM/PA (Qorvo RFFM6403) — **discontinuado**
En la guía de usuario se menciona RFFM6403 como módulo que eleva la potencia a **1 W (+30 dBm)**.  
El producto figura como **Discontinued / End of Life** (EOL anunciado 2019, LTB 2020).  
Fuentes:
- Guía OpenLST (menciona RFFM6403).  
- Qorvo product page RFFM6403 (EOL/Discontinued).

**Impacto:** alto, porque el FEM integra PA + switch + filtrado y es difícil “drop-in”.

#### Alternativa A (mínimo rediseño, alto riesgo supply)
- Comprar RFFM6403 por brokers/stock residual (costo y riesgo altos; no recomendado para una placa “repetible”).
- Útil solo para 1–3 prototipos rápidos.

#### Alternativa B (recomendación: front-end modular discreto)
Mantener CC1110 y reemplazar el FEM por:
- **PA** discreto (IC PA) + **RF switch** (o T/R con diodos/PIN) + (opcional) **LNA** + filtrado armónicos (LPF) + SAW.
- Ventaja: piezas reemplazables, supply más robusto, “fácil” de re‑spin.
- Desventaja: más RF layout y matching; requiere V&V.

Candidatos de PA (ejemplos reales, todos requieren evaluación de matching y linealidad en 435–438):
- **NXP AFIC901N** (Integrated PA, 1.8–1000 MHz, 30 dBm, requiere ~7.5 V). Interesante porque podríamos alimentarlo desde un rail derivado de batería 2S (si lo permitimos en EPS RF).  
  Datasheet: https://www.nxp.com/docs/en/data-sheet/AFIC901N.pdf  
- **Skyworks FEM 450–470 MHz** (familia FEM para UHF; ejemplo en datasheet de un FEM 450–470 MHz con PSAT ~+27 dBm). Puede servir para un diseño “casi 1W” con menor potencia o con PA externo.  
  Ejemplo datasheet: https://www.skyworksinc.com/-/media/A3700C2040BC4C3290F362388DD0CF5C.pdf  
- **SGM33685C** (PA para rangos sub‑GHz incluyendo 450–460/470–510 según hoja). Es un candidato moderno, pero hay que validar si cubre 435–438 con performance útil.  
  Datasheet: https://www.sg-micro.com/rect/assets/f86e2b35-0753-4aa2-a809-4c16e57a951c/SGM33685C.pdf  

> Nota: el objetivo de estas alternativas no es “copiar el FEM”, sino preservar el **diagrama de bloques** y mantener al CC1110 como radio base.

### 6.2 SAW filter STA1120A — “custom SAW” que se cambia por banda
La guía de usuario dice explícitamente:
- “The only part that will need to change is the custom SAW filter (U8, STA1120A)… centered at 446 MHz with 20 MHz BW… Sawtron makes a wide selection of filters in the same package.”

Esto es favorable: el diseño está pensado para que el SAW sea el componente de “tuning” de banda dentro de 400–470 MHz.  
Acción: elegir SAW para 435–438 en el mismo package/footprint.

---

## 7) Proyección de costos (BOM + PCB + ensamblado)

> Objetivo: orden de magnitud para prototipos (1–10 uds). Los precios reales dependen de disponibilidad, importación y MOQ.

### 7.1 Costo estimado por unidad (prototipo)
**Escenario 1: copiar diseño con RFFM6403 (no recomendado por supply)**  
- PCB RF 4 capas (50×60 mm aprox, ENIG): USD 20–60/u (baja cantidad)  
- Ensamblado SMD (externo): USD 30–120/u según proveedor/volumen  
- BOM electrónica:
  - CC1110: ~USD 6–15 (según canal)  
  - RFFM6403: **USD 20–80** (si se consigue)  
  - SAW + TCXO + pasivos RF: USD 10–30  
- **Total típico**: USD 70–250/u

**Escenario 2 (recomendado): front-end modular discreto, sin RFFM6403**  
- PCB RF 4 capas: USD 20–60/u  
- Ensamblado: USD 30–120/u  
- BOM:
  - CC1110: USD 6–15  
  - PA + switch + LNA + SAW + TCXO: USD 20–60 (dependiendo selección)  
- **Total típico**: USD 70–240/u (similar, pero con supply mejor y repetible)

### 7.2 Proveedores (Argentina / acceso local)
Para una estrategia realista en Buenos Aires:
- **Distribuidores locales** (rápidos, pero stock variable):
  - Electrocomponentes: https://www.electrocomponentes.com/  
  - Elemon: https://www.elemon.com.ar/  
- **Distribuidores internacionales con envío a Argentina** (mejor stock, más costo/aduana):
  - Mouser Argentina: https://ar.mouser.com/  
  - DigiKey (envío internacional)  
  - TME (sitio AR): https://www.tme.com/ar/es/  

**Nota de supply:** para ICs RF específicos, lo más robusto es Mouser/DigiKey/TME. Para pasivos, conectores, reguladores, etc., los locales suelen cubrir mucho.

---

## 8) Impacto en el presupuesto energético (EPS)

### 8.1 Consumo pico
Con 1 W RF, un front-end típico puede demandar varios watts eléctricos:
- El RFFM6403 (cuando existía) aparece listado con corrientes del orden de **~1.25 A** a **2.5–4.2 V** en distribuidores, lo que implica picos ~3–5 W DC.  
- Más el CC1110 + lógica (~0.1–0.3 W).

**Diseño EPS recomendado:**
- RF rail conmutado (3V3_RF / 5V_AUX según ICD del proyecto).
- Si el PA requiere >5 V (ej. 7.5 V tipo AFIC901N), se deberá introducir un rail dedicado (boost o buck desde 2S) y analizar eficiencia/ruido.

### 8.2 Energía por pasada (orden de magnitud)
Supongamos:
- Potencia DC TX pico: 4.5 W  
- Ventana útil de downlink: 8 min  
- Duty TX (no continuo): 30% (por ARQ/esperas/overhead)

Energía ≈ 4.5 W × 0.3 × (8/60) h ≈ 0.18 Wh por pasada.

Esto es manejable en 1.5U con operación por ventanas, pero obliga a:
- medir bien el duty real y
- limitar transmisiones en eclipse o con batería baja (SAFE MODE manda).

---

## 9) Impacto en ground base (estación terrena)

### 9.1 Hardware
- OpenLST puede usarse también en tierra como módem (mismo stack), o podemos recibir con SDR y demodular 2‑FSK.
- Para maximizar margen: Yagi/cross-yagi UHF + LNA en mástil + SDR/radio dedicado (ya alineado con el baseline).

### 9.2 Software
- OpenLST trae tooling Python (para operar/configurar radios).  
- Si migramos protocolo (p.ej. AX.25), hay material académico y tooling en el ecosistema amateur.

---

## 10) Resultados prácticos esperados

### 10.1 Ancho de banda / tasa
Hay dos perfiles posibles:

**Perfil A (conservador, alineado con MVP):**  
- FSK 1k2 (1200 bps) / framing robusto / beacon “siempre llega”.

**Perfil B (OpenLST default):**  
- 2‑FSK con bitrate raw ≈ 7416 baud, user data reportada ~3.5 kbps.  

### 10.2 Ventana de downlink (volumen de datos)
En una pasada útil de ~8 min:

- A 1.2 kbps: ≈ 70 KiB por pasada (sin contar overhead).  
- A 3.5 kbps: ≈ 205 KiB por pasada (sin contar overhead).  

En ambos casos, el limitante real suele ser:
- elevación útil,
- apuntado/polarización,
- duty permitido por potencia,
- robustez del protocolo (ARQ/FEC).

---

## 11) Sourcing BOM (BOM de alto nivel)

> **No** es la BOM completa del repo; es una BOM de compras “por bloques” para estimación y supply.

| Bloque | Parte / familia | Notas | Sourcing sugerido |
|---|---|---|---|
| SoC RF+MCU | TI **CC1110Fxx** | Activo según TI; base OpenLST | Mouser/DigiKey/TI Store |
| Reloj | TCXO ~27 MHz (o XO + calib) | estabilidad vs Doppler y tasa | Mouser/DigiKey/local |
| Filtrado banda | SAW “form-factor STA1120A” | elegir center/bw para 435–438 | Sawtron u otro vendor (mismo package) |
| Front-end (legacy) | Qorvo **RFFM6403** | Discontinued/EOL | NO recomendado |
| Front-end (nuevo) | PA + switch + LNA discreto | elección por disponibilidad | Mouser/DigiKey |
| Matching/LF | pasivos RF (0402/0603), inductores, caps NP0 | RF layout crítico | local + Mouser |
| Conectores | SMA u.FL + feedline | mecánica | local |

---

## 12) Recomendación general del approach

### 12.1 Qué haría (recomendación)
1) **Evaluar OpenLST como candidato TTC UHF** (PHY + tooling + arquitectura) por su herencia y por encajar con 70 cm.  
2) **Fork** de `openlst-hw` y crear una variante: **OpenLST‑Derived‑TTC‑435**:
   - SAW centrado para 435–438.
   - front-end discreto reemplazando RFFM6403.
   - power‑gating + medición de consumo RF (alineado con ICD EPS).
   - inhibiciones RF (mínimo 3, ver CDS Rev 14.1).
3) Mantener “compatibilidad de operación” con tu ground segment:
   - Beacon ultra robusto (posible 1k2) + modo “bulk downlink” (3–7 kbps) cuando el margen lo permita.
4) Si la validación técnica/regulatoria cierra, emitir ADR de adopción para actualizar baseline canónico.

### 12.2 Qué NO haría
- No construir un diseño que dependa del RFFM6403 como componente crítico.
- No cambiar el bandplan del MVP (salir de amateur-sat) antes de cerrar el marco legal y el filing.

---

## 13) MUST BE TRUE (condiciones mínimas para decidir “sí vamos con OpenLST”)

1) **Regulatorio:**  
   - Camino claro ENACOM + IARU (coordinación) para operar en 435–438 como amateur-sat.  
2) **Supply chain:**  
   - BOM final sin piezas EOL críticas (especialmente PA/front-end y SAW).  
3) **EPS:**  
   - Capacidad de soportar picos de TX (≥4–6 W por ráfagas) sin violar SAFE MODE ni brownouts.  
4) **RF Inhibits:**  
   - Implementación de inhibiciones RF exigidas por integradores (mín. 3 inhibiciones independientes, no temporizador).  
5) **V&V:**  
   - Ensayos de BER/link con hardware real, y validación de espectro (armónicos) en banco/campo.  
6) **Ground readiness:**  
   - Estación terrena capaz (antena+LNA+SDR) y pipeline de decodificación validado end‑to‑end.

---

## 14) Próximos pasos (concretos)

1) **Bajar y auditar BOM completa del repo** (`openlst-hw/bom`) y marcar: EOL/NRND, single‑source, y lead times.  
2) Elegir estrategia de front‑end (PA discreto):  
   - shortlist de 2–3 PAs disponibles (Mouser/DigiKey) + switch/LNA.  
3) Definir **perfil de modulación/tasa** para MVP:  
   - Beacon 1k2 “siempre llega” + modo 3–7 kbps para dump.  
4) Diseñar **OpenLST‑Derived‑TTC‑435 v0.1** en KiCad:  
   - cambios mínimos (SAW + front-end) manteniendo placement RF.  
5) Banco RF:  
   - medir potencia, espectro, sensibilidad, y corriente TX/RX.  
6) Legal:  
   - checklist ENACOM + coordinación IARU + documentación para launch provider.

---

## 15) Referencias (links)

### OpenLST (fuentes primarias)
- OpenLST firmware/tools: https://github.com/OpenLST/openlst  
- OpenLST reference hardware: https://github.com/OpenLST/openlst-hw  
- OpenLST User Guide (custom HW + SAW + PA): https://github.com/OpenLST/openlst/blob/master/open-lst/USERS_GUIDE.md  

### Obsolescencia RFFM6403
- Qorvo RFFM6403 (Discontinued/EOL): https://www.qorvo.com/products/p/RFFM6403  

### Regulaciones / coordinación
- ENACOM: reglamento radioaficionados: https://www.enacom.gob.ar/nuevo-reglamento-de-radioficionados_p3301  
- ENACOM reglamento PDF: https://www.enacom.gob.ar/multimedia/noticias/archivos/201711/archivo_20171107072645_3234.pdf  
- Resolución 1186/2024 (Argentina): https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-1186-2024-406719/texto  

### Datasheets candidatos PA (para alternativa front-end)
- NXP AFIC901N: https://www.nxp.com/docs/en/data-sheet/AFIC901N.pdf  
- Ejemplo Skyworks FEM 450–470: https://www.skyworksinc.com/-/media/A3700C2040BC4C3290F362388DD0CF5C.pdf  
- SGM33685C PA: https://www.sg-micro.com/rect/assets/f86e2b35-0753-4aa2-a809-4c16e57a951c/SGM33685C.pdf  
