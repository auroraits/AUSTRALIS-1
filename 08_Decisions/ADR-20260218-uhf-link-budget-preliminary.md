# ADR-20260218-uhf-link-budget-preliminary

- **Fecha:** 2026-02-18
- **Estado:** Accepted (preliminar — sujeto a revisión con módulo seleccionado)

## Contexto
El presupuesto de potencia del MVP usaba 2.5 W eléctrico para UHF TX sin sustento en link
budget. Esto sobredimensionaba el EPS y subestimaba el margen energético real de la misión.

## Decisión
Adoptar **500 mW RF como potencia de TX objetivo** para el downlink UHF, basado en el
siguiente link budget preliminar de diseño:

| Parámetro | Valor | Fuente |
|---|---|---|
| Frecuencia | 435 MHz | Bloqueado en MVP |
| Altitud orbital | 550 km (zenith) | Supuesto de diseño |
| Free-Space Path Loss (zenith) | ~140 dB | FSPL = 20·log(4π·d/λ) |
| Elevación mínima de operación | 10° (~2 500 km slant) | Geometría orbital |
| FSPL (elevación 10°) | ~153 dB | Peor caso geométrico |
| Antena tierra (Yagi) | +10 dBi | Estimación conservadora |
| Antena satélite (¼-onda) | ~0 dBi | Omnidireccional |
| Pérdidas misceláneas | −3 dB | Polarización, conexiones, atmosférico |
| Potencia TX | +27 dBm (500 mW RF) | Objetivo de diseño |
| Potencia recibida (peor caso) | −119 dBm | 27 + 10 + 0 − 153 − 3 |
| Sensibilidad receptor (SDR+LNA, FSK 1k2) | −120 dBm | Estimación conservadora |
| **Link margin (peor caso)** | **+1 dB** | Margen de papel; tratar como experimental, no nominal |
| **Link margin (zenith)** | **~+14 dB** | Operación nominal confortable |

Potencia eléctrica estimada para UHF TX:
- RF target: 500 mW
- Eficiencia PA estimada: 35% (referencia módulos UHF CubeSat comerciales)
- **Potencia eléctrica: ~1.5 W** (reemplaza la estimación previa de 2.5 W)

## Limitaciones y próximos pasos (TBD)
1. Seleccionar módulo transceptor UHF (candidatos: AX5043, CC1101 + PA externo, Si4463).
2. Medir eficiencia real de PA del módulo seleccionado en banco.
3. Actualizar link budget con sensibilidad real del receptor tierra y ganancia real de Yagi.
4. Validar margen con simulación de elevación variable en STK o similar.

## Implicancias
- `03_Power/Power Budget.md` — UHF TX actualizado a 1.5 W eléctrico
- `03_Power/EPS Sizing.md` — pico máximo soportable actualizado
- `00_MVP/MVP v2.2.md` — baseline UHF y notas energéticas
- `04_Communications/` — este ADR es el punto de partida del link budget formal