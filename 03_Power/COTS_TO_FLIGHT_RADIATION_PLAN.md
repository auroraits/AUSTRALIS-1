# Plan preliminar COTS-to-Flight y radiación — EPS/electrónica

**Revisión:** 2026-07-27
**Estado:** Preliminary
**Trazabilidad:** órbita, shielding, layout y partes finales `TBD`

## 1. Estado

AUSTRALIS-1 no dispone todavía de un análisis de radiación que justifique el
uso orbital de CM5, STM32, memorias, celdas solares ni ICs de potencia COTS.
Watchdog y SAFE mitigan algunos resets, pero no cubren latch-up destructivo,
Total Ionizing Dose (TID), Displacement Damage Dose (DDD), burnout, degradación
paramétrica ni corrupción persistente.

No se asignan valores de dosis o tasas SEE en este documento: dependen de
órbita/época/duración, shielding y partes exactas.

## 2. Entorno a determinar

El análisis controlado deberá registrar:

- órbita nominal y envolvente, época y vida de misión;
- modelos/herramientas y revisiones;
- TID detrás de distribución de shielding derivada del CAD;
- DDD para celdas solares, optoelectrónica y sensores;
- espectro de protones/iones y tasas de Single Event Effect (SEE);
- margen de incertidumbre y casos solar nominal/tormenta;
- supuestos de orientación y material.

## 3. Matriz por parte

Cada MPN/revisión/lote requiere:

| Campo | Evidencia |
|---|---|
| función/criticidad | efecto en SAFE y misión |
| tecnología/proceso | fuente verificable |
| TID/DDD | rating, ensayo o justificación |
| SEE | SEU/SET/SEL/SEFI/burnout/gate rupture aplicables |
| temperatura/tensión | condiciones y derating |
| shielding | espesor equivalente derivado del CAD |
| mitigación | hardware, software, redundancia o aceptación |
| V&V | procedimiento, fluencia/dosis y criterio |

Partes mínimas: CM5/RAM/eMMC, STM32/OBC, SPI NOR, microSD, sensores ADCS,
transceivers/PA, MPPT/cargador, BMS/protecciones, reguladores/switches,
supervisor/watchdog y celdas solares.

## 4. Mitigaciones candidatas a verificar

- current limiting y power-cycle independiente por dominio para SEL;
- watchdog externo y supervisor de rails;
- boot image inmutable/verificada y recuperación de filesystem;
- EDAC/ECC donde exista, scrubbing y CRC de datos críticos;
- copias redundantes de configuración con versionado/rollback;
- detección de corrupción y safe defaults;
- derating de tensión/corriente/temperatura;
- shielding optimizado contra análisis, no espesor arbitrario;
- selección/lot screening o ensayo de partes dominantes;
- degradación EOL de solar y batería en los budgets.

Ninguna mitigación se considera efectiva hasta ensayarla o justificarla contra
datos de la parte exacta. Un reset no mitiga un latch-up sin limitación de
corriente y desconexión.

## 5. Gates

| ID | Gate | Criterio |
|---|---|---|
| RAD-VV-01 | entorno | reporte TID/DDD/SEE reproducible |
| RAD-VV-02 | selección | matriz completa de partes críticas |
| RAD-VV-03 | diseño | mitigaciones incluidas en esquema/BOM/software |
| RAD-VV-04 | ensayo | evidencia de parte o prueba con criterio |
| RAD-VV-05 | integración | fault injection y recuperación verificada |
| RAD-VV-06 | EOL | budgets de potencia/solar/datos actualizados |

Hasta cerrar estos gates, todo hardware COTS permanece candidato
Bench/Flight-Like, no Flight.
