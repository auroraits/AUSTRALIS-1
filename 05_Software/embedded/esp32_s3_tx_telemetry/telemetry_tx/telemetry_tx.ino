#include <Arduino.h>
#include <Wire.h>
#include <RH_ASK.h>
#include <esp_system.h>

#include "../../common/filters/MadgwickAHRS.h"

// -------------------- Hardware pin map --------------------
static const int PIN_3V3 = -1;   // Referencia física: rail 3V3 (no GPIO)
static const int PIN_GND = -1;   // Referencia física: GND (no GPIO)
static const int PIN_SDA = 6;    // ESP32-S3 Super Mini default SDA (ajustable)
static const int PIN_SCL = 7;    // ESP32-S3 Super Mini default SCL (ajustable)
static const int TX_PIN  = 4;   // DATA hacia FS1000A

// 1/4 onda para 433 MHz ~= 17.3 cm (usar alambre rígido y vertical para pruebas)
static const float ANTENNA_LENGTH_CM = 17.3f;

// MPU6050
static const uint8_t MPU_ADDR_DEFAULT = 0x68;
static const uint8_t MPU_ADDR_ALT = 0x69;
static const uint8_t MPU_PWR_MGMT_1 = 0x6B;
static const uint8_t MPU_CONFIG = 0x1A;
static const uint8_t MPU_GYRO_CONFIG = 0x1B;
static const uint8_t MPU_ACCEL_CONFIG = 0x1C;
static const uint8_t MPU_ACCEL_XOUT_H = 0x3B;

static const float ACCEL_LSB_PER_G = 16384.0f;       // +/-2g
static const float GYRO_LSB_PER_DEG_S = 131.0f;      // +/-250 dps
static const float GYRO_DEG_TO_RAD = 0.01745329251994f;

static const float MADGWICK_BETA = 0.12f;
static const uint32_t FILTER_DT_US = 10000UL;        // 100 Hz filtro
static const uint32_t TX_DT_US = 500000UL;           // 2 Hz RF, con margen de airtime
static const uint16_t GYRO_CAL_SAMPLES = 400;

// SENSOR_TO_BODY debe ser una rotacion cartesiana derecha. Identidad es el
// unico baseline permitido hasta medir la orientacion fisica del sensor.
static constexpr int8_t M00 = 1, M01 = 0, M02 = 0;
static constexpr int8_t M10 = 0, M11 = 1, M12 = 0;
static constexpr int8_t M20 = 0, M21 = 0, M22 = 1;
static_assert(
    M00 * (M11 * M22 - M12 * M21)
      - M01 * (M10 * M22 - M12 * M20)
      + M02 * (M10 * M21 - M11 * M20) == 1,
    "SENSOR_TO_BODY must have determinant +1");

// RH_ASK en 2000 bps (OOK/ASK)
RH_ASK ask(2000, 255, TX_PIN, 255, false);
MadgwickAHRS madgwick(MADGWICK_BETA);

#pragma pack(push, 1)
struct TelemetryPacket {
  uint8_t magic;
  uint8_t version;
  uint8_t sensor_type;
  uint8_t quality_flags;
  uint32_t boot_id;
  uint32_t seq;
  uint32_t t_ms;
  int16_t ax;
  int16_t ay;
  int16_t az;
  int16_t gx;
  int16_t gy;
  int16_t gz;
  float q0;
  float q1;
  float q2;
  float q3;
  uint16_t dt_ms;
};
#pragma pack(pop)

static_assert(
    sizeof(TelemetryPacket) <= RH_ASK_MAX_MESSAGE_LEN,
    "TelemetryPacket exceeds RadioHead ASK message limit");
static constexpr uint32_t ASK_ESTIMATED_FRAME_BITS =
    (sizeof(TelemetryPacket) + 7UL) * 12UL + 48UL;
static constexpr uint32_t ASK_ESTIMATED_AIRTIME_US =
    ASK_ESTIMATED_FRAME_BITS * 1000000UL / 2000UL;
static_assert(
    TX_DT_US >= ASK_ESTIMATED_AIRTIME_US * 5UL / 4UL,
    "TX period must retain at least 25 percent airtime margin");

