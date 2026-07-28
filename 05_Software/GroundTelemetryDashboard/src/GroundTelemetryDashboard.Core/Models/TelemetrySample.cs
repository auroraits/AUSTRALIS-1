namespace GroundTelemetryDashboard.Core.Models;

public sealed record TelemetrySample(
    int ProtocolVersion,
    long BootId,
    long Seq,
    long TMs,
    int QualityFlags,
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
    DateTime ReceivedAtUtc)
{
    public bool HasQuaternion => QuaternionNormSquared > 0;

    public double QuaternionNormSquared =>
        Q0 * Q0 + Q1 * Q1 + Q2 * Q2 + Q3 * Q3;

    public string SessionId => ProtocolVersion >= 4
        ? $"v{ProtocolVersion}-{BootId:X8}"
        : $"legacy-v{ProtocolVersion}";
}
