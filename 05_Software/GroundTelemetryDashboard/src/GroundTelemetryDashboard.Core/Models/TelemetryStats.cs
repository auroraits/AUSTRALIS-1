namespace GroundTelemetryDashboard.Core.Models;

public sealed record TelemetryStats(
    long OkCount,
    long LostCountEstimado,
    long OkCountWindow,
    long LostCountWindow,
    double SuccessRateWindow,
    double PerWindow,
    long? LastSeq,
    DateTime LastUpdateUtc);
