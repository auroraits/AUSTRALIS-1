using System.IO.Ports;
using GroundTelemetryDashboard.Core.Parsing;
using GroundTelemetryDashboard.Web.Hubs;
using Microsoft.AspNetCore.SignalR;

namespace GroundTelemetryDashboard.Web.Services;

public sealed class SerialTelemetryHostedService : BackgroundService
{
    private readonly SerialConnectionManager _manager;
    private readonly TelemetryState _state;
    private readonly EvidenceRecorder _evidence;
    private readonly IHubContext<TelemetryHub> _hub;
    private readonly ILogger<SerialTelemetryHostedService> _logger;
    private DateTime _lastPush = DateTime.MinValue;

    public SerialTelemetryHostedService(
        SerialConnectionManager manager,
        TelemetryState state,
        EvidenceRecorder evidence,
        IHubContext<TelemetryHub> hub,
        ILogger<SerialTelemetryHostedService> logger)
    {
        _manager = manager;
        _state = state;
        _evidence = evidence;
        _hub = hub;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var status = _manager.GetStatus();
            if (status.State != "REQUESTED" ||
                string.IsNullOrWhiteSpace(status.PortName))
            {
                await Task.Delay(200, stoppingToken);
                continue;
            }

            try
            {
                if (!_manager.MarkOpening(status.Generation))
                {
                    continue;
                }
                status = _manager.GetStatus();
                using var port = new SerialPort(status.PortName, status.Baud)
                {
                    NewLine = "\n",
                    ReadTimeout = 500
                };
                port.Open();
                if (!_manager.MarkOpen(status.Generation))
                {
                    continue;
                }
                status = _manager.GetStatus();
                _evidence.RecordConnection(status, "opened");
                await _hub.Clients.All.SendAsync(
                    "connectionStatus",
                    status,
                    stoppingToken);

                while (!stoppingToken.IsCancellationRequested)
                {
                    var currentStatus = _manager.GetStatus();
                    if (!currentStatus.IsConnected ||
                        currentStatus.Generation != status.Generation)
                    {
                        break;
                    }

                    string line;
                    try
                    {
                        line = port.ReadLine();
                    }
                    catch (TimeoutException)
                    {
                        continue;
                    }

                    line = line.Trim();
                    _state.AddRawLine(line);
                    _evidence.RecordRawLine(line);
                    var shouldPush = ShouldPush();

                    if (shouldPush)
                    {
                        await _hub.Clients.All.SendAsync("rawLine", line, stoppingToken);
                    }

                    if (SerialLineParser.TryParseCsvLine(
                            line,
                            out var sample,
                            out var parseError) &&
                        sample is not null)
                    {
                        var registration = _state.AddSample(sample);
                        _evidence.RecordSample(sample, registration);
                        if (shouldPush)
                        {
                            if (registration.AcceptedForSeries)
                            {
                                await _hub.Clients.All.SendAsync(
                                    "telemetrySample",
                                    sample,
                                    stoppingToken);
                            }
                            await _hub.Clients.All.SendAsync(
                                "telemetryStats",
                                registration.Stats,
                                stoppingToken);
                        }
                    }
                    else if (!line.StartsWith('#') &&
                             !line.StartsWith("version,", StringComparison.OrdinalIgnoreCase))
                    {
                        _evidence.RecordRejectedLine(
                            line,
                            parseError ?? "UNKNOWN_PARSE_ERROR");
                    }
                }

                _evidence.RecordConnection(
                    _manager.GetStatus(),
                    "closed_or_reconfigured");
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Serial loop issue on port {Port}", status.PortName);
                _evidence.Record(
                    "serial_error",
                    new { status, error_type = ex.GetType().Name, ex.Message });
                _evidence.RecordConnection(status, "serial_error");
                _manager.MarkFault(status.Generation, ex.GetType().Name);
                await _hub.Clients.All.SendAsync(
                    "connectionStatus",
                    _manager.GetStatus(),
                    stoppingToken);
                try
                {
                    await _hub.Clients.All.SendAsync("rawLine",
                        $"#ERR Puerto {status.PortName} no disponible: {ex.Message}",
                        stoppingToken);
                }
                catch { /* ignorar si el hub no está listo */ }
                await Task.Delay(1000, stoppingToken);
            }
        }
    }

    private bool ShouldPush()
    {
        var now = DateTime.UtcNow;
        if (now - _lastPush < TimeSpan.FromMilliseconds(50)) return false;
        _lastPush = now;
        return true;
    }
}
