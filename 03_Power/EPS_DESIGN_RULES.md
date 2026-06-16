# EPS Design Rules (DIY Nanosat) — Draft (guía técnica, no normativa)

**Revisión:** 2026-03-13 (sin cambios de contenido; cabecera actualizada)
**Estado:** Draft
**IMPORTANTE:** Este documento es guía técnica para evaluación y diseño. **No reemplaza el baseline ni los documentos normativos.** No debe usarse como fuente normativa en la requirements_matrix ni en la compliance_matrix. Para requisitos normativos, usar ADRs `Accepted` y `00_MVP/MVP v2.2.md`.

**Objetivo:** establecer reglas de diseño (sin dimensionamiento fino) para guiar decisiones del subsistema **EPS (Electrical Power System)**: arquitectura, márgenes, protecciones, tolerancia a fallas, telemetría y térmico.  
**Alcance:** reglas aplicables a banco Flight‑Like y a versión de vuelo (con adaptación de componentes/radiation).  
**No incluye:** selección final de componentes ni números definitivos de W/Wh (se hará cuando estén cerrados los subsistemas).

**Precedencia (importante):**
- Este documento es **draft técnico** para evaluación y no reemplaza el baseline bloqueado.
- El baseline canónico se fija por: `08_Decisions/*` (`Accepted`) -> `00_MVP/MVP v2.2.md` -> `SYSTEM_BASELINE.md`.
- Cualquier punto aquí marcado como propuesta requiere ADR `Accepted` para convertirse en decisión bloqueada.

---

## 0) Supuestos de trabajo (editables)
- Órbita LEO típica (~90 min) con eclipse significativo (orden 30–40 min).  
- ADCS coarse (magnetorquers) o periodos de tumbling: generación solar variable.
- Estación terrena fuerte; prioridad: **robustez y recuperabilidad** por sobre throughput.
- Arquitectura **battery‑bus backbone** (VBAT como bus primario variable), con rails derivados (mínimo: 3V3_OBC always‑on y 5V para cargas que lo requieran). Dual‑bus (VBAT + 5V) queda como **opcional** a validar con power budget.
- La topología de batería de vuelo **bloqueada** es 2S (ADR-20260218-battery-topology-2s-flight).
- 2P2S puede evaluarse como expansión de capacidad, pero requiere ADR nueva para cambiar baseline.

> Nota: este documento puede proponer mejoras o variantes, pero no revoca decisiones ya aceptadas en ADR.

---

## 1) Principios de diseño (tenets)
1. **Recoverability first:** ante falla, el satélite debe poder volver a un estado controlable (SAFE) sin intervención humana.
2. **Fault containment:** una falla debe quedar contenida en el rail/subsistema que falla.
3. **Default SAFE:** ante reset/boot, todo lo no crítico arranca apagado.
4. **Energy closure:** cada órbita debe cerrar energía (Wh) en peor caso razonable; sin esto, todo lo demás es maquillaje.
5. **Thermal-aware power:** evitar generar calor innecesario (corriente alta = I²R). El EPS debe operar dentro de límites térmicos de batería/electrónica.

---

## 2) Budgets y márgenes (reglas relativas, no números finos)

### 2.1 Diferenciar siempre “potencia” vs “energía”
- **Potencia (W):** picos instantáneos y capacidad del bus/rails.
- **Energía (Wh/orbita):** batería + generación solar vs consumo por modos.

### 2.2 Márgenes mínimos recomendados
**(A) Potencia instantánea (picos):**
- Capacidad del **bus regulado** y de switches:  
  **P_peak_design = 1.3 × P_peak_estimada**  
  (30% margen para inrush, dispersión y degradación).
- Para rail RF/TX (el más agresivo):  
  **I_limit_OCP ≈ 1.2 × I_peak_nominal** (pero con soft‑start para no disparar por inrush).

**(B) Energía por órbita (batería):**
- Dimensionar batería por **energía útil**, no nominal.  
  Regla: usar **≤70%** de capacidad nominal como utilizable (DoD + frío + envejecimiento).  
- Margen de energía sobre eclipse:  
  **E_bat_nominal ≥ 1.6 × E_eclipse**  
  (cubre DoD, pérdidas de conversión y dispersión térmica; ajustar luego con números reales).

**(C) Generación solar (paneles/strings):**
- Diseñar para peor caso razonable de actitud/rotación post‑deploy:  
  **P_solar_avg_design ≥ 1.5 × P_load_avg_orbit** (en tramo iluminado)  
  donde ese 1.5 representa: cos(θ) promedio bajo, temperatura, degradación, electrónica y sombras parciales.
