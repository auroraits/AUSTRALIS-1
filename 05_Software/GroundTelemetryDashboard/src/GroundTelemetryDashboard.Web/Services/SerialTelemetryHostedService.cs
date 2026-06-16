using System.IO.Ports;
using GroundTelemetryDashboard.Core.Parsing;
using GroundTelemetryDashboard.Web.Hubs;
using Microsoft.AspNetCore.SignalR;

namespace GroundTelemetryDashboard.Web.Services;

public sealed class SerialTelemetryHostedService : BackgroundService
{
    private readonly SerialConnectionManager _manager;
    private readonly TelemetryState _state;
    private readonly IHubContext<TelemetryHub> _hub;
    private readonly ILogger<SerialTelemetryHostedService> _logger;
    private DateTime _lastPush = DateTime.MinValue;

    public SerialTelemetryHostedService(
        SerialConnectionManager manager,
        TelemetryState state,
        IHubContext<TelemetryHub> hub,
        ILogger<SerialTelemetryHostedService> logger)
    {
        _manager = manager;
        _state = state;
        _hub = hub;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var status = _manager.GetStatus();
            if (!status.IsConnected || string.IsNullOrWhiteSpace(status.PortName))
            {
                await Task.Delay(200, stoppingToken);
                continue;
            }

            try
            {
                using var port = new SerialPort(status.PortName, status.Baud)
                {
                    NewLine = "\n",
                    ReadTimeout = 500
                };
                port.Open();

                while (!stoppingToken.IsCancellationRequested && _manager.GetStatus().IsConnected)
                {
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
                    var shouldPush = ShouldPush();

                    if (shouldPush)
                    {
                        await _hub.Clients.All.SendAsync("rawLine", line, stoppingToken);
                    }

                    if (SerialLineParser.TryParseCsvLine(line, out var sample) && sample is not null)
                    {
                        var stats = _state.AddSample(sample);
                        if (shouldPush)
                        {
                            await _hub.Clients.All.SendAsync("telemetrySample", sample, stoppingToken);
                            await _hub.Clients.All.SendAsync("telemetryStats", stats, stoppingToken);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Serial loop issue on port {Port}", status.PortName);
                _manager.Disconnect();
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
