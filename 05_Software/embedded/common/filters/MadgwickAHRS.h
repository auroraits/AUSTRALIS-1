#pragma once

#include <Arduino.h>
#include <math.h>

// Minimal Madgwick IMU implementation (gyro + accel, no magnetometer).
// Quaternion convention: q0=w, q1=x, q2=y, q3=z.
class MadgwickAHRS {
 public:
  explicit MadgwickAHRS(float beta = 0.1f)
      : beta_(beta), q0_(1.0f), q1_(0.0f), q2_(0.0f), q3_(0.0f) {}

  void setBeta(float beta) { beta_ = beta; }

  void updateIMU(float gx, float gy, float gz, float ax, float ay, float az, float dtSeconds) {
    if (dtSeconds <= 0.0f) {
      return;
    }

    float qDot1 = 0.5f * (-q1_ * gx - q2_ * gy - q3_ * gz);
    float qDot2 = 0.5f * (q0_ * gx + q2_ * gz - q3_ * gy);
    float qDot3 = 0.5f * (q0_ * gy - q1_ * gz + q3_ * gx);
    float qDot4 = 0.5f * (q0_ * gz + q1_ * gy - q2_ * gx);

    const float accNorm = sqrtf(ax * ax + ay * ay + az * az);
    if (accNorm > 1e-6f) {
      ax /= accNorm;
      ay /= accNorm;
      az /= accNorm;

      const float twoQ0 = 2.0f * q0_;
      const float twoQ1 = 2.0f * q1_;
      const float twoQ2 = 2.0f * q2_;
      const float twoQ3 = 2.0f * q3_;
      const float fourQ0 = 4.0f * q0_;
      const float fourQ1 = 4.0f * q1_;
      const float fourQ2 = 4.0f * q2_;
      const float eightQ1 = 8.0f * q1_;
      const float eightQ2 = 8.0f * q2_;
      const float q0q0 = q0_ * q0_;
      const float q1q1 = q1_ * q1_;
      const float q2q2 = q2_ * q2_;
      const float q3q3 = q3_ * q3_;

      float s0 = fourQ0 * q2q2 + twoQ2 * ax + fourQ0 * q1q1 - twoQ1 * ay;
      float s1 = fourQ1 * q3q3 - twoQ3 * ax + 4.0f * q0q0 * q1_ - twoQ0 * ay - fourQ1 + eightQ1 * q1q1 + eightQ1 * q2q2 + fourQ1 * az;
      float s2 = 4.0f * q0q0 * q2_ + twoQ0 * ax + fourQ2 * q3q3 - twoQ3 * ay - fourQ2 + eightQ2 * q1q1 + eightQ2 * q2q2 + fourQ2 * az;
      float s3 = 4.0f * q1q1 * q3_ - twoQ1 * ax + 4.0f * q2q2 * q3_ - twoQ2 * ay;

      const float sNorm = sqrtf(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3);
      if (sNorm > 1e-6f) {
        s0 /= sNorm;
        s1 /= sNorm;
        s2 /= sNorm;
        s3 /= sNorm;

        qDot1 -= beta_ * s0;
        qDot2 -= beta_ * s1;
        qDot3 -= beta_ * s2;
        qDot4 -= beta_ * s3;
      }
    }

    q0_ += qDot1 * dtSeconds;
    q1_ += qDot2 * dtSeconds;
    q2_ += qDot3 * dtSeconds;
    q3_ += qDot4 * dtSeconds;

    const float qNorm = sqrtf(q0_ * q0_ + q1_ * q1_ + q2_ * q2_ + q3_ * q3_);
    if (qNorm > 1e-6f) {
      q0_ /= qNorm;
      q1_ /= qNorm;
      q2_ /= qNorm;
      q3_ /= qNorm;
    }
  }

  float q0() const { return q0_; }
  float q1() const { return q1_; }
  float q2() const { return q2_; }
  float q3() const { return q3_; }

 private:
  float beta_;
  float q0_;
  float q1_;
  float q2_;
  float q3_;
};
