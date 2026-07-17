# ADR-20260710-diy-low-cost-maker-latam-design-policy

- **Fecha:** 2026-07-10
- **Estado:** Accepted

---

## Contexto

AUSTRALIS-1 es un proyecto DIY Nanosat / CubeSat 1.5U de bajo costo, publicado para colaboracion abierta no comercial y reproducibilidad educativa. El proyecto necesita evitar decisiones de diseno que dependan de componentes exoticos, proveedores inaccesibles o hardware dificil de conseguir en Latinoamerica durante la etapa maker/bench.

El baseline ya separa capas `Bench`, `Flight-Like` y `Flight`. Esta ADR fija la politica transversal de seleccion para que la documentacion, la BOM y los trade studies mantengan el enfoque DIY, low cost y reproducible.

---

## Decision

Se adopta como politica de diseno:

1. **DIY first:** el diseno debe favorecer integracion, ensayo, reparacion y aprendizaje con herramientas maker razonables antes de escalar a hardware flight-like o flight.
2. **Low cost with traceability:** el costo bajo es un criterio de arquitectura, pero no reemplaza requisitos de seguridad, trazabilidad, medicion ni compliance.
3. **Open publication:** codigo, firmware, scripts, documentacion, datasets de ejemplo, CAD/PCB publicables y procedimientos deben mantenerse publicados en el mirror publico cuando no expongan secretos, datos privados, material controlado o restricciones de terceros. La licencia publica vigente sigue siendo source-available no comercial segun `LICENSE.md`.
4. **Maker/LATAM availability:** para cada item nuevo de BOM se debe preferir al menos una clase de componente maker/COTS ampliamente disponible en Argentina o Latinoamerica, o por canales internacionales comunes con alternativa local razonable.
5. **No SKU lock-in without reason:** los requisitos deben definir clases de componentes cuando sea posible, no SKUs unicos. Si se fija un SKU, el documento debe explicar por que y registrar riesgo de supply chain.
6. **Bench is not flight:** los componentes maker son validos para banco, FlatSat, EGSE y prototipos. Cualquier migracion a hardware de vuelo requiere evidencia, analisis de ambiente/compliance y, si cambia arquitectura, ADR.
7. **Exceptions documented:** si un componente no es barato, maker-accessible o disponible en LATAM, la excepcion debe quedar marcada en BOM/riesgos/trade study con mitigacion.

---

## Alternativas consideradas

1. **Optimizar solo por performance:** rechazada. Puede producir un diseno tecnicamente interesante pero dificil de construir, probar y sostener localmente.
2. **Fijar SKUs maker especificos:** rechazada como regla general. Mejora la compra inicial, pero genera fragilidad ante descontinuacion o stock variable.
3. **Separar "maker" y "flight" sin puente:** rechazada. El proyecto necesita una ruta trazable `COTS bench -> flight-like -> flight`, no dos disenos inconexos.
4. **Definir clases de componentes con disponibilidad local/regional y excepciones trazadas** (elegida).

---

## Consecuencias

- La matriz de requisitos debe incluir directrices de reproducibilidad, apertura y disponibilidad LATAM.
- La BOM debe registrar proveedor/region y mantener alternativas cuando el componente elegido tenga riesgo de disponibilidad.
- Los trade studies deben puntuar disponibilidad local/regional, costo, reemplazabilidad, documentacion y riesgo de lock-in.
- Los documentos publicos deben evitar declarar "flight-ready" a componentes maker o de banco sin evidencia.
- Las decisiones de flight hardware siguen sujetas a compliance, ambiente, integrador, ensayos y ADRs existentes.

---

## Implicancias (archivos actualizados)

- `SYSTEM_BASELINE.md`
- `architecture.md`
- `README.md`
- `01_Mission/mission_definition.md`
- `01_Mission/requirements_matrix.md`
- `01_Mission/compliance_matrix.md`
- `06_Costs/bom_overview.md`