- Degradación asumida para diseño: **25–30%** a lo largo de misión (conservador para COTS).

> Desafío a “sobredimensionar X% fijo”: el margen correcto depende de **variabilidad de actitud** y de si hay MPPT por string. Por eso acá se fijan multiplicadores conservadores (1.3 / 1.6 / 1.5) y se ajustan cuando existan perfiles de modos reales.

---

## 3) Tolerancia a fallas (qué pérdidas máximas debe tolerar)
Definir tolerancias explícitas evita discusiones eternas.

### 3.1 Reglas de tolerancia propuestas
- **Pérdida de 1 string solar completo** (de 4 laterales) sin perder misión básica (SAFE + RX + housekeeping).
- **Degradación solar total 30%** sin entrar en espiral de descarga (energy closure con duty-cycling).
- **Falla de TX/PA (rail RF)**: el satélite debe seguir **vivo y comandable** (RX + OBC + telemetría mínima).
- **Falla parcial de ADCS/payload**: no debe comprometer SAFE.

> Nota: con **battery‑bus backbone**, el objetivo es que una falla en un rail derivado (p.ej. 5V) no mate el satélite: se preserva SAFE sobre 3V3_OBC desde VBAT.

---

## 4) Arquitectura de rails y criticidad (propuesta tecnica para evaluacion)

### 4.1 Clasificación de rails
**Always‑On (críticos):**
- **3V3_OBC (always‑on)**: OBC + supervisor + telemetría EPS mínima.
- **RX_KEEPALIVE (mandatory):** rail dedicado para receptor/recepción de comandos y beacon mínimo (no comparte el rail del PA).

**Conmutables (no críticos / degradables):**
- 3V3_RF (RX/TX lógica) — puede ser siempre-on si RX es crítico y consumo bajo.
- **5V_RF / PA rail** (si existe): *siempre conmutado*.
- 3V3_ADCS, 3V3_PAYLOAD, 5V_AUX, heaters, etc.

### 4.2 Reglas de encendido (sequencing)
- **Rail ON → esperar estable/PGOOD → habilitar EN del subsistema.**
- Apagado inverso: **EN OFF → delay → rail OFF.**
- TX/PA: nunca habilitar sin “OK de batería” y sin confirmación de estabilidad del bus.

---

## 5) MUST HAVE (requisitos obligatorios de vuelo)

### 5.1 Protecciones eléctricas
- **OCP (Over‑Current Protection)** por rail conmutable crítico (mínimo: RF/PA, payload).
- **UVLO (Under‑Voltage Lockout)** a nivel batería/bus: entrada automática a SAFE.
- **OVP (Over‑Voltage Protection)** donde aplique (charger, bus, rails sensibles).
- Protección de inversión / ESD donde corresponda (con enfoque minimalista, sin sobrecargar el diseño).

### 5.2 Power gating
- **High‑side** por defecto (evitar low‑side salvo casos justificados).
- **Soft‑start / current limiting** en RF/PA y rails con capacitores grandes.
- **Fault containment**: corte del rail fallado sin tumbar el always‑on.

### 5.3 Estrategia anti “brownout loop”
- **TX default OFF** tras reset (pull‑downs/pull‑ups por hardware).
- Estado persistente de fallas (latch) para evitar re‑encender un rail defectuoso en loop.
- Política TX/PA:
  - **Auto‑recovery:** hasta **3 intentos** de re‑habilitar TX/PA tras una falla (con backoff entre intentos).
  - Luego queda **bloqueado hasta comando**.
  - Si no llega comando en **N órbitas** (parámetro), se rearma el contador y vuelve a habilitar hasta 3 intentos; repetir en loop.
  - TX/PA siempre es *rail separado* y con OCP/soft‑start para evitar brownout loop.

### 5.4 Supervisión independiente
- **EPS con MCU propio** (supervisor) para:
  - medir VBAT/IBAT, V/I de rails críticos
  - aplicar SAFE aunque el OBC esté colgado
  - registrar flags/contadores de falla
- **Watchdog hardware**: si OBC no “patea” el watchdog, reset/SAFE.

- **Beacon autónomo** ultra‑simple (TX muy baja potencia y duty bajo) + RX en always-on para comandos.
  - **MVP vuelo:** MCU EPS *no controla el stack RF completo*, pero sí puede *forzar* apagado de PA y sostener RX.  
  - Evolución: MCU EPS con capacidad de beacon mínimo (si se justifica).

