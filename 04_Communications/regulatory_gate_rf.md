# Gate regulatorio RF — AUSTRALIS-1

**Revisión:** 2026-07-27
**Estado:** Active — gates abiertos; no constituye asesoramiento legal
**Trazabilidad:** `08_Decisions/ADR-20260727-rf-regulatory-command-security-baseline.md`, ENACOM, IARU y UIT

## 1) Regla de operación

**Ausencia de autorización no equivale a autorización.** Hasta cerrar el gate
correspondiente con evidencia escrita:

- no se transmite hacia o desde el satélite;
- los ensayos son conducidos, apantallados o realizados bajo autorización
  experimental específica;
- ninguna frecuencia, potencia, callsign o modo se presenta como asignado;
- SatNOGS no sustituye licencia, coordinación ni filing.

El estado `RX-only` del satélite en 915–928 MHz no autoriza a una estación
terrestre a dirigir emisiones Tierra→espacio.

## 2) Estado de gates

| Gate | Estado | Bloquea | Evidencia mínima de cierre |
|---|---|---|---|
| `REG-UHF-AMATEUR` | Open | Todo UHF radiado operacional | dictamen/permiso ENACOM, responsable habilitado, frecuencia y emisión autorizadas |
| `REG-IARU` | Open | Frecuencia amateur-satellite | coordinación IARU documentada |
| `REG-ITU` | Open | Operación de estación espacial | presentación/coordinación/notificación por administración nacional |
| `REG-LORA-915` | Open / no autorizado por evidencia actual | LoRa Tierra→espacio B1/B2 | dictamen escrito ENACOM o autorización experimental específica |
| `REG-CONTENT` | Open | Downlink/uplink controlado | reglas escritas sobre identificación, contenido, autenticación y confidencialidad |
| `REG-GROUND` | Open | TX desde estación propia | licencia, sitio, operador, potencia, antena, procedimiento e interlocks |

Solo la autoridad competente puede cambiar un gate regulatorio a cerrado. Una
ADR, una prueba técnica, un radio club o este documento no pueden hacerlo.

## 3) UHF amateur-satellite 435–438 MHz

El rango de diseño es **435–438 MHz**, sujeto a coordinación. `435.000 MHz`
está en el borde inferior y no se usa como centro literal: sidebands, tolerancia
de oscilador y Doppler podrían salir del segmento.

El expediente debe definir, como mínimo:

- entidad responsable y persona con categoría habilitante;
- propósito experimental/no comercial compatible con el servicio;
- estación espacial y estaciones terrenas;
- frecuencia central coordinada, ancho ocupado y clase de emisión;
- potencia/EIRP, antenas, polarización y cobertura;
- identificación/callsign de toda emisión;
- modulación, coding, framing y decoder públicamente documentados cuando lo
  exija el servicio;
- contenido permitido;
- mecanismo de autenticación sin asumir cifrado/confidencialidad;
- coordinación IARU;
- datos del Apéndice 4 UIT y trámite por la administración nacional;
- plan de cese, interferencia y control operacional.

La coordinación IARU, la autorización ENACOM y el proceso UIT son actividades
relacionadas pero no intercambiables.

## 4) Identificación y contenido

Mientras el enlace se encuadre en amateur-satellite:

- todas las emisiones, no solo `PUBLIC_BEACON`, deben incorporar la
  identificación exigida;
- `CONTROLLED_DOWNLINK` significa que lo programa/opera una estación
  autorizada; no significa secreto;
- `PRIVATE_UPLINK` significa operador autorizado; no significa que el canal
  sea confidencial;
- waveform, framing y decoder no se mantienen cerrados si el marco aplicable
  exige comunicación inteligible y públicamente documentada;
- datos que necesiten confidencialidad no se transmiten hasta contar con un
  servicio y autorización compatibles.

La autenticación criptográfica sin cifrado deja comando y cabeceras en claro,
pero impide que un tercero genere un tag válido. Este enfoque debe confirmarse
por escrito con ENACOM; no se presume que cualquier suite sea aceptable.

## 5) LoRa 915–928 MHz Tierra→espacio

