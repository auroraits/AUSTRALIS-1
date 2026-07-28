# ADR-20260727-rf-regulatory-command-security-baseline

- **Fecha:** 2026-07-27
- **Estado:** Accepted
- **Supersede:** ADR-20260218 (link budget UHF), ADR-20260220 (LoRa slotted),
  ADR-20260313 (máscara UHF) y ADR-20260704 (perfiles SatNOGS)

## Contexto

Los presupuestos RF anteriores contienen geometría y márgenes no demostrados.
El hecho de que el satélite sea RX-only en 915 MHz no autoriza por sí solo una
transmisión intencional Tierra→espacio. Además, comandos y prompts tenían
efectos operacionales sin protocolo verificable de autenticación y anti-replay.

## Decisión

1. **UHF:** la frecuencia coordinada queda `TBD` dentro de la atribución y
   autorización aplicables; `435 MHz` no se usa como centro literal congelado.
   Modulación, bitrate, potencia, máscara y hardware permanecen candidatos.
2. **LoRa Tierra→espacio en 915 MHz:** objetivo experimental condicionado a
   respuesta escrita de ENACOM/administración competente. RX-only orbital no
   resuelve la autorización del transmisor terrestre. Si no resulta autorizable,
   se cambiará banda/servicio, se solicitará autorización experimental o se
   redefinirá el objetivo secundario.
3. Todo enlace de comando o carga de prompts deberá proporcionar autenticidad,
   integridad y anti-replay. CRC/hash no autenticado no satisface este requisito.
4. El protocolo deberá definir tag criptográfico, contador monotónico
   persistente, `key_epoch`, ventana anti-replay, roles, rotación/recuperación,
   separación upload/activate y ACK autenticado. Algoritmo y claves quedan TBD
   hasta threat model y revisión regulatoria.
5. No se promete confidencialidad ni “privacidad por decoder cerrado”. El beacon
   público será documentado y compatible con las obligaciones regulatorias.
6. SatNOGS permanece receive-only y sin acceso a PTT, claves o control.
7. Link budgets separados uplink/downlink, patrón integrado, Doppler/waveform,
   PER/BER objetivo, incertidumbre, EIRP, G/T, coexistencia/EMC y mediciones son
   obligatorios antes de Gate COMMS.

## Gates regulatorios

- No fijar bandplan ni radiar uplink orbital sin ruta ENACOM/IARU/ITU
  documentada y responsable legal habilitado.
- No aceptar comandos/prompt uplink sin pruebas negativas de replay, reset,
  pérdida de energía, clave errónea, frame truncado y rollback.

## Fuentes primarias

- ENACOM, Reglamento General de Radioaficionados, Resolución 3635-E/2017:
  <https://www.enacom.gob.ar/multimedia/noticias/archivos/201711/archivo_20171107072645_3234.pdf>
  SHA-256 de la copia consultada:
  `53067093cd8cb9b9792a44ca5c5a8890a4d4e44b865c389a4758448ab7ae239a`.
- ENACOM, modificación 1186/2024:
  <https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-1186-2024-406719/texto>
- ENACOM, CABFRA edición 2024 actualizada el 21-10-2025, pp. 151, 159
  y 182–188:
  <https://www.enacom.gob.ar/multimedia/noticias/archivos/202511/archivo_20251104082327_1428.pdf>
  SHA-256 de la copia consultada:
  `5240087c31abb8563e04bc5a32f4d600d0925ee0cba94559afe4255a952aa597`.
- IARU, Amateur Satellite Frequency Coordination:
  <https://www.iaru.org/wp-content/uploads/2019/12/short_info_paper.pdf>
  SHA-256 de la copia consultada:
  `791a9c681c99ac1bbc9d5e2d5ee16e90d1c2a00ca57de375d81a85b270392e74`.
- ITU-R, Support for small satellites:
  <https://www.itu.int/en/ITU-R/space/support/smallsat/Pages/default.aspx>

Copias consultadas el 2026-07-27. Toda cita se reconfirmará contra la revisión
vigente y con especialista/autoridad antes de SRR o filing; esta ADR no
constituye asesoramiento legal.
