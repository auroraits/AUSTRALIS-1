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
        CurrentStats = new TelemetryStats(0, 0, 0, 0, 1, 0, null, DateTime.UtcNow);
    }

    public TelemetryStats CurrentStats { get; private set; }

    public TelemetryStats AddSample(TelemetrySample sample)
    {
        lock (_sync)
        {
            _samples.Add(sample);
            CurrentStats = _stats.RegisterSample(sample);
            return CurrentStats;
        }
    }

    public void AddRawLine(string line)
    {
        _rawLines.Add(line);
    }
}
