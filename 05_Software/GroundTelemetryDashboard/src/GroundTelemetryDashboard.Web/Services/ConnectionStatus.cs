namespace GroundTelemetryDashboard.Web.Services;

public sealed record ConnectionStatus(
    bool IsConnected,
    string State,
    string? PortName,
    int Baud,
    long Generation,
    string? ErrorCode);
