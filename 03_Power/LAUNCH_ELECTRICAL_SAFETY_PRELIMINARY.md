# Seguridad eléctrica de lanzamiento preliminar — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Preliminary / NOT IMPLEMENTED
**Fuente:** CubeSat Design Specification Rev. 14.1, §§2.3–2.4; sujeto a
requisitos adicionales del ICD del integrador

## 1. Dictamen

El proyecto EPS Flight-Like actual no implementa las inhibiciones mínimas de
lanzamiento y no es fabricable. La ausencia del ICD final puede bloquear la
ubicación, interfaz o aceptación, pero no autoriza omitir los mínimos ya
publicados por el CDS.

Fuente primaria:

- *CubeSat Design Specification Rev. 14.1*, Cal Poly SLO, pp. 14–15.
- <https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS+REV14_1+2022-02-09.pdf>
- SHA-256 de la copia consultada:
  `221fbbbd4f632b16f3e219d1a5e2c2b04e1998c12025b793e6dfc6181af66b5d`.

La revisión, página, cláusula y checksum deben conservarse en la configuración
documental controlada.

## 2. Mínimos de diseño

| ID | Base CDS Rev. 14.1 | Requisito preliminar AUSTRALIS-1 |
|---|---|---|
| LCH-EPS-01 | §2.3.1 | Todas las funciones alimentadas permanecen apagadas hasta la eyección |
| LCH-EPS-02 | §2.3.2 | Al menos un deployment switch desconecta eléctricamente las funciones |
| LCH-EPS-03 | §2.3.5 | Existe Remove Before Flight (RBF) accesible y verificable |
| LCH-EPS-04 | §2.3.6 | El pack incorpora protección contra desbalance de celdas |
| LCH-EPS-05 | §2.3.7 | Existen al menos tres inhibiciones RF independientes |
| LCH-EPS-06 | §2.3.8 | Existen al menos tres inhibiciones independientes para impedir la liberación inadvertida de cualquier estructura desplegable |
| LCH-EPS-07 | §2.4.4 | Ningún desplegable se activa antes de 30 min desde la eyección |
| LCH-EPS-08 | §2.4.5 | Ningún transmisor se habilita antes de 45 min desde la eyección |

El ICD puede endurecer cantidades, independencia, localización, niveles,
ensayos o tiempos. Una interpretación diferente debe quedar respaldada por
una cláusula controlada o waiver escrito del integrador.

## 3. Independencia y estado seguro

Para cada inhibición se documentarán:

- principio físico y señal controlada;
- independencia frente a las demás inhibiciones;
- estado por defecto sin energía;
- efecto de corto, abierto, rebote, stuck-on y stuck-off;
- comportamiento durante integración, lanzamiento, eyección y reset;
- telemetría y prueba de estado;
- autoridad y secuencia de habilitación;
- imposibilidad de bypass por una recomendación IA.

Un contador de software no sustituye una inhibición hardware cuando el
CDS/ICD exige independencia. CRC, watchdog o comando terrestre tampoco
sustituyen un RBF o deployment switch.

## 4. Arquitectura a cerrar

El esquema y la BOM deberán incluir explícitamente:

- RBF y conectores/retornos asociados;
- deployment switch(es) y acondicionamiento;
- inhibiciones RF y de desplegables;
- lógica de tiempo desde eyección con fuente y tolerancia definidas;
- high-side switches/eFuses con default-off;
- protección del pack, balanceo, fusible y charge inhibit;
- señales de PGOOD/FAULT e instrumentación;
- mecanismo de ensayo que no invalide la independencia.

Todos los dominios —OBC, RF, IA/CM5, science, ADCS y heaters— deben tener un
estado de pre-ejection definido y verificable.

## 5. Verificación

| ID | Verificación | Criterio de aceptación |
|---|---|---|
| LCH-VV-01 | Revisión esquemática/FMEA | Cada fallo simple conserva el estado exigido o queda aceptado por el ICD |
| LCH-VV-02 | Continuidad pre-ejection | Ninguna función alimentada fuera de los estados permitidos |
| LCH-VV-03 | RBF/deployment switch | Apertura/cierre y rebote dentro de límites, sin bypass |
| LCH-VV-04 | Tres inhibiciones RF | Cada inhibición se prueba por separado y en combinación |
| LCH-VV-05 | Tres inhibiciones de desplegables | El conjunto cumple independencia y bloquea toda liberación inadvertida |
| LCH-VV-06 | Temporización | Despliegue ≥30 min y RF ≥45 min en tolerancia worst-case |
| LCH-VV-07 | Reset/brownout | No adelanta timers ni habilita cargas/transmisores |
| LCH-VV-08 | Post-ambiente | Todos los estados e inhibiciones funcionan después de vibración/TVAC |

No se declarará readiness con estos ítems `Open` o
`Blocked by Integrator`.
