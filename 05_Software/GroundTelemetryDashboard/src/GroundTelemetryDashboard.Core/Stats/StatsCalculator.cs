using GroundTelemetryDashboard.Core.Models;

namespace GroundTelemetryDashboard.Core.Stats;

public sealed class StatsCalculator
{
    private readonly TimeSpan _window;
    private readonly Queue<(DateTime AtUtc, long Ok, long Lost)> _windowEvents = new();
    private long _okTotal;
    private long _lostTotal;
    private long? _lastSeq;

    public StatsCalculator(TimeSpan? window = null)
    {
        _window = window ?? TimeSpan.FromSeconds(30);
    }

    public TelemetryStats RegisterSample(TelemetrySample sample)
    {
        var now = DateTime.UtcNow;
        var lost = 0L;

        if (_lastSeq.HasValue && sample.Seq > _lastSeq.Value + 1)
        {
            lost = sample.Seq - (_lastSeq.Value + 1);
        }

        _lastSeq = sample.Seq;
        _okTotal += 1;
        _lostTotal += lost;
        _windowEvents.Enqueue((now, 1, lost));
        EvictOld(now);

        var okWindow = _windowEvents.Sum(e => e.Ok);
        var lostWindow = _windowEvents.Sum(e => e.Lost);
        var denom = okWindow + lostWindow;
        var success = denom > 0 ? (double)okWindow / denom : 1.0;

        return new TelemetryStats(_okTotal, _lostTotal, okWindow, lostWindow, success, 1.0 - success, _lastSeq, now);
    }

    private void EvictOld(DateTime now)
    {
        while (_windowEvents.Count > 0 && now - _windowEvents.Peek().AtUtc > _window)
        {
            _windowEvents.Dequeue();
        }
    }
}
