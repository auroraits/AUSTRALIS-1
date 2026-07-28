# EPS Bench Testing

**Revisión:** 2026-07-27
**Estado:** Draft — Bench 1S exploratory only

## Objetivo
Definir un procedimiento repetible para caracterizar el arreglo de banco
(dos paneles nominales de 1.2 W), sus protecciones y el sensado INA219. Este
procedimiento no valida el array, cargador, batería, BMS ni EPS de vuelo.

## Bench COTS Policy (validation scope)
- El banco COTS 1S existe para desarrollar método, logging y fault handling.
- No tiene que replicar la topología 2S de vuelo y no recibe crédito de
  compatibilidad, heritage ni calificación.
- Toda extrapolación exige nueva asignación de requisitos, análisis y ensayo
  sobre la configuración Flight-Like exacta.

### Component Selection Rule
- identificar módulo/lote y configuración Bench;
- registrar magnitud medida, incertidumbre y limitaciones;
- no designar un “equivalente de vuelo” sin trade y ADR independientes.

> El CN3065 y cualquier módulo MPPT COTS se usan solo como instrumentos de
> prototipado. No seleccionan familia de controlador ni camino de migración.
> Cargador, MPPT por cara/string, celdas, BMS y PCB Flight-Like permanecen TBD.

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

## 3) Selección y ubicación de protección de corriente
1. Calcular fuse/current-limit desde Isc medido, corriente admisible de
   cableado/conectores y límites del cargador; registrar tolerancia y rationale.
2. Un fusible **1 A T** es solo una opción de banco y no se instala sin que el
   cálculo anterior demuestre coordinación.
3. Colocar la protección seleccionada en serie sobre la línea positiva principal desde **SOLAR_BUS+** hacia la entrada del cargador/control de banco.
4. Instalarla lo más cerca posible de la fuente (nodo de salida de paneles en paralelo).
5. Validar continuidad y repuesto antes de energizar.

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
