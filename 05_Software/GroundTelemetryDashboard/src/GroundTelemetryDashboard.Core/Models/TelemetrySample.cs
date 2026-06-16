namespace GroundTelemetryDashboard.Core.Models;

public sealed record TelemetrySample(
    long Seq,
    long TMs,
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
    public bool HasQuaternion => !(Q0 == 0 && Q1 == 0 && Q2 == 0 && Q3 == 0);
}