La Cuadro de Atribución de Bandas de Frecuencias de la República Argentina
(CABFRA) vigente consultada no demuestra una atribución
amateur-satellite/Earth-to-space para 902–928 MHz equivalente a la existente en
UHF amateur-satellite.

Una emisión B2 calculada con TLE y dirigida al paso del satélite es una
comunicación Tierra→espacio, aunque use hardware LoRa de corto alcance. No se
trata como una emisión terrestre incidental.

Por lo tanto:

- B1 always-on y B2 pass-aware están deshabilitados para operación radiada;
- la clase de nodo, AU915 o una homologación de dispositivo terrestre no
  prueban autorización espacial;
- potencia, duty cycle o antena menor no eliminan el gate;
- el objetivo de paquetes “originados en Buenos Aires” debe mantenerse
  bloqueado o trasladarse a banda/servicio autorizado;
- un eventual gateway dedicado también requiere autorización.

### 5.1 Consulta escrita requerida

La presentación a ENACOM debe describir sin eufemismos:

1. banda/canal propuesto;
2. dirección Tierra→espacio;
3. destinatario orbital identificado;
4. sitio y número de nodos;
5. potencia conducida, EIRP y antena;
6. waveform, bandwidth, duty cycle y ventanas;
7. uso de TLE/predicción;
8. contenido, identificación y autenticación;
9. objetivo experimental;
10. alternativas de banda/servicio.

El cierre debe conservar documento, expediente, fecha, alcance, condiciones y
vigencia; una respuesta verbal no basta.

## 6) Checklist de evidencia

Cada gate cerrado debe enlazar artefactos inmutables:

- `AuthorityArtifactID`;
- organismo/emisor;
- número de expediente/documento;
- alcance técnico exacto;
- vigencia y condiciones;
- responsable del proyecto;
- hash del archivo local controlado fuera del mirror si contiene datos
  sensibles;
- impacto en requisitos, ADR, link budget, plan de frecuencia y CONOPS.

Los documentos privados pueden permanecer fuera del mirror, pero el repositorio
debe registrar su ID, estado y alcance sin publicar datos personales.

## 7) Orden de trabajo

1. Nombrar entidad y responsable legal (`TBD`).
2. Abrir consulta ENACOM para `REG-LORA-915`.
3. Preparar paquete técnico UHF preliminar sin frecuencia fija.
4. Iniciar coordinación IARU con suficiente antelación.
5. Coordinar filing UIT mediante la administración nacional.
6. Obtener reglas escritas de contenido/autenticación.
7. Actualizar diseño y pruebas según las condiciones emitidas.
8. Autorizar TX radiado solo después del sign-off operacional.

## 8) Fuentes primarias

- ENACOM, Resolución 3635-E/2017, Reglamento General de Radioaficionados:
  https://www.enacom.gob.ar/multimedia/noticias/archivos/201711/archivo_20171107072645_3234.pdf
  Secciones de control: §§1.5.2, 1.5.8–1.5.9, 9.14, 13.3.9 y 13.4.2.
- Argentina, Resolución ENACOM 1186/2024:
  https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-1186-2024-406719/texto
- ENACOM, CABFRA edición 2024 actualizada 21-10-2025:
  https://www.enacom.gob.ar/multimedia/noticias/archivos/202511/archivo_20251104082327_1428.pdf
  Tablas consultadas: pp. 151, 159 y 182–188.
- IARU, *Amateur Radio Satellites — Short Information Paper*:
  https://www.iaru.org/wp-content/uploads/2019/12/short_info_paper.pdf
- ITU-R, soporte regulatorio para small satellites:
  https://www.itu.int/en/ITU-R/space/support/smallsat/Pages/default.aspx

## 9) Referencias internas

- `04_Communications/rf_subsystem_overview.md`
- `04_Communications/link_budget_uhf_preliminary.md`
- `04_Communications/link_budget_lora_uplink_preliminary.md`
- `04_Communications/uhf_command_security_protocol.md`
- `04_Communications/satnogs_public_beacon_architecture.md`
