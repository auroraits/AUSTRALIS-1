# EPS Bench Testing

## Objetivo
Definir un procedimiento corto y repetible para validar en banco el arreglo solar de prototipo (2×1.2 W), protecciones y sensado con INA219.

## Bench COTS Policy (validation scope)
- Bench setup in this document is COTS and for validation workflow only.
- Architecture alignment is mandatory: voltage topology, battery chemistry, and charging philosophy must match planned flight EPS.
- Migration path is required from bench module to custom flight-grade PCB; bench modules are not flight-ready unless explicitly qualified.

### Component Selection Rule
- Bench Option (COTS)
- Flight Architecture Equivalent
- Migration Path

> Alcance: este procedimiento aplica a banco. El cargador CN3065 se usa como cargador lineal de prueba (no MPPT). La arquitectura de vuelo recomendada sigue siendo MPPT.
> Bench MPPT modules (e.g., BQ24650 boards, CN3791 modules) are used for rapid prototyping.
> Final flight EPS will transition to custom PCB implementations derived from the same controller IC families.
> No bench module is considered flight-ready unless explicitly qualified.

## 1) Medición inicial de paneles (ambiental)
1. Colocar cada panel en condiciones de iluminación estables (sol o lámpara fija).
2. Medir **Voc** (voltaje en circuito abierto) de cada panel con multímetro.
3. Medir **Isc** (corriente de cortocircuito) de cada panel en escala de corriente adecuada y por pocos segundos.
4. Registrar condiciones: hora, tipo de fuente de luz, distancia/ángulo, temperatura ambiente.

## 2) Conexión en paralelo con diodos Schottky
1. Usar un diodo Schottky (1N5819 o SS34) por panel, en serie con el positivo de cada rama.
2. Unir salidas de ambos diodos en un nodo común **SOLAR_BUS+**.
3. Unir negativos de paneles al retorno común **GND**.
4. Verificar polaridad y caída en diodo antes de conectar el cargador.

## 3) Ubicación del fusible 1 A T
1. Colocar el fusible plástico **1 A T** en serie sobre la línea positiva principal desde **SOLAR_BUS+** hacia la entrada del cargador/control de banco.
2. Instalarlo lo más cerca posible de la fuente (nodo de salida de paneles en paralelo).
3. Validar continuidad del portafusible y repuesto disponible antes de energizar.

## 4) Instrumentación con INA219
1. Instalar un INA219 en la rama solar para medir voltaje/corriente de entrada al banco.
2. Instalar un segundo INA219 en la rama de carga (hacia carga electrónica o subsistema bajo prueba).
3. Configurar dirección I2C sin conflicto y registrar timestamp + V + I + P.
4. Ejecutar logging durante al menos 10–15 minutos por condición de iluminación.

## 5) Protocolo con lámparas (si no hay sol)
1. Usar lámpara(s) fija(s) con distancia constante y soporte mecánico para repetir geometría.
2. Definir niveles de prueba (ejemplo: 20 cm, 40 cm, 60 cm) o niveles de intensidad equivalentes.
3. En cada nivel: registrar Voc, Isc y luego curva de operación con carga conectada.
4. Mantener tiempo de estabilización térmica entre corridas y documentar cambios de temperatura.

## Registro mínimo recomendado
- Fecha/hora y operador.
- Configuración de paneles, diodos y fusible.
- Fuente de iluminación y geometría.
- Mediciones Voc/Isc por panel.
- Logs INA219 (solar y carga).
- Observaciones de estabilidad (caídas, disparo de fusible, cableado caliente).
