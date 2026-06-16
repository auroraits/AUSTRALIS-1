# BOM — EPS Bench1 1S

**Review date:** 2026-02-18
**Scope:** Banco de pruebas EPS 1S (no vuelo)
**Estado documental:** BOM histórico.

> BOM canónica vigente: sección 7 de `03_Power/EPS_Bench1_1S.md`.
> Este archivo se mantiene por trazabilidad histórica.

> Todos los ítems listados se clasifican como **Bench Only Component** salvo aclaración futura en migración a PCB custom.

## COTS modules

| Item | Modelo / referencia | Función | Cantidad | Clasificación |
|---|---|---|---:|---|
| Solar charger module | CN3065 1S board | Carga solar 1S de banco | 1 | Bench Only Component |
| Battery protection module | BMS 1S 5A | Protección celda (OVP/UVP/OCP) | 1 | Bench Only Component |
| Step-up converter | Boost 5V module | Generación de `+5V_BUS` | 1 | Bench Only Component |
| Step-down converter | Buck 3V3 module | Generación de `+3V3_BUS` | 1 | Bench Only Component |

## Discrete components

| Item | Valor / parte | Función | Cantidad | Clasificación |
|---|---|---|---:|---|
| Schottky diode | 1N5817 | OR-ing / antirretorno paneles | 1..N | Bench Only Component |
| Cableado | AWG TBD | Interconexión de potencia y retorno | TBD | Bench Only Component |

## Capacitors

| Ref | Valor | Ubicación | Cantidad | Clasificación |
|---|---|---|---:|---|
| C6 | 10uF | Entrada solar CN3065 | 1 | Bench Only Component |
| C8 | 100nF | Desacople Boost 5V | 1 | Bench Only Component |
| C5 | 470uF | Bulk `+5V_BUS` | 1 | Bench Only Component |
| C7 | 100nF | Desacople Buck 3V3 | 1 | Bench Only Component |
| C4 | 470uF | Bulk `+3V3_BUS` | 1 | Bench Only Component |
| — | 100nF | Desacople cercano CN3065 | 1 | Bench Only Component |

## Protection

| Item | Valor / parte | Función | Cantidad | Clasificación |
|---|---|---|---:|---|
| Fuse | 1A (tipo T) | Protección sobre línea solar principal | 1 | Bench Only Component |
| BMS protection | Integrado en módulo 1S 5A | Protección celda y bus protegido | 1 | Bench Only Component |

## Connectors

| Item | Tipo | Función | Cantidad | Clasificación |
|---|---|---|---:|---|
| Panel input connector | Bornera/JST (TBD) | Entrada paneles | TBD | Bench Only Component |
| Battery connector | JST-PH / equivalente (TBD) | Conexión batería 1S | TBD | Bench Only Component |
| Power bus connector | Header/Bornera (TBD) | Distribución `+5V_BUS` / `+3V3_BUS` | TBD | Bench Only Component |

## Notas de transición
- La migración a KiCad reemplazará módulos COTS por ICs dedicados equivalentes.
- Costos unitarios y proveedor/fuente quedan en **TBD** hasta consolidación de compras con fecha y moneda de referencia.
