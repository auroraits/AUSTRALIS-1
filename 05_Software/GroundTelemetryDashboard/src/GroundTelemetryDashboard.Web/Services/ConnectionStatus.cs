namespace GroundTelemetryDashboard.Web.Services;

public sealed record ConnectionStatus(bool IsConnected, string? PortName, int Baud);
