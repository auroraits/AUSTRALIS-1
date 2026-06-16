# Informe de revisión integral — DIY Nanosat
**Fecha:** 2026-03-12  
**Estado:** revisión técnica transversal del material disponible

## 1. Alcance revisado
Se revisaron:
- la línea base vigente (`00_MVP/MVP v2.2.md`, `architecture.md`, `README.md`, `SYSTEM_BASELINE.md`),
- documentación por subsistema exportada en `CONSOLIDADO.md`,
- código exportado en `CODIGO_FUENTE.txt`,
- PDFs de referencia adjuntos (CDS Rev 14.1, NASA CubeSat 101, etc.).

## 2. Limitación importante
La revisión es muy amplia, pero no equivale a una inspección perfecta del repositorio binario completo. El propio script `consolidar.ps1` excluye carpetas y evita archivos mayores a 1 MB, por lo que el bundle textual no garantiza capturar todos los activos CAD/KiCad/medios del proyecto.

## 3. Diagnóstico ejecutivo
El proyecto ya tiene una base documental superior al promedio DIY/universitario en cuatro frentes:
1. baseline canónico relativamente claro,
2. ADRs activas,
3. separación de subsistemas razonable,
4. evolución real de EPS y COMMS.

Pero hoy el cuello de botella no es la falta de ideas: es la **coherencia de baseline**, el **cierre de factibilidad del uplink LoRa**, la **madurez desigual entre EPS y RF**, y la **ausencia de una capa formal de compliance/verification**.

## 4. Hallazgos principales

### 4.1 Críticos
#### C1. Inconsistencia del modelo operativo
Conviven dos modelos distintos:
- histórico: `SAFE / SCIENCE / DOWNLINK_WINDOW`,
- vigente en misión/software: `MISSION_MODE = SAFE / NOMINAL / DOWNLINK_WINDOW` + `EPS_STATE = NOMINAL / SAFE / CRIT`.

Esto afecta requisitos, CONOPS, FSW y trazabilidad.

#### C2. Objetivo de misión vs factibilidad real del uplink LoRa
El objetivo exige recepción orbital desde nodos típicos en Buenos Aires, pero la propia documentación de COMMS concluye que el caso es justo y realista solo en elevaciones altas. El riesgo no está mal identificado; lo inconsistente es que el requisito todavía suena más fuerte que la evidencia experimental cerrada.

#### C3. Falta una compliance matrix de vuelo
No aparece una matriz viva que baje a requisitos verificables todo lo crítico de launch/compliance:
- RF inhibits,
- deployable inhibits,
- RBF/deployment switch,
- venting,
- materiales/outgassing,
- debris mitigation,
- timers operativos,
- licensing.

### 4.2 Altos
#### H1. Documentación histórica todavía demasiado “viva”
Hay documentos supersedidos con contenido viejo (HV/Geiger, modos antiguos, números viejos de energía, etc.) que siguen siendo fáciles de recuperar y pueden contaminar decisiones humanas o de herramientas.

#### H2. Madurez asimétrica entre EPS y RF
EPS ya tiene banco, roadmap COTS→flight-like y criterios de transición. RF todavía no: el proyecto KiCad de RF está prácticamente vacío y la selección de módulo/transceptor sigue abierta.

#### H3. Link budget UHF todavía con margen de papel en baja elevación
El baseline de 500 mW RF / 1k2 FSK es defendible, pero con margen bajo en el peor caso. No conviene tratar 10° de elevación como operación nominal.

#### H4. Costeo todavía demasiado ROM
El marco de costos está bien planteado, pero todavía no sirve para decidir; faltan valores trazables, fechas, moneda local y BOM por subsistema.

### 4.3 Medios
#### M1. Requirements matrix con trazabilidad mezclada con documentos draft
La matriz canónica todavía referencia `EPS_DESIGN_RULES.md`, que explícitamente está en estado draft/no normativo.

#### M2. Dashboard de banco útil pero no escalable a misión
El pipeline .NET 8 + SignalR es bueno para laboratorio, pero el estado de telemetría está en memoria (`RingBuffer`) y no hay persistencia operativa para post-mortem.

#### M3. Banco EPS 1S correcto como banco, pero no debe contaminar arquitectura de vuelo
La política COTS→Flight está bien explícita, pero conviene blindarla aún más para evitar lecturas erróneas del banco como baseline espacial.

## 5. Oportunidades de mejora de alto impacto

### 5.1 Convertir el baseline en un “single source of truth” de verdad
Acciones:
- renombrar o archivar documentos supersedidos,
- agregar encabezado machine-readable `Status: Superseded` / `Status: Draft` / `Status: Canonical`,
- hacer que `CONSOLIDADO.md` solo exporte documentos canónicos por defecto y anexos históricos en una sección separada.

### 5.2 Cerrar P1 de COMMS antes de seguir agregando payloads
Orden recomendado:
1. congelar la definición de “nodo típico” (EIRP real, antena, clock, duty),
2. cerrar ensayo uplink LoRa con CFO/Doppler,
3. fijar elevación mínima operativa,
4. seleccionar arquitectura TTC UHF final.

### 5.3 Añadir una compliance matrix viva
Una sola tabla con columnas:
- requisito,
- fuente (CDS / launch / regulación / ADR),
- owner,
- método de verificación,
- evidencia,
- estado.

### 5.4 Forzar stage-gates de ingeniería
#### Gate A — baseline coherente
- modos únicos,
- requirements matrix consistente,
- ADRs sincronizadas.

#### Gate B — COMMS cerrada
- uplink P1 validado o alcance corregido,
- TTC UHF elegido,
- pruebas de banco y campo cerradas.

#### Gate C — EPS flight-like
- transición 1S banco → 2S flight-like,
- mediciones reales de rails y picos,
- brownout campaign.

#### Gate D — integración de sistema
- budgets congelados,
- ICD viva,
- risk owners y exit criteria.

## 6. Qué haría inmediatamente
1. **Corregir el baseline de modos** en todos los documentos canónicos.
2. **Reescribir el objetivo P1 de uplink** con condiciones explícitas de éxito (elevación, tipo de nodo, SF/BW, resumen-first).
3. **Crear `01_Mission/compliance_matrix.md`**.
4. **Congelar el RF candidate shortlist** en máximo 2 opciones:
   - OpenLST-derived TTC,
   - transceptor/modem UHF más simple.
5. **Agregar persistencia al GroundTelemetryDashboard** aunque sea CSV/SQLite.
6. **Emitir una BOM por subsistema con fecha/proveedor/riesgo de supply**.

## 7. Qué no haría todavía
- No abrir nuevos payloads antes de cerrar COMMS y EPS flight-like.
- No convertir OpenLST en baseline sin resolver supply chain y ensayo real.
- No invertir demasiado en solar deployable antes de cerrar body-mounted + budget medido.

## 8. Veredicto ingenieril
El proyecto **sí puede subir de nivel** sin cambiar su ADN DIY. La clave no es agregar más complejidad, sino reducir ambigüedad:
- menos documentos “semi-vigentes”,
- menos supuestos blandos en uplink,
- más verificación,
- más disciplina de configuración.

Tu mejor siguiente salto no es “más hardware”; es **cerrar baseline + compliance + COMMS P1**. Cuando eso esté sólido, el resto del sistema va a empezar a converger mucho más rápido.
