# Satellite RF KiCad — placeholder, no design

**Revisión:** 2026-07-27
**Estado:** Placeholder / not fabricable

Los archivos KiCad de este directorio no contienen un diseño RF funcional:

- esquemático sin circuito/netlist útil;
- PCB sin outline, footprints, pads, tracks, vias ni zones;
- sin BOM, stackup, netclasses, constraints ni fabrication outputs;
- sin front-end UHF, receptor LoRa, filtros, reloj, switching o interfaces.

No deben usarse para:

- cotizar/fabricar;
- ejecutar ERC/DRC como evidencia de cierre;
- estimar masa, potencia, sensibilidad, EMC o desempeño;
- afirmar que existe una PCB RF Flight-Like.

## Criterios para reemplazar el placeholder

1. Hardware UHF y LoRa seleccionado mediante decisiones trazables.
2. Frecuencia/canalización y requisitos regulatorios definidos.
3. Schematics revisados con interfaces, protección y power gating.
4. BOM completa sin dependencias EOL críticas.
5. Stackup, impedancias, RF layout y constraints documentados.
6. ERC/DRC sin exclusiones no justificadas.
7. Gerbers/drill/position/assembly y release manifest versionados.
8. Revisión independiente del diseño.
9. Plan de bring-up, RF calibration, EMC, OTA y environmental V&V.

Hasta entonces, el directorio se conserva solo para mantener la ubicación
prevista del futuro proyecto.
