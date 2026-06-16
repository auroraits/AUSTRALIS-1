# ADR-20260313-gobierno-documental

- **Fecha:** 2026-03-13
- **Estado:** Accepted

---

## Contexto

El repositorio DIY Nanosat carecía de una metodología documental formal que definiera claramente la jerarquía de documentos, los estados permitidos, las reglas de propagación de cambios y la política de los archivos `AGENTS.md`. Esto generaba riesgo de que documentos `Draft` o `Proposed` se citaran como normativos, o que los agentes (humanos o IA) aplicaran precedencias incorrectas.

---

## Decisión

Se adopta una metodología documental global con los siguientes elementos bloqueados:

1. **Jerarquía de precedencia documental:** ADR `Accepted` → `00_MVP/MVP v2.2.md` → `SYSTEM_BASELINE.md` → documentación de subsistema → `Draft`/`Proposed`/`Preliminary` → históricos.

2. **Estados documentales explícitos:** `Accepted`, `Baseline`, `Active`, `Draft`, `Proposed`, `Preliminary`, `Superseded`, `Historical Snapshot`.

3. **`AGENTS.md` raíz** (`/AGENTS.md`): documento de gobierno máximo para agentes. Todos los `AGENTS.md` de subsistemas heredan y no pueden contradecir las reglas raíz.

4. **Cabecera mínima** para documentos clave: `Revisión`, `Estado`, `Trazabilidad`.

5. **Definición de "Hecho" documental** explícita: 7 criterios listados en `AGENTS.md`.

6. **Regla de propagación de cambios** documentada en `architecture.md` y `AGENTS.md`.

---

## Alternativas consideradas

1. **Status quo** (sin metodología formal): rechazada. El riesgo de inconsistencias escala con la cantidad de agentes y sesiones de trabajo.

2. **Wiki externa**: rechazada. El repositorio es la fuente de verdad; la metodología debe vivir en el repo.

3. **Solo actualizar README**: rechazada. Insuficiente para definir jerarquía y estados.

---

## Tradeoffs / riesgos

- A favor: reduce ambigüedad, mejora trazabilidad, facilita trabajo de agentes IA.
- En contra: overhead inicial de actualización de documentos.
- Riesgo residual: que los `AGENTS.md` de subsistemas no se actualicen oportunamente. Mitigación: regla explícita de armonización.

---

## Implicancias (archivos actualizados)

- `AGENTS.md` (raíz) — creado/actualizado.
- `architecture.md` — secciones 2, 3, 4, 5 actualizadas.
- `SYSTEM_BASELINE.md` — referencia a `AGENTS.md` agregada.
- `README.md` — sección de política de consistencia actualizada.
- Todos los `AGENTS.md` de subsistemas — armonización pendiente.