enum : uint8_t {
  PACKET_MAGIC = 'T',
  PACKET_VERSION = 4,
  SENSOR_TYPE_MPU6050 = 1,
  QUALITY_IMU_VALID = 1 << 0,
  QUALITY_ACCEL_REFERENCE_VALID = 1 << 1
};

static uint32_t g_seq = 0;
static uint32_t g_bootId = 0;
static uint32_t g_lastFilterUs = 0;
static uint32_t g_lastTxUs = 0;
static uint32_t g_txBusySkips = 0;
static TelemetryPacket g_lastPacket = {};
static uint8_t g_mpuAddr = MPU_ADDR_DEFAULT;
static float g_gyroBiasX = 0.0f;
static float g_gyroBiasY = 0.0f;
static float g_gyroBiasZ = 0.0f;

static String g_serialCmd;


bool writeMpuRegister(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(g_mpuAddr);
  Wire.write(reg);
  Wire.write(value);
  return Wire.endTransmission() == 0;
}

bool readMpuBurst(uint8_t startReg, uint8_t *buf, size_t len) {
  Wire.beginTransmission(g_mpuAddr);
  Wire.write(startReg);
  if (Wire.endTransmission(false) != 0) return false;
  size_t readLen = Wire.requestFrom((int)g_mpuAddr, (int)len, (int)true);
  if (readLen != len) return false;
  for (size_t i = 0; i < len; ++i) buf[i] = Wire.read();
  return true;
}

bool detectMpuAddress() {
  const uint8_t candidates[2] = { MPU_ADDR_DEFAULT, MPU_ADDR_ALT };
  for (uint8_t i = 0; i < 2; ++i) {
    Wire.beginTransmission(candidates[i]);
    if (Wire.endTransmission() == 0) {
      g_mpuAddr = candidates[i];
      return true;
    }
  }
  return false;
}

bool initMpu6050() {
  if (!detectMpuAddress()) return false;

  if (!writeMpuRegister(MPU_PWR_MGMT_1, 0x00)) return false; // Wake up
  if (!writeMpuRegister(MPU_CONFIG, 0x03)) return false;      // DLPF ~44Hz
  if (!writeMpuRegister(MPU_GYRO_CONFIG, 0x00)) return false; // +-250 dps
  if (!writeMpuRegister(MPU_ACCEL_CONFIG, 0x00)) return false;// +-2g
  delay(100);
  return true;
}

bool readImu(int16_t &ax, int16_t &ay, int16_t &az, int16_t &gx, int16_t &gy, int16_t &gz) {
  uint8_t raw[14];
  if (!readMpuBurst(MPU_ACCEL_XOUT_H, raw, sizeof(raw))) return false;

  ax = (int16_t)((raw[0] << 8) | raw[1]);
  ay = (int16_t)((raw[2] << 8) | raw[3]);
  az = (int16_t)((raw[4] << 8) | raw[5]);
  gx = (int16_t)((raw[8] << 8) | raw[9]);
  gy = (int16_t)((raw[10] << 8) | raw[11]);
  gz = (int16_t)((raw[12] << 8) | raw[13]);
  return true;
}

void mapVectorToBody(float &x, float &y, float &z) {
  const float sensorX = x;
  const float sensorY = y;
  const float sensorZ = z;
  x = M00 * sensorX + M01 * sensorY + M02 * sensorZ;
  y = M10 * sensorX + M11 * sensorY + M12 * sensorZ;
  z = M20 * sensorX + M21 * sensorY + M22 * sensorZ;
}

void mapAxes(float &ax, float &ay, float &az, float &gx, float &gy, float &gz) {
  mapVectorToBody(ax, ay, az);
  mapVectorToBody(gx, gy, gz);
}

