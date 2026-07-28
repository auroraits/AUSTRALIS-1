using GroundTelemetryDashboard.Core.Models;

namespace GroundTelemetryDashboard.Core.Stats;

public sealed class StatsCalculator
{
    private readonly TimeSpan _window;
    private readonly Queue<WindowEvent> _windowEvents = new();
    private long _okTotal;
    private long _lostTotal;
    private long _duplicateTotal;
    private long _outOfOrderTotal;
    private long _sessionCount;
    private long? _lastSeq;
    private long? _lastTMs;
    private long? _currentBootId;
    private int? _currentProtocolVersion;

    public StatsCalculator(TimeSpan? window = null)
    {
        _window = window ?? TimeSpan.FromSeconds(30);
    }

    public TelemetryStats RegisterSample(TelemetrySample sample)
    {
        var now = sample.ReceivedAtUtc;
        var ok = 0L;
        var lost = 0L;
        var duplicate = 0L;
        var outOfOrder = 0L;

        if (StartsNewSession(sample))
        {
            StartSession(sample);
        }

        if (!_lastSeq.HasValue)
        {
            ok = 1;
            _lastSeq = sample.Seq;
            _lastTMs = sample.TMs;
        }
        else
        {
            var current = unchecked((uint)sample.Seq);
            var previous = unchecked((uint)_lastSeq.Value);
            var delta = unchecked(current - previous);
            if (delta == 0)
            {
                duplicate = 1;
            }
            else if (delta < 0x80000000U)
            {
                ok = 1;
                lost = delta - 1;
                _lastSeq = sample.Seq;
                _lastTMs = sample.TMs;
            }
            else
            {
                outOfOrder = 1;
            }
        }

        _okTotal += ok;
        _lostTotal += lost;
        _duplicateTotal += duplicate;
        _outOfOrderTotal += outOfOrder;
        _windowEvents.Enqueue(new WindowEvent(now, ok, lost, duplicate, outOfOrder));
        EvictOld(now);

        var okWindow = _windowEvents.Sum(e => e.Ok);
        var lostWindow = _windowEvents.Sum(e => e.Lost);
        var duplicateWindow = _windowEvents.Sum(e => e.Duplicate);
        var outOfOrderWindow = _windowEvents.Sum(e => e.OutOfOrder);
        var denominator = okWindow + lostWindow;
        var success = denominator > 0 ? (double)okWindow / denominator : 1.0;

        return new TelemetryStats(
            _okTotal,
            _lostTotal,
            _duplicateTotal,
            _outOfOrderTotal,
            _sessionCount,
            okWindow,
            lostWindow,
            duplicateWindow,
            outOfOrderWindow,
            success,
            1.0 - success,
            _lastSeq,
            _currentBootId,
            now);
    }

    private bool StartsNewSession(TelemetrySample sample)
    {
        if (!_currentProtocolVersion.HasValue)
        {
            return true;
        }

        if (sample.ProtocolVersion >= 4)
        {
            return _currentProtocolVersion.Value < 4 || sample.BootId != _currentBootId;
        }

        if (_currentProtocolVersion.Value >= 4)
        {
            return true;
        }

        // Legacy packets have no boot ID. A simultaneous large time/counter
        // rollback is the explicit receiver-side reboot heuristic.
        return _lastTMs.HasValue &&
               _lastSeq.HasValue &&
               sample.TMs + 1000 < _lastTMs.Value &&
               sample.Seq + 16 < _lastSeq.Value;
    }

    private void StartSession(TelemetrySample sample)
    {
        _sessionCount++;
        _currentProtocolVersion = sample.ProtocolVersion;
        _currentBootId = sample.BootId;
        _lastSeq = null;
        _lastTMs = null;
        _windowEvents.Clear();
    }

    private void EvictOld(DateTime now)
    {
        while (_windowEvents.Count > 0 &&
               now - _windowEvents.Peek().AtUtc > _window)
        {
            _windowEvents.Dequeue();
        }
    }

    private sealed record WindowEvent(
        DateTime AtUtc,
        long Ok,
        long Lost,
        long Duplicate,
        long OutOfOrder);
}
