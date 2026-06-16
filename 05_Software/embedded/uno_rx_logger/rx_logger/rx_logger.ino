#include <Arduino.h>
#include <RH_ASK.h>
#include <string.h>
#include <math.h>

// -------------------- Hardware pin map --------------------
static const uint8_t RX_PIN = 11; // DATA desde receptor RX433 al D11
static const uint8_t TX_PIN = 12; // No usado en logger, requerido por constructor
static const uint8_t PTT_PIN = 10;

RH_ASK ask(2000, RX_PIN, TX_PIN, PTT_PIN, false);

#pragma pack(push, 1)
struct TelemetryPacketV1 {
  uint32_t seq;
  uint32_t t_ms;
  int16_t ax;
  int16_t ay;
  int16_t az;
  int16_t gx;
  int16_t gy;
  int16_t gz;
};

struct TelemetryPacketV2 {
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

struct TelemetryPacketV3 {
  uint8_t magic;
  uint8_t version;
  uint8_t sensor_type;
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

static const uint8_t PACKET_MAGIC = 'T';
static const uint8_t PACKET_VERSION_3 = 3;
static const bool ENABLE_DEBUG_RPY = false;


uint32_t packetsOk = 0;
uint32_t packetsDropped = 0;
uint32_t packetsLost = 0;
uint32_t lastSeq = 0;
bool hasLastSeq = false;
unsigned long lastSummaryMs = 0;

void initRadio() {
  if (!ask.init()) {
    Serial.println("ERR,RH_ASK_INIT");
  }
}

void printCsvV1AsExtended(const TelemetryPacketV1 &pkt) {
  Serial.print(pkt.seq); Serial.print(',');
  Serial.print(pkt.t_ms); Serial.print(',');
  Serial.print(pkt.ax); Serial.print(',');
  Serial.print(pkt.ay); Serial.print(',');
  Serial.print(pkt.az); Serial.print(',');
  Serial.print(pkt.gx); Serial.print(',');
  Serial.print(pkt.gy); Serial.print(',');
  Serial.print(pkt.gz); Serial.print(',');
  Serial.print(1.0f, 6); Serial.print(',');
  Serial.print(0.0f, 6); Serial.print(',');
  Serial.print(0.0f, 6); Serial.print(',');
  Serial.println(0.0f, 6);
}

void printCsvV2(const TelemetryPacketV2 &pkt) {
  Serial.print(pkt.seq); Serial.print(',');
  Serial.print(pkt.t_ms); Serial.print(',');
  Serial.print(pkt.ax); Serial.print(',');
  Serial.print(pkt.ay); Serial.print(',');
  Serial.print(pkt.az); Serial.print(',');
  Serial.print(pkt.gx); Serial.print(',');
  Serial.print(pkt.gy); Serial.print(',');
  Serial.print(pkt.gz); Serial.print(',');
  Serial.print(pkt.q0, 6); Serial.print(',');
  Serial.print(pkt.q1, 6); Serial.print(',');
  Serial.print(pkt.q2, 6); Serial.print(',');
  Serial.println(pkt.q3, 6);
  printDebugRpy(pkt.q0, pkt.q1, pkt.q2, pkt.q3);
}

void printCsvV3(const TelemetryPacketV3 &pkt) {
  Serial.print(pkt.seq); Serial.print(',');
  Serial.print(pkt.t_ms); Serial.print(',');
  Serial.print(pkt.ax); Serial.print(',');
  Serial.print(pkt.ay); Serial.print(',');
  Serial.print(pkt.az); Serial.print(',');
  Serial.print(pkt.gx); Serial.print(',');
  Serial.print(pkt.gy); Serial.print(',');
  Serial.print(pkt.gz); Serial.print(',');
  Serial.print(pkt.q0, 6); Serial.print(',');
  Serial.print(pkt.q1, 6); Serial.print(',');
  Serial.print(pkt.q2, 6); Serial.print(',');
  Serial.println(pkt.q3, 6);
  printDebugRpy(pkt.q0, pkt.q1, pkt.q2, pkt.q3);
}

void printDebugRpy(float qw, float qx, float qy, float qz) {
  if (!ENABLE_DEBUG_RPY) return;
  const float sinr_cosp = 2.0f * (qw * qx + qy * qz);
  const float cosr_cosp = 1.0f - 2.0f * (qx * qx + qy * qy);
  const float roll = atan2(sinr_cosp, cosr_cosp);

  const float sinp = 2.0f * (qw * qy - qz * qx);
  float pitch;
  if (fabs(sinp) >= 1.0f) pitch = copysign(1.5707963f, sinp);
  else pitch = asin(sinp);

  const float siny_cosp = 2.0f * (qw * qz + qx * qy);
  const float cosy_cosp = 1.0f - 2.0f * (qy * qy + qz * qz);
  const float yaw = atan2(siny_cosp, cosy_cosp);

  Serial.print("#RPY,roll="); Serial.print(roll * 57.29578f, 2);
  Serial.print(",pitch="); Serial.print(pitch * 57.29578f, 2);
  Serial.print(",yaw="); Serial.println(yaw * 57.29578f, 2);
}

void updateCounters(uint32_t seq) {
  packetsOk++;
  if (hasLastSeq && seq > (lastSeq + 1)) {
    packetsLost += (seq - lastSeq - 1);
  }
  lastSeq = seq;
  hasLastSeq = true;
}

void printSummaryIfNeeded() {
  unsigned long now = millis();
  if (now - lastSummaryMs >= 30000UL) {
    Serial.print("#SUMMARY,ok="); Serial.print(packetsOk);
    Serial.print(",dropped="); Serial.print(packetsDropped);
    Serial.print(",lost="); Serial.println(packetsLost);
    lastSummaryMs = now;
  }
}

void setup() {
  Serial.begin(115200);
  initRadio();
  Serial.println("seq,t_ms,ax,ay,az,gx,gy,gz,q0,q1,q2,q3");
}

void loop() {
  uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);

  if (ask.available()) {
    if (ask.recv(buf, &len)) { // CRC validado internamente por RadioHead
      if (len == sizeof(TelemetryPacketV2)) {
        TelemetryPacketV2 pkt;
        memcpy(&pkt, buf, sizeof(pkt));
        updateCounters(pkt.seq);
        printCsvV2(pkt);
      } else if (len == sizeof(TelemetryPacketV3)) {
        TelemetryPacketV3 pkt;
        memcpy(&pkt, buf, sizeof(pkt));
        if (pkt.magic == PACKET_MAGIC && pkt.version == PACKET_VERSION_3) {
          updateCounters(pkt.seq);
          printCsvV3(pkt);
        } else {
          packetsDropped++;
        }
      } else if (len == sizeof(TelemetryPacketV1)) {
        TelemetryPacketV1 pkt;
        memcpy(&pkt, buf, sizeof(pkt));
        updateCounters(pkt.seq);
        printCsvV1AsExtended(pkt);
      } else {
        packetsDropped++;
      }
    } else {
      packetsDropped++;
    }
  }

  printSummaryIfNeeded();
}