void calibrateGyroBias() {
  double sumX = 0.0;
  double sumY = 0.0;
  double sumZ = 0.0;
  uint16_t valid = 0;

  for (uint16_t i = 0; i < GYRO_CAL_SAMPLES; ++i) {
    int16_t axRaw, ayRaw, azRaw, gxRaw, gyRaw, gzRaw;
    if (readImu(axRaw, ayRaw, azRaw, gxRaw, gyRaw, gzRaw)) {
      sumX += (((float)gxRaw) / GYRO_LSB_PER_DEG_S) * GYRO_DEG_TO_RAD;
      sumY += (((float)gyRaw) / GYRO_LSB_PER_DEG_S) * GYRO_DEG_TO_RAD;
      sumZ += (((float)gzRaw) / GYRO_LSB_PER_DEG_S) * GYRO_DEG_TO_RAD;
      valid++;
    }
    delay(5);
  }

  if (valid > 0) {
    g_gyroBiasX = (float)(sumX / valid);
    g_gyroBiasY = (float)(sumY / valid);
    g_gyroBiasZ = (float)(sumZ / valid);
  }
}

void handleSerialCommands() {
  while (Serial.available() > 0) {
    const char c = (char)Serial.read();
    if (c == '\r' || c == '\n') {
      if (g_serialCmd.length() == 0) continue;
      g_serialCmd.trim();
      g_serialCmd.toUpperCase();

      if (g_serialCmd == "CAL" || g_serialCmd == "RECAL") {
        calibrateGyroBias();
        Serial.printf("#CAL,gyro_bias=%.6f,%.6f,%.6f\n", g_gyroBiasX, g_gyroBiasY, g_gyroBiasZ);
      } else if (g_serialCmd == "INFO") {
        Serial.printf("#SENSOR:MPU6050 addr=0x%02X\n", g_mpuAddr);
        Serial.printf("#CAL,gyro_bias=%.6f,%.6f,%.6f\n", g_gyroBiasX, g_gyroBiasY, g_gyroBiasZ);
      }
      g_serialCmd = "";
      continue;
    }

    if (g_serialCmd.length() < 32) {
      g_serialCmd += c;
    }
  }
}

// La transferencia RH_ASK es asincrona. No se usa waitPacketSent(): el filtro
// de 100 Hz debe continuar mientras los bits salen por interrupciones.
enum TxStartResult : uint8_t {
  TX_STARTED,
  TX_BUSY,
  TX_REJECTED
};

TxStartResult tryStartTransmit(const TelemetryPacket &pkt) {
  if (ask.mode() == RHModeTx) {
    return TX_BUSY;
  }
  const uint8_t *payload = reinterpret_cast<const uint8_t *>(&pkt);
  const uint8_t size = sizeof(TelemetryPacket);

  // send() only starts the interrupt-driven transfer. Channel loss is measured
  // at RX with boot_id/sequence gaps; it is not observable from this return.
  return ask.send(payload, size) ? TX_STARTED : TX_REJECTED;
}

void setup() {
  Serial.begin(115200);
  const unsigned long serialWaitStart = millis();
//  while (!Serial && (millis() - serialWaitStart) < 2000UL) {
    delay(2000);
//  }

  Serial.println("Telemetry TX starting...");

  g_bootId = esp_random();

  Wire.begin(PIN_SDA, PIN_SCL);

  if (!ask.init()) {
    Serial.println("ERR: RH_ASK init fail");
  }

  if (!initMpu6050()) {
    Serial.println("ERR: MPU6050 init fail");
  }

  calibrateGyroBias();

  g_lastFilterUs = micros();
  g_lastTxUs = g_lastFilterUs;

  Serial.printf("#SENSOR:MPU6050 addr=0x%02X\n", g_mpuAddr);
  Serial.printf("#BOOT,id=%08lX packet_version=%u rf_rate_hz=2\n",
                (unsigned long)g_bootId,
                PACKET_VERSION);
  Serial.printf("#CAL,gyro_bias=%.6f,%.6f,%.6f\n", g_gyroBiasX, g_gyroBiasY, g_gyroBiasZ);
  Serial.println("Telemetry TX ready");
}

