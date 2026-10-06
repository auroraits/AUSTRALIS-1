# ADR-20261005-repository-authority-and-historical-migration

- **Fecha:** 2026-10-05
- **Estado:** Accepted
- **Trazabilidad:** extiende `ADR-20260313-gobierno-documental`

## Contexto

AUSTRALIS conserva dos historias de trabajo. `auroraits/AUSTRALIS-1` contiene
la configuración pública reconciliada y validada por CI, mientras que
`auroraits/DIY-Nanosat` conserva historia privada y fue archivado. Algunos
runbooks y memorias todavía denominaban canónico al repositorio histórico, y el
checkout local de ese repositorio contiene trabajo divergente no consolidado.

Sin una autoridad explícita, la cronología de una rama, un clon local o un
archivo más nuevo podía interpretarse erróneamente como precedencia técnica.
También existía el riesgo de sincronizar árboles completos y reintroducir
decisiones superseded, artefactos no publicables o historia privada.

## Decisión

1. `auroraits/AUSTRALIS-1`, rama `main`, es la única autoridad de configuración
   técnica vigente de AUSTRALIS.
2. Un cambio adquiere autoridad solamente después de revisión y merge mediante
   pull request hacia `main`. Ramas, clones, mirrors y workspaces son propuestas
   o copias operativas.
3. Toda revisión, ensayo, claim web o release debe identificar el commit SHA
   completo de `AUSTRALIS-1` que utilizó.
4. `auroraits/DIY-Nanosat` permanece archivado y se clasifica como `Historical
   Snapshot`. Sus ramas y cambios locales no son normativos.
5. No se permite fusionar, espejar, rebasear o sincronizar en bloque la historia
   o el árbol de `DIY-Nanosat` con `AUSTRALIS-1`.
6. El material histórico útil puede migrarse únicamente mediante un pull
   request acotado desde la baseline vigente. Debe identificar origen y commit
   cuando exista, y volver a evaluarse contra ADRs, requisitos, interfaces,
   riesgos, provenance, licencias, seguridad y validadores actuales.
7. Evidencia, métricas y estados de verificación históricos no se heredan por
   analogía; requieren configuración y evidencia controlada vigentes.
8. La mayor antigüedad o novedad de un artefacto histórico no le otorga
   precedencia. Los conflictos se resuelven con la jerarquía documental vigente
   de AUSTRALIS.

## Alternativas consideradas

- **Mantener `DIY-Nanosat` como repositorio canónico privado y exportar mirrors:**
  rechazada; preserva dos autoridades, dificulta la auditoría y expone a
  contaminación por historia privada.
- **Sincronizar ambos repositorios bidireccionalmente:** rechazada; no existe una
  resolución determinística de conflictos y puede reintroducir decisiones o
  artefactos descartados.
- **Borrar el repositorio histórico:** rechazada; elimina trazabilidad y trabajo
  potencialmente recuperable.

## Tradeoffs y riesgos

- La migración selectiva requiere revisión manual y puede ser más lenta que una
  copia masiva.
- El repositorio histórico local debe preservarse sin limpieza destructiva hasta
  clasificar el trabajo útil.
- `main` necesita controles efectivos de revisión y CI; hasta habilitar
  protección server-side, el proceso de pull request sigue siendo obligatorio.

## Implicancias

- Actualizar `REPOSITORY_GOVERNANCE.md`, `README.md`, `AGENTS.md` y
  `PUBLIC_RELEASE_PROCESS.md`.
- Corregir runbooks, memoria durable y automatizaciones que todavía apunten al
  repositorio histórico como fuente vigente.
- No cambia ninguna decisión de misión, hardware o software ni verifica
  requisitos técnicos.
