namespace GroundTelemetryDashboard.Core.Models;

public sealed record TelemetrySample(
    int ProtocolVersion,
    long BootId,
    long Seq,
    long TMs,
    int SensorType,
    int QualityFlags,
    long DtMs,
    double Ax,
    double Ay,
    double Az,
    double Gx,
    double Gy,
    double Gz,
    double Q0,
    double Q1,
    double Q2,
    double Q3,
    DateTime ReceivedAtUtc,
    long ReceivedMonotonicTicks,
    string TimeQuality)
{
    public const int SensorTypeMpu6050 = 1;
    public const int QualityImuValid = 1 << 0;
    public const int QualityAccelReferenceValid = 1 << 1;
    public const int KnownQualityMask =
        QualityImuValid | QualityAccelReferenceValid;

    public bool HasQuaternion => QuaternionNormSquared > 0;

    public double QuaternionNormSquared =>
        Q0 * Q0 + Q1 * Q1 + Q2 * Q2 + Q3 * Q3;

    public string SessionId => ProtocolVersion >= 4
        ? $"v{ProtocolVersion}-{BootId:X8}"
        : $"legacy-v{ProtocolVersion}";

    public string ScientificValidationCode
    {
        get
        {
            if (ProtocolVersion < 4)
            {
                return "LEGACY_PROTOCOL";
            }
            if (SensorType != SensorTypeMpu6050)
            {
                return "UNKNOWN_SENSOR_TYPE";
            }
            if ((QualityFlags & ~KnownQualityMask) != 0)
            {
                return "UNKNOWN_QUALITY_FLAGS";
            }
            if ((QualityFlags & QualityImuValid) == 0)
            {
                return "IMU_NOT_VALID";
            }
            if (DtMs is < 1 or > 1000)
            {
                return "DT_MS_RANGE";
            }
            if (QuaternionNormSquared is < 0.81 or > 1.21)
            {
                return "QUATERNION_NORM";
            }
            return "VALID";
        }
    }

    public bool IsScientificQuality =>
        ScientificValidationCode == "VALID";

    public string MeasurementClass => IsScientificQuality
        ? "BENCH_SENSOR_VALID_UNCALIBRATED"
        : "DIAGNOSTIC_ONLY";
}
