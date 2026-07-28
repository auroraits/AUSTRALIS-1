using GroundTelemetryDashboard.Core.Collections;
using GroundTelemetryDashboard.Core.Models;
using GroundTelemetryDashboard.Core.Stats;

namespace GroundTelemetryDashboard.Web.Services;

public sealed class TelemetryState
{
    private readonly RingBuffer<TelemetrySample> _samples;
    private readonly RingBuffer<string> _rawLines;
    private readonly StatsCalculator _stats;
    private readonly object _sync = new();

    public TelemetryState(IConfiguration configuration)
    {
        var bufferSize = configuration.GetValue<int?>("Serial:BufferSize") ?? 2000;
        var window = configuration.GetValue<int?>("Serial:SuccessWindowSeconds") ?? 30;
        _samples = new RingBuffer<TelemetrySample>(bufferSize);
        _rawLines = new RingBuffer<string>(bufferSize);
        _stats = new StatsCalculator(TimeSpan.FromSeconds(window));
        CurrentStats = new TelemetryStats(
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
            null, null,
            0, 0, 0, 0, null,
            null, null, DateTime.UtcNow);
    }

    public TelemetryStats CurrentStats { get; private set; }

    public TelemetryRegistration AddSample(TelemetrySample sample)
    {
        lock (_sync)
        {
            var registration = _stats.RegisterSampleDetailed(sample);
            if (registration.AcceptedForSeries)
            {
                _samples.Add(sample);
            }
            CurrentStats = registration.Stats;
            return registration;
        }
    }

    public void AddRawLine(string line)
    {
        lock (_sync)
        {
            _rawLines.Add(line);
        }
    }
}
