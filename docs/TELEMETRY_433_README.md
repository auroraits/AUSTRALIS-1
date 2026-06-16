# TELEMETRY 433 MHz — ESP32-S3 TX + Arduino UNO RX

## 1) Hardware validado

IMU usada: **GY-521 (MPU6050)** por I2C.

- Address detectado en TX: `0x68` (AD0=0) o `0x69` (AD0=1).
- Alimentación del módulo: `3V3`.
- El TX imprime por Serial: `#SENSOR:MPU6050 addr=0x..`.

## 2) Convenciones de frame (importante)

- Quaternion transmitido: **`qw,qx,qy,qz`** (`q0..q3`).
- Three.js aplica: `set(qx,qy,qz,qw)`.
- En TX existe un bloque de remapeo editable para alinear frame sensor->body:
  - `BODY_AX_SIGN/BODY_AY_SIGN/BODY_AZ_SIGN`
  - `BODY_GX_SIGN/BODY_GY_SIGN/BODY_GZ_SIGN`

## 3) Inicialización MPU6050 en firmware TX

- Wake: `PWR_MGMT_1(0x6B)=0x00`.
- DLPF: `CONFIG(0x1A)=0x03` (~44/42 Hz).
- Gyro range: `GYRO_CONFIG(0x1B)=0x00` (±250 dps).
- Accel range: `ACCEL_CONFIG(0x1C)=0x00` (±2g).

Unidades para fusión:
- `accel_g = raw / 16384.0`
- `gyro_rad_s = (raw / 131.0) * PI/180`

## 4) Calibración

### 4.1 Gyro bias (boot)
En `setup()` se promedian muestras en reposo y se calcula bias (`gx,gy,gz` en rad/s).

### 4.2 Recalibración runtime
Por Serial del TX:
- enviar `CAL` o `RECAL` + Enter.

TX responde:
- `#CAL,gyro_bias=...`

### 4.3 Zero visual (dashboard)
El botón **Set Reference (Zero)** define la pose actual como identidad visual:
- `q_display = inverse(q_ref) * q_current`

## 5) Paquete RF y compatibilidad

### V3 (actual)
Campos en struct:
- `magic='T'`, `version=3`, `sensor_type=1(MPU6050)`
- `seq,t_ms,ax,ay,az,gx,gy,gz,q0,q1,q2,q3,dt_ms`

### Compatibilidad RX
UNO acepta:
- V3 (versionado)
- V2 (sin header)
- V1 (legacy sin quaternion, emite identidad `1,0,0,0`)

CSV de salida UNO:
`seq,t_ms,ax,ay,az,gx,gy,gz,q0,q1,q2,q3`

## 6) Frecuencias

- Filtro Madgwick: ~100 Hz.
- Envío RF: ~20 Hz.

## 7) Limitaciones

Sin magnetómetro, yaw deriva con el tiempo (esperado).
