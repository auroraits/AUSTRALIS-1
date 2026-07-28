namespace GroundTelemetryDashboard.Core.Models;

public sealed record TelemetryStats(
    long OkCount,
    long LostCountEstimated,
    long DuplicateCount,
    long OutOfOrderCount,
    long SessionCount,
    long OkCountWindow,
    long LostCountWindow,
    long DuplicateCountWindow,
    long OutOfOrderCountWindow,
    double SuccessRateWindow,
    double PerWindow,
    long? LastSeq,
    long? CurrentBootId,
    DateTime LastUpdateUtc);
