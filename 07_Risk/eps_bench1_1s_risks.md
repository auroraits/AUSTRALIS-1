# EPS Bench1 1S — Risk Matrix

**Review date:** 2026-02-18
**Scope:** Riesgos técnicos del banco EPS 1S y su transición a diseño custom.

## Risk matrix

| ID | Riesgo | Prob. | Impacto | Mitigación | Trigger condition |
|---|---|---|---|---|---|
| EPS-B1-01 | Uso de CN3065 sin MPPT real reduce representatividad energética | M | M | Documentar explícitamente limitación y validar transición a cargador buck solar en KiCad | Diferencia >TBD entre estimación y medición de energía útil |
| EPS-B1-02 | Conexión incorrecta en BMS (cargas/cargador sobre B+/B−) anula protección | M | H | Regla obligatoria de conexión en `P+/P−` + checklist de cableado | Sobrecorriente o undervoltage sin corte esperado |
| EPS-B1-03 | Módulos COTS introducen dispersión eléctrica no controlada | M | M | Ensayos por lote y márgenes conservadores; migrar a ICs dedicados | Variación de rail fuera de tolerancia TBD |
| EPS-B1-04 | Falta de telemetría integrada limita diagnóstico de fallos | H | M | Planificar telemetría de V/I/T en `EPS_Flight_Like` | Falla intermitente sin datos de causa |
| EPS-B1-05 | Interpretar banco como diseño de vuelo genera decisiones erróneas | M | H | Etiquetado "Bench Only" y ADR de estrategia COTS→Flight | Uso de BOM bench como baseline de vuelo |
| EPS-B1-06 | Vmp del panel cae por debajo de umbral de entrada del CN3065 bajo carga real | Alta | Media | Medir curva I-V real del panel bajo carga; verificar Vmp > 4.4 V (mínimo CN3065) antes de pruebas de carga completa. Si Vmp < 4.4 V, reducir carga de prueba o usar CN3791 para el banco. | Caída de tensión de panel por debajo de 4.4 V durante carga de batería |

## Riesgo residual
- Nivel residual global: **Medio** (hasta completar migración a `EPS_Flight_Like`).

## Referencias
- `03_Power/EPS_Bench1_1S.md` (canónico).
- `docs/EPS/EPS_Bench1_1S.md` (histórico).
- `08_Decisions/ADR-20260218-eps-bench1s-cots-to-custom-flight-pcb.md`.
