# ADR-20260212-move-embedded-under-05-software

## Contexto
El repositorio organiza contenido por subsistema. El firmware embebido para pruebas de telemetría 433 MHz estaba en `embedded/` en raíz, fuera del dominio `05_Software/`, lo que dificultaba la trazabilidad entre software de vuelo/terreno, documentación y evolución de herramientas de ground segment.

## Decisión
Mover el árbol de firmware embebido desde raíz a `05_Software/embedded/` usando `git mv` para preservar historial.

Además, se incorpora `05_Software/GroundTelemetryDashboard/` como solución .NET 8 para visualización de telemetría de estación terrena en tiempo real (serial COM + SignalR + Blazor Server).

## Alternativas consideradas
1. Mantener `embedded/` en raíz y documentar excepción.
2. Crear carpeta nueva paralela (`05_Software/Firmware/`) y duplicar/migrar contenido.
3. **Decisión adoptada:** mover sin duplicar a `05_Software/embedded/` para alineación directa con arquitectura por subsistemas y mínima disrupción.

## Tradeoffs / riesgos
- **Pros:** mayor coherencia arquitectónica, rutas consistentes, ownership claro del subsistema software.
- **Contras:** necesidad de actualizar documentación y scripts que referencien rutas antiguas.
- **Riesgos:** confusión temporal de rutas mitigada con actualización explícita de `README`, `architecture`, MVP y docs de telemetría.

## Implicancias (archivos a actualizar)
- `architecture.md`
- `README.md`
- `docs/TELEMETRY_433_README.md`
- `00_MVP/MVP v2.0.md`
- `05_Software/AGENTS.md`

## Estado
Accepted