### 5.5 Telemetría mínima EPS (obligatoria)
Si solo pudieras tener 6 campos:
1. VBAT  
2. IBAT  
3. VBUS_5V (o 3V3_OBC si aplica)  
4. Estado EPS (NOMINAL/SAFE/CRIT)  
5. Bitmask de fallas OCP/UVLO por rail  
6. Contadores: resets, OCP events, “TX faults”

---

## 6) Políticas operativas (software/hardware co-diseño)

### 6.1 Reglas de operación del TX
- TX solo habilitable si: VBAT > umbral y T_bat dentro de ventana.
- **Evitar TX + carga agresiva**: no es “prohibido”, pero sí “controlado”.
  - Regla: si cargador está en modo alta corriente, limitar TX o postergar.
  - El objetivo es evitar picos combinados que calienten batería y colapsen bus.

### 6.2 Modos y prioridades (árbol de potencia)
Prioridad de supervivencia:
1) 3V3_OBC + supervisor  
2) RX / comando  
3) Telemetría mínima / beacon  
4) ADCS coarse (si ayuda a energía/enlace)  
5) Payload  
6) TX/PA alta potencia

---

### 6.4 Solar-only survival (modo sin batería) — opcional, pero recomendado como salvavidas
**Objetivo:** si el pack de batería entra en falla (fault latched) o se vuelve inseguro, aislarlo y permitir operación **solo en sol** con un perfil mínimo: **RX + telemetría/beacon muy corto**.

**Reglas:**
- **Battery hard-disconnect obligatorio** en condición de falla: desconexión eléctrica real del pack (y bloqueo de carga) para evitar que una batería en corto/dañada colapse el sistema.
- El modo solar-only **NO busca continuidad**: en eclipse el satélite puede apagarse y debe poder **cold-boot** al volver al sol.
- Definir un rail dedicado **RX_KEEPALIVE** (always-on cuando SolarBus/VBAT lo permiten) que alimente:
  - MCU EPS (supervisor) + housekeeping mínimo
  - cadena de recepción RF (RX) y decodificación básica de comandos
- Definir un rail separado **TX_BURST** (conmutable) para **telemetría/beacon muy corto**:
  - habilitación solo por ventanas cortas (segundos), con **soft-start + limitación de corriente + encendido secuenciado**
  - **TX default OFF** tras reset
  - política de fallas: si el burst provoca caída de tensión / OCP, cortar y volver a RX_KEEPALIVE
- **No permitir TX continuo** en solar-only. Solo bursts mínimos y conservadores.
- Habilitación de cargas en solar-only debe estar gobernada por:
  - **UVLO con histéresis** + **PGOOD** + **delay/debounce** (V>V_on durante t_on) para evitar “motorboating”.
- Buffer de estabilidad:
  - **bulk capacitance** en SolarBus y RX_KEEPALIVE es obligatorio para transitorios (ms–s)
  - **supercap** queda como opcional a justificar: solo para holdup de bursts (segundos), no como reemplazo de batería.

**Notas de diseño:**
- En solar-only, el presupuesto de potencia debe asumir el peor caso de orientación (factor de generación bajo). El objetivo es “seguir escuchando” + “emitir vida” de forma esporádica.
- Los thresholds (V_on/V_off, t_on, límites de corriente) se fijarán cuando esté cerrado el power budget.

## 7) Solar: reglas de strings y MPPT

### 7.1 Topología recomendada (4 caras laterales)
- **1 string por cara** (independientes) por robustez ante sombras y fallas.
- MPPT **multi‑input** o por‑string (preferido si el costo/espacio lo permite).
- Objetivo: maximizar energía en condiciones variables (tumbling/coarse ADCS).

### 7.2 Anti‑propagación de fallas
- Evitar que un string defectuoso arrastre a otros (or‑ing / diodos / arquitectura de MPPT adecuada).
- Cableado y conectores con strain relief y diseño para vibración (no “flying wires” sin soporte).

---

## 8) Arquitectura de potencia: Battery‑Bus Backbone (propuesta alineada a baseline) + Dual‑Bus opcional

### 8.1 Propuesta principal: VBAT como bus primario
- El **bus primario** del satélite es **VBAT** (variable), alimentado por: *Solar strings → MPPT multi‑input → batería (2S/2P2S según budget)*.
- Los rails se derivan desde VBAT:
  - **3V3_OBC always‑on**: buck dedicado desde VBAT (**conservador y crítico**).
  - **5V rail**: buck desde VBAT para cargas que requieran 5V (switchable o semi‑crítico según misión).
  - Rails conmutables adicionales (RF/PA, payload, ADCS, etc.).

