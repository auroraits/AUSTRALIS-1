namespace GroundTelemetryDashboard.Core.Models;

public sealed record TelemetryStats(
    long LinkReceivedCount,
    long LinkLostCountEstimated,
    long DuplicateCount,
    long OutOfOrderCount,
    long TimeRegressionCount,
    long SessionCount,
    long LinkReceivedCountWindow,
    long LinkLostCountWindow,
    long DuplicateCountWindow,
    long OutOfOrderCountWindow,
    long TimeRegressionCountWindow,
    double? LinkSuccessRateWindow,
    double? LinkPerWindow,
    long ScientificAdmittedCount,
    long ScientificRejectedCount,
    long ScientificAdmittedCountWindow,
    long ScientificRejectedCountWindow,
    double? ScientificYieldWindow,
    long? LastSeq,
    long? CurrentBootId,
    DateTime LastUpdateUtc);

public sealed record TelemetryRegistration(
    TelemetryStats Stats,
    string LinkDisposition,
    string ScientificDisposition,
    bool AcceptedForSeries);
