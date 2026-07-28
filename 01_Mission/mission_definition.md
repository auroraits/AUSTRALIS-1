# Mission Definition — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — pre-SRR
**Trazabilidad:** `00_MVP/MVP v2.2.md` y ADRs `Accepted`

## 1. Declaración de misión

AUSTRALIS-1 investigará si un payload de inteligencia artificial puede asistir
operaciones de un CubeSat sin adquirir autoridad de vuelo. Un OBC
determinístico valida toda propuesta, mantiene el control y permite continuar
la misión con el payload apagado.

## 2. Objetivos

### Primario

Evaluar seguridad, utilidad y costo de recursos del candidato `gemma4:e2b`
mediante un protocolo preregistrado, un baseline determinístico, un oráculo
externo y evidencia reproducible.

### Secundarios

1. evaluar una cadena store-and-forward Tierra→órbita→tierra si el enlace
   Tierra→espacio resulta autorizable;
2. recolectar datos de sensores ambientales;
3. evaluar operación, recuperación y fault containment del bus;
4. mantener `PHOTO_DEMO` como opción no crítica.

## 3. Pregunta e hipótesis científica

Pregunta:

> ¿El candidato IA, contenido por el supervisor, aporta utilidad medible frente
> al baseline determinístico sin exceder los límites de seguridad, energía,
> latencia y temperatura preregistrados?

Antes de SRR se fijarán:

- hipótesis alternativa y nula;
- matriz de estados, fallas y escenarios adversariales;
- baseline/control;
- oráculo y rúbrica externos al modelo;
- tamaño de muestra y justificación estadística;
- métricas, umbrales e intervalos de confianza;
- criterios de exclusión/missing data;
- hashes de configuración y plan de análisis.

Mientras estos elementos sean `TBD`, la hipótesis no puede considerarse
demostrada ni refutada.

## 4. Criterio de éxito

Éxito mínimo exige simultáneamente:

1. bus seguro y recuperable durante el experimento;
2. protocolo preregistrado ejecutado sobre la muestra aprobada;
3. reglas críticas evaluadas sin tolerancia por oráculo externo;
4. métricas dentro de umbrales aprobados;
5. evidencia completa para correlacionar entrada→salida→supervisor→acción→efecto;
6. al menos 100 eventos científicos completos descargados;
7. al menos una configuración de prompt autenticada, activada y auditada;
8. ninguna no conformidad crítica abierta de seguridad, regulación o integridad.

Los pisos históricos de cinco inferencias/100 logs/un prompt no son por sí solos
evidencia científica suficiente.

El objetivo store-and-forward secundario exige un protocolo propio con cantidad
de nodos, frames transmitidos, elevación, PHY, interferencia, denominador de
éxito e intervalo de confianza. “Diez paquetes recibidos” es un piso de
demostración, no una tasa de performance.

## 5. CONOPS de alto nivel

1. post-eyección: todas las funciones inhibidas según CDS/ICD;
2. timers mínimos de deployment/transmisión;
3. boot en `MISSION_MODE=SAFE`;
4. checkout determinístico;
5. operación nominal y recolección científica solo con recursos autorizados;
6. IA ON únicamente en sol, `MISSION_MODE=NOMINAL` y
   `EPS_STATE=NOMINAL|HIGH`;
7. downlink/command windows autenticadas;
8. falla del payload IA → kill/power-cycle/lockout sin perder el bus;
9. safe/pasivación/end-of-life según plan aprobado.

Modelo canónico:

```text
MISSION_MODE = SAFE | NOMINAL | DOWNLINK_WINDOW
EPS_STATE    = CRIT | LOW | NOMINAL | HIGH
```

La máquina `EPS_STATE` deberá definir umbrales, histéresis, dwell, sensores
inválidos, boot/unknown y precedencia de fallas.

## 6. Segmentos

### Espacial

- CubeSat 1.5U; longitud de referencia `170.2 ± 0.1 mm`;
- EPS 2S + MPPT como arquitectura de referencia, diseño final TBD;
- OBC determinístico;
- payload IA power-gated;
- UHF TTC coordinado y receptor experimental terrestre;
- Science Pack;
- ADCS, estructura/térmico y mecanismos TBD.

### Terreno

- recepción pública compatible con SatNOGS, RX-only;
- estación de control AUSTRALIS autorizada y aislada;
- repositorio de evidencia raw/metadata/replay/export;
- weather/health inputs requeridos según diseño físico de estación.

### Usuario experimental

El objetivo LoRa 915 MHz Tierra→espacio permanece condicionado a una respuesta
escrita de ENACOM/administración competente. El satélite RX-only no autoriza al
transmisor terrestre. Sin autorización se cambiará servicio/banda o se
redefinirá el objetivo.

## 7. Baselines abiertos

- órbita/LTAN y deorbit;
- ADCS/pointing;
- configuración de modelo/hardware;
- budgets de potencia, energía, datos, masa y térmico;
- RF hardware/waveform/frecuencia/máscara;
- CAD/fit/mass properties;
- radiación y programa ambiental;
- célula/BMS/cargador/charge inhibit;
- métricas y thresholds científicos.

`600 km / LTAN 10:00 / LVLH perfecto` es solo un caso de análisis etiquetado.

## 8. Evidencia científica por inferencia

Cada registro incluirá, como mínimo:

- session/boot/event IDs y timestamps;
- snapshot/input raw y hash;
- raw model output y parse/validation result;
- digests de modelo, tokenizer, prompt, runtime, supervisor y firmware;
- seed/decoding/configuración;
- propuesta, tool/argumentos, reglas evaluadas y razón de accept/reject;
- acción aplicada y postestado;
- latencia, memoria, potencia/energía y temperaturas;
- quality flags, pérdida de datos y anomalías.

Un valor `confidence` sin definición/calibración no se interpretará como
probabilidad.

## 9. Restricciones

- ninguna acción directa de IA;
- IA OFF por defecto y durante SAFE/eclipses/EPS CRIT/LOW;
- comando/prompt autenticado y protegido contra replay;
- no transmitir LoRa/ISM desde órbita;
- no radiar sin autorización;
- no fabricar diseños placeholder;
- no declarar flight-ready sin V&V ambiental y compliance.

## 10. Trazabilidad

- requisitos: `requirements_matrix.md`;
- VCRM: `verification_cross_reference_matrix.csv`;
- compliance: `compliance_matrix.md`;
- reviews: `validation_plan_and_stage_gates.md`;
- riesgos: `../07_Risk/top_risks.md`;
- decisiones: `../08_Decisions/`.
