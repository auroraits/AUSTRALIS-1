# Verificación ambiental preliminar — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Preliminary
**Trazabilidad:** CubeSat Design Specification Rev. 14.1 §§3.1–3.5; niveles,
artículo y secuencia sujetos al ICD del integrador

## 1. Dictamen

La verificación ambiental no es opcional para declarar readiness. La frase
histórica “si aplica/si está disponible” no puede cerrar un artículo de vuelo.
Los niveles numéricos siguen `TBD` hasta recibir el ICD y congelar masa,
estructura, mecanismos y configuración.

Fuente primaria consultada:

- *CubeSat Design Specification Rev. 14.1*, Cal Poly SLO, pp. 16–17.
- <https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS+REV14_1+2022-02-09.pdf>
- SHA-256:
  `221fbbbd4f632b16f3e219d1a5e2c2b04e1998c12025b793e6dfc6181af66b5d`.

El CDS remite random vibration (§3.1), thermal-vacuum bakeout (§3.2), shock
según el Launch Provider (§3.3), inspección (§3.4) y una ruta
qualification/protoflight (§3.5). Los ensayos adicionales de la matriz
siguiente son requisitos de ingeniería preliminares de AUSTRALIS-1 y deben
conciliarse con el plan aprobado por el integrador.

## 2. Filosofía de artículos

Antes de PDR/CDR debe definirse una de estas rutas y su racional:

- protoflight;
- unidad de calificación + unidad de vuelo/aceptación;
- combinación aprobada por el integrador.

Cada ensayo debe registrar seriales, hardware/software/configuración,
instrumentación/calibración, límites, inspección y pruebas funcionales
pre/durante/post.

## 3. Matriz mínima

| ID | Ensayo/análisis | Criterio pendiente |
|---|---|---|
| ENV-VV-01 | inspección y fit-check | CDS + ICD, peor tolerancia |
| ENV-VV-02 | propiedades de masa | masa/CG/inercia dentro del ICD |
| ENV-VV-03 | modal survey | correlación y límite del integrador |
| ENV-VV-04 | sine burst/cuasiestático | niveles/direcciones ICD |
| ENV-VV-05 | random vibration | perfil/duración/notching ICD |
| ENV-VV-06 | shock | espectro y método según mecanismo/ICD |
| ENV-VV-07 | thermal cycling | rangos/dwell/ramp por partes |
| ENV-VV-08 | thermal balance | correlación del modelo |
| ENV-VV-09 | TVAC operacional | hot/cold, arranque y SAFE |
| ENV-VV-10 | bakeout/outgassing | límite de contaminación |
| ENV-VV-11 | EMC/EMI | modos EPS/RF/CM5/ADCS worst-case |
| ENV-VV-12 | despliegue post-ambiente | tiempo, margen y repetibilidad |
| ENV-VV-13 | end-to-end RF post-ambiente | PER/EIRP/sensibilidad dentro de criterio |

## 4. Secuencia y reglas

- ejecutar baseline funcional antes de ambiente;
- inspeccionar y repetir funcional después de cada exposición relevante;
- ensayar mecanismos después de vibración y TVAC;
- no reutilizar resultados de una configuración distinta sin evaluación de
  delta;
- registrar anomalías, NCR/waivers y riesgo residual;
- no cerrar con `Blocked by Integrator`: un blocker impide readiness.

## 5. Evidencia

La evidencia mínima incluye procedimiento aprobado, raw data, logs de
telemetría, fotografías/video, certificados de calibración, configuración,
hash de software, reporte, revisión y disposición de anomalías.

Este documento no declara que ningún ensayo haya sido ejecutado.