void loop() {
  handleSerialCommands();

  const uint32_t nowUs = micros();
  if ((uint32_t)(nowUs - g_lastFilterUs) < FILTER_DT_US) {
    delay(1);
    return;
  }

  // FRAME NOTE: pkt.ax/ay/az/gx/gy/gz contienen datos en frame SENSOR (raw ADC,
  // sin aplicar SENSOR_TO_BODY). El quaternion pkt.q0..q3 está en frame BODY
  // (con la matriz SENSOR_TO_BODY aplicada antes de Madgwick).
  // El dashboard grafica IMU en sensor frame y orientación en body frame.
  // Esto es intencional: los raw IMU sirven para diagnóstico de hardware;
  // el quaternion representa la actitud del cuerpo del satélite.
  TelemetryPacket pkt;
  pkt.seq = g_seq;
  pkt.t_ms = millis();

  if (!readImu(pkt.ax, pkt.ay, pkt.az, pkt.gx, pkt.gy, pkt.gz)) {
    g_lastFilterUs = nowUs;
    return;
  }

  const float dtSec = (float)((uint32_t)(nowUs - g_lastFilterUs)) / 1000000.0f;
  const float ax_g = ((float)pkt.ax) / ACCEL_LSB_PER_G;
  const float ay_g = ((float)pkt.ay) / ACCEL_LSB_PER_G;
  const float az_g = ((float)pkt.az) / ACCEL_LSB_PER_G;
  const float gx_rad = (((float)pkt.gx) / GYRO_LSB_PER_DEG_S) * GYRO_DEG_TO_RAD;
  const float gy_rad = (((float)pkt.gy) / GYRO_LSB_PER_DEG_S) * GYRO_DEG_TO_RAD;
  const float gz_rad = (((float)pkt.gz) / GYRO_LSB_PER_DEG_S) * GYRO_DEG_TO_RAD;

  float axBody = ax_g;
  float ayBody = ay_g;
  float azBody = az_g;
  float gxBody = gx_rad - g_gyroBiasX;
  float gyBody = gy_rad - g_gyroBiasY;
  float gzBody = gz_rad - g_gyroBiasZ;
  mapAxes(axBody, ayBody, azBody, gxBody, gyBody, gzBody);

  madgwick.updateIMU(gxBody, gyBody, gzBody, axBody, ayBody, azBody, dtSec);
  pkt.magic = PACKET_MAGIC;
  pkt.version = PACKET_VERSION;
  pkt.sensor_type = SENSOR_TYPE_MPU6050;
  pkt.quality_flags = QUALITY_IMU_VALID;
  const float accelNormG = sqrtf(axBody * axBody + ayBody * ayBody + azBody * azBody);
  if (accelNormG >= 0.5f && accelNormG <= 1.5f) {
    pkt.quality_flags |= QUALITY_ACCEL_REFERENCE_VALID;
  }
  pkt.boot_id = g_bootId;
  pkt.q0 = madgwick.q0();
  pkt.q1 = madgwick.q1();
  pkt.q2 = madgwick.q2();
  pkt.q3 = madgwick.q3();
  const float qNorm = sqrtf(pkt.q0 * pkt.q0 + pkt.q1 * pkt.q1 + pkt.q2 * pkt.q2 + pkt.q3 * pkt.q3);
  if (qNorm > 1e-6f) {
    pkt.q0 /= qNorm;
    pkt.q1 /= qNorm;
    pkt.q2 /= qNorm;
    pkt.q3 /= qNorm;
  }
  pkt.dt_ms = (uint16_t)(dtSec * 1000.0f);

  g_lastPacket = pkt;
  g_lastFilterUs = nowUs;

  if ((uint32_t)(nowUs - g_lastTxUs) < TX_DT_US) {
    return;
  }

  g_lastPacket.seq = g_seq;
  const TxStartResult txResult = tryStartTransmit(g_lastPacket);
  if (txResult == TX_BUSY) {
    g_txBusySkips++;
    return;
  }

  g_lastTxUs = nowUs;
  if (txResult == TX_STARTED) {
    g_seq++;
  }
  Serial.printf("TX boot=%08lX seq=%lu status=%s busy_skips=%lu q=[%.3f %.3f %.3f %.3f] dt=%ums\n",
                (unsigned long)g_lastPacket.boot_id,
                (unsigned long)g_lastPacket.seq,
                txResult == TX_STARTED ? "started" : "rejected_local",
                (unsigned long)g_txBusySkips,
                g_lastPacket.q0,
                g_lastPacket.q1,
                g_lastPacket.q2,
                g_lastPacket.q3,
                g_lastPacket.dt_ms);
}