### 8.2 Implicancias (por qué es superior a “5V como tronco único”)
- Reduce **SPoF**: la falla del 5V no debe matar SAFE.
- Mejora eficiencia (menos conversiones “en cascada”).
- Mejora dinámica ante picos: la batería actúa como buffer energético de baja impedancia.

### 8.3 Dual‑Bus (opcional, no adoptado en baseline)
- Opción a evaluar con números: **VBAT backbone + 5V bus “principal”** para distribución interna si simplifica arnés/subsistemas.
- Regla: aunque exista un 5V “bus”, **SAFE no depende** de él (3V3_OBC y RX_KEEPALIVE deben sobrevivir desde VBAT).

### 8.4 Sobre “buffer con capacitores” (aclaración)
- Los capacitores ayudan contra **micro‑caídas**, inrush y transitorios (ms–s).
- **No reemplazan batería** para eclipse (minutos).
## 9) Térmico EPS (reglas propuestas con impacto en estructura/PCB)

### 9.1 Principios
- En vacío no hay convección: el calor sale por **conducción interna** + **radiación** en superficies externas.
- Calor interno dominante en EPS: **I²R** (batería y distribución a alta corriente).

### 9.2 Reglas térmicas
- Preferir topologías que reduzcan corriente (2S) para bajar calor.
- Asegurar “thermal path” desde:
  - batería
  - switches de PA
  - DC/DC
  hacia estructura/radiador.
- Separación física: batería lejos de PA y DC/DC calientes.
- Telemetría térmica: **T_bat** obligatoria; T de DC/DC/PA recomendado.

### 9.3 Heaters de batería
**No bloquear como MUST** todavía:
- Son útiles para operación a bajas temperaturas, pero consumen energía valiosa.
- Regla propuesta: planificar pads/espacio/driver para heater, pero habilitarlo solo si el análisis térmico lo exige.

---

## 10) Derating (reglas de confiabilidad)
- Componentes de potencia (MOSFETs, inductores, diodos, shunts) con margen:
  - Voltaje: operar ≤70% del rating continuo.
  - Corriente: operar ≤70% del rating térmico real (no el “peak” de marketing).
- Capacitores: derating de voltaje y selección de dieléctrico estable con temperatura.
- Conectores y cableado: margen de corriente + vibración.

---

## 11) Validación mínima en banco (antes de “números finos”)
- Prueba de OCP por rail (disparo, latch, reintento).
- Prueba de UVLO (entrar SAFE sin reset loop).
- Prueba de brownout con TX simulado (carga escalón).
- Prueba de secuenciado (PGOOD/EN).
- Prueba térmica de picos (I²R) con medición de T_bat y T_switch.
- Prueba de telemetría y flags persistentes.

---

## 12) Propuestas de politica para eventual ADR

1) **RX_KEEPALIVE**: se adopta rail dedicado (no comparte rail del PA).  
2) **TX/PA fault policy**: **3 intentos** de auto‑recovery con backoff; luego **bloqueo hasta comando**. Si no llega comando en **N órbitas**, se rearma y repite el ciclo.  
3) **Heater batería**: por ahora **planificado** (pads/driver y provisión mecánica/termal). Se decide inclusión en MVP tras power budget + verificación térmica.  
4) **Fallback 3V3_OBC**: **buck desde VBAT** (no depende del 5V).

> N (número de órbitas) se define cuando se cierre el CONOPS (Concept of Operations) y el perfil de pases/telemetría.
## 13) Resumen de propuestas de diseño (requiere ADR para bloquearse)

- **Arquitectura**: **Battery‑bus backbone (VBAT)** + rails derivados. **Dual‑bus** (VBAT+5V) queda opcional a validar con números.
- **Rails críticos**: **3V3_OBC always‑on** (buck desde VBAT) + **RX_KEEPALIVE** dedicado.
- **RF/TX**: rail PA separado, con **OCP + soft‑start + sequencing**; **TX default OFF** por hardware.
- **Anti‑brownout loop**: latch de falla + política **3 reintentos** → bloqueo hasta comando → rearme tras **N órbitas** sin comando.
- **MPPT**: multi‑input por string (1 string por cara, 4 caras laterales) con tolerancia a pérdida de 1 string.
- **Supervisión**: EPS con MCU supervisor + watchdog independiente; SAFE autónomo.
- **Derating y protecciones**: OVP/UVLO/OCP obligatorios según criticidad.

---

## Nota de consistencia
- Este documento no constituye por si solo una decision de baseline.
- Si alguna propuesta de este draft contradice `08_Decisions/*` (`Accepted`) o `00_MVP/MVP v2.2.md`, prevalecen esos documentos.
